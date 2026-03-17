import json
import time
from geopy.distance import geodesic
from shapely.geometry import Point, Polygon

class GeofenceMonitor:
    def __init__(self, config_path='config/geofence_config.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.center = (
            self.config['residence']['center']['latitude'],
            self.config['residence']['center']['longitude']
        )
        self.radius = self.config['residence']['radius_meters']
        self.last_breach_time = 0
        self.cooldown = self.config['monitoring']['breach_cooldown_seconds']
        
    def is_inside_geofence(self, current_location):
        """Check if location is within circular geofence"""
        distance = geodesic(self.center, current_location).meters
        return distance <= self.radius
    
    def is_inside_polygon(self, current_location):
        """Check if location is within polygon geofence"""
        coords = self.config['residence'].get('polygon_coordinates', [])
        if not coords:
            return None
        
        polygon = Polygon(coords)
        point = Point(current_location[1], current_location[0])
        return polygon.contains(point)
    
    def check_breach(self, current_location, previous_location):
        """Detect if boundary has been crossed"""
        current_time = time.time()
        
        # Cooldown check
        if current_time - self.last_breach_time < self.cooldown:
            return False
        
        was_inside = self.is_inside_geofence(previous_location)
        is_inside = self.is_inside_geofence(current_location)
        
        # Breach detected: transition from outside to inside
        if not was_inside and is_inside:
            self.last_breach_time = current_time
            return True
        
        return False

