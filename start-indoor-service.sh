#!/bin/bash
echo "🏠 Starting indoor recording service..."
termux-wake-lock
nohup python3 src/indoor_recording_service.py > logs/indoor-service.log 2>&1 &
echo $! > logs/indoor-service.pid
echo "✅ Indoor service started! PID: $(cat logs/indoor-service.pid)"
echo "📋 View logs: tail -f logs/indoor-service.log"
