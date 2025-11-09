#!/bin/bash
# ========================================
# SharkBytes 2025 - Project Startup Script
# ========================================
# Starts all three services:
#   - Backend (FastAPI) on port 5000
#   - Frontend (Vite/React) on port 5173
#   - Sentry (Person Tracking with Camera)
#
# All services run in the background with logs
# ========================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Log directory
LOG_DIR="$PROJECT_ROOT/logs"
mkdir -p "$LOG_DIR"

# PID file directory
PID_DIR="$PROJECT_ROOT/.pids"
mkdir -p "$PID_DIR"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    SharkBytes 2025 - Startup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to check if a process is running
is_running() {
    local pid_file=$1
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0  # Running
        fi
    fi
    return 1  # Not running
}

# Function to kill a service
kill_service() {
    local service_name=$1
    local pid_file="$PID_DIR/${service_name}.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p "$pid" > /dev/null 2>&1; then
            echo -e "${YELLOW}Stopping old $service_name (PID: $pid)...${NC}"
            kill -9 "$pid" 2>/dev/null || true
            sleep 1
        fi
        rm -f "$pid_file"
    fi
}

# Clean up old processes
echo -e "${YELLOW} Cleaning up old processes...${NC}"
kill_service "backend"
kill_service "frontend"
pkill -f "uvicorn web.main" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true
sleep 2

# Check for virtual environment
if [ ! -d "sentry_env" ]; then
    echo -e "${RED}[ERROR] Error: Virtual environment not found!${NC}"
    echo -e "${YELLOW}Please run: ./setup_venv.sh${NC}"
    exit 1
fi

# Check for node_modules in frontend
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW} Installing frontend dependencies...${NC}"
    cd frontend
    npm install
    cd ..
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}[WARNING]️  Warning: .env file not found${NC}"
    echo -e "${YELLOW}Backend database features may not work${NC}"
fi

echo ""
echo -e "${GREEN}Starting services...${NC}"
echo ""

# ========================================
# Start Backend (FastAPI)
# ========================================
echo -e "${BLUE}[1/2]${NC} Starting Backend (FastAPI)..."

source sentry_env/bin/activate

# Start backend in background
nohup uvicorn web.main:app --host 0.0.0.0 --port 5000 > "$LOG_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > "$PID_DIR/backend.pid"

# Wait for backend to start
sleep 3

if ps -p $BACKEND_PID > /dev/null 2>&1; then
    echo -e "${GREEN}   [OK] Backend started${NC} (PID: $BACKEND_PID)"
    echo -e "     ${BLUE}-->${NC} http://localhost:5000"
    echo -e "     ${BLUE}-->${NC} API docs: http://localhost:5000/docs"
    echo -e "     ${BLUE}-->${NC} Logs: $LOG_DIR/backend.log"
else
    echo -e "${RED}   [FAIL] Backend failed to start${NC}"
    echo -e "${YELLOW}   Check logs: $LOG_DIR/backend.log${NC}"
    exit 1
fi

echo ""

# ========================================
# Start Frontend (Vite/React)
# ========================================
echo -e "${BLUE}[2/2]${NC} Starting Frontend (Vite/React)..."

cd frontend
nohup npm run dev > "$LOG_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > "$PID_DIR/frontend.pid"
cd ..

# Wait for frontend to start
sleep 3

if ps -p $FRONTEND_PID > /dev/null 2>&1; then
    echo -e "${GREEN}   [OK] Frontend started${NC} (PID: $FRONTEND_PID)"
    echo -e "     ${BLUE}-->${NC} http://localhost:5173"
    echo -e "     ${BLUE}-->${NC} Logs: $LOG_DIR/frontend.log"
else
    echo -e "${RED}   [FAIL] Frontend failed to start${NC}"
    echo -e "${YELLOW}   Check logs: $LOG_DIR/frontend.log${NC}"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN} All services started successfully!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}Services running:${NC}"
echo -e "  - Backend:  http://localhost:5000"
echo -e "  - Frontend: http://localhost:5173"
echo -e "  - Sentry:   Embedded in backend (camera + tracking)"
echo ""
echo -e "${YELLOW}Logs location:${NC}"
echo -e "  - Backend:  $LOG_DIR/backend.log"
echo -e "  - Frontend: $LOG_DIR/frontend.log"
echo ""
echo -e "${YELLOW}To view logs:${NC}"
echo -e "  tail -f $LOG_DIR/backend.log"
echo -e "  tail -f $LOG_DIR/frontend.log"
echo ""
echo -e "${YELLOW}To stop all services:${NC}"
echo -e "  ./stop_project.sh"
echo ""
echo -e "${GREEN}Open http://localhost:5173 in your browser!${NC}"
echo ""
