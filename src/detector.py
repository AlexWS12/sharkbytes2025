"""
Person Detector Module
======================
YOLO-based person detection with optimizations for real-time performance.
"""

from ultralytics import YOLO
from config.settings import (
    YOLO_MODEL, YOLO_CONFIDENCE, YOLO_IOU,
    YOLO_MAX_DETECTIONS, PERSON_CLASS_ID,
    CAMERA_WIDTH
)


class PersonDetector:
    """YOLO-based person detector optimized for real-time tracking."""
    
    def __init__(self, verbose=True):
        """
        Initialize YOLO model for person detection.
        
        Args:
            verbose: If True, print1 initialization messages
        """
        if verbose:
            print("[YOLO] Loading YOLOv11 model...")
        
        self.model = YOLO(YOLO_MODEL)
        
        if verbose:
            print("[YOLO] Model loaded successfully")
    
    def detect(self, frame):
        """
        Detect people in frame using YOLO.
        
        Args:
            frame: Input image frame (numpy array)
            
        Returns:
            list: List of detections, each as [x1, y1, x2, y2, confidence]
        """
        # Run YOLO with optimizations for speed
        # Device is auto-detected (will use CUDA if available, CPU otherwise)
        results = self.model(
            frame,
            verbose=False,
            conf=YOLO_CONFIDENCE,  # Confidence threshold
            iou=YOLO_IOU,  # IoU threshold for NMS
            imgsz=CAMERA_WIDTH,  # Match camera resolution for speed
            classes=[PERSON_CLASS_ID],  # Only detect person class
            half=False,  # Use FP16 if CUDA available (set to True for speed boost)
            max_det=YOLO_MAX_DETECTIONS,  # Limit detections
            agnostic_nms=True  # Faster NMS
        )
        
        detections = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Filter for person class only
                if int(box.cls[0]) == PERSON_CLASS_ID:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = float(box.conf[0])
                    detections.append([x1, y1, x2, y2, conf])
        
        return detections
