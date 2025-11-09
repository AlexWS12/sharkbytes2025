# ✅ SharkBytes 2025 - Ready to Use!

Your complete person-tracking sentry project is now set up with easy management scripts!

## 🎯 Quick Commands

### Start Everything
```bash
./start_project.sh
```

### Stop Everything
```bash
./stop_project.sh
```

### Check Status
```bash
./status_project.sh
```

## 🌐 Access Your Application

Once started (using `./start_project.sh`):

- **📱 Frontend Dashboard:** http://localhost:5173
- **🔧 Backend API:** http://localhost:5000/docs
- **📹 Video Feed:** http://localhost:5000/video_feed
- **📊 Sentry Stats:** http://localhost:5000/sentry/stats

## ✨ What's Working

✅ **Backend (FastAPI)** - Running on port 5000
  - Sentry service with camera tracking
  - Face detection (yellow circles on faces)
  - Person tracking with DeepSORT
  - Servo control for pan/tilt
  - Event logging to Supabase
  - Video streaming endpoint

✅ **Frontend (React/Vite)** - Running on port 5173
  - Live video feed with face indicators
  - Real-time anomaly log
  - Camera controls
  - Responsive UI

✅ **Sentry Service** (Embedded in backend)
  - YOLOv11 person detection
  - Face detection with Haar Cascade
  - DeepSORT target tracking
  - PCA9685 servo control
  - Real-time video processing

## 📋 Features

### Camera View
- Live MJPEG video stream
- Green box around locked target
- Yellow circle + dot on detected faces
- Red crosshair in center
- FPS counter and tracking status

### Tracking
- Automatic person detection
- Face-priority tracking
- Smooth servo movements
- Target locking by ID
- Auto-release on timeout

### Dashboard
- Activity log with events
- Severity indicators (info/warning/critical)
- Real-time updates every 5 seconds
- Camera control interface

## 📁 Important Files

```
sharkbytes2025/
├── start_project.sh     ⭐ Start everything
├── stop_project.sh      🛑 Stop everything
├── status_project.sh    📊 Check status
├── PROJECT_SCRIPTS.md   📖 Detailed documentation
├── logs/                📝 Application logs
│   ├── backend.log
│   └── frontend.log
├── .pids/               🔢 Process IDs
├── web/                 🔧 Backend code
├── frontend/            📱 Frontend code
└── sentry/              📹 Sentry code
```

## 🔍 Monitoring

### View logs in real-time:
```bash
# Backend (includes sentry)
tail -f logs/backend.log

# Frontend
tail -f logs/frontend.log

# Both
tail -f logs/*.log
```

### Check running services:
```bash
./status_project.sh
```

## 🛠 Troubleshooting

### Services won't start?
```bash
# Check logs
cat logs/backend.log
cat logs/frontend.log

# Ensure dependencies installed
./setup_venv.sh
cd frontend && npm install
```

### Camera not working?
```bash
# Check camera device
ls -l /dev/video0

# Check if camera is in use
lsof /dev/video0

# Check user permissions
groups | grep video
```

### Face detection not showing?
- Face detection is now enabled in `sentry_service.py`
- Yellow circles should appear on detected faces
- Check logs: `tail -f logs/backend.log | grep FACE`

## 🎨 Customization

### Change tracking parameters
Edit: `sentry/sentry_service.py`
- Lines 50-60: Face detection settings
- Lines 35-55: Servo and tracking parameters

### Change UI theme
Edit: `frontend/src/App.jsx` and component files

### Add new API endpoints
Edit: `web/main.py`

## 🚀 Next Steps

1. **Test it out:**
   ```bash
   ./start_project.sh
   # Open http://localhost:5173
   ```

2. **Add your Supabase credentials** (if not done):
   - Create `.env` file
   - Add `SUPABASE_URL` and `SUPABASE_KEY`

3. **Customize tracking** in `sentry/sentry_service.py`

4. **Deploy** (when ready):
   - Backend: Can run on any server with camera access
   - Frontend: Build with `cd frontend && npm run build`

## 📞 Support

For detailed documentation, see:
- `PROJECT_SCRIPTS.md` - Script documentation
- `README.md` - Project overview
- `QUICK_START.md` - Quick start guide

---

**Have fun with your person-tracking sentry! 🦈📹**
