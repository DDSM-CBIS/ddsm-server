
from flask import Blueprint, send_file, request, abort
from app import series_mng

images_bp = Blueprint('images', __name__)

@images_bp.route('/full', methods=['GET'])
def get_image():
    series_UID = request.args.get('series_UID')
    sop_uid = request.args.get('sop_uid')
    
    if not series_UID or not sop_uid:
        return abort(400, description="Missing UID or SOP UID")

    res = series_mng.get_image_by_uids(series_UID, sop_uid)
    if res is None:
        return abort(404, description="Image not found")

    return send_file(res, mimetype="image/jpeg"), 200
