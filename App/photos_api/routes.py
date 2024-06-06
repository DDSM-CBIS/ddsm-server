from tcia_utils import nbia
from flask import Blueprint, request, jsonify, send_from_directory
from .utils import *

photos_bp = Blueprint('photos', __name__)


@photos_bp.route('/photos/<patient_id>/<filename>', methods=['GET'])
def serve_photo(patient_id, filename):
    photo_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'cache', f'{patient_id}')
    # photo_directory = f'../../cache/{patient_id}'  # Replace with the actual path
    return send_from_directory(photo_directory, filename)


@photos_bp.route('/get_photos/', methods=['GET'])
def get_photos():
    # get the patient id from the api request
    patient_id = request.json['patient_id']

    # create path in our cache folder
    dst_path = f'cache/{patient_id}'
    create_if_not_exist_folder(dst_path)

    # get the photos uids from the patient_ids
    photos_uids = get_photos_uids(patient_id)
    # download the photos from uid
    nbia.downloadSeries(photos_uids, input_type="list", format="df")

    # move downloaded pics to cache
    save_client_photos_in_cache(dst_path)

    # now returning the pics urls
    photo_urls = get_photo_urls(patient_id=patient_id, dst_path=dst_path)
    # return list of photos paths to render in the front
    return jsonify({'photos': photo_urls})
