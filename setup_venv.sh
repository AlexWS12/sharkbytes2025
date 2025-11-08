#!/bin/bash#!/bin/bash



# ========================================# ========================================

# Jetson Person-Tracking Sentry - Setup# Jetson Person-Tracking Sentry - Complete Setup

# ========================================# ========================================

# Complete installation for person-tracking turret# Installs all dependencies for the person-tracking turret system

# Tested on: Jetson Orin Nano (JetPack 6.x)# 

# # Hardware Requirements:

# Hardware: USB Camera + PCA9685 + 2 Servos#   - Jetson device (Nano, Xavier, Orin, etc.)

# Software: YOLOv11 + DeepSORT + PyTorch (CUDA)#   - USB Camera (/dev/video0)

# ========================================#   - PCA9685 Servo Driver (I2C address 0x40)

#   - 2x Servos (Pan: channel 0, Tilt: channel 1)

set -e  # Exit on error#

# Software Stack:

echo ""#   - YOLOv11n for person detection

echo "=========================================="#   - DeepSORT for tracking with persistent IDs

echo "  Person-Tracking Sentry Setup"#   - Adafruit ServoKit for PCA9685 control

echo "=========================================="#   - OpenCV for camera interface

echo "  Hardware: Jetson with USB camera"# ========================================

echo "  Software: YOLOv11 + PyTorch CUDA"

echo "=========================================="set -e  # Exit on error

echo ""

echo ""

# ========================================echo "=========================================="

# STEP 1: System Dependenciesecho "  Jetson Person-Tracking Sentry Setup"

# ========================================echo "=========================================="

echo "Step 1/6: System Dependencies"echo ""

echo "----------------------------------------"

# Check if running on Jetson

sudo apt-get updateif ! command -v jetson_release &> /dev/null; then

sudo apt-get install -y \    echo "⚠️  Warning: jetson_release not found."

    python3-dev \    echo "   This script is designed for NVIDIA Jetson devices."

    python3-pip \    read -p "   Continue anyway? (y/n) " -n 1 -r

    python3-venv \    echo

    i2c-tools \    if [[ ! $REPLY =~ ^[Yy]$ ]]; then

    libopenblas-dev \        echo "Setup cancelled."

    libjpeg-dev \        exit 1

    zlib1g-dev    fi

fi

# Enable I2C

if ! groups | grep -q "i2c"; then# Check Python version

    sudo usermod -aG i2c $USERPYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')

    echo "⚠️  Added to i2c group - logout/login required"echo "✓ Python version: $PYTHON_VERSION"

fi

# Check if virtual environment already exists

echo "✓ System dependencies installed"if [ -d "sentry_env" ]; then

echo ""    echo ""

    echo "⚠️  Virtual environment 'sentry_env' already exists."

# ========================================    read -p "   Delete and recreate? (y/n) " -n 1 -r

# STEP 2: Virtual Environment    echo

# ========================================    if [[ $REPLY =~ ^[Yy]$ ]]; then

echo "Step 2/6: Virtual Environment"        echo "Removing existing virtual environment..."

echo "----------------------------------------"        rm -rf sentry_env

    else

if [ -d "sentry_env" ]; then        echo "Using existing virtual environment..."

    echo "Removing existing virtual environment..."    fi

    rm -rf sentry_envfi

fi

# ========================================

python3 -m venv sentry_env# STEP 1: System Dependencies

source sentry_env/bin/activate# ========================================

echo ""

echo "✓ Virtual environment created"echo "=========================================="

echo ""echo "Step 1/5: Installing System Dependencies"

echo "=========================================="

# ========================================echo ""

# STEP 3: Upgrade pip

# ========================================echo "Updating package lists..."

echo "Step 3/6: Upgrade pip"sudo apt-get update

echo "----------------------------------------"

echo "Installing required system packages..."

pip install --upgrade pipsudo apt-get install -y \

    python3-dev \

echo "✓ pip upgraded"    python3-pip \

echo ""    python3-venv \

    i2c-tools \

# ========================================    libopenblas-dev \

# STEP 4: Clean slate    libjpeg-dev \

# ========================================    zlib1g-dev

echo "Step 4/6: Clean old packages"

echo "----------------------------------------"echo "✓ System dependencies installed"



pip uninstall -y torch torchvision torchaudio numpy ultralytics opencv-python 2>/dev/null || true# Enable I2C if not already enabled

if ! groups | grep -q "i2c"; then

echo "✓ Old packages removed"    echo "Adding user to i2c group..."

echo ""    sudo usermod -aG i2c $USER

    echo "⚠️  Note: You may need to log out and back in for i2c group to take effect"

# ========================================fi

# STEP 5: Install Core Packages

# ========================================# ========================================

echo "Step 5/6: Install Core Packages"# STEP 2: Virtual Environment

echo "----------------------------------------"# ========================================

echo ""

echo "Installing NumPy 1.x (Jetson-compatible)..."echo "=========================================="

pip install --no-cache-dir "numpy<2"echo "Step 2/5: Creating Virtual Environment"

echo "=========================================="

echo "Installing PyTorch 2.5.0 with CUDA 12.6..."echo ""

pip install --no-cache-dir \

  https://developer.download.nvidia.com/compute/redist/jp/v61/pytorch/torch-2.5.0a0+872d972e41.nv24.08.17622132-cp310-cp310-linux_aarch64.whlif [ ! -d "sentry_env" ]; then

    echo "Creating Python virtual environment..."

echo "Installing TorchVision 0.20.0..."    python3 -m venv sentry_env

pip install --no-cache-dir \    echo "✓ Virtual environment created"

  https://github.com/ultralytics/assets/releases/download/v0.0.0/torchvision-0.20.0a0+afc54f7-cp310-cp310-linux_aarch64.whlelse

    echo "✓ Virtual environment already exists"

echo "Installing OpenCV..."fi

pip install --no-cache-dir opencv-python

# Activate virtual environment

echo "Installing Ultralytics (YOLOv11)..."echo "Activating virtual environment..."

pip install --no-cache-dir ultralyticssource sentry_env/bin/activate



echo "✓ Core packages installed"# ========================================

echo ""# STEP 3: Python Base Packages

# ========================================

# ========================================echo ""

# STEP 6: Install Application Packagesecho "=========================================="

# ========================================echo "Step 3/5: Installing Base Python Packages"

echo "Step 6/6: Install Application Packages"echo "=========================================="

echo "----------------------------------------"echo ""



echo "Installing DeepSORT tracker..."echo "Upgrading pip..."

pip install --no-cache-dir deep-sort-realtimepip install --upgrade pip



echo "Installing Adafruit libraries..."echo "Installing NumPy (Jetson-compatible version <2.0)..."

pip install --no-cache-dir adafruit-circuitpython-servokitpip install --no-cache-dir "numpy<2"

pip install --no-cache-dir adafruit-circuitpython-pca9685

echo "✓ Base packages installed"

echo "Installing Jetson GPIO..."

pip install --no-cache-dir Jetson.GPIO# ========================================

# STEP 4: PyTorch with CUDA (JetPack 6.x)

echo "✓ Application packages installed"# ========================================

echo ""echo ""

echo "=========================================="

# ========================================echo "Step 4/5: Installing PyTorch with CUDA"

# Verificationecho "=========================================="

# ========================================echo ""

echo "=========================================="

echo "  Verification"echo "Detecting JetPack version..."

echo "=========================================="JETPACK_VERSION=$(dpkg-query --showformat='${Version}' --show nvidia-jetpack 2>/dev/null || echo "unknown")

echo ""echo "JetPack: $JETPACK_VERSION"



python3 << 'EOF'echo ""

import torch, torchvision, cv2, numpy as npecho "Cleaning old packages..."

pip uninstall -y torch torchvision torchaudio 2>/dev/null || true

print("Package Versions:")

print(f"  PyTorch:     {torch.__version__}")echo ""

print(f"  TorchVision: {torchvision.__version__}")echo "Installing PyTorch 2.5.0 with CUDA 12.6 (NVIDIA official wheel)..."

print(f"  NumPy:       {np.__version__}")pip install --no-cache-dir \

print(f"  OpenCV:      {cv2.__version__}")  https://developer.download.nvidia.com/compute/redist/jp/v61/pytorch/torch-2.5.0a0+872d972e41.nv24.08.17622132-cp310-cp310-linux_aarch64.whl

print()

print("CUDA Status:")echo ""

print(f"  CUDA Build:  {torch.version.cuda}")echo "Installing TorchVision 0.20.0 (ARM64)..."

print(f"  CUDA Avail:  {torch.cuda.is_available()}")pip install --no-cache-dir \

if torch.cuda.is_available():  https://github.com/ultralytics/assets/releases/download/v0.0.0/torchvision-0.20.0a0+afc54f7-cp310-cp310-linux_aarch64.whl

    print(f"  GPU Device:  {torch.cuda.get_device_name(0)}")

else:echo ""

    print("  ⚠️  CUDA not available")echo "Verifying PyTorch installation..."

print()python3 << 'PYEOF'

import torch

# Quick package checkprint(f"PyTorch: {torch.__version__}")

try:print(f"CUDA Build: {torch.version.cuda}")

    from ultralytics import YOLOprint(f"CUDA Available: {torch.cuda.is_available()}")

    from deep_sort_realtime.deepsort_tracker import DeepSortif torch.cuda.is_available():

    from adafruit_servokit import ServoKit    print(f"CUDA Device: {torch.cuda.get_device_name(0)}")

    print("Package Imports: ✓ All packages accessible")else:

except ImportError as e:    print("⚠️  CUDA not available - may need to check installation")

    print(f"Package Import Error: {e}")PYEOF

EOF

echo "✓ PyTorch with CUDA installed"

echo ""

# ========================================

# Hardware check# STEP 5: Application Dependencies

echo "Hardware Check:"# ========================================

if [ -e /dev/video0 ]; thenecho ""

    echo "  Camera:      ✓ /dev/video0"echo "=========================================="

elseecho "Step 5/5: Installing Application Packages"

    echo "  Camera:      ⚠️  Not found at /dev/video0"echo "=========================================="

fiecho ""



if sudo i2cdetect -y 1 2>/dev/null | grep -q "40"; thenecho ""

    echo "  PCA9685:     ✓ Detected at 0x40"echo "Installing computer vision packages..."

elsepip uninstall -y opencv-python 2>/dev/null || true

    echo "  PCA9685:     ⚠️  Not detected (check wiring)"pip install --no-cache-dir opencv-python

fi

echo "Installing YOLO (includes YOLOv11)..."

echo ""pip uninstall -y ultralytics 2>/dev/null || true

pip install --no-cache-dir ultralytics

# ========================================

# Completeecho "Installing tracking library..."

# ========================================pip install deep-sort-realtime

echo "=========================================="

echo "  ✓ Setup Complete!"echo "Installing servo control libraries..."

echo "=========================================="pip install adafruit-circuitpython-servokit

echo ""pip install adafruit-circuitpython-pca9685

echo "To run the sentry:"pip install Jetson.GPIO

echo "  1. source sentry_env/bin/activate"

echo "  2. python3 person_tracking_sentry.py"echo "✓ All application packages installed"

echo ""

echo "Controls:"# ========================================

echo "  L - Toggle lock ON/OFF"# Verification

echo "  C - Center servos"# ========================================

echo "  Q - Quit"echo ""

echo ""echo "=========================================="

echo "Documentation:"echo "Verifying Installation"

echo "  README.md       - Full guide"echo "=========================================="

echo "  CONTROLS.md     - Keyboard controls"echo ""

echo "  TUNING_GUIDE.md - Performance tuning"

echo ""echo ""

echo "Expected FPS: 25-35 (with CUDA)"echo "Installed package versions:"

echo "=========================================="python3 << 'VEREOF'

echo ""import torch, torchvision, numpy as np, cv2

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
echo "  Eve Security/"
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
echo "For CUDA support (optional, better FPS):"
echo "  ./install_pytorch_jetson.sh"
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
