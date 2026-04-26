#!/usr/bin/env python3
"""
Enhanced Time Dilation Simulator
Visualizes Einstein's relativity and time warping
"""
import numpy as np
from qiskit import QuantumCircuit
from aer_simulator import AerSimulator
import time

class TimeDilationVisualizer:
    def __init__(self):
        print("⏰ TIME DILATION SIMULATOR")
        print("="*70)
        print("Einstein's Relativity: Time is NOT absolute!")
        print("="*70)
    
    def simulate_time_dilation(self, velocity_fraction=0.9):
        """Simulate relativistic time dilation"""
        
        c = 299792458  # Speed of light (m/s)
        v = velocity_fraction * c
        
        # Calculate Lorentz factor
        gamma = 1 / np.sqrt(1 - (v/c)**2)
        
        print(f"\n📊 RELATIVITY PARAMETERS:")
        print(f"   Velocity: {velocity_fraction:.1%} speed of light")
        print(f"   v = {v:.2e} m/s")
        print(f"   Lorentz Factor (γ): {gamma:.3f}")
        print(f"   Time Dilation: {gamma:.3f}x slower")
        
        # Visualization
        print("\n🎨 TIME DILATION VISUALIZATION:")
        self.draw_time_dilation(gamma, velocity_fraction)
        
        # Twin paradox
        print("\n👥 TWIN PARADOX:")
        self.draw_twin_paradox(gamma)
        
        # Quantum simulation
        print("\n⚛️  QUANTUM TIME SIMULATION:")
        qc = self.create_time_circuit(gamma)
        
        print(qc.draw(output='text'))
        
        # Simulate
        print("\n⏳ Simulating relativistic time...")
        time.sleep(1)
        
        sim = AerSimulator()
        result = sim.run(qc, shots=1000)
        counts = result.get_counts()
        
        print("\n📈 TIME MEASUREMENT RESULTS:")
        self.display_results(counts, gamma)
        
        return counts
    
    def draw_time_dilation(self, gamma, v_frac):
        """Draw time dilation effect"""
        print()
        print("   Stationary Observer          Moving Observer")
        print("   ═══════════════════          ═══════════════")
        print()
        
        # Draw clocks
        stationary_ticks = 10
        moving_ticks = int(stationary_ticks / gamma)
        
        print("   Earth Time:                  Spaceship Time:")
        print()
        print("      🕐 → 🕑 → 🕒                  🕐 → 🕑")
        print(f"      {stationary_ticks} seconds                      {moving_ticks} seconds")
        print()
        print(f"   Speed: 0% c                  Speed: {v_frac*100:.0f}% c")
        print("   Time: NORMAL ✓               Time: SLOWER! ⏱️")
        print()
        
        # Visual representation
        print("   Time Flow:")
        print("   ─────────────────────────────────────────")
        print(f"   Earth:     {'━' * stationary_ticks}")
        print(f"   Spaceship: {'━' * moving_ticks}")
        print("   ─────────────────────────────────────────")
        print()
        print(f"   ⚡ Time moves {gamma:.2f}x SLOWER on spaceship!")
        print()
    
    def draw_twin_paradox(self, gamma):
        """Draw twin paradox scenario"""
        print()
        print("   TWIN PARADOX SCENARIO:")
        print("   ═════════════════════")
        print()
        print("   Year 0: Twins are same age (25 years old)")
        print()
        print("      👨 Alice (Earth)        👨 Bob (Spaceship)")
        print("      Age: 25                Age: 25")
        print()
        print("   ↓ Bob travels at 90% speed of light for 10 years")
        print()
        print("   Year 10 (Earth time):")
        print()
        
        earth_age = 25 + 10
        ship_age = 25 + (10 / gamma)
        
        print(f"      👵 Alice (Earth)        👨 Bob (Returns)")
        print(f"      Age: {earth_age:.0f}                Age: {ship_age:.1f}")
        print()
        print(f"   🎯 Bob aged only {10/gamma:.1f} years!")
        print(f"   ⏰ Alice aged {10:.0f} years!")
        print(f"   📊 Age difference: {earth_age - ship_age:.1f} years")
        print()
    
    def create_time_circuit(self, gamma):
        """Create quantum circuit representing time dilation"""
        qc = QuantumCircuit(3, 3)
        
        # Qubit 0: Reference frame (0=stationary, 1=moving)
        # Qubit 1: Time tick 1
        # Qubit 2: Time tick 2
        
        # Create superposition of reference frames
        qc.h(0)
        
        # Time evolution depends on reference frame
        # Stationary frame: both ticks happen
        qc.x(0)
        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.x(0)
        
        # Moving frame: fewer ticks (time dilation)
        angle = np.pi / gamma
        qc.ry(angle, 1)
        qc.ry(angle, 2)
        
        qc.measure([0, 1, 2], [0, 1, 2])
        
        return qc
    
    def display_results(self, counts, gamma):
        """Display time dilation results"""
        total = sum(counts.values())
        
        print("\n   State | Count | Probability | Interpretation")
        print("   " + "─"*70)
        
        for state in sorted(counts.keys()):
            count = counts[state]
            prob = count / total if total > 0 else 0
            bar = '█' * int(prob * 30)
            
            # Interpret state
            frame = "Moving" if state[0] == '1' else "Stationary"
            ticks = state[1:].count('1')
            
            interp = f"{frame} frame: {ticks} time ticks"
            
            print(f"   {state}  | {count:4d}  | {prob:6.1%} {bar:30s} | {interp}")
        
        print("\n💡 PHYSICS EXPLANATION:")
        print()
        print("   SPECIAL RELATIVITY:")
        print("   • Time is relative, not absolute")
        print("   • Moving clocks run slower")
        print("   • Lorentz factor: γ = 1/√(1-v²/c²)")
        print("   • Time dilation: Δt' = γΔt")
        print()
        print("   EXPERIMENTAL EVIDENCE:")
        print("   • Muon decay experiments ✓")
        print("   • GPS satellites (need correction) ✓")
        print("   • Particle accelerators ✓")
        print("   • Atomic clocks on planes ✓")
        print()
        print("   CONSEQUENCES:")
        print("   • Twin paradox")
        print("   • Length contraction")
        print("   • Relativity of simultaneity")
        print("   • E = mc²")
        print()
        print("   🚀 At 90% light speed:")
        print(f"   • γ = {gamma:.3f}")
        print(f"   • 1 year on ship = {gamma:.2f} years on Earth")
        print("   • Time travel to the future!")

if __name__ == "__main__":
    viz = TimeDilationVisualizer()
    
    print("\n🚀 Starting time dilation simulation...")
    time.sleep(1)
    
    # Test at different velocities
    for v in [0.5, 0.9, 0.99]:
        print("\n" + "="*70)
        viz.simulate_time_dilation(velocity_fraction=v)
        time.sleep(2)
    
    print("\n✅ Simulation complete!")
