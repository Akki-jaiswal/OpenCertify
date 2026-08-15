import json
import os
import threading

STATS_FILE = 'stats.json'
lock = threading.Lock()

def get_stats():
    """Retrieve the current certificate count from local file."""
    with lock:
        if not os.path.exists(STATS_FILE):
            return {"sent_count": 150}
        try:
            with open(STATS_FILE, 'r') as f:
                data = json.load(f)
                return {"sent_count": data.get("sent_count", 150)}
        except Exception:
            return {"sent_count": 150}

def increment():
    """Increment the certificate count locally."""
    with lock:
        current_stats = {"sent_count": 150}
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, 'r') as f:
                    current_stats = json.load(f)
            except Exception:
                pass
        
        current_stats["sent_count"] = current_stats.get("sent_count", 150) + 1
        
        try:
            with open(STATS_FILE, 'w') as f:
                json.dump(current_stats, f)
        except Exception:
            pass
