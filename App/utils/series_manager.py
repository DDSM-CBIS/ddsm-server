import pandas as pd
from pathlib import Path
import requests
import os
import pydicom
from pydicom.pixel_data_handlers.util import apply_voi_lut
import numpy as np
from PIL import Image
from io import BytesIO

class SeriesManager:
    def __init__(self):
        self.series: pd.DataFrame = None
        self.config = None

    def set_config(self, config):
        self.config = config

    def get_base_url(self, route: str, params: list = []) -> str:  
        base = self.config["base_url"]
        
        if route == "getSeries" and len(params) == 1:
            return base + "getSeries?Collection=" + params[0]
        elif route == "getSingleImage" and len(params) == 2:
            return base + "getSingleImage?SeriesInstanceUID=" + params[0] + "&SOPInstanceUID=" + params[1]
        elif route == "getSOPInstanceUIDs" and len(params) == 1:
            return base + "getSOPInstanceUIDs?SeriesInstanceUID=" + params[0]
        elif route == "getImage" and len(params) == 1:
            return base + "getImage?NewFileNames=Yes&SeriesInstanceUID=" + params[0]
        return base
        
    def load_series(self):
        base_url = self.get_base_url(route="getSeries", params=[self.config["series_name"]])
        response = requests.get(base_url, timeout=30)
        self.series = pd.DataFrame(response.json())
    
    def get_series(self, image_format: str):
        if image_format == "all":
            return self.series
        return self.series[self.series["SeriesDescription"].str.contains(image_format, case=False)]
    
    def get_patient_series_instance_uids(self, patient_id: str, image_format: str):
        patients_series = self.get_series(image_format)
        patient_series = patients_series[patients_series["PatientID"].str.contains(patient_id)]
        return list(patient_series["SeriesInstanceUID"])
    
    def get_sop_uids(self, uid: str):
        response = requests.get(self.get_base_url(route="getSOPInstanceUIDs", params=[uid]), timeout=10)
        if not response or response.status_code != 200:
            return None
        
        response = response.json()
        result = []
        for item in response:
            result.append(item["SOPInstanceUID"])
        return result
    
    def get_image_metadata(self, uid: str):
        patient_id = self.series[self.series["SeriesInstanceUID"] == uid]["PatientID"].values[0]
        parts = patient_id.split("_")

        if len(parts) != 5:
            return "Invalid patient ID format. Expected format: <class>_<patient_id>_<left_or_right_breast>_<image_view>", 400
        
        sop_uids = self.get_sop_uids(uid)
        if sop_uids is None:
            return "No SOP UID found for the given series instance UID", 404
        
        result = {
            "class": parts[0],
            "leftOrRightBreast": parts[3],
            "imageView": parts[4],
            "sopUIDs": sop_uids
        }
        return result
    
    def get_image_by_uids(self, uid: str, sop_uid: str):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        image_folder = os.path.join(root_dir, '..', "..",'cache', 'images', f'{uid}')
        image_path = os.path.join(image_folder, f"{sop_uid}.dcm")

        if not os.path.exists(image_folder):
            path = Path(image_folder)
            path.mkdir(parents=True)

        if not os.path.exists(image_path):
            base_url = self.get_base_url(route="getSingleImage", params=[uid, sop_uid])
            response = requests.get(base_url, stream=True, timeout=30)
            
            if response.status_code != 200:
                return "Image not found", 404
            
            with open(image_path, 'wb') as file:
                file.write(response.content)

        dcm = pydicom.dcmread(image_path)
        image = apply_voi_lut(dcm.pixel_array, dcm)

        image = image - np.min(image)
        image = (image / np.max(image) * 255).astype(np.uint8)

        pil_image = Image.fromarray(image)

        img_io = BytesIO()
        pil_image.save(img_io, 'JPEG')
        img_io.seek(0)
        return img_io

    def start(self, config):
        self.set_config(config)
        self.load_series()