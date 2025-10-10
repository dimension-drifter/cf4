import logging
from dotenv import load_dotenv
from datetime import datetime

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
        if user_info and user_info.get('name'):
            history_context = f"\n\nYou are speaking with {user_info['name']}."
        
        if conversation_history:
            history_context += "\n\nRecent conversation history:"
            for msg in conversation_history:
                history_context += f"\n- {msg['speaker']}: {msg['message']}"
        
        super().__init__(
            instructions=f"""You are "Kriti," the lead AI-powered voice concierge and customer support agent for the prestigious "Pink Perl" hotel located in Jaipur, Rajasthan, India.

Your persona is that of a highly professional, warm, and exceptionally helpful human concierge. You are articulate, patient, and proactive. Your primary goal is to provide a seamless and delightful booking experience for every guest, making them feel valued and understood. You are not just a command-taker; you are an agentic assistant who guides the conversation to gather all necessary details efficiently.

{history_context}

Core Directives & Rules:

1. Introduction: Always begin the conversation by introducing yourself. For example: "Welcome to the Pink Perl hotel, you're speaking with Kriti. How may I assist you today?"

2. Hotel Name: Always refer to the hotel as "Pink Perl."

3. Task Identification: Your first step is to understand the customer's primary need. Is it a room booking, a restaurant reservation, or another inquiry?

4. Agentic Behavior: Be proactive. If a customer says, "I'd like to book a room," don't wait for them to provide all the details. Guide them by asking clarifying questions in a logical sequence.

5. Use the tools available to you:
   - save_user_info: Save customer name, phone, email
   - create_room_booking: Book hotel rooms
   - create_restaurant_booking: Book restaurant tables
   - get_my_bookings: Retrieve customer's booking history

6. Confirmation is Key: Before finalizing any booking using the tools, you MUST summarize all the details back to the customer and ask for their confirmation.

7. Handle Ambiguity: If a customer's request is unclear, ask for clarification politely.

8. Contextual Awareness: The current date is October 10, 2025. Use this for date-related calculations and suggestions. The location is Jaipur, India.

Room Types Available:
- Standard: Comfortable rooms, ₹3,500/night
- Deluxe: Spacious rooms with city view, ₹5,500/night
- Presidential Suite: Luxurious suites, ₹12,000/night

Hotel Restaurants:
- Surahi: Fine dining, authentic Rajasthani and North Indian cuisine
- Oasis: All-day, multi-cuisine dining (Continental, Italian, Asian)
- The Rooftop Lounge: Casual dining with cocktails and panoramic city views"""
        )

    @function_tool
    async def save_user_info(self, name: str = None, phone: str = None, email: str = None) -> str:
        """Save customer information like name, phone number, or email."""
        try:
            db.create_or_update_user(self.user_id, name=name, phone=phone, email=email)
            logger.info(f"Saved user info for {self.user_id}")
            return f"Thank you! I've saved your information."
        except Exception as e:
            logger.error(f"Error saving user info: {e}")
            return "I apologize, but I encountered an error saving your information."

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
        Create a hotel room booking.
        
        Args:
            room_type: Type of room (Standard, Deluxe, or Presidential Suite)
            check_in_date: Check-in date in YYYY-MM-DD format
            check_out_date: Check-out date in YYYY-MM-DD format
            num_adults: Number of adults
            num_children: Number of children (default 0)
            special_requests: Any special requests
        """
        try:
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
            
            return f"Wonderful! Your {room_type} room has been confirmed. Your booking ID is {booking_id}. Check-in is on {check_in_date} and check-out is on {check_out_date}. You will receive a confirmation email shortly."
            
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
        Create a restaurant table booking.
        
        Args:
            restaurant_name: Name of restaurant (Surahi, Oasis, or The Rooftop Lounge)
            booking_date: Date in YYYY-MM-DD format
            booking_time: Time in HH:MM format (24-hour)
            num_guests: Number of guests
            special_requests: Special requests or dietary restrictions
        """
        try:
            booking_id = db.create_restaurant_booking(
                user_id=self.user_id,
                restaurant_name=restaurant_name,
                booking_date=booking_date,
                booking_time=booking_time,
                num_guests=num_guests,
                special_requests=special_requests
            )
            
            logger.info(f"Created restaurant booking {booking_id} for user {self.user_id}")
            
            return f"Perfect! Your table for {num_guests} at {restaurant_name} is confirmed for {booking_date} at {booking_time}. Your booking ID is {booking_id}. We look forward to serving you!"
            
        except Exception as e:
            logger.error(f"Error creating restaurant booking: {e}")
            return "I apologize, but I encountered an error while making your restaurant reservation. Please try again."

    @function_tool
    async def get_my_bookings(self) -> str:
        """Get all bookings for the current user."""
        try:
            room_bookings = db.get_user_room_bookings(self.user_id)
            restaurant_bookings = db.get_user_restaurant_bookings(self.user_id)
            
            result = "Here are your bookings:\n\n"
            
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
                result = "You don't have any bookings with us yet. Would you like to make a reservation?"
            
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
        greeting = "Welcome to the Pink Perl hotel, you're speaking with Kriti. How may I assist you today?"
    
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