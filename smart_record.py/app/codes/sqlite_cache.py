import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "smart_record_cache.db")


def snapshot_patients(patient_list):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            name TEXT,
            DOB TEXT,
            HR TEXT,
            BP TEXT,
            Temp TEXT,
            Diagnosis TEXT,
            Time TEXT
        )
        """
    )
    for patient in patient_list:
        cur.execute(
            """
            INSERT INTO patients (patient_id, name, DOB, HR, BP, Temp, Diagnosis, Time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(patient_id) DO UPDATE SET
                name=excluded.name,
                DOB=excluded.DOB,
                HR=excluded.HR,
                BP=excluded.BP,
                Temp=excluded.Temp,
                Diagnosis=excluded.Diagnosis,
                Time=excluded.Time
            """,
            (
                patient["patient_id"],
                patient["name"],
                patient["DOB"],
                patient["HR"],
                patient["BP"],
                patient["Temp"],
                patient.get("Diagnosis", ""),
                patient.get("Time", ""),
            ),
        )
    conn.commit()
    conn.close()
