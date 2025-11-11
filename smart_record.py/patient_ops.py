from datetime import datetime
import csv
from tkinter import messagebox
import matplotlib.pyplot as plt

from data_access import append_to_csv, save_to_json
from utils import RED, RESET, typeprint


def add_patient(patient_list, patient_id, name, DOB, HR, BP, Temp, chief_complaint="", diagnosis="", RN_AP=None):
    if RN_AP is None:
        RN_AP = input("Personel Initials: ")

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
    save_to_json(patient)

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


def update_vitals(patient_list, patient_id):
    for patient in patient_list:
        if patient["patient_id"] == patient_id:
            typeprint("\nPatient Found! Go ahead and enter the updated vital!\n")

            new_HR = input("Updated Heart Rate: ")
            new_BP = input("Updated Blood Pressure: ")
            new_temp = input("Updated Temperature: ")
            new_diag = input("Updated Diagnosis: ")
            new_RN_AP = input("Personel Initials: ")

            new_time = datetime.now().strftime("%I:%M %p")

            patient["HR"] = new_HR
            patient["BP"] = new_BP
            patient["Temp"] = new_temp
            patient["Time"] = new_time
            patient["Diagnosis"] = new_diag
            patient["RN_AP"] = new_RN_AP

            append_to_csv(patient)
            typeprint("\nVitals updated successfully :D\n")
            typeprint(
                f"{patient['patient_id']:<8}{patient['name']:<12}{patient['DOB']:<15}{patient['HR']:<8}"
                f"{patient['BP']:<12}{patient['Temp']:<8}{patient['CC']:<20}{patient['Diagnosis']:20}"
            )
            return
    typeprint("\nNo patient found with that ID, try again!\n")


def plot_trend(patient_list, patient_id):
    patient_data = [p for p in patient_list if p["patient_id"] == patient_id]
    if not patient_data:
        messagebox.showerror("Error!", "Patient not found, Try Again!")
        return

    cleaned_points = []
    for idx, record in enumerate(patient_data, start=1):
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
