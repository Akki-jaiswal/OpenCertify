import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Firebase only once
if not firebase_admin._apps:
    try:
        # Load from file (local or Render Secret File)
        local_path = 'firebase_credentials.json'
        render_path = '/etc/secrets/firebase_credentials.json'
        
        if os.path.exists(render_path):
            cred = credentials.Certificate(render_path)
        elif os.path.exists(local_path):
            cred = credentials.Certificate(local_path)
        else:
            # Fallback if no file is found (will fail gracefully)
            print("WARNING: firebase_credentials.json not found in local or /etc/secrets!")
            cred = None

        if cred:
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://opencertify-779f8-default-rtdb.firebaseio.com/'
            })
    except Exception as e:
        print(f"Firebase initialization error: {e}")

def get_stats():
    """Retrieve the current certificate count from Firebase."""
    try:
        if not firebase_admin._apps: return {"sent_count": 150}
        ref = db.reference('stats/sent_count')
        count = ref.get()
        if count is None:
            ref.set(150)
            return {"sent_count": 150}
        return {"sent_count": count}
    except Exception as e:
        print(f"Error reading stats: {e}")
        return {"sent_count": 150}

def increment():
    """Increment the certificate count in Firebase atomically."""
    try:
        if not firebase_admin._apps: return
        ref = db.reference('stats/sent_count')
        def increment_transaction(current_value):
            if current_value is None:
                return 151
            return current_value + 1
        ref.transaction(increment_transaction)
    except Exception as e:
        print(f"Error incrementing stats: {e}")
