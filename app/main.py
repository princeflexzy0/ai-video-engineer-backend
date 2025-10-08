from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env keys

app = Flask(__name__)
CORS(app)  # Allows frontend calls
socketio = SocketIO(app, cors_allowed_origins="*")  # SocketIO for real-time status

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'Backend alive!'})

@app.route('/generate-video', methods=['POST'])
def generate_video():
    try:
        data = request.get_json() or {}  # Safe JSON parse
        script = data.get('script', 'No script provided')
        template = data.get('template', 'default')
        userId = data.get('userId', 'unknown')
        
        video_id = 'mock-123'  # TODO: import uuid; str(uuid.uuid4())
        
        # Safe sid for socket (None if HTTP-only like curl)
        sid = getattr(request, 'sid', None)
        if sid:
            emit('video_status', {'message': 'Processing...', 'videoId': video_id}, room=sid)
        else:
            print(f"Mock emit (HTTP): Processing... for user {userId}, script len: {len(script)}")
        
        # TODO: Real pipeline (uncomment when ready)
        # from scripts.polish import polish_script
        # polished = polish_script(script)
        # ... (voice, presenter, compose, upload, bubble_log)
        # if sid: emit('video_status', {'message': 'Done!', 'url': video_url}, room=sid)
        # else: print(f"Mock emit (HTTP): Done! URL: {video_url}")
        
        # Mock response
        mock_url = 'https://example.com/mock-video.mp4'
        if sid:
            emit('video_status', {'message': 'Done!', 'url': mock_url, 'videoId': video_id}, room=sid)
        else:
            print(f"Mock emit (HTTP): Done! URL: {mock_url} for user {userId}")
        
        return jsonify({'id': video_id, 'status': 'started', 'mock_url': mock_url})
    except Exception as e:
        error_msg = str(e)
        sid = getattr(request, 'sid', None)
        if sid:
            emit('video_status', {'message': f'Error: {error_msg}'}, room=sid)
        else:
            print(f"Mock error emit (HTTP): {error_msg}")
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    # Unified run: Works local (port 5000 or 8000) and Render (PORT env, host 0.0.0.0)
    port = int(os.environ.get('PORT', 8000))  # Default 8000 for local to avoid 5000 conflict
    app.run(host='0.0.0.0', debug=True, port=port)