#!/usr/bin/env python3
"""
Enhanced Quantum Entanglement Simulator
Visualizes "spooky action at a distance" and Bell states
"""
import numpy as np
from qiskit import QuantumCircuit
from aer_simulator import AerSimulator
import time

class QuantumEntanglementVisualizer:
    def __init__(self):
        print("🔗 QUANTUM ENTANGLEMENT SIMULATOR")
        print("="*70)
        print("Demonstrating Einstein's 'Spooky Action at a Distance'")
        print("="*70)
    
    def simulate_entanglement(self, bell_state='phi_plus'):
        """Simulate quantum entanglement"""
        
        bell_states = {
            'phi_plus': '|Φ⁺⟩ = (|00⟩ + |11⟩)/√2',
            'phi_minus': '|Φ⁻⟩ = (|00⟩ - |11⟩)/√2',
            'psi_plus': '|Ψ⁺⟩ = (|01⟩ + |10⟩)/√2',
            'psi_minus': '|Ψ⁻⟩ = (|01⟩ - |10⟩)/√2'
        }
        
        print(f"\n📊 ENTANGLEMENT PARAMETERS:")
        print(f"   Bell State: {bell_states[bell_state]}")
        print(f"   Particles: 2 (Alice & Bob)")
        print(f"   Separation: Arbitrary (even light-years!)")
        
        # Visualization before measurement
        print("\n🎨 ENTANGLED SYSTEM (Before Measurement):")
        self.draw_entangled_system()
        
        # Create Bell state circuit
        qc = self.create_bell_circuit(bell_state)
        
        print("\n⚛️  QUANTUM CIRCUIT:")
        print(qc.draw(output='text'))
        
        # Simulate
        print("\n⏳ Alice measures her particle...")
        time.sleep(1)
        
        sim = AerSimulator()
        result = sim.run(qc, shots=1000)
        counts = result.get_counts()
        
        # After measurement
        print("\n🎯 AFTER MEASUREMENT:")
        self.draw_measurement_results(counts)
        
        print("\n📈 CORRELATION ANALYSIS:")
        self.analyze_correlations(counts)
        
        return counts
    
    def draw_entangled_system(self):
        """Draw entangled particle system"""
        print()
        print("   Alice's Lab          Entangled Pair          Bob's Lab")
        print("   ═══════════          ═══════════════         ═══════════")
        print()
        print("       🔬                    ╱╲                     🔬")
        print("       │                    ╱  ╲                    │")
        print("       │                   ╱ ~~ ╲                   │")
        print("       ↓                  ╱  ⚛️  ╲                  ↓")
        print("      ⚛️ ←─────────────→ ╱   ↕️   ╲ ←─────────────→ ⚛️")
        print("    Particle A          ╱  LINKED  ╲            Particle B")
        print("                       ╱            ╲")
        print("                      ╱──────────────╲")
        print()
        print("   ✨ Particles are ENTANGLED!")
        print("   📡 Measuring A instantly affects B")
        print("   🚀 Faster than light? NO - no information transfer!")
        print()
    
    def draw_measurement_results(self, counts):
        """Draw measurement correlation"""
        print()
        print("   Alice Measures ↓         Correlation         ↓ Bob Measures")
        print("   ═══════════════          ═══════════          ═══════════════")
        print()
        
        # Check for perfect correlation
        has_00 = counts.get('00', 0) > 0
        has_11 = counts.get('11', 0) > 0
        has_01 = counts.get('01', 0) > 0
        has_10 = counts.get('10', 0) > 0
        
        if has_00 or has_11:
            print("   Alice: |0⟩ ────────→ ⚡ INSTANT ⚡ ────────→ Bob: |0⟩")
            print("                         CORRELATION")
            print("   Alice: |1⟩ ────────→ ⚡ INSTANT ⚡ ────────→ Bob: |1⟩")
            print()
            print("   ✅ PERFECT CORRELATION!")
            print("   📊 When Alice gets 0, Bob ALWAYS gets 0")
            print("   📊 When Alice gets 1, Bob ALWAYS gets 1")
        
        if has_01 or has_10:
            print("   Alice: |0⟩ ────────→ ⚡ INSTANT ⚡ ────────→ Bob: |1⟩")
            print("                         ANTI-CORRELATION")
            print("   Alice: |1⟩ ────────→ ⚡ INSTANT ⚡ ────────→ Bob: |0⟩")
            print()
            print("   ✅ PERFECT ANTI-CORRELATION!")
            print("   📊 When Alice gets 0, Bob ALWAYS gets 1")
            print("   📊 When Alice gets 1, Bob ALWAYS gets 0")
        
        print()
    
    def create_bell_circuit(self, bell_state):
        """Create Bell state circuit"""
        qc = QuantumCircuit(2, 2)
        
        if bell_state == 'phi_plus':
            # |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
            qc.h(0)
            qc.cx(0, 1)
        
        elif bell_state == 'phi_minus':
            # |Φ⁻⟩ = (|00⟩ - |11⟩)/√2
            qc.h(0)
            qc.z(0)
            qc.cx(0, 1)
        
        elif bell_state == 'psi_plus':
            # |Ψ⁺⟩ = (|01⟩ + |10⟩)/√2
            qc.h(0)
            qc.cx(0, 1)
            qc.x(1)
        
        elif bell_state == 'psi_minus':
            # |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2
            qc.h(0)
            qc.z(0)
            qc.cx(0, 1)
            qc.x(1)
        
        qc.measure([0, 1], [0, 1])
        
        return qc
    
    def analyze_correlations(self, counts):
        """Analyze quantum correlations"""
        total = sum(counts.values())
        
        print("\n   Outcome  | Count | Probability | Alice | Bob | Match?")
        print("   " + "─"*70)
        
        for state in ['00', '01', '10', '11']:
            count = counts.get(state, 0)
            prob = count / total if total > 0 else 0
            bar = '█' * int(prob * 30)
            
            alice = state[0]
            bob = state[1]
            match = "✅ SAME" if alice == bob else "❌ OPPOSITE"
            
            print(f"   |{state}⟩   | {count:4d}  | {prob:6.1%} {bar:30s} | {alice}     | {bob}   | {match}")
        
        # Calculate correlation coefficient
        same = counts.get('00', 0) + counts.get('11', 0)
        opposite = counts.get('01', 0) + counts.get('10', 0)
        
        correlation = (same - opposite) / total if total > 0 else 0
        
        print("\n   " + "─"*70)
        print(f"   Correlation Coefficient: {correlation:+.3f}")
        print(f"   Same outcomes: {same} ({same/total:.1%})")
        print(f"   Opposite outcomes: {opposite} ({opposite/total:.1%})")
        
        # Physics explanation
        print("\n💡 PHYSICS EXPLANATION:")
        print()
        print("   ENTANGLEMENT PROPERTIES:")
        print("   • Particles share quantum state")
        print("   • Cannot describe particles independently")
        print("   • Measurement on A affects B instantly")
        print("   • Distance doesn't matter!")
        print()
        print("   EINSTEIN'S OBJECTION:")
        print("   • Called it 'spooky action at a distance'")
        print("   • Thought quantum mechanics was incomplete")
        print("   • Proposed hidden variables")
        print()
        print("   BELL'S THEOREM (1964):")
        print("   • Proved no local hidden variables")
        print("   • Experiments confirm quantum mechanics")
        print("   • Entanglement is REAL!")
        print()
        print("   APPLICATIONS:")
        print("   • Quantum cryptography (unhackable)")
        print("   • Quantum teleportation")
        print("   • Quantum computing")
        print("   • Quantum networks")

if __name__ == "__main__":
    viz = QuantumEntanglementVisualizer()
    
    print("\n🚀 Starting entanglement simulation...")
    time.sleep(1)
    
    # Test all Bell states
    for state in ['phi_plus', 'psi_plus']:
        print("\n" + "="*70)
        viz.simulate_entanglement(bell_state=state)
        time.sleep(2)
    
    print("\n✅ Simulation complete!")
