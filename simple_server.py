# Simple Hotel Backend API Server for Testing
# This is a simplified version for testing the dashboard without LiveKit dependencies

import os
import uuid
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import random
import json

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"])  # Allow dashboard to access API

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Mock data storage (in production, use a proper database)
bookings_db = [
    {
        "id": "BK001",
        "guestName": "Rajesh Sharma",
        "email": "rajesh@example.com",
        "phone": "+91 9876543210",
        "checkIn": "2024-10-12",
        "checkOut": "2024-10-15",
        "roomNumber": "301",
        "roomType": "Deluxe",
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
        "roomNumber": "205",
        "roomType": "Standard",
        "totalAmount": 9000,
        "status": "pending",
        "paymentStatus": "pending",
        "createdAt": "2024-10-10T14:20:00Z"
    }
]

restaurant_orders_db = [
    {
        "id": "RO001",
        "orderType": "room-service",
        "roomNumber": "301",
        "customerName": "Rajesh Sharma",
        "items": [
            {"name": "Butter Chicken", "quantity": 2, "price": 450},
            {"name": "Naan", "quantity": 4, "price": 60},
            {"name": "Dal Makhani", "quantity": 1, "price": 320}
        ],
        "totalAmount": 1330,
        "status": "preparing",
        "orderTime": "2024-10-10T19:30:00Z",
        "estimatedDelivery": "2024-10-10T20:15:00Z"
    },
    {
        "id": "RO002",
        "orderType": "restaurant",
        "tableNumber": "T05",
        "customerName": "Priya Patel",
        "items": [
            {"name": "Masala Dosa", "quantity": 1, "price": 180},
            {"name": "Filter Coffee", "quantity": 2, "price": 80}
        ],
        "totalAmount": 340,
        "status": "served",
        "orderTime": "2024-10-10T09:15:00Z",
        "estimatedDelivery": "2024-10-10T09:45:00Z"
    }
]

call_logs_db = [
    {
        "id": "CALL001",
        "timestamp": "2024-10-10T18:45:00Z",
        "duration": 180,
        "callerNumber": "+91 9876543210",
        "callType": "booking_inquiry",
        "sentiment": "positive",
        "resolution": "booking_confirmed",
        "agentName": "AI Assistant",
        "transcript": "Customer inquired about room availability for October 15-17. Confirmed deluxe room booking.",
        "satisfaction": 4.5
    },
    {
        "id": "CALL002",
        "timestamp": "2024-10-10T16:20:00Z",
        "duration": 120,
        "callerNumber": "+91 9876543211",
        "callType": "room_service",
        "sentiment": "neutral",
        "resolution": "order_placed",
        "agentName": "AI Assistant",
        "transcript": "Guest requested room service for dinner. Order placed successfully.",
        "satisfaction": 4.0
    }
]

live_calls_db = [
    {
        "id": "LIVE001",
        "callerNumber": "+91 9876543212",
        "callType": "complaint",
        "status": "active",
        "startTime": "2024-10-10T20:30:00Z",
        "currentTopic": "room_temperature",
        "sentiment": "negative",
        "agentName": "AI Assistant",
        "liveTranscript": "Guest is complaining about the air conditioning not working properly..."
    }
]

# API Routes

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "🏨 The Pink Pearl Hotel Admin Dashboard Backend",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "dashboard": "/api/dashboard/stats",
            "bookings": "/api/bookings",
            "restaurant": "/api/restaurant/orders",
            "calls": "/api/calls/logs",
            "live_calls": "/api/calls/live"
        },
        "frontend": "http://localhost:3000"
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Hotel API Server is running"}), 200

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    # Generate some realistic stats
    today = datetime.now()
    stats = {
        "totalBookings": len(bookings_db),
        "occupancyRate": 75.5,
        "revenue": {
            "today": 25000,
            "month": 750000,
            "growth": 12.5
        },
        "callMetrics": {
            "totalCalls": 45,
            "avgDuration": 150,
            "satisfactionScore": 4.3,
            "resolutionRate": 92
        },
        "recentActivity": [
            {"type": "booking", "message": "New booking confirmed - Room 301", "time": "2 min ago"},
            {"type": "call", "message": "Call completed - Booking inquiry", "time": "5 min ago"},
            {"type": "order", "message": "Room service order delivered", "time": "8 min ago"}
        ],
        "chartData": {
            "revenue": [
                {"name": "Mon", "value": 12000},
                {"name": "Tue", "value": 19000},
                {"name": "Wed", "value": 15000},
                {"name": "Thu", "value": 25000},
                {"name": "Fri", "value": 30000},
                {"name": "Sat", "value": 35000},
                {"name": "Sun", "value": 28000}
            ],
            "sentiment": [
                {"name": "Positive", "value": 65, "color": "#10B981"},
                {"name": "Neutral", "value": 25, "color": "#F59E0B"},
                {"name": "Negative", "value": 10, "color": "#EF4444"}
            ]
        }
    }
    return jsonify(stats), 200

# Booking Management
@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    return jsonify(bookings_db), 200

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    new_booking = {
        "id": f"BK{random.randint(100, 999)}",
        "guestName": data.get('guestName'),
        "email": data.get('email'),
        "phone": data.get('phone'),
        "checkIn": data.get('checkIn'),
        "checkOut": data.get('checkOut'),
        "roomNumber": data.get('roomNumber'),
        "roomType": data.get('roomType'),
        "totalAmount": data.get('totalAmount'),
        "status": data.get('status', 'pending'),
        "paymentStatus": data.get('paymentStatus', 'pending'),
        "createdAt": datetime.now().isoformat()
    }
    bookings_db.append(new_booking)
    return jsonify(new_booking), 201

@app.route('/api/bookings/<booking_id>', methods=['PUT'])
def update_booking(booking_id):
    data = request.get_json()
    for i, booking in enumerate(bookings_db):
        if booking['id'] == booking_id:
            bookings_db[i].update(data)
            return jsonify(bookings_db[i]), 200
    return jsonify({"error": "Booking not found"}), 404

@app.route('/api/bookings/<booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    global bookings_db
    bookings_db = [b for b in bookings_db if b['id'] != booking_id]
    return jsonify({"message": "Booking deleted successfully"}), 200

# Restaurant Management
@app.route('/api/restaurant/orders', methods=['GET'])
def get_restaurant_orders():
    return jsonify(restaurant_orders_db), 200

@app.route('/api/restaurant/orders', methods=['POST'])
def create_restaurant_order():
    data = request.get_json()
    new_order = {
        "id": f"RO{random.randint(100, 999)}",
        "orderType": data.get('orderType'),
        "roomNumber": data.get('roomNumber'),
        "tableNumber": data.get('tableNumber'),
        "customerName": data.get('customerName'),
        "items": data.get('items', []),
        "totalAmount": data.get('totalAmount'),
        "status": data.get('status', 'pending'),
        "orderTime": datetime.now().isoformat(),
        "estimatedDelivery": (datetime.now() + timedelta(minutes=30)).isoformat()
    }
    restaurant_orders_db.append(new_order)
    return jsonify(new_order), 201

@app.route('/api/restaurant/orders/<order_id>', methods=['PUT'])
def update_restaurant_order(order_id):
    data = request.get_json()
    for i, order in enumerate(restaurant_orders_db):
        if order['id'] == order_id:
            restaurant_orders_db[i].update(data)
            return jsonify(restaurant_orders_db[i]), 200
    return jsonify({"error": "Order not found"}), 404

# Call Analytics
@app.route('/api/calls/logs', methods=['GET'])
def get_call_logs():
    return jsonify(call_logs_db), 200

@app.route('/api/calls/analytics', methods=['GET'])
def get_call_analytics():
    analytics = {
        "totalCalls": len(call_logs_db),
        "avgDuration": sum(call['duration'] for call in call_logs_db) / len(call_logs_db) if call_logs_db else 0,
        "sentimentBreakdown": {
            "positive": len([c for c in call_logs_db if c['sentiment'] == 'positive']),
            "neutral": len([c for c in call_logs_db if c['sentiment'] == 'neutral']),
            "negative": len([c for c in call_logs_db if c['sentiment'] == 'negative'])
        },
        "resolutionRate": 92.5,
        "avgSatisfaction": sum(call['satisfaction'] for call in call_logs_db) / len(call_logs_db) if call_logs_db else 0,
        "callTypeBreakdown": {
            "booking_inquiry": len([c for c in call_logs_db if c['callType'] == 'booking_inquiry']),
            "room_service": len([c for c in call_logs_db if c['callType'] == 'room_service']),
            "complaint": len([c for c in call_logs_db if c['callType'] == 'complaint']),
            "general_inquiry": len([c for c in call_logs_db if c['callType'] == 'general_inquiry'])
        }
    }
    return jsonify(analytics), 200

# Live Call Monitoring
@app.route('/api/calls/live', methods=['GET'])
def get_live_calls():
    return jsonify(live_calls_db), 200

@app.route('/api/calls/live/<call_id>/end', methods=['POST'])
def end_live_call(call_id):
    global live_calls_db
    for call in live_calls_db:
        if call['id'] == call_id:
            call['status'] = 'ended'
            call['endTime'] = datetime.now().isoformat()
            # Move to call logs
            call_log = {
                "id": call['id'],
                "timestamp": call['startTime'],
                "duration": random.randint(60, 300),
                "callerNumber": call['callerNumber'],
                "callType": call['callType'],
                "sentiment": call['sentiment'],
                "resolution": "handled",
                "agentName": call['agentName'],
                "transcript": call['liveTranscript'],
                "satisfaction": random.uniform(3.5, 5.0)
            }
            call_logs_db.append(call_log)
            live_calls_db.remove(call)
            return jsonify({"message": "Call ended successfully"}), 200
    return jsonify({"error": "Call not found"}), 404

if __name__ == '__main__':
    print("🏨 Starting Hotel Admin Dashboard Backend Server...")
    print("🔧 Backend API will be available at: http://localhost:5000")
    print("📊 Dashboard should connect at: http://localhost:3000")
    print("💚 Health check: http://localhost:5000/api/health")
    app.run(debug=True, host='0.0.0.0', port=5000)