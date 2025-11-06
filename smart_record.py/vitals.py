#list to store patients info
vitals_log = []

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

    RED = "\033[91m"
    RESET = "\033[0m"

    print(f"{'patient_id':<12}{'name':<12}{'DOB':<12}{'HR':<8}{'BP':<10}{'Temp':<10}{'Time':<8}")
    for p in patient_list:
        systolic, diastolic = map(int, p["BP"].split('/')) #turning strings into integer and split at /
        #check for abnormality
        is_abnormal = (systolic >140 or systolic <90) or (diastolic >100 or diastolic <50)

        if is_abnormal:
            bp_display = f"{RED}{p['BP']}{RESET}"
        else:
            bp_display = p['BP']

        print(f"{p['patient_id']:<8}{p['name']:<12}{p['DOB']:<12}{p['HR']:<6}{p['BP']:<10}{bp_display:<10}{p['Temp']:<6}{p['Time']:<8}")


#view all patients 
def view_patients(patient_list):
    if not patient_list:
        print ("No patient records yet :()")
    for patient in patient_list:
        print(patient)

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
    
print(f"Abnormal BP count:", count_abnormal_BP(vitals_log))

#starting interraction
if __name__ == "__main__":
    print ("Welcome to Smart Record App :D")
    while True:
        print("\nOptions: 1 = add patient, 2 = view patients, 3 = abnormal BP count, 4 = abnormal HR count, 5 = exit")
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
            print("It's a good day to save lives! See you later!!")
            break
        else:
            print("This choice does not exist! Try Again :D")

