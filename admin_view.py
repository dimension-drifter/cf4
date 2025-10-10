from flask import Flask, render_template
from database import HotelDatabase
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

db = HotelDatabase()

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard to view all bookings"""
    return render_template('admin.html')

@app.route('/admin/api/bookings')
def get_all_bookings():
    """API endpoint to get all bookings"""
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Get all room bookings
    cursor.execute("""
        SELECT rb.*, u.name, u.phone, u.email
        FROM room_bookings rb
        LEFT JOIN users u ON rb.user_id = u.user_id
        ORDER BY rb.created_at DESC
    """)
    room_bookings = cursor.fetchall()
    
    # Get all restaurant bookings
    cursor.execute("""
        SELECT rb.*, u.name, u.phone, u.email
        FROM restaurant_bookings rb
        LEFT JOIN users u ON rb.user_id = u.user_id
        ORDER BY rb.created_at DESC
    """)
    restaurant_bookings = cursor.fetchall()
    
    conn.close()
    
    return {
        'room_bookings': [
            {
                'booking_id': row[0],
                'room_type': row[2],
                'check_in': row[3],
                'check_out': row[4],
                'adults': row[5],
                'children': row[6],
                'special_requests': row[7],
                'status': row[8],
                'name': row[10],
                'phone': row[11],
                'email': row[12]
            } for row in room_bookings
        ],
        'restaurant_bookings': [
            {
                'booking_id': row[0],
                'restaurant': row[2],
                'date': row[3],
                'time': row[4],
                'guests': row[5],
                'special_requests': row[6],
                'status': row[7],
                'name': row[9],
                'phone': row[10],
                'email': row[11]
            } for row in restaurant_bookings
        ]
    }

if __name__ == '__main__':
    app.run(debug=True, port=5001)