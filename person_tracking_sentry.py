#!/usr/bin/env python3
"""
Jetson Person-Tracking Sentry Turret
=====================================
Main entry point for the person-tracking sentry system.

Uses YOLO for person detection, DeepSORT for tracking, and PCA9685 servo driver
to keep a tracked person centered in the camera frame.

Hardware:
- Jetson device
- USB Camera (/dev/video0)
- PCA9685 Servo Driver (I2C address 0x40)
- 2 Servos: Pan (channel 0) and Tilt (channel 1)

Author: AI Assistant
Date: November 8, 2025

USAGE:
    python person_tracking_sentry.py

CONTROLS:
    L - Toggle Lock ON/OFF
    C - Center servos (only when unlocked)
    Q - Quit

For configuration, edit config/settings.py
For tuning tips, see TUNING_GUIDE.md
"""

import sys
import traceback


def main():
    """Main entry point for the sentry system."""
    try:
        # Import the sentry class from modular structure
        from src.sentry import PersonTrackingSentry
        
        # Create and run the sentry
        sentry = PersonTrackingSentry(verbose=True)
        sentry.run()
        
        return 0
        
    except ImportError as e:
        print(f"\n[ERROR] Import error: {e}")
        print("\nMake sure all dependencies are installed:")
        print("  pip install -r requirements.txt")
        print("\nAnd ensure you're running from the project root directory.")
        traceback.print_exc()
        return 1
        
    except Exception as e:
        print(f"\n[ERROR] Fatal error: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
