# storage.py
import json
import os
from models import Event

EVENTS_FILE = "events.json"

def load_events():
    if not os.path.exists(EVENTS_FILE):
        return []
    try:
        with open(EVENTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        events = []
        for ev in data:
            if not isinstance(ev, dict):
                continue
            events.append(Event(
                ev.get("id", 0),
                ev.get("title", ""),
                ev.get("description", ""),
                ev.get("startDate", "")
            ))
        return events
    except Exception:
        return []

def save_events(events):
    data = [{"id": ev.id, "title": ev.title, "description": ev.description, "startDate": ev.startDate} for ev in events]
    with open(EVENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
