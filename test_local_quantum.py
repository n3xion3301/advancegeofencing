from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# Build Bell state (entangled qubits)
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Run locally (no API needed!)
sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
print(result[0].data.meas.get_counts())
