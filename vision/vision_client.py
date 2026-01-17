import asyncio
import websockets
from webcam import get_frame
from face_emotion import detect_face_and_emotion, get_detection_mode
from vision_config import DETECTION_INTERVAL, FRAME_SKIP, CURRENT_PRESET
import time
from collections import deque

WS_URL = "ws://127.0.0.1:8000/ws/chat"

# Performance monitoring
class PerformanceMonitor:
    def __init__(self, window_size=100):
        self.processing_times = deque(maxlen=window_size)
        self.frame_times = deque(maxlen=window_size)
        self.last_frame_time = time.time()
    
    def record_frame(self):
        current = time.time()
        if self.last_frame_time:
            self.frame_times.append(current - self.last_frame_time)
        self.last_frame_time = current
    
    def record_processing(self, duration):
        self.processing_times.append(duration)
    
    def get_stats(self):
        if not self.processing_times or not self.frame_times:
            return None
        return {
            'avg_processing_ms': sum(self.processing_times) / len(self.processing_times) * 1000,
            'avg_fps': 1.0 / (sum(self.frame_times) / len(self.frame_times)) if self.frame_times else 0,
            'cpu_usage_pct': (sum(self.processing_times) / sum(self.frame_times)) * 100 if self.frame_times else 0
        }

async def vision_loop():
    """
    Optimized vision system with minimal resource usage
    - Uses lightweight Haar Cascade by default
    - Processes downscaled frames
    - Caches detection results
    - Only sends updates on state changes
    - Performance monitoring and adaptive frame rates
    """
    print("=" * 60)
    print("👁️ Alisa Vision System - Starting (Optimized Mode)")
    print("=" * 60)
    print(f"Detection Method: {get_detection_mode()}")
    print(f"Current Preset: {CURRENT_PRESET}")
    print("Optimizations:")
    print(f"  ✓ Downscaled frames for processing")
    print(f"  ✓ Detection caching enabled")
    print(f"  ✓ Frame skipping ({FRAME_SKIP}x)")
    print(f"  ✓ Detection interval: {DETECTION_INTERVAL}s")
    print(f"  ✓ Adaptive performance monitoring")
    print(f"  ✓ Efficient state change detection")
    print()
    print("Monitoring:")
    print("  - User presence (face detection)")
    print("  - Attention state (focused/away)")
    print("=" * 60)
    print()
    
    frame_counter = 0
    perf_monitor = PerformanceMonitor()
    stats_counter = 0
    
    while True:  # Infinite reconnection loop
        try:
            async with websockets.connect(WS_URL) as ws:
                print(f"✅ Connected to backend at {WS_URL}")
                
                last_presence = None
                last_attention = None
                last_emotion = None
                away_time = 0
                focused_time = 0
                
                # Adaptive sleep time based on system performance
                adaptive_sleep = 0.1
                
                while True:
                    loop_start = time.time()
                    perf_monitor.record_frame()
                    
                    # Get downscaled frame for faster processing
                    frame = get_frame(downscale=True)
                    if frame is None:
                        await asyncio.sleep(0.5)
                        continue

                    # Skip frames to reduce CPU usage
                    frame_counter += 1
                    if frame_counter % FRAME_SKIP != 0:
                        await asyncio.sleep(adaptive_sleep)
                        continue

                    # Detect with caching enabled
                    detection_start = time.time()
                    face, emotion, attention = detect_face_and_emotion(frame, use_cache=True)
                    detection_time = time.time() - detection_start
                    perf_monitor.record_processing(detection_time)

                    # Track state changes
                    current_time = time.time()
                    
                    # Batch state change messages for efficiency
                    messages_to_send = []
                    
                    # User appeared/disappeared
                    if face != last_presence:
                        if face == "face":
                            print("✅ User detected")
                            messages_to_send.append("[VISION_FACE]present")
                        else:
                            print("❌ User left")
                            messages_to_send.append("[VISION_FACE]absent")
                            away_time = current_time
                        
                        last_presence = face
                    
                    # Attention state changed
                    if attention != last_attention and face == "face":
                        if attention == "focused":
                            print("👀 User looking at screen")
                            messages_to_send.append("[VISION_FACE]focused")
                            focused_time = current_time
                        else:
                            print("😴 User looking away")
                            messages_to_send.append("[VISION_FACE]distracted")
                            away_time = current_time
                        
                        last_attention = attention
                    
                    # Emotion changed (if implemented)
                    if emotion != last_emotion and face == "face" and emotion != "neutral":
                        print(f"😊 Emotion detected: {emotion}")
                        messages_to_send.append(f"[VISION_FACE]{emotion}")
                        last_emotion = emotion
                    
                    # Send all messages efficiently
                    for msg in messages_to_send:
                        await ws.send(msg)
                    
                    # Adaptive performance tuning
                    stats_counter += 1
                    if stats_counter >= 100:
                        stats = perf_monitor.get_stats()
                        if stats:
                            print(f"📊 Perf: {stats['avg_processing_ms']:.1f}ms processing, "
                                  f"{stats['avg_fps']:.1f} FPS, "
                                  f"{stats['cpu_usage_pct']:.1f}% CPU")
                            
                            # Adjust adaptive sleep based on CPU usage
                            if stats['cpu_usage_pct'] > 30:
                                adaptive_sleep = min(0.2, adaptive_sleep + 0.02)
                                print(f"⚡ High CPU, increasing sleep to {adaptive_sleep:.2f}s")
                            elif stats['cpu_usage_pct'] < 10 and adaptive_sleep > 0.05:
                                adaptive_sleep = max(0.05, adaptive_sleep - 0.01)
                        
                        stats_counter = 0
                    
                    # Sleep between detections with adaptive timing
                    elapsed = time.time() - loop_start
                    sleep_time = max(DETECTION_INTERVAL - elapsed, adaptive_sleep)
                    await asyncio.sleep(sleep_time)
                    
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
        # Cleanup
        from webcam import release_camera
        release_camera()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
