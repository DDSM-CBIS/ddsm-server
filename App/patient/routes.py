import json
from flask import Blueprint, abort, jsonify, request
from App import series_mng, data_mng

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/', methods=['GET'])
def patients():
    response = data_mng.get_patients_data()
    return jsonify(response), 200

@patients_bp.route('/<patient_id>', methods=['GET'])
def patient(patient_id):
    response = data_mng.get_patients_data(patient_id)
    return jsonify(response), 200

@patients_bp.route('/<patient_id>/images-metadata', methods=['GET'])
def get_image_metadata(patient_id):
    image_format = request.args.get('format')
    if not image_format:
        return abort(400, description="Missing image format")

    series_instance_uids = series_mng.get_patient_series_instance_uids(patient_id, image_format)
    image_metadata = {}
    for uid in series_instance_uids:
        sop_uids = series_mng.get_sop_uids(uid)
        
        if sop_uids is None:
            return abort(404, description="No SOP UID found for the given series instance UID")
        
        image_metadata[uid] = sop_uids

    return jsonify(image_metadata), 200

@patients_bp.route('/filter', methods=['GET'])
def filter_patients():
    filters = request.args.get('filters')
    
    if not filters:
        return abort(400, description="Missing filters")
    
    filters_dict = json.loads(filters)
    response = data_mng.filter_patients(filters_dict)
    result = {"patientsIds": response}
    res_str = json.dumps(result, default=str)
    return jsonify(res_str), 200
