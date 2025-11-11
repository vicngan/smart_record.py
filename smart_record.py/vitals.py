from data_access import (
    CSV_FILE,
    JSON_FILE,
    CSV_HEADERS,
    append_to_csv,
    load_data,
    load_from_csv,
    save_data,
    save_to_json,
)
from patient_ops import (
    abnormal_summary,
    add_patient,
    count_abnormal_BP,
    count_abnormal_HR,
    display_abnormal_BP,
    display_abnormal_HR,
    export_report,
    get_abnormal_BP,
    get_abnormal_HR,
    plot_trend,
    search_patient,
    update_vitals,
    view_patients,
)
from cli_app import run_cli
from gui_app import (
    gui_abnormal_summary,
    gui_add_patient,
    gui_plot_trend,
    gui_search_patients,
    gui_update_vitals,
    gui_view_patients,
    launch_gui,
)
from utils import RED, RESET, YELLOW, typeprint

__all__ = [
    "CSV_FILE",
    "JSON_FILE",
    "CSV_HEADERS",
    "RED",
    "YELLOW",
    "RESET",
    "typeprint",
    "load_from_csv",
    "append_to_csv",
    "save_to_json",
    "save_data",
    "load_data",
    "add_patient",
    "view_patients",
    "search_patient",
    "get_abnormal_HR",
    "count_abnormal_HR",
    "display_abnormal_HR",
    "get_abnormal_BP",
    "count_abnormal_BP",
    "display_abnormal_BP",
    "abnormal_summary",
    "export_report",
    "update_vitals",
    "plot_trend",
    "run_cli",
    "launch_gui",
    "gui_add_patient",
    "gui_view_patients",
    "gui_search_patients",
    "gui_abnormal_summary",
    "gui_update_vitals",
    "gui_plot_trend",
]


if __name__ == "__main__":
    patient_list = load_from_csv()
    launch_gui(patient_list)
