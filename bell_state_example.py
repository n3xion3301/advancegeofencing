import json
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler

# Load config
with open('config/ibm_quantum_config.json', 'r') as f:
    config = json.load(f)

# Connect to IBM Quantum
service = QiskitRuntimeService(channel="ibm_quantum")

# Create Bell state circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

print("Circuit created:")
print(qc)

# Run on simulator or specified backend
backend_name = config.get('backend', 'ibmq_qasm_simulator')
try:
    backend = service.backend(backend_name)
    print(f"Using backend: {backend_name}")
except:
    print(f"Backend {backend_name} not available, using simulator")
    backend = service.backend('ibmq_qasm_simulator')

sampler = Sampler(backend)
job = sampler.run(qc, shots=config.get('shots', 1024))
print(f"Job ID: {job.job_id()}")
result = job.result()
print(f"Results: {result}")
