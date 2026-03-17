import time
import threading
import os
from pathlib import Path
from dotenv import load_dotenv
from geofence_monitor import GeofenceMonitor
from termux_camera_controller import TermuxCameraController
from telegram_notifier import TelegramNotifier
from android_location import AndroidLocationProvider
from network_detector import NetworkDetector
from home_recorder import HomeRecorder

load_dotenv()

class DualModeGeofencingSystem:
    def __init__(self):
        self.geofence = GeofenceMonitor()
        self.camera = TermuxCameraController()
        self.telegram = TelegramNotifier()
        self.location_provider = AndroidLocationProvider()
        self.network = NetworkDetector()
        self.home_recorder = HomeRecorder()
        self.previous_location = None
        self.breach_count = 0
        self.away_mode = False
        self.away_threshold_meters = 200
        Path('logs').mkdir(exist_ok=True)
        
    def log_event(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}\n"
        with open('logs/events.log', 'a') as f:
            f.write(log_message)
        print(log_message.strip())
    
    def handle_location_update(self, location_data):
        current_location = (location_data['latitude'], location_data['longitude'])
        accuracy = location_data.get('accuracy', 0)
        speed = location_data.get('speed', 0)
        
        distance = self.geofence.get_distance_from_center(current_location)
        is_inside = self.geofence.is_inside_geofence(current_location)
        
        if accuracy and accuracy > 100:
            self.log_event(f"⚠️  Low accuracy: {accuracy:.1f}m - skipping")
            return
        
        was_away = self.away_mode
        self.away_mode = distance > self.away_threshold_meters
        
        status = "🟢 HOME" if is_inside else "🔴 AWAY"
        mode_indicator = "🏠 AT HOME" if not self.away_mode else "✈️ AWAY MODE"
        
        self.log_event(
            f"📍 {status} | {mode_indicator} | Distance: {distance:.1f}m | "
            f"Lat: {current_location[0]:.6f}, Lon: {current_location[1]:.6f} | "
            f"Accuracy: ±{accuracy:.1f}m | Speed: {speed:.1f}m/s"
        )
        
        if not was_away and self.away_mode:
            self.log_event("✈️ AWAY MODE ACTIVATED - Home monitoring enabled")
        
        if was_away and not self.away_mode:
            self.log_event("🏠 WELCOME HOME - Away mode deactivated")
        
        # Check for geofence breach (crossing 50m boundary)
        if self.previous_location:
            if self.geofence.check_breach(current_location, self.previous_location):
                if self.away_mode:
                    # Away mode - intruder alert
                    self.handle_breach(current_location, location_data)
                else:
                    # Home mode - backyard exploration capture
                    self.log_event("🌌 GEOFENCE BREACH - Capturing backyard exploration moment!")
                    threading.Thread(target=self._capture_home_moment, daemon=True).start()
        
        self.previous_location = current_location
    
    def _capture_home_moment(self):
        """Capture quantum world photo when crossing geofence"""
        photo = self.home_recorder.capture_quantum_moment()
        if photo:
            self.log_event(f"✅ Backyard exploration captured: {photo}")
