import pytesseract
import cv2
import win32gui

def get_active_window():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())

def analyze_screen(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)

    window = get_active_window()

    return {
        "window": window,
        "text": text[:300]  # truncate
    }
