import asyncio
import websockets
from voice_input import record_audio, speech_to_text
from voice_output import speak

WS_URL = "ws://127.0.0.1:8000/ws/chat"

async def voice_chat():
    async with websockets.connect(WS_URL) as ws:
        while True:
            input("Press ENTER to talk...")
            record_audio()
            user_text = speech_to_text()

            if not user_text.strip():
                continue

            await ws.send(user_text)

            full_reply = ""

            while True:
                msg = await ws.recv()

                if msg.startswith("[EMOTION]"):
                    continue

                if msg == "[END]":
                    break

                full_reply += msg

            print("Alisa:", full_reply)
            speak(full_reply)

asyncio.run(voice_chat())
