"""
Object Tracker Module
=====================
DeepSORT-based multi-object tracking for person detection.
"""

from deep_sort_realtime.deepsort_tracker import DeepSort
from config.settings import (
    DEEPSORT_MAX_AGE, DEEPSORT_N_INIT,
    DEEPSORT_MAX_IOU_DISTANCE, DEEPSORT_MAX_COSINE_DISTANCE,
    DEEPSORT_NN_BUDGET
)


class ObjectTracker:
    """DeepSORT-based tracker for maintaining person identities across frames."""
    
    def __init__(self, verbose=True):
        """
        Initialize DeepSORT tracker.
        
        Args:
            verbose: If True, print initialization messages
        """
        if verbose:
            print("[DEEPSORT] Initializing tracker...")
        
        self.tracker = DeepSort(
            max_age=DEEPSORT_MAX_AGE,
            n_init=DEEPSORT_N_INIT,
            max_iou_distance=DEEPSORT_MAX_IOU_DISTANCE,
            max_cosine_distance=DEEPSORT_MAX_COSINE_DISTANCE,
            nn_budget=DEEPSORT_NN_BUDGET
        )
        
        if verbose:
            print("[DEEPSORT] Tracker initialized")
    
    def update(self, detections, frame):
        """
        Update tracker with new detections.
        
        Args:
            detections: List of detections from detector, each as [x1, y1, x2, y2, conf]
            frame: Current image frame (numpy array)
            
        Returns:
            list: List of confirmed tracks, each as dict with 'id' and 'bbox' keys
        """
        # Convert detections to DeepSORT format: ([x1, y1, w, h], confidence, class)
        deepsort_detections = []
        for det in detections:
            x1, y1, x2, y2, conf = det
            w = x2 - x1
            h = y2 - y1
            deepsort_detections.append(([x1, y1, w, h], conf, 'person'))
        
        # Update tracker
        tracks = self.tracker.update_tracks(deepsort_detections, frame=frame)
        
        # Return confirmed tracks only
        confirmed_tracks = []
        for track in tracks:
            if track.is_confirmed():
                bbox = track.to_ltrb()  # [left, top, right, bottom]
                confirmed_tracks.append({
                    'id': track.track_id,
                    'bbox': bbox
                })
        
        return confirmed_tracks
    
    def reset(self):
        """Reset tracker state (clears all tracks)."""
        self.tracker = DeepSort(
            max_age=DEEPSORT_MAX_AGE,
            n_init=DEEPSORT_N_INIT,
            max_iou_distance=DEEPSORT_MAX_IOU_DISTANCE,
            max_cosine_distance=DEEPSORT_MAX_COSINE_DISTANCE,
            nn_budget=DEEPSORT_NN_BUDGET
        )
