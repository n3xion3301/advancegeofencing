#!/usr/bin/env python3
"""
Enhanced Portal System
Create and manage interdimensional portals
"""
import numpy as np
from qiskit import QuantumCircuit
from aer_simulator import AerSimulator
import time
from datetime import datetime

class PortalSystem:
    def __init__(self):
        print("🌀 INTERDIMENSIONAL PORTAL SYSTEM")
        print("="*70)
        print("Create stable wormholes between locations")
        print("="*70)
    
    def create_portal(self, destination="Astral Plane", stability=0.8):
        """Create interdimensional portal"""
        
        print(f"\n📊 PORTAL PARAMETERS:")
        print(f"   Destination: {destination}")
        print(f"   Stability: {stability*100:.0f}%")
        print(f"   Creation Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"   Portal Type: Quantum Wormhole")
        
        print("\n🎨 PORTAL STRUCTURE:")
        self.draw_portal()
    
    def draw_portal(self):
        """Draw portal visualization"""
        print()
        print("   PORTAL FORMATION:")
        print("   ═════════════════")
        print()
        print("        ╱╲")
        print("       ╱  ╲")
        print("      ╱ ⚡ ╲  ← Energy Ring")
        print("     ╱  ╱╲  ╲")
        print("    ╱  ╱🌀╲  ╲ ← Vortex Core")
        print("   ╱  ╱────╲  ╲")
        print("  ╱  ╱ GATE ╲  ╲ ← Stable Opening")
        print(" ╱  ╱────────╲  ╲")
        print("╱  ╱──────────╲  ╲")
        print("──────────────────")
        print()
        print("   Origin → 🌀 → Destination")
        print()
        print("   PORTAL LAYERS:")
        print("   • Event Horizon (outer)")
        print("   • Quantum Tunnel (middle)")
        print("   • Exit Point (inner)")
        print()
    
    def create_portal_circuit(self, stability):
        """Create quantum portal circuit"""
        qc = QuantumCircuit(4, 4)
        
        # Qubit 0: Origin point
        # Qubit 1: Tunnel stability
        # Qubit 2: Destination point
        # Qubit 3: Portal active
        
        qc.h(0)  # Origin superposition
        qc.h(2)  # Destination superposition
        
        # Create wormhole (entanglement)
        qc.cx(0, 2)
        
        # Stability control
        angle = stability * np.pi
        qc.ry(angle, 1)
        qc.cx(1, 3)
        
        # Link all components
        qc.cx(0, 1)
        qc.cx(2, 3)
        
        qc.measure(range(4), range(4))
        
        return qc
    
    def analyze_portal(self, counts, destination):
        """Analyze portal stability"""
        total = sum(counts.values())
        
        print("\n   State  | Count | Probability | Portal Status")
        print("   " + "─"*70)
        
        stable = 0
        unstable = 0
        
        for state, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            prob = count / total if total > 0 else 0
            bar = '█' * int(prob * 30)
            
            origin = state[0] == '1'
            stability = state[1] == '1'
            dest = state[2] == '1'
            active = state[3] == '1'
            
            if origin and stability and dest and active:
                status = "✅ STABLE - Portal fully open"
                stable += count
            elif origin and dest and active:
                status = "⚠️  UNSTABLE - Fluctuating"
                unstable += count
            elif active:
                status = "🌀 FORMING - Building tunnel"
                unstable += count
            else:
                status = "❌ COLLAPSED - Portal closed"
            
            print(f"   {state} | {count:4d}  | {prob:6.1%} {bar:30s} | {status}")
        
        stability_rate = (stable / total * 100) if total > 0 else 0
        
        print(f"\n   Portal Stability: {stability_rate:.1f}%")
        print(f"   Destination: {destination}")
        
        if stability_rate > 70:
            print("\n   ✅ PORTAL STABLE - Safe to traverse!")
            print("   🌀 Wormhole fully formed")
            print("   🚀 Ready for interdimensional travel")
        else:
            print("\n   ⚠️  PORTAL UNSTABLE - Do not enter!")
            print("   🔧 Increase energy input")
            print("   ⏳ Allow more formation time")

if __name__ == "__main__":
    system = PortalSystem()
    
    print("\n🚀 Creating interdimensional portal...")
    time.sleep(1)
    
    print("\n⚛️  QUANTUM PORTAL CIRCUIT:")
    qc = system.create_portal_circuit(stability=0.85)
    print(qc.draw(output='text'))
    
    print("\n⏳ Stabilizing portal...")
    time.sleep(1)
    
    sim = AerSimulator()
    result = sim.run(qc, shots=1000)
    counts = result.get_counts()
    
    print("\n📈 PORTAL ANALYSIS:")
    system.analyze_portal(counts, "Astral Plane")
    
    print("\n✅ Portal creation complete!")
