#!/bin/bash
if [ -f logs/indoor-service.pid ]; then
    PID=$(cat logs/indoor-service.pid)
    echo "🛑 Stopping indoor service (PID: $PID)..."
    kill $PID
    rm logs/indoor-service.pid
    echo "✅ Indoor service stopped!"
else
    echo "❌ Indoor service not running"
fi
