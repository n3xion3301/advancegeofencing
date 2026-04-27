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

class DualModeGeofencingSystem:
    def __init__(self):
        self.geofence = GeofenceMonitor()
        self.camera = TermuxCameraController()
        self.telegram = TelegramNotifier()
        self.location_provider = AndroidLocationProvider()
        self.previous_location = None
        self.breach_count = 0
        self.away_mode = False  # Track if user is away
        self.away_threshold_meters = 50  # Consider "away" if >200m from home
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
        
        # Determine if user is away from home
        was_away = self.away_mode
        self.away_mode = distance > self.away_threshold_meters
        
        # Status indicators
        status = "🟢 HOME" if is_inside else "🔴 AWAY"
        mode_indicator = "🏠 AT HOME" if not self.away_mode else "✈️ AWAY MODE"
        
        self.log_event(
            f"📍 {status} | {mode_indicator} | Distance: {distance:.1f}m | "
            f"Lat: {current_location[0]:.6f}, Lon: {current_location[1]:.6f} | "
            f"Accuracy: ±{accuracy:.1f}m | Speed: {speed:.1f}m/s"
        )
        
        # Alert when transitioning to away mode
        if not was_away and self.away_mode:
            self.log_event("✈️ AWAY MODE ACTIVATED - Home monitoring enabled")
            if self.telegram.enabled:
                self.telegram.send_message(
                    f"✈️ *Away Mode Activated*\n\n"
                    f"You're now {distance:.0f}m from home.\n"
                    f"🔔 You'll be alerted if anyone enters your property."
                )
        
        # Alert when returning home
        if was_away and not self.away_mode:
            self.log_event("🏠 WELCOME HOME - Away mode deactivated")
            if self.telegram.enabled:
                self.telegram.send_message("🏠 *Welcome Home!*\n\nAway mode deactivated.")
        
        # Check for breach
        if self.previous_location:
            if self.geofence.check_breach(current_location, self.previous_location):
                self.handle_breach(current_location, location_data)
        
        self.previous_location = current_location
    
    def handle_breach(self, location, location_data):
        self.breach_count += 1
        accuracy = location_data.get('accuracy', 0)
        speed = location_data.get('speed', 0)
        
        # Different alerts based on mode
        if self.away_mode:
            # CRITICAL: Someone entering while you're away!
            breach_type = "🚨 INTRUDER ALERT"
            message = (
                f"🚨 *CRITICAL: INTRUDER DETECTED!*\n\n"
                f"Someone entered your property while you're away!\n\n"
                f"*Breach #{self.breach_count}*\n"
                f"📅 Time: `{time.strftime('%Y-%m-%d %H:%M:%S')}`\n"
                f"📍 Location: `{location[0]:.6f}, {location[1]:.6f}`\n"
                f"🎯 Accuracy: ±{accuracy:.1f}m\n"
                f"🏃 Speed: {speed:.1f}m/s\n\n"
                f"📸 Capturing photos..."
            )
        else:
            # Normal: You're arriving home
            breach_type = "🏠 ARRIVAL DETECTED"
            message = (
                f"🏠 *Welcome Home!*\n\n"
                f"*Arrival #{self.breach_count}*\n"
                f"📅 Time: `{time.strftime('%Y-%m-%d %H:%M:%S')}`\n"
                f"📍 Location: `{location[0]:.6f}, {location[1]:.6f}`\n"
                f"🎯 Accuracy: ±{accuracy:.1f}m"
            )
        
        self.log_event(f"{breach_type} - Breach #{self.breach_count}")
        
        if self.telegram.enabled:
            self.telegram.send_message(message)
            self.telegram.send_location(location[0], location[1], breach_type)
        
        # Always capture photos for security
        self.log_event("📸 Starting camera capture...")
        recording_thread = threading.Thread(
            target=self._record_breach, 
            args=(location, self.away_mode)
        )
        recording_thread.daemon = True
        recording_thread.start()
    
    def _record_breach(self, location, is_intruder):
        try:
            results = self.camera.start_recording(duration_seconds=30)
            
            if isinstance(results, dict) and results.get('photos'):
                self.log_event(f"✅ Captured {len(results['photos'])} photos")
                
                if self.telegram.enabled:
                    caption_prefix = "🚨 INTRUDER" if is_intruder else "🏠 Arrival"
                    
                    for i, photo in enumerate(results['photos'], 1):
                        self.log_event(f"📤 Sending photo {i}/{len(results['photos'])}")
                        caption = f"{caption_prefix} - Photo {i}/{len(results['photos'])}"
                        self.telegram.send_file(photo, caption)
                        time.sleep(1)
                    
                    self.log_event("✅ All photos sent to Telegram")
            else:
                self.log_event(f"📝 Breach logged: {results}")
                
        except Exception as e:
            self.log_event(f"❌ Recording failed: {e}")
    
    def run(self):
        print("=" * 60)
        print("🛡️  Dual-Mode Geofencing Security System")
        print("=" * 60)
        
        self.log_event("System starting...")
        
        print("\n📱 Testing GPS access...")
        test_location = self.location_provider.get_current_location()
        
        if test_location:
            distance = self.geofence.get_distance_from_center(
                (test_location['latitude'], test_location['longitude'])
            )
            self.away_mode = distance > self.away_threshold_meters
            
            print(f"✅ GPS working!")
            print(f"   Latitude: {test_location['latitude']:.6f}")
            print(f"   Longitude: {test_location['longitude']:.6f}")
            print(f"   Distance from home: {distance:.1f}m")
            print(f"   Mode: {'✈️ AWAY' if self.away_mode else '🏠 HOME'}")
            
            if self.telegram.enabled:
                mode_status = "✈️ Away Mode" if self.away_mode else "🏠 Home Mode"
                startup_msg = f"""
🟢 *Dual-Mode Security System Started*

📍 Current: `{test_location['latitude']:.6f}, {test_location['longitude']:.6f}`
🎯 Home: `{self.geofence.center[0]:.6f}, {self.geofence.center[1]:.6f}`
📏 Distance: {distance:.0f}m
🔔 Mode: {mode_status}
📸 Camera: {'✅ Enabled' if self.camera.camera_available else '❌ Disabled'}

{'🚨 *INTRUDER ALERTS ACTIVE*' if self.away_mode else '🏠 Home monitoring active'}
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
                self.telegram.send_message("🔴 *Security System Stopped*")
            print("\n👋 Shutting down...")

if __name__ == "__main__":
    system = DualModeGeofencingSystem()
    system.run()
