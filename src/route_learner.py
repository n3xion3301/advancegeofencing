import json
from pathlib import Path
from datetime import datetime, timedelta
from geopy.distance import geodesic
import numpy as np

class RouteLearner:
    def __init__(self, memory_file='routes/learned_routes.json'):
        self.memory_file = memory_file
        self.learned_zones = []  # Areas you frequently visit
        self.normal_routes = []  # Your typical paths
        self.load_memory()
    
    def load_memory(self):
        """Load learned routes from memory"""
        if Path(self.memory_file).exists():
            with open(self.memory_file, 'r') as f:
                data = json.load(f)
                self.learned_zones = data.get('zones', [])
                self.normal_routes = data.get('routes', [])
            print(f"🧠 Loaded {len(self.learned_zones)} known zones, {len(self.normal_routes)} normal routes")
        else:
            print("🧠 Starting fresh - will learn your routes")
    
    def save_memory(self):
        """Save learned routes to memory"""
        Path(self.memory_file).parent.mkdir(exist_ok=True)
        data = {
            'zones': self.learned_zones,
            'routes': self.normal_routes,
            'last_updated': datetime.now().isoformat()
        }
        with open(self.memory_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def learn_from_route(self, route_points):
        """Learn from a completed route"""
        if len(route_points) < 5:
            return  # Too short to learn from
        
        # Extract key zones (areas where you spend time)
        zones = self._extract_zones(route_points)
        
        # Add new zones or reinforce existing ones
        for zone in zones:
            self._add_or_reinforce_zone(zone)
        
        # Store route pattern
        route_signature = self._create_route_signature(route_points)
        self.normal_routes.append({
            'signature': route_signature,
            'timestamp': datetime.now().isoformat(),
            'points': len(route_points)
        })
        
        # Keep only recent routes (last 100)
        if len(self.normal_routes) > 100:
            self.normal_routes = self.normal_routes[-100:]
        
        self.save_memory()
    
    def _extract_zones(self, points):
        """Find areas where you spend time (stopped or slow movement)"""
        zones = []
        current_zone = []
        
        for i, point in enumerate(points):
            speed = point.get('speed', 0)
            
            # If moving slowly or stopped, add to current zone
            if speed < 0.5:  # Less than 0.5 m/s
                current_zone.append(point)
            else:
                # Moving - save zone if it has enough points
                if len(current_zone) >= 3:
                    # Calculate zone center
                    avg_lat = np.mean([p['lat'] for p in current_zone])
                    avg_lon = np.mean([p['lon'] for p in current_zone])
                    zones.append({
                        'center': (avg_lat, avg_lon),
                        'visits': 1,
                        'duration': len(current_zone) * 5  # Assuming 5 sec intervals
                    })
                current_zone = []
        
        return zones
    
    def _add_or_reinforce_zone(self, new_zone):
        """Add new zone or increase visit count for existing zone"""
        zone_radius = 10  # 10 meters
        
        # Check if zone already exists
        for zone in self.learned_zones:
            distance = geodesic(zone['center'], new_zone['center']).meters
            if distance < zone_radius:
                # Reinforce existing zone
                zone['visits'] += 1
                zone['last_visit'] = datetime.now().isoformat()
                return
        
        # New zone
        new_zone['first_visit'] = datetime.now().isoformat()
        new_zone['last_visit'] = datetime.now().isoformat()
        self.learned_zones.append(new_zone)
    
    def _create_route_signature(self, points):
        """Create a simplified signature of the route"""
        # Sample every Nth point to create signature
        sample_rate = max(1, len(points) // 10)
        signature = []
        
        for i in range(0, len(points), sample_rate):
            signature.append({
                'lat': round(points[i]['lat'], 5),
                'lon': round(points[i]['lon'], 5)
            })
        
        return signature
    
    def is_normal_location(self, location):
        """Check if location is in a known zone"""
        for zone in self.learned_zones:
            distance = geodesic(zone['center'], location).meters
            if distance < 15:  # Within 15m of known zone
                return True, zone
        return False, None
    
    def is_similar_route(self, current_points):
        """Check if current route matches a known pattern"""
        if len(current_points) < 5:
            return False
        
        current_sig = self._create_route_signature(current_points)
        
        for known_route in self.normal_routes:
            similarity = self._calculate_route_similarity(current_sig, known_route['signature'])
            if similarity > 0.7:  # 70% similar
                return True
        
        return False
    
    def _calculate_route_similarity(self, sig1, sig2):
        """Calculate how similar two route signatures are"""
        if not sig1 or not sig2:
            return 0
        
        # Simple similarity: how many points are close to each other
        matches = 0
        total = min(len(sig1), len(sig2))
        
        for p1 in sig1[:total]:
            for p2 in sig2[:total]:
                dist = geodesic((p1['lat'], p1['lon']), (p2['lat'], p2['lon'])).meters
                if dist < 20:  # Within 20m
                    matches += 1
                    break
        
        return matches / total if total > 0 else 0
    
    def get_zone_summary(self):
        """Get summary of learned zones"""
        if not self.learned_zones:
            return "No zones learned yet"
        
        # Sort by visit count
        sorted_zones = sorted(self.learned_zones, key=lambda z: z['visits'], reverse=True)
        
        summary = f"🧠 Known Zones ({len(self.learned_zones)}):\n"
        for i, zone in enumerate(sorted_zones[:5], 1):
            summary += f"  {i}. Visited {zone['visits']}x - {zone['center']}\n"
        
        return summary
