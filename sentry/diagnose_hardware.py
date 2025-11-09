#!/usr/bin/env python3
"""
Hardware Diagnostic Script
Tests PCA9685 and servo connections
"""

import time
import sys

print("=" * 60)
print("  Hardware Diagnostic Tool")
print("=" * 60)
print()

# Test 1: I2C Detection
print("Test 1: Checking I2C Bus")
print("-" * 60)
import subprocess

try:
    result = subprocess.run(['i2cdetect', '-y', '1'], 
                          capture_output=True, text=True, timeout=5)
    print(result.stdout)
    
    if '40' in result.stdout:
        print("[OK] PCA9685 detected at address 0x40")
        pca_detected = True
    else:
        print("[FAIL] PCA9685 NOT detected at 0x40")
        print("\nWith your multimeter:")
        print("  1. Check V+ to GND: Should read 5-6V DC")
        print("  2. Check VCC to GND: Should read 3.3V or 5V DC")
        print("  3. Check I2C connections (SDA/SCL)")
        pca_detected = False
except Exception as e:
    print(f"[FAIL] Could not run i2cdetect: {e}")
    pca_detected = False

print()

if not pca_detected:
    print("Cannot proceed without PCA9685 detection.")
    print("\nMultimeter Checks:")
    print("  Power Test:")
    print("    - V+ to GND should be 5-6V DC")
    print("    - VCC to GND should be 3.3-5V DC")
    print("  If both are correct, PCA9685 chip may be damaged")
    sys.exit(1)

# Test 2: Initialize PCA9685
print("Test 2: Initializing PCA9685")
print("-" * 60)

try:
    from adafruit_servokit import ServoKit
    kit = ServoKit(channels=16, address=0x40, frequency=50)
    print("[OK] PCA9685 initialized successfully")
    print("  This means the chip is communicating properly")
except Exception as e:
    print(f"[FAIL] Failed to initialize: {e}")
    print("\nThe chip is detected but not responding properly")
    print("PCA9685 may be partially damaged")
    sys.exit(1)

print()

# Test 3: Channel Output Test
print("Test 3: Testing Individual Channels")
print("-" * 60)
print("This will pulse each channel 0-15 briefly")
print("Use your multimeter in DC voltage mode:")
print("  - Red probe on channel signal pin")
print("  - Black probe on GND")
print("  - You should see voltage change when channel activates")
print()

channels_to_test = [0, 1, 2, 3, 4, 5]  # Test first 6 channels
working_channels = []

for ch in channels_to_test:
    print(f"Testing channel {ch}...", end='', flush=True)
    try:
        # Send PWM signal
        kit.servo[ch].angle = 90
        time.sleep(0.5)
        kit.servo[ch].angle = 45
        time.sleep(0.5)
        kit.servo[ch].angle = 135
        time.sleep(0.5)
        kit.servo[ch].angle = 90
        time.sleep(0.3)
        
        working_channels.append(ch)
        print(" [OK] Signal sent")
    except Exception as e:
        print(f" [FAIL] Error: {e}")

print()
print(f"Channels responding: {working_channels}")
print()

# Test 4: Servo Response Test
print("Test 4: Servo Movement Test")
print("-" * 60)
print("Connect servos to channels 2 and 3")
input("Press Enter when servos are connected...")

for ch in [2, 3]:
    servo_name = "Pan (X-axis)" if ch == 2 else "Tilt (Y-axis)"
    print(f"\nTesting {servo_name} on channel {ch}")
    print(f"  Watch servo for movement...")
    
    try:
        angles = [90, 45, 135, 90]
        for angle in angles:
            print(f"  --> {angle}deg", end='', flush=True)
            kit.servo[ch].angle = angle
            time.sleep(1)
            print(" [OK]")
        
        response = input(f"  Did servo on channel {ch} move? (y/n): ").lower()
        
        if response == 'y':
            print(f"  [OK] Channel {ch} and servo are working")
        else:
            print(f"  [FAIL] Problem with channel {ch} or servo")
            print(f"\n  Multimeter checks for servo on channel {ch}:")
            print(f"    1. Voltage on signal pin while running: Should fluctuate")
            print(f"    2. Servo red to black (disconnected): Should be 5-50Ohm")
            print(f"    3. Current draw when moving: Should be 100-500mA")
            print(f"    4. If all else fails, servo may be damaged")
            
    except Exception as e:
        print(f"  [FAIL] Error: {e}")

print()
print("=" * 60)
print("  Diagnostic Complete")
print("=" * 60)
print()
print("Summary of Multimeter Tests:")
print()
print("PCA9685 Power:")
print("  - V+ to GND: Should be 5.0-6.0V DC")
print("  - VCC to GND: Should be 3.3V or 5.0V DC")
print()
print("PCA9685 Channels (while running):")
print("  - Signal pin to GND: 0-5V pulsing (DC mode shows ~1.5-2.5V avg)")
print()
print("Servos (disconnected from PCA9685):")
print("  - Red to Black wire: 5-50Ohm resistance")
print("  - Current draw (when powered): 100-500mA per servo")
print()
print("Common Failures:")
print("  - V+ = 0V: Bad power supply or wiring")
print("  - VCC = 0V: Bad connection to Jetson")
print("  - Signal always 0V: Dead PCA9685 channel")
print("  - Servo resistance = infinite: Broken motor winding")
print("  - Servo resistance = 0Ohm: Shorted motor")
print("  - No servo movement but signal present: Dead servo electronics")
print()
