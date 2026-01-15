"""
Enhanced Vision Client with Screen Context Awareness
Monitors webcam (face/attention) + screen content
Sends periodic screen updates to backend for context-aware assistance
"""
import asyncio
import cv2
import websockets
import time
from face_emotion import detect_face_and_emotion
from screen_capture import capture_screen
from screen_analyze import analyze_screen

# WebSocket connection URL
WS_URL = "ws://127.0.0.1:8000/ws/chat"

# Throttle timing (in seconds)
SCREEN_CAPTURE_INTERVAL = 5  # Capture screen every 5-10 seconds
MIN_SCREEN_CAPTURE_INTERVAL = 5
MAX_SCREEN_CAPTURE_INTERVAL = 10

async def vision_with_screen_loop():
    """Main vision loop with screen capture support."""
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Could not open webcam")
        return
    
    # State tracking
    last_presence = "unknown"
    last_attention = "unknown"
    last_emotion = "neutral"
    last_screen_capture = 0
    
    print("✅ Vision system with screen capture started")
    print(f"📸 Screen will be analyzed every {MIN_SCREEN_CAPTURE_INTERVAL}-{MAX_SCREEN_CAPTURE_INTERVAL} seconds")
    
    # Auto-reconnect loop
    while True:
        try:
            async with websockets.connect(WS_URL) as ws:
                print(f"✅ Connected to backend at {WS_URL}")
                
                while True:
                    # Capture webcam frame
                    ret, frame = cap.read()
                    
                    if not ret:
                        print("⚠️ Failed to capture webcam frame")
                        await asyncio.sleep(1)
                        continue
                    
                    # Detect face, emotion, and attention
                    face_present, emotion, attention_state = detect_face_and_emotion(frame)
                    
                    # Determine presence state
                    presence = "present" if face_present else "absent"
                    
                    # Send face/attention updates when state changes
                    if presence != last_presence:
                        message = f"[VISION_FACE]{presence}"
                        await ws.send(message)
                        if presence == "present":
                            print("✅ User detected")
                        else:
                            print("❌ User left")
                        last_presence = presence
                    
                    if attention_state != last_attention and presence == "present":
                        message = f"[VISION_FACE]{attention_state}"
                        await ws.send(message)
                        if attention_state == "focused":
                            print("👀 User looking at screen")
                        else:
                            print("😴 User looking away")
                        last_attention = attention_state
                    
                    # Periodic screen capture (throttled)
                    current_time = time.time()
                    time_since_last_capture = current_time - last_screen_capture
                    
                    if time_since_last_capture >= MIN_SCREEN_CAPTURE_INTERVAL:
                        # Capture and analyze screen
                        screen = capture_screen()
                        
                        if screen is not None:
                            info = analyze_screen(screen)
                            
                            # Send screen context to backend
                            window_title = info.get("window", "")
                            screen_text = info.get("text", "").strip()
                            
                            # Only send if there's meaningful content
                            if window_title or screen_text:
                                message = f"[VISION_SCREEN]{window_title} | {screen_text}"
                                await ws.send(message)
                                print(f"📸 Screen context: {window_title[:50]}...")
                                last_screen_capture = current_time
                    
                    # Small delay to reduce CPU usage
                    await asyncio.sleep(0.1)
                    
        except websockets.exceptions.ConnectionClosedError:
            print("⚠️ Connection lost: Backend disconnected")
            print("🔄 Reconnecting in 2 seconds...")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ Error: {e}")
            print("🔄 Reconnecting in 2 seconds...")
            await asyncio.sleep(2)
    
    # Cleanup
    cap.release()

if __name__ == "__main__":
    print("=" * 60)
    print("👁️ Enhanced Vision System - Face + Screen Context")
    print("=" * 60)
    print("Monitoring:")
    print("  - User presence (face detection)")
    print("  - Attention state (focused/away)")
    print("  - Screen content (window + text)")
    print("=" * 60)
    print()
    
    try:
        asyncio.run(vision_with_screen_loop())
    except KeyboardInterrupt:
        print("\n👋 Vision system stopped")
