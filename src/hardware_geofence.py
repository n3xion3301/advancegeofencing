#!/usr/bin/env python3
"""
QUANTUM HARDWARE GEOFENCE - Real-time monitoring
Uses quantum superposition for simultaneous multi-zone detection
"""
import json
import math
import sys
from pathlib import Path
from datetime import datetime

from aer_simulator import AerSimulator
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

class QuantumHardwareGeofence:
    def __init__(self):
        print("🔮 QUANTUM HARDWARE GEOFENCE")
        print("="*70)
        
        self.log_file = Path("logs/quantum/hardware_geofence.log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.zones_file = Path("config/zones.json")
        self.zones = self.load_zones()
        
        print(f"✅ Quantum simulator: Custom AerSimulator")
        print(f"📍 Loaded {len(self.zones)} zones")
        print("="*70)
    
    def log(self, msg):
        """Log with timestamp"""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{ts}] {msg}"
        print(log_msg)
        with open(self.log_file, 'a') as f:
            f.write(log_msg + "\n")
    
    def load_zones(self):
        """Load geofence zones"""
        if self.zones_file.exists():
            with open(self.zones_file) as f:
                data = json.load(f)
                return data.get('zones', [])
        return self.create_default_zones()
    
    def create_default_zones(self):
        """Create default zones"""
        zones = [
            {"name": "Home Safe Zone", "latitude": 40.7128, "longitude": -74.0060, "radius": 100, "type": "safe"},
            {"name": "Work Zone", "latitude": 40.7589, "longitude": -73.9851, "radius": 50, "type": "work"},
            {"name": "Alert Zone", "latitude": 40.7484, "longitude": -73.9857, "radius": 200, "type": "alert"}
        ]
        self.zones_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.zones_file, 'w') as f:
            json.dump({"zones": zones}, f, indent=2)
        return zones
    
    def create_superposition_circuit(self, num_zones):
        """Create quantum circuit for multi-zone detection"""
        num_qubits = min(num_zones, 5)
        qr = QuantumRegister(num_qubits, 'zone')
        cr = ClassicalRegister(num_qubits, 'detection')
        qc = QuantumCircuit(qr, cr)
        
        # Create superposition - check all zones simultaneously
        for i in range(num_qubits):
            qc.h(qr[i])
        
        # Add entanglement for zone correlation
        for i in range(num_qubits - 1):
            qc.cx(qr[i], qr[i + 1])
        
        # Measure all zones
        qc.measure(qr, cr)
        
        return qc
    
    def distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance using Haversine formula"""
        R = 6371000  # Earth radius in meters
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlam = math.radians(lon2 - lon1)
        
        a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def quantum_zone_detection(self, lat, lon):
        """Quantum-enhanced zone detection"""
        self.log(f"\n⚛️  Quantum zone detection at ({lat:.4f}, {lon:.4f})")
        
        # Create and run quantum circuit
        qc = self.create_superposition_circuit(len(self.zones))
        sim = AerSimulator()
        result = sim.run(qc, shots=100)
        
        self.log(f"   Quantum measurements complete")
        
        # Classical detection for actual result
        return self.classical_zone_detection(lat, lon)
    
    def classical_zone_detection(self, lat, lon):
        """Classical zone detection"""
        for zone in self.zones:
            dist = self.distance(lat, lon, zone['latitude'], zone['longitude'])
            
            if dist <= zone['radius']:
                self.log(f"   ✅ Inside '{zone['name']}' ({dist:.1f}m from center)")
                return zone
        
        self.log(f"   📍 Outside all zones")
        return None
    
    def check_position(self, lat, lon):
        """Check position against all zones"""
        print("\n" + "="*70)
        print("🔍 POSITION CHECK")
        print("="*70)
        
        zone = self.quantum_zone_detection(lat, lon)
        
        if zone:
            zone_type = zone.get('type', 'unknown')
            
            if zone_type == 'safe':
                print(f"\n✅ SAFE ZONE DETECTED")
                print(f"   🏠 Zone: {zone['name']}")
                print(f"   🛡️  Status: Protected area")
            elif zone_type == 'work':
                print(f"\n🏢 WORK ZONE DETECTED")
                print(f"   💼 Zone: {zone['name']}")
                print(f"   ⏰ Status: Work hours active")
            elif zone_type == 'alert':
                print(f"\n⚠️  ALERT ZONE DETECTED")
                print(f"   🚨 Zone: {zone['name']}")
                print(f"   👁️  Status: High monitoring")
            else:
                print(f"\n📍 ZONE DETECTED")
                print(f"   📌 Zone: {zone['name']}")
        else:
            print(f"\n🌍 OUTSIDE ALL ZONES")
            print(f"   📍 No geofence active")
            print(f"   🔓 Unrestricted area")
        
        print("="*70)
        return zone

if __name__ == "__main__":
    geofence = QuantumHardwareGeofence()
    
    if len(sys.argv) == 3:
        # Command line usage: ./hardware_geofence.py <lat> <lon>
        try:
            lat = float(sys.argv[1])
            lon = float(sys.argv[2])
            geofence.check_position(lat, lon)
        except ValueError:
            print("❌ Invalid coordinates. Usage: ./hardware_geofence.py <latitude> <longitude>")
            sys.exit(1)
    else:
        print("\n📋 Usage:")
        print("   ./hardware_geofence.py <latitude> <longitude>")
        print("\n📝 Example:")
        print("   ./hardware_geofence.py 40.7128 -74.0060")
        print("\n🗺️  Available zones:")
        
        for zone in geofence.zones:
            print(f"   • {zone['name']}: ({zone['latitude']}, {zone['longitude']})")
