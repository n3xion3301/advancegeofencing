import subprocess
import json
import time
import shutil

class AndroidLocationProvider:
    def __init__(self):
        self.last_location = None
        self.location_enabled = self._check_location_available()

    def _check_location_available(self):
        """Check if Termux API is available"""
        try:
            termux_location_path = shutil.which('termux-location')
            if termux_location_path:
                print(f"✅ Found termux-location at: {termux_location_path}")
                return True

            result = subprocess.run(
                ['termux-location', '-h'],
                capture_output=True,
                timeout=2
            )
            return True
        except Exception as e:
            print(f"⚠️  Termux API check failed: {e}")
            return False

    def get_current_location(self):
        """Get location using Termux API"""
        if not self.location_enabled:
            print("❌ Termux API not available")
            return None

        try:
            # Simple termux-location call (no -r once flag)
            result = subprocess.run(
                ['termux-location'],
                capture_output=True,
                text=True,
                timeout=30  # Longer timeout
            )

            if result.returncode == 0 and result.stdout.strip():
                location_data = json.loads(result.stdout)

                latitude = location_data.get('latitude')
                longitude = location_data.get('longitude')

                if latitude is not None and longitude is not None:
                    self.last_location = {
                        'latitude': latitude,
                        'longitude': longitude,
                        'accuracy': location_data.get('accuracy', 0),
                        'provider': location_data.get('provider', 'unknown')
                    }
                    print(f"📍 Location: ({latitude:.6f}, {longitude:.6f}) ±{location_data.get('accuracy', 0):.1f}m")
                    return self.last_location

            print(f"⚠️  Location failed: {result.stderr}")
            return self.last_location

        except subprocess.TimeoutExpired:
            print("⏱️  Location timeout (30s) - retrying next cycle")
            return self.last_location
        except Exception as e:
            print(f"❌ Location error: {e}")
            return self.last_location
