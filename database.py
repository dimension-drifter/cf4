import sqlite3
import logging
from datetime import datetime
from typing import Optional, Dict, List
import json

logger = logging.getLogger("database")

class HotelDatabase:
    def __init__(self, db_path: str = "hotel.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get a database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table - stores user information and preferences
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                phone TEXT,
                email TEXT,
                preferences TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Conversation history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                message TEXT,
                speaker TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        
        # Room bookings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS room_bookings (
                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                room_type TEXT,
                check_in_date DATE,
                check_out_date DATE,
                num_adults INTEGER,
                num_children INTEGER DEFAULT 0,
                special_requests TEXT,
                status TEXT DEFAULT 'confirmed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        
        # Restaurant bookings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS restaurant_bookings (
                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                restaurant_name TEXT,
                booking_date DATE,
                booking_time TEXT,
                num_guests INTEGER,
                special_requests TEXT,
                status TEXT DEFAULT 'confirmed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    # User Management
    def create_or_update_user(self, user_id: str, name: str = None, 
                             phone: str = None, email: str = None, 
                             preferences: Dict = None):
        """Create or update user information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        existing = cursor.fetchone()
        
        if existing:
            updates = []
            params = []
            if name:
                updates.append("name = ?")
                params.append(name)
            if phone:
                updates.append("phone = ?")
                params.append(phone)
            if email:
                updates.append("email = ?")
                params.append(email)
            if preferences:
                updates.append("preferences = ?")
                params.append(json.dumps(preferences))
            
            updates.append("last_interaction = ?")
            params.append(datetime.now())
            params.append(user_id)
            
            cursor.execute(
                f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?",
                params
            )
        else:
            cursor.execute("""
                INSERT INTO users (user_id, name, phone, email, preferences)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, name, phone, email, json.dumps(preferences or {})))
        
        conn.commit()
        conn.close()
        logger.info(f"User {user_id} created/updated")
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'user_id': row[0],
                'name': row[1],
                'phone': row[2],
                'email': row[3],
                'preferences': json.loads(row[4]) if row[4] else {},
                'created_at': row[5],
                'last_interaction': row[6]
            }
        return None
    
    # Conversation History
    def add_conversation(self, user_id: str, message: str, speaker: str):
        """Add a conversation message"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO conversations (user_id, message, speaker)
            VALUES (?, ?, ?)
        """, (user_id, message, speaker))
        
        conn.commit()
        conn.close()
    
    def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get recent conversation history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT message, speaker, timestamp
            FROM conversations
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (user_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {'message': row[0], 'speaker': row[1], 'timestamp': row[2]}
            for row in reversed(rows)
        ]
    
    # Room Bookings
    def create_room_booking(self, user_id: str, room_type: str, 
                           check_in_date: str, check_out_date: str,
                           num_adults: int, num_children: int = 0,
                           special_requests: str = "") -> int:
        """Create a room booking"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO room_bookings 
            (user_id, room_type, check_in_date, check_out_date, 
             num_adults, num_children, special_requests)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, room_type, check_in_date, check_out_date,
              num_adults, num_children, special_requests))
        
        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Room booking created: {booking_id}")
        return booking_id
    
    def get_user_room_bookings(self, user_id: str) -> List[Dict]:
        """Get all room bookings for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM room_bookings
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'booking_id': row[0],
                'user_id': row[1],
                'room_type': row[2],
                'check_in_date': row[3],
                'check_out_date': row[4],
                'num_adults': row[5],
                'num_children': row[6],
                'special_requests': row[7],
                'status': row[8],
                'created_at': row[9]
            }
            for row in rows
        ]
    
    # Restaurant Bookings
    def create_restaurant_booking(self, user_id: str, restaurant_name: str,
                                 booking_date: str, booking_time: str,
                                 num_guests: int, special_requests: str = "") -> int:
        """Create a restaurant booking"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO restaurant_bookings
            (user_id, restaurant_name, booking_date, booking_time,
             num_guests, special_requests)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, restaurant_name, booking_date, booking_time,
              num_guests, special_requests))
        
        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Restaurant booking created: {booking_id}")
        return booking_id
    
    def get_user_restaurant_bookings(self, user_id: str) -> List[Dict]:
        """Get all restaurant bookings for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM restaurant_bookings
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'booking_id': row[0],
                'user_id': row[1],
                'restaurant_name': row[2],
                'booking_date': row[3],
                'booking_time': row[4],
                'num_guests': row[5],
                'special_requests': row[6],
                'status': row[7],
                'created_at': row[8]
            }
            for row in rows
        ]
    
    def cancel_booking(self, booking_id: int, booking_type: str):
        """Cancel a booking"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        table = "room_bookings" if booking_type == "room" else "restaurant_bookings"
        cursor.execute(f"""
            UPDATE {table}
            SET status = 'cancelled'
            WHERE booking_id = ?
        """, (booking_id,))
        
        conn.commit()
        conn.close()
        logger.info(f"{booking_type} booking {booking_id} cancelled")