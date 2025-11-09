# SharkBytes Mobile - React Native Activity Log

A React Native mobile application for viewing real-time activity logs from the SharkBytes security system.

## Features

- **Real-time Event Monitoring**: Automatically polls for new events every 5 seconds
- **Event List View**: Clean, card-based interface showing all security events
- **Detailed Event View**: Tap any event to see full details and captured images
- **Pull-to-Refresh**: Swipe down to manually refresh the activity log
- **Severity-Based Color Coding**: Visual indicators for INFO, WARNING, and CRITICAL events
- **Live Status Indicator**: Shows connection status with animated pulse
- **Event Statistics**: Quick overview of total events and severity breakdown
- **Image Support**: View full-resolution images captured during events
- **Error Handling**: Clear error messages with retry functionality

## Prerequisites

Before running the app, make sure you have:

1. **Node.js** (v16 or higher)
2. **npm** or **yarn**
3. **Expo CLI**: Install globally with `npm install -g expo-cli`
4. **iOS Simulator** (for Mac users) or **Expo Go app** on your iPhone
5. **Backend API running**: The FastAPI backend should be running on your local network

## Installation

1. Navigate to the mobile directory:
   ```bash
   cd mobile
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Configuration

### Backend URL Configuration

Before running the app, you need to configure the backend URL:

1. Open `src/config/api.config.js`

2. Update the `BASE_URL`:

   **For iOS Simulator:**
   ```javascript
   BASE_URL: 'http://localhost:8000'
   ```

   **For Physical iPhone:**
   ```javascript
   BASE_URL: 'http://YOUR_COMPUTER_IP:8000'
   ```

3. To find your computer's IP address:
   - **Mac/Linux**: Run `ifconfig` and look for your local IP (usually starts with 192.168.x.x)
   - **Windows**: Run `ipconfig` and look for IPv4 Address

   Example:
   ```javascript
   BASE_URL: 'http://192.168.1.100:8000'
   ```

### Backend CORS Configuration

Make sure your FastAPI backend allows connections from your mobile device:

In `web/main.py`, the CORS middleware should allow your IP:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "http://192.168.1.100:*",  # Add your IP range
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Running the App

### Option 1: iOS Simulator (Mac only)

```bash
npm run ios
```

This will:
1. Start the Expo dev server
2. Open the iOS Simulator
3. Build and launch the app

### Option 2: Physical iPhone (Recommended for testing)

1. Install **Expo Go** from the App Store on your iPhone

2. Start the Expo dev server:
   ```bash
   npm start
   ```

3. Scan the QR code with your iPhone camera

4. The app will open in Expo Go

### Option 3: Web (for quick testing)

```bash
npm run web
```

Note: Some features may not work exactly the same on web.

## Usage

### Main Features

1. **View Activity Log**
   - Events are displayed in chronological order (newest first)
   - Each card shows timestamp, severity, description, and thumbnail (if available)
   - Severity badges are color-coded: Blue (INFO), Yellow (WARNING), Red (CRITICAL)

2. **View Event Details**
   - Tap any event card to see full details
   - View full-resolution images
   - See complete timestamp and event metadata
   - Close with the X button or swipe down

3. **Refresh Events**
   - Pull down on the list to manually refresh
   - Events auto-refresh every 5 seconds
   - Live indicator shows connection status

4. **Statistics Dashboard**
   - Total event count
   - Critical event count
   - Warning event count

### Troubleshooting

#### "Network Error" or "Failed to fetch events"

**Problem**: App can't connect to backend

**Solutions**:
1. Verify backend is running: `http://YOUR_IP:8000/health`
2. Check `BASE_URL` in `src/config/api.config.js` is correct
3. Ensure your phone and computer are on the same WiFi network
4. Check firewall settings aren't blocking port 8000
5. Update CORS settings in backend to allow your IP

#### App shows "No Events Yet"

**Problem**: Backend is connected but no events in database

**Solutions**:
1. Check if events exist: Visit `http://YOUR_IP:8000/events` in browser
2. Trigger a test event through the web interface
3. Upload a test frame to `/analyze-frame` endpoint

#### Images not loading

**Problem**: Image URLs not accessible

**Solutions**:
1. Check Supabase storage permissions
2. Verify `image_url` in events is a valid public URL
3. Check network connection

## Project Structure

```
mobile/
+-- app/                      # Expo Router app directory
|   +-- _layout.jsx          # Root layout
|   └-- index.jsx            # Main entry point
+-- src/
|   +-- components/          # Reusable components
|   |   +-- EventCard.jsx    # Individual event card
|   |   └-- EventDetail.jsx  # Event detail modal
|   +-- screens/             # Screen components
|   |   └-- ActivityLogScreen.jsx  # Main activity log screen
|   +-- services/            # API and service layers
|   |   └-- api.service.js   # API client
|   └-- config/              # Configuration
|       └-- api.config.js    # API endpoints and settings
+-- assets/                  # Images, fonts, etc.
+-- package.json
+-- app.json                 # Expo configuration
└-- babel.config.js
```

## API Endpoints Used

- `GET /events?limit=50` - Fetch recent events
- `GET /health` - Check backend health status

## Customization

### Polling Interval

Change auto-refresh frequency in `src/config/api.config.js`:

```javascript
POLLING_INTERVAL: 5000, // milliseconds (5 seconds)
```

### Event Limit

Adjust number of events fetched:

```javascript
DEFAULT_LIMIT: 50, // number of events
```

### Colors and Styling

Modify severity colors in component files:
- `EventCard.jsx`: Card styling
- `EventDetail.jsx`: Detail modal styling
- `ActivityLogScreen.jsx`: Screen layout

## Building for Production

### iOS App Store

1. Configure app.json with your bundle identifier
2. Build with EAS:
   ```bash
   npm install -g eas-cli
   eas build --platform ios
   ```

### Standalone App

For more control, eject from Expo:
```bash
npx expo prebuild
```

Then use Xcode to build and sign the app.

## Contributing

This app mirrors the functionality of the web interface in `/frontend`. When adding features:
1. Ensure API compatibility with backend
2. Follow React Native best practices
3. Test on both simulator and physical device
4. Update this README with new features

## License

Part of the SharkBytes security system.
