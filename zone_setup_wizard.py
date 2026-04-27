#!/usr/bin/env python3
"""
Interactive Zone Setup Wizard for Advanced Geofencing
Creates and manages geofencing zones with quantum features
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class ZoneSetupWizard:
    def __init__(self):
        self.zones_file = "zones_config.json"
        self.supernatural_file = "supernatural_zones.json"
        self.zones = self.load_zones()
        
    def load_zones(self) -> Dict:
        """Load existing zones or create new structure"""
        if os.path.exists(self.zones_file):
            with open(self.zones_file, 'r') as f:
                return json.load(f)
        return {"zones": [], "metadata": {"created": str(datetime.now())}}
    
    def save_zones(self):
        """Save zones to file"""
        self.zones["metadata"]["last_updated"] = str(datetime.now())
        with open(self.zones_file, 'w') as f:
            json.dump(self.zones, f, indent=2)
        print(f"\n✓ Zones saved to {self.zones_file}")
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_header(self, title: str):
        """Print formatted header"""
        print("\n" + "="*60)
        print(f"  {title}")
        print("="*60 + "\n")
    
    def get_input(self, prompt: str, default: str = None, input_type: type = str):
        """Get user input with validation"""
        while True:
            if default:
                user_input = input(f"{prompt} [{default}]: ").strip()
                if not user_input:
                    return default
            else:
                user_input = input(f"{prompt}: ").strip()
            
            if not user_input and not default:
                print("⚠ Input required. Please try again.")
                continue
            
            try:
                if input_type == float:
                    return float(user_input)
                elif input_type == int:
                    return int(user_input)
                elif input_type == bool:
                    return user_input.lower() in ['y', 'yes', 'true', '1']
                return user_input
            except ValueError:
                print(f"⚠ Invalid {input_type.__name__}. Please try again.")
    
    def create_circular_zone(self) -> Dict:
        """Create a circular geofence zone"""
        print("\n📍 Creating Circular Zone")
        print("-" * 40)
        
        zone = {
            "type": "circular",
            "name": self.get_input("Zone name", "Home"),
            "center": {
                "latitude": self.get_input("Center latitude", "0.0", float),
                "longitude": self.get_input("Center longitude", "0.0", float)
            },
            "radius_meters": self.get_input("Radius (meters)", "100", float),
            "enabled": True,
            "created": str(datetime.now())
        }
        
        # Optional features
        print("\n🔧 Optional Features:")
        if self.get_input("Add quantum detection? (y/n)", "n", bool):
            zone["quantum_enabled"] = True
            zone["quantum_sensitivity"] = self.get_input("Quantum sensitivity (0.0-1.0)", "0.5", float)
        
        if self.get_input("Add alerts? (y/n)", "y", bool):
            zone["alerts"] = {
                "on_entry": self.get_input("Alert on entry? (y/n)", "y", bool),
                "on_exit": self.get_input("Alert on exit? (y/n)", "y", bool),
                "notification_type": self.get_input("Notification type", "push")
            }
        
        if self.get_input("Add schedule? (y/n)", "n", bool):
            zone["schedule"] = {
                "active_hours": self.get_input("Active hours (e.g., 08:00-18:00)", "00:00-23:59"),
                "active_days": self.get_input("Active days (e.g., Mon,Tue,Wed)", "Mon,Tue,Wed,Thu,Fri,Sat,Sun")
            }
        
        return zone
    
    def create_polygon_zone(self) -> Dict:
        """Create a polygon geofence zone"""
        print("\n📐 Creating Polygon Zone")
        print("-" * 40)
        
        zone = {
            "type": "polygon",
            "name": self.get_input("Zone name", "Custom Area"),
            "coordinates": [],
            "enabled": True,
            "created": str(datetime.now())
        }
        
        print("\n📍 Enter polygon vertices (minimum 3 points)")
        print("Enter 'done' when finished")
        
        point_num = 1
        while True:
            print(f"\nPoint {point_num}:")
            lat_input = input("  Latitude (or 'done'): ").strip()
            
            if lat_input.lower() == 'done':
                if len(zone["coordinates"]) < 3:
                    print("⚠ Need at least 3 points for a polygon!")
                    continue
                break
            
            try:
                lat = float(lat_input)
                lon = float(input("  Longitude: ").strip())
                zone["coordinates"].append({"lat": lat, "lon": lon})
                point_num += 1
            except ValueError:
                print("⚠ Invalid coordinates. Try again.")
        
        # Optional features (same as circular)
        print("\n🔧 Optional Features:")
        if self.get_input("Add quantum detection? (y/n)", "n", bool):
            zone["quantum_enabled"] = True
            zone["quantum_sensitivity"] = self.get_input("Quantum sensitivity (0.0-1.0)", "0.5", float)
        
        return zone
    
    def create_supernatural_zone(self) -> Dict:
        """Create a supernatural/quantum zone"""
        print("\n🌌 Creating Supernatural Zone")
        print("-" * 40)
        
        zone = {
            "type": "supernatural",
            "name": self.get_input("Zone name", "Quantum Anomaly"),
            "center": {
                "latitude": self.get_input("Center latitude", "0.0", float),
                "longitude": self.get_input("Center longitude", "0.0", float)
            },
            "radius_meters": self.get_input("Radius (meters)", "50", float),
            "quantum_properties": {
                "entanglement_level": self.get_input("Entanglement level (0.0-1.0)", "0.8", float),
                "superposition_active": self.get_input("Superposition active? (y/n)", "y", bool),
                "fluctuation_rate": self.get_input("Fluctuation rate (Hz)", "1.0", float)
            },
            "detection_mode": self.get_input("Detection mode (passive/active)", "active"),
            "enabled": True,
            "created": str(datetime.now())
        }
        
        return zone
    
    def list_zones(self):
        """Display all configured zones"""
        self.print_header("Configured Zones")
        
        if not self.zones.get("zones"):
            print("No zones configured yet.\n")
            return
        
        for idx, zone in enumerate(self.zones["zones"], 1):
            status = "✓ Enabled" if zone.get("enabled", True) else "✗ Disabled"
            print(f"{idx}. {zone['name']} ({zone['type']}) - {status}")
            
            if zone["type"] == "circular":
                print(f"   Center: {zone['center']['latitude']}, {zone['center']['longitude']}")
                print(f"   Radius: {zone['radius_meters']}m")
            elif zone["type"] == "polygon":
                print(f"   Vertices: {len(zone['coordinates'])} points")
            
            if zone.get("quantum_enabled"):
                print(f"   🌌 Quantum: Sensitivity {zone.get('quantum_sensitivity', 0.5)}")
            print()
    
    def edit_zone(self):
        """Edit an existing zone"""
        self.list_zones()
        
        if not self.zones.get("zones"):
            return
        
        try:
            idx = int(input("\nEnter zone number to edit (0 to cancel): ")) - 1
            if idx < 0:
                return
            
            zone = self.zones["zones"][idx]
            print(f"\nEditing: {zone['name']}")
            print("-" * 40)
            
            zone["name"] = self.get_input("Zone name", zone["name"])
            zone["enabled"] = self.get_input("Enabled? (y/n)", "y" if zone.get("enabled", True) else "n", bool)
            
            if zone["type"] == "circular":
                zone["radius_meters"] = self.get_input("Radius (meters)", str(zone["radius_meters"]), float)
            
            print("\n✓ Zone updated!")
            
        except (ValueError, IndexError):
            print("⚠ Invalid zone number")
    
    def delete_zone(self):
        """Delete a zone"""
        self.list_zones()
        
        if not self.zones.get("zones"):
            return
        
        try:
            idx = int(input("\nEnter zone number to delete (0 to cancel): ")) - 1
            if idx < 0:
                return
            
            zone = self.zones["zones"][idx]
            confirm = input(f"Delete '{zone['name']}'? (y/n): ").lower()
            
            if confirm == 'y':
                self.zones["zones"].pop(idx)
                print("\n✓ Zone deleted!")
            
        except (ValueError, IndexError):
            print("⚠ Invalid zone number")
    
    def import_from_gps(self):
        """Import current GPS location as zone center"""
        print("\n📡 GPS Import")
        print("-" * 40)
        print("This would connect to device GPS...")
        print("(Feature coming soon - manual entry for now)")
        
        lat = self.get_input("Current latitude", "0.0", float)
        lon = self.get_input("Current longitude", "0.0", float)
        
        zone = {
            "type": "circular",
            "name": self.get_input("Zone name", "Current Location"),
            "center": {"latitude": lat, "longitude": lon},
            "radius_meters": self.get_input("Radius (meters)", "100", float),
            "enabled": True,
            "created": str(datetime.now()),
            "source": "gps_import"
        }
        
        self.zones["zones"].append(zone)
        print("\n✓ Zone created from GPS location!")
    
    def main_menu(self):
        """Main wizard menu"""
        while True:
            self.clear_screen()
            self.print_header("Zone Setup Wizard")
            
            print("1. Create Circular Zone")
            print("2. Create Polygon Zone")
            print("3. Create Supernatural/Quantum Zone")
            print("4. List All Zones")
            print("5. Edit Zone")
            print("6. Delete Zone")
            print("7. Import from GPS")
            print("8. Save & Exit")
            print("9. Exit without Saving")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                zone = self.create_circular_zone()
                self.zones["zones"].append(zone)
                print("\n✓ Circular zone created!")
                input("\nPress Enter to continue...")
                
            elif choice == "2":
                zone = self.create_polygon_zone()
                self.zones["zones"].append(zone)
                print("\n✓ Polygon zone created!")
                input("\nPress Enter to continue...")
                
            elif choice == "3":
                zone = self.create_supernatural_zone()
                self.zones["zones"].append(zone)
                print("\n✓ Supernatural zone created!")
                input("\nPress Enter to continue...")
                
            elif choice == "4":
                self.list_zones()
                input("\nPress Enter to continue...")
                
            elif choice == "5":
                self.edit_zone()
                input("\nPress Enter to continue...")
                
            elif choice == "6":
                self.delete_zone()
                input("\nPress Enter to continue...")
                
            elif choice == "7":
                self.import_from_gps()
                input("\nPress Enter to continue...")
                
            elif choice == "8":
                self.save_zones()
                print("\n👋 Goodbye!")
                break
                
            elif choice == "9":
                confirm = input("Exit without saving? (y/n): ").lower()
                if confirm == 'y':
                    print("\n👋 Goodbye!")
                    break
            
            else:
                print("⚠ Invalid option")
                input("\nPress Enter to continue...")

def main():
    """Run the zone setup wizard"""
    wizard = ZoneSetupWizard()
    wizard.main_menu()

if __name__ == "__main__":
    main()
