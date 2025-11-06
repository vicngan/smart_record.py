import csv
import os
import datetime
import time

RED = "\033[91m"
RESET = "\033[0m"

def typeprint(text, speed=0.05): #print function
        for char in text:
            print(char, end='', flush=True) #print without newline
            time.sleep(speed) #delay between chars
        print()

CSV_FILE = "vital_log.csv"

#list to store patients info
def load_from_csv(filename="vital_log.csv"):
    patient_list = []
    if os.path.isfile(filename):
        with open(filename, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                patient_list.append(row)
                row["HR"] = int(row["HR"])
                row["Temp"] = float(row["Temp"])
    return patient_list

#take data and save to .csv file 
def save_to_csv(patient, filename= "vital_log.csv"):
    #write header if file doesn't exist
    file_exists = os.path.isfile(filename) #checks if file exists

    with open(filename, mode="a", newline="")as file: #open in append mode + "a" add to the end 
        writer =csv.writer(file) #writer helper

        if not file_exists:
            writer.writerow(["patient_id", "name", "DOB", "HR", "BP", "Temp", "Time"])

        writer.writerow([
            patient["patient_id"], patient["name"], patient["DOB"],
            patient["HR"], patient["BP"], patient["Temp"], patient["Time"]
        ])

#add patient 
def add_patient(patient_list, patient_id, name, DOB, HR, BP, Temp, Time):
    from datetime import datetime
    #DOB format
    try:
        DOB_obj = datetime.strptime(DOB, "%m/%d/%Y") #string -> datetime object
        DOB = DOB_obj.strftime("%m/%d/%Y") #datetime -> string
    except ValueError:
        print("Invalid format!! Use MM/DD/YYYY")
        return

    # Timestamp
    Time = datetime.now().strftime("%I:%M %p")
    
    #PatientDict.
    patient = {
        "patient_id": patient_id,
        "name": name,
        "DOB": DOB,
        "HR": HR,
        "BP": BP,
        "Temp": Temp,
        "Time": Time,
    }

    patient_list.append(patient)
    save_to_csv(patient)
    
    typeprint("\nNew Patient Added Successfully! 🎀")
    view_patients(patient_list)

#view all patients 
def view_patients(patient_list):
    if not patient_list:
        print ("No patient records yet :()")
        return
    for patient in patient_list:
        print(patient)

    typeprint(f"{'patient_id':<12}{'name':<12}{'DOB':<12}{'HR':<8}{'BP':<10}{'Temp':<10}{'Time':<8}")
    for p in patient_list:
        systolic, diastolic = map(int, p["BP"].split('/')) #turning strings into integer and split at /
        #check for abnormality
        is_abnormal = (systolic >140 or systolic <90) or (diastolic >100 or diastolic <50)

        if is_abnormal:
            bp_display = f"{RED}{p['BP']}{RESET}"
        else:
            bp_display = p['BP']

        print(f"{p['patient_id']:<8}{p['name']:<12}{p['DOB']:<12}{p['HR']:<6}{p['BP']:<10}{bp_display:<10}{p['Temp']:<6}{p['Time']:<8}")

#search pts by ID
def search_patient(patient_list, patient_id):
    for patient in patient_list:
        if patient["patient_id"] == patient_id:
            print("\nPatient Record Found!!")
            print(f"{'ID':<10}{'Name':<12}{'DOB':<12}")
            print(f"{patient['patient_id']:<10}{patient['name']:<12}{patient['DOB']:<12}")
            return
    print("\nNo patient found with that ID, try again :D")

#count abnormal HR
def count_abnormal_HR(patient_list, threshold=100):
    count=sum(1 for patient in patient_list if patient ['HR']>threshold)
    return count 

#count abnormal BP
def count_abnormal_BP(patient_list, sys_low=90, sys_high=150, dias_low=50, dias_high=100):
    count=0
    for patient in patient_list:
        systolic, diastolic = patient ["BP"].split("/")
        systolic = int(systolic)
        diastolic = int(diastolic)

        if systolic < sys_low or systolic > sys_high or diastolic < dias_low or diastolic > dias_high:
            count += 1

    return count 
    
#update patient vitals
def update_vitals(patient_list, patient_id):
    for patient in patient_list:
        if patient["patient_id"] == patient_id:
            print("\nPatient Found! Go ahead and enter the updated vital!\n")

            new_HR = input("Updated Heart Rate: ")
            new_BP = input("Updated Blood Pressure: ")
            new_temp = input("Updated Temperature: ")

            new_Time = datetime.now().strftime("%I:%M %p")

            patient["HR"] = new_HR
            patient["BP"] = new_BP
            patient["Temp"] = new_temp
            patient["Time"] = new_Time

            save_to_csv(patient)
            print("\nVitals updated successfully :D\n")
            print(f"{patient['patient_id']:<8}{patient['name']:<12}{patient['DOB']:<12}{patient['HR']:<6}{patient['BP']:<10}{patient['Temp']:<6}{patient['Time']:<8}")
            return
    print("\nNo patient found with that ID, try again!\n")

#main program
if __name__ == "__main__":
    print ("Welcome to Smart Record App :D")
    if __name__ == "__main__":
        vitals_log = load_from_csv() #restores old record from csv
    
    while True:
        print("\nOptions:")
        print("1 = Add patient")
        print("2 = View patients")
        print("3 = Abnormal BP count")
        print("4 = Abnormal HR count")
        print("5 = Search patient")
        print("6 = Update patient vitals")
        print("7 = Exit")
        
        choice = input("please select your choice:")
        if choice == "1":
            patient_id = input("Patient ID: ")
            name = input("Patient name: ")
            DOB = input("Date of Birth: ")
            HR = input("Heart Rate: ")
            BP = input("Blood Pressure: ")
            Temp = input("Temperature: ")
            Time = input("Time: ")
            add_patient(vitals_log, patient_id, name, DOB, HR, BP, Temp, Time)
        elif choice == "2":
            view_patients(vitals_log)
        elif choice == "3":
            print(f"Abnormal BP count: {count_abnormal_BP(vitals_log)}")
        elif choice == "4":
            print(f"Abnormal HR count: {count_abnormal_HR(vitals_log)}")
        elif choice == "5":
            search_id = input("Please enter patient ID to search: ")
            search_patient(vitals_log, search_id)
        elif choice == "6":
            update_id = input("Enter Patient ID to update: ")
            update_vitals(vitals_log, update_id)
        elif choice == "7":
            print("It's a good day to save lives! See you later!!")
            break
        else:
            print("This choice does not exist! Try Again :D")
