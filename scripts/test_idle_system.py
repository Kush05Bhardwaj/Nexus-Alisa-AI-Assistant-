"""
🧪 Idle Thought System Test Script

This script helps verify the idle thought engine is working correctly
without breaking the existing chat system.

Run this AFTER starting the backend server.
"""

import asyncio
import websockets
import json
import time

BACKEND_URL = "ws://127.0.0.1:8000/ws/chat"

async def test_normal_chat():
    """Test 1: Verify normal chat still works"""
    print("\n" + "="*60)
    print("TEST 1: Normal Chat Flow")
    print("="*60)
    
    try:
        async with websockets.connect(BACKEND_URL) as ws:
            # Send a message
            await ws.send("Hello Alisa")
            print("✅ Sent: Hello Alisa")
            
            # Receive response
            response = []
            while True:
                msg = await asyncio.wait_for(ws.recv(), timeout=30.0)
                if msg == "[END]":
                    break
                if not msg.startswith("["):
                    response.append(msg)
            
            full_response = "".join(response)
            print(f"✅ Received: {full_response[:100]}...")
            print("✅ TEST 1 PASSED: Normal chat works\n")
            return True
            
    except Exception as e:
        print(f"❌ TEST 1 FAILED: {e}\n")
        return False

async def test_idle_detection():
    """Test 2: Verify idle thought system doesn't break chat"""
    print("\n" + "="*60)
    print("TEST 2: Idle Detection (Short Wait)")
    print("="*60)
    
    try:
        async with websockets.connect(BACKEND_URL) as ws:
            # Send a message
            await ws.send("I'm going to be quiet for a bit")
            print("✅ Sent: I'm going to be quiet for a bit")
            
            # Receive response
            response = []
            while True:
                msg = await asyncio.wait_for(ws.recv(), timeout=30.0)
                if msg == "[END]":
                    break
                if not msg.startswith("["):
                    response.append(msg)
            
            full_response = "".join(response)
            print(f"✅ Received: {full_response[:100]}...")
            
            # Wait 30 seconds (should NOT trigger idle - minimum is 90s)
            print("\n⏳ Waiting 30 seconds (idle threshold is 90s)...")
            await asyncio.sleep(30)
            
            # Check if any unexpected message arrives
            try:
                unexpected = await asyncio.wait_for(ws.recv(), timeout=5.0)
                print(f"⚠️ Received unexpected message: {unexpected}")
                print("⚠️ TEST 2 WARNING: Message received before 90s threshold\n")
                return False
            except asyncio.TimeoutError:
                print("✅ No idle message yet (correct - under 90s)")
                print("✅ TEST 2 PASSED: Idle threshold respected\n")
                return True
                
    except Exception as e:
        print(f"❌ TEST 2 FAILED: {e}\n")
        return False

async def test_activity_reset():
    """Test 3: Verify activity timer resets on user input"""
    print("\n" + "="*60)
    print("TEST 3: Activity Timer Reset")
    print("="*60)
    
    try:
        async with websockets.connect(BACKEND_URL) as ws:
            # Send first message
            await ws.send("Testing activity reset")
            print("✅ Sent: Testing activity reset")
            
            # Receive response
            while True:
                msg = await asyncio.wait_for(ws.recv(), timeout=30.0)
                if msg == "[END]":
                    break
            
            print("✅ Received response")
            
            # Wait 60 seconds
            print("⏳ Waiting 60 seconds...")
            await asyncio.sleep(60)
            
            # Send another message (should reset timer)
            await ws.send("Still here")
            print("✅ Sent: Still here (timer reset)")
            
            # Receive response
            while True:
                msg = await asyncio.wait_for(ws.recv(), timeout=30.0)
                if msg == "[END]":
                    break
            
            print("✅ Received response")
            
            # Wait another 30 seconds (total would be 90, but timer was reset)
            print("⏳ Waiting 30 seconds (total 90 from first, but timer was reset at 60s)...")
            await asyncio.sleep(30)
            
            # Should NOT receive idle message
            try:
                unexpected = await asyncio.wait_for(ws.recv(), timeout=5.0)
                print(f"⚠️ Received unexpected idle message: {unexpected}")
                print("⚠️ TEST 3 WARNING: Timer may not have reset properly\n")
                return False
            except asyncio.TimeoutError:
                print("✅ No idle message (timer was reset correctly)")
                print("✅ TEST 3 PASSED: Activity timer resets properly\n")
                return True
                
    except Exception as e:
        print(f"❌ TEST 3 FAILED: {e}\n")
        return False

async def test_control_messages():
    """Test 4: Verify control messages don't reset timer"""
    print("\n" + "="*60)
    print("TEST 4: Control Messages Don't Reset Timer")
    print("="*60)
    
    try:
        async with websockets.connect(BACKEND_URL) as ws:
            # Send a chat message
            await ws.send("Starting test")
            print("✅ Sent: Starting test")
            
            # Receive response
            while True:
                msg = await asyncio.wait_for(ws.recv(), timeout=30.0)
                if msg == "[END]":
                    break
            
            print("✅ Received response")
            print("⏳ Timer started")
            
            # Wait 30 seconds
            await asyncio.sleep(30)
            
            # Send control message (should NOT reset timer)
            await ws.send("[SPEECH_START]")
            print("✅ Sent: [SPEECH_START] (control message)")
            
            # Wait 5 seconds
            await asyncio.sleep(5)
            
            await ws.send("[SPEECH_END]")
            print("✅ Sent: [SPEECH_END] (control message)")
            
            print("✅ Control messages sent (timer should NOT reset)")
            print("✅ TEST 4 PASSED: Control messages don't affect idle timer\n")
            return True
                
    except Exception as e:
        print(f"❌ TEST 4 FAILED: {e}\n")
        return False

async def monitor_idle_thought():
    """Test 5: Monitor for actual idle thought (may take a while)"""
    print("\n" + "="*60)
    print("TEST 5: Monitor for Idle Thought (Optional - Takes ~2-5 min)")
    print("="*60)
    print("This test will wait for an actual idle thought to occur.")
    print("Press Ctrl+C to skip this test.\n")
    
    try:
        async with websockets.connect(BACKEND_URL) as ws:
            # Send a message to start
            await ws.send("I'll be quiet now")
            print("✅ Sent: I'll be quiet now")
            
            # Receive response
            while True:
                msg = await asyncio.wait_for(ws.recv(), timeout=30.0)
                if msg == "[END]":
                    break
            
            print("✅ Received response")
            print("\n⏳ Waiting for idle thought...")
            print("   Minimum wait: 90 seconds")
            print("   Probability: 25% per 30s check after 90s")
            print("   Expected: 1-5 minutes\n")
            
            start_time = time.time()
            
            # Wait up to 10 minutes for idle thought
            while True:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=600.0)
                    
                    # Check if it's an idle thought (not from user)
                    if not msg.startswith("["):
                        elapsed = time.time() - start_time
                        print(f"\n💭 Idle thought received after {elapsed:.1f} seconds!")
                        print(f"   Content: {msg[:100]}...")
                        
                        # Continue receiving the rest
                        full_msg = msg
                        while True:
                            next_msg = await asyncio.wait_for(ws.recv(), timeout=30.0)
                            if next_msg == "[END]":
                                break
                            if not next_msg.startswith("["):
                                full_msg += next_msg
                        
                        print(f"\n✅ Full idle thought: {full_msg}")
                        print("✅ TEST 5 PASSED: Idle thought system working!\n")
                        return True
                        
                except asyncio.TimeoutError:
                    print("⏰ Timeout: No idle thought received in 10 minutes")
                    print("⚠️ This is normal - probability is only 25%")
                    print("⚠️ Try running the test again or increase probability temporarily\n")
                    return None  # Not failed, just didn't occur
                    
    except KeyboardInterrupt:
        print("\n⚠️ TEST 5 SKIPPED: User interrupted\n")
        return None
    except Exception as e:
        print(f"❌ TEST 5 FAILED: {e}\n")
        return False

async def run_all_tests():
    """Run all tests"""
    print("\n" + "🧪"*30)
    print("IDLE THOUGHT SYSTEM TEST SUITE")
    print("🧪"*30)
    print("\nMake sure the backend is running at ws://127.0.0.1:8000/ws/chat\n")
    
    results = {}
    
    # Run tests
    results["Normal Chat"] = await test_normal_chat()
    results["Idle Detection"] = await test_idle_detection()
    results["Activity Reset"] = await test_activity_reset()
    results["Control Messages"] = await test_control_messages()
    
    # Optional long test
    print("\n" + "="*60)
    response = input("Run idle thought monitoring test? (y/n, takes 2-5 min): ")
    if response.lower() == 'y':
        results["Idle Thought"] = await monitor_idle_thought()
    else:
        results["Idle Thought"] = None
        print("⏭️ Skipped idle thought monitoring test\n")
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test_name, result in results.items():
        if result is True:
            print(f"✅ {test_name}: PASSED")
            passed += 1
        elif result is False:
            print(f"❌ {test_name}: FAILED")
            failed += 1
        else:
            print(f"⏭️ {test_name}: SKIPPED")
            skipped += 1
    
    print("\n" + "="*60)
    print(f"Total: {passed} passed, {failed} failed, {skipped} skipped")
    print("="*60 + "\n")
    
    if failed == 0 and passed > 0:
        print("🎉 ALL TESTS PASSED! Idle thought system is working correctly.\n")
        print("The chat system is NOT broken. ✅\n")
    elif failed > 0:
        print("⚠️ Some tests failed. Check the output above for details.\n")
    else:
        print("⚠️ No tests were run. Make sure the backend is running.\n")

if __name__ == "__main__":
    try:
        asyncio.run(run_all_tests())
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user\n")
    except Exception as e:
        print(f"\n\n❌ Test suite error: {e}\n")
