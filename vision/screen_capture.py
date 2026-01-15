import mss
import numpy as np

sct = mss.mss()

def capture_screen():
    monitor = sct.monitors[1]
    img = sct.grab(monitor)
    return np.array(img)
