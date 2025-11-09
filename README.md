# SharkBytes 2025 - Sentry Tracking System

AI-powered person tracking system with auto-scan and manual control capabilities.

## Quick Start

```bash
# Start the project
./start.sh

# Check status
./status.sh

# Stop the project
./stop.sh
```

Visit http://localhost:5173 to view the frontend.

## Project Structure

```
sharkbytes2025/
├── docs/                    # Documentation
│   ├── README.md           # Main documentation
│   ├── QUICK_START.md      # Quick start guide
│   ├── INTEGRATION_GUIDE.md
│   ├── PERFORMANCE_OPTIMIZATIONS.md
│   ├── TENSORRT_SETUP.md
│   └── ...
├── models/                  # AI models
│   ├── yolo11n.pt          # Base YOLO model
│   ├── yolo11n.onnx        # ONNX intermediate
│   └── yolo11n_160_fp16.engine  # TensorRT optimized
├── scripts/                 # Setup and control scripts
│   ├── setup_venv.sh       # Virtual environment setup
│   ├── start_project.sh    # Start all services
│   ├── stop_project.sh     # Stop all services
│   └── status_project.sh   # Check service status
├── tests/                   # Test and build scripts
│   ├── test_analyze_frame.py
│   ├── test_tensorrt.py
│   └── build_tensorrt_engine.py
├── sentry/                  # Sentry tracking service
├── web/                     # FastAPI backend
├── frontend/                # React frontend
├── mobile/                  # React Native mobile app
├── gemini/                  # Gemini AI integration
└── requirements.txt         # Python dependencies
```

## Features

- **Real-time person tracking** using YOLOv11 + DeepSORT
- **TensorRT optimization** for 2x YOLO speedup
- **Auto-scan mode** - automatically scans for targets
- **Manual control** - override with pan/tilt controls
- **Face detection** for improved tracking accuracy
- **Web interface** - React frontend with live video feed

## Performance

- **Average FPS**: 12-15 (peaks at 20-25)
- **YOLO inference**: 13-30ms (TensorRT optimized)
- **Resolution**: 320x320 camera input

## Documentation

See the `docs/` folder for detailed guides:
- [Quick Start Guide](docs/QUICK_START.md)
- [Performance Optimizations](docs/PERFORMANCE_OPTIMIZATIONS.md)
- [TensorRT Setup](docs/TENSORRT_SETUP.md)
- [Integration Guide](docs/INTEGRATION_GUIDE.md)

## Requirements

- Jetson Orin Nano (or compatible NVIDIA device)
- Python 3.10+
- CUDA 12.6+
- TensorRT 10.7+
- USB camera
- PCA9685 servo controller

## License

Copyright © 2025 SharkBytes
