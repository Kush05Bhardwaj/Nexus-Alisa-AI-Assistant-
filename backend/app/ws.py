from fastapi import WebSocket, WebSocketDisconnect
from .llm_client import stream_llm_response
from .memory import MemoryBuffer
from .memory_long import save_memory, fetch_recent_memories
from .modes import set_mode, get_mode_prompt
from .emotion import extract_emotion
from .prompt import build_prompt
from typing import List
import asyncio

memory = MemoryBuffer()

# Store all connected WebSocket clients
connected_clients: List[WebSocket] = []

async def broadcast_message(message: str, exclude: WebSocket = None):
    """Send a message to all connected clients, optionally excluding one"""
    disconnected = []
    broadcast_count = 0
    for client in connected_clients:
        if client != exclude:
            try:
                await client.send_text(message)
                broadcast_count += 1
            except Exception as e:
                print(f"⚠️ Broadcast error: {e}")
                disconnected.append(client)
    
    if message in ["[SPEECH_START]", "[SPEECH_END]"]:
        print(f"   → Broadcasted to {broadcast_count} client(s)")
    
    # Remove disconnected clients
    for client in disconnected:
        if client in connected_clients:
            connected_clients.remove(client)

async def keepalive_ping(websocket: WebSocket, interval: int = 20):
    """Send periodic pings to keep connection alive during long LLM generations"""
    try:
        while True:
            await asyncio.sleep(interval)
            try:
                await websocket.send_text("")  # Send empty string as keepalive
            except:
                break
    except asyncio.CancelledError:
        pass

async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    print(f"✅ Client connected. Total clients: {len(connected_clients)}")

    # Start keepalive task
    keepalive_task = asyncio.create_task(keepalive_ping(websocket))

    try:
        while True:
            user_input = await websocket.receive_text()
            
            # Log control messages
            if user_input in ["[SPEECH_START]", "[SPEECH_END]"] or user_input.startswith("/mode"):
                print(f"📨 Received: {user_input}")

            # Handle speech control messages from text_chat
            if user_input == "[SPEECH_START]":
                # Broadcast to overlay only (not back to sender)
                print("📢 Broadcasting [SPEECH_START] to overlay")
                await broadcast_message("[SPEECH_START]", exclude=websocket)
                continue
            
            if user_input == "[SPEECH_END]":
                # Broadcast to overlay only (not back to sender)
                print("📢 Broadcasting [SPEECH_END] to overlay")
                await broadcast_message("[SPEECH_END]", exclude=websocket)
                continue

            # Handle mode changes
            if user_input.startswith("/mode"):
                set_mode(user_input.split()[-1])
                await websocket.send_text("[MODE CHANGED]")
                await websocket.send_text("[END]")
                continue

            # Regular chat message
            memory.add("user", user_input)
            
            # Show conversation history stats
            summary = memory.get_summary()
            print(f"💬 Conversation: {summary['turns']} turns, ~{summary['estimated_tokens']} tokens")

            memories = fetch_recent_memories()
            system_prompt = build_prompt(get_mode_prompt(), memories)

            messages = [
                {"role": "system", "content": system_prompt},
                *memory.get()
            ]

            full_response = ""

            try:
                async for token in stream_llm_response(messages):
                    full_response += token
                    # Send to the requesting client
                    try:
                        await websocket.send_text(token)
                    except Exception as e:
                        print(f"⚠️ Error sending to requesting client: {e}")
                        break
                    # Broadcast to other clients (like overlay)
                    await broadcast_message(token, exclude=websocket)

                emotion, clean_text = extract_emotion(full_response)

                memory.add("assistant", clean_text)
                save_memory(emotion, clean_text)

                # Send emotion and end marker to all clients
                await websocket.send_text(f"[EMOTION]{emotion}")
                await broadcast_message(f"[EMOTION]{emotion}", exclude=websocket)
                
                await websocket.send_text("[END]")
                await broadcast_message("[END]", exclude=websocket)
                
            except Exception as e:
                print(f"❌ Error during LLM streaming: {e}")
                try:
                    await websocket.send_text("[ERROR]")
                    await websocket.send_text("[END]")
                except:
                    pass

    except WebSocketDisconnect:
        print(f"🔌 Client disconnected gracefully")
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
    finally:
        # Cancel keepalive task
        keepalive_task.cancel()
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        print(f"❌ Client disconnected. Total clients: {len(connected_clients)}")
