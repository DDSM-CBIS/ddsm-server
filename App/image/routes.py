from flask import Blueprint, send_file, request, abort, jsonify
from App import series_mng

images_bp = Blueprint('images', __name__)

@images_bp.route('/<patient_id>/images-metadata', methods=['GET'])
def get_image_metadata(patient_id):
    image_format = request.args.get('format')
    if not image_format:
        return abort(400, description="Missing image format")

    series_instance_uids = series_mng.get_patient_series_instance_uids(patient_id, image_format)
    image_metadata = {}
    for uid in series_instance_uids:
        metadata = series_mng.get_image_metadata(uid)
        if isinstance(metadata, tuple):
            return abort(metadata[1], description=metadata[0])
        
        image_metadata[uid] = metadata

    return jsonify(image_metadata), 200

@images_bp.route('/full', methods=['GET'])
def get_image():
    series_UID = request.args.get('series_UID')
    sop_uid = request.args.get('sop_uid')
    
    if not series_UID or not sop_uid:
        return abort(400, description="Missing UID or SOP UID")

    res = series_mng.get_image_by_uids(series_UID, sop_uid)
    if isinstance(res, tuple):
        return abort(res[1], description=res[0])

    return send_file(res, mimetype="image/jpeg"), 200
