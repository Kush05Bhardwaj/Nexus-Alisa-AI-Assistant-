"""
Phase 10A: Enhanced Vision Client with Desktop Understanding
Monitors webcam (face/attention) + understands screen context
Offers contextual help based on what user is doing
OPTIMIZED: Reduced memory usage, adaptive screen capture, better error handling
"""
import asyncio
import cv2
import websockets
import time
from collections import deque
from face_emotion import detect_face_and_emotion
from screen_capture import capture_screen
from screen_analyze import analyze_screen
from desktop_understanding import desktop_understanding

# WebSocket connection URL
WS_URL = "ws://127.0.0.1:8000/ws/chat"

# Throttle timing (in seconds)
SCREEN_CAPTURE_INTERVAL = 10  # Analyze screen every 10 seconds (not too often)
MIN_SCREEN_CAPTURE_INTERVAL = 10

# Adaptive screen capture based on user activity
SCREEN_CAPTURE_FOCUSED_INTERVAL = 8  # Faster when user is focused
SCREEN_CAPTURE_AWAY_INTERVAL = 20  # Slower when user is away

class PerformanceMonitor:
    """Monitor and track system performance"""
    def __init__(self, window_size=50):
        self.processing_times = deque(maxlen=window_size)
        self.frame_count = 0
        self.last_stats_time = time.time()
    
    def record(self, duration):
        self.processing_times.append(duration)
        self.frame_count += 1
    
    def should_print_stats(self, interval=30):
        return (time.time() - self.last_stats_time) >= interval
    
    def get_stats(self):
        if not self.processing_times:
            return None
        avg_ms = (sum(self.processing_times) / len(self.processing_times)) * 1000
        return {
            'avg_processing_ms': avg_ms,
            'frame_count': self.frame_count
        }
    
    def reset_stats_timer(self):
        self.last_stats_time = time.time()

async def vision_with_screen_loop():
    """Main vision loop with Phase 10A desktop understanding - OPTIMIZED."""
    
    # Initialize webcam with reduced resolution for better performance
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 15)
    
    if not cap.isOpened():
        print("❌ Could not open webcam")
        return
    
    # State tracking
    last_presence = "unknown"
    last_attention = "unknown"
    last_emotion = "neutral"
    last_screen_capture = 0
    last_window_title = ""
    
    # Performance monitoring
    perf_monitor = PerformanceMonitor()
    
    print("✅ Phase 10A - Desktop Understanding System started (OPTIMIZED)")
    print(f"📸 Screen analysis: Adaptive timing based on user activity")
    print(f"  • Focused: every {SCREEN_CAPTURE_FOCUSED_INTERVAL}s")
    print(f"  • Away: every {SCREEN_CAPTURE_AWAY_INTERVAL}s")
    print("🧠 Alisa will understand what you're doing and offer help when appropriate")
    print("⚡ Performance monitoring enabled")
    
    # Auto-reconnect loop
    while True:
        try:
            async with websockets.connect(WS_URL) as ws:
                print(f"✅ Connected to backend at {WS_URL}")
                
                while True:
                    loop_start = time.time()
                    
                    # Capture webcam frame
                    ret, frame = cap.read()
                    
                    if not ret:
                        print("⚠️ Failed to capture webcam frame")
                        await asyncio.sleep(1)
                        continue
                    
                    # Downscale frame for faster face detection
                    small_frame = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_LINEAR)
                    
                    # Detect face, emotion, and attention
                    face_present, emotion, attention_state = detect_face_and_emotion(small_frame)
                    
                    # Determine presence state
                    presence = "present" if face_present else "absent"
                    
                    # Batch messages for efficiency
                    messages_to_send = []
                    
                    # Send face/attention updates when state changes
                    if presence != last_presence:
                        messages_to_send.append(f"[VISION_FACE]{presence}")
                        if presence == "present":
                            print("✅ User detected")
                        else:
                            print("❌ User left")
                        last_presence = presence
                    
                    if attention_state != last_attention and presence == "present":
                        messages_to_send.append(f"[VISION_FACE]{attention_state}")
                        if attention_state == "focused":
                            print("👀 User looking at screen")
                        else:
                            print("😴 User looking away")
                        last_attention = attention_state
                    
                    # Adaptive screen capture interval based on user state
                    current_time = time.time()
                    time_since_last_capture = current_time - last_screen_capture
                    
                    # Determine adaptive interval
                    if attention_state == "focused" and presence == "present":
                        capture_interval = SCREEN_CAPTURE_FOCUSED_INTERVAL
                    else:
                        capture_interval = SCREEN_CAPTURE_AWAY_INTERVAL
                    
                    # Periodic screen capture (adaptive throttling)
                    if time_since_last_capture >= capture_interval:
                        try:
                            # Capture and analyze screen
                            screen = capture_screen()
                            
                            if screen is not None:
                                info = analyze_screen(screen)
                                
                                window_title = info.get("window", "")
                                screen_text = info.get("text", "").strip()
                                
                                # Only process if window changed or significant content
                                should_process = (
                                    window_title != last_window_title or
                                    (len(screen_text) > 20 and attention_state == "focused")
                                )
                                
                                if should_process:
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
                                        messages_to_send.append(desktop_msg)
                                        
                                        last_window_title = window_title
                                
                                last_screen_capture = current_time
                        
                        except Exception as e:
                            print(f"⚠️ Screen capture error: {e}")
                            # Continue without crashing
                    
                    # Send all batched messages efficiently
                    for msg in messages_to_send:
                        await ws.send(msg)
                    
                    # Performance monitoring
                    processing_time = time.time() - loop_start
                    perf_monitor.record(processing_time)
                    
                    if perf_monitor.should_print_stats():
                        stats = perf_monitor.get_stats()
                        if stats:
                            print(f"📊 Perf: {stats['avg_processing_ms']:.1f}ms avg, "
                                  f"{stats['frame_count']} frames processed")
                        perf_monitor.reset_stats_timer()
                    
                    # Small delay to reduce CPU usage (adaptive)
                    sleep_time = max(0.05, 0.1 - processing_time)
                    await asyncio.sleep(sleep_time)
                    
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
