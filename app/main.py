from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import logging
import threading
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

active_jobs = {}
MOCK_MODE = os.getenv('MOCK_MODE', 'True') == 'True'

@app.route('/')
def home():
    return jsonify({"service": "AI Video Engineer Backend", "version": "1.0.0", "status": "running", "mock_mode": MOCK_MODE, "endpoints": {"GET /": "API documentation", "GET /health": "Health check", "POST /generate-video": "Generate video from script", "GET /video-status/<id>": "Get video status", "GET /jobs": "List all jobs"}}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat(), "active_jobs": len(active_jobs), "mock_mode": MOCK_MODE}), 200

@app.route('/generate-video', methods=['POST'])
def generate_video():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        script = data.get('script')
        template = data.get('template', 'presenter1')
        user_id = data.get('userId', 'guest')
        if not script:
            return jsonify({"error": "Script is required"}), 400
        video_id = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        job_data = {"id": video_id, "status": "queued", "script": script, "template": template, "user_id": user_id, "progress": 0, "current_step": "Queued", "created_at": datetime.now().isoformat(), "video_url": None}
        active_jobs[video_id] = job_data
        logger.info(f"Video generation started: {video_id}")
        threading.Thread(target=simulate_video_generation, args=(video_id,), daemon=True).start()
        return jsonify({"id": video_id, "message": "Video generation started (MOCK MODE)" if MOCK_MODE else "Video generation started", "status": "queued"}), 201
    except Exception as e:
        logger.error(f"Error in generate_video: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/video-status/<video_id>', methods=['GET'])
def video_status(video_id):
    if video_id in active_jobs:
        return jsonify(active_jobs[video_id]), 200
    else:
        return jsonify({"error": "Video not found"}), 404

@app.route('/jobs', methods=['GET'])
def get_jobs():
    user_id = request.args.get('userId')
    if user_id:
        user_jobs = [job for job in active_jobs.values() if job['user_id'] == user_id]
        return jsonify({"total": len(user_jobs), "jobs": user_jobs}), 200
    return jsonify({"total": len(active_jobs), "jobs": list(active_jobs.values())}), 200

def simulate_video_generation(video_id):
    steps = [(0, "processing", "Starting..."), (10, "processing", "Polishing script..."), (25, "processing", "Generating voiceover..."), (45, "processing", "Creating avatar video..."), (65, "processing", "Composing final video..."), (85, "processing", "Uploading to storage..."), (100, "completed", "Video ready!")]
    try:
        for progress, status, step in steps:
            time.sleep(2)
            active_jobs[video_id].update({'status': status, 'progress': progress, 'current_step': step})
            logger.info(f"Video {video_id}: {progress}% - {step}")
        mock_video_url = f"https://mock-wasabi.com/ai-videos/{video_id}.mp4"
        active_jobs[video_id].update({'status': 'completed', 'progress': 100, 'video_url': mock_video_url, 'completed_at': datetime.now().isoformat()})
        logger.info(f"Video {video_id} completed")
    except Exception as e:
        logger.error(f"Error: {e}")
        active_jobs[video_id].update({'status': 'failed', 'error': str(e)})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting server on port {port} (MOCK_MODE={MOCK_MODE})")
    app.run(host='0.0.0.0', port=port, debug=False)
