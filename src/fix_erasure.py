#!/usr/bin/env python3
import sys
sys.path.insert(0, '/data/data/com.termux/files/home/advancegeofencing')

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# Simple working version
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Use StatevectorSampler
sampler = StatevectorSampler()
job = sampler.run([qc], shots=100)
result = job.result()

print("✅ Quantum Erasure Results:")
print(result)
print("\nCounts:")
print(result[0].data)
