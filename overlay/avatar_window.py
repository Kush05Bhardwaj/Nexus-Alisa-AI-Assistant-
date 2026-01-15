import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
from pathlib import Path

# Window configuration
WINDOW_SIZE = 400
ASSETS = Path("overlay/assets")

# Load image helper
def load(name):
    return ImageTk.PhotoImage(
        Image.open(ASSETS / name).resize((WINDOW_SIZE, WINDOW_SIZE))
    )

# Load all emotion faces
faces = {
    "neutral": load("base.png"),
    "happy": load("happy.png"),
    "teasing": load("teasing.png"),
    "serious": load("serious.png"),
    "calm": load("calm.png"),
    "sad": load("sad.png"),
}

eyes_closed_img = load("eyes_closed.png")
mouth_open_img = load("mouth_open.png")

current_face = "neutral"

# Create window
root = tk.Tk()
root.title("Alisa")
root.attributes("-topmost", True)
root.attributes("-transparentcolor", "white")
root.overrideredirect(True)
root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}+50+50")

# Canvas
canvas = Canvas(
    root,
    width=WINDOW_SIZE,
    height=WINDOW_SIZE,
    bg="white",
    highlightthickness=0
)
canvas.pack()

# Create image on canvas
image_on_canvas = canvas.create_image(
    0, 0, anchor="nw", image=faces["neutral"]
)

# State
is_talking = False
is_blinking = False

# Drag functionality
def start_drag(event):
    root._drag_data = {"x": event.x, "y": event.y}

def on_drag(event):
    x = root.winfo_x() + event.x - root._drag_data["x"]
    y = root.winfo_y() + event.y - root._drag_data["y"]
    root.geometry(f"+{x}+{y}")

canvas.bind("<Button-1>", start_drag)
canvas.bind("<B1-Motion>", on_drag)

# Animation functions
def animate_blink():
    global is_blinking
    if is_talking:
        root.after(3000, animate_blink)
        return
    
    is_blinking = True
    canvas.itemconfig(image_on_canvas, image=eyes_closed_img)
    root.after(150, lambda: end_blink())

def end_blink():
    global is_blinking
    is_blinking = False
    canvas.itemconfig(image_on_canvas, image=faces[current_face])
    root.after(3000, animate_blink)

def animate_mouth():
    if not is_talking:
        return
    canvas.itemconfig(image_on_canvas, image=mouth_open_img)
    root.after(120, lambda: canvas.itemconfig(
        image_on_canvas, image=faces[current_face]
    ))
    root.after(260, animate_mouth)

# Emotion setter
def set_emotion(emotion: str):
    global current_face
    if emotion not in faces:
        emotion = "neutral"
    current_face = emotion
    canvas.itemconfig(image_on_canvas, image=faces[current_face])

# Public API
def start_talking():
    global is_talking
    is_talking = True
    animate_mouth()

def stop_talking():
    global is_talking
    is_talking = False
    canvas.itemconfig(image_on_canvas, image=faces[current_face])

def run():
    root.after(3000, animate_blink)
    root.mainloop()

if __name__ == "__main__":
    run()