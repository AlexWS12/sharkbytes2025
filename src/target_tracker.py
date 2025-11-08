"""
Target Tracker Module
=====================
Manages target locking and tracking state for the sentry system.
"""

import time
from config.settings import TARGET_LOST_TIMEOUT


class TargetTracker:
    """Manages target locking and tracking state."""
    
    def __init__(self):
        """Initialize tracker state."""
        self.locked_id = None
        self.last_seen_time = None
        self.is_locked = False
        self.manual_lock_disabled = False  # Manual lock override
    
    def lock_target(self, track_id, verbose=True):
        """
        Lock onto a specific track ID.
        
        Args:
            track_id: The ID of the track to lock onto
            verbose: If True, print status messages
        """
        if not self.is_locked and not self.manual_lock_disabled:
            self.locked_id = track_id
            self.is_locked = True
            self.last_seen_time = time.time()
            if verbose:
                print(f"[TRACK] Locked onto target ID: {track_id}")
    
    def manual_unlock(self, verbose=True):
        """
        Manually unlock and disable auto-locking.
        
        Args:
            verbose: If True, print status messages
        """
        if self.is_locked and verbose:
            print(f"[TRACK] Manually unlocked from target ID: {self.locked_id}")
        
        self.unlock()
        self.manual_lock_disabled = True
        
        if verbose:
            print("[TRACK] Auto-lock DISABLED - Press 'L' to enable")
    
    def manual_lock_enable(self, verbose=True):
        """
        Re-enable auto-locking.
        
        Args:
            verbose: If True, print status messages
        """
        self.manual_lock_disabled = False
        if verbose:
            print("[TRACK] Auto-lock ENABLED - Will lock to next person detected")
    
    def update_target(self, track_id):
        """
        Update last seen time for the locked target.
        
        Args:
            track_id: The ID of the track being updated
        """
        if self.is_locked and track_id == self.locked_id:
            self.last_seen_time = time.time()
    
    def check_timeout(self, verbose=True):
        """
        Check if target has been lost for too long.
        
        Args:
            verbose: If True, print status messages
            
        Returns:
            bool: True if target timed out, False otherwise
        """
        if self.is_locked and self.last_seen_time is not None:
            elapsed = time.time() - self.last_seen_time
            if elapsed > TARGET_LOST_TIMEOUT:
                if verbose:
                    print(f"[TRACK] Target {self.locked_id} lost for {elapsed:.1f}s - unlocking")
                self.unlock()
                return True
        return False
    
    def unlock(self):
        """Unlock from current target."""
        self.locked_id = None
        self.is_locked = False
        self.last_seen_time = None
    
    def get_status(self):
        """
        Get current tracking status string.
        
        Returns:
            str: Human-readable status string
        """
        if self.manual_lock_disabled:
            return "MANUAL MODE (Lock OFF)"
        if self.is_locked:
            elapsed = time.time() - self.last_seen_time if self.last_seen_time else 0
            return f"LOCKED ID:{self.locked_id} ({elapsed:.1f}s)"
        return "SEARCHING"
    
    def is_tracking(self, track_id):
        """
        Check if currently tracking a specific ID.
        
        Args:
            track_id: The track ID to check
            
        Returns:
            bool: True if tracking this ID, False otherwise
        """
        return self.is_locked and track_id == self.locked_id
