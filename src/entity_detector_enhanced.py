#!/usr/bin/env python3
"""
Enhanced Entity Detector
Detect and classify supernatural entities
"""
import numpy as np
from qiskit import QuantumCircuit
from aer_simulator import AerSimulator
import time
from datetime import datetime

class EntityDetector:
    def __init__(self):
        print("👻 SUPERNATURAL ENTITY DETECTOR")
        print("="*70)
        print("Quantum-based paranormal entity detection")
        print("="*70)
    
    def scan_area(self, radius=50, sensitivity=0.9):
        """Scan area for entities"""
        
        print(f"\n📊 SCAN PARAMETERS:")
        print(f"   Scan Radius: {radius} meters")
        print(f"   Sensitivity: {sensitivity*100:.0f}%")
        print(f"   Scan Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"   Detection Method: Quantum Field Analysis")
        
        print("\n🎨 ENTITY CLASSIFICATION:")
        self.draw_entity_types()
    
    def draw_entity_types(self):
        """Draw entity classification chart"""
        print()
        print("   ENTITY TYPES:")
        print("   ═════════════")
        print()
        print("   👻 GHOSTS/SPIRITS")
        print("      • Human consciousness remnants")
        print("      • Emotional imprints")
        print("      • Residual hauntings")
        print()
        print("   😈 NEGATIVE ENTITIES")
        print("      • Low-vibration beings")
        print("      • Energy vampires")
        print("      • Malevolent forces")
        print()
        print("   😇 POSITIVE ENTITIES")
        print("      • Spirit guides")
        print("      • Angels/Light beings")
        print("      • Protective forces")
        print()
        print("   👤 SHADOW PEOPLE")
        print("      • Interdimensional travelers")
        print("      • Dark silhouettes")
        print("      • Peripheral vision entities")
        print()
        print("   🌀 ELEMENTAL BEINGS")
        print("      • Nature spirits")
        print("      • Fae/Elementals")
        print("      • Energy constructs")
        print()
    
    def draw_detection_zones(self):
        """Draw detection zone map"""
        print()
        print("   DETECTION ZONES:")
        print("   ════════════════")
        print()
        print("        ┌─────────────────┐")
        print("        │   Zone 1: FAR   │")
        print("        │   👻 ← 50m      │")
        print("        ├─────────────────┤")
        print("        │   Zone 2: MID   │")
        print("        │   😈 ← 25m      │")
        print("        ├─────────────────┤")
        print("        │  Zone 3: NEAR   │")
        print("        │   🌀 ← 10m      │")
        print("        ├─────────────────┤")
        print("        │ Zone 4: CONTACT │")
        print("        │   ⚡ ← 1m       │")
        print("        └─────────────────┘")
        print("              🏠 YOU")
        print()
    
    def create_detection_circuit(self, sensitivity):
        """Create entity detection circuit"""
        qc = QuantumCircuit(4, 4)
        
        # Qubit 0: Entity presence
        # Qubit 1: Entity type
        # Qubit 2: Threat level
        # Qubit 3: Distance
        
        qc.h(0)  # Superposition
        
        angle = sensitivity * np.pi
        qc.ry(angle, 0)
        
        qc.cx(0, 1)  # Type detection
        qc.cx(0, 2)  # Threat assessment
        qc.cx(0, 3)  # Distance measurement
        
        qc.h(1)
        qc.h(2)
        
        qc.measure(range(4), range(4))
        
        return qc
    
    def analyze_detection(self, counts, sensitivity):
        """Analyze entity detection results"""
        total = sum(counts.values())
        
        print("\n   State  | Count | Probability | Detection Result")
        print("   " + "─"*70)
        
        entities_detected = 0
        
        for state, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            prob = count / total if total > 0 else 0
            bar = '█' * int(prob * 30)
            
            presence = state[0] == '1'
            entity_type = state[1] == '1'
            threat = state[2] == '1'
            distance = state[3] == '1'
            
            if presence and threat:
                result = "🚨 HOSTILE ENTITY - High threat!"
                entities_detected += count
            elif presence and entity_type:
                result = "👻 ENTITY DETECTED - Neutral"
                entities_detected += count
            elif presence:
                result = "😇 BENIGN PRESENCE - Friendly"
                entities_detected += count
            else:
                result = "✅ CLEAR - No entities"
            
            print(f"   {state} | {count:4d}  | {prob:6.1%} {bar:30s} | {result}")
        
        detection_rate = (entities_detected / total * 100) if total > 0 else 0
        
        print(f"\n   Entity Detection Rate: {detection_rate:.1f}%")
        
        if detection_rate > 50:
            print("\n   ⚠️  HIGH ENTITY ACTIVITY!")
            print("   🛡️  Recommend activating protection")
            print("   📡 Continue monitoring")
        elif detection_rate > 20:
            print("\n   👻 MODERATE ACTIVITY")
            print("   👁️  Stay alert")
            print("   🔮 Normal paranormal levels")
        else:
            print("\n   ✅ AREA CLEAR")
            print("   😊 Low entity presence")
            print("   🏠 Safe environment")

if __name__ == "__main__":
    detector = EntityDetector()
    
    print("\n🚀 Initializing entity scan...")
    time.sleep(1)
    
    detector.draw_detection_zones()
    
    print("\n⚛️  QUANTUM DETECTION CIRCUIT:")
    qc = detector.create_detection_circuit(sensitivity=0.9)
    print(qc.draw(output='text'))
    
    print("\n⏳ Scanning for entities...")
    time.sleep(1)
    
    sim = AerSimulator()
    result = sim.run(qc, shots=1000)
    counts = result.get_counts()
    
    print("\n📈 SCAN RESULTS:")
    detector.analyze_detection(counts, sensitivity=0.9)
    
    print("\n✅ Scan complete!")
