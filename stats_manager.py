import json
import os
import threading

STATS_FILE = 'stats.json'
_lock = threading.Lock()

def _init_stats():
    if not os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'w') as f:
            json.dump({"sent_count": 50}, f)

def get_stats():
    with _lock:
        _init_stats()
        with open(STATS_FILE, 'r') as f:
            return json.load(f)

def increment():
    with _lock:
        _init_stats()
        with open(STATS_FILE, 'r') as f:
            data = json.load(f)
        
        data["sent_count"] += 1
        
        with open(STATS_FILE, 'w') as f:
            json.dump(data, f)
