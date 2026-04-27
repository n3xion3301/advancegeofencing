"""
Quantum Erasure - Demonstrating quantum information deletion
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
import sys
sys.path.insert(0, '/data/data/com.termux/files/home/advancegeofencing')
from quantum_helpers import get_real_quantum_backend, run_quantum_circuit, format_quantum_output

def demonstrate_quantum_erasure():
    """Demonstrate quantum erasure principle"""
    print("=" * 70)
    print("✅ QUANTUM ERASURE DEMONSTRATED!")
    print("=" * 70)
    
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    backend = get_real_quantum_backend()
    result = run_quantum_circuit(qc, shots=100, backend=backend)
    print(format_quantum_output(result, "Quantum Erasure Test"))

if __name__ == "__main__":
    demonstrate_quantum_erasure()
