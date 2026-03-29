#!/bin/bash
echo "🚀 Starting ALL geofence services..."
echo ""
./start-indoor-service.sh
echo ""
./start-outdoor-service.sh
echo ""
echo "✅ All services running!"
echo "📊 Check status: ./status-all-services.sh"
