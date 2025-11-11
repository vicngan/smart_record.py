import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, StringVar, PhotoImage

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from patient_ops import (
    add_patient,
    create_handoff_summary,
    export_report,
    plot_abnormal_overview,
    plot_trend,
    update_vitals,
)
from tasks import add_task, delete_task, load_tasks, save_tasks, tasks_for_patient, toggle_task

BASE_DIR = os.path.dirname(__file__)
THEME_CONFIG_PATH = os.path.join(BASE_DIR, "dashboard_theme.json")
NOT_FOUND_LOGO = os.path.join(BASE_DIR, "app", "static", "not_found_logo.png")
APP_LOGO = os.path.join(BASE_DIR, "app", "static", "app_logo.png")

DASHBOARD_THEMES = {
    "Pastel Blush": {
        "base_theme": "litera",
        "background": "#fff6fb",
        "banner": {"bg": "#ffd9ec", "fg": "#7d2b49", "sub_fg": "#a55173"},
        "panels": {
            "patient": {"bg": "#fff8fc", "label_bg": "#fcd6ea", "label_fg": "#7d2b49", "border": "#f5b6d0"},
            "monitor": {"bg": "#fff3f2", "label_bg": "#ffe0d7", "label_fg": "#8c3a2b", "border": "#f9c3b8"},
            "report": {"bg": "#fef8ff", "label_bg": "#f5daf7", "label_fg": "#6f3b7a", "border": "#e9c0f0"},
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
            "danger": {"bg": "#ffc9de", "hover": "#ffb1cf", "fg": "#7c1d2a", "border": "#ff8fb8"},
        },
    },
    "Mint Sorbet": {
        "base_theme": "minty",
        "background": "#f5fffb",
        "banner": {"bg": "#d4f6ec", "fg": "#1f6657", "sub_fg": "#2f7d6b"},
        "panels": {
            "patient": {"bg": "#f1fffa", "label_bg": "#d1f4e5", "label_fg": "#1a5a4d", "border": "#a8e5cf"},
            "monitor": {"bg": "#eefcf5", "label_bg": "#c7f1df", "label_fg": "#2b6a5b", "border": "#9edec7"},
            "report": {"bg": "#f6fffb", "label_bg": "#d5f6ea", "label_fg": "#245c51", "border": "#b3ebd6"},
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
            "danger": {"bg": "#ffd6da", "hover": "#ffc1c7", "fg": "#7c1d28", "border": "#ffa0ad"},
        },
    },
    "Lilac Haze": {
        "base_theme": "pulse",
        "background": "#f7f3ff",
        "banner": {"bg": "#e7dbff", "fg": "#4b2a73", "sub_fg": "#6a3c9a"},
        "panels": {
            "patient": {"bg": "#fbf6ff", "label_bg": "#e8dbff", "label_fg": "#4b2a73", "border": "#cdb0f2"},
            "monitor": {"bg": "#fdf3ff", "label_bg": "#f2dcff", "label_fg": "#6a3c9a", "border": "#dcb8ff"},
            "report": {"bg": "#f6f1ff", "label_bg": "#e0d5ff", "label_fg": "#3f2a6b", "border": "#c3b0f0"},
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
            "danger": {"bg": "#ffced9", "hover": "#ffb6c6", "fg": "#7c1d2a", "border": "#ff91a9"},
        },
    },
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
    "tab_body": "DashboardBody.TLabel",
}

BUTTON_STYLE_NAMES = {
    "primary": "DashboardPrimary.TButton",
    "secondary": "DashboardSecondary.TButton",
    "info": "DashboardInfo.TButton",
    "alert": "DashboardAlert.TButton",
    "accent": "DashboardAccent.TButton",
    "insight": "DashboardInsight.TButton",
    "success": "DashboardSuccess.TButton",
    "danger": "DashboardDanger.TButton",
}

_NOT_FOUND_LOGO_IMAGE = None
_APP_LOGO_IMAGE = None


def get_not_found_logo_image():
    global _NOT_FOUND_LOGO_IMAGE
    if _NOT_FOUND_LOGO_IMAGE is None and os.path.exists(NOT_FOUND_LOGO):
        try:
            _NOT_FOUND_LOGO_IMAGE = PhotoImage(file=NOT_FOUND_LOGO)
        except Exception:
            _NOT_FOUND_LOGO_IMAGE = None
    return _NOT_FOUND_LOGO_IMAGE


def get_app_logo_image():
    global _APP_LOGO_IMAGE
    if _APP_LOGO_IMAGE is None and os.path.exists(APP_LOGO):
        try:
            _APP_LOGO_IMAGE = PhotoImage(file=APP_LOGO)
        except Exception:
            _APP_LOGO_IMAGE = None
    return _APP_LOGO_IMAGE


def show_not_found_popup(title, message):
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

    ttk.Label(frame, text=title, style=STYLE_NAMES["tab_heading"]).pack(anchor="center", pady=(0, 8))
    ttk.Label(
        frame,
        text=message,
        style=STYLE_NAMES["tab_body"],
        wraplength=320,
        justify="center",
    ).pack(anchor="center")

    ttk.Button(frame, text="Close", command=popup.destroy, style=BUTTON_STYLE_NAMES["secondary"]).pack(pady=20, ipadx=10)


def load_saved_theme(default_theme):
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
    try:
        with open(THEME_CONFIG_PATH, "w", encoding="utf-8") as config_file:
            json.dump({"theme": theme_name}, config_file, indent=2)
    except OSError:
        pass


def apply_dashboard_theme(style, root, theme_key):
    theme = DASHBOARD_THEMES[theme_key]
    style.theme_use(theme["base_theme"])

    root.configure(bg=theme["background"])
    style.configure(STYLE_NAMES["home"], background=theme["background"])
    style.configure("TNotebook", padding=0)

    banner_colors = theme["banner"]
    style.configure(STYLE_NAMES["banner"], background=banner_colors["bg"], borderwidth=0, relief="flat")
    style.configure(
        STYLE_NAMES["banner_title"],
        background=banner_colors["bg"],
        foreground=banner_colors["fg"],
        font=("Helvetica Rounded", 26, "bold"),
    )
    style.configure(
        STYLE_NAMES["banner_subtitle"],
        background=banner_colors["bg"],
        foreground=banner_colors["sub_fg"],
        font=("Helvetica", 13),
    )

    text_colors = theme["text"]
    style.configure(
        STYLE_NAMES["tab_heading"],
        background=theme["background"],
        foreground=text_colors["primary"],
        font=("Helvetica Rounded", 16, "bold"),
    )
    style.configure(
        STYLE_NAMES["tab_body"],
        background=theme["background"],
        foreground=text_colors["muted"],
        font=("Helvetica", 11),
    )

    for panel_name, labelframe_style in (
        ("patient", STYLE_NAMES["patient_panel"]),
        ("monitor", STYLE_NAMES["monitor_panel"]),
        ("report", STYLE_NAMES["report_panel"]),
    ):
        palette = theme["panels"][panel_name]
        style.configure(
            labelframe_style,
            background=palette["bg"],
            bordercolor=palette["border"],
            relief="ridge",
            foreground=palette["label_fg"],
        )
        style.configure(
            f"{labelframe_style}.Label",
            background=palette["label_bg"],
            foreground=palette["label_fg"],
            font=("Helvetica Rounded", 13, "bold"),
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
            font=("Helvetica", 12, "bold"),
        )
        style.map(
            style_name,
            background=[("active", palette["hover"]), ("pressed", palette["hover"])],
            foreground=[("disabled", "#a0a0a0")],
        )


def create_dashboard_button(parent, label, command, style_role):
    btn = ttk.Button(parent, text=label, command=command, style=BUTTON_STYLE_NAMES[style_role])
    btn.pack(fill="x", pady=6, ipady=2)
    return btn


def gui_add_patient(patient_list):
    form = ttk.Toplevel()
    form.title("Add Patient ✨")
    form.geometry("520x640")
    form.minsize(420, 520)
    form.resizable(True, True)
    form.grab_set()

    outer = ttk.Frame(form, padding=24, style=STYLE_NAMES["home"])
    outer.pack(fill="both", expand=True)

    bg_color = ttk.Style().lookup(STYLE_NAMES["home"], "background") or "#ffffff"
    canvas = tk.Canvas(outer, highlightthickness=0, bg=bg_color)
    y_scroll = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    scroll_frame = ttk.Frame(canvas, style=STYLE_NAMES["home"])

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=y_scroll.set)

    canvas.pack(side="left", fill="both", expand=True)
    y_scroll.pack(side="right", fill="y")

    ttk.Label(scroll_frame, text="New Patient Intake 🌸", style=STYLE_NAMES["tab_heading"]).pack(anchor="w")
    ttk.Label(
        scroll_frame,
        text="Drop in vitals and quick notes below. Everything stays inside this cozy popup.",
        style=STYLE_NAMES["tab_body"],
        wraplength=380,
        justify="left",
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
        ("Personnel Initials", "RN_AP"),
    ]

    form_vars = {}
    for label_text, key in field_definitions:
        field_frame = ttk.Frame(scroll_frame, style=STYLE_NAMES["home"])
        field_frame.pack(fill="x", pady=6)
        ttk.Label(field_frame, text=label_text, style=STYLE_NAMES["tab_body"]).pack(anchor="w")
        var = StringVar()
        ttk.Entry(field_frame, textvariable=var).pack(fill="x", pady=(4, 0))
        form_vars[key] = var

    def submit():
        values = {key: var.get().strip() for key, var in form_vars.items()}
        required_keys = ["patient_id", "name", "DOB", "HR", "BP", "Temp", "RN_AP"]
        if any(not values.get(key) for key in required_keys):
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
            RN_AP=values["RN_AP"],
        )
        messagebox.showinfo("Success", "Patient added to the registry!")
        form.destroy()

    buttons_row = ttk.Frame(outer, style=STYLE_NAMES["home"])
    buttons_row.pack(fill="x", pady=(16, 0))
    ttk.Button(buttons_row, text="Cancel", command=form.destroy, style=BUTTON_STYLE_NAMES["secondary"]).pack(
        fill="x", pady=(0, 8)
    )
    ttk.Button(
        buttons_row,
        text="💾 Save Patient",
        command=submit,
        style=BUTTON_STYLE_NAMES["success"],
    ).pack(fill="x")


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

    ttk.Label(container, text="Patient Roster", style=STYLE_NAMES["tab_heading"]).pack(anchor="w")
    ttk.Label(
        container,
        text="Browse every patient with their key vitals. Scroll for more and close when done.",
        style=STYLE_NAMES["tab_body"],
        wraplength=540,
        justify="left",
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
        tree.insert(
            "",
            "end",
            values=(
                p["patient_id"],
                p["name"],
                p["DOB"],
                p["HR"],
                p["BP"],
                p["Temp"],
                p.get("CC", ""),
                p.get("Diagnosis", ""),
            ),
        )

    y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=y_scroll.set)
    tree.pack(side="left", fill="both", expand=True)
    y_scroll.pack(side="right", fill="y")

    ttk.Button(container, text="Close", command=window.destroy, style=BUTTON_STYLE_NAMES["secondary"]).pack(
        pady=14, ipadx=10
    )


def gui_search_patients(patient_list):
    search_id = simpledialog.askstring("Search", "Enter Patient ID: ")
    if not search_id:
        return
    for p in patient_list:
        if p["patient_id"] == search_id:
            info = f"{p['patient_id']} | {p['name']} | {p['DOB']}"
            messagebox.showinfo("Patient Found", info)
            return
    show_not_found_popup("Patient Not Found", "We couldn't find that patient ID. Double-check the digits or add a new record.")


def gui_abnormal_summary(patient_list):
    if not patient_list:
        messagebox.showinfo("Info", "No patient record found, Try Again!")
        return

    summary = ""
    abnormal_bp_count = 0
    abnormal_hr_count = 0

    for p in patient_list:
        systolic, diastolic = map(int, p["BP"].split("/"))
        HR = int(p["HR"])

        abnormal_bp = systolic < 90 or systolic > 140 or diastolic < 50 or diastolic > 100
        abnormal_hr = HR > 100 or HR < 50

        if abnormal_bp:
            abnormal_bp_count += 1
        if abnormal_hr:
            abnormal_hr_count += 1

        if abnormal_bp or abnormal_hr:
            summary += f"{p['patient_id']} | {p['name']}"
            summary += f" BP: {p['BP']} {'⚠️ ' if abnormal_bp else ''}"
            summary += f" HR: {p['HR']} {'⚠️ ' if abnormal_hr else ''}\n"

    if not summary:
        summary = "All patients vitals are normal!!"

    summary += f"\nTotal abnormal BP: {abnormal_bp_count}\nTotal abnormal HR: {abnormal_hr_count}"
    messagebox.showinfo("Abnormal Summary", summary)


def gui_update_vitals(patient_list):
    update_id = simpledialog.askstring("Update", "Please enter new updates: ")
    if update_id:
        update_vitals(patient_list, update_id)


def gui_plot_trend(patient_list):
    patient_id = simpledialog.askstring("Input", "Enter Patient ID for Chart")
    if patient_id:
        plot_trend(patient_list, patient_id)


def gui_scan_barcode(patient_list):
    scanned = simpledialog.askstring("Scan Barcode", "Scan or enter the patient barcode/ID:")
    if not scanned:
        return
    scanned = scanned.strip()
    patient = next((p for p in patient_list if p["patient_id"] == scanned), None)
    if patient:
        info = (
            f"{patient['patient_id']} • {patient['name']}\n"
            f"DOB: {patient['DOB']} | HR: {patient['HR']} | BP: {patient['BP']} | Temp: {patient['Temp']}\n"
            f"Diagnosis: {patient.get('Diagnosis','')}"
        )
        messagebox.showinfo("Patient Found", info)
    else:
        show_not_found_popup("Not Found", "No patient matches that barcode/ID. Try scanning again.")


def show_handoff_summary_popup(patient_list, tasks):
    summary = create_handoff_summary(patient_list, tasks)
    window = ttk.Toplevel()
    window.title("Handoff Summary 🧾")
    window.geometry("640x520")
    window.grab_set()

    container = ttk.Frame(window, padding=16, style=STYLE_NAMES["home"])
    container.pack(fill="both", expand=True)

    text_widget = tk.Text(container, wrap="word", font=("Helvetica", 12))
    text_widget.insert("1.0", summary)
    text_widget.configure(state="disabled")
    text_widget.pack(fill="both", expand=True)

    ttk.Button(container, text="Close", command=window.destroy, style=BUTTON_STYLE_NAMES["secondary"]).pack(pady=10)


def open_task_center(patient_list, tasks):
    window = ttk.Toplevel()
    window.title("Task & Reminder Center ✅")
    window.geometry("720x520")
    window.grab_set()

    container = ttk.Frame(window, padding=16, style=STYLE_NAMES["home"])
    container.pack(fill="both", expand=True)

    columns = ("id", "patient", "description", "due", "status")
    tree = ttk.Treeview(container, columns=columns, show="headings", height=12)
    for col in columns:
        width = 80 if col == "id" else 140
        tree.heading(col, text=col.title())
        tree.column(col, width=width, anchor="center")
    tree.pack(fill="both", expand=True, pady=(0, 12))

    def resolve_name(patient_id):
        patient = next((p for p in patient_list if p["patient_id"] == patient_id), None)
        return f"{patient_id} - {patient['name']}" if patient else patient_id

    def refresh_tree():
        for row in tree.get_children():
            tree.delete(row)
        for task in tasks:
            tree.insert(
                "",
                "end",
                values=(
                    task["id"],
                    resolve_name(task["patient_id"]),
                    task["description"],
                    task.get("due", ""),
                    task.get("status", "pending"),
                ),
            )

    form_frame = ttk.Frame(container, style=STYLE_NAMES["home"])
    form_frame.pack(fill="x", pady=8)

    ttk.Label(form_frame, text="Patient ID", style=STYLE_NAMES["tab_body"]).grid(row=0, column=0, sticky="w")
    patient_var = StringVar()
    ttk.Entry(form_frame, textvariable=patient_var).grid(row=1, column=0, sticky="ew", padx=(0, 8))

    ttk.Label(form_frame, text="Task Description", style=STYLE_NAMES["tab_body"]).grid(row=0, column=1, sticky="w")
    desc_var = StringVar()
    ttk.Entry(form_frame, textvariable=desc_var).grid(row=1, column=1, sticky="ew", padx=(0, 8))

    ttk.Label(form_frame, text="Due Time (optional)", style=STYLE_NAMES["tab_body"]).grid(row=0, column=2, sticky="w")
    due_var = StringVar()
    ttk.Entry(form_frame, textvariable=due_var).grid(row=1, column=2, sticky="ew")

    form_frame.columnconfigure((0, 1, 2), weight=1)

    def add_task_action():
        patient_id = patient_var.get().strip()
        description = desc_var.get().strip()
        if not patient_id or not description:
            messagebox.showerror("Missing data", "Please enter both patient ID and description.")
            return
        if not any(p["patient_id"] == patient_id for p in patient_list):
            messagebox.showerror("Unknown Patient", "That patient ID does not exist yet.")
            return
        add_task(tasks, patient_id, description, due_var.get().strip())
        refresh_tree()
        patient_var.set("")
        desc_var.set("")
        due_var.set("")

    def toggle_selected():
        selection = tree.selection()
        if not selection:
            return
        task_id = tree.item(selection[0], "values")[0]
        toggle_task(tasks, task_id)
        refresh_tree()

    def delete_selected():
        selection = tree.selection()
        if not selection:
            return
        task_id = tree.item(selection[0], "values")[0]
        delete_task(tasks, task_id)
        refresh_tree()

    button_frame = ttk.Frame(container, style=STYLE_NAMES["home"])
    button_frame.pack(fill="x", pady=4)
    ttk.Button(button_frame, text="Add Task", command=add_task_action, style=BUTTON_STYLE_NAMES["primary"]).pack(
        side="left", padx=4
    )
    ttk.Button(button_frame, text="Toggle Done", command=toggle_selected, style=BUTTON_STYLE_NAMES["accent"]).pack(
        side="left", padx=4
    )
    ttk.Button(button_frame, text="Delete Task", command=delete_selected, style=BUTTON_STYLE_NAMES["danger"]).pack(
        side="left", padx=4
    )

    refresh_tree()


def launch_gui(patient_list, tasks=None):
    tasks = tasks or []
    default_theme = "Pastel Blush"
    active_theme = load_saved_theme(default_theme)
    root = ttk.Window(title="✨ Smart Record App ✨", themename=DASHBOARD_THEMES[active_theme]["base_theme"])
    root.geometry("980x640")

    style = ttk.Style()
    apply_dashboard_theme(style, root, active_theme)
    app_logo = get_app_logo_image()
    if app_logo:
        root.iconphoto(False, app_logo)
        root._app_logo = app_logo  # keep reference

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

    title_row = ttk.Frame(banner, style=STYLE_NAMES["banner"])
    title_row.grid(row=0, column=0, sticky="w")
    if app_logo:
        ttk.Label(title_row, image=app_logo).pack(side="left", padx=(0, 12))
    ttk.Label(title_row, text="Smart Record Nurse Station", style=STYLE_NAMES["banner_title"]).pack(side="left")
    ttk.Label(
        banner,
        text="Soft pastels, quick actions, and gentle alerts for calmer charting 💖",
        style=STYLE_NAMES["banner_subtitle"],
    ).grid(row=1, column=0, sticky="w", pady=(6, 0))

    selector_container = ttk.Frame(banner, style=STYLE_NAMES["banner"])
    selector_container.grid(row=0, column=1, rowspan=2, sticky="e")
    ttk.Label(selector_container, text="Theme", style=STYLE_NAMES["banner_subtitle"]).pack(side="left", padx=(0, 8))

    theme_var = StringVar(value=active_theme)
    theme_combo = ttk.Combobox(
        selector_container,
        textvariable=theme_var,
        values=list(DASHBOARD_THEMES.keys()),
        state="readonly",
        width=16,
    )
    theme_combo.pack(side="left")

    panels_container = ttk.Frame(home_frame, style=STYLE_NAMES["home"])
    panels_container.pack(expand=True, fill="both")
    panels_container.columnconfigure((0, 1), weight=1, uniform="panel")

    patient_panel = ttk.Labelframe(
        panels_container,
        text="Patient Actions 🩺",
        padding=18,
        style=STYLE_NAMES["patient_panel"],
    )
    patient_panel.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")

    monitor_panel = ttk.Labelframe(
        panels_container,
        text="Vitals Monitor 💓",
        padding=18,
        style=STYLE_NAMES["monitor_panel"],
    )
    monitor_panel.grid(row=0, column=1, padx=12, pady=12, sticky="nsew")

    report_panel = ttk.Labelframe(
        panels_container,
        text="Reports & Tools 📋",
        padding=18,
        style=STYLE_NAMES["report_panel"],
    )
    report_panel.grid(row=1, column=0, columnspan=2, padx=12, pady=(0, 12), sticky="nsew")

    create_dashboard_button(patient_panel, "➕ Add New Patient", lambda: gui_add_patient(patient_list), style_role="primary")
    create_dashboard_button(patient_panel, "📋 View Patients", lambda: gui_view_patients(patient_list), style_role="secondary")
    create_dashboard_button(patient_panel, "🔍 Search Patient", lambda: gui_search_patients(patient_list), style_role="info")
    create_dashboard_button(patient_panel, "🧾 Scan Barcode/ID", lambda: gui_scan_barcode(patient_list), style_role="accent")

    create_dashboard_button(
        monitor_panel, "⚠️ Abnormal Summary", lambda: gui_abnormal_summary(patient_list), style_role="alert"
    )
    create_dashboard_button(monitor_panel, "🩺 Update Vitals", lambda: gui_update_vitals(patient_list), style_role="accent")
    create_dashboard_button(
        monitor_panel, "📈 Vitals Trend Chart", lambda: gui_plot_trend(patient_list), style_role="insight"
    )
    create_dashboard_button(
        monitor_panel, "📊 Abnormal Vitals Chart", lambda: plot_abnormal_overview(patient_list), style_role="info"
    )

    create_dashboard_button(
        report_panel, "📤 Export Report", lambda: export_report(patient_list), style_role="success"
    )
    create_dashboard_button(
        report_panel, "🧾 Handoff Summary", lambda: show_handoff_summary_popup(patient_list, tasks), style_role="info"
    )
    create_dashboard_button(
        report_panel, "✅ Task Reminders", lambda: open_task_center(patient_list, tasks), style_role="accent"
    )
    create_dashboard_button(report_panel, "❌ Exit", root.destroy, style_role="danger")

    def build_patient_tab():
        patient_tab.columnconfigure(0, weight=1)
        patient_shortcuts = ttk.Labelframe(
            patient_tab,
            text="Daily Patient Shortcuts 🌼",
            padding=20,
            style=STYLE_NAMES["patient_panel"],
        )
        patient_shortcuts.pack(fill="x", pady=12)
        ttk.Label(
            patient_shortcuts,
            text="Add, review, or search charts from this cuddly corner. Buttons match the pastel theme so workflows stay calm and quick.",
            style=STYLE_NAMES["tab_body"],
            wraplength=520,
            justify="left",
        ).pack(pady=(0, 12))
        create_dashboard_button(
            patient_shortcuts, "➕ Register A New Patient", lambda: gui_add_patient(patient_list), style_role="primary"
        )
        create_dashboard_button(
            patient_shortcuts, "📋 Browse Patient List", lambda: gui_view_patients(patient_list), style_role="secondary"
        )
        create_dashboard_button(
            patient_shortcuts, "🔍 Search By ID", lambda: gui_search_patients(patient_list), style_role="info"
        )

        patient_notes = ttk.Labelframe(
            patient_tab,
            text="Team Notes & Reminders 📝",
            padding=20,
            style=STYLE_NAMES["report_panel"],
        )
        patient_notes.pack(fill="both", expand=True, pady=12)
        ttk.Label(
            patient_notes,
            text="Use the abnormal summary or export tools to capture daily huddles. Keep vitals trends handy for bedside updates.",
            style=STYLE_NAMES["tab_body"],
            wraplength=540,
            justify="left",
        ).pack(pady=(0, 8))
        create_dashboard_button(
            patient_notes, "⚠️ View Abnormal Summary", lambda: gui_abnormal_summary(patient_list), style_role="alert"
        )
        create_dashboard_button(
            patient_notes, "📈 Vitals Trend Chart", lambda: gui_plot_trend(patient_list), style_role="insight"
        )

    def build_monitor_tab():
        abnormal_tab.columnconfigure(0, weight=1)
        vital_snapshot = ttk.Labelframe(
            abnormal_tab,
            text="Vitals Snapshot 💓",
            padding=20,
            style=STYLE_NAMES["monitor_panel"],
        )
        vital_snapshot.pack(fill="x", pady=12)
        ttk.Label(
            vital_snapshot,
            text="Track live alerts and refresh vitals here. Use the quick buttons to acknowledge alerts or jump right into updates.",
            style=STYLE_NAMES["tab_body"],
            wraplength=520,
            justify="left",
        ).pack(pady=(0, 10))
        create_dashboard_button(
            vital_snapshot, "🩺 Update Vitals", lambda: gui_update_vitals(patient_list), style_role="accent"
        )
        create_dashboard_button(
            vital_snapshot, "⚠️ Review Abnormal Metrics", lambda: gui_abnormal_summary(patient_list), style_role="alert"
        )

        monitor_reports = ttk.Labelframe(
            abnormal_tab,
            text="Monitoring Tools 📊",
            padding=20,
            style=STYLE_NAMES["report_panel"],
        )
        monitor_reports.pack(fill="both", expand=True, pady=12)
        ttk.Label(
            monitor_reports,
            text="Need a printable log? Export a pastel report or pull up the full roster to double-check anyone on watch.",
            style=STYLE_NAMES["tab_body"],
            wraplength=540,
            justify="left",
        ).pack(pady=(0, 10))
        create_dashboard_button(
            monitor_reports, "📤 Export Vitals Report", lambda: export_report(patient_list), style_role="success"
        )
        create_dashboard_button(
            monitor_reports, "📋 View Patient Table", lambda: gui_view_patients(patient_list), style_role="secondary"
        )

    def build_export_tab():
        export_tab.columnconfigure(0, weight=1)
        export_guides = ttk.Labelframe(
            export_tab,
            text="Shareable Reports 🌸",
            padding=20,
            style=STYLE_NAMES["report_panel"],
        )
        export_guides.pack(fill="x", pady=12)
        ttk.Label(
            export_guides,
            text="Generate gentle pastel CSVs for handoff, or pull abnormal summaries before rounds. Everything stays soft and friendly.",
            style=STYLE_NAMES["tab_body"],
            wraplength=520,
            justify="left",
        ).pack(pady=(0, 12))
        create_dashboard_button(
            export_guides, "📄 Export Patient CSV", lambda: export_report(patient_list), style_role="success"
        )
        create_dashboard_button(
            export_guides,
            "⚠️ Abnormal Summary Snapshot",
            lambda: gui_abnormal_summary(patient_list),
            style_role="alert",
        )

        export_tools = ttk.Labelframe(
            export_tab,
            text="Reference Tools 🪄",
            padding=20,
            style=STYLE_NAMES["patient_panel"],
        )
        export_tools.pack(fill="both", expand=True, pady=12)
        ttk.Label(
            export_tools,
            text="Use the vitals chart to visualize heart and blood pressure trends before attaching files to email or EMR notes.",
            style=STYLE_NAMES["tab_body"],
            wraplength=540,
            justify="left",
        ).pack(pady=(0, 10))
        create_dashboard_button(export_tools, "📈 Open Vitals Trend", lambda: gui_plot_trend(patient_list), style_role="insight")
        create_dashboard_button(export_tools, "❌ Close Dashboard", root.destroy, style_role="danger")

    build_patient_tab()
    build_monitor_tab()
    build_export_tab()

    def on_theme_change(_event=None):
        selected_theme = theme_var.get()
        apply_dashboard_theme(style, root, selected_theme)
        save_theme_choice(selected_theme)

    theme_combo.bind("<<ComboboxSelected>>", on_theme_change)
    on_theme_change()

    root.mainloop()
