# 🎥 Video Streaming Integration Guide

## What We Built

We've integrated your person-tracking sentry system directly into FastAPI with **Option B** - the complete, production-ready solution!

### Architecture

```
FastAPI Server (port 5000)
|
+-- Sentry Service (background thread)
|   +-- OpenCV camera capture
|   +-- YOLO person detection
|   +-- DeepSORT tracking
|   +-- Servo control
|   └-- Frame annotation (bounding boxes, crosshairs, stats)
|
+-- /video_feed endpoint
|   └-- MJPEG streaming of annotated frames
|
+-- /control endpoint
|   └-- Send commands to sentry (pan, tilt, lock, center)
|
└-- /sentry/stats endpoint
    └-- Get real-time stats (FPS, tracking status, servo angles)
```

---

## ✨ Features

 **Single Camera Source** - No conflicts, one system
 **Real-time MJPEG Streaming** - Works with HTML `<img>` tags
 **Full Annotations** - See tracking boxes, crosshairs, stats overlaid
 **Remote Control** - Frontend buttons directly control servos
 **Background Processing** - Runs as a thread, doesn't block API
 **Graceful Degradation** - Shows placeholder if sentry unavailable

---

##  How to Run

### Option 1: Quick Start (All at once)
```bash
./start_all.sh
```

### Option 2: Manual Start

**Terminal 1 - Backend (includes sentry):**
```bash
./start_backend.sh
```

**Terminal 2 - Frontend:**
```bash
./start_frontend.sh
```

**NOTE:** You do NOT need to run `start_sentry.sh` anymore - the sentry is now integrated into the backend!

---

##  What Changed

### 1. New File: `sentry/sentry_service.py`
- Refactored `PersonTrackingSentry` into a reusable service
- Runs as background thread instead of standalone script
- No `cv2.imshow()` - designed for headless operation
- Command queue for external control
- Thread-safe frame access

### 2. Updated: `web/main.py`
- Imports `SentryService`
- Starts sentry on FastAPI startup
- Stops sentry on shutdown
- MJPEG streaming via `generate_frames()` generator
- `/control` endpoint now sends commands to sentry
- New `/sentry/stats` endpoint for real-time data

### 3. Frontend Already Ready!
- `VideoFeed.jsx` points to `/video_feed`
- `CameraControls.jsx` sends commands to `/control`
- No changes needed!

---

## 📡 API Endpoints

### `GET /video_feed`
MJPEG stream of annotated camera frames.

**Usage:**
```html
<img src="http://localhost:5000/video_feed" alt="Camera Feed" />
```

**Response:** Multipart MJPEG stream
**Frame Rate:** ~30 FPS
**Annotations:** Bounding boxes, tracking IDs, crosshair, FPS, servo angles

---

### `POST /control`
Send control commands to the sentry.

**Request:**
```json
{
  "command": "toggle_lock"
}
```

**Commands:**
- `toggle_lock` - Enable/disable auto-tracking
- `center` - Reset camera to center position
- `pan_left` - Pan 5° left
- `pan_right` - Pan 5° right
- `tilt_up` - Tilt 5° up
- `tilt_down` - Tilt 5° down

**Response:**
```json
{
  "status": "success",
  "command": "toggle_lock"
}
```

---

### `GET /sentry/stats`
Get real-time sentry statistics.

**Response:**
```json
{
  "fps": 28.5,
  "tracking_status": "LOCKED ID:1",
  "pan_angle": 95.2,
  "tilt_angle": 88.7,
  "people_count": 1
}
```

---

## 🧪 Testing

### 1. Test Video Stream
Open in browser: http://localhost:5000/video_feed

You should see:
- Live camera feed
- Green bounding box around tracked person (if locked)
- Blue boxes around other people
- Red crosshair in center
- FPS, servo angles, tracking status overlays

### 2. Test Frontend
Open: http://localhost:5173

You should see:
- Video feed in top-left panel
- Camera controls in bottom-left panel
- Anomaly log on right side

### 3. Test Controls
Click the camera control buttons:
- Pan left/right - camera should move
- Tilt up/down - camera should move
- Center - camera returns to default position
- Lock toggle - enables/disables auto-tracking

---

## 🐛 Troubleshooting

### "Sentry service not available"
**Cause:** Missing dependencies (YOLO, OpenCV, servos)
**Solution:**
- On Jetson: All dependencies should be available
- On Mac/PC: Sentry runs in simulation mode (no actual servos, but streaming works)

### Camera not opening
**Cause:** Camera already in use or wrong index
**Solution:**
- Check `CAMERA_INDEX = 0` in `sentry/sentry_service.py`
- Make sure no other process is using the camera

### No video stream / placeholder shown
**Cause:** Sentry failed to initialize
**Solution:** Check backend logs for errors

### Controls not working
**Cause:** Sentry not running or in simulation mode
**Solution:**
- Check backend logs
- On non-Jetson systems, servos won't move but commands are logged

---

## 🎯 Benefits of This Approach

 **Production Ready** - Single integrated system
 **Scalable** - Easy to add more features
 **Maintainable** - One codebase, not two separate scripts
 **Remote Access** - Control camera from anywhere on your network
 **Real-time** - Low latency streaming
 **Annotated** - See exactly what the AI sees

---

## 🔮 Next Steps (Optional)

1. **Add WebRTC** for even lower latency (more complex)
2. **Add recording** - save video clips of anomalies
3. **Add PTZ presets** - save favorite camera positions
4. **Add zones** - define restricted areas
5. **Add notifications** - push alerts when tracking locks

---

##  Notes

- The old `person_tracking_sentry.py` still exists for standalone use
- The new `sentry_service.py` is the integrated version
- Frontend automatically handles both connected and disconnected states
- MJPEG works in all modern browsers with `<img>` tags
- No JavaScript media APIs needed!

---

Happy tracking! 🎥📹
