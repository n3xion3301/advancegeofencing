from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.visualization import plot_histogram
import matplotlib
matplotlib.use('Agg')  # For Termux
import matplotlib.pyplot as plt

# 3-qubit entanglement
qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.measure_all()

# Run locally
sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.meas.get_counts()

print(f"Results: {counts}")

# Save histogram
plot_histogram(counts)
plt.savefig('quantum_results.png')
print("Saved to quantum_results.png")
