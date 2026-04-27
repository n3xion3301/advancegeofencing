from qiskit_ibm_runtime import QiskitRuntimeService

# Connect to IBM Quantum
service = QiskitRuntimeService(channel="ibm_quantum")

# List all available backends
print("Available backends:")
print("-" * 50)
for backend in service.backends():
    status = backend.status()
    print(f"Name: {backend.name}")
    print(f"  Qubits: {backend.num_qubits}")
    print(f"  Operational: {status.operational}")
    print(f"  Pending jobs: {status.pending_jobs}")
    print()
