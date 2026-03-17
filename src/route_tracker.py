from datetime import datetime
from pathlib import Path
import json

class RouteTracker:
    def __init__(self, max_points=1000):
        self.route = []
        self.max_points = max_points
        self.start_time = None
        
    def add_point(self, location_data):
        """Add GPS point to route"""
        if not self.start_time:
            self.start_time = datetime.now()
        
        point = {
            'timestamp': datetime.now().isoformat(),
            'lat': location_data['latitude'],
            'lon': location_data['longitude'],
            'accuracy': location_data.get('accuracy', 0),
            'speed': location_data.get('speed', 0),
            'altitude': location_data.get('altitude', 0)
        }
        
        self.route.append(point)
        
        # Keep only last N points in memory
        if len(self.route) > self.max_points:
            self.route.pop(0)
    
    def get_route(self):
        """Get current route"""
        return self.route
    
    def get_stats(self):
        """Get route statistics"""
        if not self.route:
            return None
        
        total_distance = 0
        for i in range(1, len(self.route)):
            from geopy.distance import geodesic
            p1 = (self.route[i-1]['lat'], self.route[i-1]['lon'])
            p2 = (self.route[i]['lat'], self.route[i]['lon'])
            total_distance += geodesic(p1, p2).meters
        
        duration = (datetime.now() - self.start_time).total_seconds()
        
        return {
            'points': len(self.route),
            'distance_meters': round(total_distance, 1),
            'duration_seconds': round(duration),
            'avg_speed_mps': round(total_distance / duration, 2) if duration > 0 else 0
        }
    
    def save_route(self, filename=None):
        """Save route to file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'routes/route_{timestamp}.json'
        
        Path('routes').mkdir(exist_ok=True)
        
        data = {
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'points': self.route,
            'stats': self.get_stats()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filename
    
    def export_gpx(self, filename=None):
        """Export route as GPX file for mapping apps"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'routes/route_{timestamp}.gpx'
        
        Path('routes').mkdir(exist_ok=True)
        
        gpx = f'''<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="GeofenceSystem">
  <trk>
    <name>Route {self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else 'Unknown'}</name>
    <trkseg>
'''
        
        for point in self.route:
            gpx += f'''      <trkpt lat="{point['lat']}" lon="{point['lon']}">
        <ele>{point['altitude']}</ele>
        <time>{point['timestamp']}</time>
      </trkpt>
'''
        
        gpx += '''    </trkseg>
  </trk>
</gpx>'''
        
        with open(filename, 'w') as f:
            f.write(gpx)
        
        return filename
    
    def clear_route(self):
        """Clear current route"""
        self.route = []
        self.start_time = None
