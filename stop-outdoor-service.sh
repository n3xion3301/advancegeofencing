#!/bin/bash
if [ -f logs/outdoor-service.pid ]; then
    PID=$(cat logs/outdoor-service.pid)
    echo "🛑 Stopping outdoor service (PID: $PID)..."
    kill $PID
    rm logs/outdoor-service.pid
    echo "✅ Outdoor service stopped!"
else
    echo "❌ Outdoor service not running"
fi
