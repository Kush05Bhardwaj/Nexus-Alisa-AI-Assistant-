import tkinter as tk
from PIL import Image, ImageTk
import random

WINDOW_SIZE = 300

root = tk.Tk()
root.title("Alisa")
root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}+50+50")
root.attributes("-topmost", True)
root.overrideredirect(True)

canvas = tk.Canvas(
    root,
    width=WINDOW_SIZE,
    height=WINDOW_SIZE,
    bg="white",
    highlightthickness=0
)
canvas.pack()

# ---------------- Drag window ----------------
def start_drag(event):
    root._drag_x = event.x
    root._drag_y = event.y

def on_drag(event):
    x = root.winfo_x() + event.x - root._drag_x
    y = root.winfo_y() + event.y - root._drag_y
    root.geometry(f"+{x}+{y}")

canvas.bind("<Button-1>", start_drag)
canvas.bind("<B1-Motion>", on_drag)

# ---------------- Load images ----------------
base_img = ImageTk.PhotoImage(
    Image.open("assets/base.png").resize((WINDOW_SIZE, WINDOW_SIZE))
)

eyes_closed_img = ImageTk.PhotoImage(
    Image.open("assets/eyes_closed.png").resize((WINDOW_SIZE, WINDOW_SIZE))
)

mouth_open_img = ImageTk.PhotoImage(
    Image.open("assets/mouth_open.png").resize((WINDOW_SIZE, WINDOW_SIZE))
)

canvas.create_rectangle(0, 0, WINDOW_SIZE, WINDOW_SIZE, fill="white", outline="")
image_on_canvas = canvas.create_image(0, 0, anchor="nw", image=base_img)

# ---------------- Blink ----------------
def blink():
    canvas.itemconfig(image_on_canvas, image=eyes_closed_img)
    root.after(120, lambda: canvas.itemconfig(image_on_canvas, image=base_img))
    root.after(random.randint(3000, 6000), blink)

root.after(2000, blink)

# ---------------- Talking animation ----------------
is_talking = False

def start_talking():
    global is_talking
    if not is_talking:
        is_talking = True
        animate_mouth()

def stop_talking():
    global is_talking
    is_talking = False
    canvas.itemconfig(image_on_canvas, image=base_img)

def animate_mouth():
    if not is_talking:
        return
    canvas.itemconfig(image_on_canvas, image=mouth_open_img)
    root.after(120, lambda: canvas.itemconfig(image_on_canvas, image=base_img))
    root.after(260, animate_mouth)

# ---------------- Public API ----------------
def run_avatar():
    root.mainloop()
