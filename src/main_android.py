import time
import threading
import os
from pathlib import Path
from dotenv import load_dotenv
from geofence_monitor import GeofenceMonitor
from camera_controller import CameraController
from telegram_notifier import TelegramNotifier
from android_location import AndroidLocationProvider

# Load environment variables
load_dotenv()

class AndroidGeofencingSystem:
    def __init__(self):
        self.geofence = GeofenceMonitor()
        self.camera = CameraController()
        self.telegram = TelegramNotifier()
        self.location_provider = AndroidLocationProvider()
        self.previous_location = None
        self.breach_count = 0
        
        # Create logs directory
        Path('logs').mkdir(exist_ok=True)
        
    def log_event(self, message):
        """Log events to file"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}\n"
        
        with open('logs/events.log', 'a') as f:
            f.write(log_message)
        
        print(log_message.strip())
    
    def handle_location_update(self, location_data):
        """Process location updates"""
        current_location = (
            location_data['latitude'],
            location_data['longitude']
        )
        
        accuracy = location_data.get('accuracy', 0)
        speed = location_data.get('speed', 0)
        
        # Get distance from geofence center
        distance = self.geofence.get_distance_from_center(current_location)
        is_inside = self.geofence.is_inside_geofence(current_location)
        
        # Only process if accuracy is reasonable (< 100 meters)
        if accuracy and accuracy > 100:
            self.log_event(f"⚠️  Low accuracy: {accuracy:.1f}m - skipping")
            return
        
        # Log location update with status
        status = "🟢 INSIDE" if is_inside else "🔴 OUTSIDE"
        self.log_event(
            f"📍 {status} | Distance: {distance:.1f}m | "
            f"Lat: {current_location[0]:.6f}, Lon: {current_location[1]:.6f} | "
            f"Accuracy: ±{accuracy:.1f}m | Speed: {speed:.1f}m/s"
        )
        
        # Check for breach
        if self.previous_location:
            if self.geofence.check_breach(current_location, self.previous_location):
                self.handle_breach(current_location, location_data)
        
        self.previous_location = current_location
    
    def handle_breach(self, location, location_data):
        """Handle geofence breach event"""
        self.breach_count += 1
        
        accuracy = location_data.get('accuracy', 0)
        speed = location_data.get('speed', 0)
        
        breach_msg = (
            f"🚨 BREACH #{self.breach_count} DETECTED\n"
            f"Location: {location[0]:.6f}, {location[1]:.6f}\n"
            f"Accuracy: ±{accuracy:.1f}m\n"
            f"Speed: {speed:.1f}m/s"
        )
        
        self.log_event(breach_msg)
        
        # Send Telegram notification
        if self.telegram.enabled:
            self.telegram.send_breach_alert(
                location, accuracy, speed, self.breach_count
            )
        
        # Start recording in separate thread
        self.log_event("🎥 Starting camera recording...")
        recording_thread = threading.Thread(
            target=self._record_breach,
            args=(location,)
        )
        recording_thread.daemon = True
        recording_thread.start()
    
    def _record_breach(self, location):
        """Record video on breach"""
        try:
            video_file = self.camera.start_recording(duration_seconds=60)
            self.log_event(f"✅ Recording saved: {video_file}")
            
            # Send file via Telegram if available
            if self.telegram.enabled and video_file:
                self.log_event("📤 Sending file to Telegram...")
                if self.telegram.send_file(video_file, f"Breach recording at {location}"):
                    self.log_event("✅ File sent to Telegram")
                else:
                    self.log_event("❌ Failed to send file to Telegram")
                    
        except Exception as e:
            self.log_event(f"❌ Recording failed: {e}")
    
    def run(self):
        """Main monitoring loop"""
        print("=" * 60)
        print("🛡️  Android Geofencing Camera System with Telegram")
        print("=" * 60)
        
        self.log_event("System starting...")
        
        # Check if running on Android/Termux
        if not os.path.exists('/data/data/com.termux'):
            print("⚠️  Warning: Not running in Termux environment")
        
        # Test location access
        print("\n📱 Testing GPS access...")
        test_location = self.location_provider.get_current_location()
        
        if test_location:
            print(f"✅ GPS working!")
            print(f"   Latitude: {test_location['latitude']:.6f}")
            print(f"   Longitude: {test_location['longitude']:.6f}")
            print(f"   Accuracy: ±{test_location.get('accuracy', 0):.1f}m")
            
            # Send startup notification
            if self.telegram.enabled:
                startup_msg = f"""
🟢 *Geofencing System Started*

📍 Current Location:
`{test_location['latitude']:.6f}, {test_location['longitude']:.6f}`

🎯 Geofence Center:
`{self.geofence.center[0]:.6f}, {self.geofence.center[1]:.6f}`

📏 Radius: {self.geofence.radius}m
⏱️ Monitoring every 5 seconds
"""
                self.telegram.send_message(startup_msg)
                self.telegram.send_location(
                    test_location['latitude'],
                    test_location['longitude'],
                    "Current Position"
                )
        else:
            print("❌ GPS not available!")
            print("\nTroubleshooting:")
            print("1. Install Termux:API app from F-Droid")
            print("2. Run: pkg install termux-api")
            print("3. Grant location permissions to Termux")
            print("4. Enable GPS on your device")
            return
        
        print("\n🔄 Starting continuous monitoring...")
        print("Press Ctrl+C to stop\n")
        
        # Start continuous tracking
        try:
            self.location_provider.start_continuous_tracking(
                self.handle_location_update,
                interval=5  # Check every 5 seconds
            )
        except KeyboardInterrupt:
            self.log_event("System shutdown requested")
            
            # Send shutdown notification
            if self.telegram.enabled:
                self.telegram.send_message("🔴 *Geofencing System Stopped*")
            
            print("\n👋 Shutting down...")
        except Exception as e:
            self.log_event(f"Fatal error: {e}")
            print(f"\n❌ Fatal error: {e}")

if __name__ == "__main__":
    system = AndroidGeofencingSystem()
    system.run()
