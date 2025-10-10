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
        except (ProcessLookupError, subprocess.TimeoutExpired):
            try:
                proc.kill()
            except ProcessLookupError:
                pass  # Process already died
    sys.exit(0)


def check_env():
    """Checks for required environment variables."""
    required = ['LIVEKIT_URL', 'LIVEKIT_API_KEY', 'LIVEKIT_API_SECRET',
                'DEEPGRAM_API_KEY', 'GROQ_API_KEY', 'CARTESIA_API_KEY']
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        print("❌ Missing environment variables:", ", ".join(missing))
        print("Please ensure your .env file is correctly set up.")
        sys.exit(1)
    print("✅ Environment variables loaded successfully.")


def main():
    print("=" * 70)
    print("🎙️  AI VOICE ASSISTANT - HINGLISH SUPPORT")
    print("=" * 70)

    check_env()

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    try:
        # --- CORRECTED AGENT WORKER COMMAND ---
        print("\n🤖 Starting Agent Worker...")
        # We must provide the 'start' command to the agent script.
        agent_command = [
            sys.executable,
            "my_agent.py",
            "start"  # This tells the agent to run in production worker mode
        ]
        agent_proc = subprocess.Popen(agent_command,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      text=True,
                                      creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0)
        processes.append(agent_proc)
        print("✅ Agent Worker process started.")

        time.sleep(8)  # Give it a bit more time to initialize models

        # --- WEB SERVER COMMAND (UNCHANGED) ---
        print("🌐 Starting Web Server...")
        # If your file is 'web_server.py', change 'server:app' to 'web_server:app'
        server_command = [
            sys.executable,
            "-m",
            "hypercorn",
            "server:app",
            "--bind",
            "0.0.0.0:5000"
        ]
        web_proc = subprocess.Popen(server_command,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
        processes.append(web_proc)
        print("✅ Web Server process started.")

        print("\n" + "=" * 70)
        print("✅ VOICE ASSISTANT IS RUNNING!")
        print("=" * 70)
        print("📍 Open your browser: http://localhost:5000")
        print("🛑 Press Ctrl+C here to stop all services")
        print("=" * 70 + "\n")

        # Monitor the processes
        while True:
            if agent_proc.poll() is not None:
                print("❌ Agent worker stopped unexpectedly!")
                print("--- Agent Error Output ---")
                print(agent_proc.stderr.read())
                print("--------------------------")
                cleanup()
            if web_proc.poll() is not None:
                print("❌ Web server stopped unexpectedly!")
                print("--- Web Server Error Output ---")
                print(web_proc.stderr.read())
                print("-----------------------------")
                cleanup()
            time.sleep(1)

    except KeyboardInterrupt:
        cleanup()
    except Exception as e:
        print(f"\n❌ An error occurred during startup: {e}")
        cleanup()


if __name__ == '__main__':
    if not os.path.exists('server.py') and not os.path.exists('web_server.py'):
        print("❌ Error: Could not find 'server.py' or 'web_server.py'. Please make sure it exists.")
        sys.exit(1)

    main()