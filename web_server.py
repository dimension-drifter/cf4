from flask import Flask, render_template, request, jsonify
from livekit import api
import os
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("web-server")

LIVEKIT_URL = os.getenv('LIVEKIT_URL', 'ws://localhost:7880')
LIVEKIT_API_KEY = os.getenv('LIVEKIT_API_KEY')
LIVEKIT_API_SECRET = os.getenv('LIVEKIT_API_SECRET')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-token', methods=['POST'])
def get_token():
    data = request.json
    room_name = data.get('roomName', 'default-room')
    participant_name = data.get('participantName', f'user-{os.urandom(4).hex()}')
    
    logger.info(f"🔑 Generating token for {participant_name} in room {room_name}")
    
    token = api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET) \
        .with_identity(participant_name) \
        .with_name(participant_name) \
        .with_grants(api.VideoGrants(
            room_join=True,
            room=room_name,
        ))
    
    return jsonify({
        'token': token.to_jwt(),
        'url': LIVEKIT_URL
    })

if __name__ == '__main__':
    logger.info("🌐 Web Server starting on http://localhost:5000")
    app.run(debug=False, port=5000, host='0.0.0.0', use_reloader=False)