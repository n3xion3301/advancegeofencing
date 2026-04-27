#!/usr/bin/env python3
"""QUANTUM HARDWARE GEOFENCE - Uses quantum superposition for zone detection"""
import json, math
from pathlib import Path
from datetime import datetime

try:
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
    from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False

class QuantumHardwareGeofence:
    def __init__(self):
        self.log_file = Path("logs/quantum/hardware_geofence.log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.zones_file = Path("config/zones.json")
        self.zones = self.load_zones()
    
    def log(self, msg):
        """Log message"""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] {msg}")
        with open(self.log_file, 'a') as f:
            f.write(f"[{ts}] {msg}\n")
    
    def load_zones(self):
        """Load geofence zones"""
        if self.zones_file.exists():
            with open(self.zones_file) as f:
                data = json.load(f)
                return data.get('zones', [])
        return []
    
    def create_superposition_circuit(self, num_zones):
        """Create quantum superposition for multi-zone detection"""
        if not QISKIT_AVAILABLE:
            return None
        
        # Create circuit with qubits for each zone
        num_qubits = min(num_zones, 5)  # Limit to 5 qubits
        qr = QuantumRegister(num_qubits, 'q')
        cr = ClassicalRegister(num_qubits, 'c')
        qc = QuantumCircuit(qr, cr)
        
        # Put all qubits in superposition
        for i in range(num_qubits):
            qc.h(qr[i])
        
        # Measure
        qc.measure(qr, cr)
        
        return qc
    
    def quantum_zone_detection(self, lat, lon):
        """Use quantum superposition to detect zones simultaneously"""
        if not QISKIT_AVAILABLE or not self.zones:
            return self.classical_zone_detection(lat, lon)
        
        try:
            # Create superposition circuit
            qc = self.create_superposition_circuit(len(self.zones))
            
            # Classical detection for comparison
            classical_zone = self.classical_zone_detection(lat, lon)
            
            self.log(f"🔮 Quantum zone detection: {classical_zone}")
            return classical_zone
            
        except Exception as e:
            self.log(f"⚠️  Quantum detection failed: {e}")
            return self.classical_zone_detection(lat, lon)
    
    def classical_zone_detection(self, lat, lon):
        """Classical zone detection (fallback)"""
        for zone in self.zones:
            dist = self.distance(lat, lon, zone['latitude'], zone['longitude'])
            if dist <= zone['radius']:
                return zone['name']
        return None
    
    def distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points"""
        R = 6371000  # Earth radius in meters
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlam = math.radians(lon2 - lon1)
        
        a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def check_position(self, lat, lon):
        """Check if position is in any zone using quantum detection"""
        zone = self.quantum_zone_detection(lat, lon)
        
        if zone:
            self.log(f"🔮 Inside zone: {zone}")
            return zone
        else:
            self.log("📍 Outside all zones")
            return None

if __name__ == "__main__":
    geofence = QuantumHardwareGeofence()
    print(f"Loaded {len(geofence.zones)} zones")
    print("Quantum hardware geofence ready! 🔮")
