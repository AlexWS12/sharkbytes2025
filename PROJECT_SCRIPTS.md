# 🦈 SharkBytes 2025 - Quick Start Scripts

Easy-to-use scripts to manage your entire SharkBytes project.

## 📋 Available Scripts

### 🚀 Start Everything
```bash
./start_project.sh
```
Starts all services:
- **Backend** (FastAPI) on http://localhost:5000
- **Frontend** (Vite/React) on http://localhost:5173
- **Sentry** (Camera tracking - embedded in backend)

All services run in the background with logs saved to `logs/` directory.

### 🛑 Stop Everything
```bash
./stop_project.sh
```
Gracefully stops all running services.

### 📊 Check Status
```bash
./status_project.sh
```
Shows which services are running and their status.

## 📁 Project Structure

```
sharkbytes2025/
├── start_project.sh     # Start all services
├── stop_project.sh      # Stop all services
├── status_project.sh    # Check service status
├── logs/                # Service logs (auto-created)
│   ├── backend.log
│   └── frontend.log
├── .pids/               # Process ID files (auto-created)
├── web/                 # Backend (FastAPI)
├── frontend/            # Frontend (React)
└── sentry/              # Person tracking service
```

## 🔧 First Time Setup

Before using these scripts for the first time:

1. **Setup virtual environment:**
   ```bash
   ./setup_venv.sh
   ```

2. **Create `.env` file** with your Supabase credentials:
   ```bash
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

3. **Install frontend dependencies** (auto-done by start script):
   ```bash
   cd frontend && npm install
   ```

## 📝 View Logs

### Tail backend logs:
```bash
tail -f logs/backend.log
```

### Tail frontend logs:
```bash
tail -f logs/frontend.log
```

### View all logs at once:
```bash
tail -f logs/*.log
```

## 🎯 Typical Workflow

### Development
```bash
# Start everything
./start_project.sh

# Check status
./status_project.sh

# View logs while developing
tail -f logs/backend.log

# Stop when done
./stop_project.sh
```

### Quick Check
```bash
# Just check if services are running
./status_project.sh
```

## 🐛 Troubleshooting

### Services won't start?
1. Check logs: `cat logs/backend.log` or `cat logs/frontend.log`
2. Ensure virtual environment exists: `ls sentry_env/`
3. Check if ports are already in use: `netstat -tuln | grep -E "5000|5173"`

### Camera not working?
- Check camera status: `./status_project.sh`
- Verify camera device: `ls -l /dev/video0`
- Check permissions: `groups | grep video`

### Services still running after stop?
```bash
# Force kill all
pkill -f "uvicorn web.main"
pkill -f "vite"
```

## 🌐 Access Points

Once started:
- **Frontend UI:** http://localhost:5173
- **Backend API:** http://localhost:5000
- **API Documentation:** http://localhost:5000/docs
- **Video Feed:** http://localhost:5000/video_feed
- **Sentry Stats:** http://localhost:5000/sentry/stats

## ⚙️ Configuration

### Backend (port 5000)
Edit `web/main.py` or use environment variables in `.env`

### Frontend (port 5173)
Edit `frontend/vite.config.js` or `frontend/src/components/`

### Sentry (camera tracking)
Edit `sentry/sentry_service.py` for tracking parameters

## 📌 Notes

- All services run in the background (daemon mode)
- Logs are preserved in `logs/` directory
- Process IDs stored in `.pids/` directory
- Services auto-restart is NOT enabled (manual restart required)
- Camera can only be used by one process at a time (backend includes sentry)

## 🤝 Support

If you encounter issues:
1. Check logs in `logs/` directory
2. Run `./status_project.sh` to see what's running
3. Ensure all dependencies are installed (run `./setup_venv.sh`)
