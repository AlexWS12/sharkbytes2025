"""
Servo Controller Module
========================
Manages PCA9685 servo control with smoothing and safety limits.
"""

import numpy as np
from adafruit_servokit import ServoKit
from config.settings import (
    PCA9685_ADDRESS, PCA9685_CHANNELS,
    PAN_CHANNEL, TILT_CHANNEL,
    PAN_MIN, PAN_MAX, PAN_DEFAULT,
    TILT_MIN, TILT_MAX, TILT_DEFAULT,
    MAX_SERVO_STEP
)


class ServoController:
    """Manages PCA9685 servo control with smoothing and safety limits."""
    
    def __init__(self, verbose=True):
        """
        Initialize the ServoKit and set default positions.
        
        Args:
            verbose: If True, print initialization messages
        """
        if verbose:
            print("[SERVO] Initializing PCA9685 servo controller...")
        
        self.kit = ServoKit(channels=PCA9685_CHANNELS, address=PCA9685_ADDRESS)
        
        # Current servo positions
        self.pan_angle = PAN_DEFAULT
        self.tilt_angle = TILT_DEFAULT
        
        # Set initial positions
        self.set_pan(PAN_DEFAULT)
        self.set_tilt(TILT_DEFAULT)
        
        if verbose:
            print(f"[SERVO] Initialized at pan={PAN_DEFAULT}°, tilt={TILT_DEFAULT}°")
    
    def set_pan(self, angle):
        """
        Set pan servo angle with clamping to safe limits.
        
        Args:
            angle: Target angle in degrees
        """
        angle = np.clip(angle, PAN_MIN, PAN_MAX)
        self.pan_angle = angle
        self.kit.servo[PAN_CHANNEL].angle = angle
    
    def set_tilt(self, angle):
        """
        Set tilt servo angle with clamping to safe limits.
        
        Args:
            angle: Target angle in degrees
        """
        angle = np.clip(angle, TILT_MIN, TILT_MAX)
        self.tilt_angle = angle
        self.kit.servo[TILT_CHANNEL].angle = angle
    
    def move_smooth(self, target_pan, target_tilt):
        """
        Move servos toward target angles with maximum step size limiting.
        This provides smooth motion and prevents jitter.
        
        Args:
            target_pan: Target pan angle in degrees
            target_tilt: Target tilt angle in degrees
        """
        # Calculate deltas
        delta_pan = target_pan - self.pan_angle
        delta_tilt = target_tilt - self.tilt_angle
        
        # Limit maximum step size for smooth motion
        delta_pan = np.clip(delta_pan, -MAX_SERVO_STEP, MAX_SERVO_STEP)
        delta_tilt = np.clip(delta_tilt, -MAX_SERVO_STEP, MAX_SERVO_STEP)
        
        # Apply movements
        new_pan = self.pan_angle + delta_pan
        new_tilt = self.tilt_angle + delta_tilt
        
        self.set_pan(new_pan)
        self.set_tilt(new_tilt)
    
    def reset(self):
        """Reset servos to default position."""
        self.set_pan(PAN_DEFAULT)
        self.set_tilt(TILT_DEFAULT)
    
    def get_position(self):
        """
        Get current servo positions.
        
        Returns:
            tuple: (pan_angle, tilt_angle)
        """
        return self.pan_angle, self.tilt_angle
