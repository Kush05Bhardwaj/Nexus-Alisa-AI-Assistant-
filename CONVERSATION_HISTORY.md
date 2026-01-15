# Conversation History System

## Overview
Alisa now has **persistent conversation history** that remembers your conversations even after restarting!

## Features

### ✅ Persistent Storage
- All conversations saved to SQLite database (`alisa_memory.db`)
- Survives server restarts
- Automatic loading on startup

### ✅ Smart Token Management
- Keeps last ~3000 tokens of conversation (roughly 750 words)
- Automatically trims old messages when limit reached
- Always keeps at least 1 complete conversation turn

### ✅ Turn Limit
- Default: 10 conversation turns (20 messages)
- Configurable in `backend/app/memory.py`

## Configuration

Edit `backend/app/ws.py` to change limits:

```python
# Current settings:
memory = MemoryBuffer(
    max_turns=10,      # Maximum conversation turns
    max_tokens=3000,   # Token limit (~750 words)
    session_id="default"
)
```

## Usage

### View Conversation History
```powershell
python view_history.py
```

Show more messages:
```powershell
python view_history.py -n 50
```

### Clear History
```powershell
python view_history.py --clear
```

Or via API:
```powershell
curl http://127.0.0.1:8000/history/clear -X POST
```

### Get History Summary
```powershell
curl http://127.0.0.1:8000/history/summary
```

Returns:
```json
{
  "messages": 14,
  "turns": 7,
  "estimated_tokens": 450,
  "max_tokens": 3000
}
```

## How It Works

1. **User sends message** → Saved to database + added to memory buffer
2. **Alisa responds** → Response saved to database + added to memory buffer
3. **Token check** → If total tokens > 3000, oldest messages removed from memory
4. **Next message** → LLM receives recent conversation context
5. **Server restart** → Last 10 turns automatically loaded from database

## Token Estimation
- Rough estimate: **4 characters ≈ 1 token**
- Actual tokens may vary by ~20%
- System uses conservative estimates to stay safe

## Database Location
- File: `NexaAssistant/alisa_memory.db`
- Two tables:
  - `memory` - Old emotion-based memory system
  - `conversation_history` - New persistent conversation storage

## Benefits

### Before (No History)
```
You: What's your favorite color?
Alisa: Blue!

You: Why do you like that color?
Alisa: (No context - doesn't know what "that color" means)
```

### After (With History)
```
You: What's your favorite color?
Alisa: Blue!

You: Why do you like that color?
Alisa: I like blue because... (remembers talking about blue)
```

## Technical Details

### Memory Buffer
- In-memory cache of recent messages
- Fast access for LLM context
- Automatically synced with database

### Database Schema
```sql
CREATE TABLE conversation_history (
    id INTEGER PRIMARY KEY,
    role TEXT NOT NULL,           -- "user" or "assistant"
    content TEXT NOT NULL,         -- Message content
    timestamp DATETIME,            -- When message was sent
    session_id TEXT DEFAULT "default"  -- For multi-user support
);
```

### Token Limit Logic
1. Add new message to history
2. Calculate total tokens across all messages
3. If over limit, remove oldest messages until under limit
4. Never remove messages if only 1 turn remains

## Future Enhancements
- [ ] Per-user sessions (multiple users with separate histories)
- [ ] Semantic search across old conversations
- [ ] Summary generation for very old conversations
- [ ] Export/import conversation history
- [ ] Analytics (most talked about topics, emotion patterns)
