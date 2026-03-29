#!/bin/bash
echo "✨ Starting Entity Zone Monitor..."
termux-wake-lock
nohup python3 src/entity_zone_monitor.py > logs/entity-monitor.log 2>&1 &
echo $! > logs/entity-monitor.pid
echo "✅ Entity monitor started! PID: $(cat logs/entity-monitor.pid)"
echo "📋 View logs: tail -f logs/entity-monitor.log"
