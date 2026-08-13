import os
from flask import Flask, request, jsonify, send_from_directory, Response
from werkzeug.utils import secure_filename
import threading
import queue
import time
from generator import process_certificates

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__, static_url_path='', static_folder='static')
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global queue for progress updates
progress_queue = queue.Queue()

def progress_callback(message):
    progress_queue.put(message)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'csvFile' not in request.files or 'templateFile' not in request.files:
        return jsonify({"status": "error", "message": "Missing CSV or Template file"}), 400

    csv_file = request.files['csvFile']
    template_file = request.files['templateFile']
    signature_file = request.files.get('signatureFile')

    csv_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(csv_file.filename))
    template_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(template_file.filename))
    
    csv_file.save(csv_path)
    template_file.save(template_path)
    
    signature_path = None
    if signature_file and signature_file.filename:
        signature_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(signature_file.filename))
        signature_file.save(signature_path)

    config = request.form.to_dict()

    def run_process():
        process_certificates(csv_path, template_path, signature_path, config, progress_callback)
        # Clean up
        try:
            if os.path.exists(csv_path): os.remove(csv_path)
            if os.path.exists(template_path): os.remove(template_path)
            if signature_path and os.path.exists(signature_path): os.remove(signature_path)
        except Exception:
            pass

    # Start processing in a background thread
    threading.Thread(target=run_process).start()
    
    return jsonify({"status": "success", "message": "Processing started..."})

@app.route('/api/stats')
def api_stats():
    import stats_manager
    stats = stats_manager.get_stats()
    return jsonify(stats)

@app.route('/progress')
def progress():
    def generate():
        while True:
            try:
                # Wait for up to 15 seconds for a message
                msg = progress_queue.get(timeout=15)
                yield f"data: {msg}\n\n"
                if "✅ Process complete!" in msg or "❌ Error:" in msg:
                    break
            except queue.Empty:
                yield "data: ping\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5000)
