#!/usr/bin/env python3
"""
ENHANCED HOMEHAVEN
Advanced Geofencing Home Monitoring System

ENHANCEMENTS:
- Beautiful geofence zone visualizations
- GPS coordinate displays
- Entry/exit detection animations
- Home monitoring dashboards
- Zone boundary diagrams
- Real-time detection alerts
- Activity timeline tracking
- Comprehensive monitoring analytics
"""

import math
import json
import time
from datetime import datetime
from typing import Tuple, Dict, List
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class HomeHavenEnhanced:
    """Enhanced Geofencing Home Monitoring System"""
    
    def __init__(self, center_lat: float, center_lon: float, radius_meters: float):
        """
        Initialize geofence with center coordinates and radius
        
        Args:
            center_lat: Center latitude (your home)
            center_lon: Center longitude (your home)
            radius_meters: Geofence radius in meters
        """
        self.center_lat = center_lat
        self.center_lon = center_lon
        self.radius_meters = radius_meters
        
        self.detections = []
        self.inside_zone = {}
        
        self.log_dir = Path("logs/homehaven")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self._print_banner()
    
    def _print_banner(self):
        """Print stunning HomeHaven banner with ASCII art"""
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║            ✧･ﾟ: *✧･ﾟ:* HOMEHAVEN ENHANCED *:･ﾟ✧*:･ﾟ✧                    ║
║              Advanced Geofencing Home Monitoring System                  ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

                    ╔════════════════════════════════╗
                    ║                                ║
                    ║      🏠 HOME MONITORING 🏠     ║
                    ║                                ║
                    ║         ╭─────────╮            ║
                    ║       ╱             ╲          ║
                    ║     ╱                 ╲        ║
                    ║   ╱                     ╲      ║
                    ║  │    ┌───────────┐     │     ║
                    ║  │    │           │     │     ║
                    ║  │    │    🏠     │     │     ║
                    ║  │    │   HOME    │     │     ║
                    ║  │    │           │     │     ║
                    ║  │    └───────────┘     │     ║
                    ║   ╲                     ╱      ║
                    ║     ╲                 ╱        ║
                    ║       ╲             ╱          ║
                    ║         ╰─────────╯            ║
                    ║                                ║
                    ║      GEOFENCE ACTIVE           ║
                    ║                                ║
                    ║  [●] MONITORING  [◉] ACTIVE   ║
                    ║                                ║
                    ╚════════════════════════════════╝

        ┌────────────────────────────────────────────────────┐
        │  📍 GEOFENCE SPECIFICATIONS                         │
        ├────────────────────────────────────────────────────┤
        │  • Center: ({:.6f}, {:.6f})      │
        │  • Radius: {} meters                               │
        │  • Status: ACTIVE                                  │
        │  • Detections: 0                                   │
        └────────────────────────────────────────────────────┘
        """.format(self.center_lat, self.center_lon, self.radius_meters))
    
    def print_geofence_zone(self, current_lat=None, current_lon=None):
        """Print geofence zone visualization"""
        
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                        🗺️  GEOFENCE ZONE 🗺️                              ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
        """)
        
        # Draw zone boundary
        print("║                    ╭───────────────────────╮                           ║")
        print("║                  ╱                         ╲                         ║")
        print("║                ╱                             ╲                       ║")
        print("║              ╱                                 ╲                     ║")
        print("║            ╱                                     ╲                   ║")
        print("║          ╱              SAFE ZONE                 ╲                 ║")
        print("║        ╱                                           ╲               ║")
        print("║       │                                             │              ║")
        print("║       │                  ┌─────────┐                │              ║")
        print("║       │                  │         │                │              ║")
        
        if current_lat and current_lon:
            inside = self.is_inside_zone(current_lat, current_lon)
            if inside:
                print("║       │                  │  🏠 📍  │                │              ║")
            else:
                print("║       │                  │   🏠    │                │              ║")
        else:
            print("║       │                  │   🏠    │                │              ║")
        
        print("║       │                  │  HOME   │                │              ║")
        print("║       │                  │         │                │              ║")
        print("║       │                  └─────────┘                │              ║")
        print("║       │                                             │              ║")
        print("║        ╲                                           ╱               ║")
        print("║          ╲                                       ╱                 ║")
        print("║            ╲                                   ╱                   ║")
        print("║              ╲                               ╱                     ║")
        print("║                ╲                           ╱                       ║")
        print("║                  ╲                       ╱                         ║")
        print("║                    ╰───────────────────╯                           ║")
        print("║                                                                          ║")
        
        if current_lat and current_lon:
            distance = self.calculate_distance(current_lat, current_lon)
            print(f"║  Current Position: ({current_lat:.6f}, {current_lon:.6f})".ljust(76) + "║")
            print(f"║  Distance from Home: {distance:.2f} meters".ljust(76) + "║")
            
            if self.is_inside_zone(current_lat, current_lon):
                print("║  Status: ✅ INSIDE GEOFENCE".ljust(76) + "║")
            else:
                print("║  Status: ⚠️  OUTSIDE GEOFENCE".ljust(76) + "║")
        
        print("║" + " "*74 + "║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")
    
    def log(self, msg):
        """Log message with timestamp"""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{ts}] {msg}"
        print(formatted)
        
        try:
            log_file = self.log_dir / "homehaven.log"
            with open(log_file, 'a') as f:
                f.write(formatted + "\n")
        except Exception:
            pass
    
    def calculate_distance(self, lat: float, lon: float) -> float:
        """
        Calculate distance from home using Haversine formula
        
        Args:
            lat: Current latitude
            lon: Current longitude
        
        Returns:
            float: Distance in meters
        """
        # Earth radius in meters
        R = 6371000
        
        # Convert to radians
        lat1 = math.radians(self.center_lat)
        lat2 = math.radians(lat)
        delta_lat = math.radians(lat - self.center_lat)
        delta_lon = math.radians(lon - self.center_lon)
        
        # Haversine formula
        a = math.sin(delta_lat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return distance
    
    def is_inside_zone(self, lat: float, lon: float) -> bool:
        """
        Check if coordinates are inside geofence
        
        Args:
            lat: Latitude to check
            lon: Longitude to check
        
        Returns:
            bool: True if inside zone
        """
        distance = self.calculate_distance(lat, lon)
        return distance <= self.radius_meters
    
    def print_entry_alert(self, entity_id: str, lat: float, lon: float):
        """Print entry alert animation"""
        
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                        🚨 ENTRY DETECTED! 🚨                              ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
        """)
        
        print(f"║  Entity: {entity_id}".ljust(76) + "║")
        print(f"║  Location: ({lat:.6f}, {lon:.6f})".ljust(76) + "║")
        print("║" + " "*74 + "║")
        
        # Entry animation
        print("║  ┌──────────────────────────────────────────────────────────────┐".ljust(76) + "║")
        print("║  │                                                              │".ljust(76) + "║")
        print("║  │                    ╭─────────────╮                           │".ljust(76) + "║")
        print("║  │                  ╱                 ╲                         │".ljust(76) + "║")
        print("║  │                ╱                     ╲                       │".ljust(76) + "║")
        print("║  │              ╱                         ╲                     │".ljust(76) + "║")
        print("║  │            ╱          📍 ENTRY          ╲                   │".ljust(76) + "║")
        print("║  │          ╱              ↓                 ╲                 │".ljust(76) + "║")
        print("║  │        ╱          ┌─────────┐              ╲               │".ljust(76) + "║")
        print("║  │       │           │   🏠    │               │              │".ljust(76) + "║")
        print("║  │       │           │  HOME   │               │              │".ljust(76) + "║")
        print("║  │       │           └─────────┘               │              │".ljust(76) + "║")
        print("║  │        ╲                                   ╱               │".ljust(76) + "║")
        print("║  │          ╲                               ╱                 │".ljust(76) + "║")
        print("║  │            ╲                           ╱                   │".ljust(76) + "║")
        print("║  │              ╲                       ╱                     │".ljust(76) + "║")
        print("║  │                ╲                   ╱                       │".ljust(76) + "║")
        print("║  │                  ╲               ╱                         │".ljust(76) + "║")
        print("║  │                    ╰───────────╯                           │".ljust(76) + "║")
        print("║  │                                                              │".ljust(76) + "║")
        print("║  └──────────────────────────────────────────────────────────────┘".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("║  Status: ✅ ENTITY ENTERED GEOFENCE".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")
    
    def print_exit_alert(self, entity_id: str, lat: float, lon: float):
        """Print exit alert animation"""
        
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                        ⚠️  EXIT DETECTED! ⚠️                              ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
        """)
        
        print(f"║  Entity: {entity_id}".ljust(76) + "║")
        print(f"║  Location: ({lat:.6f}, {lon:.6f})".ljust(76) + "║")
        print("║" + " "*74 + "║")
        
        # Exit animation
        print("║  ┌──────────────────────────────────────────────────────────────┐".ljust(76) + "║")
        print("║  │                                                              │".ljust(76) + "║")
        print("║  │                    ╭─────────────╮                           │".ljust(76) + "║")
        print("║  │                  ╱                 ╲                         │".ljust(76) + "║")
        print("║  │                ╱                     ╲                       │".ljust(76) + "║")
        print("║  │              ╱                         ╲                     │".ljust(76) + "║")
        print("║  │            ╱                             ╲                   │".ljust(76) + "║")
        print("║  │          ╱          ┌─────────┐           ╲                 │".ljust(76) + "║")
        print("║  │        ╱            │   🏠    │             ╲               │".ljust(76) + "║")
        print("║  │       │             │  HOME   │              │              │".ljust(76) + "║")
        print("║  │       │             └─────────┘              │              │".ljust(76) + "║")
        print("║  │       │                  ↑                   │              │".ljust(76) + "║")
        print("║  │        ╲            📍 EXIT                 ╱               │".ljust(76) + "║")
        print("║  │          ╲                               ╱                 │".ljust(76) + "║")
        print("║  │            ╲                           ╱                   │".ljust(76) + "║")
        print("║  │              ╲                       ╱                     │".ljust(76) + "║")
        print("║  │                ╲                   ╱                       │".ljust(76) + "║")
        print("║  │                  ╲               ╱                         │".ljust(76) + "║")
        print("║  │                    ╰───────────╯                           │".ljust(76) + "║")
        print("║  │                                                              │".ljust(76) + "║")
        print("║  └──────────────────────────────────────────────────────────────┘".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("║  Status: ⚠️  ENTITY LEFT GEOFENCE".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")
    
    def check_position(self, entity_id: str, lat: float, lon: float):
        """
        Check entity position and trigger alerts
        
        Args:
            entity_id: Unique identifier for entity
            lat: Current latitude
            lon: Current longitude
        """
        
        inside = self.is_inside_zone(lat, lon)
        was_inside = self.inside_zone.get(entity_id, False)
        
        # Entry detection
        if inside and not was_inside:
            self.print_entry_alert(entity_id, lat, lon)
            
            detection = {
                'entity_id': entity_id,
                'event': 'ENTRY',
                'lat': lat,
                'lon': lon,
                'timestamp': datetime.now().isoformat()
            }
            self.detections.append(detection)
            self.log(f"🚨 ENTRY: {entity_id} entered geofence")
        
        # Exit detection
        elif not inside and was_inside:
            self.print_exit_alert(entity_id, lat, lon)
            
            detection = {
                'entity_id': entity_id,
                'event': 'EXIT',
                'lat': lat,
                'lon': lon,
                'timestamp': datetime.now().isoformat()
            }
            self.detections.append(detection)
            self.log(f"⚠️  EXIT: {entity_id} left geofence")
        
        # Update status
        self.inside_zone[entity_id] = inside
        
        # Show current zone
        self.print_geofence_zone(lat, lon)
    
    def display_detection_history(self):
        """Display detection history with beautiful ASCII art"""
        
        if not self.detections:
            print("\n⚠️  No detections recorded yet")
            return
        
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                        📜 DETECTION HISTORY 📜                            ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
        """)
        
        print(f"║  Total Detections: {len(self.detections)}".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")
        
        # Display recent detections
        for i, detection in enumerate(self.detections[-5:], 1):
            event = detection['event']
            entity = detection['entity_id']
            lat = detection['lat']
            lon = detection['lon']
            
            icon = "🚨" if event == "ENTRY" else "⚠️"
            
            print(f"""
┌────────────────────────────────────────────────────────────────────────┐
│  {icon} DETECTION #{i}                                                  │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Event: {event}                                                        │
│  Entity: {entity}                                                      │
│  Location: ({lat:.6f}, {lon:.6f})                                     │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────┐     │
│  │                                                              │     │
│  │                    ╭─────────────╮                           │     │
│  │                  ╱                 ╲                         │     │
│  │                ╱                     ╲                       │     │
│  │              ╱          {icon}           ╲                     │     │
│  │            ╱          ┌─────────┐         ╲                   │     │
│  │          ╱            │   🏠    │           ╲                 │     │
│  │        ╱              │  HOME   │             ╲               │     │
│  │       │               └─────────┘              │              │     │
│  │        ╲                                      ╱               │     │
│  │          ╲                                  ╱                 │     │
│  │            ╲                              ╱                   │     │
│  │              ╲                          ╱                     │     │
│  │                ╲                      ╱                       │     │
│  │                  ╲                  ╱                         │     │
│  │                    ╰──────────────╯                           │     │
│  │                                                              │     │
│  └──────────────────────────────────────────────────────────────┘     │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
            """)
    
    def visualize_monitoring_statistics(self):
        """Visualize monitoring statistics"""
        
        if not self.detections:
            print("\n⚠️  No statistics available yet")
            return
        
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                      📊 MONITORING STATISTICS 📊                          ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
        """)
        
        total_detections = len(self.detections)
        entries = sum(1 for d in self.detections if d['event'] == 'ENTRY')
        exits = sum(1 for d in self.detections if d['event'] == 'EXIT')
        
        print(f"║  Total Detections: {total_detections}".ljust(76) + "║")
        print(f"║  Entries: {entries}".ljust(76) + "║")
        print(f"║  Exits: {exits}".ljust(76) + "║")
        print("║" + " "*74 + "║")
        
        # Event distribution
        print("║  📊 Event Distribution:".ljust(76) + "║")
        print("║" + " "*74 + "║")
        
        if entries > 0:
            bar_len = int((entries / total_detections) * 40)
            bar = "█" * bar_len + "░" * (40 - bar_len)
            print(f"║  Entries │{bar}│ {entries}".ljust(76) + "║")
        
        if exits > 0:
            bar_len = int((exits / total_detections) * 40)
            bar = "█" * bar_len + "░" * (40 - bar_len)
            print(f"║  Exits   │{bar}│ {exits}".ljust(76) + "║")
        
        print("║" + " "*74 + "║")
        
        # Currently inside zone
        inside_count = sum(1 for inside in self.inside_zone.values() if inside)
        print(f"║  Currently Inside Zone: {inside_count}".ljust(76) + "║")
        print("║" + " "*74 + "║")
        
        # Activity timeline
        print("║  🏠 Activity Timeline:".ljust(76) + "║")
        print("║" + " "*74 + "║")
        
        timeline = "  "
        for detection in self.detections[-20:]:
            if detection['event'] == 'ENTRY':
                timeline += "🚨"
            else:
                timeline += "⚠️"
        
        print(f"║{timeline}".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")


def demo_homehaven():
    """Stunning demonstration of HomeHaven"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║══════════════════════════════════════════════════════════════════════════║
║                    🏠 HOMEHAVEN DEMONSTRATION 🏠                          ║
║══════════════════════════════════════════════════════════════════════════║
╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize with example home coordinates
    # Using approximate coordinates (replace with your actual home)
    home_lat = 37.7749  # San Francisco example
    home_lon = -122.4194
    radius = 50  # 50 meters
    
    haven = HomeHavenEnhanced(home_lat, home_lon, radius)
    
    # Test 1: Check position inside zone
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 1: ENTITY INSIDE GEOFENCE ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    # Simulate entity at home (inside zone)
    entity1_lat = home_lat + 0.0001  # Very close to home
    entity1_lon = home_lon + 0.0001
    haven.check_position("Person_A", entity1_lat, entity1_lon)
    
    # Test 2: Check position outside zone
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 2: ENTITY OUTSIDE GEOFENCE ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    # Simulate entity far from home (outside zone)
    entity2_lat = home_lat + 0.001  # Further away
    entity2_lon = home_lon + 0.001
    haven.check_position("Person_B", entity2_lat, entity2_lon)
    
    # Test 3: Simulate entry
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 3: SIMULATE ENTRY EVENT ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    # Person B moves closer (enters zone)
    entity2_lat = home_lat + 0.0001
    entity2_lon = home_lon + 0.0001
    haven.check_position("Person_B", entity2_lat, entity2_lon)
    
    # Test 4: Simulate exit
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 4: SIMULATE EXIT EVENT ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    # Person A moves away (exits zone)
    entity1_lat = home_lat + 0.001
    entity1_lon = home_lon + 0.001
    haven.check_position("Person_A", entity1_lat, entity1_lon)
    
    # Test 5: Detection history
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 5: DETECTION HISTORY ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    haven.display_detection_history()
    
    # Test 6: Statistics
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 6: MONITORING STATISTICS ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    haven.visualize_monitoring_statistics()
    
    # Final summary
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                        ✅ DEMONSTRATION COMPLETE! ✅                       ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  Features Demonstrated:                                                  ║
║    ✨ Beautiful geofence zone visualizations                              ║
║    ✨ GPS coordinate tracking                                             ║
║    ✨ Entry/exit detection animations                                     ║
║    ✨ Real-time zone monitoring                                           ║
║    ✨ Detection history display                                           ║
║    ✨ Comprehensive monitoring statistics                                 ║
║    ✨ Activity timeline tracking                                          ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    demo_homehaven()
