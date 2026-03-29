#!/bin/bash
echo "🌳 Starting outdoor geofence service..."
termux-wake-lock
nohup python3 src/outdoor_geofence_service.py > logs/outdoor-service.log 2>&1 &
echo $! > logs/outdoor-service.pid
echo "✅ Outdoor service started! PID: $(cat logs/outdoor-service.pid)"
echo "📋 View logs: tail -f logs/outdoor-service.log"
