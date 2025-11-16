#!/bin/bash
# Script to stop and restart the backend server

echo "Stopping existing backend servers on port 8000..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || echo "No existing servers found"

sleep 1

echo "Starting backend server..."
cd "$(dirname "$0")"
source venv/bin/activate
cd backend
python main.py

