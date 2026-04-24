#!/usr/bin/env python3
"""
🌊 QUANTUM INTERFERENCE ENHANCED
Advanced Wave Interference and Double-Slit Experiment
Quantum Superposition and Phase Manipulation
"""
import numpy as np
import math
import sys
import json
from pathlib import Path
from datetime import datetime

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from aer_simulator import AerSimulator

class QuantumInterferenceEnhanced:
    def __init__(self):
        self.operator = "n3xion3301"
        self.log_file = Path("logs/quantum/interference_enhanced.log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.show_banner()
        self.log("Quantum Interference System Initialized")
    
    def show_banner(self):
        """Display beautiful ASCII art banner"""
        print("\n" + "="*80)
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║     ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗████████╗██╗   ██╗███╗   ███╗     ║
║    ██╔═══██╗██║   ██║██╔══██╗████╗  ██║╚══██╔══╝██║   ██║████╗ ████║     ║
║    ██║   ██║██║   ██║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║     ║
║    ██║▄▄ ██║██║   ██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║     ║
║    ╚██████╔╝╚██████╔╝██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║     ║
║     ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝     ║
║                                                                          ║
║                    INTERFERENCE PATTERNS v2.0                            ║
║              Quantum Wave Interference & Double-Slit                     ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
        """)
        print("="*80)
        print(f"🌊 Operator: {self.operator}")
        print(f"⚛️  Wave-Particle Duality Demonstration")
        print("="*80)
    
    def log(self, msg):
        """Enhanced logging with timestamp"""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{ts}] {msg}"
        print(f"📝 {log_msg}")
        with open(self.log_file, 'a') as f:
            f.write(log_msg + "\n")
    
    def draw_interference_theory(self):
        """Explain quantum interference theory"""
        print("\n" + "="*80)
        print("⚛️  QUANTUM INTERFERENCE THEORY")
        print("="*80)
        print("""
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                    WAVE INTERFERENCE FUNDAMENTALS                       │
    └─────────────────────────────────────────────────────────────────────────┘
    
    SUPERPOSITION PRINCIPLE:
    ┌──────────────────────────────────────────────────────────────┐
    │  When two or more quantum states overlap, they combine       │
    │  according to their probability amplitudes:                  │
    │                                                              │
    │  |ψ_total⟩ = α|ψ₁⟩ + β|ψ₂⟩                                  │
    │                                                              │
    │  Probability = |α + β|²                                      │
    └──────────────────────────────────────────────────────────────┘
    
    CONSTRUCTIVE INTERFERENCE:
    ┌──────────────────────────────────────────────────────────────┐
    │  Waves in phase → Amplitudes ADD                             │
    │                                                              │
    │     ∿∿∿∿∿∿∿∿                                                │
    │  +  ∿∿∿∿∿∿∿∿                                                │
    │  ═══════════                                                 │
    │     ∿∿∿∿∿∿∿∿  (Larger amplitude)                            │
    │                                                              │
    │  Result: BRIGHT fringe (high probability)                    │
    └──────────────────────────────────────────────────────────────┘
    
    DESTRUCTIVE INTERFERENCE:
    ┌──────────────────────────────────────────────────────────────┐
    │  Waves out of phase → Amplitudes CANCEL                      │
    │                                                              │
    │     ∿∿∿∿∿∿∿∿                                                │
    │  +  ∼∼∼∼∼∼∼∼  (180° phase shift)                           │
    │  ═══════════                                                 │
    │     ________  (Zero amplitude)                               │
    │                                                              │
    │  Result: DARK fringe (zero probability)                      │
    └──────────────────────────────────────────────────────────────┘
    
    PHASE RELATIONSHIP:
    ┌──────────────────────────────────────────────────────────────┐
    │  Δφ = 0°, 360°, ...     → Constructive (bright)             │
    │  Δφ = 180°, 540°, ...   → Destructive (dark)                │
    │  Δφ = other angles      → Partial interference              │
    └──────────────────────────────────────────────────────────────┘
        """)
        print("="*80)
    
    def draw_double_slit_setup(self):
        """Visualize double-slit experiment setup"""
        print("\n" + "="*80)
        print("🔬 DOUBLE-SLIT EXPERIMENT SETUP")
        print("="*80)
        print("""
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                    THE FAMOUS DOUBLE-SLIT EXPERIMENT                    │
    └─────────────────────────────────────────────────────────────────────────┘
    
    EXPERIMENTAL SETUP:
    
    Source        Barrier         Screen
      ⚛️           ║ ║            ░░░
                   ║ ║            ░░░
      ━━━━━━━━━━━━━╬═╬━━━━━━━━━━━░█░  ← Bright fringe
                   ║ ║            ░░░
                   ║█║  Slit 1    ░░░  ← Dark fringe
                   ║ ║            ░░░
      Photon  ━━━━━╬═╬━━━━━━━━━━━░█░  ← Bright fringe
      or            ║ ║            ░░░
      Electron      ║█║  Slit 2    ░░░  ← Dark fringe
                   ║ ║            ░░░
                   ║ ║            ░█░  ← Bright fringe
                   ║ ║            ░░░
    
    QUANTUM BEHAVIOR:
    ┌──────────────────────────────────────────────────────────────┐
    │  1. Particle goes through BOTH slits simultaneously          │
    │     (quantum superposition)                                  │
    │                                                              │
    │  2. Particle interferes with ITSELF                          │
    │     (wave-like behavior)                                     │
    │                                                              │
    │  3. Creates interference pattern on screen                   │
    │     (alternating bright and dark fringes)                    │
    │                                                              │
    │  4. Measurement collapses superposition                      │
    │     (particle detected at ONE location)                      │
    └──────────────────────────────────────────────────────────────┘
    
    WHICH-PATH INFORMATION:
    ┌──────────────────────────────────────────────────────────────┐
    │  If you measure which slit → NO interference pattern         │
    │  If you don't measure      → Interference pattern appears    │
    │                                                              │
    │  "The act of observation changes reality!"                   │
    └──────────────────────────────────────────────────────────────┘
        """)
        print("="*80)
    
    def create_interference_circuit(self, num_paths=2, phase_shift=0):
        """Create quantum circuit for interference pattern"""
        print("\n" + "─"*80)
        print("⚛️  BUILDING QUANTUM INTERFERENCE CIRCUIT")
        print("─"*80)
        
        qr = QuantumRegister(num_paths, 'path')
        cr = ClassicalRegister(num_paths, 'detection')
        qc = QuantumCircuit(qr, cr)
        
        print(f"\n📐 Interference Parameters:")
        print(f"   Number of paths: {num_paths}")
        print(f"   Phase shift: {phase_shift:.4f} rad = {math.degrees(phase_shift):.2f}°")
        
        print(f"\n🔧 Circuit Construction:")
        
        # Step 1: Create superposition (particle goes through all slits)
        print(f"\n   Step 1: Create superposition on all {num_paths} paths")
        for i in range(num_paths):
            qc.h(qr[i])
            print(f"           H gate on path {i} → Equal superposition")
        
        # Step 2: Apply phase shifts (simulate path differences)
        print(f"\n   Step 2: Apply phase shifts (path length differences)")
        for i in range(num_paths):
            phase = phase_shift * i
            if abs(phase) > 1e-10:
                qc.p(phase, qr[i])
                print(f"           Phase({phase:.4f}) on path {i}")
        
        # Step 3: Interference (recombine paths)
        print(f"\n   Step 3: Recombine paths (interference occurs)")
        for i in range(num_paths):
            qc.h(qr[i])
            print(f"           H gate on path {i} → Interference")
        
        # Step 4: Measure
        print(f"\n   Step 4: Measure detection pattern")
        qc.measure(qr, cr)
        
        # Draw circuit
        print("\n📊 QUANTUM CIRCUIT:")
        print("─"*80)
        circuit_lines = str(qc.draw(output='text', fold=-1)).split('\n')
        for line in circuit_lines:
            print(f"    {line}")
        print("─"*80)
        
        return qc
    
    def simulate_interference(self, qc, shots=1000):
        """Simulate interference pattern"""
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
        
        print("\n📊 INTERFERENCE PATTERN:")
        print("─"*80)
        
        # Sort by state
        sorted_counts = sorted(counts.items(), key=lambda x: x[0])
        
        max_count = max(counts.values())
        
        for state, count in sorted_counts:
            percentage = (count / shots) * 100
            bar_length = int((count / max_count) * 50)
            bar = "█" * bar_length
            
            # Determine if constructive or destructive
            if percentage > 40:
                label = "BRIGHT (Constructive)"
                icon = "🔆"
            elif percentage < 10:
                label = "DARK (Destructive)"
                icon = "🌑"
            else:
                label = "Partial"
                icon = "🌓"
            
            print(f"    {icon} |{state}⟩: {bar} {count:4d} ({percentage:5.1f}%) - {label}")
        
        print("─"*80)
        
        return counts
    
    def draw_interference_pattern(self, counts, shots):
        """Draw ASCII interference pattern on screen"""
        print("\n" + "="*80)
        print("📺 DETECTION SCREEN - INTERFERENCE PATTERN")
        print("="*80)
        
        # Convert counts to intensity array
        states = sorted(counts.keys())
        intensities = [counts[s] / shots for s in states]
        
        print("\n    Intensity Distribution:")
        print("    " + "─"*70)
        
        # Draw pattern (vertical bars)
        height = 20
        for row in range(height, 0, -1):
            line = "    │"
            for intensity in intensities:
                threshold = row / height
                if intensity >= threshold:
                    line += "██"
                else:
                    line += "  "
            line += "│"
            print(line)
        
        print("    └" + "──" * len(intensities) + "┘")
        
        # Labels
        label_line = "     "
        for i, state in enumerate(states):
            label_line += f"{state} "
        print(label_line)
        
        print("\n    Pattern Analysis:")
        print("    ┌────────────────────────────────────────────────────┐")
        
        # Find peaks and valleys
        max_intensity = max(intensities)
        min_intensity = min(intensities)
        
        print(f"    │  Maximum intensity: {max_intensity*100:.1f}% (Bright fringe)  │")
        print(f"    │  Minimum intensity: {min_intensity*100:.1f}% (Dark fringe)    │")
        print(f"    │  Contrast ratio: {max_intensity/max(min_intensity, 0.01):.2f}:1           │")
        print("    └────────────────────────────────────────────────────┘")
        
        print("="*80)
    
    def analyze_phase_effects(self):
        """Demonstrate how phase affects interference"""
        print("\n" + "="*80)
        print("🔄 PHASE SHIFT ANALYSIS")
        print("="*80)
        
        phases = [
            (0, "0° - In Phase (Maximum Constructive)"),
            (np.pi/4, "45° - Partial Interference"),
            (np.pi/2, "90° - Equal Mix"),
            (3*np.pi/4, "135° - Partial Interference"),
            (np.pi, "180° - Out of Phase (Maximum Destructive)")
        ]
        
        print("\n    Testing different phase relationships:")
        print("    " + "─"*70)
        
        for phase, description in phases:
            print(f"\n    📐 Phase: {description}")
            
            # Create simple 2-path circuit
            qc = self.create_interference_circuit(num_paths=2, phase_shift=phase)
            
            # Simulate
            counts = self.simulate_interference(qc, shots=500)
            
            input("\n    Press Enter to continue to next phase...")
        
        print("\n" + "="*80)
    
    def demonstrate_which_path(self):
        """Demonstrate which-path information destroying interference"""
        print("\n" + "="*80)
        print("👁️  WHICH-PATH INFORMATION EXPERIMENT")
        print("="*80)
        print("""
    ┌─────────────────────────────────────────────────────────────────────────┐
    │              MEASUREMENT DESTROYS INTERFERENCE                          │
    └─────────────────────────────────────────────────────────────────────────┘
    
    SCENARIO 1: No measurement (which-path unknown)
    ┌──────────────────────────────────────────────────────────────┐
    │  Particle in superposition → Goes through BOTH slits         │
    │  Result: INTERFERENCE PATTERN appears                        │
    └──────────────────────────────────────────────────────────────┘
        """)
        
        print("\n    🔬 Running without measurement...")
        qc_no_measure = self.create_interference_circuit(num_paths=2, phase_shift=np.pi/2)
        counts_no_measure = self.simulate_interference(qc_no_measure, shots=1000)
        self.draw_interference_pattern(counts_no_measure, 1000)
        
        input("\n    Press Enter to see what happens WITH measurement...")
        
        print("""
    SCENARIO 2: With measurement (which-path known)
    ┌──────────────────────────────────────────────────────────────┐
    │  Measure which slit → Wave function COLLAPSES                │
    │  Particle goes through ONE slit only                         │
    │  Result: NO interference pattern (just two blobs)            │
    └──────────────────────────────────────────────────────────────┘
        """)
        
        print("\n    👁️  Adding which-path detector...")
        
        # Create circuit with intermediate measurement
        qr = QuantumRegister(2, 'path')
        cr = ClassicalRegister(2, 'detection')
        qc_measure = QuantumCircuit(qr, cr)
        
        # Superposition
        qc_measure.h(qr[0])
        qc_measure.h(qr[1])
        
        # MEASURE which path (this destroys interference!)
        qc_measure.measure(qr, cr)
        
        # Try to interfere (won't work after measurement)
        qc_measure.h(qr[0])
        qc_measure.h(qr[1])
        
        print("\n    Circuit with which-path measurement:")
        print("    " + "─"*70)
        circuit_lines = str(qc_measure.draw(output='text', fold=-1)).split('\n')
        for line in circuit_lines:
            print(f"    {line}")
        print("    " + "─"*70)
        
        counts_measure = self.simulate_interference(qc_measure, shots=1000)
        self.draw_interference_pattern(counts_measure, 1000)
        
        print("\n    ⚠️  OBSERVATION: Interference pattern DESTROYED!")
        print("    The act of measurement changed the quantum state!")
        
        print("="*80)
    
    def demonstrate_interference(self):
        """Main demonstration of quantum interference"""
        print("\n" + "╔" + "═"*78 + "╗")
        print("║" + " "*20 + "QUANTUM INTERFERENCE DEMONSTRATION" + " "*24 + "║")
        print("╚" + "═"*78 + "╝")
        
        # Show theory
        self.draw_interference_theory()
        input("\n    Press Enter to continue...")
        
        # Show double-slit setup
        self.draw_double_slit_setup()
        input("\n    Press Enter to continue...")
        
        # Basic interference
        print("\n" + "╔" + "═"*78 + "╗")
        print("║" + " "*25 + "BASIC INTERFERENCE TEST" + " "*29 + "║")
        print("╚" + "═"*78 + "╝")
        
        self.log("Testing basic 2-path interference")
        qc = self.create_interference_circuit(num_paths=2, phase_shift=np.pi/2)
        counts = self.simulate_interference(qc, shots=1000)
        self.draw_interference_pattern(counts, 1000)
        
        input("\n    Press Enter to continue...")
        
        # Phase analysis
        self.analyze_phase_effects()
        
        # Which-path experiment
        self.demonstrate_which_path()
        
        print("\n" + "╔" + "═"*78 + "╗")
        print("║" + " "*25 + "DEMONSTRATION COMPLETE" + " "*31 + "║")
        print("╚" + "═"*78 + "╝")
        
        print("\n    Key Takeaways:")
        print("    ✓ Quantum particles exhibit wave-particle duality")
        print("    ✓ Interference proves superposition of states")
        print("    ✓ Measurement destroys quantum interference")
        print("    ✓ Observer effect is fundamental to quantum mechanics")

if __name__ == "__main__":
    interference = QuantumInterferenceEnhanced()
    interference.demonstrate_interference()
