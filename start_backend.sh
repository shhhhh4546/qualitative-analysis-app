#!/bin/bash

# Start Backend Server
cd "$(dirname "$0")"
source venv/bin/activate 2>/dev/null || python -m venv venv && source venv/bin/activate
pip install -r requirements.txt -q
cd backend
python main.py

