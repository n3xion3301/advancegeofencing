#!/usr/bin/env python3
"""
ENHANCED QUANTUM CIRCUITS MEGA
Advanced Quantum Circuit Creation and Visualization System

ENHANCEMENTS:
- Beautiful quantum circuit diagrams
- Bell state visualizations
- GHZ state displays
- Quantum teleportation protocol art
- Entanglement visualizations
- Qubit state representations
- Gate operation diagrams
- Comprehensive circuit analysis
"""

import numpy as np
from datetime import datetime
from pathlib import Path
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector
import warnings
warnings.filterwarnings('ignore')


class QuantumCircuitsMegaEnhanced:
    """Enhanced Quantum Circuits Mega System"""
    
    def __init__(self):
        self.sampler = StatevectorSampler()
        self.circuits = []
        
        self.log_dir = Path("logs/circuits")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self._print_banner()
    
    def _print_banner(self):
        """Print stunning quantum circuits banner with ASCII art"""
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║         ✧･ﾟ: *✧･ﾟ:* QUANTUM CIRCUITS MEGA ENHANCED *:･ﾟ✧*:･ﾟ✧          ║
║            Advanced Quantum Circuit Creation System                      ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

                    ╔════════════════════════════════╗
                    ║                                ║
                    ║   ⚛️  QUANTUM CIRCUITS ⚛️      ║
                    ║                                ║
                    ║    |0⟩ ──[H]──●──────[M]      ║
                    ║               │               ║
                    ║    |0⟩ ───────⊕──────[M]      ║
                    ║                                ║
                    ║    BELL STATE CIRCUIT          ║
                    ║                                ║
                    ║    ┌──────────────────┐       ║
                    ║    │  ENTANGLEMENT    │       ║
                    ║    │   GENERATOR      │       ║
                    ║    └──────────────────┘       ║
                    ║                                ║
                    ║  [●] ACTIVE  [◉] CREATING     ║
                    ║                                ║
                    ╚════════════════════════════════╝

        ┌────────────────────────────────────────────────────┐
        │  🔬 CIRCUIT SPECIFICATIONS                          │
        ├────────────────────────────────────────────────────┤
        │  • Bell States: Enabled                            │
        │  • GHZ States: Enabled                             │
        │  • Quantum Teleportation: Enabled                  │
        │  • Circuits Created: 0                             │
        └────────────────────────────────────────────────────┘
        """)
    
    def print_bell_state_diagram(self):
        """Print Bell state circuit diagram"""
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                      🔔 BELL STATE CIRCUIT 🔔                             ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  Circuit Diagram:                                                        ║
║                                                                          ║
║    q₀: |0⟩ ──[H]──●──────[M]──                                          ║
║                   │                                                      ║
║    q₁: |0⟩ ───────⊕──────[M]──                                          ║
║                                                                          ║
║  Gates:                                                                  ║
║    [H]  = Hadamard Gate (Superposition)                                 ║
║    ●─⊕  = CNOT Gate (Entanglement)                                      ║
║    [M]  = Measurement                                                    ║
║                                                                          ║
║  Entanglement Visualization:                                             ║
║                                                                          ║
║         |0⟩                    |1⟩                                       ║
║          ↑                      ↑                                        ║
║          │                      │                                        ║
║          │    ╭────────────╮    │                                        ║
║          │    │            │    │                                        ║
║          └────┤ ENTANGLED  ├────┘                                        ║
║               │   PAIR     │                                             ║
║               ╰────────────╯                                             ║
║                                                                          ║
║  Result: |Φ⁺⟩ = (|00⟩ + |11⟩)/√2                                         ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
        """)
    
    def log(self, msg):
        """Log message with timestamp"""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{ts}] {msg}"
        print(formatted)
        
        try:
            log_file = self.log_dir / "circuits.log"
            with open(log_file, 'a') as f:
                f.write(formatted + "\n")
        except Exception:
            pass
    
    def create_bell_state(self):
        """
        Create Bell state (entangled pair)
        
        Returns:
            QuantumCircuit: Bell state circuit
        """
        
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                    🔔 CREATING BELL STATE 🔔                              ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
        """)
        
        print("║  Step 1: Initialize 2 qubits in |0⟩ state".ljust(76) + "║")
        print("║  Step 2: Apply Hadamard gate to qubit 0".ljust(76) + "║")
        print("║  Step 3: Apply CNOT gate (control=0, target=1)".ljust(76) + "║")
        print("║  Step 4: Measure both qubits".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")
        
        # Show diagram
        self.print_bell_state_diagram()
        
        # Create circuit
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure_all()
        
        self.circuits.append({
            'name': 'Bell State',
            'circuit': qc,
            'qubits': 2,
            'type': 'entanglement'
        })
        
        self.log("🔔 Bell state circuit created")
        
        return qc
    
    def print_ghz_state_diagram(self, num_qubits=3):
        """Print GHZ state circuit diagram"""
        
        print(f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                      🌟 GHZ STATE CIRCUIT 🌟                              ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  Circuit Diagram ({num_qubits} qubits):                                  ║
║                                                                          ║
        """)
        
        # Draw circuit for each qubit
        print("║    q₀: |0⟩ ──[H]──●──────●──────●──────[M]──".ljust(76) + "║")
        
        for i in range(1, num_qubits):
            if i == 1:
                print("║                   │                                                      ║")
                print("║    q₁: |0⟩ ───────⊕──────────────────[M]──".ljust(76) + "║")
            elif i == 2:
                print("║                          │                                               ║")
                print("║    q₂: |0⟩ ──────────────⊕──────────[M]──".ljust(76) + "║")
            else:
                print("║                                 │                                        ║")
                print(f"║    q{i}: |0⟩ ──────────────────────⊕──[M]──".ljust(76) + "║")
        
        print("║" + " "*74 + "║")
        print("║  Multi-Qubit Entanglement:".ljust(76) + "║")
        print("║" + " "*74 + "║")
        
        # Draw entanglement visualization
        print("║              ⚛️                                                              ║")
        print("║             ╱│╲                                                             ║")
        print("║            ╱ │ ╲                                                            ║")
        print("║           ╱  │  ╲                                                           ║")
        print("║          ╱   │   ╲                                                          ║")
        print("║         ⚛️────●────⚛️                                                         ║")
        
        if num_qubits > 3:
            print("║          │         │                                                        ║")
            print("║          ⚛️         ⚛️                                                        ║")
        
        print("║" + " "*74 + "║")
        print(f"║  Result: |GHZ⟩ = (|{'0'*num_qubits}⟩ + |{'1'*num_qubits}⟩)/√2".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")
    
    def create_ghz_state(self, num_qubits=3):
        """
        Create GHZ state (multi-qubit entanglement)
        
        Args:
            num_qubits: Number of qubits to entangle
        
        Returns:
            QuantumCircuit: GHZ state circuit
        """
        
        print(f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                    🌟 CREATING GHZ STATE 🌟                               ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
        """)
        
        print(f"║  Qubits: {num_qubits}".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("║  Step 1: Initialize all qubits in |0⟩ state".ljust(76) + "║")
        print("║  Step 2: Apply Hadamard gate to qubit 0".ljust(76) + "║")
        print("║  Step 3: Apply CNOT gates from qubit 0 to all others".ljust(76) + "║")
        print("║  Step 4: Measure all qubits".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")
        
        # Show diagram
        self.print_ghz_state_diagram(num_qubits)
        
        # Create circuit
        qc = QuantumCircuit(num_qubits)
        qc.h(0)
        for i in range(1, num_qubits):
            qc.cx(0, i)
        qc.measure_all()
        
        self.circuits.append({
            'name': f'GHZ State ({num_qubits} qubits)',
            'circuit': qc,
            'qubits': num_qubits,
            'type': 'multi-entanglement'
        })
        
        self.log(f"🌟 GHZ state circuit created with {num_qubits} qubits")
        
        return qc
    
    def print_teleportation_diagram(self):
        """Print quantum teleportation protocol diagram"""
        
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                  📡 QUANTUM TELEPORTATION PROTOCOL 📡                     ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  Circuit Diagram:                                                        ║
║                                                                          ║
║    q₀: |ψ⟩ ──────●──[H]──[M]──                                          ║
║                  │                                                       ║
║    q₁: |0⟩ ──[H]─⊕───────[M]──                                          ║
║                  │                                                       ║
║    q₂: |0⟩ ──────⊕────────────[X]──[Z]──                                ║
║                                                                          ║
║  Protocol Steps:                                                         ║
║                                                                          ║
║    ALICE                    CHANNEL                    BOB               ║
║   ┌──────┐                                          ┌──────┐            ║
║   │  |ψ⟩ │                                          │      │            ║
║   │      │                                          │      │            ║
║   │  q₀  │──────────────────────────────────────────│  q₂  │            ║
║   │      │         Entangled Pair                   │      │            ║
║   │  q₁  │──────────────────────────────────────────│      │            ║
║   │      │                                          │      │            ║
║   └──────┘                                          └──────┘            ║
║      │                                                 ▲                 ║
║      │                                                 │                 ║
║      └─────────── Classical Bits ─────────────────────┘                 ║
║                                                                          ║
║  Result: State |ψ⟩ transferred from Alice to Bob!                       ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
        """)
    
    def quantum_teleportation(self):
        """
        Create quantum teleportation circuit
        
        Returns:
            QuantumCircuit: Teleportation circuit
        """
        
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                📡 CREATING TELEPORTATION CIRCUIT 📡                       ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
        """)
        
        print("║  Step 1: Prepare state to teleport on qubit 0".ljust(76) + "║")
        print("║  Step 2: Create Bell pair (qubits 1 and 2)".ljust(76) + "║")
        print("║  Step 3: Apply CNOT and Hadamard gates".ljust(76) + "║")
        print("║  Step 4: Measure qubits 0 and 1".ljust(76) + "║")
        print("║  Step 5: Apply corrections to qubit 2".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")
        
        # Show diagram
        self.print_teleportation_diagram()
        
        # Create circuit
        qc = QuantumCircuit(3, 2)
        
        # Prepare state to teleport (example: |+⟩ state)
        qc.h(0)
        
        # Create Bell pair
        qc.h(1)
        qc.cx(1, 2)
        
        # Bell measurement
        qc.cx(0, 1)
        qc.h(0)
        qc.measure([0, 1], [0, 1])
        
        # Apply corrections
        qc.cx(1, 2)
        qc.cz(0, 2)
        
        self.circuits.append({
            'name': 'Quantum Teleportation',
            'circuit': qc,
            'qubits': 3,
            'type': 'teleportation'
        })
        
        self.log("📡 Quantum teleportation circuit created")
        
        return qc
    
    def display_circuits(self):
        """Display all created circuits with beautiful ASCII art"""
        
        if not self.circuits:
            print("\n⚠️  No circuits created yet")
            return
        
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                        📚 CIRCUIT LIBRARY 📚                              ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
        """)
        
        print(f"║  Total Circuits: {len(self.circuits)}".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")
        
        # Display each circuit
        for i, circ_info in enumerate(self.circuits, 1):
            name = circ_info['name']
            qubits = circ_info['qubits']
            circ_type = circ_info['type']
            
            print(f"""
┌────────────────────────────────────────────────────────────────────────┐
│  ⚛️  CIRCUIT #{i}                                                       │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Name: {name[:50]:50s}  │
│  Qubits: {qubits}                                                      │
│  Type: {circ_type[:50]:50s}  │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────┐     │
│  │                                                              │     │
│  │    ⚛️  QUANTUM CIRCUIT ⚛️                                     │     │
│  │                                                              │     │
│  │    |0⟩ ──[H]──●──────[M]──                                  │     │
│  │               │                                              │     │
│  │    |0⟩ ───────⊕──────[M]──                                  │     │
│  │                                                              │     │
│  │    ╭────────────────────╮                                   │     │
│  │    │   ENTANGLEMENT     │                                   │     │
│  │    │    GENERATOR       │                                   │     │
│  │    ╰────────────────────╯                                   │     │
│  │                                                              │     │
│  └──────────────────────────────────────────────────────────────┘     │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
            """)
    
    def visualize_statistics(self):
        """Visualize circuit statistics"""
        
        if not self.circuits:
            print("\n⚠️  No statistics available yet")
            return
        
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                      📊 CIRCUIT STATISTICS 📊                             ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
        """)
        
        total_circuits = len(self.circuits)
        total_qubits = sum(c['qubits'] for c in self.circuits)
        avg_qubits = total_qubits / total_circuits if total_circuits > 0 else 0
        
        print(f"║  Total Circuits Created: {total_circuits}".ljust(76) + "║")
        print(f"║  Total Qubits Used: {total_qubits}".ljust(76) + "║")
        print(f"║  Average Qubits per Circuit: {avg_qubits:.1f}".ljust(76) + "║")
        print("║" + " "*74 + "║")
        
        # Circuit type distribution
        from collections import Counter
        type_counts = Counter(c['type'] for c in self.circuits)
        
        print("║  📊 Circuit Type Distribution:".ljust(76) + "║")
        print("║" + " "*74 + "║")
        
        for circ_type, count in type_counts.items():
            bar_len = int((count / total_circuits) * 40)
            bar = "█" * bar_len + "░" * (40 - bar_len)
            print(f"║  {circ_type[:15]:15s}│{bar}│ {count}".ljust(76) + "║")
        
        print("║" + " "*74 + "║")
        
        # Circuit timeline
        print("║  🔬 Circuit Creation Timeline:".ljust(76) + "║")
        print("║" + " "*74 + "║")
        
        timeline = "  "
        for i in range(min(total_circuits, 20)):
            timeline += "⚛️"
        
        print(f"║{timeline}".ljust(76) + "║")
        print("║" + " "*74 + "║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")


def demo_quantum_circuits():
    """Stunning demonstration of Quantum Circuits Mega"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║══════════════════════════════════════════════════════════════════════════║
║                  ⚛️  QUANTUM CIRCUITS MEGA DEMONSTRATION ⚛️               ║
║══════════════════════════════════════════════════════════════════════════║
╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize
    circuits = QuantumCircuitsMegaEnhanced()
    
    # Test 1: Create Bell state
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 1: CREATE BELL STATE ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    bell_circuit = circuits.create_bell_state()
    
    # Test 2: Create GHZ state (3 qubits)
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 2: CREATE GHZ STATE (3 QUBITS) ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    ghz_circuit = circuits.create_ghz_state(3)
    
    # Test 3: Create GHZ state (4 qubits)
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 3: CREATE GHZ STATE (4 QUBITS) ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    ghz4_circuit = circuits.create_ghz_state(4)
    
    # Test 4: Create quantum teleportation
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 4: CREATE QUANTUM TELEPORTATION ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    teleport_circuit = circuits.quantum_teleportation()
    
    # Test 5: Display all circuits
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 5: CIRCUIT LIBRARY ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    circuits.display_circuits()
    
    # Test 6: Statistics
    print("\n" + "┏" + "━"*74 + "┓")
    print("┃" + " TEST 6: STATISTICS ".center(74) + "┃")
    print("┗" + "━"*74 + "┛")
    
    circuits.visualize_statistics()
    
    # Final summary
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                        ✅ DEMONSTRATION COMPLETE! ✅                       ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  Features Demonstrated:                                                  ║
║    ✨ Beautiful quantum circuit diagrams                                  ║
║    ✨ Bell state creation and visualization                               ║
║    ✨ GHZ state multi-qubit entanglement                                  ║
║    ✨ Quantum teleportation protocol                                      ║
║    ✨ Circuit library management                                          ║
║    ✨ Comprehensive statistics                                            ║
║    ✨ Entanglement visualizations                                         ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    demo_quantum_circuits()
