"""
Optimized screen analysis with caching and efficient text extraction
"""
import pytesseract
import cv2
import win32gui
import time
from functools import lru_cache

# Cache for window title to reduce win32gui calls
_window_cache = {
    'title': '',
    'timestamp': 0
}

WINDOW_CACHE_DURATION = 1.0  # Cache window title for 1 second

def get_active_window(use_cache=True):
    """
    Get active window title with caching
    
    Args:
        use_cache: Use cached title if recent (< 1s old)
    
    Returns:
        Window title string
    """
    global _window_cache
    
    try:
        current_time = time.time()
        
        # Use cache if enabled and recent
        if use_cache and _window_cache['title']:
            if (current_time - _window_cache['timestamp']) < WINDOW_CACHE_DURATION:
                return _window_cache['title']
        
        # Get current window title
        title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        
        # Update cache
        _window_cache['title'] = title
        _window_cache['timestamp'] = current_time
        
        return title
        
    except Exception as e:
        print(f"⚠️ Window title error: {e}")
        return ""

def analyze_screen(frame, max_text_length=500, use_preprocessing=True):
    """
    Analyze screen with optimized OCR
    
    Args:
        frame: Screen capture frame
        max_text_length: Maximum text to extract (truncate for performance)
        use_preprocessing: Apply image preprocessing for better OCR
    
    Returns:
        Dict with window title and extracted text
    """
    try:
        # Get window title with caching
        window = get_active_window(use_cache=True)
        
        # Convert to grayscale for faster OCR
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame
        
        # Preprocessing for better OCR accuracy (optional)
        if use_preprocessing:
            # Apply slight blur to reduce noise
            gray = cv2.GaussianBlur(gray, (3, 3), 0)
            
            # Increase contrast
            gray = cv2.convertScaleAbs(gray, alpha=1.2, beta=10)
        
        # OCR with optimized config
        # --psm 6: Assume uniform block of text
        # -c tessedit_char_whitelist: Limit to common chars for speed (optional)
        custom_config = r'--psm 6'
        text = pytesseract.image_to_string(gray, config=custom_config)
        
        # Truncate text for performance and memory
        if len(text) > max_text_length:
            text = text[:max_text_length]
        
        return {
            "window": window,
            "text": text.strip()
        }
        
    except Exception as e:
        print(f"⚠️ Screen analysis error: {e}")
        return {
            "window": "",
            "text": ""
        }

def clear_cache():
    """Clear the window title cache"""
    global _window_cache
    _window_cache = {'title': '', 'timestamp': 0}

