import json
import pandas as pd
from flask import Blueprint, jsonify
from data.data import calc_df, mass_df, extract_unique_values
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
    merged = pd.merge(calc_df, mass_df, how='outer')
    result_dict = {}
    
    grouped = merged.groupby('patientId')
    for patient_id, group in grouped:
        rows_list = group.drop(columns='patientId').to_dict(orient='records')
        result_dict[patient_id] = rows_list
    
    realJson = json.dumps(result_dict, default=str)
    return jsonify(realJson), 200

@patients_bp.route('/ids', methods=['GET'])
def patient_ids():
    response = extract_unique_values(['patientId'])
    realJson = json.dumps(response, default=str)
    return jsonify(realJson), 200