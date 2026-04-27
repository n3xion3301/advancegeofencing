#!/usr/bin/env python3
"""QUANTUM HOME BASE TRACKER - Track exploration from home anchor"""
import json, time, math
from datetime import datetime
from pathlib import Path

try:
    from quantum_gps_tracker import QuantumGPSTracker
    from quantum_zone_teleporter import QuantumZoneTeleporter
    from quantum_analytics import QuantumAnalytics
    QUANTUM_AVAILABLE = True
except ImportError:
    QUANTUM_AVAILABLE = False

class QuantumHomeBaseTracker:
    def __init__(self, home_lat, home_lon, home_radius):
        self.log_file = Path("logs/quantum/home_base_tracker.log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # HOME BASE COORDINATES
        self.home_lat = home_lat
        self.home_lon = home_lon
        self.home_radius = home_radius
        
        if QUANTUM_AVAILABLE:
            self.gps = QuantumGPSTracker()
            self.analytics = QuantumAnalytics()
        
        self.exploration_log = []
        self.current_location = None
        self.at_home = True
        self.distance_traveled = 0
    
    def log(self, msg):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] {msg}")
        with open(self.log_file, 'a') as f:
            f.write(f"[{ts}] {msg}\n")
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points (Haversine formula)"""
        R = 6371000  # Earth radius in meters
        
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        
        a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c  # Distance in meters
    
    def check_home_status(self, current_lat, current_lon):
        """Check if currently at home"""
        distance = self.calculate_distance(
            self.home_lat, self.home_lon,
            current_lat, current_lon
        )
        
        return distance <= self.home_radius
    
    def track_exploration(self):
        """Track exploration from home base"""
        self.log("🏠 HOME BASE QUANTUM TRACKING STARTED")
        self.log(f"   Home: ({self.home_lat}, {self.home_lon})")
        self.log(f"   Radius: {self.home_radius}m")
        self.log("━" * 60)
        
        try:
            while True:
                if QUANTUM_AVAILABLE:
                    pos = self.gps.get_gps_position()
                else:
                    # Simulate for testing
                    pos = {'latitude': self.home_lat, 'longitude': self.home_lon}
                
                if pos:
                    lat = pos['latitude']
                    lon = pos['longitude']
                    
                    # Calculate distance from home
                    distance_from_home = self.calculate_distance(
                        self.home_lat, self.home_lon, lat, lon
                    )
                    
                    # Check if at home
                    currently_at_home = self.check_home_status(lat, lon)
                    
                    # Detect home entry/exit
                    if currently_at_home and not self.at_home:
                        self.log("🏠 RETURNED HOME!")
                        self.log(f"   Distance traveled: {self.distance_traveled:.2f}m")
                        if QUANTUM_AVAILABLE:
                            self.analytics.track_event('home_return', {
                                'distance': self.distance_traveled
                            })
                    
                    elif not currently_at_home and self.at_home:
                        self.log("🚀 LEFT HOME - EXPLORATION STARTED!")
                        if QUANTUM_AVAILABLE:
                            self.analytics.track_event('home_departure')
                    
                    self.at_home = currently_at_home
                    
                    # Log exploration
                    exploration_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'latitude': lat,
                        'longitude': lon,
                        'distance_from_home': distance_from_home,
                        'at_home': currently_at_home
                    }
                    self.exploration_log.append(exploration_entry)
                    
                    # Display status
                    status = "🏠 AT HOME" if currently_at_home else "🌍 EXPLORING"
                    self.log(f"{status} | Distance from home: {distance_from_home:.2f}m")
                    
                    # Calculate total distance traveled
                    if self.current_location:
                        segment_distance = self.calculate_distance(
                            self.current_location['latitude'],
                            self.current_location['longitude'],
                            lat, lon
                        )
                        self.distance_traveled += segment_distance
                    
                    self.current_location = {'latitude': lat, 'longitude': lon}
                
                time.sleep(10)  # Update every 10 seconds
                
        except KeyboardInterrupt:
            self.log("🛑 Home base tracking stopped")
            self.save_exploration_log()
    
    def save_exploration_log(self):
        """Save exploration log"""
        log_file = Path("data/exploration_log.json")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'home_base': {
                'latitude': self.home_lat,
                'longitude': self.home_lon,
                'radius': self.home_radius
            },
            'total_distance': self.distance_traveled,
            'exploration_log': self.exploration_log
        }
        
        with open(log_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.log(f"💾 Saved exploration log: {len(self.exploration_log)} entries")
    
    def get_exploration_stats(self):
        """Get exploration statistics"""
        return {
            'total_distance': self.distance_traveled,
            'total_entries': len(self.exploration_log),
            'currently_at_home': self.at_home
        }

if __name__ == "__main__":
    # CONFIGURE YOUR HOME COORDINATES HERE
    HOME_LAT = 0.0  # Replace with your home latitude
    HOME_LON = 0.0  # Replace with your home longitude
    HOME_RADIUS = 100  # Replace with your home radius in meters
    
    tracker = QuantumHomeBaseTracker(HOME_LAT, HOME_LON, HOME_RADIUS)
    tracker.track_exploration()
