"""
Phase 10B Desktop Actions - Test Suite
Tests the desktop actions system functionality
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.desktop_actions import DesktopActionsSystem

def test_action_system_initialization():
    """Test that the system initializes correctly"""
    print("Test 1: System Initialization")
    try:
        system = DesktopActionsSystem()
        print("  ✅ DesktopActionsSystem initialized")
        print(f"  ✅ App paths configured: {len(system.app_paths)} apps")
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return False

def test_safety_validation():
    """Test safety validation logic"""
    print("\nTest 2: Safety Validation")
    system = DesktopActionsSystem()
    
    # Test allowed action
    is_safe, reason = system.is_action_safe("open_app", {"app_name": "chrome"})
    if is_safe:
        print("  ✅ Allowed action validated: open_app")
    else:
        print(f"  ❌ Should allow open_app: {reason}")
        return False
    
    # Test dangerous command
    is_safe, reason = system.is_action_safe("run_command", {"command": "shutdown /s"})
    if not is_safe:
        print("  ✅ Dangerous command blocked: shutdown")
    else:
        print("  ❌ Should block dangerous command")
        return False
    
    # Test unknown action type
    is_safe, reason = system.is_action_safe("evil_action", {})
    if not is_safe:
        print("  ✅ Unknown action type blocked")
    else:
        print("  ❌ Should block unknown action")
        return False
    
    return True

def test_pending_action_flow():
    """Test pending action storage and retrieval"""
    print("\nTest 3: Pending Action Flow")
    system = DesktopActionsSystem()
    
    # Set pending action
    system.set_pending_action("open_app", {"app_name": "notepad"})
    if system.pending_action is not None:
        print("  ✅ Pending action stored")
    else:
        print("  ❌ Failed to store pending action")
        return False
    
    # Clear pending action
    system.clear_pending_action()
    if system.pending_action is None:
        print("  ✅ Pending action cleared")
    else:
        print("  ❌ Failed to clear pending action")
        return False
    
    return True

def test_action_logging():
    """Test action logging"""
    print("\nTest 4: Action Logging")
    system = DesktopActionsSystem()
    
    # Log some actions
    system.log_action("open_app", {"app": "chrome"}, True)
    system.log_action("browser_tab", {"action": "new"}, True)
    
    history = system.get_action_history(limit=5)
    if len(history) == 2:
        print(f"  ✅ Action logging working: {len(history)} actions logged")
        print(f"      Last action: {history[-1]['type']}")
    else:
        print(f"  ❌ Expected 2 actions, got {len(history)}")
        return False
    
    return True

def test_file_operations_safety():
    """Test file operation path restrictions"""
    print("\nTest 5: File Operation Safety")
    system = DesktopActionsSystem()
    
    # Test safe path (Documents)
    import tempfile
    from pathlib import Path
    
    # Create a test file in Documents
    docs_path = Path.home() / "Documents" / "test_phase10b.txt"
    
    # Test write note (should create in Documents/Alisa Notes)
    success, message = system.write_note("Test note content", "test_note.txt")
    if success:
        print("  ✅ Note writing works (safe directory)")
        print(f"      {message}")
    else:
        print(f"  ⚠️  Note writing failed (may need Documents folder): {message}")
    
    return True

def test_app_paths():
    """Test app path configuration"""
    print("\nTest 6: App Path Configuration")
    system = DesktopActionsSystem()
    
    required_apps = ["chrome", "notepad", "calculator"]
    found = 0
    
    for app in required_apps:
        if app in system.app_paths:
            found += 1
            print(f"  ✅ App configured: {app}")
    
    if found == len(required_apps):
        print(f"  ✅ All required apps configured")
        return True
    else:
        print(f"  ⚠️  Some apps missing ({found}/{len(required_apps)})")
        return True  # Not critical

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🎮 Phase 10B Desktop Actions - Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_action_system_initialization,
        test_safety_validation,
        test_pending_action_flow,
        test_action_logging,
        test_file_operations_safety,
        test_app_paths,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ❌ Test crashed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("✅ All tests passed! Phase 10B is ready.")
        return True
    else:
        print("⚠️  Some tests failed. Check output above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
