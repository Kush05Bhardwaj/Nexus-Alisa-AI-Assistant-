"""
Vision Performance Testing Tool
Test different presets and measure performance
"""
import time
import cv2
import numpy as np
from face_emotion import detect_face_and_emotion
from webcam import get_frame, get_camera_info
from vision_config import apply_preset

def test_preset(preset_name, duration=10, show_video=False):
    """
    Test a specific preset configuration
    
    Args:
        preset_name: Name of preset to test
        duration: Test duration in seconds
        show_video: Whether to display video window
    """
    print("\n" + "=" * 60)
    print(f"Testing Preset: {preset_name.upper()}")
    print("=" * 60)
    
    # Apply preset
    apply_preset(preset_name)
    
    # Camera info
    cam_info = get_camera_info()
    if cam_info:
        print(f"Camera: {cam_info['width']}x{cam_info['height']} @ {cam_info['fps']}fps")
        print(f"Backend: {cam_info['backend']}")
    
    # Performance metrics
    frame_count = 0
    detection_times = []
    total_times = []
    
    start_time = time.time()
    last_print = start_time
    
    print(f"\nRunning test for {duration} seconds...")
    print("Press 'q' to quit early\n")
    
    try:
        while (time.time() - start_time) < duration:
            loop_start = time.time()
            
            # Get frame
            frame = get_frame(downscale=True)
            
            if frame is None:
                print("⚠️ Failed to get frame")
                time.sleep(0.1)
                continue
            
            # Detect face
            detection_start = time.time()
            face, emotion, attention = detect_face_and_emotion(frame, use_cache=True)
            detection_time = time.time() - detection_start
            
            # Record metrics
            frame_count += 1
            detection_times.append(detection_time * 1000)  # Convert to ms
            total_times.append((time.time() - loop_start) * 1000)
            
            # Show video if requested
            if show_video:
                # Scale up for display
                display_frame = cv2.resize(frame, (640, 480))
                
                # Add status text
                status = f"Face: {face} | {emotion} | {attention}"
                cv2.putText(display_frame, status, (10, 30), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                fps = frame_count / (time.time() - start_time)
                cv2.putText(display_frame, f"FPS: {fps:.1f}", (10, 60),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                cv2.imshow(f"Testing: {preset_name}", display_frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            # Print progress every second
            current_time = time.time()
            if current_time - last_print >= 1.0:
                elapsed = current_time - start_time
                fps = frame_count / elapsed
                avg_detection = sum(detection_times[-30:]) / min(len(detection_times), 30)
                print(f"  {elapsed:.1f}s: {fps:.1f} FPS, {avg_detection:.1f}ms detection")
                last_print = current_time
            
            # Small delay
            time.sleep(0.01)
    
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    
    finally:
        if show_video:
            cv2.destroyAllWindows()
    
    # Calculate final statistics
    total_duration = time.time() - start_time
    
    print("\n" + "-" * 60)
    print("RESULTS:")
    print("-" * 60)
    print(f"Duration: {total_duration:.2f} seconds")
    print(f"Frames Processed: {frame_count}")
    print(f"Average FPS: {frame_count / total_duration:.2f}")
    
    if detection_times:
        avg_detection = sum(detection_times) / len(detection_times)
        min_detection = min(detection_times)
        max_detection = max(detection_times)
        print(f"Detection Time (avg): {avg_detection:.2f}ms")
        print(f"Detection Time (min): {min_detection:.2f}ms")
        print(f"Detection Time (max): {max_detection:.2f}ms")
    
    if total_times:
        avg_total = sum(total_times) / len(total_times)
        cpu_usage = (sum(detection_times) / sum(total_times)) * 100 if total_times else 0
        print(f"Total Loop Time (avg): {avg_total:.2f}ms")
        print(f"Estimated CPU Usage: {cpu_usage:.1f}%")
    
    print("=" * 60)
    
    return {
        'preset': preset_name,
        'duration': total_duration,
        'frames': frame_count,
        'fps': frame_count / total_duration,
        'avg_detection_ms': sum(detection_times) / len(detection_times) if detection_times else 0,
        'cpu_usage_pct': cpu_usage if total_times else 0
    }

def test_all_presets(duration=10):
    """Test all available presets and compare results"""
    presets = ["ultra_light", "power_saver", "balanced", "enhanced"]
    results = []
    
    print("\n" + "=" * 60)
    print("VISION PERFORMANCE BENCHMARK")
    print("=" * 60)
    print(f"Testing {len(presets)} presets for {duration} seconds each")
    print("This will take approximately {:.0f} seconds".format(len(presets) * (duration + 2)))
    print("=" * 60)
    
    for preset in presets:
        result = test_preset(preset, duration=duration, show_video=False)
        results.append(result)
        time.sleep(1)  # Brief pause between tests
    
    # Print comparison table
    print("\n" + "=" * 60)
    print("COMPARISON TABLE")
    print("=" * 60)
    print(f"{'Preset':<15} {'FPS':<8} {'Det(ms)':<10} {'CPU%':<8} {'Score':<8}")
    print("-" * 60)
    
    for r in results:
        # Calculate performance score (higher is better)
        # Score = FPS * 10 - (detection_ms / 10) - (cpu_usage / 2)
        score = (r['fps'] * 10) - (r['avg_detection_ms'] / 10) - (r['cpu_usage_pct'] / 2)
        
        print(f"{r['preset']:<15} {r['fps']:<8.2f} {r['avg_detection_ms']:<10.2f} "
              f"{r['cpu_usage_pct']:<8.1f} {score:<8.1f}")
    
    print("=" * 60)
    
    # Find best for different use cases
    best_fps = max(results, key=lambda x: x['fps'])
    best_efficiency = max(results, key=lambda x: x['fps'] / max(x['cpu_usage_pct'], 1))
    lowest_cpu = min(results, key=lambda x: x['cpu_usage_pct'])
    
    print("\nRECOMMENDATIONS:")
    print(f"  Best FPS: {best_fps['preset']} ({best_fps['fps']:.1f} FPS)")
    print(f"  Most Efficient: {best_efficiency['preset']} (FPS/CPU ratio)")
    print(f"  Lowest CPU: {lowest_cpu['preset']} ({lowest_cpu['cpu_usage_pct']:.1f}%)")
    print("=" * 60)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        preset = sys.argv[1]
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        show_video = "--show" in sys.argv
        
        if preset == "all":
            test_all_presets(duration)
        else:
            test_preset(preset, duration, show_video)
    else:
        print("Vision Performance Testing Tool")
        print("\nUsage:")
        print("  python test_performance.py <preset> [duration] [--show]")
        print("  python test_performance.py all [duration]")
        print("\nPresets:")
        print("  ultra_light  - Minimal resource usage")
        print("  power_saver  - Battery friendly")
        print("  balanced     - Default, recommended")
        print("  enhanced     - Better accuracy")
        print("  all          - Test all presets")
        print("\nExamples:")
        print("  python test_performance.py balanced 30")
        print("  python test_performance.py ultra_light 15 --show")
        print("  python test_performance.py all 10")
        print()
        
        # Run default test
        print("Running default test (balanced preset, 10 seconds)...\n")
        test_preset("balanced", duration=10, show_video=False)
