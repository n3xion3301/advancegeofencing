#!/usr/bin/env python3
"""
Enhanced Entity Zone Setup Wizard
Fixed version with proper error handling
"""

import json
import os
import subprocess
import time
from datetime import datetime

class EnhancedZoneWizard:
    def __init__(self):
        self.config_dir = "config"
        self.zones_file = f"{self.config_dir}/entity_zones.json"
        self.zones = self.load_zones()
        
        # Preset zones with entities
        self.presets = {
            'F': {'name': 'Front Door', 'emoji': '🚪', 'entity': 'The Doorway Guardian', 'desc': 'Watches who enters', 'radius': 3},
            'B': {'name': 'Back Door', 'emoji': '🚪', 'entity': 'The Shadow Keeper', 'desc': 'Guards the rear', 'radius': 3},
            'H': {'name': 'Hallway', 'emoji': '🌀', 'entity': 'The Corridor Walker', 'desc': 'Moves through passages', 'radius': 5},
            'M': {'name': 'Mirror Spot', 'emoji': '🪞', 'entity': 'The Reflection', 'desc': 'Shows what should not be', 'radius': 2},
            'W': {'name': 'Window', 'emoji': '🪟', 'entity': 'The Watcher', 'desc': 'Observes from outside', 'radius': 3},
            'L': {'name': 'Living Room', 'emoji': '🛋️', 'entity': 'The Presence', 'desc': 'Felt but not seen', 'radius': 7},
            'K': {'name': 'Kitchen', 'emoji': '🍳', 'entity': 'The Midnight Cook', 'desc': 'Things move at night', 'radius': 5},
            'BR': {'name': 'Bedroom', 'emoji': '🛏️', 'entity': 'The Dream Walker', 'desc': 'Visits during sleep', 'radius': 6},
            'BA': {'name': 'Bathroom', 'emoji': '🚿', 'entity': 'The Mist', 'desc': 'Appears in steam', 'radius': 4},
        }
    
    def load_zones(self):
        """Load existing zones with proper error handling"""
        os.makedirs(self.config_dir, exist_ok=True)
        
        if os.path.exists(self.zones_file):
            try:
                with open(self.zones_file, 'r') as f:
                    data = json.load(f)
                    # Ensure 'zones' key exists
                    if 'zones' not in data:
                        data['zones'] = []
                    if 'metadata' not in data:
                        data['metadata'] = {"created": str(datetime.now())}
                    return data
            except (json.JSONDecodeError, Exception) as e:
                print(f"⚠️  Error loading zones file: {e}")
                print("Creating new zones file...")
        
        # Return default structure
        return {
            "zones": [],
            "metadata": {"created": str(datetime.now())}
        }
    
    def save_zones(self):
        """Save zones to file"""
        self.zones["metadata"]["last_updated"] = str(datetime.now())
        with open(self.zones_file, 'w') as f:
            json.dump(self.zones, f, indent=2)
    
    def get_location_smart(self, zone_name):
        """Smart location getter with multiple methods"""
        print(f"\n📍 Setting up location for {zone_name}...")
        print("\nChoose method:")
        print("  [1] GPS (most accurate, works in airplane mode, may take 30s)")
        print("  [2] Network location (faster, needs internet)")
        print("  [3] Manual entry (always works)")
        print("  [4] Use last known location")
        
        choice = input("\nMethod [1]: ").strip() or "1"
        
        if choice == "1":
            return self.get_gps_location()
        elif choice == "2":
            return self.get_network_location()
        elif choice == "3":
            return self.get_manual_location()
        elif choice == "4":
            return self.get_last_location()
        else:
            print("Invalid choice, using GPS...")
            return self.get_gps_location()
    
    def get_gps_location(self):
        """Get GPS location with progress indicator"""
        print("\n📡 Acquiring GPS fix...")
        print("💡 Tip: Works in airplane mode! Make sure you're near a window")
        print("⏱️  This may take 15-30 seconds...")
        
        for i in range(3):
            try:
                print(f"\nAttempt {i+1}/3...")
                result = subprocess.run(
                    ['termux-location', '-p', 'gps', '-r', 'last'],
                    capture_output=True,
                    text=True,
                    timeout=15
                )
                
                if result.returncode == 0 and result.stdout:
                    data = json.loads(result.stdout)
                    if 'latitude' in data and 'longitude' in data:
                        print(f"✓ GPS fix acquired! Accuracy: {data.get('accuracy', 'unknown')}m")
                        return {
                            'latitude': data['latitude'],
                            'longitude': data['longitude'],
                            'accuracy': data.get('accuracy'),
                            'method': 'gps'
                        }
            except subprocess.TimeoutExpired:
                print("⏱️  Timeout, retrying...")
            except Exception as e:
                print(f"⚠️  Error: {e}")
        
        print("\n❌ GPS failed after 3 attempts")
        print("Falling back to manual entry...")
        return self.get_manual_location()
    
    def get_network_location(self):
        """Get network-based location"""
        print("\n📡 Getting network location...")
        print("⚠️  Requires internet connection")
        
        try:
            result = subprocess.run(
                ['termux-location', '-p', 'network'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                if 'latitude' in data and 'longitude' in data:
                    print(f"✓ Network location acquired! Accuracy: {data.get('accuracy', 'unknown')}m")
                    return {
                        'latitude': data['latitude'],
                        'longitude': data['longitude'],
                        'accuracy': data.get('accuracy'),
                        'method': 'network'
                    }
        except Exception as e:
            print(f"⚠️  Network location failed: {e}")
        
        print("\nFalling back to manual entry...")
        return self.get_manual_location()
    
    def get_manual_location(self):
        """Manual coordinate entry"""
        print("\n📍 Manual Coordinate Entry")
        print("💡 Tip: Long-press on Google Maps to get coordinates")
        print()
        
        try:
            lat = float(input("Latitude: ").strip())
            lon = float(input("Longitude: ").strip())
            
            return {
                'latitude': lat,
                'longitude': lon,
                'accuracy': 'manual',
                'method': 'manual'
            }
        except ValueError:
            print("❌ Invalid coordinates!")
            return None
    
    def get_last_location(self):
        """Use last known location from cache"""
        cache_file = "location_cache.json"
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    loc = json.load(f)
                    print(f"\n✓ Using cached location: {loc['latitude']}, {loc['longitude']}")
                    return loc
            except Exception as e:
                print(f"⚠️  Error reading cache: {e}")
        
        print("\n❌ No cached location found")
        return self.get_gps_location()
    
    def cache_location(self, location):
        """Cache location for future use"""
        if location:
            try:
                with open("location_cache.json", 'w') as f:
                    json.dump(location, f)
            except Exception as e:
                print(f"⚠️  Could not cache location: {e}")
    
    def create_zone(self, preset_key=None):
        """Create a new zone"""
        if preset_key and preset_key in self.presets:
            preset = self.presets[preset_key]
            zone_data = {
                'name': preset['name'],
                'emoji': preset['emoji'],
                'entity': preset['entity'],
                'description': preset['desc'],
                'radius': preset['radius']
            }
        else:
            # Custom zone
            print("\n" + "="*60)
            print("🎮 CUSTOM ZONE")
            print("="*60)
            zone_data = {
                'name': input("Zone name: ").strip(),
                'emoji': input("Emoji: ").strip() or "📍",
                'entity': input("Entity name: ").strip(),
                'description': input("Description: ").strip(),
                'radius': float(input("Radius (meters, default 5): ").strip() or "5")
            }
        
        # Get location
        location = self.get_location_smart(zone_data['name'])
        
        if not location:
            print("❌ Failed to get location!")
            return False
        
        # Cache the location
        self.cache_location(location)
        
        # Create zone object
        zone = {
            **zone_data,
            'center': {
                'latitude': location['latitude'],
                'longitude': location['longitude']
            },
            'location_method': location['method'],
            'accuracy': location.get('accuracy'),
            'enabled': True,
            'created': str(datetime.now())
        }
        
        self.zones['zones'].append(zone)
        print(f"\n✅ Zone '{zone_data['name']}' created!")
        return True
    
    def view_zones(self):
        """Display all zones"""
        print("\n" + "="*60)
        print("👁️  CONFIGURED ZONES")
        print("="*60)
        
        if not self.zones.get('zones'):
            print("\n📍 No zones configured yet\n")
            return
        
        for idx, zone in enumerate(self.zones['zones'], 1):
            status = "✓" if zone.get('enabled') else "✗"
            print(f"\n{idx}. {zone.get('emoji', '📍')} {zone['name']} {status}")
            print(f"   Entity: {zone.get('entity', 'Unknown')}")
            print(f"   Location: {zone['center']['latitude']:.6f}, {zone['center']['longitude']:.6f}")
            print(f"   Radius: {zone.get('radius', 5)}m")
            print(f"   Method: {zone.get('location_method', 'unknown')}")
            if zone.get('accuracy'):
                print(f"   Accuracy: {zone['accuracy']}m")
        print()
    
    def main_menu(self):
        """Main wizard interface"""
        while True:
            print("\n" + "="*60)
            print("✨ ENTITY ZONE SETUP WIZARD ✨")
            print("="*60)
            print(f"📂 Loaded {len(self.zones.get('zones', []))} existing zones\n")
            
            print("="*60)
            print("🎯 QUICK SETUP MENU:")
            print("="*60)
            
            for key, preset in self.presets.items():
                print(f"  [{key}] {preset['emoji']} {preset['name']} - {preset['entity']}")
            
            print(f"\n  [C] 🎮 Add Custom Zone")
            print(f"  [V] 👁️  View All Zones")
            print(f"  [D] 🗑️  Delete Zone")
            print(f"  [S] 💾 Save and Exit")
            print(f"  [Q] 🚪 Quit Without Saving")
            print("="*60)
            
            choice = input("\nChoice: ").strip().upper()
            
            if choice in self.presets:
                self.create_zone(choice)
            elif choice == 'C':
                self.create_zone()
            elif choice == 'V':
                self.view_zones()
                input("\nPress Enter to continue...")
            elif choice == 'D':
                self.view_zones()
                try:
                    idx = int(input("Zone number to delete (0 to cancel): ")) - 1
                    if idx >= 0 and idx < len(self.zones['zones']):
                        deleted = self.zones['zones'].pop(idx)
                        print(f"✓ Deleted '{deleted['name']}'")
                except (ValueError, IndexError):
                    print("❌ Invalid zone number")
            elif choice == 'S':
                self.save_zones()
                print(f"\n💾 Saved {len(self.zones['zones'])} zones to {self.zones_file}!")
                self.view_zones()
                print("✅ Configuration saved!")
                break
            elif choice == 'Q':
                confirm = input("Quit without saving? (y/n): ").lower()
                if confirm == 'y':
                    print("👋 Goodbye!")
                    break
            else:
                print("❌ Invalid choice")

def main():
    wizard = EnhancedZoneWizard()
    wizard.main_menu()

if __name__ == "__main__":
    main()
