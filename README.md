# Smart Record Nurse Station

Smart Record is a pastel-friendly nurse dashboard built with Python, Tkinter, and ttkbootstrap to reimagine everyday EMR workflows. It blends a legacy CLI with a modern GUI so charting stays gentle but powerful.

## 🌸 Features That Ease EMR Burnout
- **Quick Patient Peek** with soft gridlines for vitals snapshot, plus universal search and barcode hook for instant lookup.
- **Patient Files popup**: photo upload, goals (nurse/doctor), discharge checklist, tasks, timeline, and soft-needs cues in one place.
- **SBAR handoff cards & Handoff Summary**: aesthetic Situation/Background/Assessment/Recommendation cards auto-filled from vitals and notes.
- **Task prioritizer** grouped into Do now / Do soon / Can wait, with completion toggles and counts.
- **Timeline viewer** logging admissions, vitals updates, exports, etc., so nothing falls through during rounds.
- **Vitals trend chart** that visualizes every historical entry (persisted history) for true longitudinal insight.
- **Soft needs notes** to capture emotional/communication cues, plus priority alert feed and abnormal-overview charts.
- **Themes** like Matcha Night (dark) and Blossom Minimal (light) so day/night shifts stay comfy.
- **Auto formatting**: BP/DOB/temp inputs accept "120 80" or "10 20 2005" and normalize automatically.

These pieces reduce context switching, keep empathy cues front-and-center, and make handoffs delightful—tackling common EMR pain points around scattered notes, shallow vitals history, and tedious entry.

## 🛠️ Languages & Frameworks
- **Python 3** for business logic and persistence
- **Tkinter + ttkbootstrap** for GUI widgets, theming, and dialogs
- **Pillow (PIL)** for patient photo/icon handling
- **Matplotlib** for vitals trend + abnormal overview charts
- **CSV / JSON storage** for patients, timeline, tasks, soft needs, and patient files

## 🚀 Running the App
```bash
python3 smart_record.py/vitals.py
```
Use the Theme dropdown to switch palettes, explore “🗂️ Patient File” or “🧾 Handoff Summary,” and update vitals via the “🩺 Update Vitals” popup, which logs history automatically.
