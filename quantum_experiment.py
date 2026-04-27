from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# Create a simple quantum circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Use local sampler (no API needed)
sampler = StatevectorSampler()
job = sampler.run([qc], shots=1024)
result = job.result()

print("Quantum Experiment Results:")
print(result[0].data.meas.get_counts())
