#!/usr/bin/env python3
import subprocess
import json
import time
from datetime import datetime
from geopy.distance import geodesic
import os
import sys

# Add quantum visualizer
from quantum_visualizer import QuantumVisualizer

class WiFiEntityDetector:
    def __init__(self, zones, scan_interval=5, detection_range=60, filter_networks=None):
        self.zones = zones
        self.scan_interval = scan_interval
        self.detection_range = detection_range
        self.filter_networks = filter_networks or []
        self.baseline_networks = set()
        self.detected_entities = {}
        self.location_provider = AndroidLocationProvider()
        
        # Initialize quantum visualizer
        self.quantum_viz = QuantumVisualizer()
        
        print(f"👻 WiFi Entity Detector (Filtered)")
        print(f"🚪 Monitoring {len(zones)} zones")
        print(f"📡 Scan: {scan_interval}s")
        print(f"📏 Range: {detection_range}m")
        print(f"🚫 Filtering {len(self.filter_networks)} of your networks")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        for zone_name, zone_data in zones.items():
            print(f"   🚪 {zone_name}: {zone_data['name']}")

    def get_wifi_networks(self):
        """Scan for WiFi networks using Termux API"""
        try:
            result = subprocess.run(
                ['termux-wifi-scaninfo'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                networks = json.loads(result.stdout)
                return networks
        except Exception as e:
            print(f"❌ WiFi scan error: {e}")
        return []

    def is_near_zone(self, zone_name):
        """Check if current location is near a zone"""
        location = self.location_provider.get_current_location()

        if not location:
            return False, None

        current_pos = (location['latitude'], location['longitude'])
        zone_pos = (self.zones[zone_name]['lat'], self.zones[zone_name]['lon'])
        distance = geodesic(current_pos, zone_pos).meters

        return distance <= self.detection_range, distance

    def send_notification(self, zone_name, network, distance):
        """Send Android notification"""
        try:
            zone = self.zones[zone_name]
            message = f"👻 {zone['name']}\n📡 {network.get('ssid', 'Hidden Network')}\n📏 {distance:.1f}m"

            subprocess.run([
                'termux-notification',
                '--title', f'🚨 ENTITY AT {zone_name}!',
                '--content', message,
                '--priority', 'high',
                '--sound',
                '--vibrate', '200,100,200',
                '--action', 'termux-camera-photo ~/entity_photo.jpg'
            ])
        except Exception as e:
            print(f"❌ Notification error: {e}")

    def send_telegram_alert(self, zone_name, network, distance):
        """Send Telegram alert with quantum data"""
        try:
            from telegram_notifier import TelegramNotifier
            telegram = TelegramNotifier()

            zone = self.zones[zone_name]
            timestamp = datetime.now().strftime('%H:%M:%S')

            message = f"""🚨 ENTITY AT {zone_name}!

👻 {zone['name']}
📡 WiFi: {network.get('ssid', '')}
🔍 BSSID: {network.get('bssid', 'N/A')}
📶 {network.get('level', 0)} dBm
📏 {distance:.1f}m from door
⏰ {timestamp}"""

            result = telegram.send_message(message, parse_mode=None)
            
            if result:
                print("                    ✅ Telegram sent!")
            else:
                print("                    ⚠️  Telegram failed")
                
        except Exception as e:
            print(f"                    ❌ Telegram error: {e}")

    def visualize_breach(self, zone_name, network, distance):
        """Generate quantum visualization for breach"""
        try:
            zone = self.zones[zone_name]
            entity_data = {
                'name': network.get('ssid', 'Hidden Entity'),
                'bssid': network.get('bssid', 'N/A'),
                'distance': distance,
                'zone': zone['name'],
                'signal': network.get('level', 0)
            }
            
            # Show dimensional rift
            self.quantum_viz.dimensional_rift(entity_data)
            
            # Save breach log
            self.quantum_viz.save_breach_log(entity_data)
            
        except Exception as e:
            print(f"❌ Quantum visualization error: {e}")

    def detect_entities(self):
        """Main detection loop"""
        print("\n🔍 Initial scan...")
        
        # Build baseline
        networks = self.get_wifi_networks()
        for net in networks:
            ssid = net.get('ssid', '')
            if ssid in self.filter_networks:
                print(f"   🚫 Filtered: {ssid}")
            else:
                self.baseline_networks.add(net.get('bssid'))
        
        print(f"✅ Baseline: {len(self.baseline_networks)} networks")
        print("👁️  Watching for UNKNOWN entities...\n")

        while True:
            try:
                time.sleep(self.scan_interval)
                
                # Check each zone
                for zone_name in self.zones:
                    near_zone, distance = self.is_near_zone(zone_name)
                    
                    if near_zone:
                        timestamp = datetime.now().strftime('%H:%M:%S')
                        
                        # Scan for networks
                        networks = self.get_wifi_networks()
                        unknown_count = 0
                        
                        for network in networks:
                            bssid = network.get('bssid')
                            ssid = network.get('ssid', '')
                            
                            # Skip filtered networks
                            if ssid in self.filter_networks:
                                continue
                            
                            # Check if unknown
                            if bssid not in self.baseline_networks:
                                unknown_count += 1
                                
                                # Check if already alerted
                                entity_key = f"{zone_name}_{bssid}"
                                if entity_key not in self.detected_entities:
                                    self.detected_entities[entity_key] = time.time()
                                    
                                    # ALERT!
                                    print("\n" + "="*60)
                                    print(f"🚨 UNKNOWN ENTITY AT {zone_name}!")
                                    print("="*60)
                                    print(f"👻 {self.zones[zone_name]['name']}")
                                    print(f"📡 {ssid}")
                                    print(f"🔍 {bssid}")
                                    print(f"📶 {network.get('level', 0)} dBm")
                                    print(f"📏 {distance:.1f}m")
                                    print("="*60 + "\n")
                                    
                                    # Send notifications
                                    self.send_notification(zone_name, network, distance)
                                    self.send_telegram_alert(zone_name, network, distance)
                                    
                                    # QUANTUM VISUALIZATION
                                    self.visualize_breach(zone_name, network, distance)
                        
                        # Status update
                        if unknown_count == 0:
                            print(f"[{timestamp}] 🚪 {zone_name} ({distance:.1f}m)")
                            print(f"[{timestamp}] 👁️  {len(networks)} networks (all known)")

            except KeyboardInterrupt:
                print("\n\n⏹️  Detector stopped")
                break
            except Exception as e:
                print(f"❌ Detection error: {e}")
                time.sleep(self.scan_interval)


class AndroidLocationProvider:
    def __init__(self):
        self.last_location = None
        self.location_enabled = self._check_location_available()

    def _check_location_available(self):
        """Check if Termux API is available"""
        try:
            import shutil
            termux_location_path = shutil.which('termux-location')
            if termux_location_path:
                print(f"✅ Found termux-location at: {termux_location_path}")
                return True

            result = subprocess.run(
                ['termux-location', '-h'],
                capture_output=True,
                timeout=2
            )
            return True
        except Exception as e:
            print(f"⚠️  Termux API check failed: {e}")
            return False

    def get_current_location(self):
        """Get GPS location using Termux API"""
        if not self.location_enabled:
            print("❌ Termux API not available")
            return None

        try:
            result = subprocess.run(
                ['termux-location', '-p', 'gps', '-r', 'once'],
                capture_output=True,
                text=True,
                timeout=15
            )

            if result.returncode == 0 and result.stdout.strip():
                location_data = json.loads(result.stdout)

                latitude = location_data.get('latitude')
                longitude = location_data.get('longitude')
                accuracy = location_data.get('accuracy', 0)
                altitude = location_data.get('altitude', 0)
                bearing = location_data.get('bearing', 0)
                speed = location_data.get('speed', 0)

                if latitude and longitude:
                    self.last_location = (latitude, longitude)
                    return {
                        'latitude': latitude,
                        'longitude': longitude,
                        'accuracy': accuracy,
                        'altitude': altitude,
                        'bearing': bearing,
                        'speed': speed,
                        'timestamp': time.time()
                    }
            else:
                print(f"⚠️  Location request failed: {result.stderr}")

            if self.last_location:
                print("📍 Using last known location")
                return {
                    'latitude': self.last_location[0],
                    'longitude': self.last_location[1],
                    'accuracy': None,
                    'timestamp': time.time()
                }

        except subprocess.TimeoutExpired:
            print("⏱️  Location request timed out")
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse location data: {e}")
        except Exception as e:
            print(f"❌ Location error: {e}")

        return None


if __name__ == "__main__":
    # Load configuration
    with open('config/door_zones.json', 'r') as f:
        zones = json.load(f)
    
    with open('config/my_networks.json', 'r') as f:
        my_nets = json.load(f)['my_networks']
        filter_networks = my_nets.get('ssids', []) + my_nets.get('keywords', [])
    
    # Start detector
    detector = WiFiEntityDetector(
        zones=zones,
        scan_interval=5,
        detection_range=60,
        filter_networks=filter_networks
    )
    
    detector.detect_entities()
