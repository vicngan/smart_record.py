from data_access import load_from_csv
from patient_ops import (
    add_patient,
    view_patients,
    display_abnormal_BP,
    display_abnormal_HR,
    search_patient,
    update_vitals,
    export_report,
)
from utils import typeprint


def run_cli():
    typeprint("Welcome to Smart Record App :D")
    patient_list = load_from_csv()

    while True:
        print("\nOptions:")
        print("1 = Add patient")
        print("2 = View patients")
        print("3 = Abnormal BP count")
        print("4 = Abnormal HR count")
        print("5 = Search patient")
        print("6 = Update patient vitals")
        print("7 = Export report")
        print("8 = Exit")

        choice = input("please select your choice:")

        if choice == "1":
            patient_id = input("Patient ID: ")
            name = input("Patient name: ")
            DOB = input("Date of Birth: ")
            HR = input("Heart Rate: ")
            BP = input("Blood Pressure: ")
            Temp = input("Temperature: ")
            CC = input("Chief Concerns: ")
            Diagnosis = input("Enter Patient Diagnosis: ")
            add_patient(patient_list, patient_id, name, DOB, HR, BP, Temp, CC, Diagnosis)
        elif choice == "2":
            view_patients(patient_list)
        elif choice == "3":
            display_abnormal_BP(patient_list)
        elif choice == "4":
            display_abnormal_HR(patient_list)
        elif choice == "5":
            search_id = input("Please enter patient ID to search: ")
            search_patient(patient_list, search_id)
        elif choice == "6":
            update_id = input("Enter Patient ID to update: ")
            update_vitals(patient_list, update_id)
        elif choice == "7":
            export_report(patient_list)
        elif choice == "8":
            typeprint("It's a good day to save lives! See you later!!")
            break
        else:
            typeprint("This choice does not exist! Try Again :D")
