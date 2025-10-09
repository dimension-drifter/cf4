import logging
from dotenv import load_dotenv

# Import the plugins you installed
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
from livekit.plugins import deepgram, silero, groq, cartesia
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Load environment variables from your .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("my-agent")

# Define your agent's capabilities (tools)
class MyAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are a helpful AI assistant for a business in Jaipur, India. "
                "You must understand and respond in Hinglish, a mix of Hindi and English. "
                "Be polite and conversational. If the user speaks in Hindi, reply in Hindi. "
                "If they speak English, reply in English. If they mix, you mix."
            )
        )

    # Example tool for getting weather - you can add your calendar tools here
    @function_tool
    async def get_weather(self, location: str) -> str:
        """Called when the user asks about the weather."""
        logger.info(f"Looking up weather for {location}")
        return f"The weather in {location} is sunny today."

# This function pre-warms models into memory for faster startup
def prewarm(proc: JobProcess):
    """
    This function is called before the first job is assigned to the process.
    It's a good place to load models into memory.
    """
    proc.userdata["vad"] = silero.VAD.load()

# This is the main entrypoint for your agent
async def entrypoint(ctx: JobContext):
    """
    This is the main entrypoint for your agent.
    It's called when a new job is assigned to this worker.
    """
    session = AgentSession(
        # VAD (Voice Activity Detection) - detects when the user starts and stops speaking
        vad=ctx.proc.userdata["vad"],
        
        # STT (Speech-to-Text) - transcribes user audio
        stt=deepgram.STT(model="nova-3", language="multi"), # 'multi' is great for Hinglish
        
        # LLM (The Brain) - THIS IS THE MAGIC LINE FOR GROQ
        llm=groq.LLM(model="meta-llama/llama-4-scout-17b-16e-instruct"), # Using Llama 4 Scout 17B on Groq
        
        # TTS (Text-to-Speech) - synthesizes the agent's voice
        tts=cartesia.TTS(language="hi"), 
        
        # Turn Detection - intelligently decides when the user's turn is over
        turn_detection=MultilingualModel(),
    )

    # Start the agent session and connect it to the room
    await session.start(agent=MyAgent(), room=ctx.room)

# This is how you run the worker
if __name__ == "__main__":
        cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
            # Give the inference process up to 60 seconds to initialize.
            # This is especially useful on the first run to download models.
            initialize_process_timeout=60.0,
            load_threshold=1.5
        )
    )