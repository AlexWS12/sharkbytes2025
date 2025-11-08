#!/bin/bash

# SharkBytes Mobile Setup Script
# This script helps you set up the mobile app quickly

echo "🦈 SharkBytes Mobile Setup"
echo "=========================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js v16 or higher."
    echo "   Download from: https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js version: $(node -v)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed."
    exit 1
fi

echo "✅ npm version: $(npm -v)"

# Detect OS and get local IP
echo ""
echo "🔍 Detecting your local IP address..."
echo ""

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    LOCAL_IP=$(hostname -I | awk '{print $1}')
else
    echo "⚠️  Unable to auto-detect IP. Please find it manually:"
    echo "   - Mac/Linux: Run 'ifconfig'"
    echo "   - Windows: Run 'ipconfig'"
    LOCAL_IP="YOUR_IP_HERE"
fi

echo "📍 Your local IP address: $LOCAL_IP"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"
echo ""

# Update API config with detected IP
CONFIG_FILE="src/config/api.config.js"

if [ "$LOCAL_IP" != "YOUR_IP_HERE" ]; then
    echo "⚙️  Updating API configuration..."

    # Backup original config
    cp "$CONFIG_FILE" "${CONFIG_FILE}.backup"

    # Update BASE_URL with detected IP
    sed -i.tmp "s|BASE_URL: 'http://localhost:8000'|BASE_URL: 'http://${LOCAL_IP}:8000'|g" "$CONFIG_FILE"
    rm "${CONFIG_FILE}.tmp" 2>/dev/null

    echo "✅ API config updated to: http://${LOCAL_IP}:8000"
    echo ""
else
    echo "⚠️  Please manually update $CONFIG_FILE with your IP address"
    echo ""
fi

# Check if backend is running
echo "🔌 Checking backend connection..."
if curl -s "http://${LOCAL_IP}:8000/health" > /dev/null 2>&1; then
    echo "✅ Backend is running and accessible!"
else
    echo "⚠️  Backend not detected at http://${LOCAL_IP}:8000"
    echo "   Please start the backend:"
    echo "   $ cd ../web"
    echo "   $ python main.py"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Make sure the backend is running (web/main.py)"
echo "2. Start the mobile app:"
echo "   $ npm start"
echo ""
echo "3. For iPhone: Install 'Expo Go' from App Store and scan QR code"
echo "   For Simulator: Run 'npm run ios'"
echo ""
echo "📖 See README.md for detailed instructions"
echo "⚡ See QUICKSTART.md for quick reference"
echo ""
