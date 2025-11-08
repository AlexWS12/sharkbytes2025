"""
Main Sentry System Module
==========================
Integrates detection, tracking, and servo control for person-tracking sentry.
"""

import cv2
import time
from config.settings import (
    CAMERA_INDEX, CAMERA_WIDTH, CAMERA_HEIGHT, TARGET_FPS,
    PAN_DEFAULT, TILT_DEFAULT,
    KP, KD, PAN_INVERT, TILT_INVERT,
    DEADBAND_X, DEADBAND_Y, SMOOTHING_FACTOR,
    SWEEP_SPEED, SWEEP_MIN, SWEEP_MAX, SWEEP_DIRECTION,
    WINDOW_NAME
)
from src.detector import PersonDetector
from src.tracker import ObjectTracker
from src.servo_controller import ServoController
from src.target_tracker import TargetTracker
from utils.ui_utils import (
    draw_bounding_box, draw_crosshair, draw_status_info,
    draw_controls_help, get_bbox_center
)


class PersonTrackingSentry:
    """Main sentry system integrating detection, tracking, and servo control."""
    
    def __init__(self, verbose=True):
        """
        Initialize all subsystems.
        
        Args:
            verbose: If True, print initialization messages
        """
        if verbose:
            print("\n" + "="*50)
            print("Person-Tracking Sentry Initializing...")
            print("="*50 + "\n")
        
        # Initialize camera
        if verbose:
            print("[CAMERA] Opening camera...")
        
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, TARGET_FPS)
        
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open camera at /dev/video0")
        
        if verbose:
            print(f"[CAMERA] Opened at {CAMERA_WIDTH}x{CAMERA_HEIGHT} @ {TARGET_FPS}fps")
        
        # Initialize detector and tracker
        self.detector = PersonDetector(verbose=verbose)
        self.tracker = ObjectTracker(verbose=verbose)
        
        # Initialize servo controller
        self.servo = ServoController(verbose=verbose)
        
        # Initialize target tracker
        self.target = TargetTracker()
        
        # Idle sweep state
        self.sweep_angle = PAN_DEFAULT
        self.sweep_direction = SWEEP_DIRECTION
        
        # Frame center
        self.frame_center_x = CAMERA_WIDTH // 2
        self.frame_center_y = CAMERA_HEIGHT // 2
        
        # FPS calculation
        self.fps_start_time = time.time()
        self.fps_frame_count = 0
        self.current_fps = 0
        
        # Previous error for derivative control (prevents overshooting)
        self.prev_error_x = 0
        self.prev_error_y = 0
        
        # Smoothed target positions for exponential smoothing
        self.smooth_target_x = self.frame_center_x
        self.smooth_target_y = self.frame_center_y
        
        if verbose:
            print("\n" + "="*50)
            print("Sentry System Ready!")
            print("="*50 + "\n")
    
    def control_servos(self, target_x, target_y):
        """
        Use PD control with exponential smoothing to drive servos toward target.
        
        Args:
            target_x: Target X coordinate in frame
            target_y: Target Y coordinate in frame
        """
        # Apply exponential smoothing to target position
        # This creates a smooth, natural follow motion like a gimbal
        self.smooth_target_x = (SMOOTHING_FACTOR * target_x + 
                                (1 - SMOOTHING_FACTOR) * self.smooth_target_x)
        self.smooth_target_y = (SMOOTHING_FACTOR * target_y + 
                                (1 - SMOOTHING_FACTOR) * self.smooth_target_y)
        
        # Calculate error using smoothed target (distance from center)
        error_x = self.smooth_target_x - self.frame_center_x
        error_y = self.smooth_target_y - self.frame_center_y
        
        # Apply deadband
        if abs(error_x) < DEADBAND_X:
            error_x = 0
        if abs(error_y) < DEADBAND_Y:
            error_y = 0
        
        # Calculate derivative (change in error) to prevent overshooting
        deriv_x = error_x - self.prev_error_x
        deriv_y = error_y - self.prev_error_y
        
        # Store current error for next iteration
        self.prev_error_x = error_x
        self.prev_error_y = error_y
        
        # Calculate servo adjustments using PD control
        # P term: proportional to error (main correction)
        # D term: proportional to rate of change (damping/smoothing)
        delta_pan = (error_x * KP - deriv_x * KD) * PAN_INVERT
        delta_tilt = -(error_y * KP - deriv_y * KD) * TILT_INVERT
        
        # Calculate target angles
        target_pan = self.servo.pan_angle + delta_pan
        target_tilt = self.servo.tilt_angle + delta_tilt
        
        # Move servos smoothly
        self.servo.move_smooth(target_pan, target_tilt)
    
    def idle_sweep(self):
        """Perform slow pan sweep when no target is locked."""
        self.sweep_angle += SWEEP_SPEED * self.sweep_direction
        
        # Reverse direction at limits
        if self.sweep_angle >= SWEEP_MAX:
            self.sweep_angle = SWEEP_MAX
            self.sweep_direction = -1
        elif self.sweep_angle <= SWEEP_MIN:
            self.sweep_angle = SWEEP_MIN
            self.sweep_direction = 1
        
        # Move to sweep position
        self.servo.move_smooth(self.sweep_angle, TILT_DEFAULT)
    
    def center_servos(self):
        """Center servos to default position."""
        print("[SERVO] Centering to default position...")
        self.servo.reset()
        self.sweep_angle = PAN_DEFAULT
    
    def update_fps(self):
        """Calculate and update FPS counter."""
        self.fps_frame_count += 1
        elapsed = time.time() - self.fps_start_time
        if elapsed > 1.0:
            self.current_fps = self.fps_frame_count / elapsed
            self.fps_frame_count = 0
            self.fps_start_time = time.time()
    
    def draw_ui(self, frame, tracks):
        """
        Draw UI overlays on frame.
        
        Args:
            frame: Image frame to draw on
            tracks: List of active tracks
            
        Returns:
            frame: Frame with UI overlays
        """
        # Draw all tracked people
        for track in tracks:
            bbox = track['bbox']
            track_id = track['id']
            is_locked = self.target.is_tracking(track_id)
            draw_bounding_box(frame, bbox, track_id, is_locked)
        
        # Draw frame center crosshair and deadband
        draw_crosshair(frame, self.frame_center_x, self.frame_center_y)
        
        # Draw status information
        status_text = self.target.get_status()
        servo_angles = self.servo.get_position()
        draw_status_info(frame, status_text, servo_angles, self.current_fps, len(tracks))
        
        # Draw keyboard controls
        draw_controls_help(frame)
        
        return frame
    
    def run(self):
        """Main execution loop."""
        print("[SENTRY] Starting main loop...")
        print("="*50)
        print("Keyboard Controls:")
        print("  L - Toggle Lock ON/OFF")
        print("  C - Center servos (only when unlocked)")
        print("  Q - Quit")
        print("="*50 + "\n")
        
        try:
            while True:
                # Read frame
                ret, frame = self.cap.read()
                if not ret:
                    print("[ERROR] Failed to read frame from camera")
                    break
                
                # Run detection
                detections = self.detector.detect(frame)
                
                # Update tracker
                tracks = self.tracker.update(detections, frame)
                
                # Check if locked target timed out
                self.target.check_timeout()
                
                # Process tracks
                target_found = False
                
                for track in tracks:
                    track_id = track['id']
                    bbox = track['bbox']
                    
                    # If not locked, lock onto first person detected
                    if not self.target.is_locked:
                        self.target.lock_target(track_id)
                    
                    # If this is our locked target, track it
                    if self.target.is_tracking(track_id):
                        self.target.update_target(track_id)
                        target_found = True
                        
                        # Get target center
                        target_x, target_y = get_bbox_center(bbox)
                        
                        # Drive servos to center target
                        self.control_servos(target_x, target_y)
                        break
                
                # If no target found and not locked, perform idle sweep
                if not target_found and not self.target.is_locked:
                    self.idle_sweep()
                
                # Update FPS
                self.update_fps()
                
                # Draw UI
                frame = self.draw_ui(frame, tracks)
                
                # Display frame
                cv2.imshow(WINDOW_NAME, frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == ord('Q'):
                    print("\n[SENTRY] Quit command received")
                    break
                
                elif key == ord('l') or key == ord('L'):
                    # Toggle lock on/off
                    if self.target.manual_lock_disabled:
                        self.target.manual_lock_enable()
                    else:
                        self.target.manual_unlock()
                
                elif key == ord('c') or key == ord('C'):
                    # Center servos (only if not locked)
                    if not self.target.is_locked:
                        self.center_servos()
                    else:
                        print("[SERVO] Cannot center - locked to target. Press 'L' to unlock first.")
        
        except KeyboardInterrupt:
            print("\n[SENTRY] Interrupted by user")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        print("\n[SENTRY] Cleaning up...")
        
        # Reset servos to default position
        print("[SERVO] Resetting to default position...")
        self.servo.reset()
        
        # Release camera
        print("[CAMERA] Releasing camera...")
        self.cap.release()
        
        # Close windows
        cv2.destroyAllWindows()
        
        print("[SENTRY] Shutdown complete")
