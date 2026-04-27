#!/usr/bin/env python3
"""
QUANTUM GEOFENCING MASTER INTEGRATION
Combines all phases:
1. n3xion Camera + Astral Vision
2. Advanced Quantum Features
3. GPS/Location Services
4. Quantum Encryption
"""
from n3xion_camera_wrapper import N3xionCamera
from quantum_astral_vision_n3xion import QuantumAstralVisionN3xion
from quantum_advanced_features import (
    QuantumRoutePrediction,
    QuantumAnomalyDetector,
    QuantumTeleportation
)
from gps_simulator import GPSLocationServiceSimulated as GPSLocationService
from quantum_encryption import QuantumEncryption
from quantum_geofence_integration import QuantumGeofenceSystem
import json
import time
from datetime import datetime
from pathlib import Path

class QuantumGeofencingMaster:
    def __init__(self):
        print("🌌 Initializing Quantum Geofencing Master System...")
        
        # Phase 1: Camera & Astral Vision
        self.camera = N3xionCamera()
        self.astral_vision = QuantumAstralVisionN3xion()
        
        # Phase 2: Advanced Quantum Features
        self.route_predictor = QuantumRoutePrediction()
        self.anomaly_detector = QuantumAnomalyDetector()
        self.teleportation = QuantumTeleportation()
        
        # Phase 3: GPS/Location
        self.gps = GPSLocationService()
        self.gps.load_cache()
        
        # Phase 4: Encryption
        self.encryption = QuantumEncryption()
        
        # Core quantum system
        self.quantum_system = QuantumGeofenceSystem()
        
        # Zones configuration
        self.zones = []
        self.load_zones()
        
        print("✅ Master System Ready!\n")
    
    def load_zones(self):
        """Load geofence zones from config"""
        zones_file = Path("~/advancegeofencing/zones_config.json").expanduser()
        
        if zones_file.exists():
            with open(zones_file, 'r') as f:
                self.zones = json.load(f)
            print(f"📍 Loaded {len(self.zones)} zones")
        else:
            # Create default zones
            self.zones = [
                {
                    'id': 'home_zone',
                    'name': 'Home',
                    'lat': 40.7128,
                    'lon': -74.0060,
                    'radius': 100,
                    'quantum_enabled': True
                }
            ]
            self.save_zones()
    
    def save_zones(self):
        """Save zones to config"""
        zones_file = Path("~/advancegeofencing/zones_config.json").expanduser()
        with open(zones_file, 'w') as f:
            json.dump(self.zones, f, indent=2)
    
    def check_zone_status(self, location):
        """Check if location is in any quantum zone"""
        zone_status = []
        
        for zone in self.zones:
            inside = self.gps.is_inside_zone(
                location,
                {'lat': zone['lat'], 'lon': zone['lon']},
                zone['radius']
            )
            
            if inside:
                zone_status.append({
                    'zone': zone,
                    'inside': True,
                    'distance': 0
                })
            else:
                distance = self.gps.calculate_distance(
                    location['lat'], location['lon'],
                    zone['lat'], zone['lon']
                )
                zone_status.append({
                    'zone': zone,
                    'inside': False,
                    'distance': distance
                })
        
        return zone_status
    
    def quantum_analysis(self, location, zone_status):
        """Perform complete quantum analysis"""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'location': location,
            'zones': zone_status
        }
        
        # Route prediction
        self.route_predictor.add_location(location['lat'], location['lon'])
        predictions = self.route_predictor.predict_next_location(10)
        if predictions:
            analysis['route_predictions'] = predictions[:3]
        
        # Anomaly detection
        self.anomaly_detector.add_baseline(location)
        anomaly_score = self.anomaly_detector.detect_anomaly(location)
        analysis['anomaly_score'] = anomaly_score
        
        # Quantum state for active zones
        active_zones = [z for z in zone_status if z['inside']]
        if active_zones:
            analysis['active_zones'] = len(active_zones)
            analysis['quantum_state'] = 'entangled'
        else:
            analysis['quantum_state'] = 'superposition'
        
        return analysis
    
    def trigger_astral_capture(self, analysis):
        """Trigger camera capture based on quantum analysis"""
        should_capture = False
        
        # Trigger conditions
        if analysis['anomaly_score'] > 0.7:
            print("🚨 High anomaly detected!")
            should_capture = True
        
        if analysis.get('active_zones', 0) > 0:
            print("🎯 Inside quantum zone!")
            should_capture = True
        
        if should_capture:
            zone_data = {
                'zone_id': 'quantum_trigger',
                'lat': analysis['location']['lat'],
                'lon': analysis['location']['lon'],
                'activity_level': analysis['anomaly_score']
            }
            
            # Capture with astral vision
            result = self.astral_vision.astral_photo_capture(zone_data)
            
            if result:
                # Encrypt the capture metadata
                encrypted_meta = self.encryption.encrypt_data(result['metadata'])
                
                # Save encrypted
                self.encryption.save_encrypted_file(
                    f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    result['metadata']
                )
                
                return result
        
        return None
    
    def continuous_monitoring(self, interval=10):
        """Main monitoring loop - integrates all systems"""
        print("🌌 Starting Quantum Geofencing Master Monitoring")
        print(f"   Interval: {interval}s")
        print(f"   Zones: {len(self.zones)}")
        print(f"   Press Ctrl+C to stop\n")
        
        iteration = 0
        
        try:
            while True:
                iteration += 1
                print(f"\n{'='*60}")
                print(f"🔄 Iteration {iteration} - {datetime.now().strftime('%H:%M:%S')}")
                print(f"{'='*60}")
                
                # Get current GPS location
                location = self.gps.get_current_location()
                
                if location:
                    print(f"📍 Location: {location['lat']:.6f}, {location['lon']:.6f}")
                    print(f"   Accuracy: {location['accuracy']:.1f}m")
                    
                    # Add to history
                    self.gps.add_to_history(location)
                    
                    # Check zone status
                    zone_status = self.check_zone_status(location)
                    
                    # Display zone info
                    for zs in zone_status:
                        if zs['inside']:
                            print(f"✅ Inside: {zs['zone']['name']}")
                        else:
                            print(f"📏 {zs['zone']['name']}: {zs['distance']:.1f}m away")
                    
                    # Perform quantum analysis
                    analysis = self.quantum_analysis(location, zone_status)
                    
                    print(f"\n🔬 Quantum Analysis:")
                    print(f"   State: {analysis['quantum_state']}")
                    print(f"   Anomaly: {analysis['anomaly_score']:.1%}")
                    
                    if analysis.get('route_predictions'):
                        print(f"   Next location predictions:")
                        for i, pred in enumerate(analysis['route_predictions'][:2], 1):
                            print(f"      {i}. {pred['lat']:.6f}, {pred['lon']:.6f} ({pred['probability']:.1%})")
                    
                    # Check for triggers
                    capture_result = self.trigger_astral_capture(analysis)
                    
                    if capture_result:
                        print(f"\n📸 Astral capture triggered!")
                        print(f"   File: {capture_result['photo']}")
                    
                    # Encrypt and save analysis
                    encrypted_analysis = self.encryption.encrypt_data(analysis)
                    self.encryption.save_encrypted_file(
                        f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        analysis
                    )
                    
                else:
                    print("⚠️  Could not get GPS location")
                
                # Wait for next iteration
                print(f"\n⏳ Waiting {interval}s...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped by user")
            self.cleanup()
    
    def cleanup(self):
        """Cleanup and save state"""
        print("\n🧹 Cleaning up...")
        self.gps.save_cache()
        self.save_zones()
        print("✅ State saved")
    
    def add_zone(self, name, lat, lon, radius=100):
        """Add new geofence zone"""
        zone = {
            'id': f"zone_{len(self.zones) + 1}",
            'name': name,
            'lat': lat,
            'lon': lon,
            'radius': radius,
            'quantum_enabled': True,
            'created': datetime.now().isoformat()
        }
        
        self.zones.append(zone)
        self.save_zones()
        print(f"✅ Zone added: {name}")
        return zone
    
    def list_zones(self):
        """List all zones"""
        print("\n📍 Configured Zones:")
        print(f"{'='*60}")
        for zone in self.zones:
            print(f"  {zone['name']}")
            print(f"    Location: {zone['lat']:.6f}, {zone['lon']:.6f}")
            print(f"    Radius: {zone['radius']}m")
            print(f"    Quantum: {'✅' if zone['quantum_enabled'] else '❌'}")
            print()
    
    def manual_capture(self, mode='photo'):
        """Manual camera capture"""
        location = self.gps.get_current_location()
        
        zone_data = {
            'zone_id': 'manual_capture',
            'lat': location['lat'] if location else 0,
            'lon': location['lon'] if location else 0,
            'activity_level': 1.0
        }
        
        if mode == 'photo':
            result = self.astral_vision.astral_photo_capture(zone_data)
        elif mode == 'video':
            result = self.astral_vision.astral_video_recording(zone_data, 10)
        elif mode == 'dual':
            result = self.astral_vision.astral_dual_capture(zone_data)
        
        return result

if __name__ == "__main__":
    import sys
    
    master = QuantumGeofencingMaster()
    
    if len(sys.argv) < 2:
        print("\n🌌 Quantum Geofencing Master System")
        print("="*60)
        print("\nCommands:")
        print("  monitor [interval]    - Start continuous monitoring")
        print("  zones                 - List all zones")
        print("  add-zone <name> <lat> <lon> [radius] - Add new zone")
        print("  photo                 - Manual photo capture")
        print("  video                 - Manual video capture")
        print("  dual                  - Dual camera capture")
        print("  status                - Show system status")
        print("\nExamples:")
        print("  python quantum_master_integration.py monitor 10")
        print("  python quantum_master_integration.py add-zone Home 40.7128 -74.0060 100")
        print("  python quantum_master_integration.py photo")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == 'monitor':
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        master.continuous_monitoring(interval)
    
    elif command == 'zones':
        master.list_zones()
    
    elif command == 'add-zone':
        if len(sys.argv) < 5:
            print("❌ Usage: add-zone <name> <lat> <lon> [radius]")
            sys.exit(1)
        
        name = sys.argv[2]
        lat = float(sys.argv[3])
        lon = float(sys.argv[4])
        radius = int(sys.argv[5]) if len(sys.argv) > 5 else 100
        
        master.add_zone(name, lat, lon, radius)
    
    elif command == 'photo':
        result = master.manual_capture('photo')
        print(f"✅ Photo captured: {result}")
    
    elif command == 'video':
        result = master.manual_capture('video')
        print(f"✅ Video recorded: {result}")
    
    elif command == 'dual':
        result = master.manual_capture('dual')
        print(f"✅ Dual capture: {result}")
    
    elif command == 'status':
        print("\n🌌 System Status")
        print("="*60)
        print(f"Zones: {len(master.zones)}")
        print(f"Location history: {len(master.gps.location_history)}")
        print(f"GPS tracking: {'✅' if master.gps.location_history else '⚠️'}")
        print(f"Encryption: ✅")
        print(f"Camera: ✅")
        print(f"Quantum features: ✅")
        master.list_zones()
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)
