#!/usr/bin/env python3
"""
Quantum Helpers - Utility functions for quantum circuits
"""
from aer_simulator import AerSimulator

def get_real_quantum_backend():
    """Get quantum backend (Pure Python Aer)"""
    return AerSimulator()

def run_quantum_circuit(circuit, backend=None, shots=1024):
    """Run quantum circuit and return results"""
    if backend is None:
        backend = get_real_quantum_backend()
    
    result = backend.run(circuit, shots=shots)
    return result

def format_quantum_output(counts):
    """Format quantum measurement counts for display"""
    if not counts:
        return "No results"
    
    # Sort by count (descending)
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
    output = []
    total = sum(counts.values())
    
    for state, count in sorted_counts[:10]:  # Top 10 results
        percentage = (count / total) * 100
        bar = '█' * int(percentage / 2)
        output.append(f"  |{state}⟩: {count:4d} ({percentage:5.1f}%) {bar}")
    
    return '\n'.join(output)

if __name__ == "__main__":
    from qiskit import QuantumCircuit
    
    # Test
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    backend = get_real_quantum_backend()
    result = run_quantum_circuit(qc, backend, shots=1000)
    
    print("🧪 Testing quantum_helpers:")
    print(format_quantum_output(result.get_counts()))
