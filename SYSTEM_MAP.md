# 🌌 QUANTUM GEOFENCING SYSTEM MAP 🗺️

## System Architecture Overview

Your system has 3 main layers:

1. QUANTUM CAMERA LAYER - Photo capture + quantum detection
2. GEOFENCING LAYER - Location tracking + zone monitoring  
3. ENTITY DETECTION LAYER - WiFi/network entity tracking

All layers connect to:
- Notification system (Telegram)
- Data storage (logs, recordings, captures)
- Control scripts (start/stop services)


## 📷 QUANTUM CAMERA SUBSYSTEM

Core Files:
- quantum_camera_detector.py (Main detection engine)
- quantum_visualizer.py (Physics visualizations)
- camera_visualizer_bridge.py (Connects camera to visualizer)
- camera_controller.py (Camera control)
- termux_camera_controller.py (Termux-specific)

Standalone Apps:
- quantum_camera_app_lite.py (Basic detection)
- quantum_camera_app_private.py (EXIF stripped)
- quantum_camera_visualizer_integrated.py (Full system)

Data Flow:
Camera → Capture → Quantum Analysis → Visualization → Save

Outputs:
- quantum_world/ (Captured images)
- quantum_logs/ (Detection logs)
- quantum_integrated/ (Full detection data)


## 🗺️ GEOFENCING SUBSYSTEM

Core Files:
- geofence_monitor.py (Main monitoring)
- geofence_background_service.py (Background service)
- outdoor_geofence_service.py (Outdoor tracking)
- indoor_recording_service.py (Indoor recording)
- geofence_notifier.py (Alerts)

Location & Routes:
- android_location.py (GPS location)
- route_tracker.py (Track routes)
- route_learner.py (Learn patterns)

Recording:
- home_recorder.py (Audio recording)
- home_video_recorder.py (Video recording)

Data Flow:
GPS Update → Zone Check → Trigger Action → Notify/Record

Outputs:
- routes/ (Route data)
- recordings/ (Audio/video)
- logs/ (Geofence events)

Control Scripts:
- start-geofence-service.sh
- stop-geofence-service.sh
- status-geofence-service.sh


## 👁️ ENTITY DETECTION SUBSYSTEM

Core Files:
- entity_zone_monitor.py (Main zone monitoring)
- wifi_entity_detector.py (WiFi-based detection)
- network_detector.py (Network scanning)
- entry_detector.py (Entry/exit detection)
- activity_detector.py (Activity monitoring)

Detection Methods:
- WiFi MAC address scanning
- Network device discovery
- Zone-based tracking
- Entry/exit events

Data Flow:
WiFi Scan → Entity Identified → Zone Assigned → Alert

Outputs:
- data/ (Entity data)
- logs/ (Detection events)

Control Scripts:
- start-entity-monitor.sh
- stop-entity-monitor.sh
- start-wifi-detector.sh
- stop-wifi-detector.sh
- start-entry-detector.sh
- stop-entry-detector.sh


## 🔔 NOTIFICATION SUBSYSTEM

Core Files:
- notification_service.py (Main notification service)
- telegram_notifier.py (Telegram bot integration)
- geofence_notifier.py (Geofence-specific alerts)

Notification Types:
- Quantum detection alerts
- Geofence entry/exit
- Entity detection
- Recording started/stopped
- System status updates

Data Flow:
Event Triggered → Notification Service → Telegram Bot → Your Phone

## 🔗 INTEGRATION POINTS

How the systems work together:

1. Quantum + Geofence:
   - Camera auto-triggers on zone entry
   - Quantum detection in specific zones

2. Entity + Geofence:
   - WiFi detection triggers in home zone
   - Entity tracking across zones

3. Recording + Detection:
   - Auto-record on quantum events
   - Record when entities detected

4. All Systems → Notifications:
   - Every event can trigger Telegram alert
   - Centralized notification service


## 📁 FILE STRUCTURE

advancegeofencing/
├── src/                    # All core modules
├── config/                 # Configuration files
├── data/                   # Entity/zone data
├── logs/                   # System logs
├── quantum_logs/           # Quantum detection logs
├── quantum_world/          # Quantum captures (66 test photos)
├── quantum_integrated/     # Full quantum data
├── routes/                 # Route learning data
├── recordings/             # Audio/video recordings
├── tests/                  # Test files
└── wigle-wifi-wardriving/  # WiFi wardriving data

## 🚀 STARTUP SEQUENCE

Recommended order:

1. Start background services:
   ./start-geofence-service.sh
   ./start-indoor-service.sh
   ./start-outdoor-service.sh

2. Start monitoring:
   ./start-entity-monitor.sh
   ./start-wifi-detector.sh
   ./start-entry-detector.sh

3. Start quantum camera (when needed):
   python quantum_camera_visualizer_integrated.py

4. Check status:
   ./status-all-services.sh

5. Stop everything:
   ./stop-all-services.sh

## 🎯 QUICK START

All services:
./start-all-services.sh

Check status:
./status-all-services.sh

Stop all:
./stop-all-services.sh

---
END OF SYSTEM MAP
