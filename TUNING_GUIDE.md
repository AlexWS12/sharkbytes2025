# Performance Tuning Guide

## Quick Settings Reference

### Current Optimizations Applied:
- ✅ Reduced camera resolution: 416x416 (was 640x480)
- ✅ Frame skipping: Process detection every 2nd frame
- ✅ Increased servo speed: KP=0.08, MAX_STEP=8° (smoother tracking)
- ✅ Reduced deadband: 20px (more responsive)
- ✅ YOLO optimized: 416px inference, person-only detection
- ✅ Debug output disabled

### Expected Performance:
- **FPS**: 15-25 fps (was ~2 fps)
- **Tracking**: Smooth continuous motion
- **Responsiveness**: Quick servo updates

---

## If FPS is Still Low:

### Option 1: Increase Frame Skipping
```python
SKIP_FRAMES = 3  # Process every 3rd frame (currently 2)
```
**Trade-off**: Slightly delayed target acquisition, but smoother servo motion

### Option 2: Further Reduce Resolution
```python
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 320
```
**Trade-off**: Lower detection accuracy at distance

### Option 3: Use GPU Acceleration (if available)
The script already tries to use CUDA if available. Verify with:
```bash
python3 -c "import torch; print(torch.cuda.is_available())"
```

---

## If Tracking is Jerky/Not Smooth:

### Make Servos Slower (More Gradual)
```python
MAX_SERVO_STEP = 6.0  # Reduce from 8.0
KP = 0.06              # Reduce from 0.08
```

### Make Servos Faster (More Responsive)
```python
MAX_SERVO_STEP = 10.0  # Increase from 8.0
KP = 0.10              # Increase from 0.08
```

### Adjust Deadband
```python
DEADBAND_X = 30  # Increase to reduce small movements (currently 20)
DEADBAND_Y = 30  # Increase to reduce small movements (currently 20)
```

---

## If Servos Move Wrong Direction:

### Pan moves opposite:
```python
PAN_INVERT = 1  # Change from -1 to 1 (or vice versa)
```

### Tilt moves opposite:
```python
TILT_INVERT = 1  # Change from -1 to 1 (or vice versa)
```

---

## Performance vs Quality Balance

### Maximum FPS (lowest quality):
```python
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
SKIP_FRAMES = 3
```

### Balanced (recommended):
```python
CAMERA_WIDTH = 416
CAMERA_HEIGHT = 416
SKIP_FRAMES = 2
```

### Maximum Quality (lower FPS):
```python
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
SKIP_FRAMES = 1
```

---

## Servo Tuning Matrix

| Behavior | KP | MAX_STEP | Deadband | Result |
|----------|-----|----------|----------|---------|
| Too slow | ⬆️ 0.10 | ⬆️ 10° | Same | Faster response |
| Too jerky | ⬇️ 0.04 | ⬇️ 4° | ⬆️ 30px | Smoother motion |
| Jitters in center | Same | ⬇️ 3° | ⬆️ 40px | Stable when centered |
| Overshoots | ⬇️ 0.06 | ⬇️ 5° | Same | Less overshoot |

---

## Debug Mode

To enable debug output for troubleshooting, uncomment these lines in `control_servos_proportional()`:

```python
# Debug output (disabled for performance - uncomment if needed for debugging)
if error_x != 0 or error_y != 0:
    print(f"[TRACK] Error X: {error_x:+4.0f}px  Error Y: {error_y:+4.0f}px | "
          f"Delta Pan: {delta_pan:+.2f}°  Delta Tilt: {delta_tilt:+.2f}°")
```

This will show real-time tracking errors and servo movements.

---

## Quick Test After Changes

1. Stop current script: `Ctrl+C`
2. Edit `person_tracking_sentry.py`
3. Restart: `python3 person_tracking_sentry.py`
4. Observe FPS counter in video window
5. Test servo response by moving slowly

---

**Current Config Summary:**
- Resolution: 416x416
- Skip: Every 2nd frame
- KP: 0.08
- Max Step: 8°
- Deadband: 20px
- Pan Invert: -1
- Tilt Invert: -1
