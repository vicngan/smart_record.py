import json
import os
from datetime import datetime

PATIENT_FILES = "patient_files.json"


def load_patient_files(filename: str = PATIENT_FILES):
    if os.path.isfile(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
            except json.JSONDecodeError:
                pass
    return {}


def save_patient_files(files, filename: str = PATIENT_FILES):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(files, f, indent=2)


def ensure_patient_record(files, patient_id):
    record = files.setdefault(
        patient_id,
        {
            "goals": [],
            "discharge_ready": False,
            "assigned_by": "",
            "photo": "",
        },
    )
    return record


def update_goals(files, patient_id, goals, assigned_by="", filename: str = PATIENT_FILES):
    record = ensure_patient_record(files, patient_id)
    record["goals"] = goals
    record["assigned_by"] = assigned_by
    save_patient_files(files, filename)
    return record


def set_discharge_status(files, patient_id, status, filename: str = PATIENT_FILES):
    record = ensure_patient_record(files, patient_id)
    record["discharge_ready"] = status
    save_patient_files(files, filename)
    return record


def set_photo(files, patient_id, photo_path, filename: str = PATIENT_FILES):
    record = ensure_patient_record(files, patient_id)
    record["photo"] = photo_path
    record.setdefault("photo_updated", datetime.now().isoformat())
    save_patient_files(files, filename)
    return record
