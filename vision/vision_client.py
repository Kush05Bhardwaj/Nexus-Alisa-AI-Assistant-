import asyncio
import websockets
from webcam import get_frame
from face_emotion import detect_face_and_emotion
import time

WS_URL = "ws://127.0.0.1:8000/ws/chat"

async def vision_loop():
    """
    Vision system that monitors user presence and attention.
    Sends updates to backend only when state changes (not constantly).
    Auto-reconnects if connection is lost.
    """
    print("=" * 60)
    print("👁️ Alisa Vision System - Starting")
    print("=" * 60)
    print("Monitoring:")
    print("  - User presence (face detection)")
    print("  - Emotion estimation")
    print("  - Attention state (focused/away)")
    print("=" * 60)
    print()
    
    while True:  # Infinite reconnection loop
        try:
            async with websockets.connect(WS_URL) as ws:
                print(f"✅ Connected to backend at {WS_URL}")
                
                last_presence = None
                last_attention = None
                last_emotion = None
                away_time = 0
                focused_time = 0
                
                while True:
                    frame = get_frame()
                    if frame is None:
                        await asyncio.sleep(0.5)
                        continue

                    face, emotion, attention = detect_face_and_emotion(frame)

                    # Track state changes
                    current_time = time.time()
                    
                    # User appeared/disappeared
                    if face != last_presence:
                        if face == "face":
                            print("✅ User detected")
                            await ws.send(f"[VISION_FACE]present")
                        else:
                            print("❌ User left")
                            await ws.send(f"[VISION_FACE]absent")
                            away_time = current_time
                        
                        last_presence = face
                    
                    # Attention state changed
                    if attention != last_attention and face == "face":
                        if attention == "focused":
                            print("👀 User looking at screen")
                            await ws.send(f"[VISION_FACE]focused")
                            focused_time = current_time
                        else:
                            print("😴 User looking away")
                            await ws.send(f"[VISION_FACE]distracted")
                            away_time = current_time
                        
                        last_attention = attention
                    
                    # Emotion changed (if you implement emotion detection)
                    if emotion != last_emotion and face == "face":
                        if emotion != "neutral":
                            print(f"😊 Emotion detected: {emotion}")
                            await ws.send(f"[VISION_FACE]{emotion}")
                        
                        last_emotion = emotion
                    
                    await asyncio.sleep(2)  # Check every 2 seconds
                    
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"\n⚠️ Connection lost: {e}")
            print("🔄 Reconnecting in 2 seconds...")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("🔄 Reconnecting in 2 seconds...")
            await asyncio.sleep(2)

if __name__ == "__main__":
    try:
        asyncio.run(vision_loop())
    except KeyboardInterrupt:
        print("\n\n👋 Vision system stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
