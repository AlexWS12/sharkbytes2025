#!/usr/bin/env python3
"""
Test TensorRT installation and export YOLO model to TensorRT engine
"""

import sys
import os

print("="*60)
print("TensorRT Installation Test")
print("="*60)

# Test TensorRT import
try:
    import tensorrt as trt
    print(f"✓ TensorRT version: {trt.__version__}")
    print(f"✓ TensorRT Builder: {trt.Builder is not None}")
except ImportError as e:
    print(f"✗ TensorRT import failed: {e}")
    sys.exit(1)

# Test dependencies
try:
    from ultralytics import YOLO
    import torch
    import onnx
    
    print(f"✓ Ultralytics YOLO available")
    print(f"✓ PyTorch version: {torch.__version__}")
    print(f"✓ CUDA available: {torch.cuda.is_available()}")
    print(f"✓ ONNX version: {onnx.__version__}")
    
except ImportError as e:
    print(f"✗ Missing dependency: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("All dependencies installed successfully!")
print("="*60)

# Ask user before exporting (export can take time)
print("\nWould you like to export YOLO11n to TensorRT engine?")
print("This will take 3-5 minutes and requires:")
print("  - 160x160 image size (optimized for your settings)")
print("  - FP16 precision for speed")
print("  - ~50-100MB disk space")
print("\nType 'yes' to proceed, or any other key to skip:")

try:
    response = input().strip().lower()
    if response != 'yes':
        print("\nSkipping export. TensorRT is installed and ready.")
        print("You can export manually later using:")
        print("  yolo export model=yolo11n.pt format=engine imgsz=160 half=True")
        sys.exit(0)
except KeyboardInterrupt:
    print("\n\nExport cancelled by user")
    sys.exit(0)

# Export to TensorRT
try:
    print("\n📦 Loading YOLO11n model...")
    model = YOLO('yolo11n.pt')
    print("✓ YOLO11n model loaded")
    
    print("\n🔄 Exporting to TensorRT engine...")
    print("   This will take 3-5 minutes...")
    print("   Progress:")
    
    # Export with settings optimized for Jetson
    # The export process includes ONNX conversion first, then TensorRT optimization
    engine_path = model.export(
        format='engine',           # TensorRT engine format
        imgsz=160,                 # Match our optimized size
        half=True,                 # Use FP16 for speed
        device=0,                  # Use GPU
        workspace=2,               # Workspace size in GB
        simplify=True,             # Simplify ONNX model
        verbose=False              # Reduce output spam
    )
    
    print(f"\n✓ TensorRT engine exported successfully!")
    print(f"✓ Engine saved to: {engine_path}")
    
    if os.path.exists(engine_path):
        print(f"✓ File size: {os.path.getsize(engine_path) / (1024*1024):.2f} MB")
    
    print("\n" + "="*60)
    print("SUCCESS! TensorRT engine is ready")
    print("="*60)
    print("\nNext steps:")
    print("1. Update sentry_service.py to use:", engine_path)
    print("2. Change: YOLO('yolo11n.pt') → YOLO('yolo11n.engine')")
    print("3. Expected speedup: 2-3x faster inference")
    print("4. Expected FPS: 20-25+ (up from current 12-15)")
    
except KeyboardInterrupt:
    print("\n\nExport interrupted by user")
    sys.exit(1)
except Exception as e:
    print(f"\n✗ Error during export: {e}")
    import traceback
    traceback.print_exc()
    print("\nTroubleshooting:")
    print("1. Ensure yolo11n.pt exists in current directory")
    print("2. Check available disk space (need ~100MB)")
    print("3. Check GPU memory (jtop or tegrastats)")
    sys.exit(1)
