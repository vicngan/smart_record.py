import csv
import json
import os

CSV_FILE = "patient_list.csv"
JSON_FILE = "patient_list.json"
CSV_HEADERS = [
    "patient_id",
    "name",
    "DOB",
    "HR",
    "BP",
    "Temp",
    "CC",
    "Diagnosis",
    "RN_AP",
    "Time",
]


def load_from_csv(filename: str = CSV_FILE):
    patient_list = []
    if os.path.isfile(filename):
        with open(filename, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                hr_value = row.get("HR")
                temp_value = row.get("Temp")
                try:
                    row["HR"] = int(hr_value) if hr_value not in (None, "") else 0
                except ValueError:
                    row["HR"] = 0
                try:
                    row["Temp"] = float(temp_value) if temp_value not in (None, "") else 0.0
                except ValueError:
                    row["Temp"] = 0.0
                row["Time"] = row.get("Time") or row.get("timestamp") or ""
                patient_list.append(row)
    return patient_list


def append_to_csv(patient, filename: str = CSV_FILE):
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
        if not file_exists:
            writer.writeheader()
        row = {field: patient.get(field, "") for field in CSV_HEADERS}
        writer.writerow(row)


def save_to_json(patient_list, filename: str = JSON_FILE):
    with open(filename, "a") as f:
        json.dump(patient_list, f, indent=4)


def save_data(patient_list, filename: str = JSON_FILE):
    with open(filename, "w") as f:
        json.dump(patient_list, f, indent=4)


def load_data(filename: str = JSON_FILE):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
