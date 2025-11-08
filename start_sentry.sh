#!/bin/bash
# Start the Person Tracking Sentry (OpenCV camera system)

echo "🎥 Starting Person Tracking Sentry..."
echo "======================================"

# Navigate to project root
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  Warning: Virtual environment not found. Run ./setup_venv.sh first"
    exit 1
fi

echo "🚀 Launching sentry system..."
echo ""
echo "Controls:"
echo "  L - Toggle auto-tracking lock"
echo "  C - Center camera (when unlocked)"
echo "  Q - Quit"
echo ""

python3 sentry/person_tracking_sentry.py
