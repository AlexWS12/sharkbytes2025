#!/bin/bash
# Start the FastAPI backend server

echo "🚀 Starting FastAPI Backend..."
echo "================================"

# Navigate to project root
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  Warning: Virtual environment not found. Run ./setup_venv.sh first"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found"
    echo "Please create a .env file with your Supabase credentials"
    exit 1
fi

# Start FastAPI with uvicorn
echo "🌐 Starting server at http://localhost:5000"
echo "📚 API docs will be at http://localhost:5000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn web.main:app --host 0.0.0.0 --port 5000 --reload
