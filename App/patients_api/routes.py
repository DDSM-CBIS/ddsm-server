import json
from flask import Blueprint, request, jsonify
from data.data import calc_df, mass_df, pd
from data.data import extract_unique_values
patients_bp = Blueprint('patients', __name__)


def filter_by(df: pd.DataFrame, filters: dict):
    for col, value in filters.items():
        if col in df.columns:
            if col == 'patient_id':
                df = df.loc[df[col].str.contains(value)]
            else:
                df = df.loc[df[col] == value]
    return df

@patients_bp.route('/', methods=['GET'])
def patients():
    merges = pd.merge(calc_df, mass_df, on='patient_id', how='outer')
    json_data = merges.set_index('patient_id').to_json(orient='index')
    return jsonify(json_data)

@patients_bp.route('/ids', methods=['GET'])
def patient_ids():
    response = extract_unique_values(['patientId'])
    realJson = json.dumps(response, default=str)
    return jsonify(realJson), 200
