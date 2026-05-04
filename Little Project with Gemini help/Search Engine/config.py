import datetime

HISTORY_FILE = "search_history.json"

LANG_MAP = {
    "Italiano": "it",
    "English": "en",
    "Français": "fr",
    "Español": "es",
    "Deutsch": "de",
}

DEPTH_SETTINGS = {
    "Fast": {"sentences": 5, "web_count": 1},
    "Normal": {"sentences": 10, "web_count": 3},
    "In-depth": {"sentences": 20, "web_count": 5},
}

MAX_HISTORY_ENTRIES = 20
DATE_FORMAT = "%Y-%m-%d %H:%M"
TODAY = lambda: datetime.date.today()
