"""
Test Hinglish TTS Pipeline
Tests language detection and voice selection
"""
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from voice_config import is_hinglish, get_voice_for_text, get_tts_params_for_text

# Test cases
test_cases = [
    ("Hello, how are you?", False, "en-US-AnaNeural"),
    ("Kya haal hai?", True, "en-IN-NeerjaNeural"),
    ("Yaar, this is amazing!", True, "en-IN-NeerjaNeural"),
    ("Main bahut khush hoon", True, "en-IN-NeerjaNeural"),
    ("The weather is nice today", False, "en-US-AnaNeural"),
    ("Acha, theek hai bhai", True, "en-IN-NeerjaNeural"),
]

print("🧪 Testing Hinglish Detection\n")
print("─" * 70)

all_passed = True
for text, expected_hinglish, expected_voice in test_cases:
    detected = is_hinglish(text)
    voice = get_voice_for_text(text)
    params = get_tts_params_for_text(text)
    
    status = "✓" if detected == expected_hinglish else "✗"
    voice_status = "✓" if voice == expected_voice else "✗"
    
    if detected != expected_hinglish or voice != expected_voice:
        all_passed = False
    
    print(f"{status} {voice_status} | {text}")
    print(f"      Hinglish: {detected} | Voice: {voice}")
    print(f"      Rate: {params['rate']} | Pitch: {params['pitch']}")
    print()

print("─" * 70)
if all_passed:
    print("✅ All tests passed!")
else:
    print("⚠️ Some tests failed")

# Now test actual TTS
print("\n🎤 Testing TTS Generation\n")
print("This will generate and play audio...")
print("Press Ctrl+C to skip\n")

try:
    import asyncio
    from voice_output_hinglish import speak
    
    print("1️⃣ English: ", end="", flush=True)
    speak("Hello! Testing English voice.")
    print("✓")
    
    print("2️⃣ Hinglish: ", end="", flush=True)
    speak("Namaste! Kya haal hai yaar?")
    print("✓")
    
    print("\n✅ TTS tests complete!")
    
except KeyboardInterrupt:
    print("\n⏸️ TTS tests skipped")
except Exception as e:
    print(f"\n❌ TTS error: {e}")