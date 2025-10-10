# cf4/my_agent.py
import logging
from dotenv import load_dotenv
from datetime import date

from livekit.agents import (
    Agent, AgentSession, JobContext, JobProcess, WorkerOptions, cli, function_tool
)
from livekit.agents.llm import ChatMessage, ChatRole
from livekit.plugins import deepgram, silero, groq, cartesia
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from database.database import (
    get_db, get_available_rooms, create_booking, get_room_by_number,
    create_call_session, log_conversation_turn, get_conversation_history, find_customer_by_phone
)
from database.models import Booking
# --- END IMPORTS ---

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("my-agent")

class MyAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are a helpful FEMALE AI assistant for a hotel in Jaipur, India. "
                "You must understand and respond in Hinglish, a mix of Hindi and English. "
                "Your primary role is to assist users with booking hotel rooms. "
                "If a user mentions a previous call or a query number, use the 'retrieve_past_conversation' tool "
                "to understand their history before proceeding."
            )
        )
        self.db = next(get_db())
        # Create a new call session for this agent instance
        self.call_session = create_call_session(self.db)
        logger.info(f"New call session created with ID: {self.call_session.id}")

    # --- NEW MEMORY TOOL ---
    @function_tool
    async def retrieve_past_conversation(self, query_id: int) -> str:
        """
        Called when the user refers to a past conversation using a 'query number' or 'session ID'.
        This tool loads the history of that conversation for context.
        """
        logger.info(f"Retrieving past conversation for query ID: {query_id}")
        history = get_conversation_history(self.db, query_id)
        if not history:
            return f"I'm sorry, I couldn't find any record for query number {query_id}. We can start a new one, though."

        # Load history into the LLM's context
        past_messages = []
        customer_name = "there"
        for turn in history:
            role = ChatRole.USER if turn.speaker == 'user' else ChatRole.ASSISTANT
            past_messages.append(ChatMessage(role=role, content=turn.text))
        
        # This is the key part: we are injecting the past conversation into the AI's memory
        self.llm.chat_context.messages = past_messages + self.llm.chat_context.messages
        
        # Try to find customer details from the booking linked to that session
        booking = self.db.query(Booking).filter(Booking.call_session_id == query_id).first()
        if booking and booking.customer:
            customer_name = booking.customer.name.split(" ")[0]

        return f"Welcome back, {customer_name}! I have your previous chat with ID {query_id}. We were discussing a booking. How can I help you continue?"

    # --- Existing tools remain the same ---
    @function_tool
    async def check_availability(self, check_in_date: str, check_out_date: str, num_guests: int) -> str:
        # ... (this function's code does not change)
        logger.info(f"Checking availability for {num_guests} guests from {check_in_date} to {check_out_date}")
        try:
            check_in = date.fromisoformat(check_in_date)
            check_out = date.fromisoformat(check_out_date)
            rooms = get_available_rooms(self.db, check_in, check_out, num_guests)
            if not rooms:
                return "Ma'am/Sir, unfortunately, we have no rooms available for those dates. Would you like to try different dates?"

            response = f"Yes, we have a few options for you. Your query ID for this call is {self.call_session.id}. You can use this number if you call back.\n"
            for room in rooms:
                response += f"- Room number {room.room_number}, which is a '{room.room_type}' room for up to {room.capacity} people, costs ₹{int(room.price_per_night)} per night.\n"
            response += "\nWould you like to book one of these rooms?"
            return response
        except Exception as e:
            logger.error(f"Error checking availability: {e}")
            return "I'm sorry, I encountered an error. Could you please state the dates again clearly?"


    @function_tool
    async def book_room(self, customer_name: str, phone_number: str, room_number: str, check_in_date: str, check_out_date: str, num_guests: int) -> str:
        # ... (this function is slightly modified to link the booking to the call session)
        logger.info(f"Attempting to book room {room_number} for {customer_name}")
        try:
            check_in = date.fromisoformat(check_in_date)
            check_out = date.fromisoformat(check_out_date)
            
            room_to_book = get_room_by_number(self.db, room_number)
            if not room_to_book:
                return f"I'm sorry, I couldn't find a room with the number '{room_number}'. Please check the room number."

            booking = create_booking(self.db, customer_name, phone_number, room_to_book.id, check_in, check_out, num_guests)
            
            # Link the booking to this call session
            booking.call_session_id = self.call_session.id
            self.db.commit()

            return f"Excellent! Your booking is confirmed, {customer_name}. Your booking ID is {booking.id}. We're excited to welcome you on {check_in_date}."
        except Exception as e:
            logger.error(f"Error creating booking: {e}")
            return "I'm sorry, there was a technical issue while creating your booking. Please try again."

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

async def entrypoint(ctx: JobContext):
    agent = MyAgent() # Create the agent instance first
    
    session = AgentSession(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STTT(model="nova-2", language="multi"),
        llm=groq.LLM(model="llama3-8b-8192"),
        tts=cartesia.TTS(voice="faf0731e-dfb9-4cfc-8119-259a79b27e12"),
        turn_detection=MultilingualModel(),
    )

    # --- ADD EVENT LISTENERS FOR LOGGING ---
    @session.on("user_speech")
    async def on_user_speech(transcription: str):
        if transcription:
            log_conversation_turn(agent.db, agent.call_session.id, "user", transcription)

    @session.on("agent_speech")
    async def on_agent_speech(transcription: str):
        if transcription:
            log_conversation_turn(agent.db, agent.call_session.id, "agent", transcription)
    # --- END LISTENERS ---

    await session.start(agent=agent, room=ctx.room)

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
            initialize_process_timeout=60.0,
        )
    )