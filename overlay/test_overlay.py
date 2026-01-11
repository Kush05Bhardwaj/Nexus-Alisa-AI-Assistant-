"""
Test script for avatar overlay
Tests the UI and animations without requiring backend
"""
from avatar_window import root, start_talking, stop_talking, run_avatar

def run_test():
    print("=" * 60)
    print("🧪 Avatar Overlay Test")
    print("=" * 60)
    print("Testing animations:")
    print("  • Blinking (automatic)")
    print("  • Talking animation (starts in 2 seconds)")
    print("=" * 60)
    
    # Test sequence
    root.after(2000, lambda: print("▶️  Starting talking animation..."))
    root.after(2000, start_talking)
    
    root.after(5000, lambda: print("⏸️  Stopping talking animation..."))
    root.after(5000, stop_talking)
    
    root.after(7000, lambda: print("▶️  Starting talking again..."))
    root.after(7000, start_talking)
    
    root.after(10000, lambda: print("⏸️  Stopping talking..."))
    root.after(10000, stop_talking)
    
    root.after(12000, lambda: print("✅ Test complete! Close the window or press Ctrl+C"))

if __name__ == "__main__":
    run_test()
    run_avatar()
