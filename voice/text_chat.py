import asyncio
import websockets
import os
import re
import threading
from concurrent.futures import ThreadPoolExecutor

# Try different voice output methods in order of preference
speak_func = None

try:
    # Try Edge TTS first (more reliable without RVC dependencies)
    from voice_output_edge import speak
    speak_func = speak
    print("🎀 Using Edge TTS cute voice!")
except Exception as e:
    try:
        # Fall back to RVC if Edge TTS fails
        from voice_output_rvc import speak
        speak_func = speak
        print("🎀 Using RVC waifu voice!")
    except Exception as e2:
        try:
            # Last resort: basic TTS
            from voice_output import speak
            speak_func = speak
            print("⚠️  Using basic voice output")
        except Exception as e3:
            # Fallback if no voice module works
            def speak(text):
                print(f"[SPEAK] {text}")
            speak_func = speak
            print("❌ No voice output available")

WS_URL = "ws://127.0.0.1:8000/ws/chat"

def clean_text_for_speech(text: str) -> str:
    """Remove emotion tags and other non-speech elements from text"""
    # Remove <emotion=...> tags
    text = re.sub(r'<emotion=[^>]+>', '', text)
    # Remove any remaining < > tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Official allowed emotions from prompt.py:
    # happy, calm, teasing, shy, serious, sad, neutral
    # Plus some common variations the LLM might use
    emotions = [
        # Official emotions
        'happy', 'calm', 'teasing', 'shy', 'serious', 'sad', 'neutral',
        # Common variations/extras that might appear
        'blushing', 'excited', 'angry', 'surprised', 'confused', 
        'playful', 'annoyed', 'worried', 'embarrassed', 'flustered',
        'confident', 'gentle', 'nervous', 'proud', 'cheerful'
    ]
    
    # Remove emotion word if it appears at the start of the text
    # Use word boundary to ensure we match complete words only
    for emotion in emotions:
        # Match emotion at start as a complete word with whitespace after
        pattern = r'^\s*\b' + re.escape(emotion) + r'\b\s+'
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Clean up extra whitespace and newlines
    text = ' '.join(text.split())
    text = text.strip()
    
    return text

async def text_chat():
    """
    Text-based chat interface for Alisa with voice output - perfect for midnight coding sessions!
    Type your messages and hear Alisa's voice responses without using a microphone.
    Broadcasts to overlay for avatar animations.
    """
    print("=" * 60)
    print("🌙 Alisa Text Chat - Type & Listen Mode")
    print("=" * 60)
    print("Type your messages and hear Alisa respond.")
    print("🎭 Make sure overlay is running for avatar animations!")
    print("Commands:")
    print("  - Type '/mode <mode_name>' to change conversation mode")
    print("  - Type 'exit' or 'quit' to end the chat")
    print("=" * 60)
    print()

    try:
        async with websockets.connect(WS_URL) as ws:
            while True:
                # Get user input
                user_text = input("You: ").strip()

                # Check for exit commands
                if user_text.lower() in ['exit', 'quit', 'bye']:
                    print("👋 Goodbye! Happy coding!")
                    break

                # Skip empty messages
                if not user_text:
                    continue

                # Send message to backend
                await ws.send(user_text)

                # Collect the full response
                full_reply = ""
                emotion = "neutral"

                print("Alisa: ", end="", flush=True)

                while True:
                    msg = await ws.recv()

                    # Handle emotion tag
                    if msg.startswith("[EMOTION]"):
                        emotion = msg.replace("[EMOTION]", "").strip()
                        continue

                    # Handle mode change confirmation
                    if msg == "[MODE CHANGED]":
                        full_reply = "✓ Mode changed successfully!"
                        continue

                    # Handle end of response
                    if msg == "[END]":
                        break

                    # Stream the response token by token
                    full_reply += msg
                    print(msg, end="", flush=True)

                print()  # New line after response
                
                # Show emotion if it's not neutral (optional visual feedback)
                if emotion != "neutral":
                    print(f"[Emotion: {emotion}]")
                
                # Clean the text before speaking (remove emotion tags)
                clean_reply = clean_text_for_speech(full_reply)
                
                # Speak the cleaned response - runs in separate thread to keep WebSocket alive
                if clean_reply.strip():  # Only speak if there's actual text
                    # Notify overlay to start talking animation
                    try:
                        print("📤 Sending [SPEECH_START] to overlay...")
                        await ws.send("[SPEECH_START]")
                        print("✅ [SPEECH_START] sent successfully")
                    except Exception as e:
                        print(f"⚠️ Failed to send [SPEECH_START]: {e}")
                    
                    print(f"🎤 Speaking: {clean_reply[:50]}...")
                    
                    # Run speech in executor to avoid blocking the WebSocket
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(None, speak_func, clean_reply)
                    
                    print("✅ Speech completed")
                    
                    # Notify overlay to stop talking animation
                    try:
                        print("📤 Sending [SPEECH_END] to overlay...")
                        await ws.send("[SPEECH_END]")
                        print("✅ [SPEECH_END] sent successfully")
                    except Exception as e:
                        print(f"⚠️ Failed to send [SPEECH_END]: {e}")
                
                print()  # Extra line for readability

    except websockets.exceptions.WebSocketException as e:
        print("\n❌ Connection error! Make sure the backend is running.")
        print("Run: uvicorn backend.app.main:app --reload")
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\n\n👋 Chat interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(text_chat())
