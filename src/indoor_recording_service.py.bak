#!/usr/bin/env python3
"""
Indoor Home Recording Service
Periodic notifications while you're at home for parallel universe content
"""

import json
import time
import subprocess
from datetime import datetime
from pathlib import Path
from geofence_monitor import GeofenceMonitor
from android_location import AndroidLocationProvider

class IndoorRecordingService:
    def __init__(self):
        self.home_zone = self._load_home_zone()
        self.location_provider = AndroidLocationProvider()
        self.notification_interval = 30  # minutes between notifications
        self.last_notification = None
        
    def _load_home_zone(self):
        """Load HOME zone from config"""
        config_file = Path("config/zones.json")
        if not config_file.exists():
            return None
        
        config = json.loads(config_file.read_text())
        for zone in config['zones']:
            if zone['name'] == 'HOME':
                return zone
        return None
    
    def _is_in_quiet_hours(self):
        """Check quiet hours (no notifications at night)"""
        hour = datetime.now().hour
        return hour >= 22 or hour < 7
    
    def _should_notify(self):
        """Check if enough time has passed for next notification"""
        if self.last_notification is None:
            return True
        
        elapsed = (datetime.now() - self.last_notification).seconds / 60
        return elapsed >= self.notification_interval
    
    def send_recording_reminder(self):
        """Send notification to record indoor content"""
        title = "🏠 Indoor Recording Time!"
        content = "You're home - record some parallel universe content!"
        
        try:
            # Android notification with camera button
            subprocess.run([
                'termux-notification',
                '--title', title,
                '--content', content,
                '--priority', 'default',
                '--sound',
                '--button1', '📸 Open Camera',
                '--button1-action', 'termux-camera-photo -c 0',
                '--button2', '🎥 Record Video',
                '--button2-action', 'termux-camera-video -c 0'
            ])
            
            # Telegram notification
            try:
                from telegram_notifier import TelegramNotifier
                telegram = TelegramNotifier()
                telegram.send_message(
                    f"{title}\n\n{content}\n"
                    f"⏰ {datetime.now().strftime('%H:%M:%S')}\n"
                    f"📍 You're at home - perfect for indoor shots!"
                )
            except:
                pass
                
            self.last_notification = datetime.now()
            
        except Exception as e:
            print(f"Notification error: {e}")
    
    def run(self):
        """Main service loop"""
        print("🏠 Indoor Recording Service Started")
        print(f"📍 Home zone: {self.home_zone['name'] if self.home_zone else 'Not configured'}")
        print(f"⏰ Notification interval: {self.notification_interval} minutes")
        print(f"🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        if not self.home_zone:
            print("❌ HOME zone not found in config!")
            return
        
        while True:
            try:
                location = self.location_provider.get_current_location()
                
                if not location:
                    time.sleep(60)
                    continue
                
                lat = location['latitude']
                lon = location['longitude']
                
                # Check if at home
                monitor = GeofenceMonitor(
                    center=(self.home_zone['lat'], self.home_zone['lon']),
                    radius_meters=self.home_zone['radius']
                )
                
                current_pos = (lat, lon)
                at_home = monitor.is_inside_geofence(current_pos)
                distance = monitor.get_distance_from_center(current_pos)
                
                if at_home:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🏠 At home ({distance:.1f}m from center)")
                    
                    if not self._is_in_quiet_hours() and self._should_notify():
                        print("📸 Sending recording reminder...")
                        self.send_recording_reminder()
                else:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚶 Away from home ({distance:.1f}m)")
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(60)

if __name__ == "__main__":
    service = IndoorRecordingService()
    service.run()
