# 🌍 Advanced Geofencing System for Android/Termux

[![Platform](https://img.shields.io/badge/Platform-Android%20%7C%20Termux-green.svg)](https://termux.com/)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-26%2F26%20Passing-brightgreen.svg)](test-all-tools.sh)

A powerful, real-time GPS-based geofencing system for Android devices using Termux. Automatically triggers camera recording and sends notifications when entering or exiting predefined geographic zones.

## ✨ Features

- 🎯 **Real-time GPS Tracking** - Location updates every 5 seconds with high accuracy
- 📸 **Automatic Camera Triggering** - Opens camera app automatically on zone breach
- 🔔 **Multi-Channel Notifications** - Android notifications + Telegram integration
- 🗺️ **Multiple Geofence Zones** - Configure unlimited zones with custom radius
- ⏰ **Smart Scheduling** - Active hours and quiet hours support
- 🛡️ **Cooldown System** - Prevents notification spam with configurable cooldowns
- 🎨 **Zone Customization** - Custom emojis, names, and trigger conditions per zone
- 📊 **Initial Position Detection** - Triggers notification if already inside zone on startup
- 🔄 **Dual Trigger Modes** - Entry and/or exit notifications
- 📝 **Comprehensive Logging** - Detailed logs for debugging and monitoring

## 🚀 Quick Start

### Prerequisites

- Android device with GPS
- [Termux](https://f-droid.org/en/packages/com.termux/) installed
- [Termux:API](https://f-droid.org/en/packages/com.termux.api/) app installed
- Internet connection (for Telegram notifications)

### Installation

```bash
# Clone the repository
git clone https://github.com/n3xion3301/advancegeofencing.git
cd advancegeofencing

# Install required packages
pkg update && pkg upgrade
pkg install python git termux-api

# Install Python dependencies
pip install requests geopy

# Grant Termux permissions
# Go to Android Settings → Apps → Termux → Permissions
# Enable: Location, Camera, Notifications

# Configure your zones
nano config/zones.json

# Configure Telegram (optional)
nano config/telegram_config.json

# Run tests
./test-all-tools.sh

# Start the service
bash start-geofence-service.sh

📋 Configuration
Zones Configuration (config/zones.json)


Insert at cursor
{
  "zones": [
    {
      "name": "HOME",
      "emoji": "🏠",
      "lat": 36.006975,
      "lon": -88.418078,
      "radius": 50,
      "trigger_on_enter": true,
      "trigger_on_exit": true,
      "active_hours": [0, 24],
      "cooldown_minutes": 30
    }
  ]
}

Zone Parameters:

name - Zone identifier (uppercase recommended)
emoji - Display emoji for notifications
lat / lon - Center coordinates (decimal degrees)
radius - Zone radius in meters
trigger_on_enter - Trigger when entering zone
trigger_on_exit - Trigger when exiting zone
active_hours - [start_hour, end_hour] in 24h format
cooldown_minutes - Minimum time between triggers

Telegram Configuration (config/telegram_config.json)


Insert at cursor
{
  "enabled": true,
  "bot_token": "YOUR_BOT_TOKEN",
  "chat_id": "YOUR_CHAT_ID"
}

Get Telegram Credentials:

Create bot: Talk to [@BotFather](https://t.me/botfather)
Get chat ID: Talk to [@userinfobot](https://t.me/userinfobot)

🎮 Usage
Start Services


Insert at cursor
# Main geofence service (recommended)
bash start-geofence-service.sh

# Outdoor-only service
bash start-outdoor-service.sh

# Check service status
bash status-all-services.sh

# View logs
tail -f logs/geofence-service.log

# Stop all services
bash stop-all-services.sh

Manual Testing


Insert at cursor
# Test GPS location
termux-location

# Test camera
termux-camera-photo test.jpg

# Test notification
termux-notification --title "Test" --content "Working!"

# Run comprehensive tests
./test-all-tools.sh

📱 How It Works

GPS Monitoring - Service continuously monitors your GPS location every 5 seconds
Zone Detection - Calculates distance from each configured zone center
Boundary Crossing - Detects when you enter or exit a zone
Trigger Actions:
📸 Opens camera app automatically
🔔 Sends Android notification with action buttons
📱 Sends Telegram message (if configured)
📝 Logs event with timestamp and distance


Cooldown - Prevents repeated triggers for configured duration

🛠️ Project Structure


Insert at cursor
advancegeofencing/
├── src/
│   ├── geofence_monitor.py           # Core geofencing logic
│   ├── android_location.py           # GPS location provider
│   ├── telegram_notifier.py          # Telegram integration
│   ├── geofence_background_service.py # Main service
│   └── outdoor_geofence_service.py   # Outdoor-only service
├── config/
│   ├── zones.json                    # Zone configurations
│   └── telegram_config.json          # Telegram settings
├── logs/                             # Service logs
├── photos/                           # Camera photos
├── videos/                           # Video recordings
├── start-geofence-service.sh         # Start main service
├── start-outdoor-service.sh          # Start outdoor service
├── stop-all-services.sh              # Stop all services
├── status-all-services.sh            # Check service status
├── test-all-tools.sh                 # Comprehensive test suite
└── README.md                         # This file

🧪 Testing
Run the comprehensive test suite:


Insert at cursor
./test-all-tools.sh

Tests Include:

✅ Termux API tools (location, camera, notifications)
✅ Configuration file validation
✅ Python script syntax checking
✅ Shell script existence
✅ Directory structure
✅ GPS functionality
✅ JSON validity
✅ Python module imports

Expected Result: 26/26 tests passing
📊 Example Output


Insert at cursor
🚀 Background Geofence Service Started (AUTO-OPEN CAMERA MODE)
📍 Monitoring 4 zones
⏰ 2026-03-29 05:29:08
📸 Camera app will open automatically on breach!

   🏠 HOME: (36.006975, -88.418078) r=50m
   🌳 PARK: (36.008, -88.418) r=100m
   🎮 PLAYGROUND: (36.009, -88.419) r=75m
   🌃 TOWN_CENTER: (36.0036, -88.4197) r=1000m

📍 Location: (36.005253, -88.421692) ±6.5m
🎯 Initial check: Already inside TOWN_CENTER!
🚨 🌃 TOWN_CENTER INSIDE (256.7m)
📸 Opening camera app...
✅ Telegram notifications enabled

🔧 Troubleshooting
GPS Not Working


Insert at cursor
# Check GPS permissions
termux-location

# If timeout, wait 30-60 seconds for first GPS fix
# Ensure you're outdoors or near a window

Camera Not Opening


Insert at cursor
# Test camera manually
am start -a android.media.action.IMAGE_CAPTURE

# Check camera permissions in Android settings

Service Not Starting


Insert at cursor
# Check logs
tail -f logs/geofence-service.log

# Verify Python dependencies
pip list | grep -E "requests|geopy"

# Run service directly to see errors
python src/geofence_background_service.py

Notifications Not Appearing


Insert at cursor
# Test notification manually
termux-notification --title "Test" --content "Working"

# Check notification permissions in Android settings
# Ensure Termux is not in battery optimization

🎯 Use Cases

🏠 Home Automation - Trigger smart home actions when arriving/leaving
📸 Automatic Recording - Record evidence when entering specific areas
🚗 Travel Logging - Auto-document visits to locations
👨‍👩‍👧‍👦 Family Safety - Get notified when family members arrive at locations
🏃 Fitness Tracking - Track visits to gyms, parks, running routes
🚨 Security - Alert when entering/leaving secure areas
📍 Location Reminders - Get reminded of tasks at specific locations

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
🙏 Acknowledgments

[Termux](https://termux.com/) - Android terminal emulator
[Termux:API](https://wiki.termux.com/wiki/Termux:API) - Android API access
[GeoPy](https://github.com/geopy/geopy) - Geocoding library
[Requests](https://requests.readthedocs.io/) - HTTP library

📞 Support

🐛 Issues: [GitHub Issues](https://github.com/n3xion3301/advancegeofencing/issues)
💬 Discussions: [GitHub Discussions](https://github.com/n3xion3301/advancegeofencing/discussions)
📧 Email: Create an issue for support

🔄 Changelog
v1.0.0 (2026-03-29)

✅ Initial release
✅ GPS-based geofencing with 5-second updates
✅ Automatic camera triggering
✅ Android notifications with action buttons
✅ Telegram integration
✅ Multiple zone support
✅ Cooldown and active hours system
✅ Initial position detection
✅ Comprehensive test suite (26/26 passing)


Made with ❤️ for Android/Termux users
⭐ Star this repo if you find it useful! ⭐
