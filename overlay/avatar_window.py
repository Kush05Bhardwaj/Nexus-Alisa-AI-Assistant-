import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
from pathlib import Path

# Window configuration
WINDOW_SIZE = 400
# Get the directory where this script is located, then find assets
ASSETS = Path(__file__).parent / "assets"

# Global variables (will be initialized after Tk window is created)
faces = {}
eyes_closed_img = None
mouth_open_img = None
current_face = "neutral"
root = None
canvas = None
base_layer = None  # Base face layer
overlay_layer = None  # Overlay layer for eyes/mouth
is_talking = False
is_blinking = False
talking_timeout_id = None  # Safety timeout to stop talking

# Load image helper
def load(name):
    """Load and resize image"""
    return Image.open(ASSETS / name).resize((WINDOW_SIZE, WINDOW_SIZE))

def create_composite(base_name, overlay_name=None):
    """Create a composite image by layering base + overlay"""
    base = load(base_name).convert("RGBA")
    
    if overlay_name:
        overlay = load(overlay_name).convert("RGBA")
        # Composite overlay on top of base
        base = Image.alpha_composite(base, overlay)
    
    return ImageTk.PhotoImage(base)

def initialize():
    """Initialize the window and load all images"""
    global faces, eyes_closed_img, mouth_open_img, root, canvas, base_layer, overlay_layer
    
    # Create window first
    root = tk.Tk()
    root.title("Alisa")
    root.attributes("-topmost", True)
    root.attributes("-transparentcolor", "white")
    root.overrideredirect(True)
    root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}+50+50")

    # Now load base emotion faces (after Tk is initialized)
    faces = {
        "neutral": ImageTk.PhotoImage(load("base.png").convert("RGBA")),
        "happy": ImageTk.PhotoImage(load("happy.png").convert("RGBA")),
        "teasing": ImageTk.PhotoImage(load("teasing.png").convert("RGBA")),
        "serious": ImageTk.PhotoImage(load("serious.png").convert("RGBA")),
        "calm": ImageTk.PhotoImage(load("calm.png").convert("RGBA")),
        "sad": ImageTk.PhotoImage(load("sad.png").convert("RGBA")),
    }
    
    # Load overlay images as full images (not composites)
    eyes_closed_img = ImageTk.PhotoImage(load("eyes_closed.png").convert("RGBA"))
    mouth_open_img = ImageTk.PhotoImage(load("mouth_open.png").convert("RGBA"))

    # Canvas
    canvas = Canvas(
        root,
        width=WINDOW_SIZE,
        height=WINDOW_SIZE,
        bg="white",
        highlightthickness=0
    )
    canvas.pack()

    # Create base layer on canvas
    base_layer = canvas.create_image(
        0, 0, anchor="nw", image=faces["neutral"]
    )
    
    # Create overlay layer (initially empty/transparent)
    overlay_layer = canvas.create_image(
        0, 0, anchor="nw", image=""
    )

# Drag functionality
def start_drag(event):
    root._drag_data = {"x": event.x, "y": event.y}

def on_drag(event):
    x = root.winfo_x() + event.x - root._drag_data["x"]
    y = root.winfo_y() + event.y - root._drag_data["y"]
    root.geometry(f"+{x}+{y}")

# Animation functions
def animate_blink():
    global is_blinking
    if is_talking:
        root.after(3000, animate_blink)
        return
    
    is_blinking = True
    print("👁️ Blinking...")
    # Show eyes_closed image directly
    canvas.itemconfig(base_layer, image=eyes_closed_img)
    canvas.update_idletasks()  # Force update
    root.after(150, lambda: end_blink())

def end_blink():
    global is_blinking
    is_blinking = False
    print("👁️ Eyes open")
    # ALWAYS return to neutral base face after blinking, not current emotion
    canvas.itemconfig(base_layer, image=faces["neutral"])
    canvas.update_idletasks()  # Force update
    root.after(3000, animate_blink)

def animate_mouth():
    if not is_talking:
        print("👄 Mouth animation stopped (is_talking=False)")
        # Return to neutral face when talking stops
        canvas.itemconfig(base_layer, image=faces["neutral"])
        canvas.update_idletasks()
        return
    print(f"👄 Mouth open (is_talking={is_talking})")
    # Show mouth open image directly
    canvas.itemconfig(base_layer, image=mouth_open_img)
    canvas.update_idletasks()  # Force update
    
    # Return to current emotion face
    def close_mouth():
        if not is_talking:
            print("👄 Skip closing - already stopped talking")
            return
        print(f"👄 Mouth closed (is_talking={is_talking})")
        # During talking, return to current emotion
        canvas.itemconfig(base_layer, image=faces[current_face])
        canvas.update_idletasks()  # Force update
    
    root.after(200, close_mouth)  # Mouth stays open for 200ms
    root.after(500, animate_mouth)  # Total cycle is 500ms

# Emotion setter
def set_emotion(emotion: str):
    global current_face
    if emotion not in faces:
        emotion = "neutral"
    current_face = emotion
    print(f"😊 Emotion changed to: {emotion}")
    canvas.itemconfig(base_layer, image=faces[current_face])
    canvas.update_idletasks()  # Force update

# Public API
def start_talking():
    global is_talking, talking_timeout_id
    print(f"🎤 START TALKING called (is_talking was {is_talking})")
    
    # Cancel any existing timeout
    if talking_timeout_id:
        root.after_cancel(talking_timeout_id)
        talking_timeout_id = None
    
    if not is_talking:  # Only start if not already talking
        is_talking = True
        animate_mouth()
    else:
        print("⚠️ Already talking, ignoring duplicate start")
    
    # Safety timeout: auto-stop after 30 seconds if no stop signal received
    talking_timeout_id = root.after(30000, lambda: [
        print("⚠️ SAFETY TIMEOUT: Auto-stopping talking after 30 seconds"),
        stop_talking()
    ])

def stop_talking():
    global is_talking, talking_timeout_id
    print(f"🤐 STOP TALKING called (is_talking was {is_talking})")
    
    # Cancel safety timeout
    if talking_timeout_id:
        root.after_cancel(talking_timeout_id)
        talking_timeout_id = None
    
    is_talking = False
    # Return to neutral face after speaking
    canvas.itemconfig(base_layer, image=faces["neutral"])
    canvas.update_idletasks()  # Force update
    print(f"✅ Talking stopped, returned to neutral face")

def run():
    """Initialize and run the avatar window"""
    initialize()
    
    # Bind events after canvas is created
    canvas.bind("<Button-1>", start_drag)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<Button-3>", lambda e: root.quit())  # Right-click to close
    
    # Start animations
    root.after(3000, animate_blink)
    root.mainloop()

if __name__ == "__main__":
    run()