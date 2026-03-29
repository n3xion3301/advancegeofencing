#!/bin/bash
echo "🚀 Starting background geofence service..."
termux-wake-lock
nohup python3 src/geofence_background_service.py > logs/geofence-service.log 2>&1 &
echo $! > logs/geofence-service.pid
echo "✅ Service started! PID: $(cat logs/geofence-service.pid)"
echo "📋 View logs: tail -f logs/geofence-service.log"
