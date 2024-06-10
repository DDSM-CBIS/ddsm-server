from pathlib import Path
from data.data import series_df
import os

def get_patient_image_folder(patientId):
   return os.path.join(os.path.dirname(__file__), '..', '..', 'cache', f'{patientId}')

def delete_files_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)


def get_image_uids(patient_id):
    return list(series_df[series_df['PatientID']
                       .str
                       .contains(patient_id)]
                       .SeriesInstanceUID)


def create_if_not_exist_folder(file_path: str):
    if not os.path.exists(file_path):
        path = Path(file_path)
        path.mkdir(parents=True)

def get_all_files_under_dir(directory_path):
    files_ret = []
    for root, dirs, files in os.walk(directory_path):

        for file in files:
            if file == 'LICENSE':
                continue
            file_path = os.path.join(root, file)
            dir_name = os.path.basename(root)
            PatientID = series_df[series_df.SeriesInstanceUID == dir_name]['PatientID'].iat[0]
            new_file_name = f"{PatientID}_{file[2:]}"

            new_file_path = os.path.join(root, new_file_name)
            if os.path.isfile(new_file_path):
                continue
            os.rename(file_path, new_file_path)
            files_ret.append(new_file_path)
    return files_ret


def save_client_photos_in_cache(dst_path):
    photos_paths = get_all_files_under_dir('tciaDownload/')
    
    for src_path in photos_paths:
        file_name = os.path.basename(src_path)
        cur_dst_path = dst_path + '/' + file_name
        if not os.path.isfile(cur_dst_path):
            os.rename(src_path, cur_dst_path)
    delete_files_in_folder('tciaDownload/')