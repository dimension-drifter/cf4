# server.py (Version 5 - Fixed Agent Dispatch)
import os
import uuid
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from livekit import api
from dotenv import load_dotenv

# Basic logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app) 

livekit_api = None

@app.route("/create_token", methods=["POST"])
async def create_token():
    global livekit_api

    if livekit_api is None:
        LIVEKIT_URL = os.environ.get("LIVEKIT_URL")
        LIVEKIT_API_KEY = os.environ.get("LIVEKIT_API_KEY")
        LIVEKIT_API_SECRET = os.environ.get("LIVEKIT_API_SECRET")

        if not all([LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET]):
            logging.error("LiveKit server credentials are not configured")
            return jsonify({"error": "LiveKit server credentials are not configured"}), 500

        http_url = LIVEKIT_URL.replace("wss://", "https://").replace("ws://", "http://")
        
        livekit_api = api.LiveKitAPI(http_url, LIVEKIT_API_KEY, LIVEKIT_API_SECRET)

    data = request.get_json()
    user_name = data.get("name")
    if not user_name:
        return jsonify({"error": "Name is required"}), 400

    try:
        room_name = f"agent-demo-{uuid.uuid4().hex[:8]}"
        logging.info(f"Creating new session for '{user_name}' in room '{room_name}'")
        
        await livekit_api.room.create_room(api.CreateRoomRequest(name=room_name))
        logging.info(f"Room '{room_name}' created.")

        token = (
            api.AccessToken(os.environ.get("LIVEKIT_API_KEY"), os.environ.get("LIVEKIT_API_SECRET"))
            .with_identity(user_name)
            .with_name(user_name)
            .with_grants(api.VideoGrants(room_join=True, room=room_name))
            .to_jwt()
        )
        logging.info(f"Token for '{user_name}' created.")

        # Dispatch agent to the room
        try:
            await livekit_api.agent_dispatch.create_dispatch(
                room=room_name,
                agent_name="my-agent"  # This should match the agent name from your agent worker
            )
            logging.info(f"Agent dispatched successfully to room '{room_name}'.")
        except Exception as dispatch_error:
            logging.warning(f"Agent dispatch failed (agent may join automatically): {dispatch_error}")
            # Don't fail the request - the agent worker might pick up the room automatically
        
        return jsonify({"token": token, "livekit_url": os.environ.get("LIVEKIT_URL")})
    
    except Exception as e:
        logging.error(f"An error occurred in create_token: {e}", exc_info=True)
        return jsonify({"error": "Failed to set up agent session."}), 500

# To run this server, use the command:
# hypercorn server:app --bind "0.0.0.0:5000"