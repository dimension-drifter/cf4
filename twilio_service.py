import os
import logging
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("twilio-service")

class TwilioService:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if not all([self.account_sid, self.auth_token, self.from_number]):
            logger.warning("Twilio credentials not configured. SMS notifications will be disabled.")
            self.client = None
        else:
            self.client = Client(self.account_sid, self.auth_token)
            logger.info("Twilio service initialized successfully")
    
    def format_phone_number(self, phone: str) -> str:
        """Format phone number to E.164 format with +91 prefix"""
        # Remove all non-digit characters except +
        phone = ''.join(c for c in phone if c.isdigit() or c == '+')
        
        # If already has country code, return as is
        if phone.startswith('+'):
            return phone
        
        # Remove leading 0 if present
        if phone.startswith('0'):
            phone = phone[1:]
        
        # Add +91 for Indian numbers
        return f'+91{phone}'
    
    def send_room_booking_confirmation(self, phone: str, guest_name: str, 
                                      booking_id: int, room_type: str,
                                      check_in: str, check_out: str) -> bool:
        """Send room booking confirmation SMS"""
        if not self.client:
            logger.warning("Twilio not configured. Skipping SMS.")
            return False
        
        try:
            formatted_phone = self.format_phone_number(phone)
            
            message_body = f"""
🏨 Pink Pearl Hotel - Booking Confirmed

Dear {guest_name},

Your room booking has been confirmed!

📋 Booking ID: {booking_id}
🛏️ Room Type: {room_type}
📅 Check-in: {check_in}
📅 Check-out: {check_out}

We look forward to welcoming you!

For any queries, call: +91-XXX-XXXX-XXX

- Team Pink Pearl
            """.strip()
            
            message = self.client.messages.create(
                body=message_body,
                from_=self.from_number,
                to=formatted_phone
            )
            
            logger.info(f"Room booking SMS sent to {formatted_phone}. SID: {message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send room booking SMS: {e}")
            return False
    
    def send_restaurant_booking_confirmation(self, phone: str, guest_name: str,
                                            booking_id: int, restaurant_name: str,
                                            booking_date: str, booking_time: str,
                                            num_guests: int) -> bool:
        """Send restaurant booking confirmation SMS"""
        if not self.client:
            logger.warning("Twilio not configured. Skipping SMS.")
            return False
        
        try:
            formatted_phone = self.format_phone_number(phone)
            
            message_body = f"""
🍽️ Pink Pearl Hotel - Table Reserved

Dear {guest_name},

Your table has been reserved!

📋 Booking ID: {booking_id}
🍴 Restaurant: {restaurant_name}
📅 Date: {booking_date}
🕐 Time: {booking_time}
👥 Guests: {num_guests}

We look forward to serving you!

For any changes, call: +91-XXX-XXXX-XXX

- Team Pink Pearl
            """.strip()
            
            message = self.client.messages.create(
                body=message_body,
                from_=self.from_number,
                to=formatted_phone
            )
            
            logger.info(f"Restaurant booking SMS sent to {formatted_phone}. SID: {message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send restaurant booking SMS: {e}")
            return False
    
    def send_cancellation_notification(self, phone: str, guest_name: str,
                                      booking_id: int, booking_type: str) -> bool:
        """Send booking cancellation SMS"""
        if not self.client:
            logger.warning("Twilio not configured. Skipping SMS.")
            return False
        
        try:
            formatted_phone = self.format_phone_number(phone)
            
            message_body = f"""
❌ Pink Pearl Hotel - Booking Cancelled

Dear {guest_name},

Your {booking_type} booking (ID: {booking_id}) has been cancelled.

If this was a mistake, please contact us immediately.

Call: +91999999999

- Team Pink Pearl
            """.strip()
            
            message = self.client.messages.create(
                body=message_body,
                from_=self.from_number,
                to=formatted_phone
            )
            
            logger.info(f"Cancellation SMS sent to {formatted_phone}. SID: {message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send cancellation SMS: {e}")
            return False