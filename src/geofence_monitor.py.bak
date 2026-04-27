from geopy.distance import geodesic
import time

class GeofenceMonitor:
    def __init__(self, center=(36.007085, -88.417576), radius_meters=50):
        self.center = center
        self.radius = radius_meters
        self.last_breach_time = 0
        self.cooldown = 10  # 10 seconds between breach alerts
        self.min_movement_meters = 15  # Must move at least 15m to trigger
    
    def get_distance_from_center(self, location):
        """Calculate distance from center point"""
        return geodesic(self.center, location).meters
    
    def is_inside_geofence(self, location):
        """Check if location is inside geofence"""
        distance = self.get_distance_from_center(location)
        return distance <= self.radius
    
    def check_breach(self, current_location, previous_location):
        """Detect if boundary has been crossed in EITHER direction"""
        current_time = time.time()
        
        # Cooldown check
        if current_time - self.last_breach_time < self.cooldown:
            return False
        
        # Check how far you actually moved
        movement = geodesic(previous_location, current_location).meters
        if movement < self.min_movement_meters:
            return False  # Ignore small GPS drift
        
        was_inside = self.is_inside_geofence(previous_location)
        is_inside = self.is_inside_geofence(current_location)
        
        # Breach detected: ANY transition across boundary
        if was_inside != is_inside:
            self.last_breach_time = current_time
            return True
        
        return False
