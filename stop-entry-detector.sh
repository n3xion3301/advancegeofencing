#!/bin/bash
if [ -f logs/entry-detector.pid ]; then
    PID=$(cat logs/entry-detector.pid)
    echo "🛑 Stopping entry detector (PID: $PID)..."
    kill $PID
    rm logs/entry-detector.pid
    echo "✅ Entry detector stopped!"
else
    echo "❌ Entry detector not running"
fi
