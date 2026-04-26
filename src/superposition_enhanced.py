#!/usr/bin/env python3
"""
Enhanced Quantum Superposition Simulator
Visualizes Schrödinger's Cat and quantum states
"""
import numpy as np
from qiskit import QuantumCircuit
from aer_simulator import AerSimulator
import time

class QuantumSuperpositionVisualizer:
    def __init__(self):
        print("⚛️  QUANTUM SUPERPOSITION SIMULATOR")
        print("="*70)
        print("Demonstrating Schrödinger's Cat Paradox")
        print("="*70)
    
    def simulate_superposition(self):
        """Simulate quantum superposition"""
        
        print(f"\n📊 EXPERIMENT SETUP:")
        print(f"   System: Schrödinger's Cat")
        print(f"   States: |Alive⟩ and |Dead⟩")
        print(f"   Superposition: |ψ⟩ = (|Alive⟩ + |Dead⟩)/√2")
        
        # Before opening box
        print("\n🎨 BEFORE OBSERVATION (Box Closed):")
        self.draw_closed_box()
        
        # Create superposition circuit
        qc = self.create_cat_circuit()
        
        print("\n⚛️  QUANTUM CIRCUIT:")
        print(qc.draw(output='text'))
        
        # Simulate
        print("\n⏳ Opening the box (measuring)...")
        time.sleep(1)
        
        sim = AerSimulator()
        result = sim.run(qc, shots=1000)
        counts = result.get_counts()
        
        # After observation
        print("\n🎯 AFTER OBSERVATION (Box Opened):")
        self.draw_opened_box(counts)
        
        print("\n📈 MEASUREMENT RESULTS:")
        self.display_results(counts)
        
        return counts
    
    def draw_closed_box(self):
        """Draw Schrödinger's box before measurement"""
        print()
        print("   ┌─────────────────────────────────────┐")
        print("   │                                     │")
        print("   │    🐱 BOTH ALIVE AND DEAD! 💀       │")
        print("   │                                     │")
        print("   │         |ψ⟩ = α|Alive⟩ + β|Dead⟩   │")
        print("   │                                     │")
        print("   │    ╱╲    Superposition    ╱╲       │")
        print("   │   ╱  ╲    of States      ╱  ╲      │")
        print("   │  ╱ ~~ ╲                 ╱ ~~ ╲     │")
        print("   │ ╱  😺  ╲               ╱  💀  ╲    │")
        print("   │╱────────╲             ╱────────╲   │")
        print("   │  50%       +          50%          │")
        print("   │                                     │")
        print("   └─────────────────────────────────────┘")
        print()
        print("   ❓ Cat is BOTH alive AND dead")
        print("   🌊 Wave function not collapsed")
        print("   ⚛️  Quantum superposition!")
        print()
    
    def draw_opened_box(self, counts):
        """Draw box after measurement"""
        alive = counts.get('0', 0)
        dead = counts.get('1', 0)
        total = alive + dead
        
        alive_pct = alive / total * 100 if total > 0 else 0
        dead_pct = dead / total * 100 if total > 0 else 0
        
        print()
        print("   ┌─────────────────────────────────────┐")
        print("   │                                     │")
        print("   │    WAVE FUNCTION COLLAPSED!         │")
        print("   │                                     │")
        
        if alive > dead:
            print("   │           😺 ALIVE! 😺              │")
            print("   │                                     │")
            print("   │         ╱╲                          │")
            print("   │        ╱  ╲                         │")
            print("   │       ╱ 😺 ╲                        │")
            print("   │      ╱──────╲                       │")
        else:
            print("   │           💀 DEAD 💀                │")
            print("   │                                     │")
            print("   │         ╱╲                          │")
            print("   │        ╱  ╲                         │")
            print("   │       ╱ 💀 ╲                        │")
            print("   │      ╱──────╲                       │")
        
        print("   │                                     │")
        print(f"   │   Alive: {alive_pct:.1f}%  Dead: {dead_pct:.1f}%        │")
        print("   │                                     │")
        print("   └─────────────────────────────────────┘")
        print()
        print("   ✅ Observation forced definite state!")
        print("   🎲 Outcome was probabilistic")
        print()
    
    def create_cat_circuit(self):
        """Create Schrödinger's cat circuit"""
        qc = QuantumCircuit(1, 1)
        
        # Create superposition (cat is alive AND dead)
        qc.h(0)
        
        # Measure (open the box!)
        qc.measure(0, 0)
        
        return qc
    
    def display_results(self, counts):
        """Display measurement results"""
        total = sum(counts.values())
        
        print("\n   State | Count | Probability | Cat Status")
        print("   " + "─"*60)
        
        alive = counts.get('0', 0)
        dead = counts.get('1', 0)
        
        alive_prob = alive / total if total > 0 else 0
        dead_prob = dead / total if total > 0 else 0
        
        alive_bar = '█' * int(alive_prob * 40)
        dead_bar = '█' * int(dead_prob * 40)
        
        print(f"   |0⟩   | {alive:4d}  | {alive_prob:6.1%} {alive_bar:40s} | 😺 ALIVE")
        print(f"   |1⟩   | {dead:4d}  | {dead_prob:6.1%} {dead_bar:40s} | 💀 DEAD")
        
        print("\n💡 PHYSICS EXPLANATION:")
        print()
        print("   SUPERPOSITION PRINCIPLE:")
        print("   • Quantum system can be in multiple states")
        print("   • |ψ⟩ = α|0⟩ + β|1⟩ where |α|² + |β|² = 1")
        print("   • ALL states exist simultaneously!")
        print()
        print("   SCHRÖDINGER'S CAT PARADOX:")
        print("   • Thought experiment (1935)")
        print("   • Cat in box with quantum poison")
        print("   • Until observed, cat is BOTH alive AND dead")
        print("   • Highlights measurement problem")
        print()
        print("   INTERPRETATIONS:")
        print("   • Copenhagen: Wave function collapses")
        print("   • Many-Worlds: Both outcomes exist")
        print("   • Decoherence: Environment causes collapse")
        print()
        print("   REAL APPLICATIONS:")
        print("   • Quantum computing (qubits)")
        print("   • Quantum sensors")
        print("   • Quantum cryptography")

if __name__ == "__main__":
    viz = QuantumSuperpositionVisualizer()
    
    print("\n🚀 Starting superposition simulation...")
    time.sleep(1)
    
    viz.simulate_superposition()
    
    print("\n✅ Simulation complete!")
