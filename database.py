import sqlite3
import logging
from datetime import datetime
from typing import Optional, Dict, List
import json
from twilio_service import TwilioService

logger = logging.getLogger("database")

class HotelDatabase:
    def __init__(self, db_path: str = "hotel.db"):
        self.db_path = db_path
        self.twilio = TwilioService()
        self.init_database()
        self.migrate_database()
    
    def get_connection(self):
        """Get a database connection"""
        return sqlite3.connect(self.db_path)
    
    def migrate_database(self):
        """Migrate database to add new columns if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if total_bookings column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'total_bookings' not in columns:
            logger.info("Adding total_bookings column to users table")
            cursor.execute("ALTER TABLE users ADD COLUMN total_bookings INTEGER DEFAULT 0")
        
        if 'is_verified' not in columns:
            logger.info("Adding is_verified column to users table")
            cursor.execute("ALTER TABLE users ADD COLUMN is_verified INTEGER DEFAULT 0")
        
        conn.commit()
        conn.close()
        logger.info("Database migration completed")
    
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
                last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_bookings INTEGER DEFAULT 0,
                is_verified INTEGER DEFAULT 0
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
            
            # Mark as verified if we have both name and phone
            cursor.execute("SELECT name, phone FROM users WHERE user_id = ?", (user_id,))
            current = cursor.fetchone()
            current_name = current[0] if current else None
            current_phone = current[1] if current else None
            
            final_name = name if name else current_name
            final_phone = phone if phone else current_phone
            
            if final_name and final_phone:
                updates.append("is_verified = 1")
            
            updates.append("last_interaction = ?")
            params.append(datetime.now())
            params.append(user_id)
            
            if updates:
                cursor.execute(
                    f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?",
                    params
                )
        else:
            is_verified = 1 if (name and phone) else 0
            cursor.execute("""
                INSERT INTO users (user_id, name, phone, email, preferences, is_verified)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, name, phone, email, json.dumps(preferences or {}), is_verified))
        
        conn.commit()
        conn.close()
        logger.info(f"User {user_id} created/updated - name: {name}, phone: {phone}")
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get the user row
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        # Get column names to handle different schema versions
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        conn.close()
        
        result = {
            'user_id': row[0],
            'name': row[1],
            'phone': row[2],
            'email': row[3],
            'preferences': json.loads(row[4]) if row[4] else {},
            'created_at': row[5],
            'last_interaction': row[6],
        }
        
        # Add optional columns if they exist
        if len(row) > 7:
            result['total_bookings'] = row[7]
        else:
            result['total_bookings'] = 0
            
        if len(row) > 8:
            result['is_verified'] = row[8]
        else:
            result['is_verified'] = 0
        
        return result
    
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
        """Create a room booking and send confirmation SMS"""
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
        
        # Increment total bookings for user
        cursor.execute("""
            UPDATE users 
            SET total_bookings = total_bookings + 1
            WHERE user_id = ?
        """, (user_id,))
        
        conn.commit()
        
        # Get user details for SMS
        cursor.execute("SELECT name, phone FROM users WHERE user_id = ?", (user_id,))
        user_data = cursor.fetchone()
        
        conn.close()
        
        logger.info(f"Room booking created: {booking_id}")
        
        # Send confirmation SMS
        if user_data and user_data[1]:  # Check if phone exists
            guest_name = user_data[0] or "Guest"
            phone = user_data[1]
            
            logger.info(f"Sending confirmation SMS to {phone}")
            sms_sent = self.twilio.send_room_booking_confirmation(
                phone=phone,
                guest_name=guest_name,
                booking_id=booking_id,
                room_type=room_type,
                check_in=check_in_date,
                check_out=check_out_date
            )
            
            if sms_sent:
                logger.info(f"Confirmation SMS sent for booking {booking_id}")
            else:
                logger.warning(f"Failed to send SMS for booking {booking_id}")
        else:
            logger.warning(f"No phone number found for user {user_id}, SMS not sent")
        
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
        """Create a restaurant booking and send confirmation SMS"""
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
        
        # Increment total bookings for user
        cursor.execute("""
            UPDATE users 
            SET total_bookings = total_bookings + 1
            WHERE user_id = ?
        """, (user_id,))
        
        conn.commit()
        
        # Get user details for SMS
        cursor.execute("SELECT name, phone FROM users WHERE user_id = ?", (user_id,))
        user_data = cursor.fetchone()
        
        conn.close()
        
        logger.info(f"Restaurant booking created: {booking_id}")
        
        # Send confirmation SMS
        if user_data and user_data[1]:  # Check if phone exists
            guest_name = user_data[0] or "Guest"
            phone = user_data[1]
            
            logger.info(f"Sending confirmation SMS to {phone}")
            sms_sent = self.twilio.send_restaurant_booking_confirmation(
                phone=phone,
                guest_name=guest_name,
                booking_id=booking_id,
                restaurant_name=restaurant_name,
                booking_date=booking_date,
                booking_time=booking_time,
                num_guests=num_guests
            )
            
            if sms_sent:
                logger.info(f"Confirmation SMS sent for booking {booking_id}")
            else:
                logger.warning(f"Failed to send SMS for booking {booking_id}")
        else:
            logger.warning(f"No phone number found for user {user_id}, SMS not sent")
        
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
        """Cancel a booking and send notification SMS"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        table = "room_bookings" if booking_type == "room" else "restaurant_bookings"
        
        # Get booking and user details before cancelling
        cursor.execute(f"""
            SELECT b.user_id, u.name, u.phone
            FROM {table} b
            JOIN users u ON b.user_id = u.user_id
            WHERE b.booking_id = ?
        """, (booking_id,))
        
        result = cursor.fetchone()
        
        # Update booking status
        cursor.execute(f"""
            UPDATE {table}
            SET status = 'cancelled'
            WHERE booking_id = ?
        """, (booking_id,))
        
        conn.commit()
        conn.close()
        
        logger.info(f"{booking_type} booking {booking_id} cancelled")
        
        # Send cancellation SMS
        if result and result[2]:  # Check if phone exists
            user_id, guest_name, phone = result
            guest_name = guest_name or "Guest"
            
            self.twilio.send_cancellation_notification(
                phone=phone,
                guest_name=guest_name,
                booking_id=booking_id,
                booking_type=booking_type
            )
    
    def get_all_users(self) -> List[Dict]:
        """Get all users with their information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if columns exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        has_total_bookings = 'total_bookings' in columns
        has_is_verified = 'is_verified' in columns
        
        if has_total_bookings and has_is_verified:
            cursor.execute("""
                SELECT user_id, name, phone, email, created_at, total_bookings, is_verified
                FROM users
                ORDER BY last_interaction DESC
            """)
        else:
            cursor.execute("""
                SELECT user_id, name, phone, email, created_at
                FROM users
                ORDER BY last_interaction DESC
            """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'user_id': row[0],
                'name': row[1] or 'Not provided',
                'phone': row[2] or 'Not provided',
                'email': row[3] or 'Not provided',
                'created_at': row[4],
                'total_bookings': row[5] if len(row) > 5 else 0,
                'is_verified': 'Yes' if (len(row) > 6 and row[6]) else 'No'
            }
            for row in rows
        ]