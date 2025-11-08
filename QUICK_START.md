# 🚀 Quick Start Guide

## Launching the Application

You have **three options** to start the app:

### Option 1: Start Everything at Once (Recommended for macOS)
```bash
./start_all.sh
```
This will automatically open 3 terminal tabs with all services running.

---

### Option 2: Start Services Manually (3 separate terminals)

**Terminal 1 - Backend:**
```bash
./start_backend.sh
```
- FastAPI server at `http://localhost:5000`
- API docs at `http://localhost:5000/docs`

**Terminal 2 - Frontend:**
```bash
./start_frontend.sh
```
- React dev server at `http://localhost:5173`

**Terminal 3 - Sentry (Optional):**
```bash
./start_sentry.sh
```
- OpenCV camera tracking system
- Controls: `L` (lock), `C` (center), `Q` (quit)

---

### Option 3: Manual Commands

**Backend:**
```bash
source venv/bin/activate
uvicorn web.main:app --host 0.0.0.0 --port 5000 --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

**Sentry:**
```bash
source venv/bin/activate
python3 sentry/person_tracking_sentry.py
```

---

## 🎯 Access Points

Once running, access the application at:

- **Frontend UI:** http://localhost:5173
- **Backend API:** http://localhost:5000
- **API Documentation:** http://localhost:5000/docs

---

## ⚙️ Prerequisites

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

## 🛑 Stopping the Services

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

## 📝 Notes

- The **backend** must be running for the frontend to fetch data
- The **sentry** is optional - the frontend will show mock data if it's not running
- The frontend uses **hot reload** - changes will reflect automatically
- The backend uses **auto-reload** - changes to Python files will restart the server
