# Smart Record Nurse Station

Smart Record is a pastel-friendly nurse dashboard built with Python, Tkinter, and ttkbootstrap to reimagine everyday EMR workflows. It blends CLI utilities with a modern GUI so charting stays gentle but powerful.

## 🌸 Features That Ease EMR Burnout
- **Quick Patient Peek** with soft gridlines, universal search, and barcode hook for instant lookup.
- **Patient Files popup**: photo upload, goals (nurse/doctor), discharge checklist, meds, timeline, tasks, and soft-needs cues in one place.
- **Medication Tracker** with priorities + toggle for administered doses.
- **SBAR handoff cards & Handoff Summary**: aesthetic Situation/Background/Assessment/Recommendation cards auto-filled from vitals and notes.
- **Task prioritizer** grouped into Do now / Do soon / Can wait, with completion toggles and counts.
- **Timeline viewer & patient history** logging admissions and every vitals update; trend charts now visualize all historical entries.
- **Soft Needs notes + voice dictation stub** to capture emotional/communication cues.
- **Team communication chat**, downtime overlay, and offline SQLite cache snapshots for resiliency.
- **Universal vitals chart & abnormal alerts** to highlight high-risk patients across the unit.
- **Themes** like Matcha Night (dark) and Blossom Minimal (minimal light) plus a role selector for RN/Charge/Resident views.
- **Auto formatting**: BP/DOB/temp inputs accept "120 80" or "10 20 2005" and normalize automatically.

These pieces reduce context switching, keep empathy cues front-and-center, and make handoffs delightful—tackling common EMR pain points around scattered notes, shallow vitals history, and tedious entry.

## 🛠️ Languages & Frameworks
- **Python 3** for business logic and persistence
- **Tkinter + ttkbootstrap** for GUI widgets, theming, dialogs
- **Pillow (PIL)** for patient photo/icon handling
- **Matplotlib** for vitals trend + universal charts
- **sqlite3 / CSV / JSON storage** for patients, timeline, tasks, meds, soft needs, and cached history

## 🚀 Running the App
```bash
python3 smart_record.py/vitals.py
```
Use the Theme dropdown to switch palettes, explore “🗂️ Patient File,” “💊 Med Tracker,” or “🧾 Handoff Summary,” and update vitals via the “🩺 Update Vitals” popup (with history logging). Snapshot the cache anytime with the "💾 Snapshot" button.
