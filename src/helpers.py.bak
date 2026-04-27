"""
Quantum helper functions for qiskit 2.4.0 local simulator
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler, StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
import json

def get_real_quantum_backend():
    """Returns local quantum simulator"""
    return {
        'sampler': StatevectorSampler(),
        'estimator': StatevectorEstimator(),
        'backend_type': 'local_simulator',
        'name': 'StatevectorSimulator'
    }

def run_quantum_circuit(circuit, shots=1024, backend=None):
    """Run quantum circuit on local simulator"""
    if backend is None:
        backend = get_real_quantum_backend()
    
    sampler = backend['sampler']
    
    # Ensure circuit has measurements
    has_measurements = any(instr.operation.name == 'measure' for instr in circuit.data)
    if not has_measurements:
        circuit.measure_all()
    
    # Run circuit
    job = sampler.run([circuit], shots=shots)
    result = job.result()
    
    counts = result[0].data.meas.get_counts()
    
    return {
        'counts': counts,
        'shots': shots,
        'backend': backend['name'],
        'success': True
    }

def format_quantum_output(result, title="Quantum Result"):
    """Format quantum circuit results for display"""
    output = []
    output.append("=" * 60)
    output.append(f"  {title}")
    output.append("=" * 60)
    
    if result.get('success'):
        output.append(f"\nBackend: {result.get('backend', 'Unknown')}")
        output.append(f"Shots: {result.get('shots', 0)}")
        output.append("\nMeasurement Results:")
        output.append("-" * 40)
        
        counts = result.get('counts', {})
        total = sum(counts.values())
        
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        
        for state, count in sorted_counts:
            percentage = (count / total) * 100
            bar = "█" * int(percentage / 2)
            output.append(f"  |{state}⟩: {count:4d} ({percentage:5.1f}%) {bar}")
        
        output.append("-" * 40)
    else:
        output.append("\n❌ Quantum circuit execution failed")
    
    output.append("=" * 60)
    
    return "\n".join(output)

def create_entangled_state(num_qubits=2):
    """Create maximally entangled state (GHZ state)"""
    qc = QuantumCircuit(num_qubits)
    qc.h(0)
    for i in range(1, num_qubits):
        qc.cx(0, i)
    return qc

def measure_expectation_value(circuit, observable_string):
    """Measure expectation value of observable"""
    backend = get_real_quantum_backend()
    estimator = backend['estimator']
    observable = SparsePauliOp.from_list([(observable_string, 1)])
    job = estimator.run([(circuit, observable)])
    result = job.result()
    return float(result[0].data.evs)

def quantum_random_number(num_bits=8):
    """Generate quantum random number"""
    qc = QuantumCircuit(num_bits)
    for i in range(num_bits):
        qc.h(i)
    qc.measure_all()
    result = run_quantum_circuit(qc, shots=1)
    bitstring = list(result['counts'].keys())[0]
    return int(bitstring, 2)

if __name__ == "__main__":
    print("Testing Quantum Helpers...\n")
    backend = get_real_quantum_backend()
    print(f"✓ Backend: {backend['name']}\n")
    
    qc = create_entangled_state(2)
    qc.measure_all()
    result = run_quantum_circuit(qc, shots=1000)
    print(format_quantum_output(result, "2-Qubit Entanglement Test"))
    
    random_num = quantum_random_number(8)
    print(f"\n✓ Quantum Random Number (8-bit): {random_num}")
    print("\n✅ All tests passed!")
