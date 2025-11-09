#!/usr/bin/env python3
"""
Simple Servo Test - Definitive Check
Tests one servo at a time with clear visual confirmation
"""

import time
import sys

print("=" * 60)
print("  DEFINITIVE SERVO TEST")
print("=" * 60)
print()

# Import ServoKit
try:
    from adafruit_servokit import ServoKit
    kit = ServoKit(channels=16, address=0x40, frequency=50)
    print("[OK] PCA9685 initialized")
except Exception as e:
    print(f"[FAIL] Failed to initialize PCA9685: {e}")
    sys.exit(1)

print()
print("This will move each servo VERY SLOWLY")
print("Watch carefully - you should see clear movement")
print()

# Configure servos
kit.servo[2].set_pulse_width_range(500, 2500)
kit.servo[3].set_pulse_width_range(500, 2500)

# Test Channel 2 (Pan / Horizontal)
print("=" * 60)
print("Testing CHANNEL 2 (Pan / Horizontal Servo)")
print("=" * 60)
print()

print("Starting position: 90deg (center)")
kit.servo[2].angle = 90
time.sleep(2)

print("\nMoving SLOWLY to the LEFT (45deg)...")
for angle in range(90, 44, -1):
    kit.servo[2].angle = angle
    print(f"\rAngle: {angle}deg  ", end='', flush=True)
    time.sleep(0.1)  # Very slow
print(" DONE")
time.sleep(2)

print("\nMoving SLOWLY to the RIGHT (135deg)...")
for angle in range(45, 136, 1):
    kit.servo[2].angle = angle
    print(f"\rAngle: {angle}deg  ", end='', flush=True)
    time.sleep(0.1)  # Very slow
print(" DONE")
time.sleep(2)

print("\nReturning to CENTER (90deg)...")
for angle in range(135, 89, -1):
    kit.servo[2].angle = angle
    print(f"\rAngle: {angle}deg  ", end='', flush=True)
    time.sleep(0.1)  # Very slow
print(" DONE")
time.sleep(1)

print()
response = input("Did Channel 2 servo move smoothly? (yes/no): ").lower()

if 'y' in response:
    print("[OK] Channel 2 servo is WORKING")
    channel_2_ok = True
else:
    print("[FAIL] Channel 2 servo is DEAD or disconnected")
    print("\nPossible causes:")
    print("  1. Servo is damaged/fried")
    print("  2. Servo not connected to channel 2")
    print("  3. Insufficient power supply")
    print("  4. Loose connections")
    channel_2_ok = False

print()
print("=" * 60)
print("Testing CHANNEL 3 (Tilt / Vertical Servo)")
print("=" * 60)
print()

print("Starting position: 90deg (center)")
kit.servo[3].angle = 90
time.sleep(2)

print("\nMoving SLOWLY UP (45deg)...")
for angle in range(90, 44, -1):
    kit.servo[3].angle = angle
    print(f"\rAngle: {angle}deg  ", end='', flush=True)
    time.sleep(0.1)  # Very slow
print(" DONE")
time.sleep(2)

print("\nMoving SLOWLY DOWN (135deg)...")
for angle in range(45, 136, 1):
    kit.servo[3].angle = angle
    print(f"\rAngle: {angle}deg  ", end='', flush=True)
    time.sleep(0.1)  # Very slow
print(" DONE")
time.sleep(2)

print("\nReturning to CENTER (90deg)...")
for angle in range(135, 89, -1):
    kit.servo[3].angle = angle
    print(f"\rAngle: {angle}deg  ", end='', flush=True)
    time.sleep(0.1)  # Very slow
print(" DONE")
time.sleep(1)

print()
response = input("Did Channel 3 servo move smoothly? (yes/no): ").lower()

if 'y' in response:
    print("[OK] Channel 3 servo is WORKING")
    channel_3_ok = True
else:
    print("[FAIL] Channel 3 servo is DEAD or disconnected")
    channel_3_ok = False

# Final Summary
print()
print("=" * 60)
print("  FINAL DIAGNOSIS")
print("=" * 60)
print()

if channel_2_ok and channel_3_ok:
    print("[OK][OK] BOTH SERVOS ARE WORKING!")
    print()
    print("If you saw jitter before, it was likely:")
    print("  - Commands sent too fast")
    print("  - Power supply issue (voltage sag under load)")
    print("  - Mechanical binding/friction")
    print()
    print("Hardware is GOOD - software tuning may be needed")
    
elif channel_3_ok and not channel_2_ok:
    print("[OK] Channel 3 (vertical) is WORKING")
    print("[FAIL] Channel 2 (horizontal) has a problem")
    print()
    print("Next steps:")
    print("  1. Swap the two servos physically")
    print("     - If problem follows servo: SERVO IS DEAD")
    print("     - If problem stays on channel 2: WIRING ISSUE")
    print()
    print("  2. Multimeter check on non-working servo:")
    print("     - Disconnect servo from PCA9685")
    print("     - Measure resistance: Red wire to Black wire")
    print("     - Should be: 5-50 Ohms")
    print("     - If infinite (OL): Motor is DEAD")
    print()
    print("  3. Try different power supply (5-6V, 2A minimum)")
    
elif channel_2_ok and not channel_3_ok:
    print("[OK] Channel 2 (horizontal) is WORKING")
    print("[FAIL] Channel 3 (vertical) has a problem")
    print()
    print("(Same troubleshooting as above)")
    
else:
    print("[FAIL][FAIL] BOTH SERVOS have problems")
    print()
    print("Most likely causes:")
    print("  1. Insufficient power supply")
    print("     - Check V+ to GND with multimeter: Should be 5-6V")
    print("     - Power supply must provide 2A+ for servos")
    print("  2. Both servos are damaged")
    print("  3. Wiring issue (all connections loose)")

print()
print("=" * 60)
print()
