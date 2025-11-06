import csv
import os
from datetime import datetime
import time
import tkinter as tk
from tkinter import messagebox, simpledialog
import json

RED = "\033[91m"
RESET = "\033[0m"

def typeprint(text, speed=0.05): #print function
        for char in text:
            print(char, end='', flush=True) #print without newline
            time.sleep(speed) #delay between chars
        print()

CSV_FILE = "patient_list.csv" #create a csv file

#list to store patients info
def load_from_csv(filename="patient_list.csv"):
    patient_list = [] #create an empty list to store dictionaries
    if os.path.isfile(filename): #check if file exist
        with open(filename, mode="r", newline="") as file: #open csv. in read "r" mode; reading each row as dictionary
            reader = csv.DictReader(file)
            for row in reader: #loop through each row
                patient_list.append(row) #add dictionary to list
                row["HR"] = int(row["HR"])
                row["Temp"] = float(row["Temp"])
    return patient_list

patient_list = load_from_csv()

#take data and save to .csv file 
def save_to_csv(patient, filename= "patient_list.csv"):
    #write header if file doesn't exist
    file_exists = os.path.isfile(filename) #checks if file exists
    
    with open(filename, mode="a", newline="")as file: #open in append mode + "a" add to the end 
        writer =csv.writer(file) #writer helper
        if not file_exists:
            writer.writerow(["patient_id", "name", "DOB", "HR", "BP", "Temp"])
        writer.writerow([
            patient["patient_id"], patient["name"], patient["DOB"],
            patient["HR"], patient["BP"], patient["Temp"]
            ])
        

#add patient 
def add_patient(patient_list, patient_id, name, DOB, HR, BP, Temp):
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
    }

    patient_list.append(patient)
    save_to_csv(patient)
    
    typeprint("\nNew Patient Added Successfully! 🎀")
    view_patients(patient_list)

def save_data(patient_list, filename= 'patient_list.json'):
    with open(filename, "w") as f: #open write "w" mode as f (file nickname)
        json.dump(patient_list, f, indent = 4) #write data into file in JSON format , file writing into, indent
    print("Data Saved!!!")

#view all patients 
def view_patients(patient_list):
    if not patient_list:
        print ("No patient records yet :()")
        return
    for patient in patient_list:
        print(patient)

    typeprint(f"{'patient_id':<12}{'name':<12}{'DOB':<12}{'HR':<8}{'BP':<10}{'Temp':<10}")
    for p in patient_list:
        systolic, diastolic = map(int, p["BP"].split('/')) #turning strings into integer and split at /
        #check for abnormality
        is_abnormal = (systolic >140 or systolic <90) or (diastolic >100 or diastolic <50)

        if is_abnormal: #boolean
            bp_display = f"{RED}{p['BP']}{RESET}"
        else:
            bp_display = p['BP'] #highlight significant data without affecting actual data

        print(f"{p['patient_id']:<8}{p['name']:<12}{p['DOB']:<12}{p['HR']:<6}{p['BP']:<10}{bp_display:<10}{p['Temp']:<6}")

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
def get_abnormal_HR(patient_list, HR_low=40, HR_high = 110): #return a list of patients whose HR is abnormal
    abnormal_list = [ 
        p for p in patient_list #element for element in list if condition
        if int(p["HR"])< HR_low or int(p["HR"]) > HR_high
    ]
    return abnormal_list

def count_abnormal_HR(patient_list, HR_low=40, HR_high=110): #return the count of abnormal HR
    return len(get_abnormal_HR(patient_list, HR_low, HR_high)) 

def display_abnormal_HR(patient_list, HR_low=40, HR_high=110):
    abnormal_list = [
        p for p in patient_list
        if int(p["HR"]) < HR_low or int(p["HR"]) > HR_high
    ]

    print("\nAbnormal Heart Rate Patients:")
    print("{:<10}{:<15}{:<12}{:<6}".format("ID", "Name", "DOB", "HR"))
    print("-" * 45)

    for p in abnormal_list:
        print("{:<10}{:<15}{:<12}{:<6}".format(
            p["patient_id"], p["name"], p["DOB"], p["HR"]
        ))

    print(f"\nTotal: {len(abnormal_list)}")


#count abnormal BP
def get_abnormal_BP(patient_list, sys_low=90, sys_high=140, dias_low=50, dias_high=100):
    abnormal_list = []
    for p in patient_list:
        systolic, diastolic = map(int, p["BP"].split("/"))
        if systolic < sys_low or systolic > sys_high or diastolic < dias_low or diastolic > dias_high:
            abnormal_list.append(p)
    return abnormal_list

def count_abnormal_BP(patient_list, sys_low=90, sys_high=150, dias_low=50, dias_high=100):
    return len(get_abnormal_BP(patient_list, sys_low, sys_high, dias_low, dias_high)) #len() count how many items are inside a list/string/char

def display_abnormal_BP(patient_list, sys_low=90, sys_high=150, dias_low=50, dias_high=100): #return a table of abnormal BP patients
    abnormal_list = get_abnormal_HR(patient_list)
    print(f"\nAbnormal HR count: {len(abnormal_list)}")
    print("{:<10}{:<15}{:<12}{:<6}".format("ID", "Name", "DOB", "HR"))
    print("-" * 45)
    for p in abnormal_list:
        print("{:<10}{:<15}{:<12}{:<6}".format(
            p["patient_id"], p["name"], p["DOB"], p["HR"]
        ))

RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def abnormal_summary(patient_list, HR_low=40, HR_high=110, sys_low=90, sys_high=150, dias_low=50, dias_high=100):
    if not patient_list:
        print("No patient record found :( Try again!)")
        return
    print(f"\n{'ID':<8}{'Name':<12}{'HR':<6}{'BP':<10}{'Status':<12}")

    for p in patient_list:
        hr = int(p["HR"])
        hr_display = f"{RED}{hr}{RESET}" if hr<HR_low or hr>HR_high else str(hr)

        systolic, diastolic = map(int, p['BP'].split('/'))
        systolic, diastolic = map(int, p['BP'].split('/'))
        if systolic < sys_low or systolic > sys_high or diastolic < dias_low or diastolic > dias_high:
            bp_display = f"{RED}{p['BP']}{RESET}"
        else:
            bp_display = p['BP']

        status = []
        if hr<HR_low or hr>HR_high:
            status.append ("HR abnormal!")
        if systolic<sys_low or systolic>sys_high or diastolic<dias_low or diastolic>dias_high:
            status.append ("BP abnormal!")
        status = ", ".join(status) if status else "Normal"

        print(f"{p['patient_id']:<8}{p[name]:<12}{hr_display:<6}{hr_display:<10}{bp_display:<10}{status:<12}")

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
            print(f"{patient['patient_id']:<8}{patient['name']:<12}{patient['DOB']:<12}{patient['HR']:<6}{patient['BP']:<10}{patient['Temp']:<6}")
            return
    print("\nNo patient found with that ID, try again!\n")

#main program
if __name__ == "__main__":
    print ("Welcome to Smart Record App :D")
    if __name__ == "__main__":
        patient_list = load_from_csv() #restores old record from csv
    
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
            add_patient(patient_list, patient_id, name, DOB, HR, BP, Temp)
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
            print("It's a good day to save lives! See you later!!")
            break
        else:
            print("This choice does not exist! Try Again :D")

#---------------------------------------- WEBPAGE GUI -------------------------------------------

#user input
def gui_add_patient(patient_list):
    patient_id = simpledialog.askstring("Input", "Patient ID: ") #first (window), second argument (question)
    name = simpledialog.askstring("Input", "Patient Name: ")
    DOB = simpledialog.askstring("Input", "Date of Birth: ")
    HR = simpledialog.askstring("Input", "Heart Rate: ")
    BP = simpledialog.askstring("Input", "Blood Pressure: ")
    Temp = simpledialog.askstring("Input", "Temperature: ")

    add_patient(patient_list, patient_id, name, DOB, HR, BP, Temp)

def gui_view_patients(patient_list):
    if not patient_list:
        messagebox.showinfo("Info", "No patient records found, try again!")
        return
    all_data = "" #initialize data first
    all_data += "-"*50 +"\n" #take char "-" and repeat *(x) time and \n add new line
    for p in patient_list:
        all_data += f"{p['patient_id']} | {p['name']} | {p['DOB']} | {p['HR']} | {p['BP']} | {p['Temp']}\n"
    messagebox.showinfo("All Patients", all_data)

def gui_search_patients(patient_list):
    search_id = simpledialog.askstring("Search", "Enter Patient ID: ") 
    for p in patient_list:
        if p["patient_id"] == search_id:
            info = f"{p['patient_id']} | {p['name']} | {p['DOB']}"
            messagebox.showinfo ("Patient Found", info)
            return
    messagebox.showerror("Patient Not Found, Try Again!")

def gui_abnormal_summary(patient_list):
    if not patient_list:
        messagebox.showinfo("Info", "No patient record found, Try Again!")
    
    RED = "\033[91m"
    summary = ""
    abnormal_bp_count = 0
    abnormal_hr_count = 0

    for p in patient_list:
        systolic, diastolic = map(int, p["BP"].split("/"))
        HR = int(p['HR'])

        abnormal_bp = systolic<90 or systolic >140 or diastolic<50 or diastolic>100
        abnormal_hr = HR>100 or HR<50

        if abnormal_bp:
            abnormal_bp_count +=1 #add 1 if match the criteria
        if abnormal_hr:
            abnormal_hr_count +=1
        
        if abnormal_bp or abnormal_hr:
            summary += f"{p['patient_id']} | {p['name']}" # (+=) add onto value/ continue value instead of overwriting it 
            if abnormal_bp:
                summary += f"BP: {p['BP']} ⚠️ " #p['--'] take value from '--' and f" string takes that value and put into a string
            else:
                summary += f"BP: {p['BP']}"
            if abnormal_hr:
                summary += f"HR: {p['HR']} ⚠️ "
            else:
                summary += f"HR: {p['HR']}"

        if not summary:
            summary = "All patients vitals are normal!!"
        summary += f"\nTotal abnormal BP: {abnormal_bp_count}\nTotal abnormal HR: {abnormal_hr_count}"

        messagebox.showinfo("Abnormal Summary", summary)


def gui_update_vitals(patient_list):
    update_id = simpledialog.askstring("Update", "Please enter new updates: ")
    update_vitals(patient_list, update_id)


def launch_gui(patient_list):
    root = tk.Tk()
    root.title("✨ Smart Record App ✨")
    root.geometry("700x500")
    root.configure(bg="#FFF0F5")
    
    #header
    tk.Label(root, text="Welcome to your Smart Record App ✨", font=("Helvetica", 18, "bold"), bg="#FFF0F5").pack(pady=10)
    
    #butttons
    tk.Button(root, text="Add New Patient", width=20, command=lambda: gui_add_patient(patient_list)).pack(pady=5)
    tk.Button(root, text="View Patients", width=20, command=lambda: gui_view_patients(patient_list)).pack(pady=5)
    tk.Button(root, text="Search Patient", width=20, command=lambda: gui_search_patients(patient_list)).pack(pady=5)
    tk.Button(root, text="Abnormal Summary", width=20, command=lambda: gui_abnormal_summary(patient_list)).pack(pady=5)
    tk.Button(root, text="Update New Vitals", width=20, command=lambda: gui_update_vitals(patient_list)).pack(pady=5)
    tk.Button(root, text="Exit", width=20, command=root.destroy).pack(pady=20)

    all_data = ""
    root.mainloop()
