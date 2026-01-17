"""
Optimized screen capture with caching and reduced memory usage
"""
import mss
import numpy as np
import time
from PIL import Image

sct = mss.mss()

# Cache for reducing redundant captures
_capture_cache = {
    'image': None,
    'timestamp': 0
}

CACHE_DURATION = 0.5  # Cache screen for 0.5 seconds

def capture_screen(use_cache=True, downscale=True, quality=70):
    """
    Capture screen with optimizations
    
    Args:
        use_cache: Use cached capture if recent (< 0.5s old)
        downscale: Reduce resolution by 50% for faster processing
        quality: Target quality percentage (lower = faster, smaller)
    
    Returns:
        numpy array of screen capture or None on error
    """
    global _capture_cache
    
    try:
        current_time = time.time()
        
        # Use cache if enabled and recent
        if use_cache and _capture_cache['image'] is not None:
            if (current_time - _capture_cache['timestamp']) < CACHE_DURATION:
                return _capture_cache['image']
        
        # Capture screen
        monitor = sct.monitors[1]
        img = sct.grab(monitor)
        
        # Convert to numpy array
        frame = np.array(img)
        
        # Downscale for faster processing if requested
        if downscale:
            h, w = frame.shape[:2]
            new_h, new_w = h // 2, w // 2
            frame = np.array(Image.fromarray(frame).resize((new_w, new_h), Image.Resampling.BILINEAR))
        
        # Update cache
        _capture_cache['image'] = frame
        _capture_cache['timestamp'] = current_time
        
        return frame
        
    except Exception as e:
        print(f"⚠️ Screen capture error: {e}")
        return None

def clear_cache():
    """Clear the capture cache"""
    global _capture_cache
    _capture_cache = {'image': None, 'timestamp': 0}

