from datetime import datetime
import csv
import os
import json
from tkinter import messagebox
import matplotlib.pyplot as plt

from data_access import append_to_csv, save_to_json
from timeline import log_timeline
from utils import RED, RESET, typeprint, normalize_bp, normalize_dob, normalize_temp


def _is_abnormal_hr(hr, low=40, high=110):
    try:
        hr_val = int(hr)
    except (ValueError, TypeError):
        return False
    return hr_val < low or hr_val > high


def _is_abnormal_bp(bp, sys_low=90, sys_high=150, dias_low=50, dias_high=100):
    try:
        systolic, diastolic = map(int, bp.split("/"))
    except (ValueError, AttributeError):
        return False
    return systolic < sys_low or systolic > sys_high or diastolic < dias_low or diastolic > dias_high


def _is_abnormal_temp(temp, low=95.0, high=100.4):
    try:
        temp_val = float(temp)
    except (ValueError, TypeError):
        return False
    return temp_val < low or temp_val > high


def _history_dir():
    path = os.path.join(os.path.dirname(__file__), "patient_history")
    os.makedirs(path, exist_ok=True)
    return path


def load_history(patient_id):
    history_file = os.path.join(_history_dir(), f"{patient_id}.json")
    if os.path.isfile(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def append_history(patient):
    history = load_history(patient["patient_id"])
    history.append(
        {
            "Time": patient.get("Time"),
            "HR": patient.get("HR"),
            "BP": patient.get("BP"),
            "Temp": patient.get("Temp"),
            "Diagnosis": patient.get("Diagnosis"),
        }
    )
    history_file = os.path.join(_history_dir(), f"{patient['patient_id']}.json")
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def add_patient(
    patient_list,
    patient_id,
    name,
    DOB,
    HR,
    BP,
    Temp,
    chief_complaint="",
    diagnosis="",
    RN_AP=None,
    timeline_entries=None,
):
    if RN_AP is None:
        RN_AP = input("Personel Initials: ")

    DOB = normalize_dob(DOB)
    BP = normalize_bp(BP)
    Temp = normalize_temp(Temp)

    try:
        DOB_obj = datetime.strptime(DOB, "%m/%d/%Y")
        DOB = DOB_obj.strftime("%m/%d/%Y")
    except ValueError:
        print("Invalid format!! Use MM/DD/YYYY")
        return

    time_stamp = datetime.now().strftime("%I:%M %p")
    patient = {
        "patient_id": patient_id,
        "name": name,
        "DOB": DOB,
        "HR": HR,
        "BP": BP,
        "Temp": Temp,
        "CC": chief_complaint,
        "Diagnosis": diagnosis,
        "RN_AP": RN_AP,
        "Time": time_stamp,
    }

    patient_list.append(patient)
    append_to_csv(patient)
    append_history(patient)
    save_to_json(patient)
    append_history(patient)
    if timeline_entries is not None:
        log_timeline(
            timeline_entries,
            patient_id,
            "New Patient",
            f"{name} added with HR {HR} / BP {BP} / Temp {Temp}",
        )

    typeprint("\nNew Patient Added Successfully! 🎀")
    view_patients(patient_list)
    systolic, diastolic = map(int, BP.split("/"))
    if int(HR) < 40 or int(HR) > 110 or systolic < 90 or systolic > 150 or diastolic < 50 or diastolic > 100:
        messagebox.showwarning("⚠️ Abnormal Vitals Alert", f"{name}'s vitals are abnormal!")


def view_patients(patient_list):
    if not patient_list:
        print("No patient records yet")
        return

    print(f"{'patient_id':<12}{'name':<15}{'DOB':<15}{'HR':<10}{'BP':<12}{'Temp':<8}{'CC':<15}{'Diagnosis':<15}{'RN_AP':<6}")
    print("-" * 80)

    for p in patient_list:
        systolic, diastolic = map(int, p["BP"].split("/"))
        is_abnormal = (systolic > 140 or systolic < 90) or (diastolic > 100 or diastolic < 50)
        bp_display = f"{RED}{p['BP']}{RESET}" if is_abnormal else p["BP"]

        typeprint(
            f"{p['patient_id']:<12}{p['name']:<15}{p['DOB']:<15}{p['HR']:<10}"
            f"{bp_display:<12}{p['Temp']:<8}{p.get('CC',''):<15}{p.get('Diagnosis',''):<15}{p['RN_AP']:<6}"
        )


def search_patient(patient_list, patient_id):
    for patient in patient_list:
        if patient["patient_id"] == patient_id:
            typeprint("\nPatient Record Found!!")
            print(f"{'ID':<10}{'Name':<15}{'DOB':<15}")
            typeprint(f"{patient['patient_id']:<10}{patient['name']:<15}{patient['DOB']:<15}")
            return
    typeprint("\nNo patient found with that ID, try again :D")


def get_abnormal_HR(patient_list, HR_low=40, HR_high=110):
    return [p for p in patient_list if int(p["HR"]) < HR_low or int(p["HR"]) > HR_high]


def count_abnormal_HR(patient_list, HR_low=40, HR_high=110):
    return len(get_abnormal_HR(patient_list, HR_low, HR_high))


def display_abnormal_HR(patient_list, HR_low=40, HR_high=110):
    abnormal_list = get_abnormal_HR(patient_list, HR_low, HR_high)
    print("\nAbnormal Heart Rate Patients:")
    typeprint("{:<10}{:<15}{:<15}{:<6}".format("ID", "Name", "DOB", "HR"))
    print("-" * 45)
    for p in abnormal_list:
        print("{:<10}{:<15}{:<15}{:<6}".format(p["patient_id"], p["name"], p["DOB"], p["HR"]))
    print(f"\nTotal: {len(abnormal_list)}")


def get_abnormal_BP(patient_list, sys_low=90, sys_high=140, dias_low=50, dias_high=100):
    abnormal_list = []
    for p in patient_list:
        systolic, diastolic = map(int, p["BP"].split("/"))
        if systolic < sys_low or systolic > sys_high or diastolic < dias_low or diastolic > dias_high:
            abnormal_list.append(p)
    return abnormal_list


def count_abnormal_BP(patient_list, sys_low=90, sys_high=150, dias_low=50, dias_high=100):
    return len(get_abnormal_BP(patient_list, sys_low, sys_high, dias_low, dias_high))


def display_abnormal_BP(patient_list, sys_low=90, sys_high=150, dias_low=50, dias_high=100):
    abnormal_list = get_abnormal_HR(patient_list)
    print(f"\nAbnormal HR count: {len(abnormal_list)}")
    print("{:<10}{:<15}{:<15}{:<6}".format("ID", "Name", "DOB", "HR"))
    print("-" * 45)
    for p in abnormal_list:
        typeprint("{:<10}{:<15}{:<15}{:<6}".format(p["patient_id"], p["name"], p["DOB"], p["HR"]))


def abnormal_summary(patient_list, HR_low=40, HR_high=110, sys_low=90, sys_high=150, dias_low=50, dias_high=100):
    if not patient_list:
        print("No patient record found :( Try again!)")
        return
    typeprint(f"\n{'ID':<8}{'Name':<15}{'HR':<8}{'BP':<10}{'Status':<12}")

    for p in patient_list:
        hr = int(p["HR"])
        hr_display = f"{RED}{hr}{RESET}" if hr < HR_low or hr > HR_high else str(hr)

        systolic, diastolic = map(int, p["BP"].split("/"))
        if systolic < sys_low or systolic > sys_high or diastolic < dias_low or diastolic > dias_high:
            bp_display = f"{RED}{p['BP']}{RESET}"
        else:
            bp_display = p["BP"]

        status = []
        if hr < HR_low or hr > HR_high:
            status.append("HR abnormal!")
        if systolic < sys_low or systolic > sys_high or diastolic < dias_low or diastolic > dias_high:
            status.append("BP abnormal!")
        status = ", ".join(status) if status else "Normal"

        typeprint(f"{p['patient_id']:<8}{p['name']:<12}{'DOB':<15}{hr_display:<10}{bp_display:<12}{status:<12}")


def export_report(patient_list, filename="report"):
    report = patient_list
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "DOB", "HR", "BP", "Temp"])
        for p in report:
            writer.writerow([p["patient_id"], p["name"], p["DOB"], p["HR"], p["BP"], p["Temp"]])
        messagebox.showinfo("Export", f"Report saved as {filename}")


def update_vitals(patient_list, patient_id, updates, timeline_entries=None):
    patient = next((p for p in patient_list if p["patient_id"] == patient_id), None)
    if not patient:
        typeprint("\nNo patient found with that ID, try again!\n")
        return False

    new_time = datetime.now().strftime("%I:%M %p")
    hr = updates.get("HR") or patient["HR"]
    bp = normalize_bp(updates.get("BP") or patient["BP"])
    temp = normalize_temp(updates.get("Temp") or patient["Temp"])
    diagnosis = updates.get("Diagnosis") or patient.get("Diagnosis", "")
    rn = updates.get("RN_AP") or patient.get("RN_AP", "")

    patient["HR"] = hr
    patient["BP"] = bp
    patient["Temp"] = temp
    patient["Time"] = new_time
    patient["Diagnosis"] = diagnosis
    patient["RN_AP"] = rn

    append_to_csv(patient)
    typeprint("\nVitals updated successfully :D\n")
    typeprint(
        f"{patient['patient_id']:<8}{patient['name']:<12}{patient['DOB']:<15}{patient['HR']:<8}"
        f"{patient['BP']:<12}{patient['Temp']:<8}{patient['CC']:<20}{patient['Diagnosis']:20}"
    )
    if timeline_entries is not None:
        log_timeline(
            timeline_entries,
            patient_id,
            "Vitals Update",
            f"HR {hr}, BP {bp}, Temp {temp}, Dx {diagnosis}",
        )
    return True


def plot_trend(patient_list, patient_id):
    patient_data = [p for p in patient_list if p["patient_id"] == patient_id]
    if not patient_data:
        messagebox.showerror("Error!", "Patient not found, Try Again!")
        return

    history = load_history(patient_id)
    all_records = history if history else patient_data

    cleaned_points = []
    for idx, record in enumerate(all_records, start=1):
        label = record.get("Time") or f"Entry {idx}"
        try:
            hr_value = int(record["HR"])
            systolic, diastolic = map(int, record["BP"].split("/"))
        except (ValueError, TypeError, AttributeError):
            continue
        cleaned_points.append((label, hr_value, systolic, diastolic))

    if not cleaned_points:
        messagebox.showerror("Not Enough Data", "This patient does not have valid vitals to chart yet.")
        return

    times, HRs, systolics, diastolics = zip(*cleaned_points)
    plt.figure(figsize=(8, 4))
    plt.plot(times, HRs, marker="o", label="HR")
    plt.plot(times, systolics, label="Systolic BP")
    plt.plot(times, diastolics, label="Diastolic BP")
    plt.xlabel("Time")
    plt.ylabel("Vitals")
    plt.title(f"Vitals Trend for Patient {patient_id}")
    plt.legend()
    plt.show()


def create_handoff_summary(patient_list, tasks=None):
    if not patient_list:
        return "No patients recorded yet."

    task_lookup = {}
    if tasks:
        for task in tasks:
            if task.get("status") == "done":
                continue
            task_lookup.setdefault(task["patient_id"], []).append(task)

    lines = []
    lines.append("Smart Record Handoff Summary")
    lines.append("-" * 32)
    for patient in patient_list:
        hr_status = "⚠️" if _is_abnormal_hr(patient["HR"]) else "✅"
        bp_status = "⚠️" if _is_abnormal_bp(patient["BP"]) else "✅"
        temp_status = "⚠️" if _is_abnormal_temp(patient["Temp"]) else "✅"
        outstanding = len(task_lookup.get(patient["patient_id"], []))
        lines.append(
            f"{patient['patient_id']} • {patient['name']} ({patient['DOB']})\n"
            f"   HR {patient['HR']} {hr_status} | BP {patient['BP']} {bp_status} | Temp {patient['Temp']} {temp_status}\n"
            f"   Dx: {patient.get('Diagnosis','-')} • Tasks: {outstanding} open"
        )
    return "\n".join(lines)


def plot_abnormal_overview(patient_list):
    if not patient_list:
        messagebox.showinfo("Info", "No patient records to chart yet.")
        return

    hr_count = sum(1 for p in patient_list if _is_abnormal_hr(p["HR"]))
    bp_count = sum(1 for p in patient_list if _is_abnormal_bp(p["BP"]))
    temp_count = sum(1 for p in patient_list if _is_abnormal_temp(p["Temp"]))

    labels = ["Heart Rate", "Blood Pressure", "Temperature"]
    values = [hr_count, bp_count, temp_count]
    colors = ["#f48fb1", "#f6bd60", "#9cc5c9"]

    plt.figure(figsize=(6, 4))
    bars = plt.bar(labels, values, color=colors)
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, str(value), ha="center", va="bottom")
    plt.title("Abnormal Vitals Overview")
    plt.ylabel("Patient Count")
    plt.ylim(0, max(values + [1]) + 1)
    plt.show()


def priority_alerts(patient_list):
    alerts = []
    for patient in patient_list:
        severity = None
        details = []
        if _is_abnormal_hr(patient["HR"], low=45, high=130):
            details.append(f"HR {patient['HR']}")
            severity = "critical"
        elif _is_abnormal_hr(patient["HR"]):
            details.append(f"HR {patient['HR']}")
            severity = severity or "warning"

        if _is_abnormal_bp(patient["BP"], sys_low=85, sys_high=170, dias_low=45, dias_high=110):
            details.append(f"BP {patient['BP']}")
            severity = "critical"
        elif _is_abnormal_bp(patient["BP"]):
            details.append(f"BP {patient['BP']}")
            severity = severity or "warning"

        if _is_abnormal_temp(patient["Temp"], low=94.0, high=102.0):
            details.append(f"Temp {patient['Temp']}")
            severity = severity or "warning"
        elif _is_abnormal_temp(patient["Temp"]):
            details.append(f"Temp {patient['Temp']}")
            severity = severity or "info"

        if details:
            alerts.append(
                {
                    "patient_id": patient["patient_id"],
                    "name": patient["name"],
                    "severity": severity or "info",
                    "details": ", ".join(details),
                }
            )
    return alerts
