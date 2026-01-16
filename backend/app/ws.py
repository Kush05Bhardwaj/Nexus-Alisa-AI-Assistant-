from fastapi import WebSocket, WebSocketDisconnect
from .llm_client import stream_llm_response
from .memory import MemoryBuffer
from .memory_long import save_memory, fetch_recent_memories
from .modes import set_mode, get_mode_prompt
from .emotion import extract_emotion
from .prompt import build_prompt
from typing import List
import asyncio
import time
import random

memory = MemoryBuffer()

# Store all connected WebSocket clients
connected_clients: List[WebSocket] = []

# Track last user activity for idle thought engine
last_user_activity = time.time()
idle_thought_active = False  # Prevent multiple idle thoughts at once

# Vision state tracking
vision_state = {
    "presence": "unknown",  # "present", "absent", "unknown"
    "attention": "unknown",  # "focused", "distracted", "unknown"
    "emotion": "neutral",
    "last_update": 0,
    "state_duration": 0,  # How long in current state (seconds)
    "last_reaction": 0,  # Last time Alisa reacted to vision (to avoid spam)
}

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

async def trigger_idle_response():
    """Generate and broadcast an idle thought from Alisa"""
    global idle_thought_active
    
    if idle_thought_active:
        print("⏸️ Idle thought already in progress, skipping")
        return
    
    if len(connected_clients) == 0:
        print("⏸️ No clients connected, skipping idle thought")
        return
    
    idle_thought_active = True
    print("💭 Generating idle thought...")
    
    try:
        memories = fetch_recent_memories()
        
        # Build context with idle hint
        idle_context = (
            "The user has been quiet for a while. "
            "If it feels natural, say something subtle, light, or observational. "
            "Do NOT ask direct questions. "
            "Keep it short. "
            "Silence is acceptable."
        )
        
        system_prompt = build_prompt(
            get_mode_prompt(), 
            memories, 
            vision_context=idle_context
        )
        
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        full_response = ""
        
        async for token in stream_llm_response(messages):
            full_response += token
            # Broadcast to ALL clients
            await broadcast_message(token, exclude=None)
        
        emotion, clean_text = extract_emotion(full_response)
        memory.add("assistant", clean_text)
        save_memory(emotion, clean_text)
        
        # Send emotion and end markers
        await broadcast_message(f"[EMOTION]{emotion}", exclude=None)
        await broadcast_message("[END]", exclude=None)
        
        print(f"✅ Idle thought sent: {clean_text[:60]}...")
        
    except Exception as e:
        print(f"❌ Error generating idle thought: {e}")
        import traceback
        traceback.print_exc()
    finally:
        idle_thought_active = False

async def idle_thought_loop():
    """Background task that occasionally triggers idle thoughts"""
    global last_user_activity
    
    print("🧠 Idle thought engine started")
    
    while True:
        await asyncio.sleep(30)  # Check every 30 seconds
        
        idle_time = time.time() - last_user_activity
        
        # Only consider idle after 90 seconds
        if idle_time < 90:
            continue
        
        # Probability gate: 25% chance when idle
        # This is CRITICAL to prevent spam
        if random.random() > 0.25:
            continue
        
        # Additional check: don't spam if already spoke recently
        if idle_thought_active:
            continue
        
        # Trigger the idle thought
        await trigger_idle_response()

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
    global last_user_activity
    
    await websocket.accept()
    connected_clients.append(websocket)
    print(f"✅ Client connected. Total clients: {len(connected_clients)}")

    # Start keepalive task
    keepalive_task = asyncio.create_task(keepalive_ping(websocket))

    try:
        while True:
            user_input = await websocket.receive_text()
            
            # Update last activity timestamp for REAL user messages only
            # (not control messages or vision updates)
            if not user_input.startswith("[") and not user_input.startswith("/"):
                last_user_activity = time.time()
            
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

            # Handle vision system input - user presence/emotion detection
            if user_input.startswith("[VISION_FACE]"):
                state = user_input.replace("[VISION_FACE]", "")
                current_time = time.time()
                
                # Update vision state
                old_presence = vision_state["presence"]
                old_attention = vision_state["attention"]
                
                if state == "present":
                    vision_state["presence"] = "present"
                    print(f"👁️ Vision: User present (was: {old_presence})")
                elif state == "absent":
                    vision_state["presence"] = "absent"
                    print(f"👁️ Vision: User absent (was: {old_presence})")
                elif state == "focused":
                    vision_state["attention"] = "focused"
                    print(f"👁️ Vision: User focused (was: {old_attention})")
                elif state == "distracted":
                    vision_state["attention"] = "distracted"
                    print(f"👁️ Vision: User distracted (was: {old_attention})")
                else:
                    vision_state["emotion"] = state
                    print(f"👁️ Vision: User emotion - {state}")
                
                vision_state["last_update"] = current_time
                
                # Intelligent reaction logic: Only react when meaningful
                # Don't spam reactions - wait at least 30 seconds between reactions
                time_since_last_reaction = current_time - vision_state["last_reaction"]
                should_react = False
                reaction_prompt = ""
                
                print(f"🔍 Debug - Time since last reaction: {time_since_last_reaction:.1f}s")
                
                # User returned after being away
                if (old_presence == "absent" or old_presence == "unknown") and vision_state["presence"] == "present":
                    print(f"✅ Detected: User returned (old: {old_presence} → new: present)")
                    if time_since_last_reaction > 30:
                        should_react = True
                        reaction_prompt = "The user just came back to their computer. Welcome them back warmly but casually."
                        vision_state["last_reaction"] = current_time
                        print("💭 Will react: User returned")
                    else:
                        print(f"⏸️ Not reacting yet (need {30 - time_since_last_reaction:.1f}s more)")
                
                # User went away (might comment if they were in middle of conversation)
                elif old_presence == "present" and vision_state["presence"] == "absent":
                    print(f"❌ Detected: User left (memory items: {len(memory.get())})")
                    # Only comment if conversation was recent (within last 2 minutes)
                    if len(memory.get()) > 0 and time_since_last_reaction > 60:
                        should_react = True
                        reaction_prompt = "The user just left. Make a brief, tsundere-style comment about them leaving."
                        vision_state["last_reaction"] = current_time
                        print("💭 Will react: User left during conversation")
                    else:
                        print(f"⏸️ Not reacting (memory: {len(memory.get())}, time: {time_since_last_reaction:.1f}s)")
                
                # User got distracted (looking away for a while)
                elif old_attention == "focused" and vision_state["attention"] == "distracted":
                    print(f"😴 Detected: User distracted (memory items: {len(memory.get())})")
                    # Only comment if they were actively chatting
                    if len(memory.get()) > 2 and time_since_last_reaction > 60:
                        should_react = True
                        reaction_prompt = "The user is looking away while you're talking. Tease them gently or ask if they're listening."
                        vision_state["last_reaction"] = current_time
                        print("💭 Will react: User got distracted")
                    else:
                        print(f"⏸️ Not reacting (memory: {len(memory.get())}, time: {time_since_last_reaction:.1f}s)")
                
                # Generate reaction if needed
                if should_react:
                    print(f"💭 Alisa reacting to vision event...")
                    print(f"📝 Reaction prompt: {reaction_prompt}")
                    
                    memories = fetch_recent_memories()
                    system_prompt = build_prompt(
                        get_mode_prompt(), 
                        memories, 
                        vision_context=reaction_prompt
                    )
                    
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "system", "content": reaction_prompt}  # Direct instruction
                    ]
                    
                    full_response = ""
                    try:
                        async for token in stream_llm_response(messages):
                            full_response += token
                            # Broadcast to ALL clients (text_chat, overlay, etc) - NOT just vision client
                            await broadcast_message(token, exclude=None)
                        
                        emotion, clean_text = extract_emotion(full_response)
                        memory.add("assistant", clean_text)
                        save_memory(emotion, clean_text)
                        
                        # Send emotion and end markers to all clients
                        await broadcast_message(f"[EMOTION]{emotion}", exclude=None)
                        await broadcast_message("[END]", exclude=None)
                        
                        print(f"✅ Vision reaction sent to all clients: {clean_text[:50]}...")
                        
                    except Exception as e:
                        print(f"❌ Error generating vision reaction: {e}")
                        import traceback
                        traceback.print_exc()
                
                continue

            # Handle vision system screen context
            if user_input.startswith("[VISION_SCREEN]"):
                content = user_input.replace("[VISION_SCREEN]", "")
                
                # Parse window and text
                parts = content.split(" | ", 1)
                window = parts[0].strip() if len(parts) > 0 else ""
                text = parts[1].strip() if len(parts) > 1 else ""
                
                # Store screen context in memory (system message)
                screen_context = f"Screen context: {window}"
                if text:
                    screen_context += f" - Content visible: {text[:200]}"
                
                memory.add("system", screen_context)
                print(f"📺 Screen context stored: {window[:50]}...")
                
                # Don't send response, just acknowledge and store
                continue

            # Handle mode changes
            if user_input.startswith("/mode"):
                set_mode(user_input.split()[-1])
                await websocket.send_text("[MODE CHANGED]")
                await websocket.send_text("[END]")
                continue

            # Regular chat message
            memory.add("user", user_input)
            
            # Update activity timestamp for regular chat
            last_user_activity = time.time()
            
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
