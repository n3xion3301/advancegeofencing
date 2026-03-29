#!/bin/bash
echo "👻 Starting WiFi Entity Detector..."
termux-wake-lock
nohup python3 src/wifi_entity_detector.py > logs/wifi-detector.log 2>&1 &
echo $! > logs/wifi-detector.pid
echo "✅ WiFi detector started! PID: $(cat logs/wifi-detector.pid)"
echo "📋 View logs: tail -f logs/wifi-detector.log"
