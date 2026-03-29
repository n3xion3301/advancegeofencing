#!/bin/bash
echo "🛑 Stopping ALL geofence services..."
echo ""
./stop-indoor-service.sh
echo ""
./stop-outdoor-service.sh
echo ""
termux-wake-unlock
echo "✅ All services stopped!"
