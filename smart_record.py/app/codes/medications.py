import json
import os
from datetime import datetime

MED_FILE = "medications.json"


def load_medications(filename: str = MED_FILE):
    if os.path.isfile(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
            except json.JSONDecodeError:
                pass
    return {}


def save_medications(data, filename: str = MED_FILE):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def add_medication(data, patient_id, name, dose, schedule, priority="do soon"):
    entry = {
        "name": name,
        "dose": dose,
        "schedule": schedule,
        "priority": priority,
        "given": False,
        "last_updated": datetime.now().isoformat(),
    }
    data.setdefault(patient_id, []).append(entry)
    save_medications(data)
    return entry


def toggle_med(data, patient_id, index):
    meds = data.get(patient_id, [])
    if 0 <= index < len(meds):
        meds[index]["given"] = not meds[index].get("given", False)
        meds[index]["last_updated"] = datetime.now().isoformat()
        save_medications(data)
        return meds[index]
    return None
