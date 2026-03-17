import time
import threading
import os
from pathlib import Path
from geofence_monitor import GeofenceMonitor
from camera_controller import CameraController
from notification_service import NotificationService
from android_location import AndroidLocationProvider

class AndroidGeofencingSystem:
    def __init__(self):
        self.geofence = GeofenceMonitor()
        self.camera = CameraController()
        self.notifier = NotificationService()
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
        
        # Only process if accuracy is reasonable (< 100 meters)
        if accuracy and accuracy > 100:
            self.log_event(f"⚠️  Low accuracy: {accuracy:.1f}m - skipping")
            return
        
        # Log location update
        self.log_event(
            f"📍 Lat: {current_location[0]:.6f}, "
            f"Lon: {current_location[1]:.6f}, "
            f"Accuracy: ±{accuracy:.1f}m, "
            f"Speed: {speed:.1f}m/s"
        )
        
        # Check for breach
        if self.previous_location:
            if self.geofence.check_breach(current_location, self.previous_location):
                self.handle_breach(current_location, location_data)
        
        self.previous_location = current_location
    
    def handle_breach(self, location, location_data):
        """Handle geofence breach event"""
        self.breach_count += 1
        
        breach_msg = (
            f"🚨 BREACH #{self.breach_count} DETECTED\n"
            f"Location: {location[0]:.6f}, {location[1]:.6f}\n"
            f"Accuracy: ±{location_data.get('accuracy', 0):.1f}m\n"
            f"Speed: {location_data.get('speed', 0):.1f}m/s"
        )
        
        self.log_event(breach_msg)
        
        # Send notification
        self.notifier.send_alert(
            "🚨 Geofence Breach Detected",
            breach_msg
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
            
            # Optionally send notification with video path
            self.notifier.send_alert(
                "Recording Complete",
                f"Video saved: {video_file}"
            )
        except Exception as e:
            self.log_event(f"❌ Recording failed: {e}")
    
    def run(self):
        """Main monitoring loop"""
        print("=" * 50)
        print("🛡️  Android Geofencing Camera System")
        print("=" * 50)
        
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
            print("\n👋 Shutting down...")
        except Exception as e:
            self.log_event(f"Fatal error: {e}")
            print(f"\n❌ Fatal error: {e}")

if __name__ == "__main__":
    system = AndroidGeofencingSystem()
    system.run()
