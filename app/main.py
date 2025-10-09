# In backend Codespace - create correct main.py file
cat > app/main.py << 'EOF'
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'AI Video Engineer Backend', 'status': 'online'})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'Backend alive!'})

@app.route('/generate-video', methods=['POST'])
def generate_video():
    try:
        data = request.get_json()
        script = data.get('script', '')
        template = data.get('template', 'presenter1')
        user_id = data.get('userId', 'anonymous')
        
        video_id = 'mock-123'
        
        socketio.emit('video_status', {
            'id': video_id,
            'message': 'Video generation started',
            'progress': 10,
            'userId': user_id
        }, broadcast=True)
        
        return jsonify({
            'id': video_id,
            'status': 'started',
            'mock_url': 'https://example.com/mock-video.mp4',
            'message': 'Video generation initiated'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('video_status', {'message': 'Connected to backend'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
EOF