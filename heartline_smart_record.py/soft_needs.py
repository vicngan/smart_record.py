import json
import os
from datetime import datetime

SOFT_NEEDS_FILE = "soft_needs.json"


def load_soft_needs(filename: str = SOFT_NEEDS_FILE):
    if os.path.isfile(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
            except json.JSONDecodeError:
                pass
    return {}


def save_soft_needs(notes, filename: str = SOFT_NEEDS_FILE):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2)


def add_soft_note(notes, patient_id, cue, filename: str = SOFT_NEEDS_FILE):
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "note": cue,
    }
    notes.setdefault(patient_id, []).append(entry)
    save_soft_needs(notes, filename)
    return entry


def get_soft_notes(notes, patient_id):
    return notes.get(patient_id, [])
