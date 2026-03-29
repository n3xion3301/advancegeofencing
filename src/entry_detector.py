#!/usr/bin/env python3
"""
Directional Entry Detector
Detects when entities cross from outside to inside through entry points
"""

import json
import time
import subprocess
from datetime import datetime
from pathlib import Path
from geofence_monitor import GeofenceMonitor
from android_location import AndroidLocationProvider

class EntryDetector:
    def __init__(self):
        self.entry_points = self._load_entry_points()
        self.location_provider = AndroidLocationProvider()
        self.position_history = []
        self.max_history = 10  # More history for better detection
        self.min_distance_outside = 1.0  # 1 meter minimum
        
    def _load_entry_points(self):
        """Load entry point zones"""
        config_file = Path("config/entity_zones.json")
        if not config_file.exists():
            return []
        
        config = json.loads(config_file.read_text())
        return [z for z in config['entity_zones'] 
                if 'DOOR' in z['name']]
    
    def detect_crossing_direction(self, zone, current_pos):
        """Detect if crossing from outside to inside"""
        if len(self.position_history) < 3:
            return None
        
        monitor = GeofenceMonitor(
            center=(zone['lat'], zone['lon']),
            radius_meters=zone['radius']
        )
        
        # Current position
        currently_inside = monitor.is_inside_geofence(current_pos)
        current_distance = monitor.get_distance_from_center(current_pos)
        
        # Previous position (3 readings ago for stability)
        prev_pos = self.position_history[-3]
        was_outside = not monitor.is_inside_geofence(prev_pos)
        prev_distance = monitor.get_distance_from_center(prev_pos)
        
        # Must have been at least 1m away
        if was_outside and prev_distance >= self.min_distance_outside:
            if currently_inside:
                return "ENTERING"
        
        # Exiting detection
        if not was_outside and not currently_inside:
            if current_distance >= self.min_distance_outside:
                return "EXITING"
        
        return None
    
    def send_entry_alert(self, zone, direction, distance):
        """Send alert when entity crosses threshold"""
        if direction == "ENTERING":
            title = f"🚨 {zone['emoji']} ENTITY ENTERING!"
            content = f"{zone['entity']} crossing {zone['name']} - Coming INSIDE! ({distance:.1f}m)"
            priority = "max"
            vibrate = "500,200,500,200,500"
        else:
            title = f"👋 {zone['emoji']} ENTITY LEAVING"
            content = f"{zone['entity']} crossing {zone['name']} - Going OUTSIDE ({distance:.1f}m)"
            priority = "high"
            vibrate = "200,100,200"
        
        try:
            subprocess.run([
                'termux-notification',
                '--title', title,
                '--content', content,
                '--priority', priority,
                '--sound',
                '--vibrate', vibrate,
                '--button1', '📸 Record',
                '--button1-action', 'termux-camera-photo -c 0'
            ])
            
            try:
                from telegram_notifier import TelegramNotifier
                telegram = TelegramNotifier()
                telegram.send_message(
                    f"{title}\n\n"
                    f"📍 {zone['name']}\n"
                    f"👻 {zone['entity']}\n"
                    f"🚪 Direction: {direction}\n"
                    f"📏 Distance: {distance:.1f}m\n"
                    f"⏰ {datetime.now().strftime('%H:%M:%S')}"
                )
            except:
                pass
        except Exception as e:
            print(f"Alert error: {e}")
    
    def run(self):
        """Main detection loop"""
        print("🚨 Directional Entry Detector Started")
        print(f"🚪 Monitoring {len(self.entry_points)} entry points")
        print(f"📏 Minimum distance: {self.min_distance_outside}m")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        for entry in self.entry_points:
            print(f"   {entry['emoji']} {entry['name']}: {entry['entity']}")
            print(f"      Location: ({entry['lat']}, {entry['lon']}) r={entry['radius']}m")
        print()
        
        while True:
            try:
                location = self.location_provider.get_current_location()
                
                if not location:
                    time.sleep(3)
                    continue
                
                lat = location['latitude']
                lon = location['longitude']
                current_pos = (lat, lon)
                
                # Add to history
                self.position_history.append(current_pos)
                if len(self.position_history) > self.max_history:
                    self.position_history.pop(0)
                
                # Check each entry point
                for entry in self.entry_points:
                    monitor = GeofenceMonitor(
                        center=(entry['lat'], entry['lon']),
                        radius_meters=entry['radius']
                    )
                    distance = monitor.get_distance_from_center(current_pos)
                    inside = monitor.is_inside_geofence(current_pos)
                    
                    # Show current status
                    status = "INSIDE" if inside else "OUTSIDE"
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    print(f"[{timestamp}] {entry['emoji']} {entry['name']}: {status} ({distance:.1f}m)")
                    
                    # Check for crossing
                    direction = self.detect_crossing_direction(entry, current_pos)
                    
                    if direction:
                        print(f"🚨 CROSSING DETECTED: {direction}")
                        if direction == "ENTERING":
                            self.send_entry_alert(entry, direction, distance)
                
                time.sleep(3)  # Check every 3 seconds
                
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(3)

if __name__ == "__main__":
    detector = EntryDetector()
    detector.run()
