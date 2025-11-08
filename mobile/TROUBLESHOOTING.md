# Troubleshooting Guide

## Common Issues and Solutions

### 🔴 Error: EMFILE: too many open files

**Problem**: macOS has a low default limit for open file watchers, which Metro bundler exceeds.

**Solutions**:

#### Option 1: Increase File Limit (Recommended)

1. Check current limits:
   ```bash
   ulimit -n
   # Usually shows 256 or 1024
   ```

2. Increase the limit temporarily (current terminal session):
   ```bash
   ulimit -n 4096
   ```

3. Then start the app:
   ```bash
   npm start
   ```

#### Option 2: Increase Permanently

Add to your shell profile (`~/.zshrc` or `~/.bash_profile`):

```bash
# Add this line
ulimit -n 4096
```

Then reload your shell:
```bash
source ~/.zshrc  # or source ~/.bash_profile
```

#### Option 3: Use Watchman (Best long-term solution)

Install Facebook's Watchman file watcher:

```bash
# Using Homebrew
brew install watchman

# Verify installation
watchman --version
```

Watchman is more efficient and eliminates this issue.

#### Option 4: Clean and Restart

Sometimes cached files cause issues:

```bash
# Clear Expo cache
npx expo start --clear

# Or clear everything
rm -rf node_modules
rm -rf .expo
npm install
npm start
```

---

### 🔴 Network Error / Failed to fetch events

**Problem**: App can't connect to backend

**Checklist**:

1. ✅ **Backend is running**:
   ```bash
   cd ../web
   python main.py
   ```

2. ✅ **Correct IP address** in `src/config/api.config.js`:
   ```bash
   # Find your IP
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```

3. ✅ **Same WiFi network**: Phone and computer must be on same network

4. ✅ **Test backend in browser**:
   ```
   http://YOUR_IP:8000/health
   http://YOUR_IP:8000/events
   ```

5. ✅ **Firewall allows port 8000**:
   ```bash
   # macOS - check firewall
   # System Settings → Network → Firewall
   ```

6. ✅ **CORS configuration** in `web/main.py`:
   ```python
   allow_origins=[
       "http://localhost:5173",
       "http://192.168.1.*",  # Allow your subnet
   ]
   ```

---

### 🔴 Metro Bundler Issues

**Problem**: Metro bundler crashes or won't start

**Solutions**:

```bash
# Option 1: Clear Metro cache
npx expo start --clear

# Option 2: Clear watchman cache (if installed)
watchman watch-del-all

# Option 3: Reset everything
rm -rf node_modules .expo
npm install
npm start -- --clear

# Option 4: Kill all Node processes
killall -9 node
npm start
```

---

### 🔴 iOS Simulator Not Opening

**Problem**: `npm run ios` doesn't open simulator

**Solutions**:

1. Install Xcode from Mac App Store (if not installed)

2. Install Xcode Command Line Tools:
   ```bash
   xcode-select --install
   ```

3. Open Xcode and install additional components

4. Manually open simulator:
   ```bash
   open -a Simulator
   ```

5. Then run:
   ```bash
   npm start
   ```

---

### 🔴 Images Not Loading

**Problem**: Event cards show but images don't load

**Checklist**:

1. ✅ **Valid image URLs**: Check in browser:
   ```
   http://YOUR_IP:8000/events
   # Look at image_url field
   ```

2. ✅ **Supabase permissions**: Images must be publicly accessible

3. ✅ **Network connection**: Check phone's internet

4. ✅ **Image URL format**: Should be full URL starting with `https://`

---

### 🔴 App Shows "No Events Yet"

**Problem**: Connected to backend but no events display

**Solutions**:

1. Check if events exist in database:
   ```bash
   curl http://YOUR_IP:8000/events
   ```

2. Create a test event via web interface

3. Trigger vision analysis:
   ```bash
   curl -X POST http://YOUR_IP:8000/analyze-frame \
     -F "file=@test_image.jpg"
   ```

4. Check app logs in terminal for API errors

---

### 🔴 Expo Go Not Connecting

**Problem**: QR code scanned but app won't open

**Solutions**:

1. ✅ **Latest Expo Go**: Update from App Store

2. ✅ **Same network**: Phone and computer on same WiFi

3. ✅ **Firewall**: Disable temporarily to test

4. Try direct connection:
   ```bash
   npm start
   # Press 'w' for web
   # Or press 'i' for iOS simulator
   ```

5. Use tunnel mode:
   ```bash
   npm start -- --tunnel
   ```

---

### 🔴 Module Not Found Errors

**Problem**: `Error: Unable to resolve module`

**Solutions**:

```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Clear Metro cache
npx expo start --clear

# Check for typos in imports
# Ensure all imports use correct paths
```

---

### 🔴 Build/Bundle Errors

**Problem**: App builds but crashes on launch

**Solutions**:

1. Check for syntax errors in JSX files

2. Verify all imports are correct:
   ```javascript
   // Good
   import EventCard from '../components/EventCard';

   // Bad - missing extension for JSX
   import EventCard from '../components/EventCard.jsx';
   ```

3. Clear everything:
   ```bash
   rm -rf node_modules .expo
   npm install
   npx expo start --clear
   ```

---

### 🔴 Slow Performance / Lag

**Problem**: App is slow or janky

**Solutions**:

1. Use development mode for testing:
   ```bash
   npm start
   ```

2. Check polling interval in `api.config.js`:
   ```javascript
   POLLING_INTERVAL: 5000, // Don't set too low
   ```

3. Reduce event limit:
   ```javascript
   DEFAULT_LIMIT: 25, // Instead of 50
   ```

4. Test on physical device instead of simulator

---

## Debug Mode

### Enable Detailed Logging

In `src/services/api.service.js`, the console logs are already enabled. Check terminal output for:
- API requests
- Response data
- Error messages

### Check Network Tab

In Expo Dev Tools:
1. Press `m` in terminal to open menu
2. Select "Open DevTools"
3. Check Network tab for failed requests

### React Native Debugger

For advanced debugging:
```bash
# Install React Native Debugger
brew install --cask react-native-debugger

# Then in app, shake device and select "Debug"
```

---

## Getting Help

If issues persist:

1. Check [README.md](README.md) for setup instructions
2. Review [QUICKSTART.md](QUICKSTART.md) for configuration
3. Verify backend logs in `web/main.py` terminal
4. Check Expo documentation: https://docs.expo.dev/
5. Review React Native docs: https://reactnative.dev/

---

## Quick Reset Script

Save this as `reset.sh`:

```bash
#!/bin/bash
echo "🧹 Resetting SharkBytes Mobile..."
rm -rf node_modules
rm -rf .expo
rm -rf package-lock.json
ulimit -n 4096
npm install
echo "✅ Reset complete! Run: npm start"
```

Make executable and run:
```bash
chmod +x reset.sh
./reset.sh
```
