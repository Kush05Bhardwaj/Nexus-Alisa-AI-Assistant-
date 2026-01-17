from fastapi import WebSocket, WebSocketDisconnect
from .llm_client import stream_llm_response
from .memory import MemoryBuffer
from .memory_long import save_memory, fetch_recent_memories
from .modes import set_mode, get_mode_prompt, current_mode
from .emotion import extract_emotion
from .prompt import build_prompt
from .idle_companion import companion_system  # Phase 9B: Companion mode
from .desktop_actions import DesktopActionsSystem  # Phase 10B: Desktop actions
from .task_memory import task_memory  # Phase 10C: Task memory & habits
from typing import List
import asyncio
import time
import random
import json
import re
from datetime import datetime

memory = MemoryBuffer()

# Phase 10B: Desktop actions system
actions_system = DesktopActionsSystem()

# Phase 10C: Task memory system (learns habits)
# Initialized globally, observes automatically

# Store all connected WebSocket clients
connected_clients: List[WebSocket] = []

# Track last user activity for idle thought engine
last_user_activity = time.time()
idle_thought_active = False  # Prevent multiple idle thoughts at once
last_emotion_expressed = "neutral"  # Track Alisa's last emotion

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
    """
    Generate and broadcast an idle thought from Alisa with Phase 9B companion mode
    Enhanced with natural, spontaneous companion behavior
    """
    global idle_thought_active, last_emotion_expressed
    
    if idle_thought_active:
        print("⏸️ Idle thought already in progress, skipping")
        return
    
    if len(connected_clients) == 0:
        print("⏸️ No clients connected, skipping idle thought")
        return
    
    idle_thought_active = True
    
    try:
        # Phase 9B: Use companion system for context-aware prompting
        silence_duration = companion_system.get_silence_duration()
        context_type = companion_system.get_context_type(vision_state, silence_duration)
        
        print(f"💭 Phase 9B - Companion speech ({context_type}, {silence_duration:.0f}s silence)...")
        
        # Get companion-optimized prompt
        companion_prompt = companion_system.build_companion_prompt(
            context_type=context_type,
            vision_state=vision_state,
            current_mode=current_mode,
            last_emotion=last_emotion_expressed
        )
        
        memories = fetch_recent_memories()
        
        # Build system message with companion context
        system_prompt = build_prompt(
            get_mode_prompt(), 
            memories, 
            vision_context=companion_prompt
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
        
        # GUARD: Detect broken LLM responses in idle thoughts
        valid_emotions = ["teasing", "calm", "serious", "happy", "sad", "neutral", "shy"]
        if clean_text.strip().lower() in valid_emotions or len(clean_text.strip()) < 3:
            print(f"⚠️ Idle thought broken: '{clean_text}' - skipping")
            idle_thought_active = False
            return  # Don't send broken idle thoughts
        
        last_emotion_expressed = emotion  # Track emotion for continuity
        
        # Phase 9B: Mark spontaneous speech
        companion_system.mark_spontaneous_speech()
        
        memory.add("assistant", clean_text)
        save_memory(emotion, clean_text)
        
        # Send emotion and end markers
        await broadcast_message(f"[EMOTION]{emotion}", exclude=None)
        await broadcast_message("[END]", exclude=None)
        
        print(f"✅ Companion speech ({emotion}): {clean_text[:60]}...")
        
    except Exception as e:
        print(f"❌ Error generating idle thought: {e}")
        import traceback
        traceback.print_exc()
    finally:
        idle_thought_active = False

async def idle_thought_loop():
    """
    Background task that triggers idle thoughts using Phase 9B companion system
    Natural, rare, spontaneous behavior - companion mode
    """
    global last_user_activity
    
    print("🧠 Phase 9B - Companion System initialized")
    print("🎯 Phase 10C - Task Memory & Habits initialized")
    print("   Alisa will speak spontaneously when it feels natural")
    print("   Speech is RARE - companion, not chatbot")
    print("   Alisa learns your work patterns and adapts quietly")
    
    while True:
        await asyncio.sleep(30)  # Check every 30 seconds
        
        # Phase 10C: Observe silence period
        silence_duration = (time.time() - last_user_activity) / 60  # minutes
        task_memory.observe_silence(silence_duration)
        
        # Phase 10C: Check if now is a good time based on learned patterns
        should_interrupt, reason_10c = task_memory.should_interrupt_now()
        
        # Phase 9B: Use companion system to decide if should speak
        should_speak, reason = companion_system.should_speak_spontaneously(
            vision_state=vision_state,
            current_mode=current_mode,
            is_idle_thought_active=idle_thought_active
        )
        
        # Phase 10C: Override if learned patterns say not to interrupt
        if should_speak and not should_interrupt:
            print(f"🔇 Phase 10C override: {reason_10c} (would have spoken: {reason})")
            should_speak = False
        
        if should_speak:
            # Get companion stats for logging
            stats = companion_system.get_stats()
            print(f"🎯 Phase 9B trigger: {reason}")
            print(f"✅ Phase 10C permits interrupt")
            print(f"   Stats: silence={stats['silence_duration']:.0f}s, "
                  f"companion_mode={stats['companion_mode_active']}, "
                  f"conversations={stats['conversation_count']}")
            
            await trigger_idle_response()
        else:
            # Debug: log why we're not speaking (only occasionally to avoid spam)
            if random.random() < 0.1:  # 10% of checks
                stats = companion_system.get_stats()
                print(f"🔇 Phase 9B silent: {reason} "
                      f"(silence={stats['silence_duration']:.0f}s, "
                      f"category={stats['silence_category']})")

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
    global last_user_activity, last_emotion_expressed
    
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
                        
                        # GUARD: Detect broken LLM responses
                        valid_emotions = ["teasing", "calm", "serious", "happy", "sad", "neutral", "shy"]
                        if clean_text.strip().lower() in valid_emotions or len(clean_text.strip()) < 3:
                            print(f"⚠️ Vision reaction broken: '{clean_text}' - using fallback")
                            fallbacks = {
                                "teasing": "Hmph.",
                                "shy": "...",
                                "calm": "Mhm.",
                                "serious": "...",
                                "happy": "Heh.",
                                "sad": "...",
                                "neutral": "..."
                            }
                            clean_text = fallbacks.get(emotion, "...")
                        
                        last_emotion_expressed = emotion  # Track for idle continuity
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

            # Phase 10A: Handle desktop understanding messages
            if user_input.startswith("[VISION_DESKTOP]"):
                content = user_input.replace("[VISION_DESKTOP]", "")
                
                # Parse: task|app|file_type|has_error|offer|window|text
                parts = content.split("|", 6)
                
                if len(parts) >= 7:
                    task = parts[0].strip()
                    app_type = parts[1].strip()
                    file_type = parts[2].strip()
                    has_error = parts[3].strip() == "True"
                    offer_message = parts[4].strip()
                    window = parts[5].strip()
                    text = parts[6].strip() if len(parts) > 6 else ""
                    
                    # Phase 10C: Observe activity and learn patterns
                    task_memory.observe_activity(task, {
                        "app": app_type,
                        "file_type": file_type,
                        "has_error": has_error,
                        "window": window
                    })
                    
                    # Store desktop context
                    desktop_context = f"Desktop: {task}"
                    if app_type != "unknown":
                        desktop_context += f" in {app_type}"
                    if file_type != "unknown":
                        desktop_context += f" ({file_type} file)"
                    
                    memory.add("system", desktop_context)
                    
                    # Log
                    print(f"🖥️  Desktop understanding: {task}")
                    
                    # If error detected and should offer help
                    if has_error and offer_message:
                        print(f"💡 Alisa can offer: {offer_message}")
                        
                        # Generate helpful offer (only if not offered recently)
                        # This is automatic but rare (desktop_understanding handles timing)
                        memories = fetch_recent_memories()
                        
                        offer_prompt = (
                            f"Context: {desktop_context}. "
                            f"An error was detected on the user's screen. "
                            f"Offer: {offer_message} "
                            f"Be natural and brief. Don't be pushy. "
                            f"This is an offer, not a forced conversation."
                        )
                        
                        system_prompt = build_prompt(
                            get_mode_prompt(),
                            memories,
                            vision_context=offer_prompt
                        )
                        
                        messages = [
                            {"role": "system", "content": system_prompt},
                            {"role": "system", "content": offer_prompt}
                        ]
                        
                        full_response = ""
                        try:
                            async for token in stream_llm_response(messages):
                                full_response += token
                                await broadcast_message(token, exclude=None)
                            
                            emotion, clean_text = extract_emotion(full_response)
                            
                            last_emotion_expressed = emotion
                            memory.add("assistant", clean_text)
                            save_memory(emotion, clean_text)
                            
                            await broadcast_message(f"[EMOTION]{emotion}", exclude=None)
                            await broadcast_message("[END]", exclude=None)
                            
                            print(f"✅ Phase 10A offer sent: {clean_text[:50]}...")
                            
                        except Exception as e:
                            print(f"❌ Error generating Phase 10A offer: {e}")
                
                continue

            # Handle vision system screen context (legacy, kept for compatibility)
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
            
            # Phase 10B: Handle explicit action confirmations
            if user_input.strip().lower() in ["yes", "yeah", "yep", "sure", "okay", "ok", "do it"]:
                if actions_system.pending_action:
                    print(f"✅ Phase 10B: User confirmed action")
                    success, message = actions_system.execute_pending_action()
                    
                    # Send result back to user
                    response = f"[TEASING] {message}" if success else f"[SERIOUS] {message}"
                    emotion, clean = extract_emotion(response)
                    
                    await websocket.send_text(clean)
                    await websocket.send_text(f"[EMOTION]{emotion}")
                    await websocket.send_text("[END]")
                    
                    await broadcast_message(clean, exclude=websocket)
                    await broadcast_message(f"[EMOTION]{emotion}", exclude=websocket)
                    await broadcast_message("[END]", exclude=websocket)
                    
                    continue
            
            # Phase 10B: Handle action rejections
            if user_input.strip().lower() in ["no", "nope", "nah", "cancel", "don't"]:
                if actions_system.pending_action:
                    print(f"❌ Phase 10B: User declined action")
                    actions_system.clear_pending_action()
                    
                    response = "[CALM] Alright, no problem."
                    emotion, clean = extract_emotion(response)
                    
                    await websocket.send_text(clean)
                    await websocket.send_text(f"[EMOTION]{emotion}")
                    await websocket.send_text("[END]")
                    
                    await broadcast_message(clean, exclude=websocket)
                    await broadcast_message(f"[EMOTION]{emotion}", exclude=websocket)
                    await broadcast_message("[END]", exclude=websocket)
                    
                    continue
            
            # Phase 10B: Detect action commands in user input
            action_detected = False
            action_type = None
            action_params = {}
            
            user_lower = user_input.lower()
            
            # Pattern matching for various action types
            # Open app patterns
            if re.search(r'\b(open|launch|start)\s+(\w+)', user_lower):
                match = re.search(r'\b(open|launch|start)\s+(\w+)', user_lower)
                app_name = match.group(2)
                action_detected = True
                action_type = "open_app"
                action_params = {"app_name": app_name}
                print(f"🎯 Phase 10B: Detected open app command - {app_name}")
            
            # Close app patterns
            elif re.search(r'\b(close|quit|exit)\s+(\w+)', user_lower):
                match = re.search(r'\b(close|quit|exit)\s+(\w+)', user_lower)
                app_name = match.group(2)
                action_detected = True
                action_type = "close_app"
                action_params = {"app_name": app_name}
                print(f"🎯 Phase 10B: Detected close app command - {app_name}")
            
            # Browser navigation
            elif "go to" in user_lower or "navigate to" in user_lower:
                # Extract URL
                match = re.search(r'(?:go to|navigate to)\s+([a-z0-9.-]+\.[a-z]{2,})', user_lower)
                if match:
                    url = match.group(1)
                    if not url.startswith("http"):
                        url = "https://" + url
                    action_detected = True
                    action_type = "browser_navigate"
                    action_params = {"url": url}
                    print(f"🎯 Phase 10B: Detected browser navigation - {url}")
            
            # New tab
            elif "new tab" in user_lower or "open tab" in user_lower:
                action_detected = True
                action_type = "browser_new_tab"
                action_params = {}
                print(f"🎯 Phase 10B: Detected new tab command")
            
            # Close tab
            elif "close tab" in user_lower:
                action_detected = True
                action_type = "browser_close_tab"
                action_params = {}
                print(f"🎯 Phase 10B: Detected close tab command")
            
            # Scroll
            elif re.search(r'scroll\s+(up|down)', user_lower):
                match = re.search(r'scroll\s+(up|down)', user_lower)
                direction = match.group(1)
                action_detected = True
                action_type = "scroll"
                action_params = {"amount": 3, "direction": direction}
                print(f"🎯 Phase 10B: Detected scroll command - {direction}")
            
            # Type text
            elif user_lower.startswith("type "):
                text = user_input[5:].strip()
                action_detected = True
                action_type = "type_text"
                action_params = {"text": text}
                print(f"🎯 Phase 10B: Detected type command - {text[:30]}")
            
            # Read file
            elif "read file" in user_lower or "show me" in user_lower and "file" in user_lower:
                # Try to extract filename/path
                match = re.search(r'(?:read file|show me)\s+(.+)', user_input)
                if match:
                    filepath = match.group(1).strip('"\'')
                    action_detected = True
                    action_type = "read_file"
                    action_params = {"filepath": filepath}
                    print(f"🎯 Phase 10B: Detected read file command - {filepath}")
            
            # Take note / write note
            elif "take note" in user_lower or "write note" in user_lower or "save note" in user_lower:
                # Extract note content (everything after the command)
                match = re.search(r'(?:take note|write note|save note):?\s+(.+)', user_input, re.IGNORECASE)
                if match:
                    content = match.group(1).strip()
                    action_detected = True
                    action_type = "write_note"
                    action_params = {"content": content}
                    print(f"🎯 Phase 10B: Detected write note command - {content[:30]}")
            
            # If action detected, ask for confirmation (unless it's a direct command)
            if action_detected:
                # Check if it's a direct command (explicit verb at start)
                is_direct_command = user_lower.startswith(("open ", "close ", "launch ", "start ", 
                                                           "type ", "scroll ", "new tab", "close tab"))
                
                if is_direct_command:
                    # Execute directly for explicit commands
                    print(f"⚡ Phase 10B: Direct command, executing immediately")
                    
                    # Execute action
                    success = False
                    message = ""
                    
                    if action_type == "open_app":
                        success, message = actions_system.open_app(**action_params)
                    elif action_type == "close_app":
                        success, message = actions_system.close_app(**action_params)
                    elif action_type == "browser_navigate":
                        success, message = actions_system.browser_navigate(**action_params)
                    elif action_type == "browser_new_tab":
                        success, message = actions_system.browser_new_tab()
                    elif action_type == "browser_close_tab":
                        success, message = actions_system.browser_close_tab()
                    elif action_type == "scroll":
                        success, message = actions_system.scroll(**action_params)
                    elif action_type == "type_text":
                        success, message = actions_system.type_text(**action_params)
                    elif action_type == "read_file":
                        success, message = actions_system.read_file(**action_params)
                    elif action_type == "write_note":
                        success, message = actions_system.write_note(**action_params)
                    
                    # Send result
                    if success:
                        response = f"[TEASING] {message}"
                    else:
                        response = f"[SERIOUS] {message}"
                    
                    emotion, clean = extract_emotion(response)
                    
                    await websocket.send_text(clean)
                    await websocket.send_text(f"[EMOTION]{emotion}")
                    await websocket.send_text("[END]")
                    
                    await broadcast_message(clean, exclude=websocket)
                    await broadcast_message(f"[EMOTION]{emotion}", exclude=websocket)
                    await broadcast_message("[END]", exclude=websocket)
                    
                    continue
                else:
                    # Ask for confirmation via LLM
                    print(f"❓ Phase 10B: Asking for confirmation via LLM")
                    
                    # Store pending action
                    actions_system.set_pending_action(action_type, action_params)
                    
                    # Build confirmation prompt
                    memories = fetch_recent_memories()
                    
                    action_description = {
                        "open_app": f"open {action_params.get('app_name')}",
                        "close_app": f"close {action_params.get('app_name')}",
                        "browser_navigate": f"navigate to {action_params.get('url')}",
                        "browser_new_tab": "open a new browser tab",
                        "browser_close_tab": "close the current tab",
                        "scroll": f"scroll {action_params.get('direction')}",
                        "type_text": f"type: {action_params.get('text', '')[:30]}",
                        "read_file": f"read file: {action_params.get('filepath')}",
                        "write_note": f"save a note"
                    }.get(action_type, "do that")
                    
                    confirmation_prompt = (
                        f"The user wants you to {action_description}. "
                        f"Ask for their confirmation in a natural, casual way. "
                        f"Keep it brief and conversational. Don't be formal."
                    )
                    
                    system_prompt = build_prompt(
                        get_mode_prompt(),
                        memories,
                        vision_context=confirmation_prompt
                    )
                    
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ]
                    
                    full_response = ""
                    try:
                        async for token in stream_llm_response(messages):
                            full_response += token
                            await websocket.send_text(token)
                            await broadcast_message(token, exclude=websocket)
                        
                        emotion, clean_text = extract_emotion(full_response)
                        
                        memory.add("user", user_input)
                        memory.add("assistant", clean_text)
                        save_memory(emotion, clean_text)
                        
                        await websocket.send_text(f"[EMOTION]{emotion}")
                        await websocket.send_text("[END]")
                        
                        await broadcast_message(f"[EMOTION]{emotion}", exclude=websocket)
                        await broadcast_message("[END]", exclude=websocket)
                        
                        print(f"✅ Phase 10B: Confirmation question sent")
                        
                    except Exception as e:
                        print(f"❌ Error generating confirmation: {e}")
                    
                    continue

            # Regular chat message
            memory.add("user", user_input)
            
            # Update activity timestamp for regular chat
            last_user_activity = time.time()
            
            # Phase 9B: Update companion system on user activity
            companion_system.update_user_activity()
            
            # Phase 10C: Observe user interaction
            task_memory.observe_interaction("chat")
            
            # Phase 10C: Get adaptive suggestions based on learned patterns
            adaptive_suggestions = task_memory.get_adaptive_suggestions()
            
            # Show conversation history stats
            summary = memory.get_summary()
            print(f"💬 Conversation: {summary['turns']} turns, ~{summary['estimated_tokens']} tokens")

            memories = fetch_recent_memories()
            system_prompt = build_prompt(get_mode_prompt(), memories, task_insights=adaptive_suggestions)

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
                
                # GUARD: Detect broken LLM responses (just emotion word, no content)
                # Valid emotions that might be the entire response
                valid_emotions = ["teasing", "calm", "serious", "happy", "sad", "neutral", "shy"]
                if clean_text.strip().lower() in valid_emotions or len(clean_text.strip()) < 3:
                    # LLM output was broken (just emotion word or too short)
                    print(f"⚠️ Detected broken response: '{clean_text}' - using fallback")
                    # Use a contextual fallback based on emotion
                    fallbacks = {
                        "teasing": "...",
                        "shy": "Um...",
                        "calm": "Mhm.",
                        "serious": "I see.",
                        "happy": "Heh.",
                        "sad": "...",
                        "neutral": "..."
                    }
                    clean_text = fallbacks.get(emotion, "...")
                
                last_emotion_expressed = emotion  # Track for idle continuity

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
        
        # Phase 10C: Save learned patterns on disconnect
        print("💾 Phase 10C: Saving learned patterns...")
        task_memory.end_session()
        insights = task_memory.get_habit_insights()
        print(f"   📊 Session stats: {insights['session_interactions']} interactions")
        print(f"   🎯 Total tasks observed: {insights['total_tasks_observed']}")
        
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        print(f"❌ Client disconnected. Total clients: {len(connected_clients)}")
