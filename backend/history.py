import json
import os

HISTORY_FILE = "download_history.json"

def get_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def add_history(item):
    hist = get_history()
    hist.insert(0, item)
    with open(HISTORY_FILE, "w") as f:
        json.dump(hist[:50], f, indent=4)

def clear_history():
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f, indent=4)
