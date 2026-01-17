# 🎯 Phase 10C: Task Memory & Habits - Quick Reference

## Overview

**Phase 10C** makes Alisa learn and adapt to your work patterns quietly.

**Key Principle**: "She observes, learns, and adapts - without announcing it"

---

## Quick Start

### No Setup Required!

Phase 10C starts automatically when the backend runs.

```powershell
# Just start the backend as usual
.\scripts\start_backend.ps1
```

Alisa immediately begins:
- ✅ Observing your activities
- ✅ Learning your patterns
- ✅ Adapting her behavior

---

## What Gets Learned

| Category | What's Tracked | How It Adapts |
|----------|---------------|---------------|
| **Work Schedule** | Hours when you're active | Less interruptions during peak hours |
| **Silence Preferences** | When you prefer quiet | Respects your focus times |
| **App Usage** | Which apps for which tasks | Personalized suggestions |
| **Workflows** | Common task sequences | Predictive assistance |

---

## API Reference

### Core Class

```python
from backend.app.task_memory import TaskMemorySystem

# Initialize (auto-created in ws.py)
task_memory = TaskMemorySystem()
```

### Observation Methods

#### observe_activity()

```python
task_memory.observe_activity(
    task_type="coding_python",
    app_name="vscode",
    file_ext=".py"
)
```

**When to call**: Desktop context changes (Phase 10A updates)

**Parameters**:
- `task_type` (str): Type of task (coding_python, browsing, etc.)
- `app_name` (str, optional): Application name
- `file_ext` (str, optional): File extension

**Records**:
- Timestamp by hour → work_schedule
- App preference → app_usage
- Task signature → repeated_tasks
- Task transition → task_sequences

---

#### observe_silence()

```python
task_memory.observe_silence(
    duration_seconds=600  # 10 minutes
)
```

**When to call**: Companion mode triggers after silence

**Parameters**:
- `duration_seconds` (int): How long the silence lasted

**Records**:
- Duration by hour → silence_preferences

**Learn**: Which hours user prefers quiet

---

#### observe_interaction()

```python
task_memory.observe_interaction(
    interaction_type="chat"  # or "voice", "action"
)
```

**When to call**: User sends message, uses voice, requests action

**Parameters**:
- `interaction_type` (str): Type of interaction

**Records**:
- Timestamp by hour → work_schedule

**Learns**: Activity patterns

---

### Analysis Methods

#### analyze_patterns()

```python
patterns = task_memory.analyze_patterns()
```

**Returns**:
```python
{
    "peak_coding_hours": [14, 15, 20],
    "preferred_silence_hours": [9, 10, 22],
    "common_workflows": [
        {
            "sequence": ["coding_python|vscode", "browsing_docs|chrome"],
            "frequency": 5,
            "avg_time_between": 180
        }
    ],
    "app_preferences": {
        "coding_python": "vscode",
        "browsing": "chrome"
    },
    "total_tasks_observed": 47
}
```

**When to call**: Session end (automatic)

**Purpose**: Extract insights from observations

---

#### should_interrupt_now()

```python
should_interrupt, reason = task_memory.should_interrupt_now(
    silence_duration_seconds=600
)
```

**Returns**: `(bool, str)` - (should interrupt, reason)

**Examples**:
```python
(True, "OK to interrupt")
(False, "Quiet hour 9: silence too short")
(False, "Peak hour 14: need longer silence")
```

**When to call**: Before companion speaks (Phase 9B)

**Logic**:
- Checks if current hour is preferred quiet time
- Compares silence to learned patterns
- Considers peak hours

---

#### get_adaptive_suggestions()

```python
suggestions = task_memory.get_adaptive_suggestions()
```

**Returns**:
```python
{
    "current_time_context": {
        "is_peak_hour": True,
        "is_quiet_preferred": False,
        "activity_level": "high"
    },
    "workflow_hints": {
        "likely_next_task": {
            "task": "browsing_docs|chrome",
            "confidence": "medium",
            "expected_in_seconds": 180
        }
    },
    "behavioral_hints": {
        "interruption_style": "minimal",
        "explanation_depth": "brief",
        "timing_preference": "wait_for_pause"
    }
}
```

**When to call**: Before building LLM prompt

**Purpose**: Provide context for adaptive behavior

---

### Storage Methods

#### save_memory()

```python
task_memory.save_memory()
```

**When to call**: Session end (automatic on disconnect)

**Saves to**: `C:\Users\[You]\Documents\Alisa Memory\task_memory.json`

**Contents**: All observations + analyzed patterns

---

#### load_memory()

```python
task_memory.load_memory()
```

**When to call**: System initialization (automatic)

**Loads from**: `C:\Users\[You]\Documents\Alisa Memory\task_memory.json`

**Handles**: Missing files, corrupted data

---

#### end_session()

```python
task_memory.end_session()
```

**When to call**: On disconnect (automatic)

**Does**:
1. Analyzes patterns
2. Saves to disk
3. Logs session stats

---

## Integration Points

### WebSocket (ws.py)

#### Observation Points

```python
# Desktop understanding
async def handle_desktop_understanding(websocket, data):
    if task_memory:
        task_memory.observe_activity(
            data.get('task_type'),
            data.get('app_name'),
            data.get('file_ext')
        )

# Chat messages
async def handle_regular_chat(websocket, data):
    if task_memory:
        task_memory.observe_interaction("chat")

# Disconnect
@websocket_router.on_disconnect
async def websocket_disconnect(websocket: WebSocket):
    if task_memory:
        task_memory.end_session()
```

#### Companion Override

```python
async def idle_thought_loop():
    # Check learned patterns before speaking
    if task_memory:
        should_interrupt, reason = task_memory.should_interrupt_now(silence_seconds)
        if not should_interrupt:
            logging.info(f"🎯 Phase 10C override: {reason}")
            continue
```

#### Adaptive Prompts

```python
async def handle_regular_chat(websocket, data):
    # Get suggestions
    adaptive_suggestions = {}
    if task_memory:
        adaptive_suggestions = task_memory.get_adaptive_suggestions()
    
    # Build enhanced prompt
    system_prompt = build_prompt(
        mode=current_mode,
        task_insights=adaptive_suggestions
    )
```

---

### Prompt Builder (prompt.py)

```python
def build_prompt(
    mode: str = "assistant",
    has_vision: bool = False,
    task_insights: Dict[str, Any] = None
) -> str:
    # ... base prompt ...
    
    if task_insights:
        # Add learned pattern hints
        habit_text = "\n\n## 🎯 Learned Patterns & Context\n"
        
        time_ctx = task_insights.get("current_time_context", {})
        if time_ctx.get("is_peak_hour"):
            habit_text += "- User is typically most productive at this time\n"
        
        # ... more hints ...
        
        system_prompt += habit_text
    
    return system_prompt
```

---

## Data Structures

### Work Schedule

```python
work_schedule: Dict[str, List[float]]

# Example
{
    "14": [1705502100.5, 1705502400.2],
    "15": [1705503200.1]
}
```

**Key**: Hour (0-23)  
**Value**: List of timestamps  
**Purpose**: Track activity by hour  

---

### App Usage

```python
app_usage: Dict[str, Dict[str, int]]

# Example
{
    "coding_python": {"vscode": 15, "notepad": 2},
    "browsing": {"chrome": 20, "edge": 3}
}
```

**Key**: Task type  
**Value**: {app_name: count}  
**Purpose**: Learn app preferences  

---

### Silence Preferences

```python
silence_preferences: Dict[str, List[int]]

# Example
{
    "9": [45, 50, 42],
    "22": [30, 35]
}
```

**Key**: Hour (0-23)  
**Value**: List of silence durations (minutes)  
**Purpose**: Learn focus patterns  

---

### Task Sequences

```python
task_sequences: List[Dict]

# Example
[
    {
        "from": "coding_python|vscode",
        "to": "browsing_docs|chrome",
        "time_between_seconds": 180,
        "timestamp": 1705502400
    }
]
```

**Purpose**: Learn workflows  

---

## Common Patterns

### Pattern 1: Adding Observation

```python
# In your WebSocket handler
if task_memory:
    task_memory.observe_activity("new_task_type", "app_name")
```

### Pattern 2: Checking Before Interrupting

```python
# In companion logic
if task_memory:
    should, reason = task_memory.should_interrupt_now(silence_duration)
    if not should:
        # Skip interruption
        return
```

### Pattern 3: Getting Context

```python
# Before LLM call
suggestions = {}
if task_memory:
    suggestions = task_memory.get_adaptive_suggestions()

system_prompt = build_prompt(task_insights=suggestions)
```

---

## File Locations

| Purpose | Path |
|---------|------|
| **Core System** | `backend/app/task_memory.py` |
| **Integration** | `backend/app/ws.py` |
| **Prompt Enhancement** | `backend/app/prompt.py` |
| **Stored Memory** | `Documents/Alisa Memory/task_memory.json` |
| **Tests** | `scripts/test_phase10c.py` |

---

## Logs & Debugging

### Log Messages

```
🎯 Phase 10C: Activity observed - coding_python in vscode
🎯 Phase 10C: Silence recorded - 600s at hour 14
🎯 Phase 10C override: Quiet hour 9: silence too short
💾 Phase 10C: Saving learned patterns...
   📊 Session stats: 12 interactions
   🎯 Total tasks observed: 47
```

### Viewing Memory File

```powershell
# Open in editor
notepad "$env:USERPROFILE\Documents\Alisa Memory\task_memory.json"

# Or use Python
python -m json.tool "$env:USERPROFILE\Documents\Alisa Memory\task_memory.json"
```

---

## Testing

### Run Tests

```powershell
python scripts/test_phase10c.py
```

### Manual Testing

```python
from backend.app.task_memory import TaskMemorySystem

# Create instance
tm = TaskMemorySystem()

# Observe some activities
tm.observe_activity("coding_python", "vscode", ".py")
tm.observe_activity("browsing", "chrome")
tm.observe_silence(600)

# Analyze
patterns = tm.analyze_patterns()
print(patterns)

# Check interrupt logic
should, reason = tm.should_interrupt_now(300)
print(f"Should interrupt: {should}, Reason: {reason}")

# Get suggestions
suggestions = tm.get_adaptive_suggestions()
print(suggestions)
```

---

## Quick Troubleshooting

### Memory not saving?

**Check**:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

Look for: `💾 Phase 10C: Saving learned patterns...`

---

### Patterns not applying?

**Verify** patterns exist:
```python
tm = TaskMemorySystem()
tm.load_memory()
print(tm.patterns)
```

---

### Observations not recording?

**Check** task_memory is initialized:
```python
# In ws.py
task_memory = TaskMemorySystem()
print(f"Task memory: {task_memory}")
```

---

## Performance

| Metric | Value |
|--------|-------|
| **CPU Impact** | <0.5% |
| **RAM Usage** | ~5MB |
| **Disk Space** | ~50KB |
| **Save Time** | 100-200ms |
| **Load Time** | 50-100ms |

**Impact**: Negligible

---

## Privacy

✅ **All local** - No cloud storage  
✅ **User-controlled** - You own the file  
✅ **Transparent** - Plain JSON format  
✅ **Deletable** - Remove anytime  

**Not tracked**:
- ❌ File contents
- ❌ Typed text
- ❌ URLs
- ❌ Personal data

---

## Examples

### Example 1: Peak Hour Detection

```python
# After a week of coding at 2-3pm daily
patterns = tm.analyze_patterns()
# Result: {"peak_coding_hours": [14, 15]}

# Now at 2:30pm
should, reason = tm.should_interrupt_now(300)  # 5 min silence
# Result: (False, "Peak hour 14: need longer silence")
```

---

### Example 2: Quiet Hours

```python
# After several mornings of 45+ min focus
patterns = tm.analyze_patterns()
# Result: {"preferred_silence_hours": [9, 10]}

# At 9:15am, 10 min silence
should, reason = tm.should_interrupt_now(600)
# Result: (False, "Quiet hour 9: silence too short")
```

---

### Example 3: Workflow Learning

```python
# After coding → browsing docs 5 times
patterns = tm.analyze_patterns()
# Result: {
#   "common_workflows": [
#     {"sequence": ["coding→browsing"], "frequency": 5}
#   ]
# }

# While coding
suggestions = tm.get_adaptive_suggestions()
# Result: {
#   "workflow_hints": {
#     "likely_next_task": "browsing_docs|chrome"
#   }
# }
```

---

## Cheat Sheet

### Initialization
```python
from backend.app.task_memory import TaskMemorySystem
tm = TaskMemorySystem()
```

### Observation
```python
tm.observe_activity("task", "app", ".ext")
tm.observe_silence(seconds)
tm.observe_interaction("type")
```

### Analysis
```python
patterns = tm.analyze_patterns()
should, why = tm.should_interrupt_now(seconds)
hints = tm.get_adaptive_suggestions()
```

### Storage
```python
tm.save_memory()
tm.load_memory()
tm.end_session()
```

---

## Summary

Phase 10C adds **quiet learning** to Alisa:

✅ Observes work patterns  
✅ Learns preferences  
✅ Adapts behavior  
✅ Respects your rhythm  
✅ Gets smarter over time  

**All automatic. All local. All yours.**

---

**Quick Reference Complete**

For full details, see:
- `PHASE_10C_SUMMARY.md` - Overview
- `docs/PHASE_10C_IMPLEMENTATION.md` - Deep dive
- `docs/PHASE_10C_VISUAL_GUIDE.md` - Diagrams
