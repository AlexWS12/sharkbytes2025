#!/bin/bash
# ========================================
# SharkBytes 2025 - Status Checker
# ========================================
# Check status of all services
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
echo -e "${BLUE}   📊 SharkBytes 2025 - Status${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

running_count=0
total_services=2

# Function to check service status
check_service() {
    local service_name=$1
    local service_lower=$(echo "$service_name" | tr '[:upper:]' '[:lower:]')
    local pid_file="$PID_DIR/${service_lower}.pid"
    local port=$2
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p "$pid" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ $service_name${NC} (PID: $pid)"
            
            # Check if port is listening
            if [ -n "$port" ]; then
                if netstat -tuln 2>/dev/null | grep -q ":$port "; then
                    echo -e "  ${BLUE}→${NC} Listening on port $port"
                else
                    echo -e "  ${YELLOW}⚠${NC} Process running but port $port not listening"
                fi
            fi
            
            ((running_count++))
            return 0
        else
            echo -e "${RED}✗ $service_name${NC} (Not running, stale PID file)"
            return 1
        fi
    else
        echo -e "${RED}✗ $service_name${NC} (Not running)"
        return 1
    fi
}

# Check services
check_service "Backend" 5000
check_service "Frontend" 5173

echo ""

# Check camera access
echo -e "${YELLOW}Camera Status:${NC}"
if lsof /dev/video0 2>/dev/null | grep -q "python"; then
    echo -e "  ${GREEN}✓${NC} Camera in use by backend sentry service"
elif lsof /dev/video0 2>/dev/null; then
    echo -e "  ${YELLOW}⚠${NC} Camera in use by another process"
    lsof /dev/video0 2>/dev/null | tail -n +2
else
    echo -e "  ${RED}✗${NC} Camera not in use"
fi

echo ""

# Summary
echo -e "${BLUE}========================================${NC}"
if [ $running_count -eq $total_services ]; then
    echo -e "${GREEN}All services are running! 🎉${NC}"
    echo ""
    echo -e "${BLUE}Access the application:${NC}"
    echo -e "  Frontend: http://localhost:5173"
    echo -e "  Backend:  http://localhost:5000"
    echo -e "  API Docs: http://localhost:5000/docs"
elif [ $running_count -gt 0 ]; then
    echo -e "${YELLOW}Some services are running ($running_count/$total_services)${NC}"
    echo ""
    echo -e "${YELLOW}To start all services:${NC}"
    echo -e "  ./start_project.sh"
else
    echo -e "${RED}No services are running${NC}"
    echo ""
    echo -e "${YELLOW}To start all services:${NC}"
    echo -e "  ./start_project.sh"
fi
echo -e "${BLUE}========================================${NC}"
echo ""
