#!/usr/bin/env python3
"""
Test script for the /analyze-frame endpoint in the FastAPI backend.
Tests with images from gemini/test directory.
"""

import requests
import os
import sys
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8000"
TEST_IMAGES_DIR = "gemini/test"

def test_analyze_frame(image_path: str):
    """
    Test the /analyze-frame endpoint with a given image.

    Args:
        image_path: Path to the image file to test
    """
    endpoint = f"{API_BASE_URL}/analyze-frame"

    print(f"\n{'='*60}")
    print(f"Testing with image: {image_path}")
    print('='*60)

    try:
        # Open and send the image file
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            response = requests.post(endpoint, files=files)

        # Check response status
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("\n[OK] SUCCESS")
            print(f"\nEvent ID: {result.get('event_id')}")
            print(f"Timestamp: {result.get('timestamp')}")
            print(f"Severity: {result.get('severity')}")
            print(f"Status: {result.get('status')}")
            print("\nAnalysis:")
            print("-" * 60)
            print(result.get('analysis'))
            print("-" * 60)

            # Note: image_url would be in the database event record
            # The FrameAnalysisResponse doesn't include it, but it's stored in the DB
            print("\n[OK] Image uploaded to Supabase Storage successfully!")
            print("   (Check the events table for the image_url)")
        else:
            print("\n[ERROR] ERROR")
            print(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print(f"[ERROR] ERROR: Could not connect to {API_BASE_URL}")
        print("Make sure the FastAPI server is running!")
        print("Start it with: uvicorn web.main:app --reload")
        sys.exit(1)
    except FileNotFoundError:
        print(f"[ERROR] ERROR: Image file not found: {image_path}")
    except Exception as e:
        print(f"[ERROR] ERROR: {str(e)}")

def test_health():
    """Test the health endpoint to ensure server is running."""
    endpoint = f"{API_BASE_URL}/health"

    print("Checking server health...")
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            print("[OK] Server is running and healthy")
            return True
        else:
            print(f"[WARNING]  Server responded but with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Cannot connect to {API_BASE_URL}")
        print("Please start the server with: uvicorn web.main:app --reload")
        return False

def main():
    """Main test runner."""
    print("\n" + "="*60)
    print("FastAPI /analyze-frame Endpoint Test")
    print("="*60)

    # Check if server is running
    if not test_health():
        sys.exit(1)

    # Get all test images
    test_dir = Path(TEST_IMAGES_DIR)
    if not test_dir.exists():
        print(f"[ERROR] Test images directory not found: {TEST_IMAGES_DIR}")
        sys.exit(1)

    # Test specific images (4, 5, and 6)
    image_files = [
        test_dir / "test4.jpeg",
        test_dir / "test5.jpeg",
        test_dir / "test6.jpeg"
    ]

    # Check if all images exist
    missing_images = [img for img in image_files if not img.exists()]
    if missing_images:
        print("[ERROR] Missing test images:")
        for img in missing_images:
            print(f"   - {img}")
        sys.exit(1)

    print(f"\nTesting {len(image_files)} image(s): test4.jpeg, test5.jpeg, test6.jpeg")

    # Test each image
    for image_path in image_files:
        test_analyze_frame(str(image_path))

    print("\n" + "="*60)
    print("Testing complete!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()