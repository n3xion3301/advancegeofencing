#!/bin/bash
echo "📊 GEOFENCE SERVICES STATUS"
echo "================================"
echo ""
echo "🏠 INDOOR SERVICE:"
if [ -f logs/indoor-service.pid ]; then
    PID=$(cat logs/indoor-service.pid)
    if ps -p $PID > /dev/null; then
        echo "   ✅ RUNNING (PID: $PID)"
        echo "   Last 3 logs:"
        tail -3 logs/indoor-service.log | sed 's/^/      /'
    else
        echo "   ❌ STOPPED"
    fi
else
    echo "   ❌ NOT RUNNING"
fi
echo ""
echo "🌳 OUTDOOR SERVICE:"
if [ -f logs/outdoor-service.pid ]; then
    PID=$(cat logs/outdoor-service.pid)
    if ps -p $PID > /dev/null; then
        echo "   ✅ RUNNING (PID: $PID)"
        echo "   Last 3 logs:"
        tail -3 logs/outdoor-service.log | sed 's/^/      /'
    else
        echo "   ❌ STOPPED"
    fi
else
    echo "   ❌ NOT RUNNING"
fi
echo ""
echo "================================"
