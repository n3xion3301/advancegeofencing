#!/bin/bash
if [ -f logs/wifi-detector.pid ]; then
    PID=$(cat logs/wifi-detector.pid)
    echo "🛑 Stopping WiFi detector (PID: $PID)..."
    kill $PID
    rm logs/wifi-detector.pid
    echo "✅ WiFi detector stopped!"
else
    echo "❌ WiFi detector not running"
fi
