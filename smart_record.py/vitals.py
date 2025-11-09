import csv
import os
from datetime import datetime
import time
import matplotlib.pyplot as plt
import json

RED = "\033[91m"
RESET = "\033[0m"

def typeprint(text, speed=0.05): #print function
        for char in text:
            print(char, end='', flush=True) #print without newline
            time.sleep(speed) #delay between chars
        print()

CSV_FILE = "patient_list.csv" #create a csv file
JSON_FILE = "patient_list.json"

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
def append_to_csv(patient, filename= "patient_list.csv"):
    #write header if file doesn't exist
    file_exists = os.path.isfile(filename) #checks if file exists
    
    with open(filename, "a", newline="")as file: #open in append mode 
        writer =csv.writer(file) #writer helper
        if not file_exists:
            writer.writerow(["patient_id", "name", "DOB", "HR", "BP", "Temp", "CC", "Diagnosis"])
        for p in patient_list:
            writer.writerow([
            patient["patient_id"], patient["name"], patient["DOB"],
            patient["HR"], patient["BP"], patient["Temp"],
            patient["CC"], patient["Diagnosis"], patient["RN_AP"]
        ])

def save_to_json(patient_list, filename= JSON_FILE):
    with open(filename, "a") as f:
        json.dump(patient_list, f, indent=4)

#------------------------------------ LOGISTICS -----------------------------

#add patient 
def add_patient(patient_list, patient_id, name, DOB, HR, BP, Temp, chief_complaint= "", diagnosis= "" ):
    RN_AP = input("Personel Initials: ")

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
        "CC" : chief_complaint,
        "Diagnosis": diagnosis,
        "RN_AP": RN_AP
    }

    patient_list.append(patient)
    append_to_csv(patient)
    save_to_json(patient)
    
    typeprint("\nNew Patient Added Successfully! 🎀")
    
    view_patients(patient_list)
    systolic, diastolic = map(int, BP.split ("/"))
    if int(HR) < 40 or int(HR) > 110 or systolic < 90 or systolic > 150 or diastolic < 50 or diastolic > 100:
        messagebox.showwarning("⚠️ Abnormal Vitals Alert", f"{name}'s vitals are abnormal!")

def save_data(patient_list, filename= 'patient_list.json'):
    with open(filename, "w") as f: #open write "w" mode as f (file nickname)
        json.dump(patient_list, f, indent = 4) #write data into file in JSON format , file writing into, indent
    typeprint("Data Saved!!!")

def load_data(filename='patient_list.json'):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return[]

#------------------------------ SEARCH/DISPLAY -------------------------------

#view all patients 
def view_patients(patient_list):
    if not patient_list:
        print ("No patient records yet")
        return

    print(f"{'patient_id':<12}{'name':<15}{'DOB':<15}{'HR':<10}{'BP':<12}{'Temp':<8}{'CC':<15}{'Diagnosis':<15}{'RN_AP':<6}")
    print("-" *80)

    for p in patient_list:
        systolic, diastolic = map(int, p["BP"].split('/')) #turning strings into integer and split at /
        
        #check for abnormality
        is_abnormal = (systolic >140 or systolic <90) or (diastolic >100 or diastolic <50)

        if is_abnormal: #boolean
            bp_display = f"{RED}{p['BP']}{RESET}"
        else:
            bp_display = p['BP'] #highlight significant data without affecting actual data

        typeprint(f"{p['patient_id']:<12}{p['name']:<15}{p['DOB']:<15}{p['HR']:<10}{bp_display:<12}{p['Temp']:<8}{p.get('CC',''):<15}{p.get('Diagnosis',''):<15}{p['RN_AP']:<6}")

#search pts by ID
def search_patient(patient_list, patient_id):
    for patient in patient_list:
        if patient["patient_id"] == patient_id:
            typeprint("\nPatient Record Found!!")

            print(f"{'ID':<10}{'Name':<15}{'DOB':<15}")
            typeprint(f"{patient['patient_id']:<10}{patient['name']:<15}{patient['DOB']:<15}")
            return
    typeprint("\nNo patient found with that ID, try again :D")

def display_patients(patient_list): #display pt.lists
    if not patient_list:
        messagebox.showinfo("Info", "No Patient Found, Try Again!")
        return 
    
    window = tk.Toplevel() #create a popup window on top of main app
    window.title("All Patients") 
    tree = ttk.Treeview(window, columns= ("ID", "name", "DOB", "HR", "BP", "Temp", "CC", "Diagnosis"), show="headings") #table Tkinter/ hide first empty column 
    for col in tree["column"]: #column names for table
        tree.heading(col, text=col)
        tree.column(col, width=100)
    for p in patient_list:
        tree.insert("", "end", values=(p["patient_id"], p["name"], p["DOB"], p["HR"], p["BP"], p["Temp"])) #insert a row in table at the end 
    tree.pack(expand=True, fill="both") #place table in window and stretch to fill 
    window.mainloop() #event loop for popup so it stays open instead of close instantly 

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
    typeprint("{:<10}{:<15}{:<15}{:<6}".format("ID", "Name", "DOB", "HR"))
    print("-" * 45)

    for p in abnormal_list:
        print("{:<10}{:<15}{:<15}{:<6}".format(
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
    print("{:<10}{:<15}{:<15}{:<6}".format("ID", "Name", "DOB", "HR"))
    print("-" * 45)
    for p in abnormal_list:
        typeprint("{:<10}{:<15}{:<15}{:<6}".format(
            p["patient_id"], p["name"], p["DOB"], p["HR"]
        ))

RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def abnormal_summary(patient_list, HR_low=40, HR_high=110, sys_low=90, sys_high=150, dias_low=50, dias_high=100):
    if not patient_list:
        print("No patient record found :( Try again!)")
        return
    typeprint(f"\n{'ID':<8}{'Name':<15}{'HR':<8}{'BP':<10}{'Status':<12}")

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

        typeprint(f"{p['patient_id']:<8}{p['name']:<12}{'DOB':<15}{hr_display:<10}{bp_display:<12}{status:<12}")

#------------------------------ EXPORT ----------------------------------------------
def export_report(patient_list, filename="report"):
    report = patient_list
    with open (filename, "w", newline=" ") as f:
        writer = csv.writer(f)
        writer.writerow(["ID","Name","DOB","HR","BP","Temp"])
        for p in report:
            writer.writerow([p["patient_id"], p["name"], p["DOB"], p["HR"], p["BP"], p["Temp"]])
        messagebox.showinfo("Export",f"Report saved as {filename}") 

#--------------------------------- UPDATE ----------------------------------------
#update patient vitals
def update_vitals(patient_list, patient_id):
    for patient in patient_list:
        if patient["patient_id"] == patient_id:
            typeprint("\nPatient Found! Go ahead and enter the updated vital!\n")

            new_HR = input("Updated Heart Rate: ")
            new_BP = input("Updated Blood Pressure: ")
            new_temp = input("Updated Temperature: ")
            new_diag = input("Updated Diagnosis: ")
            new_RN_AP = input("Personel Initials: ")

            new_Time = datetime.now().strftime("%I:%M %p")

            patient["HR"] = new_HR
            patient["BP"] = new_BP
            patient["Temp"] = new_temp
            patient["Time"] = new_Time
            patient["Diagnosis"] = new_diag
            patient["RN_AP"] = new_RN_AP

            append_to_csv(patient)
            typeprint("\nVitals updated successfully :D\n")
            typeprint(f"{patient['patient_id']:<8}{patient['name']:<12}{patient['DOB']:<15}{patient['HR']:<8}{patient['BP']:<12}{patient['Temp']:<8}{patient['CC']:<20}{patient['Diagnosis']:20}")
            return
    typeprint("\nNo patient found with that ID, try again!\n")

#------------------------------ TREND PLOT ------------------------------------
def plot_trend(patient_list, patient_id):
    patient_data = [p for p in patient_list if p['patient_id']== patient_id]
    if not patient_data:
        messagebox.showerror("Error!", "Patient not found, Try Again!")
        return
    
    times = [p["Time"] for p in patient_data]
    HRs = [p["HR"] for p in patient_data]
    BPs = [list(map(int, p["BP"].split("/"))) for p in patient_data]
    systolics = [bp[0] for bp in BPs]
    diastolics = [bp[1] for bp in BPs]

    plt.plot(times, HRs, label="HR") #draw a line graph of "x" over time (y)
    plt.plot(times, systolics, label="Systolic BP")
    plt.plot(times, diastolics, label="Diastolic BP")
    plt.xlabel("Time")
    plt.ylabel("Vitals")
    plt.title(f"Vitals Trend for Patient {patient_id}")
    plt.legend() #shows a key legend
    plt.show() #display
#------------------------------- MAIN PROGRAM ----------------------------------
def run_cli(patient_list):
    typeprint ("Welcome to Smart Record App :D")
    patient_list= load_from_csv() #restore old record 

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

#---------------------------------------- WEBPAGE GUI -------------------------------------------
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

#user input
def gui_add_patient(patient_list):
    patient_id = simpledialog.askstring("Input", "Patient ID: ") #first (window), second argument (question)
    name = simpledialog.askstring("Input", "Patient Name: ")
    DOB = simpledialog.askstring("Input", "Date of Birth: ")
    HR = simpledialog.askstring("Input", "Heart Rate: ")
    BP = simpledialog.askstring("Input", "Blood Pressure: ")
    Temp = simpledialog.askstring("Input", "Temperature: ")
    CC = simpledialog.askstring("Input", "Chief Complaints: ")
    Diagnosis = simpledialog.askstring("Input", "Patient Diagnosis: ")
    
    add_patient(patient_list, patient_id, name, DOB, HR, BP, Temp, CC, Diagnosis)

def gui_view_patients(patient_list):
    if not patient_list:
        messagebox.showinfo("Info", "No patient records found, try again!")
        return
    all_data = "" #initialize data first
    all_data += "-"*70 +"\n" #take char "-" and repeat *(x) time and \n add new line
    for p in patient_list:
        all_data += f"{p['patient_id']} | {p['name']} | {p['DOB']} | {p['HR']} | {p['BP']} | {p['Temp']} | {p['CC']} | {p['Diagnosis']} \n"
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

def gui_plot_trend(patient_list):
    patient_id = simpledialog.askstring ("Input", "Enter Patient ID for Chart") 
    plot_trend(patient_list, patient_id) #draws trend graph 
        #ask -> send answer -> graph

#--------------------------------------- GUI STYLE  --------------------------------------
def button_style(btn):
    btn.configure(
        bg="white",
        fg="#5E4A47",
        activebackground="#F6D7C2",
        activeforeground="#5E4A47",
        relief="groove",
        bd=3,
        font=("Helvetica Rounded", 12, "bold")
    )
    
def make_cute(btn):
    btn.config(bg="white", fg="#C47A88", relief="flat", bd=0, padx=12, pady=6, font=("Helvetica", 12))
    btn.bind("<Enter>", lambda e: btn.config(bg="#FFE5D9"))
    btn.bind("<Leave>", lambda e: btn.config(bg="white"))

#--------------------------------------- GUI LAUNCH --------------------------------------
from ttkbootstrap import Style
import ttkbootstrap as ttk
import tkinter as tk 

def launch_gui(patient_list):
    style = Style (theme="flatly")
    root = style.master
    root.title("✨ Smart Record App ✨")
    root.geometry("800x500")
    root.configure(bg="#FFF0F5")
    
    #header
    title_label = ttk.Label(root, text="✨ Welcome to your Smart Record App ✨", font=("Helvetica Rounded", 22, "bold"), bg="#FFF0F5", fg="#5E4A47").pack(pady=20)
    title_label.pack(pady=20)

    #butttons
    buttons = [
        ("Add New Patient", lambda: gui_add_patient(patient_list)),
        ("View Patients", lambda: gui_view_patients(patient_list)),
        ("Search Patient", lambda: gui_search_patients(patient_list)),
        ("Abnormal Summary", lambda: gui_abnormal_summary(patient_list)),
        ("Update New Vitals", lambda: gui_update_vitals(patient_list)),
        ("Export Report", lambda: export_report(patient_list)),
        ("Vitals Trend Chart", lambda: gui_plot_trend(patient_list)),
        ("Exit", root.destroy)
    ]

    for text, command in buttons:
        button_style(root, text, command)

    root.mainloop()

if __name__== "__main__":
    patient_list = load_from_csv() #load all stored pts into patient_list
    launch_gui(patient_list) #launch GUI