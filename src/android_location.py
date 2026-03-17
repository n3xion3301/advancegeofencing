import subprocess
import json
import time

class AndroidLocationProvider:
    def __init__(self):
        self.last_location = None
        self.location_enabled = self._check_location_available()
        
    def _check_location_available(self):
        """Check if Termux API is available"""
        try:
            result = subprocess.run(
                ['which', 'termux-location'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def get_current_location(self):
        """Get GPS location using Termux API"""
        if not self.location_enabled:
            print("❌ Termux API not available")
            return None
            
        try:
            # Request location from Termux API with GPS provider
            result = subprocess.run(
                ['termux-location', '-p', 'gps', '-r', 'once'],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode == 0 and result.stdout.strip():
                location_data = json.loads(result.stdout)
                
                latitude = location_data.get('latitude')
                longitude = location_data.get('longitude')
                accuracy = location_data.get('accuracy', 0)
                altitude = location_data.get('altitude', 0)
                bearing = location_data.get('bearing', 0)
                speed = location_data.get('speed', 0)
                
                if latitude and longitude:
                    self.last_location = (latitude, longitude)
                    return {
                        'latitude': latitude,
                        'longitude': longitude,
                        'accuracy': accuracy,
                        'altitude': altitude,
                        'bearing': bearing,
                        'speed': speed,
                        'timestamp': time.time()
                    }
            else:
                print(f"⚠️  Location request failed: {result.stderr}")
            
            # Return last known location if current fails
            if self.last_location:
                print("📍 Using last known location")
                return {
                    'latitude': self.last_location[0],
                    'longitude': self.last_location[1],
                    'accuracy': None,
                    'timestamp': time.time()
                }
                
        except subprocess.TimeoutExpired:
            print("⏱️  Location request timed out")
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse location data: {e}")
        except Exception as e:
            print(f"❌ Location error: {e}")
            
        return None
    
    def start_continuous_tracking(self, callback, interval=5):
        """Continuously track location and call callback on updates"""
        print(f"🔄 Starting continuous tracking (interval: {interval}s)")
        
        while True:
            try:
                location = self.get_current_location()
                if location:
                    callback(location)
                else:
                    print("⚠️  No location data available")
                    
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n⏹️  Stopping location tracking")
                break
            except Exception as e:
                print(f"❌ Tracking error: {e}")
                time.sleep(interval)
