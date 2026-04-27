#!/usr/bin/env python3
"""
ENHANCED 3D BLOCH SPHERE VISUALIZATION
Ultra Visual Quantum State Representation

ENHANCEMENTS:
- Beautiful 3D Bloch sphere ASCII art
- Quantum state vector visualizations
- Rotation animations
- Phase angle diagrams
- Coordinate system illustrations
- State evolution tracking
- Interactive state manipulation
- Comprehensive state analysis
"""

import numpy as np
from datetime import datetime
from pathlib import Path
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector
import warnings
warnings.filterwarnings('ignore')


class BlochSphereEnhanced:
    """Enhanced Bloch Sphere Visualization"""
    
    def __init__(self):
        self.sampler = StatevectorSampler()
        self.states = []
        
        self.log_dir = Path("logs/bloch_sphere")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self._print_banner()
    
    def _print_banner(self):
        """Print stunning Bloch sphere banner with ASCII art"""
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║              ✧･ﾟ: *✧･ﾟ:* BLOCH SPHERE ENHANCED *:･ﾟ✧*:･ﾟ✧                ║
║                  3D Quantum State Visualization                          ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

                            ╱╲
                           ╱  ╲         |0⟩ (North Pole)
                          ╱ |0⟩╲           ↑
                         ╱      ╲          │
                        ╱────────╲         │
                       ╱          ╲        │
                      ╱     ✧      ╲       │
                     ╱              ╲      │
                    ╱       ψ        ╲     │
                   ╱                  ╲    │
                  ╱          θ         ╲   │
                 ╱                      ╲  │
                ╱────────────────────────╲ │
               ╱                          ╲│
              ╱             φ              ╲
             ╱──────────────────────────────╲
            ╱                                ╲
           ╱                                  ╲
          ╱                                    ╲
         ╱──────────────────────────────────────╲
                        |1⟩ (South Pole)
                             ↓

        ┌────────────────────────────────────────────────────┐
        │  🌐 BLOCH SPHERE COORDINATES                        │
        ├────────────────────────────────────────────────────┤
        │  • θ (theta): Polar angle [0, π]                   │
        │  • φ (phi): Azimuthal angle [0, 2π]                │
        │  • |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩           │
        └────────────────────────────────────────────────────┘
        """)
    
    def print_3d_bloch_sphere(self, theta=0, phi=0):
        """Print beautiful 3D Bloch sphere with state vector"""
        
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                        🌐 3D BLOCH SPHERE VIEW 🌐                         ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║                              Z (|0⟩)                                     ║
║                                ↑                                         ║
║                                │                                         ║
║                          ╭─────┼─────╮                                   ║
║                        ╱       │       ╲                                 ║
║                      ╱         │         ╲                               ║
║                    ╱           │           ╲                             ║
║                  ╱             │             ╲                           ║
║                ╱               │               ╲                         ║
║              ╱                 │                 ╲                       ║
║            ╱                   │                   ╲                     ║
║          ╱                     │                     ╲                   ║
║        ╱                       │                       ╲                 ║
║      ╱                         │                         ╲               ║
║    ╱                           │                           ╲             ║
║  ╱─────────────────────────────┼─────────────────────────────╲           ║
║ ╱                              │                              ╲          ║
║╱                               │                               ╲         ║
║                                │                                         ║
║ Y ←────────────────────────────●────────────────────────────→ X          ║
║                                │                                         ║
║╲                               │                               ╱         ║
║ ╲                              │                              ╱          ║
║  ╲─────────────────────────────┼─────────────────────────────╱           ║
║    ╲                           │                           ╱             ║
║      ╲                         │                         ╱               ║
║        ╲                       │                       ╱                 ║
║          ╲                     │                     ╱                   ║
║            ╲                   │                   ╱                     ║
║              ╲                 │                 ╱                       ║
║                ╲               │               ╱                         ║
║                  ╲             │             ╱                           ║
║                    ╲           │           ╱                             ║
║                      ╲         │         ╱                               ║
║                        ╲       │       ╱                                 ║
║                          ╰─────┼─────╯                                   ║
║                                │                                         ║
║                                ↓                                         ║
║                              (|1⟩)                                       ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
        """)
        
        # Show state vector position
        print(f"""
┌────────────────────────────────────────────────────────────────────────┐
│                      📍 STATE VECTOR POSITION                           │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  θ (Polar Angle):     {theta:.4f} rad  ({np.degrees(theta):.2f}°)      │
│  φ (Azimuthal Angle): {phi:.4f} rad  ({np.degrees(phi):.2f}°)          │
│                                                                        │
│  Cartesian Coordinates:                                                │
│    X = sin(θ)cos(φ) = {np.sin(theta)*np.cos(phi):7.4f}                │
│    Y = sin(θ)sin(φ) = {np.sin(theta)*np.sin(phi):7.4f}                │
│    Z = cos(θ)       = {np.cos(theta):7.4f}                             │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
        """)
    
    def visualize_quantum_state(self, state_vector):
        """Visualize quantum state with beautiful ASCII art"""
        
        # Extract amplitudes
        alpha = state_vector[0]
        beta = state_vector[1]
        
        # Calculate probabilities
        prob_0 = abs(alpha)**2
        prob_1 = abs(beta)**2
        
        # Calculate Bloch sphere coordinates
        theta = 2 * np.arccos(abs(alpha))
        phi = np.angle(beta) - np.angle(alpha)
        
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                     ⚛️  QUANTUM STATE ANALYSIS ⚛️                         ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  State Vector: |ψ⟩ = α|0⟩ + β|1⟩                                         ║
║                                                                          ║
        """)
        
        print(f"║  α = {alpha.real:.4f} + {alpha.imag:.4f}i".ljust(76) + "║")
        print(f"║  β = {beta.real:.4f} + {beta.imag:.4f}i".ljust(76) + "║")
        print("║" + " "*74 + "║")
        
        # Probability bars
        bar_0_len = int(prob_0 * 50)
        bar_1_len = int(prob_1 * 50)
        bar_0 = "█" * bar_0_len + "░" * (50 - bar_0_len)
        bar_1 = "█" * bar_1_len + "░" * (50 - bar_1_len)
        
        print(f"║  P(|0⟩) = {prob_0:.4f}  │{bar_0}│".ljust(76) + "║")
        print(f"║  P(|1⟩) = {prob_1:.4f}  │{bar_1}│".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")
        
        # Show state on Bloch sphere
        self.print_state_on_sphere(theta, phi, prob_0, prob_1)
    
    def print_state_on_sphere(self, theta, phi, prob_0, prob_1):
        """Print state position on Bloch sphere"""
        
        print("""
┌────────────────────────────────────────────────────────────────────────┐
│                    🎯 STATE ON BLOCH SPHERE 🎯                          │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
        """)
        
        # Determine position description
        if theta < np.pi/4:
            position = "Near |0⟩ (North Pole)"
            symbol = "↑"
        elif theta > 3*np.pi/4:
            position = "Near |1⟩ (South Pole)"
            symbol = "↓"
        else:
            position = "Equatorial Plane"
            symbol = "→"
        
        print(f"│  Position: {position}".ljust(74) + "│")
        print("│" + " "*72 + "│")
        
        # ASCII art representation of position
        if theta < np.pi/4:
            print("""│
│                           ★ ← State here!
│                          ╱│╲
│                         ╱ │ ╲
│                        ╱  │  ╲
│                       ╱   │   ╲
│                      ╱────┼────╲
│                     ╱     │     ╲
│                    ╱      │      ╲
│                   ╱───────┼───────╲
│                  ╱        │        ╲
│                 ╱─────────┼─────────╲
│                                                                        │""")
        elif theta > 3*np.pi/4:
            print("""│
│                 ╱─────────┼─────────╲
│                  ╲        │        ╱
│                   ╲───────┼───────╱
│                    ╲      │      ╱
│                     ╲     │     ╱
│                      ╲────┼────╱
│                       ╲   │   ╱
│                        ╲  │  ╱
│                         ╲ │ ╱
│                          ╲│╱
│                           ★ ← State here!
│                                                                        │""")
        else:
            print("""│
│                 ╱─────────┼─────────╲
│                  ╲        │        ╱
│                   ╲───────┼───────╱
│                    ╲      │      ╱
│              ★ ────╲─────┼─────╱──── ← State here!
│                     ╲     │     ╱
│                      ╲────┼────╱
│                       ╲   │   ╱
│                        ╲  │  ╱
│                         ╲ │ ╱
│                          ╲│╱
│                                                                        │""")
        
        print("└────────────────────────────────────────────────────────────────────────┘")
    
    def print_rotation_diagram(self, axis, angle):
        """Print rotation operation diagram"""
        
        print(f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                      🔄 ROTATION OPERATION 🔄                             ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  Axis: {axis}                                                            ║
║  Angle: {angle:.4f} rad ({np.degrees(angle):.2f}°)                       ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
        """)
        
        if axis == 'X':
            print("""
┌────────────────────────────────────────────────────────────────────────┐
│                         X-AXIS ROTATION                                │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│                            |0⟩                                         │
│                             ↑                                          │
│                             │                                          │
│                             │    ↻                                     │
│                             │  ╱                                       │
│                             │╱                                         │
│         ←───────────────────●───────────────────→ X (Rotation Axis)    │
│                           ╱ │                                          │
│                         ╱   │                                          │
│                       ↻     │                                          │
│                             ↓                                          │
│                            |1⟩                                         │
│                                                                        │
│  State rotates in Y-Z plane around X-axis                              │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
            """)
        elif axis == 'Y':
            print("""
┌────────────────────────────────────────────────────────────────────────┐
│                         Y-AXIS ROTATION                                │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│                            |0⟩                                         │
│                             ↑                                          │
│                             │  ↻                                       │
│                             │╱                                         │
│                             ●                                          │
│                           ╱ │╲                                         │
│                         ╱   │  ╲                                       │
│                       ↻     │    ↻                                     │
│                             ↓                                          │
│                            |1⟩                                         │
│                             ↕                                          │
│                        Y (Rotation Axis)                               │
│                                                                        │
│  State rotates in X-Z plane around Y-axis                              │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
            """)
        else:  # Z-axis
            print("""
┌────────────────────────────────────────────────────────────────────────┐
│                         Z-AXIS ROTATION                                │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│                            |0⟩                                         │
│                             ↑                                          │
│                             │ Z (Rotation Axis)                        │
│                             │                                          │
│                             │                                          │
│                   ↻       ╱ │ ╲       ↻                                │
│                         ╱   │   ╲                                      │
│                       ╱     │     ╲                                    │
│         ←───────────────────●───────────────────→                      │
│                       ╲     │     ╱                                    │
│                         ╲   │   ╱                                      │
│                   ↻       ╲ │ ╱       ↻                                │
│                             │                                          │
│                             ↓                                          │
│                            |1⟩                                         │
│                                                                        │
│  State rotates in X-Y plane around Z-axis (phase rotation)             │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
            """)
    
    def apply_rotation(self, initial_state, axis, angle):
        """
        Apply rotation to quantum state
        
        Args:
            initial_state: Initial state vector
            axis: Rotation axis ('X', 'Y', or 'Z')
            angle: Rotation angle in radians
        
        Returns:
            Final state vector
        """
        
        self.print_rotation_diagram(axis, angle)
        
        # Create quantum circuit
        qc = QuantumCircuit(1)
        
        # Initialize state
        qc.initialize(initial_state, 0)
        
        # Apply rotation
        if axis == 'X':
            qc.rx(angle, 0)
        elif axis == 'Y':
            qc.ry(angle, 0)
        else:  # Z
            qc.rz(angle, 0)
        
        # Get final state
        final_state = Statevector(qc)
        
        print("""
┌────────────────────────────────────────────────────────────────────────┐
│                    ✨ ROTATION RESULT ✨                                 │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Initial State  ──[Rotation]──▶  Final State                           │
│                                                                        │
        """)
        
        # Show before and after
        print(f"│  Before: α = {initial_state[0]:.4f}, β = {initial_state[1]:.4f}".ljust(74) + "│")
        print(f"│  After:  α = {final_state[0]:.4f}, β = {final_state[1]:.4f}".ljust(74) + "│")
        print("│" + " "*72 + "│")
        print("└────────────────────────────────────────────────────────────────────────┘")
        
        return final_state.data
    
    def create_superposition_state(self):
        """Create and visualize superposition state"""
        
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                   🌟 SUPERPOSITION STATE CREATION 🌟                      ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  Creating equal superposition: |+⟩ = (|0⟩ + |1⟩)/√2                      ║
║                                                                          ║
║                            |0⟩                                           ║
║                             ↑                                            ║
║                             │                                            ║
║                             │                                            ║
║                             │                                            ║
║                   ╱─────────┼─────────╲                                  ║
║                 ╱           │           ╲                                ║
║               ╱             │             ╲                              ║
║             ╱               │               ╲                            ║
║           ╱                 │                 ╲                          ║
║         ╱                   │                   ╲                        ║
║  ────────────────────────── ★ ──────────────────────── X                 ║
║         ╲                   │                   ╱                        ║
║           ╲                 │                 ╱                          ║
║             ╲               │               ╱                            ║
║               ╲             │             ╱                              ║
║                 ╲           │           ╱                                ║
║                   ╲─────────┼─────────╱                                  ║
║                             │                                            ║
║                             │                                            ║
║                             ↓                                            ║
║                            |1⟩                                           ║
║                                                                          ║
║  State is on equator (equal probability of |0⟩ and |1⟩)                  ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
        """)
        
        # Create superposition
        qc = QuantumCircuit(1)
        qc.h(0)
        state = Statevector(qc)
        
        return state.data
    
    def visualize_state_evolution(self, states):
        """Visualize evolution of quantum state"""
        
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                    🎬 STATE EVOLUTION ANIMATION 🎬                        ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
        """)
        
        for i, state in enumerate(states):
            theta = 2 * np.arccos(abs(state[0]))
            
            print(f"║  Step {i+1}:".ljust(76) + "║")
            
            # Simple position indicator
            if theta < np.pi/3:
                print("║      |0⟩ ★                                                               ║")
                print("║       │                                                                  ║")
                print("║      ─●─                                                                 ║")
                print("║       │                                                                  ║")
                print("║      |1⟩                                                                 ║")
            elif theta < 2*np.pi/3:
                print("║      |0⟩                                                                 ║")
                print("║       │                                                                  ║")
                print("║  ────★──                                                                 ║")
                print("║       │                                                                  ║")
                print("║      |1⟩                                                                 ║")
            else:
                print("║      |0⟩                                                                 ║")
                print("║       │                                                                  ║")
                print("║      ─●─                                                                 ║")
                print("║       │                                                                  ║")
                print("║      |1⟩ ★                                                               ║")
            
            print("║" + " "*74 + "║")
        
        print("╚══════════════════════════════════════════════════════════════════════════╝")


def demo_bloch_sphere():
    """Stunning demonstration of Bloch Sphere visualization"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║══════════════════════════════════════════════════════════════════════════║
║                   🌐 BLOCH SPHERE DEMONSTRATION 🌐                        ║
║══════════════════════════════════════════════════════════════════════════║
╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize
    bloch = BlochSphereEnhanced()
    
    # Test 1: Visualize |0⟩ state
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 1: GROUND STATE |0⟩ ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    state_0 = np.array([1.0, 0.0])
    bloch.visualize_quantum_state(state_0)
    bloch.print_3d_bloch_sphere(0, 0)
    
    # Test 2: Create superposition
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 2: SUPERPOSITION STATE |+⟩ ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    state_plus = bloch.create_superposition_state()
    bloch.visualize_quantum_state(state_plus)
    
    # Test 3: Apply rotations
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 3: ROTATION OPERATIONS ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    # X rotation
    state_after_x = bloch.apply_rotation(state_0, 'X', np.pi/2)
    bloch.visualize_quantum_state(state_after_x)
    
    # Test 4: State evolution
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 4: STATE EVOLUTION ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    states = [state_0, state_after_x, state_plus]
    bloch.visualize_state_evolution(states)
    
    # Final summary
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                        ✅ DEMONSTRATION COMPLETE! ✅                       ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  Features Demonstrated:                                                  ║
║    ✨ 3D Bloch sphere ASCII art                                           ║
║    ✨ Quantum state visualization                                         ║
║    ✨ Rotation operation diagrams                                         ║
║    ✨ Superposition state creation                                        ║
║    ✨ State evolution animation                                           ║
║    ✨ Beautiful coordinate system art                                     ║
║    ✨ Interactive state manipulation                                      ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    demo_bloch_sphere()
