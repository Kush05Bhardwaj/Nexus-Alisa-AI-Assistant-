"""
Optimized webcam module with better resource management and error handling
"""
import cv2
import numpy as np
from vision_config import CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_FPS, PROCESS_WIDTH, PROCESS_HEIGHT
import time

# Initialize camera with optimized settings
cap = None
_last_init_attempt = 0
_init_cooldown = 5.0  # Wait 5 seconds between reinit attempts

def init_camera():
    """Initialize camera with error handling and cooldown"""
    global cap, _last_init_attempt
    
    current_time = time.time()
    
    # Check cooldown
    if cap is None and (current_time - _last_init_attempt) < _init_cooldown:
        return False
    
    _last_init_attempt = current_time
    
    try:
        if cap is None:
            cap = cv2.VideoCapture(0)
            
            if cap.isOpened():
                # Set camera properties
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
                cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
                
                # Reduce buffering for lower latency
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                
                print(f"✅ Camera initialized: {CAMERA_WIDTH}x{CAMERA_HEIGHT} @ {CAMERA_FPS}fps")
                return True
            else:
                cap = None
                print("⚠️ Failed to open camera")
                return False
    except Exception as e:
        cap = None
        print(f"⚠️ Camera init error: {e}")
        return False

# Initialize on module load
init_camera()

def get_frame(downscale=True, retry_on_fail=True):
    """
    Get frame from webcam with optional downscaling for faster processing
    
    Args:
        downscale: If True, returns a smaller frame for detection
        retry_on_fail: Attempt to reinitialize camera on failure
    
    Returns:
        Frame as numpy array or None on error
    """
    global cap
    
    # Ensure camera is initialized
    if cap is None or not cap.isOpened():
        if retry_on_fail:
            if not init_camera():
                return None
        else:
            return None
    
    try:
        ret, frame = cap.read()
        
        if not ret:
            # Try to reinitialize on failure
            if retry_on_fail:
                print("⚠️ Frame capture failed, attempting camera reinit...")
                release_camera()
                if init_camera():
                    ret, frame = cap.read()
                    if not ret:
                        return None
                else:
                    return None
            else:
                return None
        
        # Downscale for faster processing if requested
        if downscale and frame is not None:
            frame = cv2.resize(frame, (PROCESS_WIDTH, PROCESS_HEIGHT), 
                             interpolation=cv2.INTER_LINEAR)
        
        return frame
        
    except Exception as e:
        print(f"⚠️ Frame capture error: {e}")
        return None

def release_camera():
    """Release camera resources"""
    global cap
    if cap is not None:
        try:
            cap.release()
            print("📷 Camera released")
        except Exception as e:
            print(f"⚠️ Error releasing camera: {e}")
        finally:
            cap = None

def get_camera_info():
    """Get current camera configuration"""
    if cap is None or not cap.isOpened():
        return None
    
    try:
        return {
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': int(cap.get(cv2.CAP_PROP_FPS)),
            'backend': cap.getBackendName()
        }
    except Exception as e:
        print(f"⚠️ Error getting camera info: {e}")
        return None

