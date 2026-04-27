#!/usr/bin/env python3
"""
GPS/Location Services for Quantum Geofencing
Integrates with Termux API for real location data
"""
import subprocess
import json
from datetime import datetime
from pathlib import Path

class GPSLocationService:
    def __init__(self):
        self.location_history = []
        self.cache_file = Path("~/advancegeofencing/location_cache.json").expanduser()
        print("📍 GPS Location Service Initialized")
    
    def get_current_location(self):
        """Get current GPS location using Termux API"""
        try:
            result = subprocess.run(
                ['termux-location', '-p', 'gps'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                location = json.loads(result.stdout)
                return {
                    'lat': location['latitude'],
                    'lon': location['longitude'],
                    'accuracy': location.get('accuracy', 0),
                    'altitude': location.get('altitude', 0),
                    'speed': location.get('speed', 0),
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"⚠️  GPS error: {e}")
            return None
    
    def start_location_tracking(self):
        """Start continuous GPS tracking"""
        try:
            subprocess.Popen(
                ['termux-location', '-p', 'gps', '-r', 'location_updates'],
                stdout=subprocess.PIPE
            )
            print("✅ GPS tracking started")
            return True
        except Exception as e:
            print(f"❌ Failed to start tracking: {e}")
            return False
    
    def stop_location_tracking(self):
        """Stop GPS tracking"""
        try:
            subprocess.run(['termux-location', '-r', 'location_updates', 'off'])
            print("🛑 GPS tracking stopped")
        except Exception as e:
            print(f"⚠️  Error stopping: {e}")
    
    def add_to_history(self, location):
        """Add location to history"""
        if location:
            self.location_history.append(location)
            if len(self.location_history) > 100:
                self.location_history.pop(0)
            self.save_cache()
    
    def save_cache(self):
        """Save location history to cache"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.location_history, f, indent=2)
        except Exception as e:
            print(f"⚠️  Cache save error: {e}")
    
    def load_cache(self):
        """Load location history from cache"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    self.location_history = json.load(f)
                print(f"📂 Loaded {len(self.location_history)} cached locations")
            else:
                print("📂 No cache file found, starting fresh")
        except Exception as e:
            print(f"⚠️  Cache load error: {e}")
            self.location_history = []
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points (Haversine formula)"""
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371000  # Earth radius in meters
        
        lat1_rad = radians(lat1)
        lat2_rad = radians(lat2)
        delta_lat = radians(lat2 - lat1)
        delta_lon = radians(lon2 - lon1)
        
        a = sin(delta_lat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        distance = R * c
        return distance
    
    def is_inside_zone(self, current_location, zone_center, radius_meters):
        """Check if current location is inside a geofence zone"""
        if not current_location:
            return False
        
        distance = self.calculate_distance(
            current_location['lat'],
            current_location['lon'],
            zone_center['lat'],
            zone_center['lon']
        )
        
        return distance <= radius_meters
    
    def get_movement_vector(self):
        """Calculate movement direction and speed from history"""
        if len(self.location_history) < 2:
            return None
        
        recent = self.location_history[-2:]
        
        dlat = recent[1]['lat'] - recent[0]['lat']
        dlon = recent[1]['lon'] - recent[0]['lon']
        
        distance = self.calculate_distance(
            recent[0]['lat'], recent[0]['lon'],
            recent[1]['lat'], recent[1]['lon']
        )
        
        return {
            'direction': {'dlat': dlat, 'dlon': dlon},
            'distance': distance,
            'speed': recent[1].get('speed', 0)
        }

if __name__ == "__main__":
    import time
    
    gps = GPSLocationService()
    gps.load_cache()
    
    print("\n📍 GPS Location Service Test\n")
    
    # Get current location
    print("Getting current location...")
    location = gps.get_current_location()
    
    if location:
        print(f"✅ Location: {location['lat']:.6f}, {location['lon']:.6f}")
        print(f"   Accuracy: {location['accuracy']:.1f}m")
        print(f"   Altitude: {location['altitude']:.1f}m")
        print(f"   Speed: {location['speed']:.1f} m/s")
        
        gps.add_to_history(location)
        
        # Test zone detection
        test_zone = {
            'lat': location['lat'],
            'lon': location['lon']
        }
        
        inside = gps.is_inside_zone(location, test_zone, 100)
        print(f"\n🎯 Inside test zone (100m): {inside}")
        
        # Test movement vector
        if len(gps.location_history) >= 2:
            vector = gps.get_movement_vector()
            if vector:
                print(f"\n🧭 Movement:")
                print(f"   Distance: {vector['distance']:.1f}m")
                print(f"   Speed: {vector['speed']:.1f} m/s")
    else:
        print("❌ Could not get location")
        print("   Make sure Termux:API is installed")
        print("   Grant location permissions")
    
    print("\n✅ GPS Service Test Complete")
