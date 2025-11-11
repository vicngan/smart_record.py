import time
import re
from datetime import datetime

RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def typeprint(text, speed=0.05):
    """Print text with a gentle typing animation."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(speed)
    print()


def normalize_bp(value):
    if not value:
        return value
    digits = re.findall(r"\d+", str(value))
    if len(digits) >= 2:
        return f"{int(digits[0])}/{int(digits[1])}"
    return str(value).strip()


def normalize_dob(value):
    if not value:
        return value
    digits = re.findall(r"\d+", str(value))
    if len(digits) >= 3:
        month, day, year = digits[:3]
        year = int(year)
        if year < 100:
            year += 2000 if year < 30 else 1900
        try:
            dob = datetime(year, int(month), int(day))
            return dob.strftime("%m/%d/%Y")
        except ValueError:
            return str(value).strip()
    return str(value).strip()


def normalize_temp(value):
    if value is None or value == "":
        return value
    stripped = str(value).replace("°", "").replace("F", "").strip()
    try:
        temp = float(stripped)
        return f"{temp:.1f}"
    except ValueError:
        return str(value).strip()
