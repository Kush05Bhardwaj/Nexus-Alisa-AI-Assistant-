"""
Phase 10A: Desktop Understanding System
Analyzes screen content to understand what user is doing and offer contextual help

Key Features:
- Detects active application
- Identifies file types being viewed
- Recognizes error messages
- Understands user's current task
- Offers help (doesn't force it)
- Lightweight and privacy-aware
"""

import re
import time
from typing import Dict, Optional, List, Tuple
from datetime import datetime

class DesktopUnderstandingSystem:
    """
    Understands desktop context and decides when/how to offer assistance
    
    Philosophy:
    - She UNDERSTANDS but doesn't ACT yet
    - She OFFERS help, doesn't force it
    - Privacy-first, minimal processing
    """
    
    def __init__(self):
        self.last_screen_context = {}
        self.last_analysis_time = 0
        self.current_task = "unknown"
        self.error_detected = False
        self.last_offer_time = 0
        
        # Application categories
        self.app_categories = {
            "code": ["vscode", "visual studio code", "pycharm", "sublime", "atom", "notepad++", "vim"],
            "browser": ["chrome", "firefox", "edge", "brave", "opera"],
            "document": ["word", "excel", "powerpoint", "libreoffice", "notepad"],
            "pdf": ["acrobat", "pdf", "foxit"],
            "terminal": ["powershell", "cmd", "terminal", "git bash", "wsl"],
            "media": ["vlc", "spotify", "youtube", "netflix"],
            "communication": ["discord", "slack", "teams", "zoom", "skype"],
        }
        
        # Error patterns (common error keywords)
        self.error_patterns = [
            r"error",
            r"exception",
            r"failed",
            r"not found",
            r"cannot",
            r"unable to",
            r"invalid",
            r"undefined",
            r"null reference",
            r"syntax error",
            r"traceback",
            r"stack trace",
        ]
        
        # File extension detection
        self.file_extensions = {
            "code": [".py", ".js", ".ts", ".java", ".cpp", ".c", ".cs", ".go", ".rs", ".php"],
            "web": [".html", ".css", ".jsx", ".tsx", ".vue"],
            "data": [".json", ".xml", ".yaml", ".yml", ".csv", ".sql"],
            "doc": [".txt", ".md", ".pdf", ".docx", ".xlsx"],
            "config": [".config", ".ini", ".env", ".toml"],
        }
    
    def analyze_screen_context(
        self,
        window_title: str,
        screen_text: str
    ) -> Dict:
        """
        Analyze screen context to understand what user is doing
        
        Returns:
        {
            "app_type": str,
            "task": str,
            "file_type": str,
            "has_error": bool,
            "error_text": str,
            "should_offer_help": bool,
            "offer_message": str,
            "context_summary": str
        }
        """
        
        analysis = {
            "app_type": "unknown",
            "task": "unknown",
            "file_type": "unknown",
            "has_error": False,
            "error_text": "",
            "should_offer_help": False,
            "offer_message": "",
            "context_summary": "",
            "confidence": 0.0
        }
        
        window_lower = window_title.lower()
        text_lower = screen_text.lower()
        
        # 1. Detect application type
        analysis["app_type"] = self._detect_app_type(window_lower)
        
        # 2. Detect file type
        analysis["file_type"] = self._detect_file_type(window_title, screen_text)
        
        # 3. Detect errors
        error_info = self._detect_errors(screen_text)
        analysis["has_error"] = error_info["has_error"]
        analysis["error_text"] = error_info["error_text"]
        
        # 4. Infer current task
        analysis["task"] = self._infer_task(analysis["app_type"], analysis["file_type"], text_lower)
        
        # 5. Build context summary
        analysis["context_summary"] = self._build_context_summary(analysis)
        
        # 6. Decide if should offer help
        offer_decision = self._should_offer_help(analysis)
        analysis["should_offer_help"] = offer_decision["should_offer"]
        analysis["offer_message"] = offer_decision["message"]
        analysis["confidence"] = offer_decision["confidence"]
        
        # Update state
        self.last_screen_context = analysis
        self.last_analysis_time = time.time()
        self.current_task = analysis["task"]
        self.error_detected = analysis["has_error"]
        
        return analysis
    
    def _detect_app_type(self, window_title: str) -> str:
        """Detect which type of application is active"""
        for category, keywords in self.app_categories.items():
            for keyword in keywords:
                if keyword in window_title:
                    return category
        return "unknown"
    
    def _detect_file_type(self, window_title: str, screen_text: str) -> str:
        """Detect file type from window title or content"""
        combined = window_title + " " + screen_text
        
        for file_type, extensions in self.file_extensions.items():
            for ext in extensions:
                if ext in combined.lower():
                    return file_type
        
        return "unknown"
    
    def _detect_errors(self, screen_text: str) -> Dict:
        """Detect error messages in screen text"""
        text_lower = screen_text.lower()
        
        for pattern in self.error_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                # Extract surrounding context (50 chars before and after)
                start = max(0, match.start() - 50)
                end = min(len(screen_text), match.end() + 50)
                error_context = screen_text[start:end].strip()
                
                return {
                    "has_error": True,
                    "error_text": error_context[:200],  # Limit length
                    "error_type": match.group()
                }
        
        return {"has_error": False, "error_text": "", "error_type": ""}
    
    def _infer_task(self, app_type: str, file_type: str, text_content: str) -> str:
        """Infer what task the user is doing"""
        
        # Coding tasks
        if app_type == "code":
            if file_type == "code":
                if "import" in text_content or "def " in text_content:
                    return "coding_python"
                elif "function" in text_content or "const " in text_content:
                    return "coding_javascript"
                else:
                    return "coding"
            elif file_type == "data":
                return "editing_data"
            elif file_type == "config":
                return "configuration"
        
        # Browser tasks
        elif app_type == "browser":
            if "youtube" in text_content or "video" in text_content:
                return "watching_video"
            elif "github" in text_content:
                return "browsing_code"
            elif "stackoverflow" in text_content or "stack overflow" in text_content:
                return "researching_problem"
            else:
                return "browsing"
        
        # Document tasks
        elif app_type == "document" or app_type == "pdf":
            return "reading_document"
        
        # Terminal tasks
        elif app_type == "terminal":
            if "python" in text_content:
                return "running_python"
            elif "npm" in text_content or "node" in text_content:
                return "running_node"
            elif "git" in text_content:
                return "using_git"
            else:
                return "terminal_work"
        
        return "general_work"
    
    def _build_context_summary(self, analysis: Dict) -> str:
        """Build human-readable context summary"""
        app = analysis["app_type"]
        task = analysis["task"]
        file = analysis["file_type"]
        
        summaries = {
            "coding_python": "User is writing Python code",
            "coding_javascript": "User is writing JavaScript code",
            "coding": "User is coding",
            "editing_data": "User is editing data files",
            "configuration": "User is editing configuration files",
            "browsing": "User is browsing the web",
            "watching_video": "User is watching a video",
            "browsing_code": "User is browsing code on GitHub",
            "researching_problem": "User is researching a problem",
            "reading_document": "User is reading a document",
            "running_python": "User is running Python commands",
            "running_node": "User is running Node.js commands",
            "using_git": "User is using Git",
            "terminal_work": "User is working in terminal",
            "general_work": f"User is working in {app}"
        }
        
        return summaries.get(task, "User is working")
    
    def _should_offer_help(self, analysis: Dict) -> Dict:
        """
        Decide if Alisa should offer help
        
        Criteria:
        - Has error detected
        - Error is recent (not old)
        - Haven't offered help recently (avoid spam)
        - User seems stuck (same error for a while)
        
        Returns: {should_offer: bool, message: str, confidence: float}
        """
        
        current_time = time.time()
        time_since_last_offer = current_time - self.last_offer_time
        
        # Never spam - at least 5 minutes between offers
        if time_since_last_offer < 300:
            return {"should_offer": False, "message": "", "confidence": 0.0}
        
        # ERROR DETECTED
        if analysis["has_error"]:
            # Only offer on fresh errors
            if time_since_last_offer > 300:  # 5 minutes
                self.last_offer_time = current_time
                
                error_snippet = analysis["error_text"][:100]
                
                # Build offer message based on task
                if analysis["task"] == "coding_python":
                    message = f"I see you have a Python error. Want me to help?"
                elif analysis["task"] == "coding":
                    message = f"Looks like there's an error. Need help?"
                elif analysis["task"] == "terminal_work":
                    message = f"Command error? Want me to take a look?"
                else:
                    message = f"I noticed an error. Want me to help?"
                
                return {
                    "should_offer": True,
                    "message": message,
                    "confidence": 0.8,
                    "reason": "error_detected"
                }
        
        # READING PDF FOR A LONG TIME
        if analysis["app_type"] == "pdf" and analysis["task"] == "reading_document":
            # Could offer to summarize, but only if user has been reading for a while
            # Not implemented yet - too intrusive
            pass
        
        # USER RESEARCHING (StackOverflow, GitHub issues)
        if analysis["task"] == "researching_problem":
            # Could offer help if researching same problem for a while
            # Not implemented yet
            pass
        
        # Default: don't offer
        return {"should_offer": False, "message": "", "confidence": 0.0}
    
    def get_context_for_companion(self) -> str:
        """
        Get formatted context for companion system (Phase 9B integration)
        
        Returns context string to add to companion prompts
        """
        if not self.last_screen_context:
            return ""
        
        ctx = self.last_screen_context
        
        parts = []
        
        # Add task context
        if ctx.get("context_summary"):
            parts.append(f"Screen context: {ctx['context_summary']}.")
        
        # Add file type if relevant
        if ctx.get("file_type") and ctx["file_type"] != "unknown":
            parts.append(f"Working with {ctx['file_type']} files.")
        
        # Add error context if present
        if ctx.get("has_error"):
            parts.append(f"There's an error on screen: {ctx['error_text'][:100]}")
        
        # Add offer if appropriate
        if ctx.get("should_offer_help"):
            parts.append(f"\nYou can offer: {ctx['offer_message']}")
        
        return " ".join(parts)
    
    def get_stats(self) -> Dict:
        """Get current desktop understanding stats"""
        return {
            "current_task": self.current_task,
            "error_detected": self.error_detected,
            "last_analysis": time.time() - self.last_analysis_time if self.last_analysis_time > 0 else None,
            "context": self.last_screen_context.get("context_summary", ""),
        }

# Global instance
desktop_understanding = DesktopUnderstandingSystem()
