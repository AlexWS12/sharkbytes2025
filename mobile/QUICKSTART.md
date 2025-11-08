# Quick Start Guide - SharkBytes Mobile

Get the mobile app running in 5 minutes!

## Step 1: Install Dependencies

```bash
cd mobile
npm install
```

## Step 2: Configure Backend URL

1. Find your computer's IP address:

   **Mac/Linux:**
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```

   **Windows:**
   ```cmd
   ipconfig
   ```

   Look for an IP like `192.168.1.100`

2. Edit `src/config/api.config.js`:
   ```javascript
   export const API_CONFIG = {
     BASE_URL: 'http://192.168.1.100:8000', // Use your IP
     // ...
   };
   ```

## Step 3: Start Backend

Make sure your FastAPI backend is running:

```bash
# From the repository root
cd web
python main.py
```

Verify it's accessible at: `http://YOUR_IP:8000/health`

## Step 4: Run the App

**For iPhone (Physical Device):**
```bash
npm start
```
Then scan QR code with Expo Go app

**For iOS Simulator:**
```bash
npm run ios
```

## Step 5: Test Connection

The app should show:
- ✅ Green "LIVE" indicator
- ✅ List of events (if any exist)

If you see errors, check:
- Backend is running
- IP address is correct
- Phone and computer on same WiFi
- Firewall allows port 8000

## Common Commands

```bash
# Start dev server
npm start

# Run on iOS simulator
npm run ios

# Clear cache and restart
npm start --clear

# View logs
npm start -- --ios
```

## Testing the App

1. Upload a test image to trigger an event:
   ```bash
   curl -X POST http://YOUR_IP:8000/analyze-frame \
     -F "file=@test_image.jpg"
   ```

2. Watch the event appear in the mobile app!

## Need Help?

- Check [README.md](README.md) for detailed documentation
- Verify backend health: `http://YOUR_IP:8000/health`
- Check Expo logs for errors
- Ensure CORS is configured in `web/main.py`
