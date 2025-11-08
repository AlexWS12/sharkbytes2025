#!/bin/bash
# Start all services (Backend, Frontend, and Sentry) in separate terminal tabs

echo "🚀 Starting All Services..."
echo "============================"
echo ""
echo "This will open 3 terminal tabs:"
echo "  1. FastAPI Backend (port 5000)"
echo "  2. React Frontend (port 5173)"
echo "  3. Person Tracking Sentry"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Check if we're on macOS (for Terminal app)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Detected macOS - Using Terminal.app"

    # Open backend in new tab
    osascript -e "tell application \"Terminal\"" \
              -e "tell application \"System Events\" to keystroke \"t\" using {command down}" \
              -e "do script \"cd '$SCRIPT_DIR' && ./start_backend.sh\" in front window" \
              -e "end tell"

    sleep 1

    # Open frontend in new tab
    osascript -e "tell application \"Terminal\"" \
              -e "tell application \"System Events\" to keystroke \"t\" using {command down}" \
              -e "do script \"cd '$SCRIPT_DIR' && ./start_frontend.sh\" in front window" \
              -e "end tell"

    sleep 1

    # Open sentry in new tab
    osascript -e "tell application \"Terminal\"" \
              -e "tell application \"System Events\" to keystroke \"t\" using {command down}" \
              -e "do script \"cd '$SCRIPT_DIR' && ./start_sentry.sh\" in front window" \
              -e "end tell"

    echo "✅ All services started in separate tabs!"
else
    echo "⚠️  Auto-launch only works on macOS"
    echo ""
    echo "Please manually run in separate terminals:"
    echo "  Terminal 1: ./start_backend.sh"
    echo "  Terminal 2: ./start_frontend.sh"
    echo "  Terminal 3: ./start_sentry.sh"
fi
