import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, StringVar, PhotoImage, filedialog

try:
    from PIL import Image, ImageDraw, ImageTk
except ImportError:
    Image = None
    ImageDraw = None
    ImageTk = None

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from patient_ops import (
    add_patient,
    create_handoff_summary,
    export_report,
    plot_abnormal_overview,
    plot_trend,
    update_vitals,
    priority_alerts,
)
from tasks import add_task, delete_task, load_tasks, save_tasks, tasks_for_patient, toggle_task
from timeline import recent_events
from soft_needs import add_soft_note, get_soft_notes, save_soft_needs
from patient_files import (
    load_patient_files,
    save_patient_files,
    ensure_patient_record,
    update_goals,
    set_discharge_status,
    set_photo,
)

BASE_DIR = os.path.dirname(__file__)
THEME_CONFIG_PATH = os.path.join(BASE_DIR, "dashboard_theme.json")
NOT_FOUND_LOGO = os.path.join(BASE_DIR, "app", "static", "not_found_logo.png")
APP_LOGO = os.path.join(BASE_DIR, "app", "static", "heartline_icon.png")

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
    "Matcha Night": {
        "base_theme": "darkly",
        "background": "#1b1c1d",
        "banner": {"bg": "#2b2e30", "fg": "#d6f5c4", "sub_fg": "#bde7af"},
        "panels": {
            "patient": {"bg": "#222425", "label_bg": "#2f3533", "label_fg": "#d6f5c4", "border": "#3c4a3f"},
            "monitor": {"bg": "#242728", "label_bg": "#313736", "label_fg": "#f6d8e7", "border": "#4c5a4d"},
            "report": {"bg": "#242627", "label_bg": "#313534", "label_fg": "#fce4ef", "border": "#56624d"},
        },
        "text": {"primary": "#f6d8e7", "muted": "#c3d6c4"},
        "buttons": {
            "primary": {"bg": "#7ecf94", "hover": "#6bb880", "fg": "#142616", "border": "#6bb880"},
            "secondary": {"bg": "#3f4c44", "hover": "#4c5b50", "fg": "#dcebd6", "border": "#4c5b50"},
            "info": {"bg": "#5cb3c5", "hover": "#4ca1b2", "fg": "#0e1d22", "border": "#4ca1b2"},
            "alert": {"bg": "#f08fab", "hover": "#e07492", "fg": "#270b13", "border": "#e07492"},
            "accent": {"bg": "#b0d38f", "hover": "#97c270", "fg": "#1a260f", "border": "#97c270"},
            "insight": {"bg": "#cba0d8", "hover": "#b484c6", "fg": "#190c20", "border": "#b484c6"},
            "success": {"bg": "#6bc28b", "hover": "#58ab75", "fg": "#09170e", "border": "#58ab75"},
            "danger": {"bg": "#f38a93", "hover": "#d96d77", "fg": "#28090c", "border": "#d96d77"},
        },
    },
    "Blossom Minimal": {
        "base_theme": "journal",
        "background": "#fefefd",
        "banner": {"bg": "#f9f6f1", "fg": "#6f6a5d", "sub_fg": "#9a9487"},
        "panels": {
            "patient": {"bg": "#ffffff", "label_bg": "#f6f3ef", "label_fg": "#6f6a5d", "border": "#e4dfd6"},
            "monitor": {"bg": "#ffffff", "label_bg": "#f4f1ed", "label_fg": "#6f6a5d", "border": "#ded8ce"},
            "report": {"bg": "#ffffff", "label_bg": "#f6f1ec", "label_fg": "#6f6a5d", "border": "#e4dcd0"},
        },
        "text": {"primary": "#5f5a4f", "muted": "#9a9487"},
        "buttons": {
            "primary": {"bg": "#f6b7c6", "hover": "#f2a1b4", "fg": "#59303c", "border": "#f2a1b4"},
            "secondary": {"bg": "#ebe7de", "hover": "#dfd9ce", "fg": "#605a4f", "border": "#dfd9ce"},
            "info": {"bg": "#d6e8f2", "hover": "#bfd9e8", "fg": "#2b4856", "border": "#bfd9e8"},
            "alert": {"bg": "#ffd9b8", "hover": "#ffc89a", "fg": "#5e3c24", "border": "#ffc89a"},
            "accent": {"bg": "#e2efd8", "hover": "#cfe4c2", "fg": "#304929", "border": "#cfe4c2"},
            "insight": {"bg": "#f0def2", "hover": "#e3c7e8", "fg": "#463457", "border": "#e3c7e8"},
            "success": {"bg": "#d0eadf", "hover": "#bbdece", "fg": "#224235", "border": "#bbdece"},
            "danger": {"bg": "#f7c3c3", "hover": "#f3aaaa", "fg": "#5a2a2a", "border": "#f3aaaa"},
        },
    },
}

TITLE_FONT = ("Comic Sans MS", 28, "bold")

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
            if Image and ImageTk:
                with Image.open(APP_LOGO) as img:
                    img.thumbnail((100, 100), Image.LANCZOS)
                    _APP_LOGO_IMAGE = ImageTk.PhotoImage(img.copy())
            else:
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
    style.configure(
        "QuickTreeview",
        rowheight=32,
        bordercolor="#f0dbe7",
        relief="flat",
    )
    style.map("QuickTreeview", background=[("selected", "#fbeff6")])

    banner_colors = theme["banner"]
    style.configure(STYLE_NAMES["banner"], background=banner_colors["bg"], borderwidth=0, relief="flat")
    style.configure(
        STYLE_NAMES["banner_title"],
        background=banner_colors["bg"],
        foreground=banner_colors["fg"],
        font=TITLE_FONT,
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


def gui_add_patient(patient_list, timeline_entries=None):
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
            timeline_entries=timeline_entries,
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


def gui_update_vitals(patient_list, timeline_entries=None):
    update_id = simpledialog.askstring("Update Vitals", "Patient ID to update:")
    if not update_id:
        return
    patient = next((p for p in patient_list if p["patient_id"] == update_id), None)
    if not patient:
        show_not_found_popup("Not Found", "No patient matches that ID.")
        return

    form = ttk.Toplevel()
    form.title(f"Update Vitals • {patient['name']}")
    form.geometry("460x600")
    form.grab_set()

    container = ttk.Frame(form, padding=24, style=STYLE_NAMES["home"])
    container.pack(fill="both", expand=True)

    ttk.Label(container, text="Update only what changed; leave blank to keep current values.", style=STYLE_NAMES["tab_body"]).pack(anchor="w", pady=(0, 12))

    field_definitions = [
        ("Heart Rate", "HR", patient["HR"]),
        ("Blood Pressure (e.g. 120/80)", "BP", patient["BP"]),
        ("Temperature", "Temp", patient["Temp"]),
        ("Diagnosis", "Diagnosis", patient.get("Diagnosis", "")),
        ("Personnel Initials", "RN_AP", patient.get("RN_AP", "")),
    ]

    vars_map = {}
    for label_text, key, value in field_definitions:
        frame = ttk.Frame(container, style=STYLE_NAMES["home"])
        frame.pack(fill="x", pady=6)
        ttk.Label(frame, text=f"{label_text} (Current: {value})", style=STYLE_NAMES["tab_body"]).pack(anchor="w")
        var = StringVar()
        ttk.Entry(frame, textvariable=var).pack(fill="x", pady=(4, 0))
        vars_map[key] = var

    def submit():
        updates = {k: v.get().strip() for k, v in vars_map.items() if v.get().strip()}
        if not updates:
            messagebox.showinfo("No Changes", "You didn't enter any updates.")
            return
        success = update_vitals(patient_list, update_id, updates, timeline_entries=timeline_entries)
        if success:
            form.destroy()

    ttk.Button(container, text="Save Updates", command=submit, style=BUTTON_STYLE_NAMES["success"]).pack(fill="x", pady=(12, 0))
    ttk.Button(container, text="Cancel", command=form.destroy, style=BUTTON_STYLE_NAMES["secondary"]).pack(fill="x", pady=(8, 0))


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

    columns = ("id", "patient", "priority", "description", "due", "status")
    tree = ttk.Treeview(container, columns=columns, show="headings", height=12)
    for col in columns:
        width = 80 if col == "id" else 140
        tree.heading(col, text=col.title())
        tree.column(col, width=width, anchor="center")
    tree.pack(fill="both", expand=True, pady=(0, 12))

    def resolve_name(patient_id):
        patient = next((p for p in patient_list if p["patient_id"] == patient_id), None)
        return f"{patient_id} - {patient['name']}" if patient else patient_id

    summary_var = StringVar()

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
                    task.get("priority", "do soon"),
                    task["description"],
                    task.get("due", ""),
                    task.get("status", "pending"),
                ),
            )
        counts = {"do now": 0, "do soon": 0, "can wait": 0}
        for task in tasks:
            counts[task.get("priority", "do soon")] = counts.get(task.get("priority", "do soon"), 0) + 1
        summary_var.set(
            f"Do now: {counts.get('do now',0)}  •  Do soon: {counts.get('do soon',0)}  •  Can wait: {counts.get('can wait',0)}"
        )

    form_frame = ttk.Frame(container, style=STYLE_NAMES["home"])
    form_frame.pack(fill="x", pady=8)

    ttk.Label(form_frame, text="Patient ID", style=STYLE_NAMES["tab_body"]).grid(row=0, column=0, sticky="w")
    patient_var = StringVar()
    ttk.Entry(form_frame, textvariable=patient_var).grid(row=1, column=0, sticky="ew", padx=(0, 8))

    ttk.Label(form_frame, text="Task Description", style=STYLE_NAMES["tab_body"]).grid(row=0, column=1, sticky="w")
    desc_var = StringVar()
    ttk.Entry(form_frame, textvariable=desc_var).grid(row=1, column=1, sticky="ew", padx=(0, 8))

    ttk.Label(form_frame, text="Priority", style=STYLE_NAMES["tab_body"]).grid(row=0, column=2, sticky="w")
    priority_var = StringVar(value="do soon")
    priority_combo = ttk.Combobox(
        form_frame,
        textvariable=priority_var,
        values=["do now", "do soon", "can wait"],
        state="readonly",
    )
    priority_combo.grid(row=1, column=2, sticky="ew", padx=(0, 8))

    ttk.Label(form_frame, text="Due Time (optional)", style=STYLE_NAMES["tab_body"]).grid(row=0, column=3, sticky="w")
    due_var = StringVar()
    ttk.Entry(form_frame, textvariable=due_var).grid(row=1, column=3, sticky="ew")

    form_frame.columnconfigure((0, 1, 2, 3), weight=1)

    def add_task_action():
        patient_id = patient_var.get().strip()
        description = desc_var.get().strip()
        if not patient_id or not description:
            messagebox.showerror("Missing data", "Please enter both patient ID and description.")
            return
        if not any(p["patient_id"] == patient_id for p in patient_list):
            messagebox.showerror("Unknown Patient", "That patient ID does not exist yet.")
            return
        add_task(tasks, patient_id, description, due_var.get().strip(), priority_var.get())
        refresh_tree()
        patient_var.set("")
        desc_var.set("")
        due_var.set("")
        priority_var.set("do soon")

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

    ttk.Label(container, textvariable=summary_var, style=STYLE_NAMES["tab_body"]).pack(pady=(0, 6), anchor="w")
    refresh_tree()
def open_timeline_view(timeline_entries, patient_list):
    window = ttk.Toplevel()
    window.title("Care Timeline 🕒")
    window.geometry("720x520")
    window.grab_set()

    container = ttk.Frame(window, padding=16, style=STYLE_NAMES["home"])
    container.pack(fill="both", expand=True)

    columns = ("timestamp", "patient", "event", "description")
    tree = ttk.Treeview(container, columns=columns, show="headings", height=18)
    for col in columns:
        width = 120 if col != "description" else 280
        tree.heading(col, text=col.title())
        tree.column(col, width=width, anchor="center")
    tree.pack(fill="both", expand=True)

    def resolve_name(pid):
        patient = next((p for p in patient_list if p["patient_id"] == pid), None)
        return f"{pid} - {patient['name']}" if patient else pid

    for entry in recent_events(timeline_entries):
        tree.insert(
            "",
            "end",
            values=(entry["timestamp"], resolve_name(entry["patient_id"]), entry["event"], entry["description"]),
        )

    ttk.Button(container, text="Close", command=window.destroy, style=BUTTON_STYLE_NAMES["secondary"]).pack(pady=10)


def open_search_center(patient_list, tasks, timeline_entries, query):
    if not query:
        return
    query_lower = query.lower()
    window = ttk.Toplevel()
    window.title(f"Search Results for '{query}'")
    window.geometry("760x540")
    window.grab_set()

    container = ttk.Frame(window, padding=16, style=STYLE_NAMES["home"])
    container.pack(fill="both", expand=True)

    columns = ("type", "patient", "details")
    tree = ttk.Treeview(container, columns=columns, show="headings", height=18)
    for col in columns:
        width = 100 if col == "type" else 200 if col == "patient" else 360
        tree.heading(col, text=col.title())
        tree.column(col, width=width, anchor="w")
    tree.pack(fill="both", expand=True)

    def match(text):
        return query_lower in str(text).lower()

    for p in patient_list:
        if match(p["patient_id"]) or match(p["name"]) or match(p.get("Diagnosis", "")) or match(p.get("CC", "")):
            tree.insert("", "end", values=("Patient", f"{p['patient_id']} - {p['name']}", p.get("Diagnosis", "")))

    for task in tasks:
        if match(task["description"]) or match(task["patient_id"]):
            tree.insert("", "end", values=("Task", task["patient_id"], task["description"]))

    for entry in timeline_entries:
        if match(entry["description"]) or match(entry["patient_id"]):
            tree.insert("", "end", values=("Timeline", entry["patient_id"], entry["description"]))

    ttk.Button(container, text="Close", command=window.destroy, style=BUTTON_STYLE_NAMES["secondary"]).pack(pady=10)


def open_sbar_cards(patient_list, soft_notes):
    window = ttk.Toplevel()
    window.title("SBAR Cards 💌")
    window.geometry("820x600")
    window.grab_set()

    canvas = tk.Canvas(window, bg="#fef6fb", highlightthickness=0)
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    inner = ttk.Frame(canvas, padding=24, style=STYLE_NAMES["home"])
    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=inner, anchor="nw")

    for patient in patient_list:
        card = ttk.Frame(inner, padding=18, style=STYLE_NAMES["patient_panel"])
        card.pack(fill="x", pady=10)
        ttk.Label(card, text=f"{patient['patient_id']} • {patient['name']}", style=STYLE_NAMES["tab_heading"]).pack(
            anchor="w"
        )
        ttk.Label(card, text=f"S: {patient.get('CC','N/A')}", style=STYLE_NAMES["tab_body"]).pack(anchor="w", pady=(4, 0))
        ttk.Label(card, text=f"B: DOB {patient['DOB']} | Dx: {patient.get('Diagnosis','')}", style=STYLE_NAMES["tab_body"]).pack(
            anchor="w",
            pady=(2, 0),
        )
        ttk.Label(
            card,
            text=f"A: HR {patient['HR']}  BP {patient['BP']}  Temp {patient['Temp']}",
            style=STYLE_NAMES["tab_body"],
        ).pack(anchor="w", pady=(2, 0))
        notes = soft_notes.get(patient["patient_id"], [])
        rec = notes[-1]["note"] if notes else "Kind reminder: add soft need note ❤️"
        ttk.Label(card, text=f"R: {rec}", style=STYLE_NAMES["tab_body"]).pack(anchor="w", pady=(2, 0))

    ttk.Button(inner, text="Close", command=window.destroy, style=BUTTON_STYLE_NAMES["secondary"]).pack(pady=12)


def open_soft_needs_center(patient_list, soft_notes):
    window = ttk.Toplevel()
    window.title("Soft Needs Notes 🌸")
    window.geometry("680x520")
    window.grab_set()

    container = ttk.Frame(window, padding=16, style=STYLE_NAMES["home"])
    container.pack(fill="both", expand=True)

    columns = ("patient", "note")
    tree = ttk.Treeview(container, columns=columns, show="headings", height=12)
    for col, width in (("patient", 180), ("note", 400)):
        tree.heading(col, text=col.title())
        tree.column(col, width=width, anchor="w")
    tree.pack(fill="both", expand=True, pady=(0, 12))

    def refresh():
        for row in tree.get_children():
            tree.delete(row)
        for pid, entries in soft_notes.items():
            patient = next((p for p in patient_list if p["patient_id"] == pid), None)
            prefix = f"{pid} - {patient['name']}" if patient else pid
            for entry in entries[-5:]:
                tree.insert("", "end", values=(prefix, f"{entry['timestamp']}: {entry['note']}"))

    form = ttk.Frame(container, style=STYLE_NAMES["home"])
    form.pack(fill="x")
    ttk.Label(form, text="Patient ID", style=STYLE_NAMES["tab_body"]).grid(row=0, column=0, sticky="w")
    pid_var = StringVar()
    ttk.Entry(form, textvariable=pid_var).grid(row=1, column=0, sticky="ew", padx=(0, 8))

    ttk.Label(form, text="Soft Need / Cue", style=STYLE_NAMES["tab_body"]).grid(row=0, column=1, sticky="w")
    note_var = StringVar()
    ttk.Entry(form, textvariable=note_var).grid(row=1, column=1, sticky="ew")
    form.columnconfigure((0, 1), weight=1)

    def add_note():
        pid = pid_var.get().strip()
        cue = note_var.get().strip()
        if not pid or not cue:
            messagebox.showerror("Missing info", "Enter both patient ID and note.")
            return
        add_soft_note(soft_notes, pid, cue)
        refresh()
        pid_var.set("")
        note_var.set("")

    ttk.Button(form, text="Add Note", command=add_note, style=BUTTON_STYLE_NAMES["success"]).grid(row=1, column=2, padx=8)
    ttk.Button(container, text="Close", command=window.destroy, style=BUTTON_STYLE_NAMES["secondary"]).pack(pady=8)
    refresh()


def open_patient_file(patient, tasks, timeline_entries, soft_notes, patient_files):
    ensure_patient_record(patient_files, patient["patient_id"])
    window = ttk.Toplevel()
    window.title(f"Patient File • {patient['name']}")
    window.geometry("880x640")
    window.grab_set()

    container = ttk.Frame(window, padding=16, style=STYLE_NAMES["home"])
    container.pack(fill="both", expand=True)
    container.columnconfigure(1, weight=1)

    photo_frame = ttk.Frame(container, padding=10, style=STYLE_NAMES["patient_panel"])
    photo_frame.grid(row=0, column=0, rowspan=2, sticky="ns")
    photo_canvas = tk.Label(photo_frame, bg="#fffafc")
    photo_canvas.pack()

    record = patient_files.get(patient["patient_id"], {})

    def load_photo():
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if not path:
            return
        set_photo(patient_files, patient["patient_id"], path)
        save_patient_files(patient_files)
        record["photo"] = path
        display_photo()

    def display_photo():
        path = record.get("photo")
        if path and os.path.isfile(path) and Image and ImageTk:
            with Image.open(path) as img:
                img.thumbnail((200, 200))
                photo = ImageTk.PhotoImage(img.copy())
                photo_canvas.configure(image=photo)
                photo_canvas.image = photo
        else:
            photo_canvas.configure(text="No Photo", image="", width=20, height=10)

    ttk.Button(photo_frame, text="Upload Photo", command=load_photo, style=BUTTON_STYLE_NAMES["secondary"]).pack(pady=8)
    display_photo()

    info_frame = ttk.Frame(container, padding=10, style=STYLE_NAMES["home"])
    info_frame.grid(row=0, column=1, sticky="ew")
    ttk.Label(
        info_frame,
        text=f"{patient['patient_id']} • {patient['name']}",
        style=STYLE_NAMES["tab_heading"],
    ).pack(anchor="w")
    ttk.Label(
        info_frame,
        text=f"DOB: {patient['DOB']}  |  HR {patient['HR']}  BP {patient['BP']}  Temp {patient['Temp']}",
        style=STYLE_NAMES["tab_body"],
    ).pack(anchor="w", pady=(4, 0))

    goals_frame = ttk.Labelframe(container, text="Goals & Discharge", padding=12, style=STYLE_NAMES["patient_panel"])
    goals_frame.grid(row=1, column=1, sticky="ew", pady=(12, 0))

    goals_text = tk.Text(goals_frame, height=4)
    goals_text.pack(fill="x")
    if record.get("goals"):
        goals_text.insert("1.0", "\n".join(record["goals"]))
    assigned_var = StringVar(value=record.get("assigned_by", ""))
    ttk.Entry(goals_frame, textvariable=assigned_var).pack(fill="x", pady=(6, 0))

    discharge_var = tk.BooleanVar(value=record.get("discharge_ready", False))
    ttk.Checkbutton(goals_frame, text="Ready for discharge", variable=discharge_var).pack(anchor="w", pady=4)

    def save_goals():
        goals = [line.strip() for line in goals_text.get("1.0", "end").splitlines() if line.strip()]
        update_goals(patient_files, patient["patient_id"], goals, assigned_var.get())
        set_discharge_status(patient_files, patient["patient_id"], discharge_var.get())
        save_patient_files(patient_files)
        messagebox.showinfo("Saved", "Patient goals updated.")

    ttk.Button(goals_frame, text="Save Goals", command=save_goals, style=BUTTON_STYLE_NAMES["success"]).pack(anchor="e")

    tabs = ttk.Notebook(container)
    tabs.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(12, 0))
    container.rowconfigure(2, weight=1)

    def build_list(tab, items):
        tree = ttk.Treeview(tab, columns=("info",), show="headings", height=8)
        tree.heading("info", text="Details")
        tree.column("info", anchor="w")
        tree.pack(fill="both", expand=True)
        for line in items:
            tree.insert("", "end", values=(line,))

    task_tab = ttk.Frame(tabs, padding=10, style=STYLE_NAMES["home"])
    tabs.add(task_tab, text="Tasks")
    patient_tasks = [t for t in tasks if t["patient_id"] == patient["patient_id"]]
    build_list(
        task_tab,
        [f"[{t.get('priority','do soon')}] {t['description']} ({t.get('status','pending')})" for t in patient_tasks]
        or ["No tasks yet."],
    )

    timeline_tab = ttk.Frame(tabs, padding=10, style=STYLE_NAMES["home"])
    tabs.add(timeline_tab, text="Timeline")
    patient_timeline = [
        f"{e['timestamp']} - {e['event']}: {e['description']}"
        for e in timeline_entries
        if e["patient_id"] == patient["patient_id"]
    ]
    build_list(timeline_tab, patient_timeline or ["No timeline entries."])

    soft_tab = ttk.Frame(tabs, padding=10, style=STYLE_NAMES["home"])
    tabs.add(soft_tab, text="Soft Needs")
    patient_soft = [f"{n['timestamp']}: {n['note']}" for n in soft_notes.get(patient["patient_id"], [])]
    build_list(soft_tab, patient_soft or ["Add a soft note from the Soft Needs center."])


def open_patient_file_prompt(patient_list, tasks, timeline_entries, soft_notes, patient_files):
    pid = simpledialog.askstring("Patient File", "Enter Patient ID:")
    if not pid:
        return
    patient = next((p for p in patient_list if p["patient_id"] == pid), None)
    if not patient:
        show_not_found_popup("Not Found", "No patient matches that ID.")
        return
    open_patient_file(patient, tasks, timeline_entries, soft_notes, patient_files)

def launch_gui(patient_list, tasks=None, timeline_entries=None, soft_notes=None, patient_files=None):
    tasks = tasks or []
    timeline_entries = timeline_entries or []
    soft_notes = soft_notes or {}
    patient_files = patient_files or load_patient_files()
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
    title_row.grid(row=0, column=0, columnspan=2, sticky="nsew")
    banner.columnconfigure(0, weight=1)
    if app_logo:
        logo_label = ttk.Label(title_row, image=app_logo)
        logo_label.image = app_logo
        logo_label.pack(side="top", pady=(0, 6))
    ttk.Label(title_row, text="Smart Record Nurse Station", style=STYLE_NAMES["banner_title"]).pack(side="top")

    control_row = ttk.Frame(banner, style=STYLE_NAMES["banner"])
    control_row.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(12, 0))
    control_row.columnconfigure(0, weight=1)

    search_var = StringVar()
    search_entry = ttk.Entry(control_row, textvariable=search_var)
    search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
    ttk.Button(
        control_row,
        text="🔎 Search",
        command=lambda: open_search_center(patient_list, tasks, timeline_entries, search_var.get()),
        style=BUTTON_STYLE_NAMES["info"],
    ).grid(row=0, column=1, padx=(0, 8))

    ttk.Button(
        control_row,
        text="🕒 Timeline",
        command=lambda: open_timeline_view(timeline_entries, patient_list),
        style=BUTTON_STYLE_NAMES["secondary"],
    ).grid(row=0, column=2, padx=(0, 8))

    ttk.Label(control_row, text="Theme", style=STYLE_NAMES["banner_subtitle"]).grid(row=0, column=3, padx=(12, 6))
    theme_var = StringVar(value=active_theme)
    theme_combo = ttk.Combobox(
        control_row,
        textvariable=theme_var,
        values=list(DASHBOARD_THEMES.keys()),
        state="readonly",
        width=16,
    )
    theme_combo.grid(row=0, column=4)

    quick_frame = ttk.Labelframe(
        home_frame,
        text="Quick Patient Peek 👀",
        padding=16,
        style=STYLE_NAMES["patient_panel"],
    )
    quick_frame.pack(fill="x", pady=(12, 0))
    quick_canvas = tk.Canvas(quick_frame, height=140, highlightthickness=0, bg="#fffef9")
    quick_canvas.pack(fill="x")
    headers = ["ID", "Name", "Diagnosis", "HR", "BP"]

    def redraw_quick(event=None):
        quick_canvas.delete("all")
        w = quick_canvas.winfo_width()
        h = quick_canvas.winfo_height()
        row_height = h // 5
        col_positions = [0, w * 0.1, w * 0.4, w * 0.6, w * 0.78, w]

        for i in range(6):
            y = i * row_height
            quick_canvas.create_line(0, y, w, y, fill="#eed8e4")
        for x in col_positions:
            quick_canvas.create_line(x, 0, x, h, fill="#eed8e4")

        for idx, title in enumerate(headers):
            quick_canvas.create_text(
                (col_positions[idx] + col_positions[idx + 1]) / 2,
                10,
                text=title,
                fill="#8b6f79",
                font=("Helvetica", 11, "bold"),
            )

        for row, patient in enumerate(patient_list[:5]):
            y = (row + 1) * row_height + 10
            values = [
                patient["patient_id"],
                patient["name"],
                patient.get("Diagnosis", ""),
                patient["HR"],
                patient["BP"],
            ]
            for idx, value in enumerate(values):
                quick_canvas.create_text(
                    (col_positions[idx] + col_positions[idx + 1]) / 2,
                    y,
                    text=value,
                    font=("Helvetica", 11),
                )

    quick_canvas.bind("<Configure>", redraw_quick)

    panels_container = ttk.Frame(home_frame, style=STYLE_NAMES["home"])
    panels_container.pack(expand=True, fill="both", pady=(12, 0))
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

    create_dashboard_button(
        patient_panel,
        "➕ Add New Patient",
        lambda: gui_add_patient(patient_list, timeline_entries),
        style_role="primary",
    )
    create_dashboard_button(patient_panel, "📋 View Patients", lambda: gui_view_patients(patient_list), style_role="secondary")
    create_dashboard_button(patient_panel, "🔍 Search Patient", lambda: gui_search_patients(patient_list), style_role="info")
    create_dashboard_button(
        patient_panel,
        "🗂️ Patient File",
        lambda: open_patient_file_prompt(patient_list, tasks, timeline_entries, soft_notes, patient_files),
        style_role="insight",
    )
    create_dashboard_button(patient_panel, "🧾 Scan Barcode/ID", lambda: gui_scan_barcode(patient_list), style_role="accent")

    create_dashboard_button(
        monitor_panel, "⚠️ Abnormal Summary", lambda: gui_abnormal_summary(patient_list), style_role="alert"
    )
    create_dashboard_button(
        monitor_panel,
        "🩺 Update Vitals",
        lambda: gui_update_vitals(patient_list, timeline_entries),
        style_role="accent",
    )
    create_dashboard_button(
        monitor_panel, "📈 Vitals Trend Chart", lambda: gui_plot_trend(patient_list), style_role="insight"
    )
    create_dashboard_button(
        monitor_panel, "📊 Abnormal Vitals Chart", lambda: plot_abnormal_overview(patient_list), style_role="info"
    )
    alert_frame = ttk.Labelframe(monitor_panel, text="Priority Alerts 🚨", padding=12, style=STYLE_NAMES["monitor_panel"])
    alert_frame.pack(fill="both", expand=True, pady=(12, 0))
    alert_tree = ttk.Treeview(alert_frame, columns=("patient", "details"), show="headings", height=5)
    alert_tree.heading("patient", text="Patient")
    alert_tree.heading("details", text="Details")
    alert_tree.column("patient", width=140)
    alert_tree.column("details", width=240)
    alert_tree.pack(fill="both", expand=True)

    def refresh_alerts():
        for row in alert_tree.get_children():
            alert_tree.delete(row)
        severity_colors = {
            "critical": "[CRITICAL]",
            "warning": "[Warning]",
            "info": "[Info]",
        }
        for alert in priority_alerts(patient_list):
            label = f"{alert['patient_id']} - {alert['name']} {severity_colors.get(alert['severity'], '')}"
            alert_tree.insert("", "end", values=(label, alert["details"]))

    refresh_alerts()

    report_actions = [
        ("📤 Export Report", lambda: export_report(patient_list), "success"),
        ("🧾 Handoff Summary", lambda: show_handoff_summary_popup(patient_list, tasks), "info"),
        ("✅ Task Reminders", lambda: open_task_center(patient_list, tasks), "accent"),
        ("🪄 SBAR Cards", lambda: open_sbar_cards(patient_list, soft_notes), "info"),
        ("🌸 Soft Needs Notes", lambda: open_soft_needs_center(patient_list, soft_notes), "secondary"),
        ("❌ Exit", root.destroy, "danger"),
    ]
    for i in range(0, len(report_actions), 2):
        row = ttk.Frame(report_panel, style=STYLE_NAMES["report_panel"])
        row.pack(fill="x", pady=4)
        for text, command, style_role in report_actions[i : i + 2]:
            btn = ttk.Button(row, text=text, command=command, style=BUTTON_STYLE_NAMES[style_role])
            btn.pack(side="left", fill="x", expand=True, padx=4)

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
            patient_shortcuts,
            "➕ Register A New Patient",
            lambda: gui_add_patient(patient_list, timeline_entries),
            style_role="primary",
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
            vital_snapshot,
            "🩺 Update Vitals",
            lambda: gui_update_vitals(patient_list, timeline_entries),
            style_role="accent",
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
