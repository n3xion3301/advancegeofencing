#!/data/data/com.termux/files/usr/bin/bash

echo "🚀 Starting Advanced Geofencing System"

# Acquire wakelock to prevent device sleep
termux-wake-lock

# Navigate to project directory
cd ~/advancegeofencing

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start the service
python src/main_android.py

# Release wakelock on exit
termux-wake-unlock
