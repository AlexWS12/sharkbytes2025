"""
Configuration settings for the Person-Tracking Sentry system.
All tunable parameters are defined here for easy adjustment.
"""

# ========================================
# Camera Configuration
# ========================================

CAMERA_INDEX = 0  # /dev/video0
CAMERA_WIDTH = 320  # Small resolution for better FPS
CAMERA_HEIGHT = 320  # Small resolution for better FPS
TARGET_FPS = 30
SKIP_FRAMES = 1  # Process every frame (1=no skipping)

# ========================================
# Servo Hardware Configuration
# ========================================

PCA9685_ADDRESS = 0x40
PCA9685_CHANNELS = 16
PAN_CHANNEL = 0
TILT_CHANNEL = 1

# Servo angle limits (degrees)
PAN_MIN = 10
PAN_MAX = 170
PAN_DEFAULT = 90

TILT_MIN = 20
TILT_MAX = 150
TILT_DEFAULT = 90

# ========================================
# Control Parameters (Tuning)
# ========================================

# PD Controller gains
KP = 0.020  # Proportional gain - lower = smoother, slower tracking
KD = 0.25   # Derivative gain - higher = more damping, less overshoot

# Movement limits and smoothing
MAX_SERVO_STEP = 1.5  # Maximum servo movement per iteration (degrees)
SMOOTHING_FACTOR = 0.3  # Exponential smoothing (0-1): lower = smoother but slower

# Deadband zones (prevents jitter when close to target)
DEADBAND_X = 25  # Horizontal deadband in pixels (±)
DEADBAND_Y = 25  # Vertical deadband in pixels (±)

# Servo direction multipliers (change to -1 to invert)
PAN_INVERT = -1   # Set to -1 if servo moves opposite direction
TILT_INVERT = -1  # Set to -1 if servo moves opposite direction

# ========================================
# Detection & Tracking Parameters
# ========================================

# YOLO detection settings
YOLO_MODEL = 'yolo11n.pt'  # YOLOv11 Nano model
YOLO_CONFIDENCE = 0.35  # Confidence threshold for detections
YOLO_IOU = 0.5  # IoU threshold for NMS
YOLO_MAX_DETECTIONS = 5  # Maximum detections per frame
PERSON_CLASS_ID = 0  # COCO class ID for person

# DeepSORT tracker settings
DEEPSORT_MAX_AGE = 30  # Frames to keep track without detection
DEEPSORT_N_INIT = 3  # Frames needed to confirm track
DEEPSORT_MAX_IOU_DISTANCE = 0.7
DEEPSORT_MAX_COSINE_DISTANCE = 0.3
DEEPSORT_NN_BUDGET = 100

# Target tracking
TARGET_LOST_TIMEOUT = 2.0  # Seconds before considering target lost

# ========================================
# Idle Sweep Behavior
# ========================================

SWEEP_SPEED = 0.5  # Degrees per frame when searching
SWEEP_MIN = 30  # Minimum pan angle for sweep
SWEEP_MAX = 150  # Maximum pan angle for sweep
SWEEP_DIRECTION = 1  # 1 = right, -1 = left

# ========================================
# UI Configuration
# ========================================

WINDOW_NAME = 'Person-Tracking Sentry'
SHOW_FPS = True
SHOW_TRACKING_INFO = True
SHOW_CONTROLS_HELP = True
