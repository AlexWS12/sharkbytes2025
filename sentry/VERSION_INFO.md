# Package Versions & System Info# Version Information & Optimizations



## Current Installation ## Current Package Versions 



| Package | Version | Purpose || Package | Version | Notes |

|---------|---------|---------||---------|---------|-------|

| **PyTorch** | 2.5.0+nv24.08 | Deep learning framework (CUDA 12.6) || **ultralytics** | 8.3.225 | Latest - includes YOLOv11 |

| **TorchVision** | 0.20.0 | Vision models and transforms || **deep-sort-realtime** | 1.3.2 | Latest tracking library |

| **NumPy** | 1.26.4 | Array operations (Jetson-compatible) || **PyTorch** | 2.9.0 | Latest (CPU version) |

| **OpenCV** | 4.12.0 | Camera interface and image processing || **torchvision** | 0.24.0 | Latest |

| **Ultralytics** | 8.3.225 | YOLOv11 detection engine || **opencv-python** | 4.12.0.88 | Latest |

| **DeepSORT** | 1.3.2 | Multi-object tracking |

| **Adafruit ServoKit** | 1.3.22 | PCA9685 servo control |## YOLO Model Upgrade 

| **Jetson.GPIO** | 2.1.12 | Jetson GPIO interface |

### Changed from YOLOv8n --> YOLOv11n

## CUDA Status

**YOLOv11 Benefits:**

```-  **~22% faster** inference than YOLOv8

CUDA Build:      12.6-  **Higher mAP** (mean Average Precision) - better detection accuracy

CUDA Available:  [OK] Yes-  **Smaller model size** - same parameters, better optimization

GPU Device:      Orin-  **Improved person detection** at various distances

```-  **Better handling of occlusions** and partial views



## YOLOv11 vs YOLOv8### Model Comparison:



We use **YOLOv11n** (nano) for optimal performance:| Model | Parameters | Speed (ms) | mAP50 | Best For |

|-------|-----------|------------|-------|----------|

| Metric | YOLOv8n | YOLOv11n | Improvement || YOLOv8n | 3.2M | 80 | 37.3 | Old baseline |

|--------|---------|----------|-------------|| **YOLOv11n** | **2.6M** | **~62** | **39.5** | **Current *** |

| Parameters | 3.2M | 2.6M | -19% || YOLOv11s | 9.4M | ~110 | 47.0 | More accuracy |

| Inference Speed | ~80ms | ~62ms | +22% faster || YOLOv11m | 20.1M | ~185 | 51.5 | High accuracy |

| mAP50 | 37.3 | 39.5 | +2.2 points |

| Model Size | 6.2MB | 5.4MB | Smaller |**We're using YOLOv11n** - optimal balance of speed and accuracy for real-time tracking on Jetson.



**Result**: YOLOv11n gives better accuracy with faster speed!## Current Optimizations Applied



## System Optimizations### Camera Settings

```python

### Detection PipelineCAMERA_WIDTH = 320      # Small for max FPS

- Resolution: 320x320 (optimal for speed/quality)CAMERA_HEIGHT = 320     # Square for YOLO

- Model: yolo11n.pt (nano for real-time)TARGET_FPS = 30

- Confidence: 0.35```

- Classes: Person only (class 0)

- Max detections: 5### YOLO Inference

```python

### TrackingModel: yolo11n.pt       # Latest nano model

- DeepSORT with embedding networkImage size: 320px       # Matches camera

- Track persistence: 30 framesConfidence: 0.35        # Good balance

- IoU threshold: 0.7Max detections: 5       # Limit processing

- No frame skipping (realtime tracking)Classes: [0]            # Person only

Agnostic NMS: True     # Faster NMS

### Servo Control```

- Controller: PD (Proportional-Derivative)

- KP = 0.035 (proportional gain)### Servo Control (PD Controller)

- KD = 0.15 (derivative damping)```python

- Max step: 3deg/frameKP = 0.035              # Proportional gain (prevents overshoot)

- Deadband: 25pxKD = 0.15               # Derivative gain (damping)

MAX_SERVO_STEP = 3.0deg   # Smooth motion

### PerformanceDEADBAND = 25px         # Stable center

- FPS: 25-35 (with CUDA)```

- Latency: ~30-40ms

- Detection range: 2-15 meters### Tracking

```python

## Installation SourceDeepSORT: 1.3.2         # Latest tracker

Frame skip: DISABLED    # Process every frame (no stale boxes)

All packages installed from:Max age: 30 frames      # Track persistence

- **PyTorch**: NVIDIA official wheel (developer.download.nvidia.com)```

- **TorchVision**: Ultralytics ARM64 build (github.com/ultralytics)

- **Others**: PyPI standard packages## Expected Performance



## Compatibility### Current Setup (CPU):

- **FPS**: 10-15 fps

 Tested on: Jetson Orin Nano (JetPack 6.x)  - **Latency**: ~60-100ms

 Python: 3.10.12  - **Detection Range**: 2-15 meters

 CUDA: 12.6  - **Tracking**: Smooth, no overshoot

 Architecture: ARM64 (aarch64)

### With CUDA (Future):

## Upgrade Notes- **FPS**: 25-35 fps

- **Latency**: ~30-40ms

To update individual packages:- **Half Precision**: 2x speed boost possible



```bash## Performance Tips

source sentry_env/bin/activate

### To Further Increase FPS:

# Update Ultralytics (YOLO)1. **Enable CUDA** (if you get PyTorch with CUDA working)

pip install --upgrade ultralytics2. **Enable FP16**: Set `half=True` in detect_people()

3. **Reduce resolution**: Try 256x256 (but detection quality drops)

# Update DeepSORT4. **Use RTSP stream**: If using USB camera causes lag

pip install --upgrade deep-sort-realtime

### To Increase Detection Range:

# Update Adafruit libraries1. **Increase resolution**: Try 416x416 or 640x640

pip install --upgrade adafruit-circuitpython-servokit2. **Lower confidence**: Set `conf=0.25` (more false positives)

```3. **Use larger model**: Try `yolo11s.pt` (slower but better)



WARNING: **Do not upgrade PyTorch or NumPy** without testing - use versions specified in setup script.### To Improve Tracking Smoothness:

1. **Adjust KP**: Lower = slower, smoother (try 0.025-0.045)

---2. **Adjust MAX_STEP**: Lower = smoother (try 2-5deg)

3. **Increase deadband**: Less jitter near center (try 30-40px)

**Last Updated**: November 7, 2025  

**Setup Script**: setup_venv.sh (single-command installation)## Upgrade Path to CUDA


For Jetson Orin Nano with JetPack 5.x/6.x:

```bash
# Method 1: NVIDIA PyTorch wheel (Recommended)
# Visit: https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048
# Download appropriate wheel for your JetPack version
# Install: pip install <wheel-file>.whl

# Method 2: Try the provided script
./install_pytorch_jetson.sh
```

After CUDA is working:
1. Set `half=True` in code for FP16 inference
2. Verify with: `python3 -c "import torch; print(torch.cuda.is_available())"`
3. Should see 2-3x FPS improvement

## Comparison to Other Solutions

| Solution | FPS | Accuracy | Complexity |
|----------|-----|----------|------------|
| OpenCV Haar Cascades | 30+ | Low | Simple |
| MobileNet SSD | 20-25 | Medium | Medium |
| **YOLOv11n (current)** | **10-15** | **High** | **Medium** |
| YOLOv11s | 6-10 | Very High | Medium |
| YOLOv8x | 2-4 | Highest | High |

**Our choice (YOLOv11n)** provides the best balance for real-time tracking with persistent ID management.

## Version History

- **Nov 8, 2025**: Upgraded to YOLOv11n from YOLOv8n
- **Nov 8, 2025**: Initial setup with latest packages
- **ultralytics 8.3.225**: Includes YOLOv11 support

## Future Improvements

1.  YOLOv11 - **DONE**
2. PENDING: CUDA PyTorch for Jetson
3. FUTURE: Consider YOLOv11s if detection quality needed
4. FUTURE: Implement integral term for PID control (currently PD)
5. FUTURE: Add face detection for tighter tracking
6. FUTURE: Multi-person queue system

---

**Current Status**: Optimized with latest versions 
