#!/usr/bin/env python3
"""
Background Geofence Monitor Service
AUTO-OPENS CAMERA when geofence is breached!
NOW TRIGGERS ON INITIAL POSITION TOO!
"""

import json
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from geofence_monitor import GeofenceMonitor
from android_location import AndroidLocationProvider

class BackgroundGeofenceService:
    def __init__(self):
        self.zones = self._load_zones()
        self.location_provider = AndroidLocationProvider()
        self.last_triggers = {}
        self.initial_check_done = False  # NEW: Track initial check
        self.zone_states = {}  # NEW: Track if inside/outside each zone

    def _load_zones(self):
        """Load geofence zones"""
        config_file = Path("config/zones.json")
        if not config_file.exists():
            return []
        config = json.loads(config_file.read_text())
        return config['zones']

    def _is_in_quiet_hours(self):
        """Check quiet hours"""
        hour = datetime.now().hour
        return False  # Quiet hours disabled

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

    def open_camera_app(self):
        """Open the camera app for manual recording"""
        try:
            print(f"📸 Opening camera app...")
            subprocess.run(['am', 'start', '-a', 'android.media.action.IMAGE_CAPTURE'])
            return True
        except Exception as e:
            print(f"❌ Failed to open camera: {e}")
            return False

    def send_android_notification(self, zone, trigger_type):
        """Send Android notification"""
        title = f"{zone['emoji']} GEOFENCE {trigger_type}!"
        content = f"Zone: {zone['name']} - Camera opened! Start recording!"

        try:
            cmd = [
                'termux-notification',
                '--title', title,
                '--content', content,
                '--priority', 'max',
                '--sound',
                '--vibrate', '500,200,500',
                '--button1', '📹 Open Camera Again',
                '--button1-action', 'am start -n app.media.action.IMAGE_CAPTURE',
                '--button2', '📸 Quick Photo',
                '--button2-action', 'termux-camera-photo -c 0'
            ]
            
            subprocess.run(cmd)

            # Telegram notification
            try:
                from telegram_notifier import TelegramNotifier
                telegram = TelegramNotifier()
                
                msg = (
                    f"🚨 {title}\n\n"
                    f"📍 Zone: {zone['name']}\n"
                    f"⏰ {datetime.now().strftime('%H:%M:%S')}\n"
                    f"📸 Camera app opened automatically!\n"
                    f"🎥 Start recording manually!"
                )
                
                telegram.send_message(msg)
                    
            except Exception as e:
                print(f"Telegram error: {e}")

        except Exception as e:
            print(f"Notification error: {e}")

    def check_zones(self, lat, lon):
        """Check all zones for breaches"""
        current_pos = (lat, lon)
        triggered_zones = []

        for zone in self.zones:
            monitor = GeofenceMonitor(
                center=(zone['lat'], zone['lon']),
                radius_meters=zone['radius']
            )

            distance = monitor.get_distance_from_center(current_pos)
            inside = monitor.is_inside_geofence(current_pos)
            zone_name = zone['name']

            # Initialize zone state if first time
            if zone_name not in self.zone_states:
                self.zone_states[zone_name] = inside

            should_trigger = False
            trigger_type = None

            # NEW: On initial check, trigger if already inside
            if not self.initial_check_done and inside and zone['trigger_on_enter']:
                should_trigger = True
                trigger_type = "INSIDE"
                print(f"🎯 Initial check: Already inside {zone_name}!")

            # Normal boundary crossing detection
            elif self.zone_states[zone_name] != inside:
                if inside and zone['trigger_on_enter']:
                    should_trigger = True
                    trigger_type = "ENTER"
                elif not inside and zone['trigger_on_exit']:
                    should_trigger = True
                    trigger_type = "EXIT"
                
                # Update state
                self.zone_states[zone_name] = inside

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
        print("🚀 Background Geofence Service Started (AUTO-OPEN CAMERA MODE)")
        print(f"📍 Monitoring {len(self.zones)} zones")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📸 Camera app will open automatically on breach!")
        print(f"🎯 Will trigger on initial position if already inside!")
        print()

        for zone in self.zones:
            print(f"   {zone['emoji']} {zone['name']}: ({zone['lat']}, {zone['lon']}) r={zone['radius']}m")
        print()

        while True:
            try:
                location = self.location_provider.get_current_location()

                if not location:
                    time.sleep(5)
                    continue

                lat = location['latitude']
                lon = location['longitude']

                triggered = self.check_zones(lat, lon)

                # Mark initial check as done after first location check
                if not self.initial_check_done:
                    self.initial_check_done = True

                for item in triggered:
                    zone = item['zone']
                    trigger_type = item['type']
                    
                    print(f"🚨 {zone['emoji']} {zone['name']} {trigger_type} ({item['distance']:.1f}m)")
                    
                    # AUTO-OPEN CAMERA APP!
                    self.open_camera_app()
                    
                    # Send notification
                    self.send_android_notification(zone, trigger_type)

                time.sleep(5)  # Check every 5 seconds

            except KeyboardInterrupt:
                print("\n👋 Service stopped")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    service = BackgroundGeofenceService()
    service.run()
