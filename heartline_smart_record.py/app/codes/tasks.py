import json
import os
import uuid

TASKS_FILE = "tasks.json"


def load_tasks(filename: str = TASKS_FILE):
    if os.path.isfile(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    return []


def save_tasks(tasks, filename: str = TASKS_FILE):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def add_task(tasks, patient_id, description, due="", priority="do soon", filename: str = TASKS_FILE):
    task = {
        "id": str(uuid.uuid4())[:8],
        "patient_id": patient_id,
        "description": description,
        "due": due,
        "priority": priority,
        "status": "pending",
    }
    tasks.append(task)
    save_tasks(tasks, filename)
    return task


def toggle_task(tasks, task_id, filename: str = TASKS_FILE):
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done" if task.get("status") != "done" else "pending"
            save_tasks(tasks, filename)
            return task
    return None


def delete_task(tasks, task_id, filename: str = TASKS_FILE):
    initial_len = len(tasks)
    tasks[:] = [task for task in tasks if task["id"] != task_id]
    if len(tasks) != initial_len:
        save_tasks(tasks, filename)
        return True
    return False


def tasks_for_patient(tasks, patient_id):
    return [task for task in tasks if task["patient_id"] == patient_id]
