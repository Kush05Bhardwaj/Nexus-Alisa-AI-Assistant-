"""
Alisa Voice Chat - Full-featured voice interface
- Voice input with speech recognition
- Voice output with Edge TTS
- Async vision reaction support
- Emotion display
- Overlay integration
- Mode switching
- Clean console output
"""

import asyncio
import websockets
import os
import re
from pathlib import Path
import edge_tts
import pygame

# Voice input modules
try:
    from voice_input import record_audio, speech_to_text
    VOICE_INPUT_AVAILABLE = True
except ImportError:
    VOICE_INPUT_AVAILABLE = False
    print("⚠️ Voice input not available. Install faster-whisper and sounddevice.")

# Voice output - USE HINGLISH-AWARE VERSION FOR BEST RESULTS
try:
    from voice_output_hinglish import speak_async as speak_hinglish
    USE_HINGLISH_TTS = True
    print("🇮🇳 Hinglish-aware TTS enabled!")
except ImportError:
    USE_HINGLISH_TTS = False
    print("⚠️ Hinglish TTS not available, using basic Edge TTS")

WS_URL = "ws://127.0.0.1:8000/ws/chat"

# Import voice configuration
try:
    from voice_config import get_voice, SPEECH_RATE, PITCH_SHIFT
    VOICE = get_voice()
except ImportError:
    VOICE = "en-US-AnaNeural"
    SPEECH_RATE = "+10%"
    PITCH_SHIFT = "+5Hz"

OUTPUT_FILE = "alisa_voice.mp3"

# Emotion emoji mapping
EMOTION_EMOJI = {
    'happy': '😊',
    'calm': '😌',
    'teasing': '😏',
    'shy': '😳',
    'serious': '😐',
    'sad': '😢',
    'neutral': '🙂',
    'excited': '🤩',
    'playful': '😄',
    'confident': '😎'
}


async def speak_with_timing(text, ws):
    """
    Generate TTS and play audio with perfect timing for overlay sync.
    Now with Hinglish support via RVC!
    """
    try:
        # If Hinglish-aware TTS is available, use it
        if USE_HINGLISH_TTS:
            # Notify overlay
            try:
                await ws.send("[SPEECH_START]")
            except Exception as e:
                print(f"⚠️ Failed to send [SPEECH_START]: {e}")
            
            # Use Hinglish-aware TTS with RVC
            await speak_hinglish(text)
            
            # Notify overlay end
            try:
                await ws.send("[SPEECH_END]")
            except Exception as e:
                print(f"⚠️ Failed to send [SPEECH_END]: {e}")
            
            return
        
        # Fallback to basic Edge TTS
        communicate = edge_tts.Communicate(text, VOICE, rate=SPEECH_RATE, pitch=PITCH_SHIFT)
        await communicate.save(OUTPUT_FILE)
        
        # Prepare and play audio
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        pygame.mixer.music.load(OUTPUT_FILE)
        pygame.mixer.music.play()
        
        # Notify overlay
        try:
            await ws.send("[SPEECH_START]")
        except Exception as e:
            print(f"⚠️ Failed to send [SPEECH_START]: {e}")
        
        # Wait for playback
        def wait_for_playback():
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, wait_for_playback)
        
        pygame.mixer.music.unload()
        
    except Exception as e:
        print(f"❌ TTS error: {e}")


def clean_text_for_speech(text: str) -> str:
    """Remove emotion tags and emotion words from text"""
    text = re.sub(r'<emotion=[^>]+>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    
    emotions = [
        'happy', 'calm', 'teasing', 'shy', 'serious', 'sad', 'neutral',
        'excited', 'playful', 'confident', 'gentle', 'cheerful',
        'blushing', 'surprised', 'nervous', 'embarrassed', 'flustered',
        'angry', 'annoyed', 'worried', 'confused'
    ]
    
    # Remove emotion word at start
    for emotion in emotions:
        pattern = r'^\s*\b' + re.escape(emotion) + r'\b[\s\n]+'
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Remove standalone emotion words
    for emotion in emotions:
        pattern = r'^\s*' + re.escape(emotion) + r'\s*$'
        text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)
    
    return ' '.join(text.split()).strip()


async def listen_for_messages(ws):
    """
    Background task that listens for server messages.
    Handles both user-initiated responses and proactive vision reactions.
    """
    while True:
        try:
            full_reply = ""
            emotion = "neutral"
            
            # Collect the complete message first (don't print tokens as they arrive)
            while True:
                msg = await ws.recv()
                
                if msg.startswith("[EMOTION]"):
                    emotion = msg.replace("[EMOTION]", "").strip()
                elif msg == "[END]":
                    break
                elif not (msg.startswith("[") and msg.endswith("]")):
                    # Collect text tokens
                    full_reply += msg
            
            # Now print the complete message all at once
            if full_reply.strip():
                # Clear current line
                print("\r" + " " * 80 + "\r", end="", flush=True)
                
                # Clean the text for display and speech
                clean_display = clean_text_for_speech(full_reply)
                
                # Show emotion emoji
                emoji = EMOTION_EMOJI.get(emotion.lower(), '🙂')
                print(f"{clean_display} {emoji}")
                
                # Speak the cleaned text
                if clean_display.strip():
                    await speak_with_timing(clean_display, ws)
                    
                    # Notify overlay to stop
                    try:
                        await ws.send("[SPEECH_END]")
                    except Exception as e:
                        print(f"⚠️ Failed to send [SPEECH_END]: {e}")
                
                print()  # Blank line for readability
            
        except websockets.exceptions.ConnectionClosed:
            print("\n❌ Connection closed")
            break
        except Exception as e:
            print(f"\n❌ Error in message listener: {e}")
            break


async def voice_input_loop(ws):
    """
    Main loop for voice input - press Enter to record and speak.
    """
    while True:
        try:
            # Wait for user to press Enter
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: input("🎤 Press ENTER to speak... "))
            
            print("🎤 Listening...")
            
            # Record and transcribe (blocking operations in executor)
            def record_and_transcribe():
                record_audio()
                return speech_to_text()
            
            user_text = await loop.run_in_executor(None, record_and_transcribe)
            
            if not user_text or not user_text.strip():
                print("⚠️ No speech detected. Try again.\n")
                continue
            
            # Show what user said - no prefix, just the message
            print(f"{user_text}")
            
            # Check for exit commands
            if user_text.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                print("👋 Goodbye! Happy coding!")
                break
            
            # Send to backend
            await ws.send(user_text)
            # Response handled by background listener
            
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


async def voice_chat():
    """
    Main voice chat interface with full feature support.
    """
    print("=" * 60)
    print("🎙️ Alisa Voice Chat - Speak & Listen Mode")
    print("=" * 60)
    print("Speak to Alisa and hear her voice responses!")
    print("🎭 Make sure overlay is running for avatar animations!")
    print("👁️ Alisa can see you and react proactively!")
    print("Commands:")
    print("  - Press ENTER, then speak your message")
    print("  - Say 'exit' or 'quit' to end the chat")
    print("=" * 60)
    print()
    
    if not VOICE_INPUT_AVAILABLE:
        print("❌ Voice input not available!")
        print("Install requirements: pip install faster-whisper sounddevice")
        return
    
    try:
        async with websockets.connect(WS_URL) as ws:
            # Start background message listener
            listener_task = asyncio.create_task(listen_for_messages(ws))
            
            # Wait for listener to start
            await asyncio.sleep(0.1)
            
            # Run voice input loop
            await voice_input_loop(ws)
            
            # Cancel listener when done
            listener_task.cancel()
            
    except websockets.exceptions.WebSocketException as e:
        print("\n❌ Connection error! Make sure the backend is running.")
        print("Run: cd backend && uvicorn app.main:app --reload")
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Run the voice chat
    asyncio.run(voice_chat())
