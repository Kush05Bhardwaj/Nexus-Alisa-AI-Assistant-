"""
Phase 10A: Enhanced Vision Client with Desktop Understanding
Monitors webcam (face/attention) + understands screen context
Offers contextual help based on what user is doing
"""
import asyncio
import cv2
import websockets
import time
from face_emotion import detect_face_and_emotion
from screen_capture import capture_screen
from screen_analyze import analyze_screen
from desktop_understanding import desktop_understanding

# WebSocket connection URL
WS_URL = "ws://127.0.0.1:8000/ws/chat"

# Throttle timing (in seconds)
SCREEN_CAPTURE_INTERVAL = 10  # Analyze screen every 10 seconds (not too often)
MIN_SCREEN_CAPTURE_INTERVAL = 10

async def vision_with_screen_loop():
    """Main vision loop with Phase 10A desktop understanding."""
    
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
    
    print("✅ Phase 10A - Desktop Understanding System started")
    print(f"📸 Screen will be analyzed every {SCREEN_CAPTURE_INTERVAL} seconds")
    print("🧠 Alisa will understand what you're doing and offer help when appropriate")
    
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
                            
                            window_title = info.get("window", "")
                            screen_text = info.get("text", "").strip()
                            
                            # Phase 10A: Desktop Understanding
                            if window_title or screen_text:
                                analysis = desktop_understanding.analyze_screen_context(
                                    window_title=window_title,
                                    screen_text=screen_text
                                )
                                
                                # Log desktop understanding
                                print(f"🖥️  Context: {analysis['context_summary']}")
                                if analysis["has_error"]:
                                    print(f"⚠️  Error detected: {analysis['error_text'][:60]}...")
                                if analysis["should_offer_help"]:
                                    print(f"💡 Alisa can offer: {analysis['offer_message']}")
                                
                                # Send to backend with understanding context
                                # Format: [VISION_DESKTOP]task|app|file_type|has_error|offer|window|text
                                desktop_msg = (
                                    f"[VISION_DESKTOP]"
                                    f"{analysis['task']}|"
                                    f"{analysis['app_type']}|"
                                    f"{analysis['file_type']}|"
                                    f"{analysis['has_error']}|"
                                    f"{analysis['offer_message']}|"
                                    f"{window_title}|"
                                    f"{screen_text[:200]}"
                                )
                                await ws.send(desktop_msg)
                                
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
    print("👁️ Phase 10A - Desktop Understanding System")
    print("=" * 60)
    print("Features:")
    print("  ✅ Face detection & attention tracking")
    print("  ✅ Screen content analysis")
    print("  ✅ Desktop understanding (what you're doing)")
    print("  ✅ Error detection")
    print("  ✅ Contextual help offers")
    print("=" * 60)
    print()
    
    try:
        asyncio.run(vision_with_screen_loop())
    except KeyboardInterrupt:
        print("\n👋 Vision system stopped")
