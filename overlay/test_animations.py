"""
Test script to manually trigger avatar animations
"""
import avatar_window

def test_emotions():
    """Test all emotions with proper delays"""
    print("\n=== Testing Emotions ===")
    emotions = ["neutral", "happy", "teasing", "serious", "calm", "sad"]
    
    for i, emotion in enumerate(emotions):
        delay = i * 2000  # 2 seconds between each emotion
        avatar_window.root.after(delay, lambda e=emotion: [
            print(f"\nSwitching to: {e}"),
            avatar_window.set_emotion(e)
        ])

def test_talking():
    """Test talking animation for longer duration"""
    print("\n=== Testing Talking ===")
    avatar_window.root.after(0, avatar_window.start_talking)
    # Stop after 5 seconds (enough time to see multiple mouth movements)
    avatar_window.root.after(5000, avatar_window.stop_talking)

def run_tests():
    """Run all tests after window is shown"""
    # Start with emotions test
    avatar_window.root.after(1000, test_emotions)
    # Start talking test after emotions (6 emotions * 2 sec = 12 sec + 2 sec buffer)
    avatar_window.root.after(14000, test_talking)

if __name__ == "__main__":
    print("Starting avatar window with tests...")
    avatar_window.initialize()
    
    # Bind events
    avatar_window.canvas.bind("<Button-1>", avatar_window.start_drag)
    avatar_window.canvas.bind("<B1-Motion>", avatar_window.on_drag)
    avatar_window.canvas.bind("<Button-3>", lambda e: avatar_window.root.quit())
    
    # Start blink animation
    avatar_window.root.after(3000, avatar_window.animate_blink)
    
    # Schedule tests
    run_tests()
    
    # Run
    print("Window running - tests will run automatically")
    print("Right-click to close")
    avatar_window.root.mainloop()
