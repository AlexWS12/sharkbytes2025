"""
UI Utilities Module
===================
Functions for drawing overlays and displaying information on video frames.
"""

import cv2
from config.settings import (
    CAMERA_WIDTH, CAMERA_HEIGHT,
    DEADBAND_X, DEADBAND_Y,
    WINDOW_NAME
)


def draw_bounding_box(frame, bbox, track_id, is_locked_target):
    """
    Draw a bounding box for a tracked person.
    
    Args:
        frame: Image frame to draw on
        bbox: Bounding box coordinates [x1, y1, x2, y2]
        track_id: Track ID number
        is_locked_target: True if this is the locked target
    """
    x1, y1, x2, y2 = map(int, bbox)
    
    # Color: green for locked target, blue for others
    if is_locked_target:
        color = (0, 255, 0)  # Green
        thickness = 3
        label = f"TARGET ID:{track_id}"
    else:
        color = (255, 100, 0)  # Blue
        thickness = 2
        label = f"ID:{track_id}"
    
    # Draw bounding box
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
    
    # Draw label
    cv2.putText(frame, label, (x1, y1 - 10),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    # Draw center point for locked target
    if is_locked_target:
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)


def draw_crosshair(frame, center_x, center_y):
    """
    Draw crosshair at frame center.
    
    Args:
        frame: Image frame to draw on
        center_x: X coordinate of center
        center_y: Y coordinate of center
    """
    # Draw center crosshair
    cv2.line(frame, (center_x - 20, center_y),
            (center_x + 20, center_y), (0, 0, 255), 2)
    cv2.line(frame, (center_x, center_y - 20),
            (center_x, center_y + 20), (0, 0, 255), 2)
    
    # Draw deadband zone
    cv2.rectangle(frame,
                 (center_x - DEADBAND_X, center_y - DEADBAND_Y),
                 (center_x + DEADBAND_X, center_y + DEADBAND_Y),
                 (0, 255, 255), 1)


def draw_status_info(frame, status_text, servo_angles, fps, track_count):
    """
    Draw status information overlay.
    
    Args:
        frame: Image frame to draw on
        status_text: Current tracking status
        servo_angles: Tuple of (pan_angle, tilt_angle)
        fps: Current frames per second
        track_count: Number of active tracks
    """
    pan_angle, tilt_angle = servo_angles
    
    # Draw status text
    cv2.putText(frame, f"Status: {status_text}", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    # Draw servo angles
    servo_text = f"Pan: {pan_angle:.1f}  Tilt: {tilt_angle:.1f}"
    cv2.putText(frame, servo_text, (10, 60),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Draw FPS
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 90),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Draw track count
    cv2.putText(frame, f"Tracks: {track_count}", (10, 120),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)


def draw_controls_help(frame):
    """
    Draw keyboard controls help text.
    
    Args:
        frame: Image frame to draw on
    """
    controls_y_start = CAMERA_HEIGHT - 80
    cv2.putText(frame, "Controls:", (10, controls_y_start),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    cv2.putText(frame, "L: Lock ON/OFF", (10, controls_y_start + 20),
               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
    cv2.putText(frame, "C: Center (when unlocked)", (10, controls_y_start + 40),
               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
    cv2.putText(frame, "Q: Quit", (10, controls_y_start + 60),
               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)


def get_bbox_center(bbox):
    """
    Calculate center point of bounding box.
    
    Args:
        bbox: Bounding box coordinates [x1, y1, x2, y2]
        
    Returns:
        tuple: (center_x, center_y)
    """
    x1, y1, x2, y2 = bbox
    cx = int((x1 + x2) / 2)
    cy = int((y1 + y2) / 2)
    return cx, cy
