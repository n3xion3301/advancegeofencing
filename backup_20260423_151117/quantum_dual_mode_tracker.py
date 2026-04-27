#!/usr/bin/env python3
"""QUANTUM DUAL MODE TRACKER - Exploration & Private modes"""
import json, time, math
from datetime import datetime
from pathlib import Path

try:
    from quantum_gps_tracker import QuantumGPSTracker
    from quantum_analytics import QuantumAnalytics
    QUANTUM_AVAILABLE = True
except ImportError:
    QUANTUM_AVAILABLE = False

class QuantumDualModeTracker:
    def __init__(self, home_lat, home_lon, home_radius):
        self.log_file = Path("logs/quantum/dual_mode_tracker.log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # HOME BASE
        self.home_lat = home_lat
        self.home_lon = home_lon
        self.home_radius = home_radius
        
        if QUANTUM_AVAILABLE:
            self.gps = QuantumGPSTracker()
            self.analytics = QuantumAnalytics()
        
        self.mode = "EXPLORATION"  # or "PRIVATE"
        self.exploration_log = []
        self.distance_traveled = 0
    
    def log(self, msg):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] {msg}")
        with open(self.log_file, 'a') as f:
            f.write(f"[{ts}] {msg}\n")
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points"""
        R = 6371000  # Earth radius in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        
        a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def is_inside_home(self, lat, lon):
        """Check if inside home radius"""
        distance = self.calculate_distance(self.home_lat, self.home_lon, lat, lon)
        return distance <= self.home_radius
    
    def exploration_mode(self):
        """🌍 EXPLORATION MODE - Track everywhere, never stop"""
        self.mode = "EXPLORATION"
        self.log("🌍 EXPLORATION MODE ACTIVATED")
        self.log("   Tracking EVERYWHERE you go!")
        self.log("   Home is anchor point only")
        self.log("━" * 60)
        
        last_pos = None
        
        try:
            while True:
                if QUANTUM_AVAILABLE:
                    pos = self.gps.get_gps_position()
                else:
                    pos = {'latitude': self.home_lat, 'longitude': self.home_lon}
                
                if pos:
                    lat = pos['latitude']
                    lon = pos['longitude']
                    
                    # Distance from home
                    distance_from_home = self.calculate_distance(
                        self.home_lat, self.home_lon, lat, lon
                    )
                    
                    # Check if at home
                    at_home = self.is_inside_home(lat, lon)
                    
                    # Log everything (never stops!)
                    entry = {
                        'timestamp': datetime.now().isoformat(),
                        'latitude': lat,
                        'longitude': lon,
                        'distance_from_home': distance_from_home,
                        'at_home': at_home,
                        'mode': 'EXPLORATION'
                    }
                    self.exploration_log.append(entry)
                    
                    # Calculate distance traveled
                    if last_pos:
                        segment = self.calculate_distance(
                            last_pos['latitude'], last_pos['longitude'],
                            lat, lon
                        )
                        self.distance_traveled += segment
                    
                    # Display
                    location = "🏠 HOME" if at_home else "🌍 EXPLORING"
                    self.log(f"{location} | {distance_from_home:.0f}m from home | Total: {self.distance_traveled:.0f}m")
                    
                    last_pos = {'latitude': lat, 'longitude': lon}
                
                time.sleep(10)
                
        except KeyboardInterrupt:
            self.log("🛑 Exploration mode stopped")
            self.save_log()
    
    def private_mode(self):
        """🏠 PRIVATE MODE - Only record inside home"""
        self.mode = "PRIVATE"
        self.log("🏠 PRIVATE MODE ACTIVATED")
        self.log("   Recording ONLY inside home radius")
        self.log(f"   Home radius: {self.home_radius}m")
        self.log("━" * 60)
        
        try:
            while True:
                if QUANTUM_AVAILABLE:
                    pos = self.gps.get_gps_position()
                else:
                    pos = {'latitude': self.home_lat, 'longitude': self.home_lon}
                
                if pos:
                    lat = pos['latitude']
                    lon = pos['longitude']
                    
                    # Only record if inside home
                    if self.is_inside_home(lat, lon):
                        entry = {
                            'timestamp': datetime.now().isoformat(),
                            'latitude': lat,
                            'longitude': lon,
                            'mode': 'PRIVATE'
                        }
                        self.exploration_log.append(entry)
                        
                        self.log("🏠 RECORDING (inside home)")
                    else:
                        self.log("⏸️  PAUSED (outside home radius)")
                
                time.sleep(10)
                
        except KeyboardInterrupt:
            self.log("🛑 Private mode stopped")
            self.save_log()
    
    def save_log(self):
        """Save tracking log"""
        log_file = Path(f"data/{self.mode.lower()}_log.json")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'mode': self.mode,
            'home_base': {
                'latitude': self.home_lat,
                'longitude': self.home_lon,
                'radius': self.home_radius
            },
            'total_distance': self.distance_traveled,
            'total_entries': len(self.exploration_log),
            'log': self.exploration_log
        }
        
        with open(log_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.log(f"💾 Saved {len(self.exploration_log)} entries")

if __name__ == "__main__":
    import sys
    
    # YOUR HOME COORDINATES
    HOME_LAT = 0.0  # Replace with your latitude
    HOME_LON = 0.0  # Replace with your longitude
    HOME_RADIUS = 100  # Replace with your radius (meters)
    
    tracker = QuantumDualModeTracker(HOME_LAT, HOME_LON, HOME_RADIUS)
    
    # Choose mode from command line
    if len(sys.argv) > 1:
        mode = sys.argv[1].upper()
        if mode == "EXPLORATION":
            tracker.exploration_mode()
        elif mode == "PRIVATE":
            tracker.private_mode()
        else:
            print("Usage: python3 quantum_dual_mode_tracker.py [EXPLORATION|PRIVATE]")
    else:
        print("🌍 EXPLORATION MODE: python3 quantum_dual_mode_tracker.py EXPLORATION")
        print("🏠 PRIVATE MODE:     python3 quantum_dual_mode_tracker.py PRIVATE")
