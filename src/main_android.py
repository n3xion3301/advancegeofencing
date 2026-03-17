import time
import threading
import os
from pathlib import Path
from dotenv import load_dotenv
from geofence_monitor import GeofenceMonitor
from termux_camera_controller import TermuxCameraController
from telegram_notifier import TelegramNotifier
from android_location import AndroidLocationProvider

load_dotenv()

class AndroidGeofencingSystem:
    def __init__(self):
        self.geofence = GeofenceMonitor()
        self.camera = TermuxCameraController()
        self.telegram = TelegramNotifier()
        self.location_provider = AndroidLocationProvider()
        self.previous_location = None
        self.breach_count = 0
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
        
        status = "🟢 INSIDE" if is_inside else "🔴 OUTSIDE"
        self.log_event(
            f"📍 {status} | Distance: {distance:.1f}m | "
            f"Lat: {current_location[0]:.6f}, Lon: {current_location[1]:.6f} | "
            f"Accuracy: ±{accuracy:.1f}m | Speed: {speed:.1f}m/s"
        )
        
        if self.previous_location:
            if self.geofence.check_breach(current_location, self.previous_location):
                self.handle_breach(current_location, location_data)
        
        self.previous_location = current_location
    
    def handle_breach(self, location, location_data):
        self.breach_count += 1
        accuracy = location_data.get('accuracy', 0)
        speed = location_data.get('speed', 0)
        
        breach_msg = (
            f"🚨 BREACH #{self.breach_count} DETECTED\n"
            f"Location: {location[0]:.6f}, {location[1]:.6f}\n"
            f"Accuracy: ±{accuracy:.1f}m | Speed: {speed:.1f}m/s"
        )
        
        self.log_event(breach_msg)
        
        if self.telegram.enabled:
            self.telegram.send_breach_alert(location, accuracy, speed, self.breach_count)
        
        self.log_event("📸 Starting camera capture...")
        recording_thread = threading.Thread(target=self._record_breach, args=(location,))
        recording_thread.daemon = True
        recording_thread.start()
    
    def _record_breach(self, location):
        try:
            results = self.camera.start_recording(duration_seconds=30)
            
            if isinstance(results, dict) and results.get('photos'):
                self.log_event(f"✅ Captured {len(results['photos'])} photos")
                
                if self.telegram.enabled:
                    for i, photo in enumerate(results['photos'], 1):
                        self.log_event(f"📤 Sending photo {i}/{len(results['photos'])}")
                        self.telegram.send_file(photo, f"Breach #{self.breach_count} - Photo {i}")
                        time.sleep(1)
                    self.log_event("✅ All photos sent to Telegram")
            else:
                self.log_event(f"📝 Breach logged: {results}")
                
        except Exception as e:
            self.log_event(f"❌ Recording failed: {e}")
    
    def run(self):
        print("=" * 60)
        print("🛡️  Android Geofencing Camera System")
        print("=" * 60)
        
        self.log_event("System starting...")
        
        print("\n📱 Testing GPS access...")
        test_location = self.location_provider.get_current_location()
        
        if test_location:
            print(f"✅ GPS working!")
            print(f"   Latitude: {test_location['latitude']:.6f}")
            print(f"   Longitude: {test_location['longitude']:.6f}")
            print(f"   Accuracy: ±{test_location.get('accuracy', 0):.1f}m")
            
            if self.telegram.enabled:
                startup_msg = f"""
🟢 *Geofencing System Started*

📍 Current: `{test_location['latitude']:.6f}, {test_location['longitude']:.6f}`
🎯 Geofence: `{self.geofence.center[0]:.6f}, {self.geofence.center[1]:.6f}`
📏 Radius: {self.geofence.radius}m
📸 Camera: {'✅ Enabled' if self.camera.camera_available else '❌ Disabled'}
"""
                self.telegram.send_message(startup_msg)
                self.telegram.send_location(
                    test_location['latitude'],
                    test_location['longitude'],
                    "Current Position"
                )
        else:
            print("❌ GPS not available!")
            return
        
        print("\n🔄 Starting continuous monitoring...")
        print("Press Ctrl+C to stop\n")
        
        try:
            self.location_provider.start_continuous_tracking(
                self.handle_location_update, interval=5
            )
        except KeyboardInterrupt:
            self.log_event("System shutdown requested")
            if self.telegram.enabled:
                self.telegram.send_message("🔴 *System Stopped*")
            print("\n👋 Shutting down...")

if __name__ == "__main__":
    system = AndroidGeofencingSystem()
    system.run()
