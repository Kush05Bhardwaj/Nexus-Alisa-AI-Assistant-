MODES = {
    "teasing": "You tease gently and act playful.",
    "serious": "You are calm, mature, and direct.",
    "calm": "You speak softly and reassuringly."
}

current_mode = "teasing"

def set_mode(mode):
    global current_mode
    if mode in MODES:
        current_mode = mode

def get_mode_prompt():
    return MODES[current_mode]
