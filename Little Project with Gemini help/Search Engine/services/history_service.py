import datetime
import json
import os

from config import DATE_FORMAT, HISTORY_FILE, MAX_HISTORY_ENTRIES


def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return []
    return []


def save_to_history(topic, filepath):
    history = load_history()
    entry = {
        "topic": topic,
        "date": datetime.datetime.now().strftime(DATE_FORMAT),
        "path": filepath,
    }

    if history and history[0]["topic"] == topic and history[0]["path"] == filepath:
        return

    history.insert(0, entry)
    if len(history) > MAX_HISTORY_ENTRIES:
        history = history[:MAX_HISTORY_ENTRIES]

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)
