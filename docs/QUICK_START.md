#  Quick Start Guide

## Launching the Application

The easiest way to start everything:

### Start All Services (Recommended)
```bash
./start_project.sh
```
This will automatically start:
- Backend (FastAPI) at `http://localhost:5000`
- Frontend (React) at `http://localhost:5173`
- Sentry (camera tracking embedded in backend)

All services run in the background with logs saved to `logs/` directory.

---

##  Managing Services

### Check Status
```bash
./status_project.sh
```
Shows which services are running and their status.

### Stop All Services
```bash
./stop_project.sh
```
Gracefully stops all running services.

### View Logs
```bash
# Backend logs
tail -f logs/backend.log

# Frontend logs
tail -f logs/frontend.log

# Both
tail -f logs/*.log
```

---

## 🎯 Access Points

Once running, access the application at:

- **Frontend UI:** http://localhost:5173
- **Backend API:** http://localhost:5000
- **API Documentation:** http://localhost:5000/docs
- **Video Feed:** http://localhost:5000/video_feed
- **Sentry Stats:** http://localhost:5000/sentry/stats

---

##  Prerequisites

Before starting, ensure you have:

1. **Python virtual environment set up:**
   ```bash
   ./setup_venv.sh
   ```

2. **Frontend dependencies installed:**
   ```bash
   cd frontend && npm install
   ```

3. **Environment variables configured:**
   - Create a `.env` file with your Supabase credentials:
     ```
     SUPABASE_URL=your_supabase_url
     SUPABASE_KEY=your_supabase_key
     GEMINI_API_KEY=your_gemini_api_key
     ```

---

##  Stopping the Services

Press `Ctrl+C` in each terminal to stop the respective service.

---

## 🐛 Troubleshooting

**Port already in use:**
- Backend (5000): Check if another process is using port 5000
- Frontend (5173): Check if another Vite server is running

**Virtual environment not found:**
```bash
./setup_venv.sh
```

**Missing dependencies:**
```bash
# Python
source venv/bin/activate
pip install -r requirements.txt

# Node.js
cd frontend
npm install
```

---

##  Notes

- The **backend** must be running for the frontend to fetch data
- The **sentry** is optional - the frontend will show mock data if it's not running
- The frontend uses **hot reload** - changes will reflect automatically
- The backend uses **auto-reload** - changes to Python files will restart the server
