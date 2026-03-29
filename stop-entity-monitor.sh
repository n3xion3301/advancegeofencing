#!/bin/bash
if [ -f logs/entity-monitor.pid ]; then
    PID=$(cat logs/entity-monitor.pid)
    echo "🛑 Stopping entity monitor (PID: $PID)..."
    kill $PID
    rm logs/entity-monitor.pid
    echo "✅ Entity monitor stopped!"
else
    echo "❌ Entity monitor not running"
fi
