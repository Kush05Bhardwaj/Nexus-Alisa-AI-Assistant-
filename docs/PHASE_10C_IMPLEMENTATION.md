# 🎯 Phase 10C: Task Memory & Habits - Full Implementation Guide

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Core Components](#core-components)
3. [Data Structures](#data-structures)
4. [Learning Mechanisms](#learning-mechanisms)
5. [Integration Points](#integration-points)
6. [Adaptive Behaviors](#adaptive-behaviors)
7. [Storage System](#storage-system)
8. [Testing](#testing)

---

## Architecture Overview

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 10C: LEARNING LAYER                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ OBSERVATION  │ → │   ANALYSIS   │ → │  ADAPTATION  │  │
│  │              │    │              │    │              │  │
│  │ • Activities │    │ • Patterns   │    │ • Timing     │  │
│  │ • Silences   │    │ • Workflows  │    │ • Prompts    │  │
│  │ • Switches   │    │ • Prefs      │    │ • Behavior   │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         ↓                    ↓                    ↓         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            PERSISTENT MEMORY (JSON)                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
┌─────────────────────────────────────────────────────────────┐
│               INTEGRATION WITH EXISTING PHASES               │
├─────────────────────────────────────────────────────────────┤
│  Phase 9B          Phase 10A         Phase 10B             │
│  (Companion)       (Understanding)   (Actions)              │
│       ↓                  ↓                ↓                 │
│  Uses patterns    Provides context   Gets preferences      │
└─────────────────────────────────────────────────────────────┘
```

### Flow Diagram

```
User Activity → Desktop Understanding (10A)
                       ↓
              ┌─────────────────┐
              │  Task Memory    │ ← WebSocket Events
              │  System (10C)   │
              └─────────────────┘
                       ↓
              ┌─────────────────┐
              │  Observations   │
              │  • activity()   │
              │  • silence()    │
              │  • interaction()│
              └─────────────────┘
                       ↓
              ┌─────────────────┐
              │  Pattern        │
              │  Analysis       │
              └─────────────────┘
                       ↓
              ┌─────────────────┐
              │  Adaptive       │
              │  Suggestions    │
              └─────────────────┘
                       ↓
         ┌────────────┴────────────┐
         ↓                         ↓
   Companion (9B)            Prompt Builder
   Interrupt Logic           (Enhanced Context)
```

---

## Core Components

### 1. TaskMemorySystem Class

**Location**: `backend/app/task_memory.py`

**Purpose**: Central learning system that observes, analyzes, and adapts

**Key Methods**:

#### Observation Methods

```python
def observe_activity(self, task_type: str, app_name: str = None, file_ext: str = None)
```
**Purpose**: Records a new activity observation  
**Called**: When desktop context changes (Phase 10A)  
**Records**: Task type, app, file extension, timestamp  
**Updates**: work_schedule, app_usage, task_sequences  

```python
def observe_silence(self, duration_seconds: int)
```
**Purpose**: Records a silence period  
**Called**: When companion mode triggers after silence  
**Records**: Hour and duration of silence  
**Updates**: silence_preferences  

```python
def observe_interaction(self, interaction_type: str)
```
**Purpose**: Records user interaction (chat, voice, etc.)  
**Called**: On each user message  
**Records**: Timestamp by hour  
**Updates**: work_schedule  

#### Analysis Methods

```python
def analyze_patterns(self) -> Dict[str, Any]
```
**Purpose**: Extracts insights from observations  
**Called**: On session end  
**Returns**: Dictionary of learned patterns  
**Analyzes**:
- Peak working hours (top 3 most active)
- Preferred silence hours (longest average silences)
- Common workflows (repeated task sequences)
- App preferences (most used app per task)

```python
def should_interrupt_now(self, silence_duration_seconds: int) -> tuple[bool, str]
```
**Purpose**: Decides if interruption is appropriate  
**Called**: By Phase 9B companion logic  
**Returns**: (should_interrupt: bool, reason: str)  
**Checks**:
- Current hour in preferred silence hours
- Recent silence too short for this hour
- Peak hours require extra caution

```python
def get_adaptive_suggestions(self) -> Dict[str, Any]
```
**Purpose**: Provides behavioral hints for LLM  
**Called**: When building system prompt  
**Returns**: Dictionary with timing, workflow, preference hints  
**Used**: To subtly adjust Alisa's behavior  

#### Storage Methods

```python
def save_memory(self)
```
**Purpose**: Persists learned patterns to disk  
**Called**: On session end (disconnect)  
**Saves**: All observations + analyzed patterns  
**Location**: `Documents/Alisa Memory/task_memory.json`  

```python
def load_memory(self)
```
**Purpose**: Restores learned patterns from disk  
**Called**: On system initialization  
**Loads**: Previous observations and patterns  
**Handles**: Missing files, corrupted data  

### 2. Data Tracking

#### Work Schedule

```python
self.work_schedule: Dict[str, List[float]] = defaultdict(list)
```

**Structure**:
```json
{
  "14": [1705502100.5, 1705502400.2, ...],
  "15": [1705503200.1, 1705503500.8, ...],
  "20": [1705515600.3, 1705515900.7, ...]
}
```

**Purpose**: Track activity by hour  
**Usage**: Identify peak working hours  

#### App Usage

```python
self.app_usage: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
```

**Structure**:
```json
{
  "coding_python": {
    "vscode": 15,
    "notepad": 2
  },
  "browsing": {
    "chrome": 20,
    "edge": 3
  }
}
```

**Purpose**: Track app preferences per task  
**Usage**: Personalized suggestions  

#### Silence Preferences

```python
self.silence_preferences: Dict[str, List[int]] = defaultdict(list)
```

**Structure**:
```json
{
  "9": [45, 50, 42, 48],
  "22": [30, 35, 28, 33]
}
```

**Purpose**: Track silence durations by hour  
**Usage**: Learn when user prefers focus  

#### Repeated Tasks

```python
self.repeated_tasks: Dict[str, int] = defaultdict(int)
```

**Structure**:
```json
{
  "coding_python|vscode|.py": 15,
  "browsing_docs|chrome": 12,
  "testing|browser|.html": 8
}
```

**Purpose**: Track task frequency  
**Usage**: Identify common workflows  

#### Task Sequences

```python
self.task_sequences: List[Dict[str, Any]] = []
```

**Structure**:
```json
[
  {
    "from": "coding_python|vscode",
    "to": "browsing_docs|chrome",
    "time_between_seconds": 180,
    "timestamp": 1705502400
  },
  ...
]
```

**Purpose**: Track task transitions  
**Usage**: Learn workflows, predict next steps  

---

## Data Structures

### Pattern Dictionary

Returned by `analyze_patterns()`:

```python
{
  "peak_coding_hours": [14, 15, 20],  # Top 3 active hours
  "preferred_silence_hours": [9, 10, 22],  # Hours with long silences
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
  "total_tasks_observed": 47,
  "sessions_tracked": 12
}
```

### Adaptive Suggestions

Returned by `get_adaptive_suggestions()`:

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
    "interruption_style": "minimal",  # or "normal", "proactive"
    "explanation_depth": "brief",  # or "detailed"
    "timing_preference": "wait_for_pause"
  }
}
```

---

## Learning Mechanisms

### 1. Peak Hours Detection

**Algorithm**:
```python
# Count activities per hour
hour_counts = Counter()
for hour, timestamps in work_schedule.items():
    hour_counts[hour] = len(timestamps)

# Get top 3 most active hours
peak_hours = [h for h, _ in hour_counts.most_common(3)]
```

**Example**:
```
Observations:
  Hour 14: 25 activities
  Hour 15: 22 activities
  Hour 20: 18 activities
  Hour 10: 5 activities
  
Result: peak_coding_hours = [14, 15, 20]
```

### 2. Silence Preference Learning

**Algorithm**:
```python
# Calculate average silence duration per hour
silence_avgs = {}
for hour, durations in silence_preferences.items():
    if durations:
        silence_avgs[hour] = sum(durations) / len(durations)

# Sort by average duration (longest = preferred quiet)
sorted_hours = sorted(silence_avgs.items(), key=lambda x: x[1], reverse=True)
preferred_quiet_hours = [int(h) for h, _ in sorted_hours[:3]]
```

**Example**:
```
Observations:
  Hour 9:  [45, 50, 42] → avg 45.7 mins
  Hour 22: [30, 35, 28] → avg 31.0 mins
  Hour 14: [5, 8, 10]   → avg 7.7 mins
  
Result: preferred_silence_hours = [9, 22] (long silences)
```

### 3. Workflow Detection

**Algorithm**:
```python
# Group task sequences by (from, to) pair
workflow_freq = defaultdict(list)
for seq in task_sequences:
    key = (seq['from'], seq['to'])
    workflow_freq[key].append(seq['time_between_seconds'])

# Filter for repeated sequences (≥3 times)
common_workflows = []
for (from_task, to_task), times in workflow_freq.items():
    if len(times) >= 3:
        common_workflows.append({
            'sequence': [from_task, to_task],
            'frequency': len(times),
            'avg_time_between': sum(times) / len(times)
        })
```

**Example**:
```
Observations:
  coding_python → browsing_docs (5 times, avg 180s)
  browsing_docs → coding_python (4 times, avg 120s)
  testing → debugging (2 times) ← not included (< 3)
  
Result: common_workflows = [
  {sequence: [coding→browsing], frequency: 5, avg_time: 180}
]
```

### 4. App Preference Learning

**Algorithm**:
```python
# For each task type, find most used app
app_prefs = {}
for task_type, apps in app_usage.items():
    if apps:
        most_used_app = max(apps.items(), key=lambda x: x[1])[0]
        app_prefs[task_type] = most_used_app
```

**Example**:
```
Observations:
  coding_python: {vscode: 15, notepad: 2}
  browsing: {chrome: 20, edge: 3}
  
Result: app_preferences = {
  coding_python: "vscode",
  browsing: "chrome"
}
```

---

## Integration Points

### 1. WebSocket Observations (ws.py)

#### Desktop Understanding Handler

```python
async def handle_desktop_understanding(websocket, data):
    # ... existing code ...
    
    # Phase 10C: Observe desktop activity
    if task_memory:
        task_type = data.get('task_type', 'unknown')
        app_name = data.get('app_name')
        file_ext = data.get('file_ext')
        task_memory.observe_activity(task_type, app_name, file_ext)
```

**Purpose**: Learn from desktop context  
**Frequency**: Every desktop understanding update (~5 seconds)  

#### Idle Thought Loop

```python
async def idle_thought_loop():
    # ... existing silence tracking ...
    
    # Phase 10C: Check learned patterns before interrupting
    if task_memory:
        should_interrupt, reason = task_memory.should_interrupt_now(silence_seconds)
        if not should_interrupt:
            logging.info(f"🎯 Phase 10C override: {reason}")
            continue  # Skip companion speech
    
    # ... proceed with companion mode ...
```

**Purpose**: Respect learned preferences  
**Frequency**: Every silence check  

#### Chat Handler

```python
async def handle_regular_chat(websocket, data):
    # Phase 10C: Observe interaction
    if task_memory:
        task_memory.observe_interaction("chat")
    
    # Get adaptive suggestions
    adaptive_suggestions = {}
    if task_memory:
        adaptive_suggestions = task_memory.get_adaptive_suggestions()
    
    # Build prompt with task insights
    system_prompt = build_prompt(
        mode=current_mode,
        has_vision=False,
        task_insights=adaptive_suggestions
    )
    
    # ... rest of chat handling ...
```

**Purpose**: Learn from interactions + adapt behavior  
**Frequency**: Every chat message  

#### Disconnect Handler

```python
@websocket_router.on_disconnect
async def websocket_disconnect(websocket: WebSocket):
    # ... existing cleanup ...
    
    # Phase 10C: Save learned patterns
    if task_memory:
        logging.info("💾 Phase 10C: Saving learned patterns...")
        task_memory.end_session()
```

**Purpose**: Persist learned data  
**Frequency**: On session end  

### 2. Prompt Enhancement (prompt.py)

```python
def build_prompt(
    mode: str = "assistant",
    has_vision: bool = False,
    task_insights: Dict[str, Any] = None
) -> str:
    # ... base prompt construction ...
    
    # Add learned habit insights
    if task_insights:
        habit_text = "\n\n## 🎯 Learned Patterns & Context\n"
        
        # Time context
        time_ctx = task_insights.get("current_time_context", {})
        if time_ctx.get("is_peak_hour"):
            habit_text += "- User is typically most productive at this time (peak hour)\n"
        if time_ctx.get("is_quiet_preferred"):
            habit_text += "- User typically prefers minimal interruptions at this hour\n"
        
        # Workflow hints
        workflow = task_insights.get("workflow_hints", {})
        if workflow.get("likely_next_task"):
            next_task = workflow["likely_next_task"]
            habit_text += f"- Based on patterns, user may transition to {next_task['task']} soon\n"
        
        # Behavioral adjustments
        behavior = task_insights.get("behavioral_hints", {})
        if behavior.get("interruption_style") == "minimal":
            habit_text += "- Keep responses brief and focused\n"
        
        system_prompt += habit_text
    
    return system_prompt
```

**Purpose**: Subtly adjust LLM behavior based on learned patterns  
**Effect**: More personalized, context-aware responses  

---

## Adaptive Behaviors

### 1. Interrupt Timing

**Logic** (in `should_interrupt_now()`):

```python
current_hour = datetime.now().hour

# Check if current hour is preferred quiet time
if current_hour in self.patterns.get('preferred_silence_hours', []):
    # Require longer silence before interrupting
    avg_silence = self._get_avg_silence_for_hour(current_hour)
    if silence_duration < avg_silence * 0.8:  # 80% of usual
        return False, f"Quiet hour {current_hour}: silence too short"

# Check if peak coding hour
if current_hour in self.patterns.get('peak_coding_hours', []):
    # Be extra cautious during productive time
    if silence_duration < 900:  # 15 minutes minimum
        return False, f"Peak hour {current_hour}: need longer silence"

return True, "OK to interrupt"
```

**Result**: Less interruption during:
- Hours with historically long silences
- Peak productivity hours
- Recent context switches

### 2. LLM Context Enhancement

**Subtle Hints** (added to system prompt):

```
Before learning:
  [Standard prompt]

After learning (example):
  [Standard prompt]
  
  ## 🎯 Learned Patterns & Context
  - User is typically most productive at this time (peak hour)
  - User typically prefers minimal interruptions at this hour
  - Based on patterns, user may transition to browsing_docs soon
  - Keep responses brief and focused
```

**Effect**: Alisa naturally adjusts without announcing it

### 3. Workflow Predictions

**Example Flow**:

```
1. User: coding_python in VS Code (2 minutes)
2. Phase 10C: "Workflow coding→browsing usually happens in ~3 min"
3. Phase 10A: Detects error in code
4. Alisa: "Need help? Or want me to open the docs?" ← contextual!
```

**Implementation** (future enhancement for Phase 10B):

```python
# In desktop actions logic
adaptive_hints = task_memory.get_adaptive_suggestions()
likely_next = adaptive_hints.get('workflow_hints', {}).get('likely_next_task')

if likely_next and error_detected:
    # Proactively suggest next step in workflow
    return f"Want me to open {likely_next['task']}?"
```

---

## Storage System

### File Structure

**Location**:
```
C:\Users\[YourName]\Documents\Alisa Memory\task_memory.json
```

**Format**:
```json
{
  "version": "1.0",
  "last_saved": 1705503022.456,
  "work_schedule": {
    "14": [1705502100.5, 1705502400.2],
    "15": [1705503200.1]
  },
  "app_usage": {
    "coding_python": {"vscode": 15}
  },
  "silence_preferences": {
    "9": [45, 50]
  },
  "repeated_tasks": {
    "coding_python|vscode|.py": 15
  },
  "task_sequences": [
    {
      "from": "coding_python|vscode",
      "to": "browsing_docs|chrome",
      "time_between_seconds": 180,
      "timestamp": 1705502400
    }
  ],
  "patterns": {
    "peak_coding_hours": [14, 15, 20],
    "preferred_silence_hours": [9, 22],
    "common_workflows": [...],
    "app_preferences": {...},
    "total_tasks_observed": 47
  }
}
```

### Persistence Logic

#### Save (on disconnect)

```python
def save_memory(self):
    data = {
        'version': '1.0',
        'last_saved': time.time(),
        'work_schedule': dict(self.work_schedule),
        'app_usage': {k: dict(v) for k, v in self.app_usage.items()},
        'silence_preferences': dict(self.silence_preferences),
        'repeated_tasks': dict(self.repeated_tasks),
        'task_sequences': self.task_sequences,
        'patterns': self.patterns
    }
    
    memory_dir.mkdir(parents=True, exist_ok=True)
    with open(memory_file, 'w') as f:
        json.dump(data, f, indent=2)
```

#### Load (on startup)

```python
def load_memory(self):
    if not memory_file.exists():
        return
    
    try:
        with open(memory_file, 'r') as f:
            data = json.load(f)
        
        self.work_schedule = defaultdict(list, data.get('work_schedule', {}))
        self.app_usage = defaultdict(lambda: defaultdict(int))
        for task, apps in data.get('app_usage', {}).items():
            self.app_usage[task] = defaultdict(int, apps)
        # ... restore other fields ...
        self.patterns = data.get('patterns', {})
        
    except Exception as e:
        logging.error(f"Failed to load task memory: {e}")
```

---

## Testing

### Test File: `scripts/test_phase10c.py`

#### Test 1: Observation Recording

```python
def test_observation_recording():
    tm = TaskMemorySystem()
    
    # Observe activities
    tm.observe_activity("coding_python", "vscode", ".py")
    tm.observe_activity("coding_python", "vscode", ".py")
    tm.observe_activity("browsing", "chrome")
    
    # Check recordings
    assert "coding_python" in tm.app_usage
    assert tm.app_usage["coding_python"]["vscode"] == 2
    assert len(tm.task_sequences) > 0
```

#### Test 2: Pattern Analysis

```python
def test_pattern_analysis():
    tm = TaskMemorySystem()
    
    # Simulate a week of work
    for day in range(7):
        for hour in [14, 15, 20]:  # Peak hours
            for _ in range(3):
                tm.observe_activity("coding_python", "vscode")
    
    # Analyze
    patterns = tm.analyze_patterns()
    
    assert 14 in patterns["peak_coding_hours"]
    assert 15 in patterns["peak_coding_hours"]
    assert 20 in patterns["peak_coding_hours"]
```

#### Test 3: Silence Learning

```python
def test_silence_learning():
    tm = TaskMemorySystem()
    
    # Simulate morning quiet hours
    for _ in range(5):
        # Hour 9: long silences
        tm.silence_preferences["9"].append(45)
        
    # Hour 14: short silences
    for _ in range(5):
        tm.silence_preferences["14"].append(5)
    
    patterns = tm.analyze_patterns()
    assert 9 in patterns["preferred_silence_hours"]
    assert 14 not in patterns["preferred_silence_hours"]
```

#### Test 4: Interrupt Logic

```python
def test_interrupt_logic():
    tm = TaskMemorySystem()
    
    # Set up patterns
    tm.patterns = {
        "preferred_silence_hours": [9, 22],
        "peak_coding_hours": [14, 15]
    }
    tm.silence_preferences["9"] = [45, 50]  # avg ~47 mins
    
    # Test: 9am, 10 min silence
    with patch('backend.app.task_memory.datetime') as mock_dt:
        mock_dt.now.return_value.hour = 9
        should, reason = tm.should_interrupt_now(600)  # 10 mins
        assert not should  # Too short for quiet hour
    
    # Test: 9am, 40 min silence
    with patch('backend.app.task_memory.datetime') as mock_dt:
        mock_dt.now.return_value.hour = 9
        should, reason = tm.should_interrupt_now(2400)  # 40 mins
        assert should  # Long enough
```

#### Test 5: Persistence

```python
def test_persistence():
    tm1 = TaskMemorySystem()
    
    # Add some data
    tm1.observe_activity("coding_python", "vscode")
    tm1.observe_silence(600)
    tm1.analyze_patterns()
    tm1.save_memory()
    
    # Load in new instance
    tm2 = TaskMemorySystem()
    tm2.load_memory()
    
    assert tm2.app_usage["coding_python"]["vscode"] > 0
    assert len(tm2.silence_preferences) > 0
```

### Running Tests

```powershell
# From project root
python scripts/test_phase10c.py
```

**Expected Output**:
```
✅ Test 1: Observation recording - PASS
✅ Test 2: Pattern analysis - PASS
✅ Test 3: Silence learning - PASS
✅ Test 4: Interrupt logic - PASS
✅ Test 5: Persistence - PASS

All Phase 10C tests passed!
```

---

## Summary

Phase 10C implements a complete learning system:

✅ **Observation**: Tracks activities, silences, interactions  
✅ **Analysis**: Extracts meaningful patterns  
✅ **Adaptation**: Adjusts behavior based on learning  
✅ **Integration**: Works seamlessly with Phases 9B, 10A, 10B  
✅ **Persistence**: Saves and loads learned habits  
✅ **Privacy**: All local, user-controlled  

**Result**: Alisa gets smarter and more personalized over time.

---

**The final evolution is complete.**
