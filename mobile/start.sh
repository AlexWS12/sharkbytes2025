#!/bin/bash

# SharkBytes Mobile Startup Script
# Handles file limits and starts the app properly

echo " Starting SharkBytes Mobile..."
echo ""

# Increase file limit
ulimit -n 4096

# Check if watchman is installed
if command -v watchman &> /dev/null; then
    echo "[OK] Watchman is installed"

    # Clear watchman cache to avoid issues
    echo " Clearing watchman cache..."
    watchman watch-del-all 2>/dev/null
else
    echo "[WARNING]  Watchman not found (installing...)"
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo " Installing dependencies..."
    npm install
fi

# Clear any existing Metro cache
echo " Clearing Metro bundler cache..."
rm -rf .expo 2>/dev/null

echo ""
echo " Starting Expo..."
echo ""
echo "Options:"
echo "  • Scan QR code with Expo Go app (iPhone)"
echo "  • Press 'i' for iOS Simulator"
echo "  • Press 'w' for web browser"
echo ""

# Start with clear cache
npx expo start --clear
