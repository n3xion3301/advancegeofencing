#!/usr/bin/env python3
"""
Enhanced Wave Function Collapse Simulator
Visualizes quantum measurement and superposition collapse
"""
import numpy as np
from qiskit import QuantumCircuit
from aer_simulator import AerSimulator
import time

class WaveFunctionCollapseVisualizer:
    def __init__(self):
        print("🌊 WAVE FUNCTION COLLAPSE SIMULATOR")
        print("="*70)
        print("Demonstrating quantum superposition and measurement")
        print("="*70)
    
    def simulate_collapse(self, num_qubits=2):
        """Simulate wave function collapse"""
        
        print(f"\n📊 SYSTEM PARAMETERS:")
        print(f"   Number of Qubits: {num_qubits}")
        print(f"   Hilbert Space Dimension: {2**num_qubits}")
        print(f"   Possible States: {2**num_qubits}")
        
        # Before measurement
        print("\n🎨 BEFORE MEASUREMENT (Superposition):")
        self.draw_superposition(num_qubits)
        
        # Create quantum circuit
        qc = self.create_superposition_circuit(num_qubits)
        
        print("\n⚛️  QUANTUM CIRCUIT:")
        print(qc.draw(output='text'))
        
        # Simulate
        print("\n⏳ Performing measurement...")
        time.sleep(1)
        
        sim = AerSimulator()
        result = sim.run(qc, shots=1000)
        counts = result.get_counts()
        
        # After measurement
        print("\n🎯 AFTER MEASUREMENT (Collapsed):")
        self.draw_collapsed(counts)
        
        print("\n📈 MEASUREMENT STATISTICS:")
        self.display_results(counts, num_qubits)
        
        return counts
    
    def draw_superposition(self, num_qubits):
        """Draw wave function in superposition"""
        print()
        print("   Wave Function: |ψ⟩ = Σ αᵢ|i⟩")
        print()
        print("   State Space (all states exist simultaneously):")
        print("   ┌─────────────────────────────────────┐")
        
        states = [format(i, f'0{num_qubits}b') for i in range(2**num_qubits)]
        
        for i, state in enumerate(states):
            amplitude = 1/np.sqrt(2**num_qubits)
            prob = amplitude**2
            
            # Wave visualization
            wave = "~" * int(prob * 40)
            print(f"   │ |{state}⟩  {wave:40s} │ α={amplitude:.3f}")
        
        print("   └─────────────────────────────────────┘")
        print()
        print("   ✨ All states coexist in superposition!")
        print("   📊 Each state has equal probability")
        print()
    
    def draw_collapsed(self, counts):
        """Draw collapsed wave function"""
        print()
        print("   Wave Function COLLAPSED to definite state!")
        print()
        
        # Find most common state
        max_state = max(counts, key=counts.get)
        
        print("   ┌─────────────────────────────────────┐")
        print(f"  │                                     │")
        print(f"  │     COLLAPSED TO: |{max_state}⟩     │")
        print(f"  │                                     │")
        print(f"  │              ████████               │")
        print(f"  │              ████████               │")
        print(f"  │              ████████               │")
        print(f"  │         ─────────────────           │")
        print("   │                                     │")
        print("   └─────────────────────────────────────┘")
        print()
        print("   ⚡ Measurement forced the system into ONE state!")
        print("   🎲 The outcome was probabilistic")
        print()
    
    def create_superposition_circuit(self, num_qubits):
        """Create circuit with superposition"""
        qc = QuantumCircuit(num_qubits, num_qubits)
        
        # Create equal superposition
        for i in range(num_qubits):
            qc.h(i)
        
        # Add some entanglement
        for i in range(num_qubits - 1):
            qc.cx(i, i + 1)
        
        # Measure (causes collapse!)
        qc.measure(range(num_qubits), range(num_qubits))
        
        return qc
    
    def display_results(self, counts, num_qubits):
        """Display measurement results"""
        total = sum(counts.values())
        
        print("\n   State   | Count | Probability | Visualization")
        print("   " + "─"*70)
        
        # Sort by count
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        
        for state, count in sorted_counts:
            prob = count / total
            bar = '█' * int(prob * 40)
            
            print(f"   |{state}⟩  | {count:4d}  | {prob:6.1%}  {bar}")
        
        print("\n   " + "─"*70)
        
        # Calculate entropy
        entropy = -sum((c/total) * np.log2(c/total) for c in counts.values() if c > 0)
        max_entropy = num_qubits
        
        print(f"\n   Shannon Entropy: {entropy:.3f} bits")
        print(f"   Maximum Entropy: {max_entropy:.3f} bits")
        print(f"   Randomness: {entropy/max_entropy:.1%}")
        
        # Physics explanation
        print("\n💡 PHYSICS EXPLANATION:")
        print()
        print("   BEFORE MEASUREMENT:")
        print("   • System exists in superposition of ALL states")
        print("   • Wave function |ψ⟩ = Σ αᵢ|i⟩")
        print("   • No definite value - only probabilities")
        print()
        print("   DURING MEASUREMENT:")
        print("   • Observer interacts with quantum system")
        print("   • Wave function instantaneously collapses")
        print("   • Decoherence destroys superposition")
        print()
        print("   AFTER MEASUREMENT:")
        print("   • System in ONE definite eigenstate")
        print("   • Probability |αᵢ|² determines outcome")
        print("   • Information gained, entropy reduced")
        print()
        print("   🎯 This is the MEASUREMENT PROBLEM!")
        print("   🤔 Why does observation cause collapse?")
        print("   🌌 Still debated in quantum foundations!")

if __name__ == "__main__":
    viz = WaveFunctionCollapseVisualizer()
    
    print("\n🚀 Starting wave function collapse simulation...")
    time.sleep(1)
    
    # Simulate 3-qubit system
    viz.simulate_collapse(num_qubits=3)
    
    print("\n✅ Simulation complete!")
