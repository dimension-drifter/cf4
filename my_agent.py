import logging
from dotenv import load_dotenv
from datetime import datetime
import re

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    function_tool,
    RunContext,
)
from livekit.plugins import deepgram, silero, google, cartesia
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from database import HotelDatabase

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("my-agent")

# Initialize database
db = HotelDatabase()

class MyAgent(Agent):
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        
        # Get user info and conversation history
        user_info = db.get_user(user_id)
        conversation_history = db.get_conversation_history(user_id, limit=5)
        
        # Build context from history
        history_context = ""
        user_profile_info = ""
        
        if user_info:
            if user_info.get('name'):
                history_context = f"\n\nYou are speaking with {user_info['name']}."
                user_profile_info += f"Guest Name: {user_info['name']}\n"
            if user_info.get('phone'):
                user_profile_info += f"Phone: {user_info['phone']}\n"
            if user_info.get('email'):
                user_profile_info += f"Email: {user_info['email']}\n"
        
        if conversation_history:
            history_context += "\n\nRecent conversation history:"
            for msg in conversation_history:
                history_context += f"\n- {msg['speaker']}: {msg['message']}"
        
        # Check if we have user's basic info
        has_name = user_info and user_info.get('name')
        has_phone = user_info and user_info.get('phone')
        
        info_collection_prompt = ""
        if not has_name or not has_phone:
            info_collection_prompt = """

IMPORTANT - Information Collection Priority:
- If you don't have the guest's NAME, politely ask for it early in the conversation (e.g., "May I have your name, please?")
- If you don't have the guest's PHONE NUMBER, ask for it before confirming any booking (e.g., "Could you please share your contact number?")
- Use the save_user_info tool IMMEDIATELY after receiving name or phone number
- Make this feel natural and conversational, not like a form-filling exercise
- You can ask for both together: "May I have your name and contact number to proceed with the booking?"
"""
        
        super().__init__(
            instructions=f"""You are "Kriti," the lead AI-powered voice concierge and customer support agent for the prestigious "Pink Perl" hotel located in Jaipur, Rajasthan, India.

Your persona is that of a highly professional, warm, and exceptionally helpful human concierge. You are articulate, patient, and proactive. Your primary goal is to provide a seamless and delightful booking experience for every guest, making them feel valued and understood. You are not just a command-taker; you are an agentic assistant who guides the conversation to gather all necessary details efficiently.

{history_context}

{f"GUEST PROFILE IN SYSTEM:{chr(10)}{user_profile_info}" if user_profile_info else "NEW GUEST - Profile not yet created"}

{info_collection_prompt}

Core Directives & Rules:

1. Introduction: Always begin the conversation by introducing yourself. For example: "Welcome to the Pink Perl hotel, you're speaking with Kriti. How may I assist you today?"

2. Hotel Name: Always refer to the hotel as "Pink Perl."

3. Guest Information Collection:
   - ALWAYS collect guest name and phone number before finalizing any booking
   - Ask naturally during the conversation flow
   - Use save_user_info tool immediately after receiving this information
   - Acknowledge when information is saved: "Thank you, [Name]! I've saved your details."

4. Task Identification: Your first step is to understand the customer's primary need. Is it a room booking, a restaurant reservation, or another inquiry?

5. Agentic Behavior: Be proactive. If a customer says, "I'd like to book a room," don't wait for them to provide all the details. Guide them by asking clarifying questions in a logical sequence.

6. Use the tools available to you:
   - save_user_info: Save customer name, phone, email (USE THIS FIRST when you get new information)
   - create_room_booking: Book hotel rooms (only after you have name and phone)
   - create_restaurant_booking: Book restaurant tables (only after you have name and phone)
   - get_my_bookings: Retrieve customer's booking history

7. Confirmation is Key: Before finalizing any booking using the tools, you MUST:
   - Ensure you have guest's name and phone number
   - Summarize all the booking details back to the customer
   - Ask for their confirmation
   - Only then proceed with the booking

8. Handle Ambiguity: If a customer's request is unclear, ask for clarification politely.

9. Contextual Awareness: The current date is October 10, 2025. Use this for date-related calculations and suggestions. The location is Jaipur, India.

Room Types Available:
- Standard: Comfortable rooms, ₹3,500/night
- Deluxe: Spacious rooms with city view, ₹5,500/night
- Presidential Suite: Luxurious suites, ₹12,000/night

Hotel Restaurants:
- Surahi: Fine dining, authentic Rajasthani and North Indian cuisine
- Oasis: All-day, multi-cuisine dining (Continental, Italian, Asian)
- The Rooftop Lounge: Casual dining with cocktails and panoramic city views

Remember: Always maintain a warm, helpful tone. Make guests feel special and valued."""
        )

    @function_tool
    async def save_user_info(self, name: str = None, phone: str = None, email: str = None) -> str:
        """Save customer information like name, phone number, or email. Call this immediately when you receive any of this information."""
        try:
            # Validate and format phone number if provided
            if phone:
                # Remove any spaces, dashes, or special characters
                phone = re.sub(r'[^\d+]', '', phone)
                # Ensure it's a valid format
                if not re.match(r'^\+?\d{10,15}$', phone):
                    return "I couldn't save that phone number. Could you please provide a valid 10-digit mobile number?"
            
            db.create_or_update_user(self.user_id, name=name, phone=phone, email=email)
            logger.info(f"Saved user info for {self.user_id}: name={name}, phone={phone}, email={email}")
            
            # Create a friendly response
            response_parts = []
            if name:
                response_parts.append(f"your name as {name}")
            if phone:
                response_parts.append(f"your contact number")
            if email:
                response_parts.append(f"your email")
            
            if response_parts:
                return f"Perfect! I've saved {' and '.join(response_parts)} in our system."
            else:
                return "Information saved successfully."
                
        except Exception as e:
            logger.error(f"Error saving user info: {e}")
            return "I apologize, but I encountered an error saving your information. Could you please repeat that?"

    @function_tool
    async def create_room_booking(
        self, 
        room_type: str,
        check_in_date: str,
        check_out_date: str,
        num_adults: int,
        num_children: int = 0,
        special_requests: str = ""
    ) -> str:
        """
        Create a hotel room booking. Only use this after you have confirmed the guest's name and phone number.
        
        Args:
            room_type: Type of room (Standard, Deluxe, or Presidential Suite)
            check_in_date: Check-in date in YYYY-MM-DD format
            check_out_date: Check-out date in YYYY-MM-DD format
            num_adults: Number of adults
            num_children: Number of children (default 0)
            special_requests: Any special requests
        """
        try:
            # Verify we have guest information before booking
            user_info = db.get_user(self.user_id)
            if not user_info or not user_info.get('name') or not user_info.get('phone'):
                return "Before I can confirm your booking, I need to collect some information. May I have your name and contact number, please?"
            
            booking_id = db.create_room_booking(
                user_id=self.user_id,
                room_type=room_type,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                num_adults=num_adults,
                num_children=num_children,
                special_requests=special_requests
            )
            
            logger.info(f"Created room booking {booking_id} for user {self.user_id}")
            
            guest_name = user_info.get('name', 'Guest')
            return f"Wonderful, {guest_name}! Your {room_type} room has been confirmed. Your booking ID is {booking_id}. Check-in is on {check_in_date} and check-out is on {check_out_date}. We'll send a confirmation to your registered number. Looking forward to welcoming you!"
            
        except Exception as e:
            logger.error(f"Error creating room booking: {e}")
            return "I apologize, but I encountered an error while processing your booking. Please try again."

    @function_tool
    async def create_restaurant_booking(
        self,
        restaurant_name: str,
        booking_date: str,
        booking_time: str,
        num_guests: int,
        special_requests: str = ""
    ) -> str:
        """
        Create a restaurant table booking. Only use this after you have confirmed the guest's name and phone number.
        
        Args:
            restaurant_name: Name of restaurant (Surahi, Oasis, or The Rooftop Lounge)
            booking_date: Date in YYYY-MM-DD format
            booking_time: Time in HH:MM format (24-hour)
            num_guests: Number of guests
            special_requests: Special requests or dietary restrictions
        """
        try:
            # Verify we have guest information before booking
            user_info = db.get_user(self.user_id)
            if not user_info or not user_info.get('name') or not user_info.get('phone'):
                return "Before I can reserve your table, I need to collect some information. May I have your name and contact number, please?"
            
            booking_id = db.create_restaurant_booking(
                user_id=self.user_id,
                restaurant_name=restaurant_name,
                booking_date=booking_date,
                booking_time=booking_time,
                num_guests=num_guests,
                special_requests=special_requests
            )
            
            logger.info(f"Created restaurant booking {booking_id} for user {self.user_id}")
            
            guest_name = user_info.get('name', 'Guest')
            return f"Perfect, {guest_name}! Your table for {num_guests} at {restaurant_name} is confirmed for {booking_date} at {booking_time}. Your booking ID is {booking_id}. We'll send you a confirmation message. We look forward to serving you!"
            
        except Exception as e:
            logger.error(f"Error creating restaurant booking: {e}")
            return "I apologize, but I encountered an error while making your restaurant reservation. Please try again."

    @function_tool
    async def get_my_bookings(self) -> str:
        """Get all bookings for the current user."""
        try:
            user_info = db.get_user(self.user_id)
            room_bookings = db.get_user_room_bookings(self.user_id)
            restaurant_bookings = db.get_user_restaurant_bookings(self.user_id)
            
            guest_name = user_info.get('name', 'Guest') if user_info else 'Guest'
            result = f"Here are your bookings, {guest_name}:\n\n"
            
            if room_bookings:
                result += "Room Bookings:\n"
                for booking in room_bookings:
                    if booking['status'] == 'confirmed':
                        result += f"- {booking['room_type']} room, {booking['check_in_date']} to {booking['check_out_date']}, Booking ID: {booking['booking_id']}\n"
            
            if restaurant_bookings:
                result += "\nRestaurant Bookings:\n"
                for booking in restaurant_bookings:
                    if booking['status'] == 'confirmed':
                        result += f"- {booking['restaurant_name']}, {booking['booking_date']} at {booking['booking_time']}, {booking['num_guests']} guests, Booking ID: {booking['booking_id']}\n"
            
            if not room_bookings and not restaurant_bookings:
                result = f"{guest_name}, you don't have any bookings with us yet. Would you like to make a reservation?"
            
            return result
            
        except Exception as e:
            logger.error(f"Error fetching bookings: {e}")
            return "I apologize, but I encountered an error retrieving your bookings."

def prewarm(proc: JobProcess):
    """Pre-warm models into memory"""
    proc.userdata["vad"] = silero.VAD.load()

async def entrypoint(ctx: JobContext):
    """Main entrypoint for the agent"""
    
    # Get user ID from room participant
    await ctx.connect()
    user_id = ctx.room.local_participant.identity
    
    logger.info(f"Starting session for user: {user_id}")
    
    # Create or update user record
    db.create_or_update_user(user_id)
    
    session = AgentSession(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=cartesia.TTS(language="hi", voice="faf0731e-dfb9-4cfc-8119-259a79b27e12"),
        turn_detection=MultilingualModel(),
    )

    # Start the agent session
    agent = MyAgent(user_id=user_id)
    
    # Hook to save conversations - MUST be synchronous functions
    @session.on("agent_speech")
    def on_agent_speech(text: str):
        db.add_conversation(user_id, text, "Agent")
    
    @session.on("user_speech")
    def on_user_speech(text: str):
        db.add_conversation(user_id, text, "User")
    
    await session.start(agent=agent, room=ctx.room)
    
    # Get user info for personalized greeting
    user_info = db.get_user(user_id)
    
    if user_info and user_info.get('name'):
        greeting = f"Welcome back to the Pink Perl hotel, {user_info['name']}! This is Kriti. How may I assist you today?"
    else:
        greeting = "Welcome to the Pink Perl hotel! You're speaking with Kriti. How may I assist you today?"
    
    logger.info("🎤 Sending greeting to user...")
    await session.say(greeting, allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
            initialize_process_timeout=60.0,
            load_threshold=0.9
        )
    )