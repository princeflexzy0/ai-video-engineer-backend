cat > app/main.py << 'EOF'
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'Backend alive!'})

@app.route('/generate-video', methods=['POST'])
def generate_video():
    data = request.json
    script = data.get('script')
    template = data.get('template')
    user_id = data.get('userId')
    
    # Mock response for now
    video_id = 'mock-123'
    
    # Emit socket event (if connected)
    try:
        socketio.emit('video_status', {
            'id': video_id,
            'message': 'Video generation started',
            'progress': 10
        })
    except Exception as e:
        print(f"Socket emit error: {e}")
    
    return jsonify({
        'id': video_id,
        'status': 'started',
        'mock_url': 'https://example.com/mock-video.mp4'
    })

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('video_status', {'message': 'Connected to backend'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
EOF