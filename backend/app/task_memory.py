"""
Phase 10C: Task Memory & Habits System
Alisa learns and remembers your work patterns and adapts quietly

Key Features:
- Remembers how you work
- Learns when you usually code
- Knows when you prefer silence
- Tracks which tasks you repeat
- Adapts behavior quietly without asking

Philosophy:
- She observes and learns
- Never intrusive
- Subtle adaptations
- Respects patterns
- Gets smarter over time
"""

import json
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter

class TaskMemorySystem:
    """
    Learns and remembers user's work patterns and habits
    
    Tracks:
    - Work schedule (when you code, when you're active)
    - Application usage patterns (which apps for which tasks)
    - Preferred silence times (when you don't want interruptions)
    - Repeated tasks (common workflows)
    - Context switches (how you transition between tasks)
    """
    
    def __init__(self, storage_path: str = None):
        # Storage
        if storage_path is None:
            storage_path = Path.home() / "Documents" / "Alisa Memory" / "task_memory.json"
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Memory structures
        self.work_schedule = defaultdict(list)  # hour -> [timestamps]
        self.app_usage = defaultdict(lambda: defaultdict(int))  # task_type -> {app: count}
        self.silence_preferences = defaultdict(list)  # hour -> [duration in minutes]
        self.repeated_tasks = defaultdict(int)  # task_signature -> count
        self.task_sequences = []  # [(task1, task2, time_between)]
        self.context_switches = []  # [(from_context, to_context, timestamp)]
        
        # Observation tracking
        self.current_session = {
            "start_time": time.time(),
            "tasks_observed": [],
            "apps_used": [],
            "interactions": 0,
            "silence_periods": [],
        }
        
        # Pattern analysis cache
        self.patterns = {
            "peak_coding_hours": [],
            "preferred_silence_hours": [],
            "common_workflows": [],
            "app_preferences": {},
            "typical_session_length": 0,
        }
        
        # Load existing memory
        self.load_memory()
    
    def observe_activity(self, activity_type: str, context: Dict):
        """
        Observe and record user activity
        
        Args:
            activity_type: Type of activity (coding, browsing, chatting, etc.)
            context: Additional context (app, file_type, task, etc.)
        """
        timestamp = time.time()
        current_hour = datetime.fromtimestamp(timestamp).hour
        
        # Record work schedule
        self.work_schedule[current_hour].append(timestamp)
        
        # Record app usage
        if "app" in context:
            app = context["app"]
            self.app_usage[activity_type][app] += 1
        
        # Track tasks
        task_signature = self._create_task_signature(activity_type, context)
        self.repeated_tasks[task_signature] += 1
        
        # Add to current session
        self.current_session["tasks_observed"].append({
            "type": activity_type,
            "context": context,
            "timestamp": timestamp
        })
        
        if "app" in context and context["app"] not in self.current_session["apps_used"]:
            self.current_session["apps_used"].append(context["app"])
        
        # Detect task sequences
        if len(self.current_session["tasks_observed"]) >= 2:
            prev_task = self.current_session["tasks_observed"][-2]
            curr_task = self.current_session["tasks_observed"][-1]
            time_between = curr_task["timestamp"] - prev_task["timestamp"]
            
            if time_between < 300:  # Within 5 minutes
                self.task_sequences.append((
                    self._create_task_signature(prev_task["type"], prev_task["context"]),
                    self._create_task_signature(curr_task["type"], curr_task["context"]),
                    time_between
                ))
    
    def observe_interaction(self, interaction_type: str = "chat"):
        """Record user interaction with Alisa"""
        self.current_session["interactions"] += 1
    
    def observe_silence(self, duration_minutes: float):
        """
        Record a period of silence (user didn't interact)
        
        Args:
            duration_minutes: How long the silence lasted
        """
        current_hour = datetime.now().hour
        self.silence_preferences[current_hour].append(duration_minutes)
        
        self.current_session["silence_periods"].append({
            "duration": duration_minutes,
            "hour": current_hour,
            "timestamp": time.time()
        })
    
    def observe_context_switch(self, from_context: str, to_context: str):
        """
        Record when user switches between different contexts
        
        Args:
            from_context: Previous context (e.g., "coding_python")
            to_context: New context (e.g., "browsing_docs")
        """
        self.context_switches.append((from_context, to_context, time.time()))
    
    def _create_task_signature(self, activity_type: str, context: Dict) -> str:
        """Create a unique signature for a task"""
        parts = [activity_type]
        
        if "app" in context:
            parts.append(context["app"])
        if "file_type" in context:
            parts.append(context["file_type"])
        if "task" in context:
            parts.append(context["task"])
        
        return "|".join(parts)
    
    def analyze_patterns(self):
        """
        Analyze collected data to extract patterns
        Called periodically to update pattern cache
        """
        # Analyze peak coding hours
        self.patterns["peak_coding_hours"] = self._find_peak_hours()
        
        # Analyze preferred silence hours
        self.patterns["preferred_silence_hours"] = self._find_silence_preferences()
        
        # Analyze common workflows
        self.patterns["common_workflows"] = self._find_common_workflows()
        
        # Analyze app preferences
        self.patterns["app_preferences"] = self._find_app_preferences()
        
        # Calculate typical session length
        self.patterns["typical_session_length"] = self._calculate_session_length()
    
    def _find_peak_hours(self) -> List[int]:
        """Find hours when user is most active"""
        if not self.work_schedule:
            return []
        
        # Count activities per hour
        hour_counts = {hour: len(timestamps) for hour, timestamps in self.work_schedule.items()}
        
        if not hour_counts:
            return []
        
        # Find top 3 hours
        sorted_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)
        peak_hours = [hour for hour, count in sorted_hours[:3]]
        
        return sorted(peak_hours)
    
    def _find_silence_preferences(self) -> List[int]:
        """Find hours when user prefers longer silence"""
        if not self.silence_preferences:
            return []
        
        # Calculate average silence duration per hour
        avg_silence = {}
        for hour, durations in self.silence_preferences.items():
            if durations:
                avg_silence[hour] = sum(durations) / len(durations)
        
        if not avg_silence:
            return []
        
        # Find hours with longest average silence (top 3)
        sorted_hours = sorted(avg_silence.items(), key=lambda x: x[1], reverse=True)
        silence_hours = [hour for hour, avg in sorted_hours[:3]]
        
        return sorted(silence_hours)
    
    def _find_common_workflows(self) -> List[Tuple[str, str, int]]:
        """Find commonly repeated task sequences"""
        if not self.task_sequences:
            return []
        
        # Count sequence occurrences
        sequence_counts = Counter()
        for task1, task2, time_between in self.task_sequences:
            sequence_counts[(task1, task2)] += 1
        
        # Get top 5 sequences
        common = []
        for (task1, task2), count in sequence_counts.most_common(5):
            if count >= 2:  # At least observed twice
                # Calculate average time between
                times = [tb for t1, t2, tb in self.task_sequences if t1 == task1 and t2 == task2]
                avg_time = sum(times) / len(times) if times else 0
                common.append((task1, task2, int(avg_time)))
        
        return common
    
    def _find_app_preferences(self) -> Dict[str, str]:
        """Find preferred app for each activity type"""
        preferences = {}
        
        for activity_type, app_counts in self.app_usage.items():
            if app_counts:
                # Find most used app for this activity
                preferred_app = max(app_counts.items(), key=lambda x: x[1])[0]
                preferences[activity_type] = preferred_app
        
        return preferences
    
    def _calculate_session_length(self) -> int:
        """Calculate typical session length in minutes"""
        # Look at historical sessions (would need to track session ends)
        # For now, use current session as baseline
        current_length = (time.time() - self.current_session["start_time"]) / 60
        return int(current_length)
    
    def should_interrupt_now(self) -> Tuple[bool, str]:
        """
        Determine if now is a good time to interrupt based on learned patterns
        
        Returns: (should_interrupt: bool, reason: str)
        """
        current_hour = datetime.now().hour
        
        # Check if current hour is a preferred silence hour
        if current_hour in self.patterns["preferred_silence_hours"]:
            return False, "user_prefers_silence_at_this_hour"
        
        # Check if it's peak working hour (user is focused)
        if current_hour in self.patterns["peak_coding_hours"]:
            # During peak hours, be extra cautious
            if self.current_session["interactions"] < 2:
                return False, "peak_working_hour_minimal_interaction"
        
        # Check recent silence duration
        recent_silence = self._get_recent_silence_duration()
        if recent_silence < 2:  # Less than 2 minutes of silence
            return False, "user_was_just_active"
        
        return True, "good_time_to_interact"
    
    def _get_recent_silence_duration(self) -> float:
        """Get minutes since last interaction"""
        if not self.current_session["tasks_observed"]:
            return (time.time() - self.current_session["start_time"]) / 60
        
        last_activity = self.current_session["tasks_observed"][-1]["timestamp"]
        return (time.time() - last_activity) / 60
    
    def get_adaptive_suggestions(self) -> Dict:
        """
        Get suggestions for Alisa's behavior based on learned patterns
        
        Returns: Dict with behavioral suggestions
        """
        current_hour = datetime.now().hour
        
        suggestions = {
            "be_quiet": False,
            "expect_coding": False,
            "common_apps": [],
            "likely_next_task": None,
            "suggested_silence_duration": 5,  # minutes
        }
        
        # Silence suggestion
        if current_hour in self.patterns["preferred_silence_hours"]:
            suggestions["be_quiet"] = True
            
            # Calculate suggested silence duration for this hour
            if current_hour in self.silence_preferences:
                durations = self.silence_preferences[current_hour]
                if durations:
                    suggestions["suggested_silence_duration"] = int(sum(durations) / len(durations))
        
        # Coding expectation
        if current_hour in self.patterns["peak_coding_hours"]:
            suggestions["expect_coding"] = True
        
        # Common apps for current context
        if self.current_session["tasks_observed"]:
            last_task = self.current_session["tasks_observed"][-1]
            activity_type = last_task["type"]
            
            if activity_type in self.patterns["app_preferences"]:
                suggestions["common_apps"] = [self.patterns["app_preferences"][activity_type]]
        
        # Predict likely next task based on workflows
        if self.current_session["tasks_observed"]:
            current_task_sig = self._create_task_signature(
                self.current_session["tasks_observed"][-1]["type"],
                self.current_session["tasks_observed"][-1]["context"]
            )
            
            # Find workflows starting with current task
            for task1, task2, avg_time in self.patterns["common_workflows"]:
                if task1 == current_task_sig:
                    suggestions["likely_next_task"] = {
                        "task": task2,
                        "expected_in_seconds": avg_time
                    }
                    break
        
        return suggestions
    
    def get_habit_insights(self) -> Dict:
        """
        Get insights about learned habits for display/debugging
        
        Returns: Human-readable insights
        """
        insights = {
            "peak_hours": self.patterns["peak_coding_hours"],
            "quiet_hours": self.patterns["preferred_silence_hours"],
            "total_tasks_observed": sum(self.repeated_tasks.values()),
            "unique_tasks": len(self.repeated_tasks),
            "common_workflows": len(self.patterns["common_workflows"]),
            "app_preferences": self.patterns["app_preferences"],
            "session_interactions": self.current_session["interactions"],
        }
        
        return insights
    
    def save_memory(self):
        """Persist learned patterns to disk"""
        try:
            data = {
                "version": "1.0",
                "last_saved": time.time(),
                "work_schedule": {str(k): v for k, v in self.work_schedule.items()},
                "app_usage": {k: dict(v) for k, v in self.app_usage.items()},
                "silence_preferences": {str(k): v for k, v in self.silence_preferences.items()},
                "repeated_tasks": dict(self.repeated_tasks),
                "task_sequences": self.task_sequences,
                "context_switches": self.context_switches,
                "patterns": self.patterns,
            }
            
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Failed to save task memory: {e}")
            return False
    
    def load_memory(self):
        """Load learned patterns from disk"""
        try:
            if not self.storage_path.exists():
                return False
            
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
            
            # Restore data structures
            self.work_schedule = defaultdict(list, {int(k): v for k, v in data.get("work_schedule", {}).items()})
            
            app_usage_data = data.get("app_usage", {})
            self.app_usage = defaultdict(lambda: defaultdict(int))
            for activity, apps in app_usage_data.items():
                self.app_usage[activity] = defaultdict(int, apps)
            
            self.silence_preferences = defaultdict(list, {int(k): v for k, v in data.get("silence_preferences", {}).items()})
            self.repeated_tasks = defaultdict(int, data.get("repeated_tasks", {}))
            self.task_sequences = data.get("task_sequences", [])
            self.context_switches = data.get("context_switches", [])
            self.patterns = data.get("patterns", self.patterns)
            
            return True
        except Exception as e:
            print(f"Failed to load task memory: {e}")
            return False
    
    def end_session(self):
        """Mark end of current session and save"""
        # Analyze patterns before saving
        self.analyze_patterns()
        
        # Save to disk
        self.save_memory()
        
        # Reset current session
        self.current_session = {
            "start_time": time.time(),
            "tasks_observed": [],
            "apps_used": [],
            "interactions": 0,
            "silence_periods": [],
        }

# Global instance
task_memory = TaskMemorySystem()
