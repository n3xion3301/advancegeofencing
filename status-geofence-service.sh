#!/bin/bash
if [ -f logs/geofence-service.pid ]; then
    PID=$(cat logs/geofence-service.pid)
    if ps -p $PID > /dev/null; then
        echo "✅ Service is RUNNING (PID: $PID)"
        echo "📋 Last 10 log lines:"
        tail -10 logs/geofence-service.log
    else
        echo "❌ Service is STOPPED (stale PID file)"
        rm logs/geofence-service.pid
    fi
else
    echo "❌ Service is NOT running"
fi
