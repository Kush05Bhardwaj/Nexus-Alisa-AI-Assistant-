"""
Alisa Assistant - Overlay Entry Point
Integrates avatar UI with WebSocket client using thread-safe communication
Also allows voice modules to directly control the avatar
"""
import threading
import asyncio
import avatar_window
import avatar_controller
import websockets

WS_URL = "ws://127.0.0.1:8000/ws/chat"

class AvatarApp:
    def __init__(self):
        self.ws_task = None
        self.loop = None
    
    def safe_start_talking(self):
        """Thread-safe way to start talking animation"""
        print("📞 safe_start_talking() called from WebSocket thread")
        avatar_window.root.after(0, avatar_window.start_talking)
    
    def safe_stop_talking(self):
        """Thread-safe way to stop talking animation"""
        print("📞 safe_stop_talking() called from WebSocket thread")
        avatar_window.root.after(0, avatar_window.stop_talking)
    
    def safe_on_emotion(self, emotion: str):
        """Thread-safe way to handle emotion"""
        avatar_window.root.after(0, lambda: avatar_controller.on_emotion(emotion))
    
    async def listen_to_backend(self):
        """WebSocket listener running in background thread with auto-reconnect"""
        reconnect_delay = 2  # seconds
        
        while True:
            try:
                async with websockets.connect(WS_URL) as ws:
                    print(f"✅ Connected to backend at {WS_URL}")
                    while True:
                        msg = await ws.recv()
                        
                        # Only log important control messages
                        if msg in ["[SPEECH_START]", "[SPEECH_END]", "[END]"] or msg.startswith("[EMOTION]"):
                            print(f"🔵 [WS RECEIVED] {msg}")
                        
                        # Handle speech control signals from text_chat
                        if msg == "[SPEECH_START]":
                            # Text chat is starting to speak - start mouth animation
                            print("🎤 [OVERLAY] Speech started - animating mouth")
                            self.safe_start_talking()
                        
                        elif msg == "[SPEECH_END]":
                            # Text chat finished speaking - stop mouth animation
                            print("🤐 [OVERLAY] Speech ended - stopping mouth")
                            self.safe_stop_talking()
                        
                        # Handle emotion changes
                        elif msg.startswith("[EMOTION]"):
                            emotion = msg.replace("[EMOTION]", "").strip()
                            print(f"😊 [OVERLAY] Emotion: {emotion}")
                            self.safe_on_emotion(emotion)
                        
                        # Ignore other messages (LLM tokens, [END], etc.)
                        # We only care about speech control, not text generation
                        elif msg == "[END]":
                            # End of LLM generation - do nothing (speech might not have started yet)
                            print("🏁 [OVERLAY] Received [END] - ignoring")
                        elif msg == "":
                            # Keepalive ping - ignore
                            pass
                        else:
                            # LLM streaming token - ignore (don't animate during text generation)
                            pass
                            
            except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK) as e:
                print(f"❌ Connection closed: {e}")
                print(f"🔄 Reconnecting in {reconnect_delay} seconds...")
                await asyncio.sleep(reconnect_delay)
            except OSError as e:
                print(f"❌ Could not connect to backend. Make sure it's running on port 8000. Error: {e}")
                print(f"🔄 Retrying in {reconnect_delay} seconds...")
                await asyncio.sleep(reconnect_delay)
            except Exception as e:
                print(f"❌ WebSocket error: {e}")
                print(f"🔄 Reconnecting in {reconnect_delay} seconds...")
                await asyncio.sleep(reconnect_delay)
    
    def start_websocket_thread(self):
        """Start WebSocket client in background thread"""
        def run_async_loop():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self.listen_to_backend())
        
        ws_thread = threading.Thread(target=run_async_loop, daemon=True)
        ws_thread.start()
        print("🚀 WebSocket listener started in background thread")
    
    def run(self):
        """Start the avatar application"""
        print("=" * 50)
        print("🤖 Alisa Assistant - Avatar Overlay")
        print("=" * 50)
        
        # Start WebSocket listener in background
        self.start_websocket_thread()
        
        # Run Tkinter UI in main thread
        print("🎨 Starting avatar UI...")
        print("💡 TIP: Voice output will now trigger avatar animations!")
        print("💡 TIP: Emotions will change avatar expressions!")
        print("💡 Right-click on avatar to close")
        avatar_window.run()

if __name__ == "__main__":
    app = AvatarApp()
    app.run()
