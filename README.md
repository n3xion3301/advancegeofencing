# Advanced Geofencing Camera System

Automated camera recording system triggered by geofence breach detection.

## Features

- 🗺️ Circular and polygon geofence support
- 📹 Automatic camera recording on breach
- 🔔 Real-time notifications
- ⏱️ Configurable cooldown periods
- 📊 Breach logging and analytics

## Quick Start

### Installation

```bash
# Clone repository
git clone https://gitlab.com/n3xion3301/advancegeofencing.git
cd advancegeofencing

# Install dependencies
pip install -r requirements.txt

Configuration


Edit config/geofence_config.json with your coordinates:


{
  "residence": {
    "center": {
      "latitude": YOUR_LATITUDE,
      "longitude": YOUR_LONGITUDE
    },
    "radius_meters": 50
  }
}
Insert at cursor


Configure camera settings in config/camera_config.json


Run


python src/main.py
Insert at cursor

Architecture


├── config/          # Configuration files
├── src/             # Source code
│   ├── geofence_monitor.py
│   ├── camera_controller.py
│   ├── notification_service.py
│   └── main.py
├── tests/           # Unit tests
├── recordings/      # Video recordings
└── logs/            # System logs
Insert at cursor

Requirements


Python 3.8+
Webcam or IP camera
GPS module (optional, for automatic location tracking)

License

MIT License

## Android Setup (Termux)

### Prerequisites

1. Install **Termux** from F-Droid (NOT Google Play)
2. Install **Termux:API** from F-Droid
3. Grant location permissions to Termux

### Installation

```bash
# Update packages
pkg update && pkg upgrade

# Install required packages
pkg install python git termux-api

# Clone repository
git clone https://gitlab.com/n3xion3301/advancegeofencing.git
cd advancegeofencing

# Install Python dependencies
pip install -r requirements.txt

Configuration

Edit config/geofence_config.json with your residence coordinates:

nano config/geofence_config.json
Insert at cursor

Update the latitude and longitude values.
Running


# Simple run
python src/main_android.py

# Or use the startup script
./start_android.sh
Insert at cursor

Running in Background


# Start in background
nohup python src/main_android.py > logs/service.log 2>&1 &

# Check if running
ps aux | grep main_android

# Stop service
pkill -f main_android.py
Insert at cursor

Troubleshooting

GPS not working:

Ensure Termux:API is installed
Grant location permissions: Settings → Apps → Termux → Permissions
Enable GPS/Location on your device
Try running: termux-location to test

Camera not working:

Grant camera permissions to Termux
Test with: termux-camera-photo test.jpg


Service stops when screen locks:

Use termux-wake-lock (included in start script)
Consider using Termux:Boot for auto-start

