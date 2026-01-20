"""
Voice Configuration for Alisa
Change these settings to customize your waifu's voice!
"""

# Voice Selection for Edge TTS (used before RVC conversion)
# These are cute/young sounding voices perfect for anime characters

VOICE_OPTIONS = {
    # English Voices (sorted by cuteness factor 😊)
    "ana": "en-US-AnaNeural",           # 🌟 RECOMMENDED - Young, bright, energetic
    "jenny": "en-US-JennyNeural",       # Neural, clear, professional
    "aria": "en-US-AriaNeural",         # Friendly, conversational
    "michelle": "en-US-MichelleNeural", # Young adult, clear
    
    # Indian English Voices (for Hinglish! 🇮🇳)
    "neerja": "en-IN-NeerjaNeural",     # 🌟 RECOMMENDED for Hinglish - Young, clear Indian English
    "swara": "hi-IN-SwaraNeural",       # Hindi female voice (good for Hindi-heavy Hinglish)
    
    # Japanese Voices (for maximum kawaii 🎌)
    "nanami": "ja-JP-NanamiNeural",     # 💖 Most anime-like, high pitch
    "aoi": "ja-JP-AoiNeural",           # Cute, youthful
    
    # Chinese Voices (also cute options 🎎)
    "xiaoxiao": "zh-CN-XiaoxiaoNeural", # Sweet, young-sounding
    "xiaoyi": "zh-CN-XiaoyiNeural",     # Cute, friendly
}

# 🎀 CHOOSE YOUR WAIFU VOICE HERE 🎀
# Options: "ana", "nanami", "xiaoxiao", "jenny", "neerja" (for Hinglish), etc.
SELECTED_VOICE = "ana"  # Change this to try different voices!

# 🇮🇳 HINGLISH MODE 🇮🇳
# When enabled, automatically switches to Indian voice for Hinglish text
HINGLISH_AUTO_DETECT = True

# Voice options for Hinglish (try different ones!)
# "neerja" = Indian English (more natural for mixed Hinglish)
# "swara" = Pure Hindi (might sound younger/cuter)
HINGLISH_VOICE = "swara"  # Try "swara" for cuter sound, "neerja" for clarity

# Get the actual voice ID
def get_voice():
    return VOICE_OPTIONS.get(SELECTED_VOICE, VOICE_OPTIONS["ana"])

def get_hinglish_voice():
    return VOICE_OPTIONS.get(HINGLISH_VOICE, VOICE_OPTIONS["neerja"])

# TTS Settings
SPEECH_RATE = "+15%"  # Make speech slightly faster/cuter (use +XX% or -XX%)
PITCH_SHIFT = "+10Hz"  # Make voice slightly higher pitched (use +XXHz or -XXHz)

# Hinglish-specific settings - WAIFU MODE 🎀
# Higher pitch and faster rate for cute anime-like voice
HINGLISH_SPEECH_RATE = "+20%"  # Faster for cuteness (was +10%)
HINGLISH_PITCH_SHIFT = "+15Hz"  # Much higher pitch for waifu sound (was +8Hz)

# Advanced: Custom SSML for emotion expression
# You can add prosody changes based on emotion
EMOTION_PROSODY = {
    "happy": {"rate": "+15%", "pitch": "+8Hz"},
    "sad": {"rate": "-10%", "pitch": "-5Hz"},
    "angry": {"rate": "+20%", "pitch": "+10Hz"},
    "neutral": {"rate": "+10%", "pitch": "+5Hz"},
}

def get_prosody(emotion="neutral"):
    """Get prosody settings for an emotion"""
    return EMOTION_PROSODY.get(emotion, EMOTION_PROSODY["neutral"])

# Hinglish detection - simple regex patterns
import re

def is_hinglish(text: str) -> bool:
    """
    Detect if text contains Hinglish (Hindi words in Roman script)
    Returns True if Hinglish is detected
    """
    if not HINGLISH_AUTO_DETECT:
        return False
    
    # Common Hinglish patterns and words
    hinglish_patterns = [
        r'\b(hai|hain|ho|hoon|tha|thi|kya|kaise|kaisa|kyun|kab|kahan)\b',  # Common verbs/question words (removed 'the')
        r'\b(acha|accha|theek|thik|bilkul|zaroor|shayad|abhi|kabhi|phir)\b',  # Common adverbs
        r'\b(bhai|yaar|dost|beta|ji|na|haan|nahi|nai)\b',  # Common colloquial terms
        r'\b(bahut|bohat|itna|utna|kitna|jyada|kam|zyada)\b',  # Quantity words
        r'\b(dekh|dekho|suno|bolo|karo|hoga|hogi|hoge)\b',  # Action verbs (removed duplicate 'karo')
        r'\b(mera|meri|mere|tera|teri|tere|uska|uski|uske|tumhara|tumhari|tumhare)\b',  # Possessives
        r'\b(apna|apni|apne|koi|kuch|sab|sabhi|main|mein|tum|aap)\b',  # Pronouns
    ]
    
    text_lower = text.lower()
    
    # Check if any Hinglish pattern matches
    for pattern in hinglish_patterns:
        if re.search(pattern, text_lower):
            return True
    
    # Also check for Devanagari script (pure Hindi)
    if re.search(r'[\u0900-\u097F]', text):
        return True
    
    return False

def get_voice_for_text(text: str) -> str:
    """
    Get appropriate voice based on text content
    Returns Hinglish voice if Hinglish detected, otherwise default voice
    """
    if is_hinglish(text):
        return get_hinglish_voice()
    return get_voice()

def get_tts_params_for_text(text: str) -> dict:
    """
    Get TTS parameters (rate, pitch) based on text content
    Returns dict with 'rate' and 'pitch' keys
    """
    if is_hinglish(text):
        return {
            "rate": HINGLISH_SPEECH_RATE,
            "pitch": HINGLISH_PITCH_SHIFT
        }
    return {
        "rate": SPEECH_RATE,
        "pitch": PITCH_SHIFT
    }