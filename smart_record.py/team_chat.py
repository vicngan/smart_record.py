import json
import os
from datetime import datetime

CHAT_FILE = "team_chat.json"


def load_messages(filename: str = CHAT_FILE):
    if os.path.isfile(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return data
            except json.JSONDecodeError:
                pass
    return []


def add_message(messages, author, role, text, filename: str = CHAT_FILE):
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "author": author,
        "role": role,
        "text": text,
    }
    messages.append(entry)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2)
    return entry
