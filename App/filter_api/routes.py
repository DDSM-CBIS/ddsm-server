import json
from flask import Blueprint, jsonify
from data.utils import get_common_columns, extract_unique_values, get_distinct_columns
filter_bp = Blueprint('filter', __name__)

@filter_bp.route('/options', methods=['GET'])
def filter_options():
    columns_to_extract = get_common_columns()
    response = extract_unique_values(columns_to_extract)
    
    real = {}
    for key in response:
        real[key] = response[key]
    
    realJson = json.dumps(real, default=str)
    return jsonify(realJson), 200

@filter_bp.route('/abnormality-options', methods=['GET'])
def filter_options_mass():
    columns_to_extract = get_distinct_columns()
    response = extract_unique_values(columns_to_extract)
    real = {}
    for key in response:
        real[key] = response[key]

    realJson = json.dumps(real, default=str)
    return jsonify(realJson), 200

@filter_bp.route('/patients-ids', methods=['GET'])
def filter_options_patients():
    response = extract_unique_values(['patientId'])
    realJson = json.dumps(response, default=str)
    return jsonify(realJson), 200

