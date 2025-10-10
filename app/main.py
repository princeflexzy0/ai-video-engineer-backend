from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# In-memory job storage (replace with database in production)
active_jobs = {}

# Environment variables
MOCK_MODE = os.getenv('MOCK_MODE', 'True') == 'True'

@app.route('/')
def home():
    """Root endpoint - API documentation"""
    return jsonify({
        "service": "AI Video Engineer Backend",
        "version": "1.0.0",
        "status": "running",
        "mock_mode": MOCK_MODE,
        "endpoints": {
            "health": "/health",
            "generate": "/generate-video (POST)",
            "status": "/video-status/<id> (GET)",
            "jobs": "/jobs (GET)"
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_jobs": len(active_jobs),
        "mock_mode": MOCK_MODE
    }), 200

@app.route('/generate-video', methods=['POST'])
def generate_video():
    """Generate video from script"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        script = data.get('script')
        template = data.get('template', 'presenter1')
        user_id = data.get('userId', 'guest')
        
        if not script:
            return jsonify({"error": "Script is required"}), 400
        
        # Generate unique video ID
        video_id = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Initialize job
        active_jobs[video_id] = {
            "id": video_id,
            "status": "queued",
            "script": script,
            "template": template,
            "user_id": user_id,
            "progress": 0,
            "current_step": "Queued",
            "created_at": datetime.now().isoformat()
        }
        
        logger.info(f"Video generation started: {video_id}")
        
        if MOCK_MODE:
            # Simulate video generation
            socketio.start_background_task(simulate_video_generation, video_id)
            message = "Video generation started (MOCK MODE - No API calls)"
        else:
            # Real video generation (implement later)
            socketio.start_background_task(process_video_generation, video_id)
            message = "Video generation started"
        
        return jsonify({
            "id": video_id,
            "message": message,
            "status": "queued"
        }), 201
        
    except Exception as e:
        logger.error(f"Error in generate_video: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/video-status/<video_id>', methods=['GET'])
def video_status(video_id):
    """Get video generation status"""
    if video_id in active_jobs:
        return jsonify(active_jobs[video_id]), 200
    else:
        return jsonify({"error": "Video not found"}), 404

@app.route('/jobs', methods=['GET'])
def get_jobs():
    """Get all video jobs"""
    return jsonify({
        "total": len(active_jobs),
        "jobs": list(active_jobs.values())
    }), 200

def simulate_video_generation(video_id):
    """Mock video generation with progress updates"""
    import time
    
    steps = [
        (0, "queued", "Queued"),
        (10, "processing", "Polishing script with AI..."),
        (25, "processing", "Generating voiceover..."),
        (45, "processing", "Creating avatar video..."),
        (65, "processing", "Composing final video..."),
        (85, "processing", "Uploading to storage..."),
        (100, "completed", "Video ready!")
    ]
    
    for progress, status, step in steps:
        time.sleep(2)  # Simulate processing time
        
        active_jobs[video_id].update({
            'status': status,
            'progress': progress,
            'current_step': step
        })
        
        # Emit progress via WebSocket
        socketio.emit('video_progress', {
            'id': video_id,
            'progress': progress,
            'current_step': step,
            'status': status
        })
        
        logger.info(f"Video {video_id}: {progress}% - {step}")
    
    # Mark as completed
    active_jobs[video_id].update({
        'status': 'completed',
        'progress': 100,
        'video_url': 'https://example.com/mock-video.mp4',
        'completed_at': datetime.now().isoformat()
    })
    
    socketio.emit('video_progress', {
        'id': video_id,
        'progress': 100,
        'status': 'completed',
        'video_url': 'https://example.com/mock-video.mp4'
    })

def process_video_generation(video_id):
    """Real video generation (to be implemented)"""
    # TODO: Implement real video generation pipeline
    # 1. Polish script with OpenAI
    # 2. Generate voiceover with ElevenLabs
    # 3. Create avatar video with HeyGen
    # 4. Compose video with FFmpeg
    # 5. Upload to Wasabi S3
    # 6. Log metadata to Bubble
    pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
