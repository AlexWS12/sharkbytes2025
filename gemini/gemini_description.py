import os
import google.generativeai as genai
from pathlib import Path
from PIL import Image
import json
from datetime import datetime
from dotenv import load_dotenv

# Load from .env
load_dotenv()

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set GEMINI_API_KEY in your .env file")

genai.configure(api_key=GEMINI_API_KEY)

def list_available_models():
    """List all available models for debugging"""
    print("Available models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"  - {m.name}")
    print()

# Initialize the model (using Gemini 2.0 Flash)
model = genai.GenerativeModel('gemini-2.0-flash')

def analyze_security_image(image_path):
    """
    Analyze a security camera image and return a detailed description
    
    Args:
        image_path: Path to the image file
        
    Returns:
        dict: Analysis results including description, detected objects, and timestamp
    """
    try:
        # Load the image
        img = Image.open(image_path)
        
        # Create a security-focused prompt
        prompt = """Analyze this security camera image and respond in this exact format:
DESCRIPTION: [One sentence describing what you see]
SEVERITY: [info/warning/critical]

Use 'info' for normal activities, 'warning' for suspicious activities, and 'critical' for immediate threats or emergencies."""

        # Generate content
        response = model.generate_content([prompt, img])

        # Parse the response to extract description and severity
        response_text = response.text.strip()
        description = ""
        severity = "info"

        # Parse structured response
        lines = response_text.split('\n')
        for line in lines:
            if line.startswith('DESCRIPTION:'):
                description = line.replace('DESCRIPTION:', '').strip()
            elif line.startswith('SEVERITY:'):
                severity_value = line.replace('SEVERITY:', '').strip().lower()
                if severity_value in ['info', 'warning', 'critical']:
                    severity = severity_value
        
        # Prepare result
        result = {
            "image": os.path.basename(image_path),
            "timestamp": datetime.now().isoformat(),
            "analysis": description if description else response.text,
            "severity": severity,
            "status": "success"
        }
        
        return result
        
    except Exception as e:
        return {
            "image": os.path.basename(image_path),
            "timestamp": datetime.now().isoformat(),
            "analysis": None,
            "status": "error",
            "error": str(e)
        }

def process_test_images():
    """
    Process all test images in the tests folder
    """
    test_folder = Path("tests")
    
    
    # Look for test images
    test_images = ["test1.jpg", "test2.jpg", "test3.jpg"]
    results = []
    
    print("=" * 60)
    print("SECURITY CAMERA IMAGE ANALYSIS")
    print("=" * 60)
    print()
    
    for img_name in test_images:
        img_path = test_folder / img_name
        
        if not img_path.exists():
            print(f"⚠️  {img_name} not found, skipping...")
            continue
        
        print(f"📸 Analyzing {img_name}...")
        print("-" * 60)
        
        result = analyze_security_image(img_path)
        results.append(result)
        
        if result["status"] == "success":
            print(result["analysis"])
        else:
            print(f"❌ Error: {result['error']}")
        
        print()
        print("-" * 60)
        print()
    
    # Save results to JSON
    output_file = "security_analysis_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Analysis complete! Results saved to {output_file}")
    print(f"📊 Processed {len(results)} images")

if __name__ == "__main__":
    process_test_images()