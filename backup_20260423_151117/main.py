import time
import threading
from geofence_monitor import GeofenceMonitor
from camera_controller import CameraController
from notification_service import NotificationService

class GeofencingCameraSystem:
    def __init__(self):
        self.geofence = GeofenceMonitor()
        self.camera = CameraController()
        self.notifier = NotificationService()
        self.previous_location = None
        
    def get_current_location(self):
        """Get device location - implement based on your platform"""
        # Option 1: GPS module (Raspberry Pi, etc.)
        # Option 2: Phone GPS via API
        # Option 3: WiFi triangulation
        # Placeholder - replace with actual implementation
        return (40.7128, -74.0060)
    
    def handle_breach(self, location):
        """Handle geofence breach event"""
        print(f"🚨 BREACH DETECTED at {location}")
        
        # Start recording in separate thread
        recording_thread = threading.Thread(
            target=self.camera.start_recording,
            args=(60,)  # 60 seconds recording
        )
        recording_thread.start()
        
        # Send notification
        self.notifier.send_alert(
            "Geofence Breach Detected",
            f"Someone entered your residence area at {location}"
        )
    
    def run(self):
        """Main monitoring loop"""
        print("🛡️  Geofencing Camera System Started")
        
        while True:
            try:
                current_location = self.get_current_location()
                
                if self.previous_location:
                    if self.geofence.check_breach(current_location, self.previous_location):
                        self.handle_breach(current_location)
                
                self.previous_location = current_location
                time.sleep(5)  # Check every 5 seconds
                
            except KeyboardInterrupt:
                print("\n👋 Shutting down...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    system = GeofencingCameraSystem()
    system.run()

