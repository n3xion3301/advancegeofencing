#!/bin/bash
if [ -f logs/geofence-service.pid ]; then
    PID=$(cat logs/geofence-service.pid)
    echo "🛑 Stopping geofence service (PID: $PID)..."
    kill $PID
    rm logs/geofence-service.pid
    termux-wake-unlock
    echo "✅ Service stopped!"
else
    echo "❌ Service not running"
fi
