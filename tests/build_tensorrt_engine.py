#!/usr/bin/env python3
"""
Convert YOLO ONNX model to TensorRT engine manually
This avoids the ultralytics export issues and gives us more control
"""

import tensorrt as trt
import os
import sys

TRT_LOGGER = trt.Logger(trt.Logger.INFO)

def build_engine(onnx_file, engine_file, fp16=True, workspace=2):
    """
    Build TensorRT engine from ONNX file
    
    Args:
        onnx_file: Path to ONNX model
        engine_file: Path to save TensorRT engine
        fp16: Use FP16 precision for speed
        workspace: Workspace size in GB
    """
    print(f"Building TensorRT engine from {onnx_file}...")
    print(f"FP16 mode: {fp16}")
    print(f"Workspace: {workspace}GB")
    
    # Create builder and network
    builder = trt.Builder(TRT_LOGGER)
    network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
    parser = trt.OnnxParser(network, TRT_LOGGER)
    
    # Parse ONNX
    print("\nParsing ONNX file...")
    with open(onnx_file, 'rb') as f:
        if not parser.parse(f.read()):
            print('ERROR: Failed to parse ONNX file')
            for error in range(parser.num_errors):
                print(parser.get_error(error))
            return None
    
    print(f"✓ ONNX parsed successfully")
    print(f"  Network inputs: {network.num_inputs}")
    print(f"  Network outputs: {network.num_outputs}")
    
    # Configure builder
    config = builder.create_builder_config()
    config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, workspace * (1 << 30))  # GB to bytes
    
    if fp16 and builder.platform_has_fast_fp16:
        print("✓ FP16 mode enabled")
        config.set_flag(trt.BuilderFlag.FP16)
    else:
        print("⚠ FP16 not available, using FP32")
    
    # Build engine
    print("\nBuilding TensorRT engine...")
    print("This will take 2-5 minutes...")
    
    serialized_engine = builder.build_serialized_network(network, config)
    
    if serialized_engine is None:
        print("ERROR: Failed to build engine")
        return None
    
    # Save engine
    print(f"\n✓ Engine built successfully")
    print(f"Saving to {engine_file}...")
    
    with open(engine_file, 'wb') as f:
        f.write(serialized_engine)
    
    engine_size = os.path.getsize(engine_file) / (1024 * 1024)
    print(f"✓ Engine saved: {engine_size:.2f} MB")
    
    return engine_file

if __name__ == "__main__":
    # Check for ONNX file
    onnx_file = "yolo11n.onnx"
    if not os.path.exists(onnx_file):
        print(f"ERROR: {onnx_file} not found")
        print("Please run ONNX export first:")
        print("  python3 -c \"from ultralytics import YOLO; YOLO('yolo11n.pt').export(format='onnx', imgsz=160)\"")
        sys.exit(1)
    
    engine_file = "yolo11n_160_fp16.engine"
    
    print("="*60)
    print("TensorRT Engine Builder")
    print("="*60)
    print(f"Input:  {onnx_file}")
    print(f"Output: {engine_file}")
    print("="*60)
    
    result = build_engine(onnx_file, engine_file, fp16=True, workspace=2)
    
    if result:
        print("\n" + "="*60)
        print("SUCCESS!")
        print("="*60)
        print(f"TensorRT engine ready: {engine_file}")
        print("\nTo use in sentry_service.py:")
        print(f"  Change: YOLO('yolo11n.pt')")
        print(f"  To:     YOLO('{engine_file}')")
        print("\nExpected performance:")
        print("  • 2-3x faster inference")
        print("  • 20-25+ FPS (up from 12-15)")
    else:
        print("\n" + "="*60)
        print("FAILED - See errors above")
        print("="*60)
        sys.exit(1)
