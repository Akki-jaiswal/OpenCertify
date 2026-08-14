import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Firebase only once
if not firebase_admin._apps:
    try:
        # Load from file (local or Render Secret File)
        cred_path = 'firebase_credentials.json'
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
        else:
            # Fallback if no file is found (will fail gracefully)
            print("WARNING: firebase_credentials.json not found!")
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
        ref = db.reference('stats/sent_count')
        count = ref.get()
        if count is None:
            # Initialize to 50 if database is totally empty
            ref.set(50)
            return {"sent_count": 50}
        return {"sent_count": count}
    except Exception as e:
        print(f"Error reading stats: {e}")
        return {"sent_count": 50}  # Fallback

def increment():
    """Increment the certificate count in Firebase atomically."""
    try:
        ref = db.reference('stats/sent_count')
        # Use a transaction to safely increment even if multiple threads write at once
        def increment_transaction(current_value):
            if current_value is None:
                return 51
            return current_value + 1
            
        ref.transaction(increment_transaction)
    except Exception as e:
        print(f"Error incrementing stats: {e}")
