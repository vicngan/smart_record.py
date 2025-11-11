import json
import os
from datetime import datetime

TIMELINE_FILE = "timeline.json"


def load_timeline(filename: str = TIMELINE_FILE):
    if os.path.isfile(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return data
            except json.JSONDecodeError:
                pass
    return []


def save_timeline(entries, filename: str = TIMELINE_FILE):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def log_timeline(entries, patient_id, event_type, description, filename: str = TIMELINE_FILE):
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "patient_id": patient_id,
        "event": event_type,
        "description": description,
    }
    entries.append(entry)
    save_timeline(entries, filename)
    return entry


def recent_events(entries, limit=25):
    return sorted(entries, key=lambda e: e.get("timestamp", ""), reverse=True)[:limit]
