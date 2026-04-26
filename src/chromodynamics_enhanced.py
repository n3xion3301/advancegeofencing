#!/usr/bin/env python3
"""
Enhanced Quantum Chromodynamics Simulator
Visualizes quarks, gluons, and color charge
"""
import numpy as np
from qiskit import QuantumCircuit
from aer_simulator import AerSimulator
import time

class QuantumChromodynamicsVisualizer:
    def __init__(self):
        print("🎨 QUANTUM CHROMODYNAMICS SIMULATOR")
        print("="*70)
        print("The Strong Force: Quarks, Gluons, and Color Charge")
        print("="*70)
    
    def simulate_qcd(self):
        """Simulate quantum chromodynamics"""
        
        print(f"\n📊 QCD PARAMETERS:")
        print(f"   Force: Strong Nuclear Force")
        print(f"   Carriers: Gluons (8 types)")
        print(f"   Charge: Color (Red, Green, Blue)")
        print(f"   Coupling: αₛ ≈ 0.1 - 1 (energy dependent)")
        print(f"   Range: ~1 femtometer (10⁻¹⁵ m)")
        
        # Visualization
        print("\n🎨 COLOR CHARGE VISUALIZATION:")
        self.draw_color_charge()
        
        # Quark confinement
        print("\n🔒 QUARK CONFINEMENT:")
        self.draw_confinement()
        
        # Gluon exchange
        print("\n⚛️  GLUON EXCHANGE:")
        self.draw_gluon_exchange()
        
        # Hadron structure
        print("\n🔬 HADRON STRUCTURE:")
        self.draw_hadrons()
        
        # Quantum circuit
        print("\n⚛️  QUANTUM COLOR SIMULATION:")
        qc = self.create_qcd_circuit()
        
        print(qc.draw(output='text'))
        
        # Simulate
        print("\n⏳ Simulating color interactions...")
        time.sleep(1)
        
        sim = AerSimulator()
        result = sim.run(qc, shots=1000)
        counts = result.get_counts()
        
        print("\n📈 COLOR CHARGE RESULTS:")
        self.display_results(counts)
        
        return counts
    
    def draw_color_charge(self):
        """Draw color charge concept"""
        print()
        print("   COLOR CHARGE (not actual colors!):")
        print("   ═══════════════════════════════════")
        print()
        print("   Quarks carry 'color' charge:")
        print()
        print("      🔴 RED        🟢 GREEN      🔵 BLUE")
        print()
        print("   Anti-quarks carry anti-color:")
        print()
        print("      🔴̄ ANTI-RED   🟢̄ ANTI-GREEN  🔵̄ ANTI-BLUE")
        print()
        print("   COLOR CONFINEMENT RULE:")
        print("   Only COLOR-NEUTRAL combinations exist!")
        print()
        print("   ✅ ALLOWED:")
        print("   • 🔴 + 🟢 + 🔵 = ⚪ (Baryon: proton, neutron)")
        print("   • 🔴 + 🔴̄ = ⚪ (Meson: pion, kaon)")
        print()
        print("   ❌ FORBIDDEN:")
        print("   • 🔴 alone (isolated quark)")
        print("   • 🔴 + 🟢 (not color-neutral)")
        print()
    
    def draw_confinement(self):
        """Draw quark confinement"""
        print()
        print("   QUARK CONFINEMENT:")
        print("   ══════════════════")
        print()
        print("   Try to separate quarks:")
        print()
        print("   Initial: Proton (uud)")
        print("   ┌─────────────────┐")
        print("   │  🔴u  🟢u  🔵d  │")
        print("   └─────────────────┘")
        print()
        print("   Pull quarks apart:")
        print("   ┌──────┐    ┌──────┐")
        print("   │ 🔴u  │~~~~│  🟢u  │  ← Gluon flux tube")
        print("   └──────┘    └──────┘")
        print("        ↑ Energy increases!")
        print()
        print("   Pull harder:")
        print("   ┌───┐        ┌───┐")
        print("   │🔴u│~~~~~~~~│🟢u│  ← More energy!")
        print("   └───┘        └───┘")
        print()
        print("   Energy too high → NEW QUARK PAIR CREATED!")
        print("   ┌───┐  ⚡  ┌───┐")
        print("   │🔴u│ q q̄ │🟢u│")
        print("   └───┘      └───┘")
        print("     ↓        ↓")
        print("   Meson    Meson")
        print()
        print("   🔒 You CANNOT isolate a single quark!")
        print("   💪 Strong force gets STRONGER with distance!")
        print()
    
    def draw_gluon_exchange(self):
        """Draw gluon exchange between quarks"""
        print()
        print("   GLUON EXCHANGE:")
        print("   ═══════════════")
        print()
        print("   Quarks exchange gluons (force carriers):")
        print()
        print("   Before:")
        print("   🔴 Red quark          🟢 Green quark")
        print()
        print("   Exchange:")
        print("   🔴 ─────→ 🌈 ─────→ 🟢")
        print("      Red-Green gluon")
        print()
        print("   After:")
        print("   🟢 Green quark        🔴 Red quark")
        print()
        print("   COLORS SWAPPED!")
        print()
        print("   Gluon properties:")
        print("   • Carries color charge itself!")
        print("   • 8 types of gluons")
        print("   • Can interact with each other")
        print("   • Creates 'gluon self-coupling'")
        print()
        print("   Gluon types:")
        print("   1. 🔴🟢̄  (Red-AntiGreen)")
        print("   2. 🔴🔵̄  (Red-AntiBlue)")
        print("   3. 🟢🔴̄  (Green-AntiRed)")
        print("   4. 🟢🔵̄  (Green-AntiBlue)")
        print("   5. 🔵🔴̄  (Blue-AntiRed)")
        print("   6. 🔵🟢̄  (Blue-AntiGreen)")
        print("   7-8. Mixed states")
        print()
    
    def draw_hadrons(self):
        """Draw hadron structure"""
        print()
        print("   HADRON STRUCTURE:")
        print("   ═════════════════")
        print()
        print("   BARYONS (3 quarks):")
        print("   ───────────────────")
        print()
        print("   Proton (uud):")
        print("   ┌─────────────────┐")
        print("   │                 │")
        print("   │   🔴u   🟢u     │")
        print("   │      ╲ │ ╱      │")
        print("   │       ╲│╱       │")
        print("   │        🔵d       │")
        print("   │                 │")
        print("   └─────────────────┘")
        print("   Charge: +1, Color: ⚪ (neutral)")
        print()
        print("   Neutron (udd):")
        print("   ┌─────────────────┐")
        print("   │                 │")
        print("   │   🔴u   🟢d     │")
        print("   │      ╲ │ ╱      │")
        print("   │       ╲│╱       │")
        print("   │        🔵d       │")
        print("   │                 │")
        print("   └─────────────────┘")
        print("   Charge: 0, Color: ⚪ (neutral)")
        print()
        print("   MESONS (quark + antiquark):")
        print("   ───────────────────────────")
        print()
        print("   Pion π⁺ (ud̄):")
        print("   ┌─────────────┐")
        print("   │             │")
        print("   │   🔴u ←→ 🔵̄d̄ │")
        print("   │             │")
        print("   └─────────────┘")
        print("   Charge: +1, Color: ⚪ (neutral)")
        print()
    
    def create_qcd_circuit(self):
        """Create quantum circuit for QCD"""
        qc = QuantumCircuit(3, 3)
        
        # 3 qubits represent 3 color charges
        # Qubit 0: Red
        # Qubit 1: Green  
        # Qubit 2: Blue
        
        # Create color superposition
        for i in range(3):
            qc.h(i)
        
        # Color interactions (gluon exchange)
        # Swap colors
        qc.cx(0, 1)
        qc.cx(1, 2)
        qc.cx(2, 0)
        
        # Color rotations
        qc.ry(np.pi/3, 0)
        qc.ry(np.pi/3, 1)
        qc.ry(np.pi/3, 2)
        
        # More interactions
        qc.cx(0, 2)
        qc.cx(1, 0)
        
        qc.measure(range(3), range(3))
        
        return qc
    
    def display_results(self, counts):
        """Display QCD results"""
        total = sum(counts.values())
        
        print("\n   State | Count | Probability | Color Configuration")
        print("   " + "─"*70)
        
        color_names = {
            '000': 'All Red (forbidden)',
            '001': 'RR Blue',
            '010': 'R Green R',
            '011': 'R Green Blue',
            '100': 'Green RR',
            '101': 'Green R Blue',
            '110': 'Green Green R',
            '111': 'RGB (color neutral ✓)'
        }
        
        # Sort by count
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        
        for state, count in sorted_counts[:8]:
            prob = count / total if total > 0 else 0
            bar = '█' * int(prob * 30)
            
            config = color_names.get(state, 'Unknown')
            
            print(f"   {state}  | {count:4d}  | {prob:6.1%} {bar:30s} | {config}")
        
        print("\n💡 PHYSICS EXPLANATION:")
        print()
        print("   QUANTUM CHROMODYNAMICS (QCD):")
        print("   • Theory of strong nuclear force")
        print("   • Quarks interact via gluons")
        print("   • Color charge (not real color!)")
        print("   • SU(3) gauge symmetry")
        print()
        print("   KEY FEATURES:")
        print("   • Asymptotic freedom (weak at high energy)")
        print("   • Confinement (strong at low energy)")
        print("   • Gluons carry color charge")
        print("   • Self-interacting force")
        print()
        print("   QUARK FLAVORS:")
        print("   • Up (u), Down (d), Strange (s)")
        print("   • Charm (c), Bottom (b), Top (t)")
        print("   • Each comes in 3 colors")
        print()
        print("   EXPERIMENTAL EVIDENCE:")
        print("   • Deep inelastic scattering ✓")
        print("   • Jet production in colliders ✓")
        print("   • Lattice QCD calculations ✓")
        print("   • Quark-gluon plasma (RHIC, LHC) ✓")
        print()
        print("   APPLICATIONS:")
        print("   • Nuclear physics")
        print("   • Particle physics")
        print("   • Neutron stars")
        print("   • Early universe")
        print()
        print("   🏆 Nobel Prize 2004:")
        print("      Gross, Politzer, Wilczek")
        print("      'For discovery of asymptotic freedom'")

if __name__ == "__main__":
    viz = QuantumChromodynamicsVisualizer()
    
    print("\n🚀 Starting QCD simulation...")
    time.sleep(1)
    
    viz.simulate_qcd()
    
    print("\n✅ Simulation complete!")
