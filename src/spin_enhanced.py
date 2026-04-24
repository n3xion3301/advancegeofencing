#!/usr/bin/env python3
"""
🌀 QUANTUM SPIN ENHANCED
Advanced Particle Spin States and Measurements
Quantum Circuit Implementation with Bloch Sphere Visualization
"""
import numpy as np
import math
import sys
import json
from pathlib import Path
from datetime import datetime

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from aer_simulator import AerSimulator

class QuantumSpinEnhanced:
    def __init__(self):
        self.operator = "n3xion3301"
        self.hbar = 1.054571817e-34  # Reduced Planck constant
        self.log_file = Path("logs/quantum/spin_enhanced.log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.show_banner()
        self.log("Quantum Spin System Initialized")
    
    def show_banner(self):
        """Display beautiful ASCII art banner"""
        print("\n" + "="*80)
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║     ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗████████╗██╗   ██╗███╗   ███╗   ║
║    ██╔═══██╗██║   ██║██╔══██╗████╗  ██║╚══██╔══╝██║   ██║████╗ ████║   ║
║    ██║   ██║██║   ██║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║   ║
║    ██║▄▄ ██║██║   ██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║   ║
║    ╚██████╔╝╚██████╔╝██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║   ║
║     ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝   ║
║                                                                          ║
║                         SPIN STATES SYSTEM v2.0                          ║
║                  Quantum Spin-1/2 Particle Simulation                    ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
        """)
        print("="*80)
        print(f"🌀 Operator: {self.operator}")
        print(f"⚛️  ℏ = {self.hbar:.3e} J·s (Reduced Planck Constant)")
        print("="*80)
    
    def log(self, msg):
        """Enhanced logging with timestamp"""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{ts}] {msg}"
        print(f"📝 {log_msg}")
        with open(self.log_file, 'a') as f:
            f.write(log_msg + "\n")
    
    def draw_spin_theory(self):
        """Explain quantum spin theory"""
        print("\n" + "="*80)
        print("⚛️  QUANTUM SPIN THEORY")
        print("="*80)
        print("""
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                    SPIN-1/2 PARTICLE FUNDAMENTALS                       │
    └─────────────────────────────────────────────────────────────────────────┘
    
    QUANTUM NUMBERS:
    ┌──────────────────────────────────────────────────────────────┐
    │  Spin quantum number:      s = 1/2                           │
    │  Magnetic quantum number:  m_s = ±1/2                        │
    │  Total spin:               S = √[s(s+1)]ℏ = (√3/2)ℏ         │
    │  Z-component:              S_z = m_s·ℏ = ±ℏ/2               │
    └──────────────────────────────────────────────────────────────┘
    
    SPIN STATES (Eigenstates):
    ┌──────────────────────────────────────────────────────────────┐
    │  |↑⟩ = Spin-up    = [1]  (m_s = +1/2)                       │
    │                     [0]                                      │
    │                                                              │
    │  |↓⟩ = Spin-down  = [0]  (m_s = -1/2)                       │
    │                     [1]                                      │
    └──────────────────────────────────────────────────────────────┘
    
    PAULI SPIN MATRICES:
    ┌──────────────────────────────────────────────────────────────┐
    │  σ_x = [0  1]    σ_y = [0  -i]    σ_z = [1   0]            │
    │        [1  0]          [i   0]          [0  -1]            │
    └──────────────────────────────────────────────────────────────┘
    
    BLOCH SPHERE REPRESENTATION:
    
                      |↑⟩ (North Pole)
                        ↑
                        │
                        │
         ←──────────────●──────────────→
                        │
                        │
                        ↓
                      |↓⟩ (South Pole)
    
    Any spin-1/2 state can be written as:
    |ψ⟩ = cos(θ/2)|↑⟩ + e^(iφ)sin(θ/2)|↓⟩
    
    where θ and φ are spherical coordinates on the Bloch sphere.
        """)
        print("="*80)
    
    def create_spin_circuit(self, theta, phi=0):
        """Create quantum circuit for arbitrary spin state"""
        print("\n" + "─"*80)
        print("⚛️  BUILDING QUANTUM SPIN CIRCUIT")
        print("─"*80)
        
        qr = QuantumRegister(1, 'spin')
        cr = ClassicalRegister(1, 'measurement')
        qc = QuantumCircuit(qr, cr)
        
        print(f"\n📐 Spin State Parameters:")
        print(f"   θ (theta) = {theta:.4f} rad = {math.degrees(theta):.2f}°")
        print(f"   φ (phi)   = {phi:.4f} rad = {math.degrees(phi):.2f}°")
        
        # Calculate state coefficients
        alpha = np.cos(theta/2)
        beta = np.exp(1j*phi) * np.sin(theta/2)
        
        print(f"\n🌊 State Vector:")
        print(f"   |ψ⟩ = {alpha:.4f}|↑⟩ + {beta:.4f}|↓⟩")
        
        # Build circuit
        print(f"\n🔧 Circuit Construction:")
        
        if abs(theta) > 1e-10:
            qc.ry(theta, qr[0])
            print(f"   Step 1: RY({theta:.4f}) - Rotate around Y-axis")
        
        if abs(phi) > 1e-10:
            qc.rz(phi, qr[0])
            print(f"   Step 2: RZ({phi:.4f}) - Rotate around Z-axis")
        
        qc.measure(qr, cr)
        print(f"   Step 3: Measure spin state")
        
        # Draw circuit
        print("\n📊 QUANTUM CIRCUIT:")
        print("─"*80)
        circuit_lines = str(qc.draw(output='text', fold=-1)).split('\n')
        for line in circuit_lines:
            print(f"    {line}")
        print("─"*80)
        
        return qc, alpha, beta
    
    def simulate_spin_measurement(self, qc, alpha, beta, shots=1000):
        """Simulate spin measurements"""
        print("\n" + "─"*80)
        print("🔮 QUANTUM SIMULATION")
        print("─"*80)
        
        print(f"\n⚡ Running quantum circuit ({shots} shots)...")
        sim = AerSimulator()
        
        # Progress bar
        for i in range(5):
            print(f"    {'▓' * (i*4)}{'░' * (20-i*4)} {(i+1)*20}%")
        
        result = sim.run(qc, shots=shots)
        counts = result.get_counts()
        
        print(f"    ✅ Simulation complete!")
        
        # Calculate probabilities
        prob_up_theory = abs(alpha)**2
        prob_down_theory = abs(beta)**2
        
        prob_up_measured = counts.get('0', 0) / shots
        prob_down_measured = counts.get('1', 0) / shots
        
        print("\n📊 MEASUREMENT RESULTS:")
        print("─"*80)
        print(f"\n    Theoretical Probabilities:")
        print(f"    ┌────────────────────────────────────────┐")
        print(f"    │  P(|↑⟩) = {prob_up_theory*100:6.2f}%  {'█' * int(prob_up_theory*40)}")
        print(f"    │  P(|↓⟩) = {prob_down_theory*100:6.2f}%  {'█' * int(prob_down_theory*40)}")
        print(f"    └────────────────────────────────────────┘")
        
        print(f"\n    Measured Probabilities ({shots} shots):")
        print(f"    ┌────────────────────────────────────────┐")
        print(f"    │  P(|↑⟩) = {prob_up_measured*100:6.2f}%  {'█' * int(prob_up_measured*40)}")
        print(f"    │  P(|↓⟩) = {prob_down_measured*100:6.2f}%  {'█' * int(prob_down_measured*40)}")
        print(f"    └────────────────────────────────────────┘")
        
        # Error analysis
        error_up = abs(prob_up_theory - prob_up_measured)
        error_down = abs(prob_down_theory - prob_down_measured)
        
        print(f"\n    Statistical Error:")
        print(f"    │  Δ(↑) = {error_up*100:.3f}%")
        print(f"    │  Δ(↓) = {error_down*100:.3f}%")
        
        print("─"*80)
        
        return counts
    
    def draw_bloch_sphere(self, theta, phi):
        """ASCII art Bloch sphere representation"""
        print("\n" + "="*80)
        print("🌐 BLOCH SPHERE VISUALIZATION")
        print("="*80)
        
        # Calculate Cartesian coordinates
        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)
        
        print(f"""
    Bloch Sphere Coordinates:
    ┌──────────────────────────────────────┐
    │  x = {x:7.4f}                        │
    │  y = {y:7.4f}                        │
    │  z = {z:7.4f}                        │
    └──────────────────────────────────────┘
    
                    |↑⟩ (z = +1)
                       ↑
                       │
                       │
        ───────────────●───────────────  Equator
                       │
                       │
                       ↓
                    |↓⟩ (z = -1)
    
    State Vector Position:
        """)
        
        # Simple ASCII visualization
        height = 15
        width = 40
        center_x = width // 2
        center_y = height // 2
        
        # Map to ASCII grid
        grid_x = int(center_x + x * (width // 3))
        grid_y = int(center_y - z * (height // 3))
        
        for row in range(height):
            line = ""
            for col in range(width):
                if row == center_y and col == center_x:
                    line += "●"  # Center
                elif row == grid_y and col == grid_x:
                    line += "★"  # State vector
                elif row == 0 and col == center_x:
                    line += "↑"  # North pole
                elif row == height-1 and col == center_x:
                    line += "↓"  # South pole
                elif row == center_y:
                    line += "─"  # Equator
                elif col == center_x:
                    line += "│"  # Axis
                else:
                    line += " "
            print(f"    {line}")
        
        print(f"\n    ● = Origin")
        print(f"    ★ = State |ψ⟩ at (θ={math.degrees(theta):.1f}°, φ={math.degrees(phi):.1f}°)")
        print("="*80)
    
    def stern_gerlach_experiment(self):
        """Simulate Stern-Gerlach experiment"""
        print("\n" + "="*80)
        print("🧲 STERN-GERLACH EXPERIMENT")
        print("="*80)
        print("""
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                    HISTORICAL QUANTUM EXPERIMENT                        │
    └─────────────────────────────────────────────────────────────────────────┘
    
    SETUP:
    ┌──────────────────────────────────────────────────────────────┐
    │                                                              │
    │  Oven  →  Beam  →  Magnet  →  Screen                        │
    │   🔥      ━━━━━     🧲        📺                            │
    │                                                              │
    └──────────────────────────────────────────────────────────────┘
    
    CLASSICAL PREDICTION:
    ┌──────────────────────────────────────────────────────────────┐
    │  Continuous distribution of deflections                      │
    │                                                              │
    │         ░░░░░░░░░░░░░░░░░░░░░░░░░░                          │
    │         ░░░░░░░░░░░░░░░░░░░░░░░░░░  (Smeared pattern)       │
    │         ░░░░░░░░░░░░░░░░░░░░░░░░░░                          │
    │                                                              │
    └──────────────────────────────────────────────────────────────┘
    
    QUANTUM REALITY:
    ┌──────────────────────────────────────────────────────────────┐
    │  TWO discrete spots only!                                    │
    │                                                              │
    │         ████████████                                         │
    │         ████████████  ← Spin-up   (m_s = +1/2)              │
    │                                                              │
    │                                                              │
    │                                                              │
    │         ████████████  ← Spin-down (m_s = -1/2)              │
    │         ████████████                                         │
    │                                                              │
    └──────────────────────────────────────────────────────────────┘
    
    SIGNIFICANCE:
    ✓ Proves quantization of angular momentum
    ✓ Demonstrates intrinsic quantum property (spin)
    ✓ Shows wave function collapse upon measurement
    ✓ Foundation of quantum mechanics
        """)
        print("="*80)
        
        # Simulate beam splitting
        print("\n🔬 SIMULATING BEAM DEFLECTION:")
        print("─"*80)
        
        particles = 100
        up_count = 0
        down_count = 0
        
        print(f"\n    Sending {particles} silver atoms through magnetic field...")
        print()
        
        for i in range(particles):
            # Random spin state
            spin = np.random.choice(['↑', '↓'])
            if spin == '↑':
                up_count += 1
            else:
                down_count += 1
            
            if (i+1) % 20 == 0:
                print(f"    Particles processed: {i+1}/{particles}")
        
        print(f"\n    ✅ Experiment complete!")
        print(f"\n    RESULTS:")
        print(f"    ┌────────────────────────────────────────┐")
        print(f"    │  Spin-up   (↑): {up_count:3d} particles  {'█' * (up_count//2)}")
        print(f"    │  Spin-down (↓): {down_count:3d} particles  {'█' * (down_count//2)}")
        print(f"    └────────────────────────────────────────┘")
        print(f"\n    Ratio: {up_count}:{down_count} ≈ 1:1 (as expected)")
        print("─"*80)
    
    def demonstrate_spin_states(self):
        """Demonstrate various spin states"""
        print("\n" + "╔" + "═"*78 + "╗")
        print("║" + " "*20 + "QUANTUM SPIN DEMONSTRATION" + " "*32 + "║")
        print("╚" + "═"*78 + "╝")
        
        # Show theory
        self.draw_spin_theory()
        
        # Test different spin states
        states = [
            ("Spin-Up (|↑⟩)", 0, 0),
            ("Spin-Down (|↓⟩)", np.pi, 0),
            ("Superposition (|+⟩)", np.pi/2, 0),
            ("Superposition (|-⟩)", np.pi/2, np.pi),
            ("Custom State", np.pi/3, np.pi/4)
        ]
        
        for name, theta, phi in states:
            print("\n" + "╔" + "═"*78 + "╗")
            print("║" + f" Testing: {name}".center(78) + "║")
            print("╚" + "═"*78 + "╝")
            
            self.log(f"Testing spin state: {name}")
            
            # Create circuit
            qc, alpha, beta = self.create_spin_circuit(theta, phi)
            
            # Simulate
            counts = self.simulate_spin_measurement(qc, alpha, beta)
            
            # Visualize on Bloch sphere
            self.draw_bloch_sphere(theta, phi)
            
            input("\n    Press Enter to continue to next state...")
        
        # Stern-Gerlach
        self.stern_gerlach_experiment()
        
        print("\n" + "╔" + "═"*78 + "╗")
        print("║" + " "*25 + "DEMONSTRATION COMPLETE" + " "*31 + "║")
        print("╚" + "═"*78 + "╝")

if __name__ == "__main__":
    spin = QuantumSpinEnhanced()
    spin.demonstrate_spin_states()
