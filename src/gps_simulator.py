#!/usr/bin/env python3
"""
GPS Simulator for Testing
Generates realistic GPS data without requiring actual GPS signal
"""
import json
import random
import time
from datetime import datetime
from pathlib import Path
import math

class GPSSimulator:
    def __init__(self, start_lat=40.7128, start_lon=-74.0060):
        self.current_lat = start_lat
        self.current_lon = start_lon
        self.speed = 0.0  # m/s
        self.heading = 0.0  # degrees
        self.altitude = 10.0
        self.accuracy = 5.0
        
        # Movement patterns
        self.patterns = ['stationary', 'walking', 'driving', 'random']
        self.current_pattern = 'walking'
        
        print(f"🎮 GPS Simulator Initialized at {start_lat:.6f}, {start_lon:.6f}")
    
    def set_pattern(self, pattern):
        """Set movement pattern"""
        if pattern in self.patterns:
            self.current_pattern = pattern
            print(f"📍 Pattern set to: {pattern}")
    
    def get_simulated_location(self):
        """Generate simulated GPS location"""
        
        # Update position based on pattern
        if self.current_pattern == 'stationary':
            # Small random drift
            self.current_lat += random.uniform(-0.00001, 0.00001)
            self.current_lon += random.uniform(-0.00001, 0.00001)
            self.speed = 0.0
            self.accuracy = random.uniform(3.0, 8.0)
        
        elif self.current_pattern == 'walking':
            # Walking speed: 1-2 m/s
            self.speed = random.uniform(1.0, 2.0)
            self.heading += random.uniform(-15, 15)
            
            # Move in current heading
            distance = self.speed * 1.0  # 1 second
            dlat = (distance * math.cos(math.radians(self.heading))) / 111320
            dlon = (distance * math.sin(math.radians(self.heading))) / (111320 * math.cos(math.radians(self.current_lat)))
            
            self.current_lat += dlat
            self.current_lon += dlon
            self.accuracy = random.uniform(5.0, 15.0)
        
        elif self.current_pattern == 'driving':
            # Driving speed: 5-15 m/s
            self.speed = random.uniform(5.0, 15.0)
            self.heading += random.uniform(-5, 5)
            
            distance = self.speed * 1.0
            dlat = (distance * math.cos(math.radians(self.heading))) / 111320
            dlon = (distance * math.sin(math.radians(self.heading))) / (111320 * math.cos(math.radians(self.current_lat)))
            
            self.current_lat += dlat
            self.current_lon += dlon
            self.accuracy = random.uniform(8.0, 20.0)
        
        elif self.current_pattern == 'random':
            # Random movement
            self.current_lat += random.uniform(-0.0001, 0.0001)
            self.current_lon += random.uniform(-0.0001, 0.0001)
            self.speed = random.uniform(0, 3.0)
            self.accuracy = random.uniform(5.0, 25.0)
        
        # Altitude variation
        self.altitude += random.uniform(-2.0, 2.0)
        self.altitude = max(0, min(100, self.altitude))
        
        return {
            'lat': self.current_lat,
            'lon': self.current_lon,
            'accuracy': self.accuracy,
            'altitude': self.altitude,
            'speed': self.speed,
            'bearing': self.heading,
            'timestamp': datetime.now().isoformat(),
            'simulated': True
        }
    
    def simulate_route(self, waypoints, steps_per_waypoint=10):
        """Simulate movement through waypoints"""
        route = []
        
        for i in range(len(waypoints) - 1):
            start = waypoints[i]
            end = waypoints[i + 1]
            
            for step in range(steps_per_waypoint):
                progress = step / steps_per_waypoint
                
                lat = start['lat'] + (end['lat'] - start['lat']) * progress
                lon = start['lon'] + (end['lon'] - start['lon']) * progress
                
                self.current_lat = lat
                self.current_lon = lon
                
                location = self.get_simulated_location()
                route.append(location)
        
        return route

# Integrate with existing GPS service
class GPSLocationServiceSimulated:
    def __init__(self, use_simulator=True):
        self.location_history = []
        self.cache_file = Path("~/advancegeofencing/location_cache.json").expanduser()
        self.use_simulator = use_simulator
        
        if use_simulator:
            self.simulator = GPSSimulator()
            print("📍 GPS Location Service (SIMULATED MODE)")
        else:
            print("📍 GPS Location Service (REAL GPS)")
    
    def get_current_location(self):
        """Get location - simulated or real"""
        if self.use_simulator:
            return self.simulator.get_simulated_location()
        else:
            # Original GPS code
            import subprocess
            try:
                result = subprocess.run(
                    ['termux-location', '-p', 'gps'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    location = json.loads(result.stdout)
                    return {
                        'lat': location['latitude'],
                        'lon': location['longitude'],
                        'accuracy': location.get('accuracy', 0),
                        'altitude': location.get('altitude', 0),
                        'speed': location.get('speed', 0),
                        'timestamp': datetime.now().isoformat(),
                        'simulated': False
                    }
            except Exception as e:
                print(f"⚠️  GPS error: {e}")
                print("🎮 Falling back to simulator...")
                self.use_simulator = True
                self.simulator = GPSSimulator()
                return self.simulator.get_simulated_location()
    
    def set_pattern(self, pattern):
        """Set simulator movement pattern"""
        if self.use_simulator:
            self.simulator.set_pattern(pattern)
    
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
        """Calculate distance between two points"""
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371000
        lat1_rad = radians(lat1)
        lat2_rad = radians(lat2)
        delta_lat = radians(lat2 - lat1)
        delta_lon = radians(lon2 - lon1)
        
        a = sin(delta_lat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c
    
    def is_inside_zone(self, current_location, zone_center, radius_meters):
        """Check if inside zone"""
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
        """Calculate movement vector"""
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
    print("🎮 GPS Simulator Test\n")
    
    sim = GPSSimulator(40.7128, -74.0060)
    
    print("Testing movement patterns:\n")
    
    patterns = ['stationary', 'walking', 'driving']
    
    for pattern in patterns:
        print(f"📍 Pattern: {pattern}")
        sim.set_pattern(pattern)
        
        for i in range(3):
            loc = sim.get_simulated_location()
            print(f"   {i+1}. {loc['lat']:.6f}, {loc['lon']:.6f} - Speed: {loc['speed']:.1f} m/s")
            time.sleep(0.5)
        print()
    
    print("✅ Simulator test complete!")
