# Performance Tuning Guide# Performance Tuning Guide



> **Note:** With the new modular structure, all settings are in `config/settings.py`> **Note:** With the new modular structure, all settings are in `config/settings.py`



## Quick Settings Reference## Quick Settings Reference



### Current Optimizations Applied:### Current Optimizations Applied:

-  Small camera resolution: 320x320 for speed-  Small camera resolution: 320x320 for speed

-  Smooth servo control: KP=0.020, MAX_STEP=1.5deg-  Smooth servo control: KP=0.020, MAX_STEP=1.5deg

-  Exponential smoothing: 0.3 factor for gimbal-like motion-  Exponential smoothing: 0.3 factor for gimbal-like motion

-  PD control: KD=0.25 for damping-  PD control: KD=0.25 for damping

-  Deadband: 25px to reduce jitter-  Deadband: 25px to reduce jitter

-  YOLO optimized: YOLOv11n, person-only detection-  YOLO optimized: YOLOv11n, person-only detection

-  Frame processing: Every frame for smooth tracking-  Frame processing: Every frame for smooth tracking



### Expected Performance:### Expected Performance:

- **FPS**: 15-30 fps (depending on hardware)- **FPS**: 15-30 fps (depending on hardware)

- **Tracking**: Smooth, cinematic motion- **Tracking**: Smooth, cinematic motion

- **Responsiveness**: Natural gimbal-like follow- **Responsiveness**: Natural gimbal-like follow



------



## Adjusting Parameters## Adjusting Parameters



**All settings are in:** `config/settings.py`**All settings are in:** `config/settings.py`



### Camera Resolution & Performance### Camera Resolution & Performance

### Camera Resolution & Performance

#### For Better FPS:

```python**Location:** `config/settings.py`

CAMERA_WIDTH = 320   # Current setting - good balance

CAMERA_HEIGHT = 240  # Even faster#### For Better FPS:

``````python

CAMERA_WIDTH = 320   # Current setting - good balance

#### For Better Detection Quality:CAMERA_HEIGHT = 240  # Even faster

```python```

CAMERA_WIDTH = 640

CAMERA_HEIGHT = 480#### For Better Detection Quality:

``````python

**Trade-off**: Lower FPS, better long-distance detectionCAMERA_WIDTH = 640

CAMERA_HEIGHT = 480

---```

**Trade-off**: Lower FPS, better long-distance detection

## Smoothness vs Speed Trade-offs

---

### Make Motion SMOOTHER (More Cinematic)

## Smoothness vs Speed Trade-offs

**Edit:** `config/settings.py`

### Make Motion SMOOTHER (More Cinematic)

```python```python

# Reduce proportional gain (slower corrections)MAX_SERVO_STEP = 6.0  # Reduce from 8.0

KP = 0.015  # Lower from 0.020KP = 0.06              # Reduce from 0.08

```

# Limit servo speed even more

MAX_SERVO_STEP = 1.0  # Lower from 1.5### Make Servos Faster (More Responsive)

```python

# Increase smoothing (more lag, but silkier)MAX_SERVO_STEP = 10.0  # Increase from 8.0

SMOOTHING_FACTOR = 0.2  # Lower from 0.3KP = 0.10              # Increase from 0.08

```

# Increase damping (prevent overshoot)

KD = 0.30  # Higher from 0.25### Adjust Deadband

``````python

DEADBAND_X = 30  # Increase to reduce small movements (currently 20)

**Effect:** Very smooth, gimbal-like motion (slightly slower response)DEADBAND_Y = 30  # Increase to reduce small movements (currently 20)

```

### Make Motion FASTER (More Responsive)

---

**Edit:** `config/settings.py`

## If Servos Move Wrong Direction:

```python

# Increase proportional gain### Pan moves opposite:

KP = 0.030  # Higher from 0.020```python

PAN_INVERT = 1  # Change from -1 to 1 (or vice versa)

# Allow faster servo movement```

MAX_SERVO_STEP = 2.5  # Higher from 1.5

### Tilt moves opposite:

# Reduce smoothing (less lag)```python

SMOOTHING_FACTOR = 0.4  # Higher from 0.3TILT_INVERT = 1  # Change from -1 to 1 (or vice versa)

```

# Reduce damping slightly

KD = 0.20  # Lower from 0.25---

```

## Performance vs Quality Balance

**Effect:** Snappier tracking (may be less smooth)

### Maximum FPS (lowest quality):

---```python

CAMERA_WIDTH = 320

## Detection & Tracking TuningCAMERA_HEIGHT = 240

SKIP_FRAMES = 3

### Reduce False Positives```



**Edit:** `config/settings.py`### Balanced (recommended):

```python

```pythonCAMERA_WIDTH = 416

YOLO_CONFIDENCE = 0.45  # Increase from 0.35CAMERA_HEIGHT = 416

```SKIP_FRAMES = 2

```

**Effect:** Fewer false detections, but may miss distant people

### Maximum Quality (lower FPS):

### Faster Detection (Lower FPS Cost)```python

CAMERA_WIDTH = 640

**Edit:** `config/settings.py`CAMERA_HEIGHT = 480

SKIP_FRAMES = 1

```python```

YOLO_MAX_DETECTIONS = 3  # Reduce from 5

CAMERA_WIDTH = 320       # Already optimized---

```

## Servo Tuning Matrix

### Longer Lock Duration

| Behavior | KP | MAX_STEP | Deadband | Result |

**Edit:** `config/settings.py`|----------|-----|----------|----------|---------|

| Too slow | UP 0.10 | UP 10deg | Same | Faster response |

```python| Too jerky | DOWN 0.04 | DOWN 4deg | UP 30px | Smoother motion |

TARGET_LOST_TIMEOUT = 3.0  # Increase from 2.0 seconds| Jitters in center | Same | DOWN 3deg | UP 40px | Stable when centered |

```| Overshoots | DOWN 0.06 | DOWN 5deg | Same | Less overshoot |



**Effect:** Won't unlock as quickly when person briefly disappears---



---## Debug Mode



## Servo Limits & SafetyTo enable debug output for troubleshooting, uncomment these lines in `control_servos_proportional()`:



### Restrict Movement Range```python

# Debug output (disabled for performance - uncomment if needed for debugging)

**Edit:** `config/settings.py`if error_x != 0 or error_y != 0:

    print(f"[TRACK] Error X: {error_x:+4.0f}px  Error Y: {error_y:+4.0f}px | "

```python          f"Delta Pan: {delta_pan:+.2f}deg  Delta Tilt: {delta_tilt:+.2f}deg")

# Pan limits (horizontal)```

PAN_MIN = 30   # Increase from 10

PAN_MAX = 150  # Decrease from 170This will show real-time tracking errors and servo movements.



# Tilt limits (vertical)---

TILT_MIN = 40  # Increase from 20

TILT_MAX = 130 # Decrease from 150## Quick Test After Changes

```

1. Stop current script: `Ctrl+C`

### Change Default Position2. Edit `person_tracking_sentry.py`

3. Restart: `python3 person_tracking_sentry.py`

**Edit:** `config/settings.py`4. Observe FPS counter in video window

5. Test servo response by moving slowly

```python

PAN_DEFAULT = 90   # Center position---

TILT_DEFAULT = 80  # Slightly down

```**Current Config Summary:**

- Resolution: 416x416

### If Servos Move Wrong Direction- Skip: Every 2nd frame

- KP: 0.08

**Edit:** `config/settings.py`- Max Step: 8deg

- Deadband: 20px

```python- Pan Invert: -1

PAN_INVERT = 1   # Change from -1 (or vice versa)- Tilt Invert: -1

TILT_INVERT = 1  # Change from -1 (or vice versa)
```

---

## Deadband Tuning

### Reduce Jitter (Wider Deadband)

**Edit:** `config/settings.py`

```python
DEADBAND_X = 35  # Increase from 25
DEADBAND_Y = 35  # Increase from 25
```

**Effect:** Less jittery when target is near center, but less precise centering

### More Precise Centering (Narrow Deadband)

**Edit:** `config/settings.py`

```python
DEADBAND_X = 15  # Decrease from 25
DEADBAND_Y = 15  # Decrease from 25
```

**Effect:** More precise, but may cause micro-jitter

---

## Sweep Behavior (When No Target)

### Faster Sweep Speed

**Edit:** `config/settings.py`

```python
SWEEP_SPEED = 1.0  # Increase from 0.5 degrees/frame
```

### Wider Sweep Range

**Edit:** `config/settings.py`

```python
SWEEP_MIN = 10   # Lower from 30
SWEEP_MAX = 170  # Higher from 150
```

---

## Testing Your Changes

After editing `config/settings.py`:

1. Save the file
2. Run the system:
   ```bash
   python person_tracking_sentry.py
   ```
3. Observe behavior
4. Press **Q** to quit
5. Adjust and repeat

### Quick Test Checklist

- [ ] Motion is smooth (not jerky)
- [ ] Tracking is responsive (not laggy)
- [ ] FPS is acceptable (15+ fps)
- [ ] No oscillation around target
- [ ] Servo movement feels natural
- [ ] Center deadband reduces jitter

---

## Recommended Presets

### Preset 1: Maximum Smoothness
```python
KP = 0.015
KD = 0.30
MAX_SERVO_STEP = 1.0
SMOOTHING_FACTOR = 0.2
DEADBAND_X = 30
DEADBAND_Y = 30
```

### Preset 2: Balanced (Default)
```python
KP = 0.020
KD = 0.25
MAX_SERVO_STEP = 1.5
SMOOTHING_FACTOR = 0.3
DEADBAND_X = 25
DEADBAND_Y = 25
```

### Preset 3: Fast Response
```python
KP = 0.030
KD = 0.20
MAX_SERVO_STEP = 2.5
SMOOTHING_FACTOR = 0.4
DEADBAND_X = 20
DEADBAND_Y = 20
```

### Preset 4: Maximum Performance (FPS)
```python
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
YOLO_CONFIDENCE = 0.40
YOLO_MAX_DETECTIONS = 3
```

---

## Understanding the Parameters

### KP (Proportional Gain)
- **What it does:** Controls how aggressively servos move toward target
- **Higher:** Faster corrections, may overshoot
- **Lower:** Slower, smoother corrections
- **Range:** 0.010 - 0.050

### KD (Derivative Gain)
- **What it does:** Dampens movement to prevent overshoot
- **Higher:** More damping, smoother deceleration
- **Lower:** Less damping, may oscillate
- **Range:** 0.10 - 0.40

### MAX_SERVO_STEP
- **What it does:** Limits maximum servo movement per frame
- **Higher:** Faster movement possible
- **Lower:** Forces gradual movement
- **Range:** 0.5 - 5.0 degrees

### SMOOTHING_FACTOR
- **What it does:** Blends current and previous target positions
- **Higher (closer to 1):** Less smoothing, more responsive
- **Lower (closer to 0):** More smoothing, laggier
- **Range:** 0.1 - 0.5

### DEADBAND
- **What it does:** Creates "don't move" zone near center
- **Higher:** Reduces jitter, less precise
- **Lower:** More precise, may jitter
- **Range:** 10 - 40 pixels

---

## Advanced: PID Control Tuning

The system uses PD control (Proportional-Derivative). For advanced users:

### Current Formula:
```python
delta = (error * KP) - (derivative * KD)
```

### If Overshooting:
1. Increase KD (more damping)
2. Decrease KP (less aggressive)

### If Too Slow:
1. Increase KP (more aggressive)
2. Decrease KD (less damping)

### If Oscillating:
1. Increase KD significantly
2. Add more smoothing (lower SMOOTHING_FACTOR)

---

## GPU Acceleration

If you have CUDA available:

**Edit:** `src/detector.py`
```python
# In PersonDetector.detect() method
half=True,  # Change from False - enables FP16
```

**Check CUDA availability:**
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

---

## Monitoring Performance

### Watch FPS Counter
Displayed in top-left of video window

### Watch Status
- `SEARCHING` - Looking for people
- `LOCKED ID:X` - Tracking person X
- `MANUAL MODE` - Auto-lock disabled

### Watch Servo Angles
Displayed below status showing current Pan/Tilt

---

## Common Issues & Solutions

### Servo Moves Too Fast
--> Lower `MAX_SERVO_STEP`  
--> Lower `KP`

### Servo Too Slow
--> Increase `MAX_SERVO_STEP`  
--> Increase `KP`

### Jittery Near Center
--> Increase `DEADBAND_X` and `DEADBAND_Y`

### Overshoots Target
--> Increase `KD`  
--> Lower `SMOOTHING_FACTOR`

### Lags Behind Fast Movement
--> Increase `SMOOTHING_FACTOR`  
--> Increase `KP`

---

**For more details, see:** `README.md` and `ARCHITECTURE.md`
