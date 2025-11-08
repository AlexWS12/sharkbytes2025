#!/usr/bin/env python3
"""
Jitter Diagnosis - Find the exact problem angles
"""

import time
from adafruit_servokit import ServoKit

print("=" * 60)
print("  JITTER ANGLE DIAGNOSIS")
print("=" * 60)
print()

# Which channel has the jitter?
channel = int(input("Which channel has jitter? (2 or 3): "))
if channel not in [2, 3]:
    print("Invalid channel")
    exit(1)

print(f"\nTesting Channel {channel}")
print("Watch the servo carefully at each angle")
print()

kit = ServoKit(channels=16, address=0x40, frequency=50)
kit.servo[channel].set_pulse_width_range(500, 2500)

# Test specific problem zones
test_angles = [60, 70, 75, 78, 79, 80, 81, 82, 85, 90, 
               95, 100, 105, 115, 118, 119, 120, 121, 122, 125, 130]

jitter_angles = []

print("Testing angles around the problem zones (80° and 120°)...")
print("Press Enter after observing each angle")
print()

for angle in test_angles:
    kit.servo[channel].angle = angle
    time.sleep(0.5)  # Let it settle
    
    # Ask user if they see jitter
    response = input(f"Angle {angle:3d}° - Jittery? (y/n/quit): ").lower().strip()
    
    if response == 'quit' or response == 'q':
        break
    elif response == 'y' or response == 'yes':
        jitter_angles.append(angle)
        print(f"  ✗ Jitter detected at {angle}°")
    else:
        print(f"  ✓ Smooth at {angle}°")

print()
print("=" * 60)
print("  DIAGNOSIS")
print("=" * 60)
print()

if jitter_angles:
    print(f"Jitter detected at angles: {jitter_angles}")
    print()
    
    # Analyze pattern
    if len(jitter_angles) <= 3:
        print("DIAGNOSIS: Dead spots in servo potentiometer")
        print()
        print("The servo has specific angles where the position sensor fails.")
        print("This is internal servo damage - the potentiometer is worn.")
        print()
        print("Solution: REPLACE THE SERVO")
        print()
        print("Workaround (temporary):")
        print("  • Avoid those specific angles in your code")
        print("  • Add angle limits to skip problem zones")
        
    elif all(70 <= a <= 90 for a in jitter_angles):
        print("DIAGNOSIS: Gear binding in lower mid-range")
        print()
        print("The servo's gears are damaged or worn in this range.")
        print()
        print("Solution: REPLACE THE SERVO")
        
    elif all(110 <= a <= 130 for a in jitter_angles):
        print("DIAGNOSIS: Gear binding in upper mid-range")
        print()
        print("The servo's gears are damaged or worn in this range.")
        print()
        print("Solution: REPLACE THE SERVO")
        
    else:
        print("DIAGNOSIS: Multiple problem zones")
        print()
        print("The servo has widespread internal issues.")
        print()
        print("Solution: DEFINITELY REPLACE THE SERVO")
    
    print()
    print("Additional checks:")
    print("  1. Is anything physically blocking the servo arm?")
    print("  2. Remove servo arm, test bare servo - still jitters?")
    print("     • If yes: Internal servo problem")
    print("     • If no: Mechanical binding from mount/load")
    print()
    print("  3. Swap this servo with the working one")
    print("     • If jitter moves to other channel: SERVO IS BAD")
    print("     • If jitter stays on same channel: Wiring/power issue")
    
else:
    print("No jitter detected!")
    print()
    print("Possible reasons:")
    print("  1. Jitter is intermittent")
    print("  2. Jitter only happens under load (with camera attached)")
    print("  3. Power supply voltage drops when both servos move")
    print()
    print("Try:")
    print("  • Test with camera/payload attached")
    print("  • Measure voltage at servo during movement")
    print("  • Use better power supply (6V, 3A+)")

print()
print("=" * 60)
print()

# Return to center
print("Returning to center (90°)...")
kit.servo[channel].angle = 90
time.sleep(1)

print("Test complete")
print()
