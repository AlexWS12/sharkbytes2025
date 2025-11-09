#!/bin/bash

# ========================================
# Jetson Person-Tracking Sentry - Complete Setup
# ========================================
# Installs all dependencies for the person-tracking turret system
# 
# Hardware Requirements:
#   - Jetson device (Nano, Xavier, Orin, etc.)
#   - USB Camera (/dev/video0)
#   - PCA9685 Servo Driver (I2C address 0x40)
#   - 2x Servos (Pan: channel 0, Tilt: channel 1)
#
# Software Stack:
#   - YOLOv11n for person detection
#   - DeepSORT for tracking with persistent IDs
#   - Adafruit ServoKit for PCA9685 control
#   - OpenCV for camera interface
# ========================================

set -e  # Exit on error

echo ""
echo "=========================================="
echo "  Jetson Person-Tracking Sentry Setup"
echo "=========================================="
echo ""

# Check if running on Jetson
if ! command -v jetson_release &> /dev/null; then
    echo "⚠️  Warning: jetson_release not found."
    echo "   This script is designed for NVIDIA Jetson devices."
    read -p "   Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 1
    fi
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Check if virtual environment already exists
if [ -d "sentry_env" ]; then
    echo ""
    echo "⚠️  Virtual environment 'sentry_env' already exists."
    read -p "   Delete and recreate? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing virtual environment..."
        rm -rf sentry_env
    else
        echo "Using existing virtual environment..."
    fi
fi

# ========================================
# STEP 1: System Dependencies
# ========================================
echo ""
echo "=========================================="
echo "Step 1/5: Installing System Dependencies"
echo "=========================================="
echo ""

echo "Updating package lists..."
sudo apt-get update

echo "Installing required system packages..."
sudo apt-get install -y \
    python3-dev \
    python3-pip \
    python3-venv \
    i2c-tools \
    libopenblas-dev \
    libjpeg-dev \
    zlib1g-dev

echo "✓ System dependencies installed"

# Enable I2C if not already enabled
if ! groups | grep -q "i2c"; then
    echo "Adding user to i2c group..."
    sudo usermod -aG i2c $USER
    echo "⚠️  Note: You may need to log out and back in for i2c group to take effect"
fi

# ========================================
# STEP 2: Virtual Environment
# ========================================
echo ""
echo "=========================================="
echo "Step 2/5: Creating Virtual Environment"
echo "=========================================="
echo ""

if [ ! -d "sentry_env" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv sentry_env
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source sentry_env/bin/activate

# ========================================
# STEP 3: Python Base Packages
# ========================================
echo ""
echo "=========================================="
echo "Step 3/5: Installing Base Python Packages"
echo "=========================================="
echo ""

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing NumPy (Jetson-compatible version <2.0)..."
pip install --no-cache-dir "numpy<2"

echo "✓ Base packages installed"

# ========================================
# STEP 4: PyTorch with CUDA (JetPack 6.x)
# ========================================
echo ""
echo "=========================================="
echo "Step 4/5: Installing PyTorch with CUDA"
echo "=========================================="
echo ""

echo "Detecting JetPack version..."
JETPACK_VERSION=$(dpkg-query --showformat='${Version}' --show nvidia-jetpack 2>/dev/null || echo "unknown")
echo "JetPack: $JETPACK_VERSION"

echo ""
echo "Cleaning old packages..."
pip uninstall -y torch torchvision torchaudio 2>/dev/null || true

echo ""
echo "Installing PyTorch 2.5.0 with CUDA 12.6 (NVIDIA official wheel)..."
pip install --no-cache-dir \
  https://developer.download.nvidia.com/compute/redist/jp/v61/pytorch/torch-2.5.0a0+872d972e41.nv24.08.17622132-cp310-cp310-linux_aarch64.whl

echo ""
echo "Installing TorchVision 0.20.0 (ARM64)..."
pip install --no-cache-dir \
  https://github.com/ultralytics/assets/releases/download/v0.0.0/torchvision-0.20.0a0+afc54f7-cp310-cp310-linux_aarch64.whl

echo ""
echo "Verifying PyTorch installation..."
python3 << 'PYEOF'
import torch
print(f"PyTorch: {torch.__version__}")
print(f"CUDA Build: {torch.version.cuda}")
print(f"CUDA Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA Device: {torch.cuda.get_device_name(0)}")
else:
    print("⚠️  CUDA not available - may need to check installation")
PYEOF

echo "✓ PyTorch with CUDA installed"

# ========================================
# STEP 5: Application Dependencies
# ========================================
echo ""
echo "=========================================="
echo "Step 5/5: Installing Application Packages"
echo "=========================================="
echo ""

echo ""
echo "Installing computer vision packages..."
pip uninstall -y opencv-python 2>/dev/null || true
pip install --no-cache-dir opencv-python

echo "Installing YOLO (includes YOLOv11)..."
pip uninstall -y ultralytics 2>/dev/null || true
pip install --no-cache-dir ultralytics

echo "Installing tracking library..."
pip install deep-sort-realtime

echo "Installing servo control libraries..."
pip install adafruit-circuitpython-servokit
pip install adafruit-circuitpython-pca9685
pip install Jetson.GPIO

echo "✓ All application packages installed"

# ========================================
# Verification
# ========================================
echo ""
echo "=========================================="
echo "Verifying Installation"
echo "=========================================="
echo ""

echo ""
echo "Installed package versions:"
python3 << 'VEREOF'
import torch, torchvision, numpy as np, cv2
print(f"PyTorch:     {torch.__version__} (CUDA {torch.version.cuda})")
print(f"TorchVision: {torchvision.__version__}")
print(f"NumPy:       {np.__version__}")
print(f"OpenCV:      {cv2.__version__}")
print(f"CUDA:        {'✓ Available' if torch.cuda.is_available() else '✗ Not Available'}")
if torch.cuda.is_available():
    print(f"GPU:         {torch.cuda.get_device_name(0)}")
VEREOF

echo ""
pip list | grep -E "(ultralytics|deep-sort|adafruit-circuitpython-servokit|Jetson.GPIO)" | column -t

# ========================================
# Hardware Check
# ========================================
echo ""
echo "=========================================="
echo "Hardware Check"
echo "=========================================="
echo ""

echo "Checking for camera..."
if [ -e /dev/video0 ]; then
    echo "✓ Camera found at /dev/video0"
else
    echo "⚠️  No camera found at /dev/video0"
fi

echo ""
echo "Checking for PCA9685 on I2C..."
if command -v i2cdetect &> /dev/null; then
    echo "Scanning I2C bus 1..."
    if sudo i2cdetect -y 1 | grep -q "40"; then
        echo "✓ PCA9685 found at address 0x40"
    else
        echo "⚠️  PCA9685 not detected at 0x40"
        echo "   Make sure it's connected and powered"
    fi
else
    echo "⚠️  i2cdetect not available, skipping I2C check"
fi

# ========================================
# Download YOLOv11 Model
# ========================================
echo ""
echo "=========================================="
echo "Downloading YOLOv11 Model"
echo "=========================================="
echo ""

if [ ! -f "yolo11n.pt" ]; then
    echo "YOLOv11n model will be downloaded on first run."
    echo "This is a ~5.4MB download and will happen automatically."
else
    echo "✓ YOLOv11n model already present"
fi

# ========================================
# Final Instructions
# ========================================
echo ""
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "Project Structure:"
echo "  Sentry/"
echo "  ├── person_tracking_sentry.py    # Main script"
echo "  ├── sentry_env/                  # Virtual environment"
echo "  ├── yolo11n.pt                   # YOLO model (downloaded on first run)"
echo "  ├── README.md                    # Documentation"
echo "  ├── CONTROLS.md                  # Keyboard controls guide"
echo "  ├── TUNING_GUIDE.md              # Performance tuning"
echo "  └── VERSION_INFO.md              # Package versions & optimizations"
echo ""
echo "To run the sentry:"
echo "  1. Activate virtual environment:"
echo "     source sentry_env/bin/activate"
echo ""
echo "  2. Run the script:"
echo "     python3 person_tracking_sentry.py"
echo ""
echo "  3. Keyboard controls:"
echo "     L - Toggle auto-lock ON/OFF"
echo "     C - Center servos (when unlocked)"
echo "     Q - Quit"
echo ""
echo "Documentation:"
echo "  README.md         - Full setup and hardware wiring"
echo "  CONTROLS.md       - Detailed keyboard controls"
echo "  TUNING_GUIDE.md   - Performance and servo tuning"
echo "  VERSION_INFO.md   - Software versions and optimizations"
echo ""
echo "Current Status:"
echo "  • YOLOv11n for detection (latest, 22% faster than v8)"
echo "  • DeepSORT for tracking"
echo "  • PD controller for smooth servo motion"
echo "  • PyTorch 2.5.0 with CUDA 12.6 (JetPack 6.1)"
echo "  • Expected FPS: 10-15 (CPU), 25-35 (with CUDA)"
echo ""
echo "Note: This setup includes CUDA support for JetPack 6.x (Orin series)"
echo "      Using NVIDIA official PyTorch wheels for maximum compatibility"
echo ""
echo "=========================================="
echo ""
