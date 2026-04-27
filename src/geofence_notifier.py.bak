#!/usr/bin/env python3
"""
Multi-Zone Geofence with Activity Detection & Telegram Notifications
No automatic saving - just live detection and notifications
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from collections import deque
import numpy as np
from geofence_monitor import GeofenceMonitor
from telegram_notifier import TelegramNotifier
from android_location import AndroidLocationProvider

class ActivityDetector:
    """Lightweight activity detector - NO auto-saving"""
    def __init__(self):
        self.speed_history = deque(maxlen=20)
        
        # Activity thresholds (m/s)
        self.STANDING = 0.5
        self.WALKING = 2.0
        self.RUNNING = 4.0
        self.BIKING = 8.0
        
    def detect_activity(self, speed):
        """Detect current activity based on speed"""
        self.speed_history.append(speed)
        
        if len(self.speed_history) < 5:
            return "🔄 DETECTING"
        
        avg_speed = np.mean(list(self.speed_history))
        speed_variance = np.var(list(self.speed_history))
        
        # Detect activity type
        if avg_speed < self.STANDING:
            return "🧍 STANDING"
        elif avg_speed < self.WALKING:
            if speed_variance < 0.5:
                return "🚶 WALKING"
            else:
                return "🚶‍♂️ WALKING_VARIED"
        elif avg_speed < self.RUNNING:
            return "🏃 RUNNING"
        elif avg_speed < self.BIKING:
            return "🚴 BIKING"
        else:
            return "🚗 VEHICLE"

class GeofenceNotifier:
    def __init__(self):
        self.zones = self._load_zones()
        self.telegram = TelegramNotifier()
        self.activity_detector = ActivityDetector()
        self.location_provider = AndroidLocationProvider()
        self.last_triggers = {}
        
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
    
    def check_zones(self, lat, lon):
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
                # Apply filters
                if self._is_in_quiet_hours():
                    continue
                
                if not self._is_in_active_hours(zone['active_hours']):
                    continue
                
                if not self._can_trigger(zone['name'], zone['cooldown_minutes']):
                    continue
                
                # TRIGGER!
                triggered_zones.append({
                    'name': zone['name'],
                    'emoji': zone['emoji'],
                    'type': trigger_type,
                    'distance': distance
                })
                
                self.last_triggers[zone['name']] = datetime.now()
        
        return triggered_zones
    
    def send_notification(self, zone, activity):
        """Send Telegram notification with activity"""
        message = f"""
🎬 {zone['emoji']} GEOFENCE {zone['type']}!

📍 Zone: {zone['name']}
📏 Distance: {zone['distance']:.1f}m
⏰ Time: {datetime.now().strftime('%H:%M:%S')}
🏃 Activity: {activity}

📸 Ready to record for Instagram!
"""
        self.telegram.send_message(message)
        print(f"✅ Telegram notification sent!")
    
    def run(self):
        """Main loop"""
        print("🚀 Geofence Notifier with Activity Detection!")
        print(f"📍 Monitoring {len(self.zones)} zones")
        print(f"⏰ Current time: {datetime.now().strftime('%H:%M:%S')}")
        
        for zone in self.zones:
            print(f"   {zone['emoji']} {zone['name']}: "
                  f"({zone['lat']}, {zone['lon']}) r={zone['radius']}m")
        print()
        
        iteration = 0
        
        while True:
            try:
                # Get GPS data
                location = self.location_provider.get_current_location()
                
                if not location:
                    print("⚠️  No GPS data available")
                    time.sleep(10)
                    continue
                
                lat = location['latitude']
                lon = location['longitude']
                speed = location.get('speed', 0)
                
                # Detect activity
                activity = self.activity_detector.detect_activity(speed)
                
                # Check zones
                triggered = self.check_zones(lat, lon)
                
                # Send notifications
                for zone in triggered:
                    print(f"\n🎬 {zone['emoji']} {zone['name']} {zone['type']}!")
                    self.send_notification(zone, activity)
                
                # Log every 10 iterations
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
                print("\n\n👋 Stopped!")
                print(f"⏱️  Total triggers: {len(self.last_triggers)}")
                if self.last_triggers:
                    print(f"   Zones: {', '.join(self.last_triggers.keys())}")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(10)

if __name__ == "__main__":
    notifier = GeofenceNotifier()
    notifier.run()
