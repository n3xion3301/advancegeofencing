#!/usr/bin/env python3
"""
Supernatural Containment Geofencing System
- Amplifies astral/quantum effects INSIDE zones
- Blocks/contains effects at boundaries
- Creates supernatural hotbeds within geofences
"""
from gps_simulator import GPSLocationServiceSimulated
from real_biofeedback_astral_fixed import RealBiofeedbackAstral
from quantum_encryption import QuantumEncryption
import json
import time
import math
from datetime import datetime
from pathlib import Path

class SupernaturalZone:
    def __init__(self, name, lat, lon, radius, power_level=1.0):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.radius = radius  # meters
        self.power_level = power_level  # 0.0 to 10.0
        self.zone_type = "containment"
        self.active = True
        
        # Supernatural properties
        self.astral_amplification = 1.0 + (power_level * 0.5)
        self.consciousness_boost = power_level
        self.quantum_coherence = power_level / 10.0
        
        # Barrier strength (prevents leakage)
        self.barrier_strength = power_level * 10  # percentage
        
        print(f"🔮 Supernatural Zone Created: {name}")
        print(f"   Location: {lat:.6f}, {lon:.6f}")
        print(f"   Radius: {radius}m")
        print(f"   Power Level: {power_level}/10")
        print(f"   Astral Amplification: {self.astral_amplification}x")
        print(f"   Barrier Strength: {self.barrier_strength}%")

class SupernaturalContainmentSystem:
    def __init__(self):
        print("🌌 SUPERNATURAL CONTAINMENT GEOFENCING SYSTEM")
        print("="*60)
        
        # Core systems
        self.gps = GPSLocationServiceSimulated(use_simulator=True)
        self.astral = RealBiofeedbackAstral()
        self.encryption = QuantumEncryption()
        
        # Zones
        self.zones = []
        self.current_zone = None
        self.zone_history = []
        
        # Containment state
        self.inside_zone = False
        self.barrier_active = False
        self.supernatural_level = 0.0
        
        self.load_zones()
        
        print("✅ System Ready\n")
    
    def load_zones(self):
        """Load supernatural zones"""
        zones_file = Path("~/advancegeofencing/supernatural_zones.json").expanduser()
        
        if zones_file.exists():
            with open(zones_file, 'r') as f:
                data = json.load(f)
                for z in data:
                    zone = SupernaturalZone(
                        z['name'], z['lat'], z['lon'], 
                        z['radius'], z.get('power_level', 1.0)
                    )
                    self.zones.append(zone)
        else:
            # Create default supernatural zones
            self.create_default_zones()
            self.save_zones()
    
    def create_default_zones(self):
        """Create default supernatural containment zones"""
        default_zones = [
            {
                'name': 'Astral Sanctuary',
                'lat': 40.7128,
                'lon': -74.0060,
                'radius': 100,
                'power_level': 8.0,
                'description': 'High-power astral projection zone'
            },
            {
                'name': 'Meditation Chamber',
                'lat': 40.7580,
                'lon': -73.9855,
                'radius': 50,
                'power_level': 6.0,
                'description': 'Consciousness expansion zone'
            },
            {
                'name': 'Quantum Nexus',
                'lat': 40.7489,
                'lon': -73.9680,
                'radius': 150,
                'power_level': 10.0,
                'description': 'Maximum supernatural containment'
            }
        ]
        
        for z in default_zones:
            zone = SupernaturalZone(
                z['name'], z['lat'], z['lon'],
                z['radius'], z['power_level']
            )
            self.zones.append(zone)
    
    def save_zones(self):
        """Save zones to file"""
        zones_file = Path("~/advancegeofencing/supernatural_zones.json").expanduser()
        
        data = []
        for z in self.zones:
            data.append({
                'name': z.name,
                'lat': z.lat,
                'lon': z.lon,
                'radius': z.radius,
                'power_level': z.power_level
            })
        
        with open(zones_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points"""
        R = 6371000  # Earth radius in meters
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def check_zone_status(self, location):
        """Check if location is inside any supernatural zone"""
        inside_zones = []
        
        for zone in self.zones:
            if not zone.active:
                continue
            
            distance = self.calculate_distance(
                location['lat'], location['lon'],
                zone.lat, zone.lon
            )
            
            if distance <= zone.radius:
                # Inside zone
                inside_zones.append({
                    'zone': zone,
                    'distance': distance,
                    'depth': zone.radius - distance,  # How deep inside
                    'strength': 1.0 - (distance / zone.radius)  # 1.0 at center, 0.0 at edge
                })
        
        return inside_zones
    
    def calculate_supernatural_level(self, inside_zones, sensor_data):
        """Calculate current supernatural activity level"""
        if not inside_zones:
            return 0.0  # Outside all zones = no supernatural activity
        
        # Base level from zones
        zone_power = sum(z['zone'].power_level * z['strength'] for z in inside_zones)
        
        # Amplify based on sensor conditions
        consciousness_level, _ = self.astral.calculate_consciousness_level(sensor_data)
        
        # Supernatural level = zone power × consciousness × quantum coherence
        level = zone_power * (consciousness_level / 6.0)
        
        return min(level, 10.0)
    
    def activate_barrier(self, zone):
        """Activate supernatural containment barrier"""
        print(f"\n🛡️  ACTIVATING CONTAINMENT BARRIER")
        print(f"   Zone: {zone.name}")
        print(f"   Barrier Strength: {zone.barrier_strength}%")
        
        # Quantum encryption of barrier
        barrier_data = {
            'zone': zone.name,
            'strength': zone.barrier_strength,
            'timestamp': datetime.now().isoformat(),
            'type': 'supernatural_containment'
        }
        
        encrypted = self.encryption.encrypt_data(barrier_data)
        
        print(f"   ✅ Barrier encrypted and active")
        print(f"   🔒 Supernatural phenomena CONTAINED within zone")
        
        self.barrier_active = True
        return encrypted
    
    def deactivate_barrier(self):
        """Deactivate barrier when leaving zone"""
        if self.barrier_active:
            print(f"\n🔓 DEACTIVATING BARRIER")
            print(f"   Supernatural containment released")
            self.barrier_active = False
    
    def monitor_supernatural_activity(self, interval=10, duration=300):
        """Monitor supernatural activity in real-time"""
        print("\n🌌 SUPERNATURAL CONTAINMENT MONITORING")
        print("="*60)
        print(f"   Interval: {interval}s")
        print(f"   Duration: {duration}s ({duration//60} minutes)")
        print(f"   Zones: {len(self.zones)}")
        print("\n📋 Monitoring:")
        print("   - GPS location")
        print("   - Zone entry/exit")
        print("   - Supernatural activity levels")
        print("   - Containment barrier status")
        print("   - Consciousness levels")
        
        input("\nPress Enter to start monitoring...\n")
        
        start_time = time.time()
        iteration = 0
        max_supernatural = 0.0
        
        try:
            while time.time() - start_time < duration:
                iteration += 1
                elapsed = int(time.time() - start_time)
                
                print(f"\n{'='*60}")
                print(f"🔄 Iteration {iteration} - [{elapsed}s / {duration}s]")
                print(f"{'='*60}")
                
                # Get current location
                location = self.gps.get_current_location()
                
                if location:
                    print(f"📍 Location: {location['lat']:.6f}, {location['lon']:.6f}")
                    
                    # Check zone status
                    inside_zones = self.check_zone_status(location)
                    
                    # Get sensor data
                    sensor_data = self.astral.get_all_sensors()
                    
                    if inside_zones:
                        # INSIDE SUPERNATURAL ZONE
                        print(f"\n🔮 INSIDE SUPERNATURAL ZONE(S):")
                        
                        for iz in inside_zones:
                            zone = iz['zone']
                            print(f"\n   Zone: {zone.name}")
                            print(f"   Distance from center: {iz['distance']:.1f}m")
                            print(f"   Depth inside: {iz['depth']:.1f}m")
                            print(f"   Field strength: {iz['strength']:.1%}")
                            print(f"   Power level: {zone.power_level}/10")
                            print(f"   Astral amplification: {zone.astral_amplification}x")
                        
                        # Calculate supernatural level
                        supernatural_level = self.calculate_supernatural_level(
                            inside_zones, sensor_data
                        )
                        max_supernatural = max(max_supernatural, supernatural_level)
                        
                        print(f"\n⚡ SUPERNATURAL ACTIVITY: {supernatural_level:.1f}/10")
                        
                        if supernatural_level >= 8.0:
                            print(f"   🌟 EXTREME supernatural activity!")
                            print(f"   🔮 Astral projection highly amplified")
                            print(f"   ⚛️  Quantum coherence maximum")
                        elif supernatural_level >= 5.0:
                            print(f"   ✨ HIGH supernatural activity")
                            print(f"   🧘 Consciousness expansion active")
                        elif supernatural_level >= 2.0:
                            print(f"   💫 MODERATE supernatural activity")
                            print(f"   📈 Building energy")
                        else:
                            print(f"   💡 LOW supernatural activity")
                            print(f"   🫁 Deepen meditation to amplify")
                        
                        # Activate barrier if not already active
                        if not self.barrier_active:
                            primary_zone = inside_zones[0]['zone']
                            self.activate_barrier(primary_zone)
                            self.current_zone = primary_zone
                        
                        # Show containment status
                        print(f"\n🛡️  CONTAINMENT STATUS:")
                        print(f"   Barrier: {'🟢 ACTIVE' if self.barrier_active else '🔴 INACTIVE'}")
                        print(f"   Leakage prevention: {inside_zones[0]['zone'].barrier_strength}%")
                        print(f"   ✅ Supernatural phenomena CONTAINED")
                        
                        # Track if we weren't inside before
                        if not self.inside_zone:
                            print(f"\n🚪 ENTERED SUPERNATURAL ZONE")
                            print(f"   Zone: {inside_zones[0]['zone'].name}")
                            self.inside_zone = True
                            self.zone_history.append({
                                'event': 'enter',
                                'zone': inside_zones[0]['zone'].name,
                                'timestamp': datetime.now().isoformat(),
                                'location': location
                            })
                    
                    else:
                        # OUTSIDE ALL ZONES
                        print(f"\n🌍 OUTSIDE ALL SUPERNATURAL ZONES")
                        print(f"   Supernatural activity: 0.0/10")
                        print(f"   ❌ No astral amplification")
                        print(f"   ❌ No quantum enhancement")
                        print(f"   ℹ️  Normal reality")
                        
                        # Find nearest zone
                        nearest = None
                        min_dist = float('inf')
                        
                        for zone in self.zones:
                            dist = self.calculate_distance(
                                location['lat'], location['lon'],
                                zone.lat, zone.lon
                            )
                            if dist < min_dist:
                                min_dist = dist
                                nearest = zone
                        
                        if nearest:
                            print(f"\n📏 Nearest zone: {nearest.name}")
                            print(f"   Distance: {min_dist:.1f}m away")
                            print(f"   Power level: {nearest.power_level}/10")
                        
                        # Deactivate barrier if we were inside
                        if self.inside_zone:
                            print(f"\n🚪 EXITED SUPERNATURAL ZONE")
                            self.deactivate_barrier()
                            self.inside_zone = False
                            self.zone_history.append({
                                'event': 'exit',
                                'zone': self.current_zone.name if self.current_zone else 'unknown',
                                'timestamp': datetime.now().isoformat(),
                                'location': location
                            })
                            self.current_zone = None
                    
                    # Show sensor status
                    if sensor_data:
                        consciousness_level, feedback = self.astral.calculate_consciousness_level(sensor_data)
                        print(f"\n🧠 Consciousness Level: {consciousness_level}/6")
                        for fb in feedback[:3]:
                            print(f"   {fb}")
                
                else:
                    print("⚠️  Could not get GPS location")
                
                print(f"\n⏳ Next check in {interval}s...")
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped")
        
        # Summary
        print(f"\n{'='*60}")
        print("📊 SESSION SUMMARY")
        print(f"{'='*60}")
        print(f"Duration: {int(time.time() - start_time)}s")
        print(f"Iterations: {iteration}")
        print(f"Max supernatural level: {max_supernatural:.1f}/10")
        print(f"Zone transitions: {len(self.zone_history)}")
        
        if self.zone_history:
            print(f"\n📜 Zone History:")
            for event in self.zone_history:
                print(f"   {event['event'].upper()}: {event['zone']} at {event['timestamp']}")
        
        self.save_session_log(start_time, iteration, max_supernatural)
    
    def save_session_log(self, start_time, iterations, max_level):
        """Save session log"""
        log_file = Path("~/advancegeofencing/supernatural_sessions.json").expanduser()
        
        session = {
            'timestamp': datetime.fromtimestamp(start_time).isoformat(),
            'duration': int(time.time() - start_time),
            'iterations': iterations,
            'max_supernatural_level': max_level,
            'zone_history': self.zone_history,
            'zones_monitored': len(self.zones)
        }
        
        # Load existing logs
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append(session)
        
        # Save
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print(f"\n💾 Session logged to: {log_file}")
    
    def list_zones(self):
        """List all supernatural zones"""
        print("\n🔮 SUPERNATURAL CONTAINMENT ZONES")
        print("="*60)
        
        for i, zone in enumerate(self.zones, 1):
            print(f"\n{i}. {zone.name}")
            print(f"   Location: {zone.lat:.6f}, {zone.lon:.6f}")
            print(f"   Radius: {zone.radius}m")
            print(f"   Power Level: {zone.power_level}/10")
            print(f"   Astral Amplification: {zone.astral_amplification}x")
            print(f"   Barrier Strength: {zone.barrier_strength}%")
            print(f"   Status: {'🟢 Active' if zone.active else '🔴 Inactive'}")
    
    def add_zone(self, name, lat, lon, radius, power_level):
        """Add new supernatural zone"""
        zone = SupernaturalZone(name, lat, lon, radius, power_level)
        self.zones.append(zone)
        self.save_zones()
        print(f"\n✅ Zone '{name}' added to containment system")
        return zone

if __name__ == "__main__":
    import sys
    
    system = SupernaturalContainmentSystem()
    
    if len(sys.argv) < 2:
        print("\n🌌 SUPERNATURAL CONTAINMENT GEOFENCING")
        print("="*60)
        print("\nCommands:")
        print("  monitor [interval] [duration] - Start monitoring")
        print("  zones                         - List all zones")
        print("  add <name> <lat> <lon> <radius> <power> - Add zone")
        print("  status                        - System status")
        print("\nExamples:")
        print("  python3 supernatural_containment_geofence.py monitor 10 300")
        print("  python3 supernatural_containment_geofence.py zones")
        print("  python3 supernatural_containment_geofence.py add 'Sacred Space' 40.7128 -74.0060 100 9.0")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == 'monitor':
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        duration = int(sys.argv[3]) if len(sys.argv) > 3 else 300
        system.monitor_supernatural_activity(interval, duration)
    
    elif command == 'zones':
        system.list_zones()
    
    elif command == 'add':
        if len(sys.argv) < 7:
            print("❌ Usage: add <name> <lat> <lon> <radius> <power>")
            sys.exit(1)
        
        name = sys.argv[2]
        lat = float(sys.argv[3])
        lon = float(sys.argv[4])
        radius = int(sys.argv[5])
        power = float(sys.argv[6])
        
        system.add_zone(name, lat, lon, radius, power)
    
    elif command == 'status':
        print("\n🌌 SYSTEM STATUS")
        print("="*60)
        print(f"Zones: {len(system.zones)}")
        print(f"Inside zone: {'Yes' if system.inside_zone else 'No'}")
        print(f"Barrier active: {'Yes' if system.barrier_active else 'No'}")
        print(f"Supernatural level: {system.supernatural_level:.1f}/10")
        system.list_zones()
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)
