# Quantum Computing Imports
import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_bloch_multivector

# Scientific Computing
import numpy as np
import scipy
from scipy import optimize

# Visualization
import matplotlib.pyplot as plt
import matplotlib

# Standard Library
import sys
import os
import json
from pathlib import Path
from datetime import datetime

import os
#!/usr/bin/env python3
"""
import os
Quantum Hardware Geofence System
Uses IBM Quantum Computing for secure location verification
"""
import os

import json
import os
import math
import subprocess
from datetime import datetime
class QuantumGeofence:
    def __init__(self):
        self.load_configs()
        self.service = None
        self.backend = None

    def load_configs(self):
        """Load IBM Quantum and geofence configurations"""
        with open(os.path.expanduser('~/advancegeofencing/config/ibm_quantum_config.json'), 'r') as f:
            self.ibm_config = json.load(f)

        with open(os.path.expanduser('~/advancegeofencing/config/geofence_config.json'), 'r') as f:
            self.geofence_config = json.load(f)

    def initialize_quantum_backend(self):
        """Initialize IBM Quantum backend"""
        try:
            self.service = QiskitRuntimeService(
                channel="ibm_quantum_platform",
                token=self.ibm_config['ibm_quantum_token'],
                instance=self.ibm_config['instance']
            )
            # Auto-select least busy backend
            self.backend = self.service.least_busy(
                operational=True,
                simulator=False,
                min_num_qubits=127
            )
            print(f"✅ Auto-selected: {self.backend.name} (least busy!)")
            return True
        except Exception as e:
            print(f"⚠️  Quantum backend unavailable: {e}")
            return False

    def get_current_location(self):
        """Get current GPS location using termux-location"""
        try:
            result = subprocess.run(
                ['termux-location', '-p', 'gps'],
                capture_output=True,
                text=True,
                timeout=30
            )
            location_data = json.loads(result.stdout)
            return {
                'latitude': location_data['latitude'],
                'longitude': location_data['longitude'],
                'accuracy': location_data.get('accuracy', 0)
            }
        except Exception as e:
            print(f"⚠️  Location unavailable: {e}")
            return None

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two GPS coordinates (Haversine formula)"""
        R = 6371000  # Earth radius in meters

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi/2)**2 + \
            math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R * c

    def is_inside_geofence(self, current_location):
        """Check if current location is inside geofence"""
        if not current_location:
            return False

        home = self.geofence_config['residence']['center']
        radius = self.geofence_config['residence']['radius_meters']

        distance = self.calculate_distance(
            current_location['latitude'],
            current_location['longitude'],
            home['latitude'],
            home['longitude']
        )

        return distance <= radius, distance

    def generate_quantum_random_number(self):
        """Generate quantum random number using superposition"""
        if not self.backend:
            # Fallback to classical random if quantum unavailable
            import random
            return random.randint(0, 255)

        try:
            # Create quantum circuit for random number generation
            qc = QuantumCircuit(8, 8)

            # Put all qubits in superposition
            for i in range(8):
                qc.h(i)

            # Measure all qubits
            qc.measure(range(8), range(8))

            # Transpile and run
            # Batch mode for free tier
            sampler = Sampler(mode=self.backend)
            transpiled = transpile(qc, self.backend, optimization_level=1)
            job = sampler.run([transpiled], shots=1)
            result = job.result(timeout=120)

            # Get measurement result
            # DEBUG: See what's in DataBin
                        # DEBUG output removed

            # Try to get counts
            try:
                # Get the first available measurement key from DataBin
                meas_key = list(result[0].data.keys())[0]
                counts = result[0].data[meas_key].get_counts()
            except AttributeError as e:
                print(f"Error with .meas: {e}")
                # Try alternative access
                for attr in dir(result[0].data):
                    if not attr.startswith('_'):
                        print(f"Trying .{attr}...")
                        try:
                            data = getattr(result[0].data, attr)
                            if hasattr(data, 'get_counts'):
                                counts = data.get_counts()
                                print(f"SUCCESS with .{attr}.get_counts()!")
                                break
                        except:
                            pass
            bitstring = list(counts.keys())[0]
            return int(bitstring, 2)

        except Exception as e:
            print(f"⚠️  Quantum RNG failed: {e}")
            import random
            return random.randint(0, 255)

    def detect_reality_shift(self):
        """Use quantum circuit to detect reality shifts"""
        if not self.backend:
            return {"shift_detected": False, "probability": 0}

        try:
            # Create quantum circuit for reality shift detection
            qc = QuantumCircuit(3, 3)

            # Create entangled state
            qc.h(0)
            qc.cx(0, 1)
            qc.cx(1, 2)

            # Add phase rotation based on location
            location = self.get_current_location()
            if location:
                phase = (location['latitude'] + location['longitude']) % (2 * math.pi)
                qc.rz(phase, 0)

            # Measure
            qc.measure(range(3), range(3))

            # Run on quantum hardware
            # Batch mode for free tier
            sampler = Sampler(mode=self.backend)
            transpiled = transpile(qc, self.backend, optimization_level=2)
            job = sampler.run([transpiled], shots=100)
            result = job.result(timeout=120)

            # DEBUG: See what's in DataBin
                        # DEBUG output removed

            # Try to get counts
            try:
                # Get the first available measurement key from DataBin
                meas_key = list(result[0].data.keys())[0]
                counts = result[0].data[meas_key].get_counts()
            except AttributeError as e:
                print(f"Error with .meas: {e}")
                # Try alternative access
                for attr in dir(result[0].data):
                    if not attr.startswith('_'):
                        print(f"Trying .{attr}...")
                        try:
                            data = getattr(result[0].data, attr)
                            if hasattr(data, 'get_counts'):
                                counts = data.get_counts()
                                print(f"SUCCESS with .{attr}.get_counts()!")
                                break
                        except:
                            pass

            # Analyze results for anomalies
            total_shots = sum(counts.values())
            max_count = max(counts.values())
            shift_probability = 1 - (max_count / total_shots)

            return {
                "shift_detected": shift_probability > 0.5,
                "probability": shift_probability * 100,
                "measurements": counts
            }

        except Exception as e:
            print(f"⚠️  Reality shift detection failed: {e}")
            return {"shift_detected": False, "probability": 0}

    def quantum_verify_location(self):
        """Quantum-enhanced location verification"""
        print("\n⚛️  QUANTUM GEOFENCE VERIFICATION")
        print("=" * 70)

        # Initialize quantum backend
        quantum_available = self.initialize_quantum_backend()

        if quantum_available:
            print(f"✅ Quantum Backend: {self.backend.name}")
        else:
            print("⚠️  Quantum Backend: Unavailable (using classical fallback)")

        # Get current location
        print("\n📍 Getting GPS location...")
        location = self.get_current_location()

        if not location:
            print("❌ Location unavailable")
            return False

        print(f"   Latitude: {location['latitude']:.6f}")
        print(f"   Longitude: {location['longitude']:.6f}")
        print(f"   Accuracy: ±{location['accuracy']:.1f}m")

        # Check geofence
        inside, distance = self.is_inside_geofence(location)

        home = self.geofence_config['residence']['center']
        radius = self.geofence_config['residence']['radius_meters']

        print(f"\n🏠 Home Geofence:")
        print(f"   Center: {home['latitude']:.6f}, {home['longitude']:.6f}")
        print(f"   Radius: {radius}m")
        print(f"   Distance: {distance:.1f}m")

        if inside:
            print(f"   Status: ✅ INSIDE GEOFENCE")
        else:
            print(f"   Status: ❌ OUTSIDE GEOFENCE ({distance - radius:.1f}m away)")

        # Quantum verification
        if quantum_available:
            print("\n⚛️  Quantum Verification:")

            # Generate quantum random number for authentication
            qrn = self.generate_quantum_random_number()
            print(f"   Quantum Auth Code: {qrn}")

            # Detect reality shifts
            print("\n🌀 Reality Shift Detection:")
            shift_data = self.detect_reality_shift()

            if shift_data['shift_detected']:
                print(f"   ⚠️  REALITY SHIFT DETECTED!")
                print(f"   Probability: {shift_data['probability']:.1f}%")
            else:
                print(f"   ✅ Reality Stable")
                print(f"   Coherence: {100 - shift_data['probability']:.1f}%")

        print("\n" + "=" * 70)

        return inside

    def monitor_geofence(self):
        """Continuous geofence monitoring"""
        print("\n🔄 Starting Quantum Geofence Monitoring...")
        print("Press Ctrl+C to stop\n")

        try:
            import time
            interval = self.geofence_config['monitoring']['check_interval_seconds']

            while True:
                self.quantum_verify_location()
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n\n✅ Monitoring stopped")

def main():
    """Main function"""
    qg = QuantumGeofence()

    print("\n⚛️  QUANTUM HARDWARE GEOFENCE SYSTEM")
    print("=" * 70)
    print("1 - 📍 Verify Location (Single Check)")
    print("2 - 🔄 Monitor Geofence (Continuous)")
    print("0 - 🚪 Exit")
    print("=" * 70)

    choice = input("\nChoose: ").strip()

    if choice == '1':
        qg.quantum_verify_location()
    elif choice == '2':
        qg.monitor_geofence()
    else:
        print("Exiting...")

if __name__ == "__main__":
    main()
