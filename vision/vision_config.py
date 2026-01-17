"""
Vision System Configuration
Adjust these settings to balance between performance and accuracy
OPTIMIZED: Added more presets and fine-tuning options
"""

# === DETECTION METHOD ===
# Set to True to use MediaPipe (more accurate, heavier on resources)
# Set to False to use Haar Cascade (lighter, fast, CPU-friendly)
USE_MEDIAPIPE = False

# === PERFORMANCE SETTINGS ===
# How often to run detection (in seconds)
# Lower = more responsive, Higher = less CPU usage
DETECTION_INTERVAL = 1.5

# Process every Nth frame (1 = all frames, 2 = every other frame)
# Higher = less CPU usage but may miss quick changes
FRAME_SKIP = 2

# Use detection caching to avoid redundant processing
# Recent results are reused if < 0.5 seconds old
USE_DETECTION_CACHE = True

# === CAMERA SETTINGS ===
# Camera resolution (lower = faster processing)
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 15

# Processing resolution (frames are downscaled to this for detection)
PROCESS_WIDTH = 320
PROCESS_HEIGHT = 240

# === DETECTION THRESHOLDS ===
# Haar Cascade settings
CASCADE_SCALE_FACTOR = 1.2   # 1.1 = slower but more accurate, 1.3 = faster but may miss faces
CASCADE_MIN_NEIGHBORS = 4     # Higher = fewer false positives but may miss faces
CASCADE_MIN_FACE_SIZE = (40, 40)

# MediaPipe settings (if enabled)
MEDIAPIPE_MIN_CONFIDENCE = 0.7  # 0.5 = more detections, 0.8 = fewer false positives

# === ATTENTION DETECTION ===
# Minimum number of eyes detected for "focused" state
MIN_EYES_FOR_FOCUS = 2

# === MEMORY OPTIMIZATION ===
# Enable aggressive memory management
USE_AGGRESSIVE_MEMORY_CLEANUP = True

# Maximum cache sizes
MAX_DETECTION_CACHE_AGE = 0.5  # seconds
MAX_SCREEN_CACHE_AGE = 0.5     # seconds

# === PRESETS ===
def apply_preset(preset_name):
    """
    Apply predefined configuration presets
    
    Presets:
    - "ultra_light": Minimal CPU usage, good for low-end systems
    - "power_saver": Battery-friendly settings for laptops
    - "balanced": Good balance between performance and accuracy (default)
    - "enhanced": Better accuracy, uses more resources
    - "maximum": Best accuracy, highest resource usage
    """
    global USE_MEDIAPIPE, DETECTION_INTERVAL, FRAME_SKIP
    global CASCADE_SCALE_FACTOR, CASCADE_MIN_NEIGHBORS
    global CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_FPS
    global PROCESS_WIDTH, PROCESS_HEIGHT
    
    if preset_name == "ultra_light":
        USE_MEDIAPIPE = False
        DETECTION_INTERVAL = 2.5
        FRAME_SKIP = 4
        CASCADE_SCALE_FACTOR = 1.3
        CASCADE_MIN_NEIGHBORS = 3
        CAMERA_WIDTH = 640
        CAMERA_HEIGHT = 480
        CAMERA_FPS = 10
        PROCESS_WIDTH = 240
        PROCESS_HEIGHT = 180
        print("✅ Applied preset: Ultra Light (minimal resources)")
        
    elif preset_name == "power_saver":
        USE_MEDIAPIPE = False
        DETECTION_INTERVAL = 2.0
        FRAME_SKIP = 3
        CASCADE_SCALE_FACTOR = 1.25
        CASCADE_MIN_NEIGHBORS = 3
        CAMERA_WIDTH = 640
        CAMERA_HEIGHT = 480
        CAMERA_FPS = 12
        PROCESS_WIDTH = 320
        PROCESS_HEIGHT = 240
        print("✅ Applied preset: Power Saver (battery friendly)")
        
    elif preset_name == "balanced":
        USE_MEDIAPIPE = False
        DETECTION_INTERVAL = 1.5
        FRAME_SKIP = 2
        CASCADE_SCALE_FACTOR = 1.2
        CASCADE_MIN_NEIGHBORS = 4
        CAMERA_WIDTH = 640
        CAMERA_HEIGHT = 480
        CAMERA_FPS = 15
        PROCESS_WIDTH = 320
        PROCESS_HEIGHT = 240
        print("✅ Applied preset: Balanced (default)")
        
    elif preset_name == "enhanced":
        USE_MEDIAPIPE = True
        DETECTION_INTERVAL = 1.0
        FRAME_SKIP = 1
        CASCADE_SCALE_FACTOR = 1.1
        CASCADE_MIN_NEIGHBORS = 5
        CAMERA_WIDTH = 1280
        CAMERA_HEIGHT = 720
        CAMERA_FPS = 20
        PROCESS_WIDTH = 640
        PROCESS_HEIGHT = 480
        print("✅ Applied preset: Enhanced (better accuracy)")
        
    elif preset_name == "maximum":
        USE_MEDIAPIPE = True
        DETECTION_INTERVAL = 0.5
        FRAME_SKIP = 1
        CASCADE_SCALE_FACTOR = 1.05
        CASCADE_MIN_NEIGHBORS = 6
        CAMERA_WIDTH = 1920
        CAMERA_HEIGHT = 1080
        CAMERA_FPS = 30
        PROCESS_WIDTH = 640
        PROCESS_HEIGHT = 480
        print("✅ Applied preset: Maximum (best quality, high resources)")
        
    else:
        print(f"⚠️ Unknown preset: {preset_name}")

# Default preset
CURRENT_PRESET = "balanced"

