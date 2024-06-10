from tcia_utils import nbia
from flask import Blueprint, jsonify, send_file, abort
import os
import pydicom
from pydicom.pixel_data_handlers.util import apply_voi_lut
import numpy as np
from PIL import Image
from io import BytesIO
from .utils import *

images_bp = Blueprint('images', __name__)

@images_bp.route('/<patientId>/details', methods=['GET'])
def get_images_details_by_patientId(patientId):
        dst_path = get_patient_image_folder(patientId)
        create_if_not_exist_folder(dst_path)

        image_uids = get_image_uids(patientId)
        nbia.downloadSeries(image_uids, input_type="list", format="df")
        save_client_photos_in_cache(dst_path)

        filenames = [f for f in os.listdir(dst_path) if os.path.isfile(os.path.join(dst_path, f))]
        return jsonify({"filenames": filenames}), 200


@images_bp.route('/<patientId>/<filename>', methods=['GET'])
def get_images_by_patient(patientId, filename):
        # TODO1: Store in local database SQLite
        image_folder = get_patient_image_folder(patientId)
        file_path = os.path.join(image_folder, filename)

        if not os.path.exists(file_path):
            return abort(404, description="Image not found")
        
        dicom = pydicom.dcmread(file_path)
        image = apply_voi_lut(dicom.pixel_array, dicom)
        
        image = image - np.min(image)
        image = (image / np.max(image) * 255).astype(np.uint8)
        
        pil_image = Image.fromarray(image)
        
        img_io = BytesIO()
        pil_image.save(img_io, 'JPEG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/jpeg'), 200
