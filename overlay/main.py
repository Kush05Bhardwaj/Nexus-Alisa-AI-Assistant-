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
        avatar_window.root.after(0, avatar_window.start_talking)
    
    def safe_stop_talking(self):
        """Thread-safe way to stop talking animation"""
        avatar_window.root.after(0, avatar_window.stop_talking)
    
    def safe_on_emotion(self, emotion: str):
        """Thread-safe way to handle emotion"""
        avatar_window.root.after(0, lambda: avatar_controller.on_emotion(emotion))
    
    async def listen_to_backend(self):
        """WebSocket listener running in background thread"""
        try:
            async with websockets.connect(WS_URL) as ws:
                print(f"✅ Connected to backend at {WS_URL}")
                while True:
                    msg = await ws.recv()
                    
                    if msg == "[END]":
                        self.safe_stop_talking()
                    
                    elif msg == "[SPEECH_START]":
                        # Text chat is starting to speak
                        self.safe_start_talking()
                    
                    elif msg == "[SPEECH_END]":
                        # Text chat finished speaking
                        self.safe_stop_talking()
                    
                    elif msg.startswith("[EMOTION]"):
                        emotion = msg.replace("[EMOTION]", "").strip()
                        self.safe_on_emotion(emotion)
                    
                    else:
                        # Streaming token received - start talking
                        self.safe_start_talking()
                        
        except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK) as e:
            print(f"❌ Connection closed: {e}")
        except OSError as e:
            print(f"❌ Could not connect to backend. Make sure it's running on port 8000. Error: {e}")
        except Exception as e:
            print(f"❌ WebSocket error: {e}")
    
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
