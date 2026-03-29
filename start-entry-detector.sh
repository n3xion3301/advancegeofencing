#!/bin/bash
echo "🚨 Starting Entry Detector..."
termux-wake-lock
nohup python3 src/entry_detector.py > logs/entry-detector.log 2>&1 &
echo $! > logs/entry-detector.pid
echo "✅ Entry detector started! PID: $(cat logs/entry-detector.pid)"
echo "📋 View logs: tail -f logs/entry-detector.log"
