import shutil

from data.data import series_df
import os


def delete_files_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)


def get_photos_uids(patient_id):
    photos_uids = list(series_df[series_df['PatientID']
                       .str
                       .contains(patient_id)]
                       .SeriesInstanceUID)
    return photos_uids


def create_if_not_exist_folder(folder_location: str):
    if not os.path.isdir(folder_location):
        os.mkdir(folder_location)

def get_all_files_under_dir(directory_path):
    files_ret = []
    for root, dirs, files in os.walk(directory_path):

        for file in files:
            if file == 'LICENSE':
                continue
            # Get the full path of the file and its extension
            file_path = os.path.join(root, file)
            # Get the name of the directory containing the file
            dir_name = os.path.basename(root)
            # get series name from dir name
            PatientID = series_df[series_df.SeriesInstanceUID == dir_name]['PatientID'].iat[0]
            # Create the new name for the file
            new_file_name = f"{PatientID}_{file[2:]}"

            # Construct the new path with the new file name
            new_file_path = os.path.join(root, new_file_name)
            if os.path.isfile(new_file_path):
                continue
            # Rename the file and move it to the same directory
            os.rename(file_path, new_file_path)
            files_ret.append(new_file_path)
    return files_ret


def save_client_photos_in_cache(dst_path):
    # collect all the pictures locations
    photos_paths = get_all_files_under_dir('tciaDownload/')
    # moving them to cache
    for src_path in photos_paths:
        file_name = os.path.basename(src_path)
        cur_dst_path = dst_path + '/' + file_name
        if not os.path.isfile(cur_dst_path):
            os.rename(src_path, cur_dst_path)
    delete_files_in_folder('tciaDownload/')


def get_photo_urls(patient_id, dst_path):
    return [f"http://127.0.0.1:5000/photos/{patient_id}/{filename}" for filename in os.listdir(dst_path)]