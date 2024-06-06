import json
from flask import Blueprint, request, jsonify
from data.data import calc_df, mass_df, pd
from data.data import extract_unique_values
filter_bp = Blueprint('filter', __name__)


def filter_by(df: pd.DataFrame, filters: dict):
    for col, value in filters.items():
        if col in df.columns:
            if col == 'patient_id':
                df = df.loc[df[col].str.contains(value)]
            else:
                df = df.loc[df[col] == value]
    return df


@filter_bp.route('/', methods=['GET'])
def filtering():
    # get the filters as json from the user in an API request
    filters = request.json
    # filter the calc data
    calc_by_filters = set(filter_by(calc_df, filters)['patient_id'])
    # filter the mass data
    mass_by_filters = set(filter_by(mass_df, filters)['patient_id'])
    # unite all the patient_id that conform to the filters
    patients = mass_by_filters.union(calc_by_filters)
    # return list of
    return jsonify(list(patients))

@filter_bp.route('/options', methods=['GET'])
def filter_options():
    print("filter options")
    columns_to_extract = [
        'leftOrRightBreast',
        'imageView',
        'abnormalityId',
        'abnormalityType',
        'breastDensity',
        'subtlety',
        'assessment',
        'pathology'
    ]
    response = extract_unique_values(columns_to_extract)
    real = {}
    for key in response:
        real[key] = response[key]
    
    realJson = json.dumps(real, default=str)
    return jsonify(realJson), 200

@filter_bp.route('/abnormality-options', methods=['GET'])
def filter_options_mass():
    columns_to_extract = [
        'calcType',
        'calcDistribution',
        'massShape',
        'massMargins',
    ]
    response = extract_unique_values(columns_to_extract)
    real = {}
    for key in response:
        real[key] = response[key]

        
    realJson = json.dumps(real, default=str)
    return jsonify(realJson), 200

