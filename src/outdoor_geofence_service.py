#!/usr/bin/env python3
"""
Outdoor Geofence Service
Monitors outdoor zones (parks, playgrounds, etc.) and notifies on crossing
"""

import json
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from geofence_monitor import GeofenceMonitor
from android_location import AndroidLocationProvider

class OutdoorGeofenceService:
    def __init__(self):
        self.zones = self._load_outdoor_zones()
        self.location_provider = AndroidLocationProvider()
        self.last_triggers = {}
        
    def _load_outdoor_zones(self):
        """Load outdoor zones (exclude HOME)"""
        config_file = Path("config/zones.json")
        if not config_file.exists():
            return []
        
        config = json.loads(config_file.read_text())
        # Filter out HOME zone
        return [z for z in config['zones'] if z['name'] != 'HOME']
    
    def _is_in_quiet_hours(self):
        """Check quiet hours"""
        hour = datetime.now().hour
        return hour >= 22 or hour < 6
    
    def _can_trigger(self, zone_name, cooldown_minutes):
        """Check cooldown"""
        if zone_name not in self.last_triggers:
            return True
        
        last_trigger = self.last_triggers[zone_name]
        elapsed = (datetime.now() - last_trigger).seconds / 60
        return elapsed >= cooldown_minutes
    
    def _is_in_active_hours(self, active_hours):
        """Check active hours"""
        hour = datetime.now().hour
        return active_hours[0] <= hour < active_hours[1]
    
    def send_zone_notification(self, zone, trigger_type, distance):
        """Send notification for outdoor zone crossing"""
        title = f"{zone['emoji']} {zone['name']} {trigger_type}!"
        content = f"Distance: {distance:.1f}m - Record outdoor content!"
        
        try:
            subprocess.run([
                'termux-notification',
                '--title', title,
                '--content', content,
                '--priority', 'high',
                '--sound',
                '--vibrate', '200,100,200',
                '--button1', '📸 Open Camera',
                '--button1-action', 'termux-camera-photo -c 0',
                '--button2', '🎥 Record Video',
                '--button2-action', 'termux-camera-video -c 0'
            ])
            
            # Telegram
            try:
                from telegram_notifier import TelegramNotifier
                telegram = TelegramNotifier()
                telegram.send_message(
                    f"🎬 {title}\n\n"
                    f"📍 Zone: {zone['name']}\n"
                    f"📏 Distance: {distance:.1f}m\n"
                    f"⏰ {datetime.now().strftime('%H:%M:%S')}\n\n"
                    f"📸 Perfect spot for outdoor recording!"
                )
            except:
                pass
                
        except Exception as e:
            print(f"Notification error: {e}")
    
    def check_zones(self, lat, lon):
        """Check outdoor zones"""
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
                
                triggered_zones.append({
                    'zone': zone,
                    'type': trigger_type,
                    'distance': distance
                })
                
                self.last_triggers[zone['name']] = datetime.now()
        
        return triggered_zones
    
    def run(self):
        """Main service loop"""
        print("🌳 Outdoor Geofence Service Started")
        print(f"📍 Monitoring {len(self.zones)} outdoor zones")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        for zone in self.zones:
            print(f"   {zone['emoji']} {zone['name']}: ({zone['lat']}, {zone['lon']}) r={zone['radius']}m")
        print()
        
        while True:
            try:
                location = self.location_provider.get_current_location()
                
                if not location:
                    time.sleep(30)
                    continue
                
                lat = location['latitude']
                lon = location['longitude']
                
                triggered = self.check_zones(lat, lon)
                
                for item in triggered:
                    zone = item['zone']
                    print(f"🚨 {zone['emoji']} {zone['name']} {item['type']} ({item['distance']:.1f}m)")
                    self.send_zone_notification(zone, item['type'], item['distance'])
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(30)

if __name__ == "__main__":
    service = OutdoorGeofenceService()
    service.run()
