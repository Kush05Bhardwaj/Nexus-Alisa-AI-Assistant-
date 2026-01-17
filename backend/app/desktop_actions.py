"""
Phase 10B: Desktop Actions System
Allows Alisa to perform actions with explicit user permission

Key Features:
- Open/close apps
- Control browser tabs
- Scroll, click, type
- Read files
- Take notes
- Run scripts

Safety:
- Always requires user confirmation
- Never autonomous without consent
- Explicit command triggers OR confirmation questions
"""

import subprocess
import os
import time
import pyautogui
import psutil
from typing import Dict, Optional, Tuple, List
from datetime import datetime
from pathlib import Path

class DesktopActionsSystem:
    """
    Manages desktop actions with permission-based execution
    
    Safety Model:
    - Action requested → Ask for permission → Execute if granted
    - Explicit commands (e.g., "open chrome") → Execute directly
    - Never autonomous without consent
    """
    
    def __init__(self):
        # Safety settings
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
        pyautogui.PAUSE = 0.5  # Half-second pause between actions
        
        # Action tracking
        self.last_action_time = 0
        self.actions_this_session = []
        self.pending_action = None
        
        # Common applications paths (Windows)
        self.app_paths = {
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
            "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "vscode": r"C:\Users\{username}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            "explorer": "explorer.exe",
            "cmd": "cmd.exe",
            "powershell": "powershell.exe",
        }
        
        # Replace {username} with actual username
        username = os.getenv("USERNAME", "User")
        for app, path in self.app_paths.items():
            self.app_paths[app] = path.replace("{username}", username)
    
    def is_action_safe(self, action_type: str, params: Dict) -> Tuple[bool, str]:
        """
        Validate if an action is safe to execute
        
        Returns: (is_safe: bool, reason: str)
        """
        # Check if too many actions in short time (rate limiting)
        if len(self.actions_this_session) > 20:
            recent = [a for a in self.actions_this_session if time.time() - a["timestamp"] < 60]
            if len(recent) > 10:
                return False, "Too many actions in short time (rate limit)"
        
        # Validate action type
        allowed_actions = [
            "open_app", "close_app", "switch_window",
            "browser_tab", "browser_navigate",
            "type_text", "press_key", "click", "scroll",
            "read_file", "write_note",
            "run_command"
        ]
        
        if action_type not in allowed_actions:
            return False, f"Unknown action type: {action_type}"
        
        # Additional safety checks per action type
        if action_type == "run_command":
            command = params.get("command", "")
            # Blacklist dangerous commands
            dangerous_patterns = ["rm -rf", "del /f", "format", "shutdown", "restart"]
            if any(pattern in command.lower() for pattern in dangerous_patterns):
                return False, "Dangerous command blocked"
        
        if action_type == "write_note":
            path = params.get("path", "")
            # Only allow writing to safe directories
            safe_dirs = [
                os.path.expanduser("~\\Documents"),
                os.path.expanduser("~\\Desktop"),
                os.path.expanduser("~\\Downloads"),
            ]
            path_obj = Path(path).resolve()
            if not any(str(path_obj).startswith(safe_dir) for safe_dir in safe_dirs):
                return False, "Can only write to Documents/Desktop/Downloads"
        
        return True, "Action is safe"
    
    def log_action(self, action_type: str, params: Dict, success: bool):
        """Log executed action"""
        self.actions_this_session.append({
            "timestamp": time.time(),
            "type": action_type,
            "params": params,
            "success": success
        })
        self.last_action_time = time.time()
    
    # ==================== APP MANAGEMENT ====================
    
    def open_app(self, app_name: str, args: List[str] = None) -> Tuple[bool, str]:
        """
        Open an application
        
        Args:
            app_name: Application name (e.g., "chrome", "notepad")
            args: Optional command-line arguments
        
        Returns: (success: bool, message: str)
        """
        try:
            app_name = app_name.lower()
            
            if app_name in self.app_paths:
                path = self.app_paths[app_name]
            else:
                path = app_name  # Try as executable name
            
            # Build command
            cmd = [path]
            if args:
                cmd.extend(args)
            
            # Launch
            subprocess.Popen(cmd, shell=True)
            
            self.log_action("open_app", {"app": app_name, "args": args}, True)
            return True, f"Opened {app_name}"
            
        except Exception as e:
            self.log_action("open_app", {"app": app_name, "args": args}, False)
            return False, f"Failed to open {app_name}: {str(e)}"
    
    def close_app(self, app_name: str) -> Tuple[bool, str]:
        """
        Close an application by name
        
        Args:
            app_name: Application process name
        
        Returns: (success: bool, message: str)
        """
        try:
            closed = False
            app_name = app_name.lower()
            
            # Map common names to process names
            process_names = {
                "chrome": "chrome.exe",
                "firefox": "firefox.exe",
                "edge": "msedge.exe",
                "notepad": "notepad.exe",
                "vscode": "Code.exe",
            }
            
            process_name = process_names.get(app_name, f"{app_name}.exe")
            
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() == process_name.lower():
                    proc.terminate()
                    closed = True
            
            if closed:
                self.log_action("close_app", {"app": app_name}, True)
                return True, f"Closed {app_name}"
            else:
                return False, f"{app_name} is not running"
                
        except Exception as e:
            self.log_action("close_app", {"app": app_name}, False)
            return False, f"Failed to close {app_name}: {str(e)}"
    
    # ==================== BROWSER CONTROL ====================
    
    def browser_new_tab(self) -> Tuple[bool, str]:
        """Open new browser tab (Ctrl+T)"""
        try:
            pyautogui.hotkey('ctrl', 't')
            self.log_action("browser_tab", {"action": "new"}, True)
            return True, "Opened new tab"
        except Exception as e:
            return False, f"Failed: {str(e)}"
    
    def browser_close_tab(self) -> Tuple[bool, str]:
        """Close current browser tab (Ctrl+W)"""
        try:
            pyautogui.hotkey('ctrl', 'w')
            self.log_action("browser_tab", {"action": "close"}, True)
            return True, "Closed tab"
        except Exception as e:
            return False, f"Failed: {str(e)}"
    
    def browser_switch_tab(self, direction: str = "next") -> Tuple[bool, str]:
        """Switch browser tabs"""
        try:
            if direction == "next":
                pyautogui.hotkey('ctrl', 'tab')
            else:
                pyautogui.hotkey('ctrl', 'shift', 'tab')
            
            self.log_action("browser_tab", {"action": "switch", "direction": direction}, True)
            return True, f"Switched to {direction} tab"
        except Exception as e:
            return False, f"Failed: {str(e)}"
    
    def browser_navigate(self, url: str) -> Tuple[bool, str]:
        """Navigate to URL (focus address bar and type)"""
        try:
            # Focus address bar
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.3)
            
            # Type URL
            pyautogui.write(url, interval=0.05)
            pyautogui.press('enter')
            
            self.log_action("browser_navigate", {"url": url}, True)
            return True, f"Navigating to {url}"
        except Exception as e:
            return False, f"Failed: {str(e)}"
    
    # ==================== KEYBOARD/MOUSE ACTIONS ====================
    
    def type_text(self, text: str, interval: float = 0.05) -> Tuple[bool, str]:
        """
        Type text at current cursor position
        
        Args:
            text: Text to type
            interval: Delay between keystrokes (seconds)
        """
        try:
            pyautogui.write(text, interval=interval)
            self.log_action("type_text", {"length": len(text)}, True)
            return True, f"Typed {len(text)} characters"
        except Exception as e:
            return False, f"Failed: {str(e)}"
    
    def press_key(self, key: str, modifiers: List[str] = None) -> Tuple[bool, str]:
        """
        Press a key or key combination
        
        Args:
            key: Main key (e.g., "enter", "a", "f5")
            modifiers: Optional modifier keys (e.g., ["ctrl", "shift"])
        """
        try:
            if modifiers:
                pyautogui.hotkey(*modifiers, key)
            else:
                pyautogui.press(key)
            
            self.log_action("press_key", {"key": key, "modifiers": modifiers}, True)
            return True, f"Pressed {key}"
        except Exception as e:
            return False, f"Failed: {str(e)}"
    
    def click(self, x: int = None, y: int = None, button: str = "left") -> Tuple[bool, str]:
        """
        Click at position or current cursor location
        
        Args:
            x, y: Optional coordinates (None = current position)
            button: "left", "right", or "middle"
        """
        try:
            if x is not None and y is not None:
                pyautogui.click(x, y, button=button)
            else:
                pyautogui.click(button=button)
            
            self.log_action("click", {"x": x, "y": y, "button": button}, True)
            return True, "Clicked"
        except Exception as e:
            return False, f"Failed: {str(e)}"
    
    def scroll(self, amount: int, direction: str = "down") -> Tuple[bool, str]:
        """
        Scroll up or down
        
        Args:
            amount: Number of scroll units
            direction: "up" or "down"
        """
        try:
            scroll_amount = -amount if direction == "down" else amount
            pyautogui.scroll(scroll_amount)
            
            self.log_action("scroll", {"amount": amount, "direction": direction}, True)
            return True, f"Scrolled {direction}"
        except Exception as e:
            return False, f"Failed: {str(e)}"
    
    # ==================== FILE OPERATIONS ====================
    
    def read_file(self, filepath: str, max_lines: int = 50) -> Tuple[bool, str]:
        """
        Read file contents
        
        Args:
            filepath: Path to file
            max_lines: Maximum lines to read
        
        Returns: (success: bool, content_or_error: str)
        """
        try:
            path = Path(filepath).resolve()
            
            if not path.exists():
                return False, f"File not found: {filepath}"
            
            if path.stat().st_size > 1_000_000:  # 1MB limit
                return False, "File too large (>1MB)"
            
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()[:max_lines]
                content = ''.join(lines)
                
                if len(lines) == max_lines:
                    content += f"\n\n[... file truncated, showing first {max_lines} lines ...]"
            
            self.log_action("read_file", {"path": filepath}, True)
            return True, content
            
        except Exception as e:
            self.log_action("read_file", {"path": filepath}, False)
            return False, f"Failed to read file: {str(e)}"
    
    def write_note(self, content: str, filename: str = None) -> Tuple[bool, str]:
        """
        Write a note to Documents folder
        
        Args:
            content: Note content
            filename: Optional filename (auto-generated if None)
        
        Returns: (success: bool, filepath_or_error: str)
        """
        try:
            # Default to Documents/Alisa Notes
            notes_dir = Path.home() / "Documents" / "Alisa Notes"
            notes_dir.mkdir(exist_ok=True)
            
            # Generate filename if not provided
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"note_{timestamp}.txt"
            
            # Ensure .txt extension
            if not filename.endswith('.txt'):
                filename += '.txt'
            
            filepath = notes_dir / filename
            
            # Write note
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.log_action("write_note", {"path": str(filepath)}, True)
            return True, f"Note saved to: {filepath}"
            
        except Exception as e:
            self.log_action("write_note", {"filename": filename}, False)
            return False, f"Failed to write note: {str(e)}"
    
    # ==================== COMMAND EXECUTION ====================
    
    def run_command(self, command: str, shell: bool = True) -> Tuple[bool, str]:
        """
        Run a shell command
        
        Args:
            command: Command to execute
            shell: Execute through shell
        
        Returns: (success: bool, output_or_error: str)
        
        WARNING: Only safe commands allowed
        """
        try:
            # Safety check
            is_safe, reason = self.is_action_safe("run_command", {"command": command})
            if not is_safe:
                return False, f"Command blocked: {reason}"
            
            # Execute with timeout
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            output = result.stdout if result.stdout else result.stderr
            
            self.log_action("run_command", {"command": command}, result.returncode == 0)
            return result.returncode == 0, output[:1000]  # Limit output
            
        except subprocess.TimeoutExpired:
            return False, "Command timed out (10s limit)"
        except Exception as e:
            self.log_action("run_command", {"command": command}, False)
            return False, f"Failed: {str(e)}"
    
    # ==================== WINDOW MANAGEMENT ====================
    
    def switch_window(self, direction: str = "next") -> Tuple[bool, str]:
        """Switch between windows (Alt+Tab)"""
        try:
            if direction == "next":
                pyautogui.hotkey('alt', 'tab')
            else:
                pyautogui.hotkey('alt', 'shift', 'tab')
            
            self.log_action("switch_window", {"direction": direction}, True)
            return True, f"Switched to {direction} window"
        except Exception as e:
            return False, f"Failed: {str(e)}"
    
    def minimize_window(self) -> Tuple[bool, str]:
        """Minimize current window (Win+Down)"""
        try:
            pyautogui.hotkey('win', 'down')
            self.log_action("minimize_window", {}, True)
            return True, "Window minimized"
        except Exception as e:
            return False, f"Failed: {str(e)}"
    
    def maximize_window(self) -> Tuple[bool, str]:
        """Maximize current window (Win+Up)"""
        try:
            pyautogui.hotkey('win', 'up')
            self.log_action("maximize_window", {}, True)
            return True, "Window maximized"
        except Exception as e:
            return False, f"Failed: {str(e)}"
    
    # ==================== HELPER METHODS ====================
    
    def get_action_history(self, limit: int = 10) -> List[Dict]:
        """Get recent action history"""
        return self.actions_this_session[-limit:]
    
    def clear_pending_action(self):
        """Clear any pending action awaiting confirmation"""
        self.pending_action = None
    
    def set_pending_action(self, action_type: str, params: Dict):
        """Store an action pending user confirmation"""
        self.pending_action = {
            "type": action_type,
            "params": params,
            "timestamp": time.time()
        }
    
    def execute_pending_action(self) -> Tuple[bool, str]:
        """Execute the pending action if one exists"""
        if self.pending_action is None:
            return False, "No pending action"
        
        action = self.pending_action
        self.pending_action = None
        
        # Route to appropriate method
        action_type = action["type"]
        params = action["params"]
        
        method_map = {
            "open_app": lambda: self.open_app(**params),
            "close_app": lambda: self.close_app(**params),
            "browser_tab": lambda: self.browser_new_tab() if params.get("action") == "new" else self.browser_close_tab(),
            "browser_navigate": lambda: self.browser_navigate(**params),
            "type_text": lambda: self.type_text(**params),
            "press_key": lambda: self.press_key(**params),
            "scroll": lambda: self.scroll(**params),
            "read_file": lambda: self.read_file(**params),
            "write_note": lambda: self.write_note(**params),
            "run_command": lambda: self.run_command(**params),
        }
        
        if action_type in method_map:
            return method_map[action_type]()
        else:
            return False, f"Unknown action type: {action_type}"
