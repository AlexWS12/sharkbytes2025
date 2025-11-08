#!/usr/bin/env python3
"""
Servo Hardware Test Script
Tests PCA9685 servo driver and servo motors
"""

import time
import sys

print("=" * 50)
print("  Servo Hardware Test")
print("=" * 50)
print()

# Test 1: Check if ServoKit library is available
print("Test 1: Checking ServoKit library...")
try:
    from adafruit_servokit import ServoKit
    print("✓ ServoKit library imported successfully")
except ImportError as e:
    print(f"✗ Failed to import ServoKit: {e}")
    print("\nInstall with: pip install adafruit-circuitpython-servokit")
    sys.exit(1)

print()

# Test 2: Initialize PCA9685
print("Test 2: Initializing PCA9685...")
print("   Expected I2C address: 0x40")
print("   Expected I2C bus: 1")
try:
    kit = ServoKit(channels=16, address=0x40, frequency=50)
    print("✓ PCA9685 initialized successfully")
except Exception as e:
    print(f"✗ Failed to initialize PCA9685: {e}")
    print("\nTroubleshooting:")
    print("  1. Check I2C connections (SDA, SCL)")
    print("  2. Verify PCA9685 is powered (VCC, GND)")
    print("  3. Run: sudo i2cdetect -y 1")
    print("     You should see '40' in the output")
    print("  4. Check if you're in the i2c group: groups")
    sys.exit(1)

print()

# Test 3: Configure servo parameters
print("Test 3: Configuring servo parameters...")
PAN_CHANNEL = 2   # Pan servo on channel 2 (X-axis, left/right)
TILT_CHANNEL = 3  # Tilt servo on channel 3 (Y-axis, up/down)

# Servo speed control (lower = slower, smoother)
PAN_SPEED_DELAY = 0.05   # Delay between pan movements (increase if jittery)
TILT_SPEED_DELAY = 0.03  # Delay between tilt movements

try:
    # Set pulse width range (typical for most servos)
    kit.servo[PAN_CHANNEL].set_pulse_width_range(500, 2500)
    kit.servo[TILT_CHANNEL].set_pulse_width_range(500, 2500)
    
    # Optional: Set actuation range if servos don't reach full 180°
    # kit.servo[PAN_CHANNEL].actuation_range = 180
    # kit.servo[TILT_CHANNEL].actuation_range = 180
    
    print(f"✓ Servos configured:")
    print(f"   Pan (X):  Channel {PAN_CHANNEL} (delay: {PAN_SPEED_DELAY}s)")
    print(f"   Tilt (Y): Channel {TILT_CHANNEL} (delay: {TILT_SPEED_DELAY}s)")
    print(f"   Pulse width: 500-2500 μs")
except Exception as e:
    print(f"✗ Failed to configure servos: {e}")
    sys.exit(1)

print()

# Test 4: Center servos
print("Test 4: Centering servos (90°)...")
try:
    kit.servo[PAN_CHANNEL].angle = 90
    time.sleep(PAN_SPEED_DELAY)
    kit.servo[TILT_CHANNEL].angle = 90
    time.sleep(TILT_SPEED_DELAY)
    time.sleep(1)
    print("✓ Servos centered")
    print("   Both servos should be at their center position")
except Exception as e:
    print(f"✗ Failed to center servos: {e}")
    sys.exit(1)

print()

# Test 5: Movement test
print("Test 5: Movement test...")
print("   The servos will move through a sequence")
print("   Watch for smooth motion and listen for any unusual sounds")
print("   Pay attention to the X-axis (pan) servo for jitter")
print()

try:
    movements = [
        ("Center (90°, 90°)", 90, 90),
        ("Pan Left (45°, 90°)", 45, 90),
        ("Pan Right (135°, 90°)", 135, 90),
        ("Center (90°, 90°)", 90, 90),
        ("Tilt Up (90°, 45°)", 90, 45),
        ("Tilt Down (90°, 135°)", 90, 135),
        ("Center (90°, 90°)", 90, 90),
        ("Diagonal (45°, 45°)", 45, 45),
        ("Diagonal (135°, 135°)", 135, 135),
        ("Center (90°, 90°)", 90, 90),
    ]
    
    for description, pan_angle, tilt_angle in movements:
        print(f"   → {description}")
        kit.servo[PAN_CHANNEL].angle = pan_angle
        time.sleep(PAN_SPEED_DELAY)  # Add delay after pan movement
        kit.servo[TILT_CHANNEL].angle = tilt_angle
        time.sleep(TILT_SPEED_DELAY)  # Add delay after tilt movement
        time.sleep(1.0)  # Wait to observe the position
    
    print("✓ Movement test complete")
    
except Exception as e:
    print(f"✗ Movement test failed: {e}")
    sys.exit(1)

print()

# Test 6: Interactive test
print("Test 6: Interactive control")
print("=" * 50)
print()
print("Manual servo control (type command + Enter):")
print("  Commands:")
print("    w - Tilt up 5°")
print("    s - Tilt down 5°")
print("    a - Pan left 5°")
print("    d - Pan right 5°")
print("    c - Center both servos")
print("    q - Quit")
print()
print("Tip: Hold Enter to repeat last command quickly")
print()

# Initialize angles to current position
pan_angle = 90
tilt_angle = 90

try:
    print(f"Current -> Pan: {pan_angle}°  Tilt: {tilt_angle}°")
    print("Enter command: ", end='', flush=True)
    
    while True:
        try:
            key = input().strip().lower()
            
            if not key:  # Empty input, skip
                print("Enter command: ", end='', flush=True)
                continue
                
            if key == 'q':
                print("\nQuitting...")
                break
            elif key == 'w':  # Tilt up
                tilt_angle = max(0, tilt_angle - 5)
                kit.servo[TILT_CHANNEL].angle = tilt_angle
                time.sleep(TILT_SPEED_DELAY)
                print(f"Tilt UP   -> Pan: {pan_angle:3d}°  Tilt: {tilt_angle:3d}°")
            elif key == 's':  # Tilt down
                tilt_angle = min(180, tilt_angle + 5)
                kit.servo[TILT_CHANNEL].angle = tilt_angle
                time.sleep(TILT_SPEED_DELAY)
                print(f"Tilt DOWN -> Pan: {pan_angle:3d}°  Tilt: {tilt_angle:3d}°")
            elif key == 'a':  # Pan left
                pan_angle = max(0, pan_angle - 5)
                kit.servo[PAN_CHANNEL].angle = pan_angle
                time.sleep(PAN_SPEED_DELAY)
                print(f"Pan LEFT  -> Pan: {pan_angle:3d}°  Tilt: {tilt_angle:3d}°")
            elif key == 'd':  # Pan right
                pan_angle = min(180, pan_angle + 5)
                kit.servo[PAN_CHANNEL].angle = pan_angle
                time.sleep(PAN_SPEED_DELAY)
                print(f"Pan RIGHT -> Pan: {pan_angle:3d}°  Tilt: {tilt_angle:3d}°")
            elif key == 'c':  # Center - move gradually to reduce jitter
                print("Centering (smooth movement)...")
                # Move gradually to center to avoid jitter
                target_pan = 90
                target_tilt = 90
                
                # Move in small increments
                while abs(pan_angle - target_pan) > 2 or abs(tilt_angle - target_tilt) > 2:
                    if pan_angle < target_pan:
                        pan_angle = min(pan_angle + 3, target_pan)
                    elif pan_angle > target_pan:
                        pan_angle = max(pan_angle - 3, target_pan)
                    
                    if tilt_angle < target_tilt:
                        tilt_angle = min(tilt_angle + 3, target_tilt)
                    elif tilt_angle > target_tilt:
                        tilt_angle = max(tilt_angle - 3, target_tilt)
                    
                    kit.servo[PAN_CHANNEL].angle = pan_angle
                    time.sleep(PAN_SPEED_DELAY)
                    kit.servo[TILT_CHANNEL].angle = tilt_angle
                    time.sleep(TILT_SPEED_DELAY)
                    time.sleep(0.05)  # Small delay between steps
                
                # Final position
                pan_angle = target_pan
                tilt_angle = target_tilt
                kit.servo[PAN_CHANNEL].angle = pan_angle
                time.sleep(PAN_SPEED_DELAY)
                kit.servo[TILT_CHANNEL].angle = tilt_angle
                time.sleep(TILT_SPEED_DELAY)
                
                print(f"CENTERED  -> Pan: {pan_angle:3d}°  Tilt: {tilt_angle:3d}°")
            else:
                print(f"Unknown command: '{key}'. Use w/a/s/d/c/q")
            
            print("Enter command: ", end='', flush=True)
            
        except EOFError:
            print("\nEnd of input")
            break

except KeyboardInterrupt:
    print("\n\nInterrupted by user")

print()
print("=" * 50)
print("  Test Complete")
print("=" * 50)
print()
print("Summary:")
print("  If all tests passed and servos moved smoothly:")
print("    ✓ Hardware is working correctly")
print()
print("  If X-axis (pan) servo jitters:")
print("    1. Increase PAN_SPEED_DELAY in the script (currently 0.03s)")
print("    2. Check power supply - insufficient power causes jitter")
print("    3. Check mechanical load - friction or binding")
print("    4. Try different pulse width range (e.g., 1000-2000)")
print("    5. Verify servo is not damaged or low quality")
print()
print("  If servos jitter or don't move:")
print("    - Check power supply (servos need 5-6V, 2A+)")
print("    - Verify servo connections to PCA9685")
print("    - Ensure common ground between Jetson and PCA9685")
print("    - Try adding capacitors (100-470µF) across power rails")
print()
print("  If PCA9685 not detected:")
print("    - Check I2C wiring (SDA to pin 3, SCL to pin 5)")
print("    - Verify address jumpers on PCA9685")
print("    - Run: sudo i2cdetect -y 1")
print()
print("Tuning Tips:")
print("  Edit test_servos.py and adjust these values:")
print(f"    PAN_SPEED_DELAY = {PAN_SPEED_DELAY}  (increase if X-axis jitters)")
print(f"    TILT_SPEED_DELAY = {TILT_SPEED_DELAY}  (increase if Y-axis jitters)")
print("  Typical range: 0.01 to 0.1 seconds")
print()
