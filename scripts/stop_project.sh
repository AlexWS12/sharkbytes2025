#!/bin/bash
# ========================================
# SharkBytes 2025 - Stop All Services
# ========================================
# Stops all running services gracefully
# ========================================

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

# PID file directory
PID_DIR="$PROJECT_ROOT/.pids"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    SharkBytes 2025 - Shutdown${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

stopped_count=0

# Function to stop a service
stop_service() {
    local service_name=$1
    local service_lower=$(echo "$service_name" | tr '[:upper:]' '[:lower:]')
    local pid_file="$PID_DIR/${service_lower}.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p "$pid" > /dev/null 2>&1; then
            echo -e "${YELLOW}Stopping $service_name (PID: $pid)...${NC}"
            kill -15 "$pid" 2>/dev/null || true
            sleep 2
            
            # Check if still running and force kill if needed
            if ps -p "$pid" > /dev/null 2>&1; then
                echo -e "${YELLOW}   → Force killing $service_name...${NC}"
                kill -9 "$pid" 2>/dev/null || true
                sleep 1
            fi
            
            # Verify stopped
            if ! ps -p "$pid" > /dev/null 2>&1; then
                echo -e "${GREEN}   [OK] $service_name stopped${NC}"
                ((stopped_count++))
            else
                echo -e "${RED}   [FAIL] Failed to stop $service_name${NC}"
            fi
        else
            echo -e "${YELLOW}$service_name not running${NC}"
        fi
        rm -f "$pid_file"
    else
        echo -e "${YELLOW}$service_name PID file not found${NC}"
    fi
}

# Stop services
stop_service "Backend"
stop_service "Frontend"

# Kill any remaining uvicorn or vite processes
echo ""
echo -e "${YELLOW}Cleaning up any remaining processes...${NC}"

# Kill uvicorn (backend) - force kill
pkill -9 -f "uvicorn web.main" 2>/dev/null && echo -e "${GREEN}   [OK] Cleaned up uvicorn processes${NC}" || true

# Kill vite (frontend) - force kill
pkill -9 -f "vite" 2>/dev/null && echo -e "${GREEN}   [OK] Cleaned up vite processes${NC}" || true

# Kill node processes running dev server
pkill -9 -f "npm run dev" 2>/dev/null && echo -e "${GREEN}   [OK] Cleaned up npm processes${NC}" || true

echo ""
if [ $stopped_count -gt 0 ]; then
    echo -e "${GREEN} All services stopped successfully!${NC}"
else
    echo -e "${YELLOW}No services were running${NC}"
fi
echo ""
