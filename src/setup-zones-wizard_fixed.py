#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

class ZoneSetupWizard:
    def __init__(self):
        self.zones = []
        self.config_file = Path("config/entity_zones.json")
        # FIX: Create config directory if it doesn't exist
        self.config_file.parent.mkdir(parents=True, exist_ok=True)

    def get_current_location(self):
        """Get GPS coordinates"""
        try:
            result = subprocess.run(
                ['termux-location', '-p', 'gps'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                location = json.loads(result.stdout)
                return location['latitude'], location['longitude']
            return None, None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None, None

    def add_zone(self, name, emoji, entity, description, radius):
        """Add a zone with current GPS location"""
        print(f"\n📍 Walk to your {name}...")
        input("Press ENTER when you're at the exact spot...")

        print("📡 Getting GPS coordinates...")
        lat, lon = self.get_current_location()

        if lat is None:
            print("❌ Failed to get location!")
            return False

        print(f"✅ Location captured: {lat}, {lon}")

        zone = {
            'name': name,
            'emoji': emoji,
            'entity': entity,
            'description': description,
            'lat': lat,
            'lon': lon,
            'radius': radius,
            'active_hours': [6, 22]
        }

        self.zones.append(zone)
        print(f"✅ {emoji} {name} added!")
        return True

    def add_custom_zone(self):
        """Add custom zone"""
        print("\n" + "="*60)
        print("🎮 CUSTOM ZONE")
        print("="*60)

        name = input("Zone name: ").strip().upper().replace(' ', '_')
        emoji = input("Emoji: ").strip() or "📍"
        entity = input("Entity name: ").strip()
        description = input("Description: ").strip()
        radius = int(input("Radius (meters, default 5): ").strip() or "5")

        self.add_zone(name, emoji, entity, description, radius)

    def save_zones(self):
        """Save zones to config"""
        # FIX: Ensure directory exists before saving
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        config = {'entity_zones': self.zones}
        self.config_file.write_text(json.dumps(config, indent=2))
        print(f"\n💾 Saved {len(self.zones)} zones to {self.config_file}!")

    def load_existing_zones(self):
        """Load existing zones"""
        if self.config_file.exists():
            config = json.loads(self.config_file.read_text())
            self.zones = config.get('entity_zones', [])
            print(f"📂 Loaded {len(self.zones)} existing zones")

    def show_zones(self):
        """Display all zones"""
        if not self.zones:
            print("\n📍 No zones configured yet")
            return

        print("\n" + "="*60)
        print("📍 CONFIGURED ENTITY ZONES")
        print("="*60)

        for i, zone in enumerate(self.zones, 1):
            print(f"\n{i}. {zone['emoji']} {zone['name']}")
            print(f"   Entity: {zone['entity']}")
            print(f"   Description: {zone['description']}")
            print(f"   Location: ({zone['lat']}, {zone['lon']})")
            print(f"   Radius: {zone['radius']}m")

    def run(self):
        """Main wizard loop"""
        print("="*60)
        print("✨ ENTITY ZONE SETUP WIZARD ✨")
        print("="*60)

        self.load_existing_zones()

        while True:
            print("\n" + "="*60)
            print("🎯 QUICK SETUP MENU:")
            print("="*60)
            print("  [F] 🚪 Front Door - The Doorway Guardian")
            print("  [B] 🚪 Back Door - The Shadow Keeper")
            print("  [H] 🌀 Hallway - The Corridor Walker")
            print("  [M] 🪞 Mirror Spot - The Reflection")
            print("  [W] 🪟 Window - The Watcher")
            print("  [L] 🛋️  Living Room - The Presence")
            print()
            print("  [C] 🎮 Add Custom Zone")
            print("  [V] 👁️  View All Zones")
            print("  [S] 💾 Save and Exit")
            print("  [Q] 🚪 Quit Without Saving")
            print("="*60)

            choice = input("\nChoice: ").strip().upper()

            if choice == 'F':
                self.add_zone(
                    'FRONT_DOOR', '🚪',
                    'The Doorway Guardian',
                    'Portal between normal and parallel worlds',
                    5
                )
            elif choice == 'B':
                self.add_zone(
                    'BACK_DOOR', '🚪',
                    'The Shadow Keeper',
                    'Where shadows cross dimensions',
                    5
                )
            elif choice == 'H':
                self.add_zone(
                    'HALLWAY', '🌀',
                    'The Corridor Walker',
                    'Infinite hallway between realities',
                    3
                )
            elif choice == 'M':
                self.add_zone(
                    'MIRROR_SPOT', '🪞',
                    'The Reflection',
                    'Your parallel self appears here',
                    2
                )
            elif choice == 'W':
                self.add_zone(
                    'WINDOW', '🪟',
                    'The Watcher',
                    'Observer from the other side',
                    3
                )
            elif choice == 'L':
                self.add_zone(
                    'LIVING_ROOM', '🛋️',
                    'The Presence',
                    'Unseen entity in familiar space',
                    10
                )
            elif choice == 'C':
                self.add_custom_zone()
            elif choice == 'V':
                self.show_zones()
            elif choice == 'S':
                self.save_zones()
                self.show_zones()
                print("\n✅ Configuration saved!")
                break
            elif choice == 'Q':
                print("\n👋 Exiting without saving")
                break
            else:
                print("\n❌ Invalid choice!")

if __name__ == "__main__":
    wizard = ZoneSetupWizard()
    wizard.run()
