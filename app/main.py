from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import sys
import uuid
from datetime import datetime
import threading

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

try:
    from polish import polish_script
    from voiceover import generate_voiceover
    from presenter import create_heygen_video
    from composition import compose_video
    from storage import upload_to_wasabi
    from bubble import save_to_bubble
except ImportError as e:
    print(f"Warning: Could not import processing scripts: {e}")
    print("Running in mock mode...")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

active_jobs = {}

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'AI Video Engineer Backend',
        'status': 'online',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'generate': '/generate-video'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'Backend alive!',
        'timestamp': datetime.utcnow().isoformat(),
        'active_jobs': len(active_jobs)
    })

def process_video(video_id, script, template, user_id):
    try:
        socketio.emit('video_status', {
            'id': video_id,
            'status': 'processing',
            'message': 'Polishing script with AI...',
            'progress': 10,
            'userId': user_id
        }, broadcast=True)
        
        polished_script = polish_script(script)
        
        socketio.emit('video_status', {
            'id': video_id,
            'status': 'processing',
            'message': 'Generating voiceover...',
            'progress': 30,
            'userId': user_id
        }, broadcast=True)
        
        audio_file = generate_voiceover(polished_script, f"temp_{video_id}_audio.mp3")
        
        socketio.emit('video_status', {
            'id': video_id,
            'status': 'processing',
            'message': 'Creating AI presenter video...',
            'progress': 50,
            'userId': user_id
        }, broadcast=True)
        
        presenter_video_url = create_heygen_video(polished_script, template)
        
        import requests
        presenter_video_path = f"temp_{video_id}_presenter.mp4"
        with open(presenter_video_path, 'wb') as f:
            f.write(requests.get(presenter_video_url).content)
        
        socketio.emit('video_status', {
            'id': video_id,
            'status': 'processing',
            'message': 'Composing final video...',
            'progress': 70,
            'userId': user_id
        }, broadcast=True)
        
        final_video_path = compose_video(presenter_video_path, audio_file, f"final_{video_id}.mp4")
        
        socketio.emit('video_status', {
            'id': video_id,
            'status': 'processing',
            'message': 'Uploading to cloud storage...',
            'progress': 85,
            'userId': user_id
        }, broadcast=True)
        
        video_url = upload_to_wasabi(final_video_path, f"videos/{video_id}.mp4")
        
        socketio.emit('video_status', {
            'id': video_id,
            'status': 'processing',
            'message': 'Finalizing...',
            'progress': 95,
            'userId': user_id
        }, broadcast=True)
        
        save_to_bubble({
            'id': video_id,
            'userId': user_id,
            'script': polished_script,
            'videoUrl': video_url,
            'template': template
        })
        
        for temp_file in [audio_file, presenter_video_path, final_video_path]:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        socketio.emit('video_status', {
            'id': video_id,
            'status': 'completed',
            'message': 'Video generation complete!',
            'progress': 100,
            'videoUrl': video_url,
            'userId': user_id
        }, broadcast=True)
        
        active_jobs[video_id] = {
            'status': 'completed',
            'videoUrl': video_url,
            'completedAt': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        error_message = str(e)
        print(f"❌ Error processing video {video_id}: {error_message}")
        
        socketio.emit('video_status', {
            'id': video_id,
            'status': 'failed',
            'message': f'Error: {error_message}',
            'progress': 0,
            'userId': user_id
        }, broadcast=True)
        
        active_jobs[video_id] = {
            'status': 'failed',
            'error': error_message,
            'failedAt': datetime.utcnow().isoformat()
        }

@app.route('/generate-video', methods=['POST'])
def generate_video():
    try:
        data = request.get_json()
        script = data.get('script', '').strip()
        template = data.get('template', 'presenter1')
        user_id = data.get('userId', 'anonymous')
        
        if not script:
            return jsonify({'error': 'Script is required'}), 400
        
        video_id = str(uuid.uuid4())
        
        active_jobs[video_id] = {
            'status': 'started',
            'startedAt': datetime.utcnow().isoformat()
        }
        
        thread = threading.Thread(
            target=process_video,
            args=(video_id, script, template, user_id)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'id': video_id,
            'status': 'started',
            'message': 'Video generation initiated'
        }), 202
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/video-status/<video_id>', methods=['GET'])
def get_video_status(video_id):
    job = active_jobs.get(video_id)
    if not job:
        return jsonify({'error': 'Video not found'}), 404
    return jsonify(job)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('video_status', {'message': 'Connected to AI Video Engineer backend'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
