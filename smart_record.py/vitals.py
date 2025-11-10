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
CSV_HEADERS = ["patient_id", "name", "DOB", "HR", "BP", "Temp", "CC", "Diagnosis", "RN_AP", "Time"]

#list to store patients info
def load_from_csv(filename="patient_list.csv"):
    patient_list = [] #create an empty list to store dictionaries
    if os.path.isfile(filename): #check if file exist
        with open(filename, mode="r", newline="") as file: #open csv. in read "r" mode; reading each row as dictionary
            reader = csv.DictReader(file)
            for row in reader: #loop through each row
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
                patient_list.append(row) #add dictionary to list
    return patient_list

patient_list = load_from_csv()

#take data and save to .csv file 
def append_to_csv(patient, filename= "patient_list.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
        if not file_exists:
            writer.writeheader()
        row = {field: patient.get(field, "") for field in CSV_HEADERS}
        writer.writerow(row)

def save_to_json(patient_list, filename= JSON_FILE):
    with open(filename, "a") as f:
        json.dump(patient_list, f, indent=4)

#------------------------------------ LOGISTICS -----------------------------

#add patient 
def add_patient(patient_list, patient_id, name, DOB, HR, BP, Temp, chief_complaint= "", diagnosis= "", RN_AP=None ):
    if RN_AP is None:
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
        "RN_AP": RN_AP,
        "Time": Time
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
    
    window = ttk.Toplevel() #create a popup window on top of main app
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
import ttkbootstrap as ttk
from tkinter import messagebox, simpledialog, StringVar, PhotoImage

#user input
def gui_add_patient(patient_list):
    form = ttk.Toplevel()
    form.title("Add Patient ✨")
    form.geometry("460x620")
    form.resizable(False, False)
    form.grab_set()

    container = ttk.Frame(form, padding=24, style=STYLE_NAMES["home"])
    container.pack(fill="both", expand=True)

    ttk.Label(
        container,
        text="New Patient Intake 🌸",
        style=STYLE_NAMES["tab_heading"]
    ).pack(anchor="w")
    ttk.Label(
        container,
        text="Drop in vitals and quick notes below. Everything stays inside this cozy popup.",
        style=STYLE_NAMES["tab_body"],
        wraplength=380,
        justify="left"
    ).pack(anchor="w", pady=(0, 16))

    field_definitions = [
        ("Patient ID", "patient_id"),
        ("Patient Name", "name"),
        ("Date of Birth (MM/DD/YYYY)", "DOB"),
        ("Heart Rate", "HR"),
        ("Blood Pressure (e.g. 120/80)", "BP"),
        ("Temperature", "Temp"),
        ("Chief Complaint", "CC"),
        ("Diagnosis", "Diagnosis"),
        ("Personnel Initials", "RN_AP")
    ]

    form_vars = {}
    for label_text, key in field_definitions:
        field_frame = ttk.Frame(container, style=STYLE_NAMES["home"])
        field_frame.pack(fill="x", pady=6)
        ttk.Label(
            field_frame,
            text=label_text,
            style=STYLE_NAMES["tab_body"]
        ).pack(anchor="w")
        var = StringVar()
        ttk.Entry(field_frame, textvariable=var).pack(fill="x", pady=(4, 0))
        form_vars[key] = var

    def submit():
        values = {key: var.get().strip() for key, var in form_vars.items()}
        required_keys = ["patient_id", "name", "DOB", "HR", "BP", "Temp", "RN_AP"]
        missing = [key for key in required_keys if not values.get(key)]
        if missing:
            messagebox.showerror("Missing Info", "Please fill out all required fields before saving.")
            return
        add_patient(
            patient_list,
            values["patient_id"],
            values["name"],
            values["DOB"],
            values["HR"],
            values["BP"],
            values["Temp"],
            values.get("CC", ""),
            values.get("Diagnosis", ""),
            RN_AP=values["RN_AP"]
        )
        messagebox.showinfo("Success", "Patient added to the registry!")
        form.destroy()

    buttons_row = ttk.Frame(container, style=STYLE_NAMES["home"])
    buttons_row.pack(fill="x", pady=(20, 0))
    ttk.Button(
        buttons_row,
        text="Cancel",
        command=form.destroy,
        style=BUTTON_STYLE_NAMES["secondary"]
    ).pack(side="left", fill="x", expand=True, padx=(0, 8))
    ttk.Button(
        buttons_row,
        text="Save Patient",
        command=submit,
        style=BUTTON_STYLE_NAMES["primary"]
    ).pack(side="left", fill="x", expand=True)

def gui_view_patients(patient_list):
    if not patient_list:
        show_not_found_popup("No Patients Yet", "Once you add patients, they will appear in this pastel roster.")
        return

    window = ttk.Toplevel()
    window.title("Patient Roster 💖")
    window.geometry("820x520")
    window.resizable(False, False)
    window.grab_set()

    container = ttk.Frame(window, padding=24, style=STYLE_NAMES["home"])
    container.pack(fill="both", expand=True)

    ttk.Label(
        container,
        text="Patient Roster",
        style=STYLE_NAMES["tab_heading"]
    ).pack(anchor="w")
    ttk.Label(
        container,
        text="Browse every patient with their key vitals. Scroll for more and close when done.",
        style=STYLE_NAMES["tab_body"],
        wraplength=540,
        justify="left"
    ).pack(anchor="w", pady=(0, 16))

    columns = ("ID", "Name", "DOB", "HR", "BP", "Temp", "CC", "Diagnosis")
    table_frame = ttk.Frame(container, style=STYLE_NAMES["home"])
    table_frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
    for col in columns:
        tree.heading(col, text=col)
        width = 80 if col in ("ID", "HR", "Temp") else 110
        if col in ("CC", "Diagnosis"):
            width = 150
        tree.column(col, width=width, anchor="center")

    for p in patient_list:
        tree.insert("", "end", values=(
            p["patient_id"],
            p["name"],
            p["DOB"],
            p["HR"],
            p["BP"],
            p["Temp"],
            p.get("CC", ""),
            p.get("Diagnosis", "")
        ))

    y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=y_scroll.set)
    tree.pack(side="left", fill="both", expand=True)
    y_scroll.pack(side="right", fill="y")

    ttk.Button(
        container,
        text="Close",
        command=window.destroy,
        style=BUTTON_STYLE_NAMES["secondary"]
    ).pack(pady=14, ipadx=10)

def gui_search_patients(patient_list):
    search_id = simpledialog.askstring("Search", "Enter Patient ID: ") 
    if not search_id:
        return
    for p in patient_list:
        if p["patient_id"] == search_id:
            info = f"{p['patient_id']} | {p['name']} | {p['DOB']}"
            messagebox.showinfo ("Patient Found", info)
            return
    show_not_found_popup("Patient Not Found", "We couldn't find that patient ID. Double-check the digits or add a new record.")

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
THEME_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "dashboard_theme.json")
NOT_FOUND_LOGO = os.path.join(os.path.dirname(__file__), "app", "static", "not_found_logo.png")

DASHBOARD_THEMES = {
    "Pastel Blush": {
        "base_theme": "litera",
        "background": "#fff6fb",
        "banner": {"bg": "#ffd9ec", "fg": "#7d2b49", "sub_fg": "#a55173"},
        "panels": {
            "patient": {"bg": "#fff8fc", "label_bg": "#fcd6ea", "label_fg": "#7d2b49", "border": "#f5b6d0"},
            "monitor": {"bg": "#fff3f2", "label_bg": "#ffe0d7", "label_fg": "#8c3a2b", "border": "#f9c3b8"},
            "report": {"bg": "#fef8ff", "label_bg": "#f5daf7", "label_fg": "#6f3b7a", "border": "#e9c0f0"}
        },
        "text": {"primary": "#5c1d34", "muted": "#91606f"},
        "buttons": {
            "primary": {"bg": "#f48fb1", "hover": "#f7a7c2", "fg": "#5c1d34", "border": "#f06292"},
            "secondary": {"bg": "#ffe6f1", "hover": "#ffd6ea", "fg": "#6d3a4d", "border": "#f8bbd0"},
            "info": {"bg": "#fde7f3", "hover": "#fad5eb", "fg": "#7d2d4d", "border": "#f7c2dd"},
            "alert": {"bg": "#ffd2da", "hover": "#ffbac6", "fg": "#7c1d2a", "border": "#ff94a4"},
            "accent": {"bg": "#fbcfe8", "hover": "#f5badf", "fg": "#6a2441", "border": "#f48fb1"},
            "insight": {"bg": "#f8e7ff", "hover": "#f0d4ff", "fg": "#5b3173", "border": "#e7c2ff"},
            "success": {"bg": "#d7f5e9", "hover": "#c5f0df", "fg": "#285c4d", "border": "#a4dec7"},
            "danger": {"bg": "#ffc9de", "hover": "#ffb1cf", "fg": "#7c1d2a", "border": "#ff8fb8"}
        }
    },
    "Mint Sorbet": {
        "base_theme": "minty",
        "background": "#f5fffb",
        "banner": {"bg": "#d4f6ec", "fg": "#1f6657", "sub_fg": "#2f7d6b"},
        "panels": {
            "patient": {"bg": "#f1fffa", "label_bg": "#d1f4e5", "label_fg": "#1a5a4d", "border": "#a8e5cf"},
            "monitor": {"bg": "#eefcf5", "label_bg": "#c7f1df", "label_fg": "#2b6a5b", "border": "#9edec7"},
            "report": {"bg": "#f6fffb", "label_bg": "#d5f6ea", "label_fg": "#245c51", "border": "#b3ebd6"}
        },
        "text": {"primary": "#1d5f4f", "muted": "#3e7b6d"},
        "buttons": {
            "primary": {"bg": "#8be0c1", "hover": "#78d7b6", "fg": "#0f4437", "border": "#5ec9a5"},
            "secondary": {"bg": "#e0fff4", "hover": "#ccf7e7", "fg": "#215c4e", "border": "#b5efda"},
            "info": {"bg": "#cff5ff", "hover": "#b7ebfa", "fg": "#16526b", "border": "#9de0f3"},
            "alert": {"bg": "#ffe0c7", "hover": "#ffd0ab", "fg": "#7c3f18", "border": "#ffb880"},
            "accent": {"bg": "#c9f3e7", "hover": "#b2eadc", "fg": "#1f5f52", "border": "#9ddfce"},
            "insight": {"bg": "#e5ecff", "hover": "#d4ddff", "fg": "#2f3f7a", "border": "#b7c4ff"},
            "success": {"bg": "#c4f1d5", "hover": "#b0e7c7", "fg": "#1f5a35", "border": "#90d7ab"},
            "danger": {"bg": "#ffd6da", "hover": "#ffc1c7", "fg": "#7c1d28", "border": "#ffa0ad"}
        }
    },
    "Lilac Haze": {
        "base_theme": "pulse",
        "background": "#f7f3ff",
        "banner": {"bg": "#e7dbff", "fg": "#4b2a73", "sub_fg": "#6a3c9a"},
        "panels": {
            "patient": {"bg": "#fbf6ff", "label_bg": "#e8dbff", "label_fg": "#4b2a73", "border": "#cdb0f2"},
            "monitor": {"bg": "#fdf3ff", "label_bg": "#f2dcff", "label_fg": "#6a3c9a", "border": "#dcb8ff"},
            "report": {"bg": "#f6f1ff", "label_bg": "#e0d5ff", "label_fg": "#3f2a6b", "border": "#c3b0f0"}
        },
        "text": {"primary": "#4b2a73", "muted": "#6d4a93"},
        "buttons": {
            "primary": {"bg": "#c6a8ff", "hover": "#b795ff", "fg": "#351f5c", "border": "#a780ff"},
            "secondary": {"bg": "#efe8ff", "hover": "#e1d4ff", "fg": "#50327c", "border": "#d1bfff"},
            "info": {"bg": "#dfe7ff", "hover": "#cbd7ff", "fg": "#273e78", "border": "#b2c3ff"},
            "alert": {"bg": "#ffd7ed", "hover": "#ffc0e1", "fg": "#7a1f4d", "border": "#ff9fce"},
            "accent": {"bg": "#f3d9ff", "hover": "#e9c1ff", "fg": "#4f2478", "border": "#d8a6ff"},
            "insight": {"bg": "#d5e3ff", "hover": "#c0d3ff", "fg": "#1f3f7a", "border": "#a5c0ff"},
            "success": {"bg": "#dae8ff", "hover": "#c5d9ff", "fg": "#274164", "border": "#b3ccff"},
            "danger": {"bg": "#ffced9", "hover": "#ffb6c6", "fg": "#7c1d2a", "border": "#ff91a9"}
        }
    }
}

STYLE_NAMES = {
    "home": "DashboardHome.TFrame",
    "banner": "DashboardBanner.TFrame",
    "banner_title": "DashboardBannerTitle.TLabel",
    "banner_subtitle": "DashboardBannerSubtitle.TLabel",
    "patient_panel": "DashboardPatient.TLabelframe",
    "monitor_panel": "DashboardMonitor.TLabelframe",
    "report_panel": "DashboardReport.TLabelframe",
    "tab_heading": "DashboardTabHeading.TLabel",
    "tab_body": "DashboardBody.TLabel"
}

BUTTON_STYLE_NAMES = {
    "primary": "DashboardPrimary.TButton",
    "secondary": "DashboardSecondary.TButton",
    "info": "DashboardInfo.TButton",
    "alert": "DashboardAlert.TButton",
    "accent": "DashboardAccent.TButton",
    "insight": "DashboardInsight.TButton",
    "success": "DashboardSuccess.TButton",
    "danger": "DashboardDanger.TButton"
}

_NOT_FOUND_LOGO_IMAGE = None


def get_not_found_logo_image():
    """Lazy-load and cache the pastel not-found logo."""
    global _NOT_FOUND_LOGO_IMAGE
    if _NOT_FOUND_LOGO_IMAGE is None and os.path.exists(NOT_FOUND_LOGO):
        try:
            _NOT_FOUND_LOGO_IMAGE = PhotoImage(file=NOT_FOUND_LOGO)
        except Exception:
            _NOT_FOUND_LOGO_IMAGE = None
    return _NOT_FOUND_LOGO_IMAGE


def show_not_found_popup(title, message):
    """Display a custom popup with the pastel not-found logo and helpful text."""
    popup = ttk.Toplevel()
    popup.title(title)
    popup.geometry("420x420")
    popup.resizable(False, False)
    popup.grab_set()

    frame = ttk.Frame(popup, padding=24, style=STYLE_NAMES["home"])
    frame.pack(fill="both", expand=True)

    logo = get_not_found_logo_image()
    if logo:
        logo_label = ttk.Label(frame, image=logo)
        logo_label.image = logo
        logo_label.pack(pady=(0, 16))

    ttk.Label(
        frame,
        text=title,
        style=STYLE_NAMES["tab_heading"]
    ).pack(anchor="center", pady=(0, 8))
    ttk.Label(
        frame,
        text=message,
        style=STYLE_NAMES["tab_body"],
        wraplength=320,
        justify="center"
    ).pack(anchor="center")

    ttk.Button(
        frame,
        text="Close",
        command=popup.destroy,
        style=BUTTON_STYLE_NAMES["secondary"]
    ).pack(pady=20, ipadx=10)


def load_saved_theme(default_theme):
    """Return the saved theme if present, otherwise fall back to default."""
    try:
        with open(THEME_CONFIG_PATH, "r", encoding="utf-8") as config_file:
            data = json.load(config_file)
            saved_theme = data.get("theme")
            if saved_theme in DASHBOARD_THEMES:
                return saved_theme
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        pass
    return default_theme


def save_theme_choice(theme_name):
    """Persist the chosen theme so the dashboard opens with it next time."""
    try:
        with open(THEME_CONFIG_PATH, "w", encoding="utf-8") as config_file:
            json.dump({"theme": theme_name}, config_file, indent=2)
    except OSError:
        # Non-fatal; app can continue without saving.
        pass


def apply_dashboard_theme(style, root, theme_key):
    """Apply the selected pastel theme across frames, panels, and buttons."""
    theme = DASHBOARD_THEMES[theme_key]
    style.theme_use(theme["base_theme"])

    root.configure(bg=theme["background"])
    style.configure(STYLE_NAMES["home"], background=theme["background"])
    style.configure("TNotebook", padding=0)

    banner_colors = theme["banner"]
    style.configure(
        STYLE_NAMES["banner"],
        background=banner_colors["bg"],
        borderwidth=0,
        relief="flat"
    )
    style.configure(
        STYLE_NAMES["banner_title"],
        background=banner_colors["bg"],
        foreground=banner_colors["fg"],
        font=("Helvetica Rounded", 26, "bold")
    )
    style.configure(
        STYLE_NAMES["banner_subtitle"],
        background=banner_colors["bg"],
        foreground=banner_colors["sub_fg"],
        font=("Helvetica", 13)
    )

    text_colors = theme["text"]
    style.configure(
        STYLE_NAMES["tab_heading"],
        background=theme["background"],
        foreground=text_colors["primary"],
        font=("Helvetica Rounded", 16, "bold")
    )
    style.configure(
        STYLE_NAMES["tab_body"],
        background=theme["background"],
        foreground=text_colors["muted"],
        font=("Helvetica", 11)
    )

    for panel_name, labelframe_style in (
        ("patient", STYLE_NAMES["patient_panel"]),
        ("monitor", STYLE_NAMES["monitor_panel"]),
        ("report", STYLE_NAMES["report_panel"])
    ):
        palette = theme["panels"][panel_name]
        style.configure(
            labelframe_style,
            background=palette["bg"],
            bordercolor=palette["border"],
            relief="ridge",
            foreground=palette["label_fg"]
        )
        style.configure(
            f"{labelframe_style}.Label",
            background=palette["label_bg"],
            foreground=palette["label_fg"],
            font=("Helvetica Rounded", 13, "bold")
        )

    for role, style_name in BUTTON_STYLE_NAMES.items():
        palette = theme["buttons"][role]
        style.configure(
            style_name,
            background=palette["bg"],
            foreground=palette["fg"],
            bordercolor=palette["border"],
            focusthickness=1,
            focuscolor=palette["border"],
            padding=(16, 10),
            font=("Helvetica", 12, "bold")
        )
        style.map(
            style_name,
            background=[("active", palette["hover"]), ("pressed", palette["hover"])],
            foreground=[("disabled", "#a0a0a0")]
        )


def create_dashboard_button(parent, label, command, style_role):
    btn = ttk.Button(parent, text=label, command=command, style=BUTTON_STYLE_NAMES[style_role])
    btn.pack(fill="x", pady=6, ipady=2)
    return btn


#--------------------------------------- GUI LAUNCH --------------------------------------
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def launch_gui(patient_list):
    default_theme = "Pastel Blush"
    active_theme = load_saved_theme(default_theme)
    root = ttk.Window(
        title="✨ Smart Record App ✨",
        themename=DASHBOARD_THEMES[active_theme]["base_theme"]
    )
    root.geometry("980x640")

    style = ttk.Style()
    apply_dashboard_theme(style, root, active_theme)

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both", padx=16, pady=16)

    home_frame = ttk.Frame(notebook, padding=30, style=STYLE_NAMES["home"])
    patient_tab = ttk.Frame(notebook, padding=30, style=STYLE_NAMES["home"])
    abnormal_tab = ttk.Frame(notebook, padding=30, style=STYLE_NAMES["home"])
    export_tab = ttk.Frame(notebook, padding=30, style=STYLE_NAMES["home"])

    notebook.add(home_frame, text="🏠 Home")
    notebook.add(patient_tab, text="🩺 Patients")
    notebook.add(abnormal_tab, text="⚠️ Monitor")
    notebook.add(export_tab, text="📄 Export")

    banner = ttk.Frame(home_frame, padding=24, style=STYLE_NAMES["banner"])
    banner.pack(fill="x", pady=(0, 25))
    banner.columnconfigure(0, weight=1)

    ttk.Label(
        banner,
        text="Smart Record Nurse Station",
        style=STYLE_NAMES["banner_title"]
    ).grid(row=0, column=0, sticky="w")
    ttk.Label(
        banner,
        text="Soft pastels, quick actions, and gentle alerts for calmer charting 💖",
        style=STYLE_NAMES["banner_subtitle"]
    ).grid(row=1, column=0, sticky="w", pady=(6, 0))

    selector_container = ttk.Frame(banner, style=STYLE_NAMES["banner"])
    selector_container.grid(row=0, column=1, rowspan=2, sticky="e")
    ttk.Label(
        selector_container,
        text="Theme",
        style=STYLE_NAMES["banner_subtitle"]
    ).pack(side="left", padx=(0, 8))

    theme_var = StringVar(value=active_theme)
    theme_combo = ttk.Combobox(
        selector_container,
        textvariable=theme_var,
        values=list(DASHBOARD_THEMES.keys()),
        state="readonly",
        width=16
    )
    theme_combo.pack(side="left")

    panels_container = ttk.Frame(home_frame, style=STYLE_NAMES["home"])
    panels_container.pack(expand=True, fill="both")
    panels_container.columnconfigure((0, 1), weight=1, uniform="panel")

    patient_panel = ttk.Labelframe(
        panels_container,
        text="Patient Actions 🩺",
        padding=18,
        style=STYLE_NAMES["patient_panel"]
    )
    patient_panel.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")

    monitor_panel = ttk.Labelframe(
        panels_container,
        text="Vitals Monitor 💓",
        padding=18,
        style=STYLE_NAMES["monitor_panel"]
    )
    monitor_panel.grid(row=0, column=1, padx=12, pady=12, sticky="nsew")

    report_panel = ttk.Labelframe(
        panels_container,
        text="Reports & Tools 📋",
        padding=18,
        style=STYLE_NAMES["report_panel"]
    )
    report_panel.grid(row=1, column=0, columnspan=2, padx=12, pady=(0, 12), sticky="nsew")

    create_dashboard_button(
        patient_panel,
        "➕ Add New Patient",
        lambda: gui_add_patient(patient_list),
        style_role="primary"
    )
    create_dashboard_button(
        patient_panel,
        "📋 View Patients",
        lambda: gui_view_patients(patient_list),
        style_role="secondary"
    )
    create_dashboard_button(
        patient_panel,
        "🔍 Search Patient",
        lambda: gui_search_patients(patient_list),
        style_role="info"
    )

    create_dashboard_button(
        monitor_panel,
        "⚠️ Abnormal Summary",
        lambda: gui_abnormal_summary(patient_list),
        style_role="alert"
    )
    create_dashboard_button(
        monitor_panel,
        "🩺 Update Vitals",
        lambda: gui_update_vitals(patient_list),
        style_role="accent"
    )
    create_dashboard_button(
        monitor_panel,
        "📈 Vitals Trend Chart",
        lambda: gui_plot_trend(patient_list),
        style_role="insight"
    )

    create_dashboard_button(
        report_panel,
        "📤 Export Report",
        lambda: export_report(patient_list),
        style_role="success"
    )
    create_dashboard_button(
        report_panel,
        "❌ Exit",
        root.destroy,
        style_role="danger"
    )

    # Patient tab pastel panels
    patient_tab.columnconfigure(0, weight=1)
    patient_shortcuts = ttk.Labelframe(
        patient_tab,
        text="Daily Patient Shortcuts 🌼",
        padding=20,
        style=STYLE_NAMES["patient_panel"]
    )
    patient_shortcuts.pack(fill="x", pady=12)
    ttk.Label(
        patient_shortcuts,
        text="Add, review, or search charts from this cuddly corner. Buttons match the pastel theme so workflows stay calm and quick.",
        style=STYLE_NAMES["tab_body"],
        wraplength=520,
        justify="left"
    ).pack(pady=(0, 12))
    create_dashboard_button(
        patient_shortcuts,
        "➕ Register A New Patient",
        lambda: gui_add_patient(patient_list),
        style_role="primary"
    )
    create_dashboard_button(
        patient_shortcuts,
        "📋 Browse Patient List",
        lambda: gui_view_patients(patient_list),
        style_role="secondary"
    )
    create_dashboard_button(
        patient_shortcuts,
        "🔍 Search By ID",
        lambda: gui_search_patients(patient_list),
        style_role="info"
    )

    patient_notes = ttk.Labelframe(
        patient_tab,
        text="Team Notes & Reminders 📝",
        padding=20,
        style=STYLE_NAMES["report_panel"]
    )
    patient_notes.pack(fill="both", expand=True, pady=12)
    ttk.Label(
        patient_notes,
        text="Use the abnormal summary or export tools to capture daily huddles. Keep vitals trends handy for bedside updates.",
        style=STYLE_NAMES["tab_body"],
        wraplength=540,
        justify="left"
    ).pack(pady=(0, 8))
    create_dashboard_button(
        patient_notes,
        "⚠️ View Abnormal Summary",
        lambda: gui_abnormal_summary(patient_list),
        style_role="alert"
    )
    create_dashboard_button(
        patient_notes,
        "📈 Vitals Trend Chart",
        lambda: gui_plot_trend(patient_list),
        style_role="insight"
    )

    # Monitor tab panels
    abnormal_tab.columnconfigure(0, weight=1)
    vital_snapshot = ttk.Labelframe(
        abnormal_tab,
        text="Vitals Snapshot 💓",
        padding=20,
        style=STYLE_NAMES["monitor_panel"]
    )
    vital_snapshot.pack(fill="x", pady=12)
    ttk.Label(
        vital_snapshot,
        text="Track live alerts and refresh vitals here. Use the quick buttons to acknowledge alerts or jump right into updates.",
        style=STYLE_NAMES["tab_body"],
        wraplength=520,
        justify="left"
    ).pack(pady=(0, 10))
    create_dashboard_button(
        vital_snapshot,
        "🩺 Update Vitals",
        lambda: gui_update_vitals(patient_list),
        style_role="accent"
    )
    create_dashboard_button(
        vital_snapshot,
        "⚠️ Review Abnormal Metrics",
        lambda: gui_abnormal_summary(patient_list),
        style_role="alert"
    )

    monitor_reports = ttk.Labelframe(
        abnormal_tab,
        text="Monitoring Tools 📊",
        padding=20,
        style=STYLE_NAMES["report_panel"]
    )
    monitor_reports.pack(fill="both", expand=True, pady=12)
    ttk.Label(
        monitor_reports,
        text="Need a printable log? Export a pastel report or pull up the full roster to double-check anyone on watch.",
        style=STYLE_NAMES["tab_body"],
        wraplength=540,
        justify="left"
    ).pack(pady=(0, 10))
    create_dashboard_button(
        monitor_reports,
        "📤 Export Vitals Report",
        lambda: export_report(patient_list),
        style_role="success"
    )
    create_dashboard_button(
        monitor_reports,
        "📋 View Patient Table",
        lambda: gui_view_patients(patient_list),
        style_role="secondary"
    )

    # Export tab panels
    export_tab.columnconfigure(0, weight=1)
    export_guides = ttk.Labelframe(
        export_tab,
        text="Shareable Reports 🌸",
        padding=20,
        style=STYLE_NAMES["report_panel"]
    )
    export_guides.pack(fill="x", pady=12)
    ttk.Label(
        export_guides,
        text="Generate gentle pastel CSVs for handoff, or pull abnormal summaries before rounds. Everything stays soft and friendly.",
        style=STYLE_NAMES["tab_body"],
        wraplength=520,
        justify="left"
    ).pack(pady=(0, 12))
    create_dashboard_button(
        export_guides,
        "📄 Export Patient CSV",
        lambda: export_report(patient_list),
        style_role="success"
    )
    create_dashboard_button(
        export_guides,
        "⚠️ Abnormal Summary Snapshot",
        lambda: gui_abnormal_summary(patient_list),
        style_role="alert"
    )

    export_tools = ttk.Labelframe(
        export_tab,
        text="Reference Tools 🪄",
        padding=20,
        style=STYLE_NAMES["patient_panel"]
    )
    export_tools.pack(fill="both", expand=True, pady=12)
    ttk.Label(
        export_tools,
        text="Use the vitals chart to visualize heart and blood pressure trends before attaching files to email or EMR notes.",
        style=STYLE_NAMES["tab_body"],
        wraplength=540,
        justify="left"
    ).pack(pady=(0, 10))
    create_dashboard_button(
        export_tools,
        "📈 Open Vitals Trend",
        lambda: gui_plot_trend(patient_list),
        style_role="insight"
    )
    create_dashboard_button(
        export_tools,
        "❌ Close Dashboard",
        root.destroy,
        style_role="danger"
    )

    def on_theme_change(_event=None):
        selected_theme = theme_var.get()
        apply_dashboard_theme(style, root, selected_theme)
        save_theme_choice(selected_theme)

    theme_combo.bind("<<ComboboxSelected>>", on_theme_change)
    on_theme_change()

    root.mainloop()

if __name__== "__main__":
    patient_list = load_from_csv() #load all stored pts into patient_list
    launch_gui(patient_list) #launch GUI
