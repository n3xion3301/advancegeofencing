import json
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler

# Load config
with open('config/ibm_quantum_config.json', 'r') as f:
    config = json.load(f)

# Connect to IBM Quantum
service = QiskitRuntimeService(channel="ibm_quantum")

# Create a simple quantum circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

print("Circuit:")
print(qc)

# Get least busy real quantum backend
print("\nFinding least busy quantum computer...")
backend = service.least_busy(operational=True, simulator=False)
print(f"Selected backend: {backend.name}")
print(f"Number of qubits: {backend.num_qubits}")

# Run the circuit
sampler = Sampler(backend)
job = sampler.run(qc, shots=config.get('shots', 1024))
print(f"\nJob submitted! Job ID: {job.job_id()}")
print("Waiting for results...")

result = job.result()
print(f"\nResults from {backend.name}:")
print(result)
