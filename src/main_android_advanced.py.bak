#!/usr/bin/env python3
"""
Advanced Geofencing with Multi-Zone & ML
"""

import json
import time
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from geofence_monitor import GeofenceMonitor
from route_tracker import RouteTracker
from activity_detector import ActivityDetector

class AdvancedGeofenceSystem:
    def __init__(self):
        self.zones = self._load_zones()
        self.activity_detector = ActivityDetector()
        self.route_tracker = RouteTracker()
        self.last_triggers = {}
        self.session_start = datetime.now()
        
    def _load_zones(self):
        """Load geofence zones from config"""
        config_file = Path("config/zones.json")
        if not config_file.exists():
            print("❌ zones.json not found!")
            return []
        
        config = json.loads(config_file.read_text())
        return config['zones']
    
    def _is_in_quiet_hours(self):
        """Check if current time is in quiet hours"""
        hour = datetime.now().hour
        return hour >= 22 or hour < 6
    
    def _can_trigger(self, zone_name, cooldown_minutes):
        """Check if zone can trigger (cooldown expired)"""
        
        if zone_name not in self.last_triggers:
            return True
        
        last_trigger = self.last_triggers[zone_name]
        elapsed = (datetime.now() - last_trigger).seconds / 60
        
        return elapsed >= cooldown_minutes
    
    def _is_in_active_hours(self, active_hours):
        """Check if current time is in zone's active hours"""
        hour = datetime.now().hour
        return active_hours[0] <= hour < active_hours[1]
    
    def check_zones(self, lat, lon, speed, accuracy, bearing):
        """Check all geofence zones"""
        
        current_pos = (lat, lon)
        triggered_zones = []
        
        for zone in self.zones:
            monitor = GeofenceMonitor(
                center=(zone['lat'], zone['lon']),
                radius_meters=zone['radius']
            )
            
            distance = monitor.get_distance_from_center(current_pos)
            inside = monitor.is_inside_geofence(current_pos)
            
            should_trigger = False
            trigger_type = None
            
            if inside and zone['trigger_on_enter']:
                should_trigger = True
                trigger_type = "ENTER"
            elif not inside and zone['trigger_on_exit']:
                should_trigger = True
                trigger_type = "EXIT"
            
            if should_trigger:
                if self._is_in_quiet_hours():
                    continue
                
                if not self._is_in_active_hours(zone['active_hours']):
                    continue
                
                if not self._can_trigger(zone['name'], zone['cooldown_minutes']):
                    continue
                
                will_cross, eta = self.activity_detector.predict_geofence_crossing(
                    current_pos, (zone['lat'], zone['lon']), 
                    zone['radius'], speed, bearing
                )
                
                if trigger_type == "EXIT" and will_cross:
                    print(f"🔮 Predicted crossing {zone['name']} in {eta}s")
                
                triggered_zones.append({
                    'name': zone['name'],
                    'emoji': zone['emoji'],
                    'type': trigger_type,
                    'distance': distance
                })
                
                self.last_triggers[zone['name']] = datetime.now()
        
        return triggered_zones
    
    def run(self):
        """Main loop"""
        
        print("🚀 Advanced Geofencing System Started!")
        print(f"📍 Monitoring {len(self.zones)} zones")
        print(f"⏰ Current time: {datetime.now().strftime('%H:%M:%S')}")
        
        for zone in self.zones:
            print(f"   {zone['emoji']} {zone['name']}: "
                  f"({zone['lat']}, {zone['lon']}) r={zone['radius']}m")
        print()
        
        iteration = 0
        
        while True:
            try:
                # Mock GPS data
                lat, lon = 36.007155, -88.417490
                speed = 1.5
                accuracy = 5.0
                bearing = 45
                
                activity = self.activity_detector.detect_activity(speed, accuracy)
                triggered = self.check_zones(lat, lon, speed, accuracy, bearing)
                
                for zone in triggered:
                    print(f"\n🎬 {zone['emoji']} {zone['name']} {zone['type']}!")
                    print(f"📸 Opening camera for Instagram content...")
                    print(f"📏 Distance: {zone['distance']:.1f}m")
                
                location_data = {
                    'lat': lat,
                    'lon': lon,
                    'speed': speed,
                    'accuracy': accuracy,
                    'bearing': bearing,
                    'timestamp': datetime.now().isoformat()
                }
                self.route_tracker.add_point(location_data)
                
                if iteration % 10 == 0:
                    if triggered:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                              f"{activity} | ⚡ {len(triggered)} zones triggered!")
                    else:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                              f"{activity} | Monitoring...")
                
                iteration += 1
                time.sleep(10)
                
            except KeyboardInterrupt:
                print("\n\n📊 Session Summary:")
                self._print_summary()
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                import traceback
                traceback.print_exc()
                break
    
    def _print_summary(self):
        """Print session summary"""
        
        duration = (datetime.now() - self.session_start).seconds // 60
        stats = self.activity_detector.get_activity_stats(hours=24)
        
        print(f"⏱️  Duration: {duration} minutes")
        print(f"🎯 Triggers: {len(self.last_triggers)} zones")
        if self.last_triggers:
            print(f"   Zones triggered: {', '.join(self.last_triggers.keys())}")
        print(f"📊 Activities: {stats.get('breakdown', {})}")
        
        # Fix: get_route() returns a list, not dict
        route_points = self.route_tracker.get_route()
        if route_points and len(route_points) > 0:
            # Calculate total distance from points
            total_distance = 0
            for i in range(1, len(route_points)):
                from geopy.distance import geodesic
                p1 = (route_points[i-1]['lat'], route_points[i-1]['lon'])
                p2 = (route_points[i]['lat'], route_points[i]['lon'])
                total_distance += geodesic(p1, p2).meters
            
            route_data = {
                'total_distance': total_distance,
                'duration_minutes': duration
            }
            category = self.activity_detector.categorize_session(route_data)
            print(f"🏷️  Session: {category}")
            print(f"📏 Distance: {total_distance:.1f}m")

if __name__ == "__main__":
    system = AdvancedGeofenceSystem()
    system.run()
