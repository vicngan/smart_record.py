import time

RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def typeprint(text, speed=0.05):
    """Print text with a gentle typing animation."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(speed)
    print()
