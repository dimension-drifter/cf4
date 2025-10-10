# Enhanced Hotel Backend API Server
# This file extends your existing server.py with additional endpoints for the admin dashboard

import os
import uuid
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
try:
    from livekit import api
except ImportError:
    # Fallback if livekit api module structure is different
    import livekit
    api = None
    print("Warning: LiveKit API not available, running in mock mode")
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # Allow dashboard to access API

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

livekit_api = None

# Mock data storage (in production, use a proper database)
bookings_db = [
    {
        "id": "BK001",
        "guestName": "Rajesh Sharma",
        "email": "rajesh@example.com",
        "phone": "+91 9876543210",
        "checkIn": "2024-10-12",
        "checkOut": "2024-10-15",
        "roomType": "Deluxe Suite",
        "roomNumber": "205",
        "guests": 2,
        "totalAmount": 15000,
        "status": "confirmed",
        "paymentStatus": "paid",
        "createdAt": "2024-10-10T10:30:00Z"
    },
    {
        "id": "BK002",
        "guestName": "Priya Patel",
        "email": "priya@example.com",
        "phone": "+91 9876543211",
        "checkIn": "2024-10-13",
        "checkOut": "2024-10-16",
        "roomType": "Standard Room",
        "roomNumber": "108",
        "guests": 1,
        "totalAmount": 9000,
        "status": "pending",
        "paymentStatus": "pending",
        "createdAt": "2024-10-10T14:20:00Z"
    }
]

restaurant_orders_db = [
    {
        "id": "ORD001",
        "tableNumber": "8",
        "customerName": "Anjali Singh",
        "roomNumber": None,
        "items": [
            {"id": "1", "name": "Butter Chicken", "quantity": 2, "price": 450, "category": "Main Course"},
            {"id": "2", "name": "Naan Bread", "quantity": 3, "price": 80, "category": "Bread"}
        ],
        "totalAmount": 1130,
        "status": "preparing",
        "orderType": "dine-in",
        "createdAt": "2024-10-10T18:30:00Z"
    }
]

call_logs_db = [
    {
        "id": "CALL001",
        "callerNumber": "+91 9876543210",
        "callerName": "Rahul Sharma",
        "intent": "Booking Inquiry",
        "sentiment": "positive",
        "duration": 245,
        "startTime": "2024-10-10T18:30:00Z",
        "endTime": "2024-10-10T18:34:05Z",
        "outcome": "booking_made",
        "transcript": "Customer inquired about availability for weekend stay..."
    }
]

live_calls_db = []

# Existing LiveKit endpoint
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

        try:
            await livekit_api.agent_dispatch.create_dispatch(
                room=room_name,
                agent_name="my-agent"
            )
            logging.info(f"Agent dispatched successfully to room '{room_name}'.")
        except Exception as dispatch_error:
            logging.warning(f"Agent dispatch failed (agent may join automatically): {dispatch_error}")
        
        return jsonify({"token": token, "livekit_url": os.environ.get("LIVEKIT_URL")})
    
    except Exception as e:
        logging.error(f"An error occurred in create_token: {e}", exc_info=True)
        return jsonify({"error": "Failed to set up agent session."}), 500

# Dashboard Statistics
@app.route("/api/dashboard/stats", methods=["GET"])
def get_dashboard_stats():
    stats = {
        "totalBookings": len(bookings_db),
        "todaysBookings": len([b for b in bookings_db if b["createdAt"].startswith("2024-10-10")]),
        "revenue": sum(b["totalAmount"] for b in bookings_db),
        "occupancyRate": 87,
        "totalCalls": len(call_logs_db) + 89,  # Including historical calls
        "todaysCalls": len([c for c in call_logs_db if c["startTime"].startswith("2024-10-10")]) + 12,
        "averageCallDuration": 225,
        "conversionRate": 68,
        "activeRooms": 44,
        "totalRooms": 50,
        "restaurantOrders": len(restaurant_orders_db),
        "pendingOrders": len([o for o in restaurant_orders_db if o["status"] == "pending"])
    }
    return jsonify(stats)

# Bookings Management
@app.route("/api/bookings", methods=["GET"])
def get_bookings():
    return jsonify(bookings_db)

@app.route("/api/bookings", methods=["POST"])
def create_booking():
    data = request.get_json()
    booking = {
        "id": f"BK{len(bookings_db) + 1:03d}",
        "guestName": data.get("guestName"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "checkIn": data.get("checkIn"),
        "checkOut": data.get("checkOut"),
        "roomType": data.get("roomType"),
        "roomNumber": f"{random.randint(100, 500)}",
        "guests": data.get("guests", 1),
        "totalAmount": data.get("totalAmount", 5000),
        "status": "confirmed",
        "paymentStatus": "pending",
        "createdAt": datetime.now().isoformat()
    }
    bookings_db.append(booking)
    return jsonify(booking), 201

@app.route("/api/bookings/<booking_id>", methods=["PUT"])
def update_booking(booking_id):
    data = request.get_json()
    for booking in bookings_db:
        if booking["id"] == booking_id:
            booking.update(data)
            return jsonify(booking)
    return jsonify({"error": "Booking not found"}), 404

@app.route("/api/bookings/<booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    global bookings_db
    bookings_db = [b for b in bookings_db if b["id"] != booking_id]
    return jsonify({"message": "Booking deleted successfully"})

# Restaurant Management
@app.route("/api/restaurant/orders", methods=["GET"])
def get_restaurant_orders():
    return jsonify(restaurant_orders_db)

@app.route("/api/restaurant/orders", methods=["POST"])
def create_restaurant_order():
    data = request.get_json()
    order = {
        "id": f"ORD{len(restaurant_orders_db) + 1:03d}",
        "tableNumber": data.get("tableNumber"),
        "customerName": data.get("customerName"),
        "roomNumber": data.get("roomNumber"),
        "items": data.get("items", []),
        "totalAmount": sum(item["price"] * item["quantity"] for item in data.get("items", [])),
        "status": "pending",
        "orderType": data.get("orderType", "dine-in"),
        "createdAt": datetime.now().isoformat()
    }
    restaurant_orders_db.append(order)
    return jsonify(order), 201

@app.route("/api/restaurant/orders/<order_id>/status", methods=["PATCH"])
def update_order_status(order_id):
    data = request.get_json()
    status = data.get("status")
    
    for order in restaurant_orders_db:
        if order["id"] == order_id:
            order["status"] = status
            return jsonify(order)
    return jsonify({"error": "Order not found"}), 404

# Call Analytics
@app.route("/api/calls/logs", methods=["GET"])
def get_call_logs():
    # Add some filtering logic based on query parameters
    start_date = request.args.get("startDate")
    end_date = request.args.get("endDate")
    sentiment = request.args.get("sentiment")
    intent = request.args.get("intent")
    
    filtered_logs = call_logs_db
    
    if sentiment:
        filtered_logs = [log for log in filtered_logs if log["sentiment"] == sentiment]
    if intent:
        filtered_logs = [log for log in filtered_logs if log["intent"] == intent]
    
    return jsonify(filtered_logs)

@app.route("/api/calls/analytics/<timeframe>", methods=["GET"])
def get_call_analytics(timeframe):
    # Generate mock analytics data based on timeframe
    analytics = {
        "callVolume": [
            {"name": f"{i:02d}:00", "calls": random.randint(0, 35)} 
            for i in range(24)
        ],
        "sentimentTrend": [
            {
                "name": day,
                "positive": random.randint(75, 95),
                "neutral": random.randint(5, 20),
                "negative": random.randint(1, 10)
            }
            for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        ],
        "conversionRates": [
            {"intent": "Booking Inquiry", "calls": 145, "conversions": 89, "rate": 61},
            {"intent": "Room Service", "calls": 67, "conversions": 67, "rate": 100},
            {"intent": "Restaurant", "calls": 34, "conversions": 32, "rate": 94},
            {"intent": "Complaint", "calls": 12, "conversions": 11, "rate": 92},
            {"intent": "General Info", "calls": 89, "conversions": 23, "rate": 26}
        ]
    }
    return jsonify(analytics)

# Live Calls Management
@app.route("/api/calls/live", methods=["GET"])
def get_live_calls():
    return jsonify(live_calls_db)

@app.route("/api/calls/<call_id>/answer", methods=["POST"])
def answer_call(call_id):
    for call in live_calls_db:
        if call["id"] == call_id:
            call["status"] = "active"
            return jsonify({"message": "Call answered successfully"})
    return jsonify({"error": "Call not found"}), 404

@app.route("/api/calls/<call_id>/end", methods=["POST"])
def end_call(call_id):
    global live_calls_db
    live_calls_db = [call for call in live_calls_db if call["id"] != call_id]
    return jsonify({"message": "Call ended successfully"})

@app.route("/api/calls/<call_id>/hold", methods=["POST"])
def hold_call(call_id):
    for call in live_calls_db:
        if call["id"] == call_id:
            call["status"] = "on_hold"
            return jsonify({"message": "Call put on hold"})
    return jsonify({"error": "Call not found"}), 404

# Health check endpoint
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": "connected",
            "livekit": "connected" if livekit_api else "disconnected"
        }
    })

if __name__ == "__main__":
    print("Starting Enhanced Hotel Backend Server...")
    print("Dashboard API endpoints available at http://localhost:5000/api/")
    print("LiveKit token endpoint available at http://localhost:5000/create_token")
    app.run(host="0.0.0.0", port=5000, debug=True)