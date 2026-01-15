import asyncio
import websockets
import os
import re
import edge_tts
import pygame

# Import voice configuration for custom TTS
try:
    from voice_config import get_voice, SPEECH_RATE, PITCH_SHIFT
    VOICE = get_voice()
except ImportError:
    VOICE = "en-US-AnaNeural"
    SPEECH_RATE = "+10%"
    PITCH_SHIFT = "+5Hz"

WS_URL = "ws://127.0.0.1:8000/ws/chat"
OUTPUT_FILE = "alisa_voice.mp3"

def clean_text_for_speech(text):
    """Remove emotion tags and formatting from text before speaking."""
    text = re.sub(r'<emotion=[^>]+>', '', text)
    text = re.sub(r'</emotion>', '', text)
    text = re.sub(r'\*[^*]+\*', '', text)
    return text.strip()

async def speak_with_timing(text, ws):
    """Generate TTS and play audio with proper timing signals."""
    try:
        # Generate TTS audio
        communicate = edge_tts.Communicate(text, VOICE, rate=SPEECH_RATE, pitch=PITCH_SHIFT)
        await communicate.save(OUTPUT_FILE)
        
        # Prepare audio playback
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        pygame.mixer.music.load(OUTPUT_FILE)
        
        # Start playback and immediately signal overlay
        pygame.mixer.music.play()
        await ws.send("[SPEECH_START]")
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
            
    except Exception as e:
        print(f"⚠️ TTS error: {e}")

async def text_chat():
    """
    Text-based chat interface with voice output and vision reaction support.
    """
    print("=" * 60)
    print("🌙 Alisa Text Chat - Type & Listen Mode")
    print("=" * 60)
    print("Type your messages and hear Alisa respond.")
    print("🎭 Make sure overlay is running for avatar animations!")
    print("👁️ Alisa can now see you and react proactively!")
    print("Commands:")
    print("  - Type '/mode <mode_name>' to change conversation mode")
    print("  - Type 'exit' or 'quit' to end the chat")
    print("=" * 60)
    print()

    try:
        async with websockets.connect(WS_URL) as ws:
            while True:
                # Get user input in a non-blocking way
                loop = asyncio.get_event_loop()
                
                # Create a task for user input
                input_task = loop.run_in_executor(None, lambda: input("You: ").strip())
                
                # Create a task for receiving messages (vision reactions)
                async def wait_for_message_or_input():
                    """Wait for either user input OR a server message."""
                    receive_task = asyncio.create_task(ws.recv())
                    input_future = asyncio.ensure_future(input_task)
                    
                    done, pending = await asyncio.wait(
                        [receive_task, input_future],
                        return_when=asyncio.FIRST_COMPLETED
                    )
                    
                    # Cancel the pending task
                    for task in pending:
                        task.cancel()
                        try:
                            await task
                        except asyncio.CancelledError:
                            pass
                    
                    # Return which one completed and its result
                    completed_task = done.pop()
                    if completed_task == input_future:
                        return ("input", completed_task.result())
                    else:
                        return ("message", completed_task.result())
                
                result_type, result_value = await wait_for_message_or_input()
                
                if result_type == "input":
                    # User typed something
                    user_text = result_value
                    
                    # Check for exit commands
                    if user_text.lower() in ['exit', 'quit', 'bye']:
                        print("👋 Goodbye! Happy coding!")
                        break

                    # Skip empty messages
                    if not user_text:
                        continue

                    # Send message to backend
                    await ws.send(user_text)
                    
                    # Now wait for response
                    full_reply = ""
                    emotion = "neutral"
                    
                    print("Alisa: ", end="", flush=True)
                    
                    while True:
                        msg = await ws.recv()
                        
                        if msg.startswith("[EMOTION]"):
                            emotion = msg.replace("[EMOTION]", "").strip()
                            continue
                        
                        if msg == "[END]":
                            break
                        
                        if msg.startswith("[") and msg.endswith("]"):
                            continue
                        
                        full_reply += msg
                        print(msg, end="", flush=True)
                    
                    print()  # New line
                    
                    # Speak
                    clean_reply = clean_text_for_speech(full_reply)
                    if clean_reply.strip():
                        await speak_with_timing(clean_reply, ws)
                        await ws.send("[SPEECH_END]")
                    
                    print()  # Extra line for readability
                    
                else:
                    # Server sent a proactive message (vision reaction!)
                    msg = result_value
                    
                    # Clear input line and show Alisa speaking
                    print("\r" + " " * 80 + "\r", end="", flush=True)
                    print("Alisa: ", end="", flush=True)
                    
                    full_reply = ""
                    emotion = "neutral"
                    
                    # Process this message and subsequent ones
                    while True:
                        if msg.startswith("[EMOTION]"):
                            emotion = msg.replace("[EMOTION]", "").strip()
                        elif msg == "[END]":
                            break
                        elif not (msg.startswith("[") and msg.endswith("]")):
                            full_reply += msg
                            print(msg, end="", flush=True)
                        
                        msg = await ws.recv()
                    
                    print()  # New line
                    
                    # Speak
                    clean_reply = clean_text_for_speech(full_reply)
                    if clean_reply.strip():
                        await speak_with_timing(clean_reply, ws)
                        await ws.send("[SPEECH_END]")
                    
                    print()  # Extra line

    except websockets.exceptions.WebSocketException as e:
        print("\n❌ Connection error! Make sure the backend is running.")
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(text_chat())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
