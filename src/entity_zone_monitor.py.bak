#!/usr/bin/env python3
"""
Entity Zone Monitor
Monitors specific indoor locations where parallel universe entities appear
Sends notifications when you're near these creative hotspots
"""

import json
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from geofence_monitor import GeofenceMonitor
from android_location import AndroidLocationProvider

class EntityZoneMonitor:
    def __init__(self):
        self.entity_zones = self._load_entity_zones()
        self.location_provider = AndroidLocationProvider()
        self.current_zone = None
        self.zone_entry_time = None
        self.last_notifications = {}
        self.notification_interval = 5  # Notify every 5 minutes while in zone
        
    def _load_entity_zones(self):
        """Load entity zones from config"""
        config_file = Path("config/entity_zones.json")
        if not config_file.exists():
            # Create default entity zones
            default_zones = {
                "entity_zones": [
                    {
                        "name": "FRONT_DOOR",
                        "emoji": "🚪",
                        "entity": "The Doorway Guardian",
                        "description": "Portal between worlds",
                        "lat": 0,
                        "lon": 0,
                        "radius": 5,
                        "active_hours": [6, 22]
                    }
                ]
            }
            config_file.write_text(json.dumps(default_zones, indent=2))
            print(f"⚠️  Created default entity_zones.json - please configure!")
            return default_zones['entity_zones']
        
        config = json.loads(config_file.read_text())
        return config['entity_zones']
    
    def _is_in_quiet_hours(self):
        """Check quiet hours"""
        hour = datetime.now().hour
        return hour >= 22 or hour < 6
    
    def _should_notify(self, zone_name):
        """Check if should send notification"""
        if zone_name not in self.last_notifications:
            return True
        
        elapsed = (datetime.now() - self.last_notifications[zone_name]).seconds / 60
        return elapsed >= self.notification_interval
    
    def send_entity_notification(self, zone, distance, duration_minutes=0):
        """Send notification about entity zone"""
        if duration_minutes > 0:
            title = f"✨ {zone['emoji']} ENTITY ACTIVE!"
            content = f"{zone['entity']} present for {duration_minutes} min - RECORD NOW!"
        else:
            title = f"✨ {zone['emoji']} ENTITY DETECTED!"
            content = f"{zone['entity']} - {zone['description']}"
        
        try:
            # High priority notification with camera buttons
            subprocess.run([
                'termux-notification',
                '--id', f'entity_{zone["name"]}',
                '--title', title,
                '--content', content,
                '--priority', 'max',
                '--sound',
                '--vibrate', '300,200,300,200,300',
                '--ongoing',  # Persistent notification
                '--button1', '📸 Photo',
                '--button1-action', 'termux-camera-photo -c 0',
                '--button2', '🎥 Video',
                '--button2-action', 'termux-camera-video -c 0',
                '--button3', '❌ Dismiss',
                '--button3-action', f'termux-notification-remove entity_{zone["name"]}'
            ])
            
            # Telegram with entity info
            try:
                from telegram_notifier import TelegramNotifier
                telegram = TelegramNotifier()
                
                msg = f"✨ **ENTITY ZONE ACTIVE** ✨\n\n"
                msg += f"{zone['emoji']} **{zone['name']}**\n"
                msg += f"👻 Entity: *{zone['entity']}*\n"
                msg += f"📝 {zone['description']}\n"
                msg += f"📏 Distance: {distance:.1f}m\n"
                
                if duration_minutes > 0:
                    msg += f"⏱️ Duration: {duration_minutes} minutes\n"
                
                msg += f"⏰ {datetime.now().strftime('%H:%M:%S')}\n\n"
                msg += f"🎬 **RECORD YOUR PARALLEL UNIVERSE CONTENT NOW!**"
                
                telegram.send_message(msg)
            except:
                pass
            
            self.last_notifications[zone['name']] = datetime.now()
            
        except Exception as e:
            print(f"Notification error: {e}")
    
    def clear_entity_notification(self, zone):
        """Clear persistent notification when leaving zone"""
        try:
            subprocess.run([
                'termux-notification-remove',
                f'entity_{zone["name"]}'
            ])
        except:
            pass
    
    def check_entity_zones(self, lat, lon):
        """Check if near any entity zones"""
        current_pos = (lat, lon)
        active_zone = None
        
        for zone in self.entity_zones:
            monitor = GeofenceMonitor(
                center=(zone['lat'], zone['lon']),
                radius_meters=zone['radius']
            )
            
            distance = monitor.get_distance_from_center(current_pos)
            inside = monitor.is_inside_geofence(current_pos)
            
            # Check active hours
            hour = datetime.now().hour
            if not (zone['active_hours'][0] <= hour < zone['active_hours'][1]):
                continue
            
            if inside:
                active_zone = zone
                
                # Entering new zone
                if self.current_zone != zone['name']:
                    print(f"\n✨ ENTERED ENTITY ZONE: {zone['emoji']} {zone['name']}")
                    print(f"   Entity: {zone['entity']}")
                    print(f"   Distance: {distance:.1f}m")
                    
                    self.current_zone = zone['name']
                    self.zone_entry_time = datetime.now()
                    
                    if not self._is_in_quiet_hours():
                        self.send_entity_notification(zone, distance)
                
                # Still in zone - periodic reminders
                elif self.zone_entry_time:
                    duration = (datetime.now() - self.zone_entry_time).seconds / 60
                    
                    if duration >= 1 and self._should_notify(zone['name']):
                        print(f"⏱️  In {zone['name']} for {int(duration)} minutes")
                        if not self._is_in_quiet_hours():
                            self.send_entity_notification(zone, distance, int(duration))
                
                break
        
        # Left all zones
        if active_zone is None and self.current_zone is not None:
            print(f"\n🚶 LEFT ENTITY ZONE: {self.current_zone}")
            
            # Clear notification
            for zone in self.entity_zones:
                if zone['name'] == self.current_zone:
                    self.clear_entity_notification(zone)
                    break
            
            self.current_zone = None
            self.zone_entry_time = None
    
    def run(self):
        """Main monitoring loop"""
        print("✨ Entity Zone Monitor Started")
        print(f"👻 Monitoring {len(self.entity_zones)} entity zones")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        for zone in self.entity_zones:
            print(f"   {zone['emoji']} {zone['name']}: {zone['entity']}")
            print(f"      Location: ({zone['lat']}, {zone['lon']}) r={zone['radius']}m")
        print()
        
        while True:
            try:
                location = self.location_provider.get_current_location()
                
                if not location:
                    time.sleep(10)
                    continue
                
                lat = location['latitude']
                lon = location['longitude']
                
                self.check_entity_zones(lat, lon)
                
                time.sleep(10)  # Check every 10 seconds for precise detection
                
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(10)

if __name__ == "__main__":
    monitor = EntityZoneMonitor()
    monitor.run()
