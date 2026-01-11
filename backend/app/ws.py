from fastapi import WebSocket, WebSocketDisconnect
from .llm_client import stream_llm_response
from .memory import MemoryBuffer
from .memory_long import save_memory, fetch_recent_memories
from .modes import set_mode, get_mode_prompt
from .emotion import extract_emotion
from .prompt import build_prompt

memory = MemoryBuffer()

async def websocket_chat(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            user_input = await websocket.receive_text()

            if user_input.startswith("/mode"):
                set_mode(user_input.split()[-1])
                await websocket.send_text("[MODE CHANGED]")
                await websocket.send_text("[END]")
                continue


            memory.add("user", user_input)

            memories = fetch_recent_memories()
            system_prompt = build_prompt(get_mode_prompt(), memories)

            messages = [
                {"role": "system", "content": system_prompt},
                *memory.get()
            ]

            full_response = ""

            async for token in stream_llm_response(messages):
                full_response += token
                await websocket.send_text(token)

            emotion, clean_text = extract_emotion(full_response)

            memory.add("assistant", clean_text)
            save_memory(emotion, clean_text)

            await websocket.send_text(f"[EMOTION]{emotion}")
            await websocket.send_text("[END]")

    except WebSocketDisconnect:
        print("Client disconnected")
