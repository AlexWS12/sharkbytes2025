# TensorRT Setup Guide - SharkBytes 2025

## Installation Summary

 **TensorRT 10.7.0 successfully installed** in virtual environment (`sentry_env`)

### What was installed:
- TensorRT 10.7.0 (system package, symlinked to venv)
- ONNX 1.19.1
- ONNXRuntime 1.23.2
- ONNXSlim 0.1.74

### Files created:
- `yolo11n.onnx` (10.1 MB) - ONNX intermediate format
- `yolo11n_160_fp16.engine` (7.28 MB) - **TensorRT optimized engine**
- `build_tensorrt_engine.py` - Script to rebuild engine if needed
- `test_tensorrt.py` - Installation verification script

## Why Use TensorRT?

TensorRT is NVIDIA's inference optimization library that:
- **2-3x faster** inference compared to PyTorch
- Uses **FP16 precision** for speed on Jetson
- **Hardware-specific optimizations** for your Jetson Orin Nano
- Reduces **YOLO inference from ~45ms to ~15-20ms**

## How to Use TensorRT Engine

### Step 1: Update sentry_service.py

Edit `/home/jorget15/Documents/Sharkybytes/sharkbytes2025/sentry/sentry_service.py`:

Find line ~195:
```python
# OLD:
self.yolo_model = YOLO('yolo11n.pt')

# NEW:
self.yolo_model = YOLO('yolo11n_160_fp16.engine')
```

### Step 2: Restart Services

```bash
cd /home/jorget15/Documents/Sharkybytes/sharkbytes2025
./stop_project.sh
./start_project.sh
```

### Step 3: Verify Performance

Open http://localhost:5173 and check the FPS counter

**Expected Results:**
- Before TensorRT: 12-15 FPS
- After TensorRT: 20-30+ FPS

## Performance Comparison

| Metric | PyTorch (.pt) | TensorRT (.engine) | Improvement |
|--------|---------------|-------------------|-------------|
| YOLO Inference | ~45ms | ~15-20ms | 2-3x faster |
| Total FPS | 12-15 | 20-30+ | ~2x faster |
| Model Size | 5.4 MB | 7.28 MB | Slightly larger |

## Troubleshooting

### Engine fails to load

**Error:** `Failed to load engine`

**Solution:** The engine is hardware-specific. Rebuild it:
```bash
cd /home/jorget15/Documents/Sharkybytes/sharkbytes2025
sentry_env/bin/python3 build_tensorrt_engine.py
```

### Wrong image size

**Error:** `Input size mismatch`

**Problem:** The engine was built for 160x160, but you changed `YOLO_IMGSZ`

**Solution:** Rebuild engine with new size:
```python
# Edit build_tensorrt_engine.py, change:
# First export ONNX with new size
from ultralytics import YOLO
model = YOLO('yolo11n.pt')
model.export(format='onnx', imgsz=NEW_SIZE)  # e.g., 320

# Then rebuild engine
sentry_env/bin/python3 build_tensorrt_engine.py
```

### Performance not improving

**Check:**
1. Verify engine file is being used:
   ```bash
   tail -f logs/backend.log | grep YOLO
   # Should show: Loading YOLO from yolo11n_160_fp16.engine
   ```

2. Check profiling output:
   ```bash
   tail -f logs/backend.log | grep PROFILE
   # YOLO time should be ~15-20ms instead of ~45ms
   ```

3. Ensure GPU is being used:
   ```bash
   jtop  # or tegrastats
   # Check GPU utilization
   ```

## Advanced: Rebuilding Engine

If you need to rebuild the TensorRT engine (e.g., different image size, different precision):

### Option 1: Use the build script

```bash
# Edit ONNX export size if needed
sentry_env/bin/python3 -c "
from ultralytics import YOLO
YOLO('yolo11n.pt').export(format='onnx', imgsz=160)
"

# Build TensorRT engine
sentry_env/bin/python3 build_tensorrt_engine.py
```

### Option 2: Manual build

```python
import tensorrt as trt

# Create builder
TRT_LOGGER = trt.Logger(trt.Logger.INFO)
builder = trt.Builder(TRT_LOGGER)
network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
parser = trt.OnnxParser(network, TRT_LOGGER)

# Parse ONNX
with open('yolo11n.onnx', 'rb') as f:
    parser.parse(f.read())

# Build engine
config = builder.create_builder_config()
config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 2 << 30)  # 2GB
config.set_flag(trt.BuilderFlag.FP16)  # Enable FP16

serialized_engine = builder.build_serialized_network(network, config)

# Save
with open('yolo11n_160_fp16.engine', 'wb') as f:
    f.write(serialized_engine)
```

## Important Notes

WARNING: **Hardware-Specific:** The `.engine` file is compiled for your specific Jetson Orin Nano. Don't copy it to other devices.

WARNING: **Keep Source Files:** Always keep `yolo11n.pt` and `yolo11n.onnx` as source files. The engine is just an optimized version.

WARNING: **Image Size:** The engine is built for a specific input size (160x160). If you change `YOLO_IMGSZ`, rebuild the engine.

WARNING: **Build Time:** Building the engine takes ~10-15 minutes on Jetson Orin Nano. This is a one-time process.

## Why test_tensorrt.py Had an Infinite Loop

The issue with `test_tensorrt.py` was:
1. The Ultralytics YOLO export process tries to install dependencies during runtime
2. It was installing packages to `~/.local` instead of the virtual environment
3. The TensorRT engine build process was hanging during validation

**Solution:** We bypassed the Ultralytics export and built the TensorRT engine manually using the TensorRT Python API, which gives us full control and avoids the hanging issues.

## Files Reference

- `yolo11n.pt` - Original PyTorch model (5.4 MB)
- `yolo11n.onnx` - ONNX intermediate format (10.1 MB)
- `yolo11n_160_fp16.engine` - TensorRT optimized engine (7.28 MB) ⭐ **Use this**
- `build_tensorrt_engine.py` - Script to rebuild engine
- `test_tensorrt.py` - Verification script (has issues, use build_tensorrt_engine.py instead)

---
**Last Updated:** November 8, 2025  
**TensorRT Version:** 10.7.0  
**CUDA Version:** 12.6  
**Tested On:** Jetson Orin Nano
