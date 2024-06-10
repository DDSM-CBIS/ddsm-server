import json
import pandas as pd
from flask import Blueprint, jsonify
from data.utils import calcDf, massDf
patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/', methods=['GET'])
def patients():
    patients = {}

    for df in [calcDf, massDf]:
        for index, row in df.iterrows():
            patient_id = row['patientId']
            if patient_id not in patients:
                patients[patient_id] = []
            patients[patient_id].append(row.dropna().drop('patientId').to_dict())
    
    realJson = json.dumps(patients, default=str)
    return jsonify(realJson), 200