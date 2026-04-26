#!/usr/bin/env python3
"""
Enhanced Hawking Radiation Simulator
Visualizes black hole evaporation with detailed physics
"""
import numpy as np
from qiskit import QuantumCircuit
from aer_simulator import AerSimulator
import time

class HawkingRadiationVisualizer:
    def __init__(self):
        print("🌌 HAWKING RADIATION SIMULATOR")
        print("="*70)
        print("Simulating quantum effects near black hole event horizon")
        print("="*70)
    
    def visualize_black_hole(self, mass, time_step):
        """Visualize black hole with Hawking radiation"""
        
        # Calculate Schwarzschild radius
        G = 6.674e-11  # Gravitational constant
        c = 3e8        # Speed of light
        r_s = (2 * G * mass) / (c**2)
        
        # Hawking temperature
        hbar = 1.055e-34
        k_b = 1.381e-23
        T_H = (hbar * c**3) / (8 * np.pi * G * mass * k_b)
        
        print(f"\n📊 BLACK HOLE PROPERTIES:")
        print(f"   Mass: {mass:.2e} kg")
        print(f"   Schwarzschild Radius: {r_s:.2e} m")
        print(f"   Hawking Temperature: {T_H:.2e} K")
        print(f"   Evaporation Rate: {self.evaporation_rate(mass):.2e} kg/s")
        
        # ASCII visualization
        print("\n🎨 BLACK HOLE VISUALIZATION:")
        print()
        self.draw_black_hole(mass, time_step)
        
        # Quantum circuit for particle-antiparticle pair
        print("\n⚛️  QUANTUM PARTICLE PAIR CREATION:")
        qc = self.create_pair_circuit()
        
        # Simulate
        sim = AerSimulator()
        result = sim.run(qc, shots=1000)
        counts = result.get_counts()
        
        print("\n📈 MEASUREMENT RESULTS:")
        self.display_results(counts)
        
        return counts
    
    def draw_black_hole(self, mass, time_step):
        """Draw ASCII black hole with radiation"""
        size = min(20, max(5, int(np.log10(mass))))
        
        print("        Hawking Radiation ↑")
        print("              ✨ ✨ ✨")
        print("           ✨       ✨")
        print("         ✨           ✨")
        print("        ✨   Event    ✨")
        print("       ✨   Horizon   ✨")
        print("        ✨           ✨")
        print("         ✨         ✨")
        print("           ✨  ⚫  ✨")
        print("              ✨✨✨")
        print("         Singularity ↓")
        print()
        print("   Virtual Particle Pairs:")
        print("   ━━━━━━━━━━━━━━━━━━━━━━")
        print("   e⁺ ←→ e⁻  (created)")
        print("   e⁺ → ∞    (escapes)")
        print("   e⁻ → ⚫    (falls in)")
        print()
    
    def create_pair_circuit(self):
        """Create quantum circuit for particle pair"""
        qc = QuantumCircuit(2, 2)
        
        # Create entangled pair (particle-antiparticle)
        qc.h(0)
        qc.cx(0, 1)
        
        # One particle escapes (measure)
        qc.measure([0, 1], [0, 1])
        
        return qc
    
    def evaporation_rate(self, mass):
        """Calculate evaporation rate"""
        hbar = 1.055e-34
        c = 3e8
        G = 6.674e-11
        return (hbar * c**6) / (15360 * np.pi * G**2 * mass**2)
    
    def display_results(self, counts):
        """Display measurement results with physics interpretation"""
        total = sum(counts.values())
        
        print("\n   State  | Count | Probability | Interpretation")
        print("   " + "─"*60)
        
        interpretations = {
            '00': 'Both particles annihilated',
            '01': 'Antiparticle escaped, particle fell in',
            '10': 'Particle escaped, antiparticle fell in',
            '11': 'Both particles escaped (rare!)'
        }
        
        for state in ['00', '01', '10', '11']:
            count = counts.get(state, 0)
            prob = count / total if total > 0 else 0
            bar = '█' * int(prob * 40)
            interp = interpretations.get(state, 'Unknown')
            print(f"   |{state}⟩  | {count:4d}  | {prob:5.1%} {bar:40s} | {interp}")

if __name__ == "__main__":
    viz = HawkingRadiationVisualizer()
    
    # Simulate small black hole
    mass = 1e15  # kg (small black hole)
    
    print("\n🚀 Starting simulation...")
    time.sleep(1)
    
    viz.visualize_black_hole(mass, time_step=0)
    
    print("\n✅ Simulation complete!")
