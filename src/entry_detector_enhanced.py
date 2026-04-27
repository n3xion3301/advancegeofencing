#!/usr/bin/env python3
"""
ENHANCED DIRECTIONAL ENTRY DETECTOR
Advanced Entry Point Crossing Detection System

ENHANCEMENTS:
- Beautiful entry point visualizations
- Directional crossing animations
- Outside-to-inside transition displays
- Entry detection alerts
- Position history tracking
- Comprehensive entry analytics
- Real-time crossing monitoring
"""

import json
import time
import subprocess
from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

try:
    from geofence_monitor import GeofenceMonitor
    from android_location import AndroidLocationProvider
    LOCATION_AVAILABLE = True
except ImportError:
    LOCATION_AVAILABLE = False


class EntryDetectorEnhanced:
    """Enhanced Directional Entry Detector System"""
    
    def __init__(self):
        self.entry_points = self._load_entry_points()
        
        if LOCATION_AVAILABLE:
            self.location_provider = AndroidLocationProvider()
        
        self.position_history = []
        self.max_history = 10  # More history for better detection
        self.min_distance_outside = 1.0  # 1 meter minimum
        
        self.entry_events = []
        self.crossing_history = []
        
        self.log_dir = Path("logs/quantum")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self._print_banner()
    
    def _print_banner(self):
        """Print stunning entry detector banner with ASCII art"""
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║      ✧･ﾟ: *✧･ﾟ:* DIRECTIONAL ENTRY DETECTOR *:･ﾟ✧*:･ﾟ✧                 ║
║         Advanced Entry Point Crossing Detection System                   ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

                    ╔════════════════════════════════╗
                    ║                                ║
                    ║   🚪 ENTRY DETECTOR 🚪         ║
                    ║                                ║
                    ║    ┌────────────────────┐     ║
                    ║    │                    │     ║
                    ║    │   OUTSIDE          │     ║
                    ║    │                    │     ║
                    ║    │      📍 ──▶        │     ║
                    ║    │                    │     ║
                    ║    ├────────────────────┤     ║
                    ║    │    🚪 ENTRY 🚪     │     ║
                    ║    ├────────────────────┤     ║
                    ║    │                    │     ║
                    ║    │        ──▶ 📍      │     ║
                    ║    │                    │     ║
                    ║    │   INSIDE           │     ║
                    ║    │                    │     ║
                    ║    └────────────────────┘     ║
                    ║                                ║
                    ║  [●] MONITORING  [◉] ACTIVE   ║
                    ║                                ║
                    ╚════════════════════════════════╝

        ┌────────────────────────────────────────────────────┐
        │  🚪 DETECTOR SPECIFICATIONS                         │
        ├────────────────────────────────────────────────────┤
        │  • Entry Points: Loading...                        │
        │  • History Depth: 10 positions                     │
        │  • Min Distance: 1.0 meters                        │
        │  • Status: Initialized                             │
        └────────────────────────────────────────────────────┘
        """)
    
    def print_entry_point(self, entry_name, entry_data):
        """Print entry point visualization"""
        
        print(f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                      🚪 ENTRY POINT 🚪                                    ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
        """)
        
        print(f"║  Entry: {entry_name}".ljust(76) + "║")
        print(f"║  Description: {entry_data.get('description', 'Unknown')}".ljust(76) + "║")
        print("║" + " "*74 + "║")
        
        # Entry point visualization
        print("║  ┌──────────────────────────────────────────────────────────────┐".ljust(76) + "║")
        print("║  │                                                              │".ljust(76) + "║")
        print(f"║  │                    🚪 {entry_name} 🚪".ljust(76) + "║")
        print("║  │                                                              │".ljust(76) + "║")
        print("║  │                    OUTSIDE                                   │".ljust(76) + "║")
        print("║  │                       ↓                                      │".ljust(76) + "║")
        print("║  │                       ↓                                      │".ljust(76) + "║")
        print("║  │                  ┌─────────┐                                 │".ljust(76) + "║")
        print("║  │                  │  🚪 🚪  │                                 │".ljust(76) + "║")
        print("║  │                  │ ENTRY  │                                  │".ljust(76) + "║")
        print("║  │                  │  POINT │                                  │".ljust(76) + "║")
        print("║  │                  └─────────┘                                 │".ljust(76) + "║")
        print("║  │                       ↓                                      │".ljust(76) + "║")
        print("║  │                       ↓                                      │".ljust(76) + "║")
        print("║  │                    INSIDE                                    │".ljust(76) + "║")
        print("║  │                                                              │".ljust(76) + "║")
        print("║  └──────────────────────────────────────────────────────────────┘".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")
    
    def print_crossing_animation(self, direction):
        """Print crossing animation"""
        
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                      🚪 CROSSING DETECTED! 🚪                             ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
        """)
        
        print(f"║  Direction: {direction}".ljust(76) + "║")
        print("║" + " "*74 + "║")
        
        # Crossing animation
        print("║  ┌──────────────────────────────────────────────────────────────┐".ljust(76) + "║")
        print("║  │                                                              │".ljust(76) + "║")
        
        if direction == "ENTERING":
            print("║  │                    ⚠️  ENTRY! ⚠️                              │".ljust(76) + "║")
            print("║  │                                                              │".ljust(76) + "║")
            print("║  │                    OUTSIDE                                   │".ljust(76) + "║")
            print("║  │                       📍                                     │".ljust(76) + "║")
            print("║  │                       │                                      │".ljust(76) + "║")
            print("║  │                       ↓                                      │".ljust(76) + "║")
            print("║  │                  ┌─────────┐                                 │".ljust(76) + "║")
            print("║  │                  │  🚪 🚪  │                                 │".ljust(76) + "║")
            print("║  │                  │ ENTRY  │                                  │".ljust(76) + "║")
            print("║  │                  └─────────┘                                 │".ljust(76) + "║")
            print("║  │                       ↓                                      │".ljust(76) + "║")
            print("║  │                       │                                      │".ljust(76) + "║")
            print("║  │                       📍                                     │".ljust(76) + "║")
            print("║  │                    INSIDE                                    │".ljust(76) + "║")
        else:
            print("║  │                    ⚠️  EXIT! ⚠️                               │".ljust(76) + "║")
            print("║  │                                                              │".ljust(76) + "║")
            print("║  │                    INSIDE                                    │".ljust(76) + "║")
            print("║  │                       📍                                     │".ljust(76) + "║")
            print("║  │                       │                                      │".ljust(76) + "║")
            print("║  │                       ↑                                      │".ljust(76) + "║")
            print("║  │                  ┌─────────┐                                 │".ljust(76) + "║")
            print("║  │                  │  🚪 🚪  │                                 │".ljust(76) + "║")
            print("║  │                  │ ENTRY  │                                  │".ljust(76) + "║")
            print("║  │                  └─────────┘                                 │".ljust(76) + "║")
            print("║  │                       ↑                                      │".ljust(76) + "║")
            print("║  │                       │                                      │".ljust(76) + "║")
            print("║  │                       📍                                     │".ljust(76) + "║")
            print("║  │                    OUTSIDE                                   │".ljust(76) + "║")
        
        print("║  │                                                              │".ljust(76) + "║")
        print("║  └──────────────────────────────────────────────────────────────┘".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")
    
    def _load_entry_points(self):
        """Load entry point zones"""
        config_file = Path("config/entity_zones.json")
        
        if not config_file.exists():
            # Create default entry points
            default_points = {
                "front_door": {
                    "lat": 37.7749,
                    "lon": -122.4194,
                    "radius": 2.0,
                    "description": "Front Door Entry"
                },
                "back_door": {
                    "lat": 37.7750,
                    "lon": -122.4195,
                    "radius": 2.0,
                    "description": "Back Door Entry"
                }
            }
            
            return default_points
        
        # Load existing entry points
        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except Exception:
            return {}
    
    def log(self, msg):
        """Log message with timestamp"""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{ts}] {msg}"
        print(formatted)
        
        try:
            log_file = self.log_dir / "entry_detector.log"
            with open(log_file, 'a') as f:
                f.write(formatted + "\n")
        except Exception:
            pass
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points"""
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371000  # Earth radius in meters
        
        lat1_rad = radians(lat1)
        lat2_rad = radians(lat2)
        delta_lat = radians(lat2 - lat1)
        delta_lon = radians(lon2 - lon1)
        
        a = sin(delta_lat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        
        return distance
    
    def detect_crossing(self, lat, lon):
        """Detect if crossing an entry point"""
        
        # Add current position to history
        self.position_history.append({
            'lat': lat,
            'lon': lon,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only recent history
        if len(self.position_history) > self.max_history:
            self.position_history.pop(0)
        
        # Need at least 2 positions to detect crossing
        if len(self.position_history) < 2:
            return None
        
        # Check each entry point
        for entry_name, entry_data in self.entry_points.items():
            entry_lat = entry_data['lat']
            entry_lon = entry_data['lon']
            radius = entry_data.get('radius', 2.0)
            
            # Get previous and current distances
            prev_pos = self.position_history[-2]
            curr_pos = self.position_history[-1]
            
            prev_dist = self.calculate_distance(
                prev_pos['lat'], prev_pos['lon'],
                entry_lat, entry_lon
            )
            
            curr_dist = self.calculate_distance(
                curr_pos['lat'], curr_pos['lon'],
                entry_lat, entry_lon
            )
            
            # Detect crossing
            if prev_dist > radius and curr_dist <= radius:
                # Entering
                return {
                    'entry': entry_name,
                    'direction': 'ENTERING',
                    'data': entry_data
                }
            elif prev_dist <= radius and curr_dist > radius:
                # Exiting
                return {
                    'entry': entry_name,
                    'direction': 'EXITING',
                    'data': entry_data
                }
        
        return None
    
    def monitor_position(self, lat, lon):
        """Monitor position for entry detection"""
        
        crossing = self.detect_crossing(lat, lon)
        
        if crossing:
            entry_name = crossing['entry']
            direction = crossing['direction']
            entry_data = crossing['data']
            
            # Show crossing animation
            self.print_crossing_animation(direction)
            
            # Send notification
            self.send_notification(entry_name, direction, entry_data)
            
            # Record event
            event = {
                'entry': entry_name,
                'direction': direction,
                'timestamp': datetime.now().isoformat()
            }
            self.entry_events.append(event)
            self.crossing_history.append(event)
            
            self.log(f"🚪 {direction}: {entry_name}")
            
            return crossing
        
        return None
    
    def send_notification(self, entry_name, direction, entry_data):
        """Send entry detection notification"""
        
        print(f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                      📢 NOTIFICATION 📢                                   ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
        """)
        
        print(f"║  Entry: {entry_name}".ljust(76) + "║")
        print(f"║  Direction: {direction}".ljust(76) + "║")
        print("║" + " "*74 + "║")
        
        # Notification visualization
        print("║  ┌──────────────────────────────────────────────────────────────┐".ljust(76) + "║")
        print("║  │                                                              │".ljust(76) + "║")
        print("║  │                    🔔 ALERT! 🔔                               │".ljust(76) + "║")
        print("║  │                                                              │".ljust(76) + "║")
        
        if direction == "ENTERING":
            print(f"║  │              Entering: {entry_name}".ljust(76) + "║")
            print("║  │                                                              │".ljust(76) + "║")
            print("║  │                      📍 ──▶ 🚪                                │".ljust(76) + "║")
        else:
            print(f"║  │              Exiting: {entry_name}".ljust(76) + "║")
            print("║  │                                                              │".ljust(76) + "║")
            print("║  │                      🚪 ──▶ 📍                                │".ljust(76) + "║")
        
        print("║  │                                                              │".ljust(76) + "║")
        print(f"║  │              {entry_data.get('description', '')}".ljust(76) + "║")
        print("║  │                                                              │".ljust(76) + "║")
        print("║  └──────────────────────────────────────────────────────────────┘".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")
        
        self.log(f"📢 Notification: {direction} {entry_name}")
    
    def display_entry_points(self):
        """Display all entry points"""
        
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                      🗺️  ENTRY POINTS MAP 🗺️                             ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
        """)
        
        print(f"║  Total Entry Points: {len(self.entry_points)}".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")
        
        for entry_name, entry_data in self.entry_points.items():
            self.print_entry_point(entry_name, entry_data)
    
    def display_crossing_history(self):
        """Display crossing history"""
        
        if not self.crossing_history:
            print("\n⚠️  No crossings yet")
            return
        
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                    📚 CROSSING HISTORY 📚                                 ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
        """)
        
        print(f"║  Total Crossings: {len(self.crossing_history)}".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")
        
        for i, crossing in enumerate(self.crossing_history[-5:], 1):
            entry = crossing['entry']
            direction = crossing['direction']
            
            arrow = "──▶" if direction == "ENTERING" else "◀──"
            
            print(f"""
┌────────────────────────────────────────────────────────────────────────┐
│  🚪 CROSSING #{i}                                                       │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Entry: {entry}                                                        │
│  Direction: {direction}                                                │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────┐     │
│  │                                                              │     │
│  │    📍 {arrow} 🚪                                              │     │
│  │                                                              │     │
│  │    {direction}                                               │     │
│  │                                                              │     │
│  └──────────────────────────────────────────────────────────────┘     │
│                                                                        │
│  Status: ✅ RECORDED                                                    │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
            """)
    
    def visualize_statistics(self):
        """Visualize entry statistics"""
        
        if not self.entry_events:
            print("\n⚠️  No statistics available yet")
            return
        
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                      📊 ENTRY STATISTICS 📊                               ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
        """)
        
        total_events = len(self.entry_events)
        entries = sum(1 for e in self.entry_events if e['direction'] == 'ENTERING')
        exits = sum(1 for e in self.entry_events if e['direction'] == 'EXITING')
        
        print(f"║  Total Events: {total_events}".ljust(76) + "║")
        print(f"║  Entries: {entries}".ljust(76) + "║")
        print(f"║  Exits: {exits}".ljust(76) + "║")
        print("║" + " "*74 + "║")
        
        # Direction distribution
        print("║  📊 Direction Distribution:".ljust(76) + "║")
        print("║" + " "*74 + "║")
        
        if entries > 0:
            bar_len = int((entries / total_events) * 40)
            bar = "█" * bar_len + "░" * (40 - bar_len)
            print(f"║  ENTERING    │{bar}│ {entries}".ljust(76) + "║")
        
        if exits > 0:
            bar_len = int((exits / total_events) * 40)
            bar = "█" * bar_len + "░" * (40 - bar_len)
            print(f"║  EXITING     │{bar}│ {exits}".ljust(76) + "║")
        
        print("║" + " "*74 + "║")
        
        # Crossing timeline
        print("║  🚪 Crossing Timeline:".ljust(76) + "║")
        print("║" + " "*74 + "║")
        
        timeline = "  "
        for event in self.entry_events[-20:]:
            timeline += "▶" if event['direction'] == 'ENTERING' else "◀"
        
        print(f"║{timeline}".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")


def demo_entry_detector():
    """Demonstration of Entry Detector"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║══════════════════════════════════════════════════════════════════════════║
║              🚪 DIRECTIONAL ENTRY DETECTOR DEMONSTRATION 🚪               ║
║══════════════════════════════════════════════════════════════════════════║
╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize
    detector = EntryDetectorEnhanced()
    
    # Test 1: Display entry points
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 1: DISPLAY ENTRY POINTS ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    detector.display_entry_points()
    
    # Test 2: Simulate entry crossing
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 2: CROSS FRONT DOOR (ENTERING) ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    # Outside position
    detector.monitor_position(37.7748, -122.4193)
    # Inside position
    detector.monitor_position(37.7749, -122.4194)
    
    # Test 3: Simulate exit crossing
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 3: CROSS BACK DOOR (EXITING) ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    # Inside position
    detector.monitor_position(37.7750, -122.4195)
    # Outside position
    detector.monitor_position(37.7751, -122.4196)
    
    # Test 4: Crossing history
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 4: CROSSING HISTORY ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    detector.display_crossing_history()
    
    # Test 5: Statistics
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 5: ENTRY STATISTICS ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    detector.visualize_statistics()
    
    # Final summary
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                        ✅ DEMONSTRATION COMPLETE! ✅                       ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  Features Demonstrated:                                                  ║
║    ✨ Beautiful entry point visualizations                                ║
║    ✨ Directional crossing animations                                     ║
║    ✨ Entry/exit detection alerts                                         ║
║    ✨ Position history tracking                                           ║
║    ✨ Crossing history displays                                           ║
║    ✨ Comprehensive entry statistics                                      ║
║                                                                          ║
║  Key Insight:                                                            ║
║    Directional entry detection tracks when entities cross from           ║
║    outside to inside (or vice versa) through entry points. This          ║
║    enables precise monitoring of boundary crossings!                     ║
║                                                                          ║
║  Real-World Applications:                                                ║
║    • Building access monitoring                                          ║
║    • Security zone tracking                                              ║
║    • Room entry/exit detection                                           ║
║    • Directional flow analysis                                           ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    demo_entry_detector()
