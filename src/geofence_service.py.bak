#!/usr/bin/env python3
"""QUANTUM GEOFENCE SERVICE - Main quantum geofencing service"""
import json, time
from datetime import datetime
from pathlib import Path

try:
    from quantum_gps_tracker import QuantumGPSTracker
    from quantum_hardware_geofence import QuantumHardwareGeofence
    from quantum_camera import QuantumCamera
    from quantum_video_recorder import QuantumVideoRecorder
    from quantum_telegram_notifier import QuantumTelegramNotifier
except ImportError as e:
    print(f"⚠️  Import error: {e}")
    print("Make sure all quantum modules are in src/ directory")

class QuantumGeofenceService:
    def __init__(self):
        self.log_file = Path("logs/quantum/geofence_service.log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize quantum components
        self.gps = QuantumGPSTracker()
        self.geofence = QuantumHardwareGeofence()
        self.camera = QuantumCamera()
        self.video = QuantumVideoRecorder()
        self.telegram = QuantumTelegramNotifier()
        
        self.current_zone = None
    
    def log(self, msg):
        """Log message"""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] {msg}")
        with open(self.log_file, 'a') as f:
            f.write(f"[{ts}] {msg}\n")
    
    def handle_zone_entry(self, zone_name):
        """Handle zone entry event"""
        self.log(f"🔮 ZONE ENTRY: {zone_name}")
        
        # Take quantum photo
        self.camera.take_photo()
        
        # Send quantum notification
        self.telegram.send_zone_alert(zone_name, "ENTRY")
        
        self.current_zone = zone_name
    
    def handle_zone_exit(self, zone_name):
        """Handle zone exit event"""
        self.log(f"🔮 ZONE EXIT: {zone_name}")
        
        # Record quantum video
        self.video.record_video(10)
        
        # Send quantum notification
        self.telegram.send_zone_alert(zone_name, "EXIT")
        
        self.current_zone = None
    
    def run(self):
        """Run quantum geofence service"""
        self.log("🔮⚛️ QUANTUM GEOFENCE SERVICE STARTED")
        self.log("━" * 60)
        
        try:
            while True:
                # Get quantum-enhanced GPS position
                pos = self.gps.get_gps_position()
                
                if pos:
                    lat = pos['latitude']
                    lon = pos['longitude']
                    
                    # Check quantum geofence
                    zone = self.geofence.check_position(lat, lon)
                    
                    # Detect zone changes
                    if zone and zone != self.current_zone:
                        self.handle_zone_entry(zone)
                    elif not zone and self.current_zone:
                        self.handle_zone_exit(self.current_zone)
                
                time.sleep(10)
                
        except KeyboardInterrupt:
            self.log("🛑 Quantum Geofence Service stopped")

if __name__ == "__main__":
    service = QuantumGeofenceService()
    service.run()
