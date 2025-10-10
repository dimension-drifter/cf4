"""
Simple starter that runs agent and web server in separate processes
"""
import subprocess
import sys
import os
import time
import signal
from dotenv import load_dotenv

load_dotenv()

processes = []

def cleanup(signum=None, frame=None):
    """Clean up all processes"""
    print("\n\n👋 Shutting down Voice Assistant...")
    print("=" * 70)
    for proc in processes:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except:
            try:
                proc.kill()
            except:
                pass
    sys.exit(0)

def check_env():
    required = ['LIVEKIT_URL', 'LIVEKIT_API_KEY', 'LIVEKIT_API_SECRET', 
                'DEEPGRAM_API_KEY', 'GROQ_API_KEY', 'CARTESIA_API_KEY']
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        print("❌ Missing environment variables:", missing)
        sys.exit(1)

def main():
    print("=" * 70)
    print("🎙️  AI VOICE ASSISTANT - HINGLISH SUPPORT")
    print("=" * 70)
    
    check_env()
    
    # Register cleanup
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    
    try:
        # Start agent worker
        print("\n🤖 Starting Agent Worker...")
        agent_proc = subprocess.Popen(
            [sys.executable, 'my_agent.py', 'start'],
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
        )
        processes.append(agent_proc)
        
        # Wait for agent to initialize
        print("⏳ Waiting for agent to initialize...")
        time.sleep(10)
        
        # Start web server
        print("🌐 Starting Web Server...")
        web_proc = subprocess.Popen(
            [sys.executable, 'web_server.py']
        )
        processes.append(web_proc)
        
        print("\n" + "=" * 70)
        print("✅ VOICE ASSISTANT IS RUNNING!")
        print("=" * 70)
        print("📍 Open your browser: http://localhost:5000")
        print("🛑 Press Ctrl+C here to stop both services")
        print("=" * 70 + "\n")
        
        # Keep running
        while True:
            time.sleep(1)
            # Check if processes are still running
            if agent_proc.poll() is not None:
                print("❌ Agent worker stopped unexpectedly!")
                cleanup()
            if web_proc.poll() is not None:
                print("❌ Web server stopped unexpectedly!")
                cleanup()
                
    except KeyboardInterrupt:
        cleanup()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        cleanup()

if __name__ == '__main__':
    main()