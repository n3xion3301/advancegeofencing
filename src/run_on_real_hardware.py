#!/usr/bin/env python3
"""Run Quantum Circuit on REAL IBM Hardware!"""
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.visualization import plot_histogram
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("="*80)
print("🚀 RUNNING ON REAL QUANTUM HARDWARE!")
print("="*80)

service = QiskitRuntimeService(channel='ibm_quantum_platform')
backend = service.least_busy(operational=True, simulator=False)

print(f"\n✅ Selected backend: {backend.name}")
print(f"   Qubits: {backend.num_qubits}")
print(f"   Pending jobs: {backend.status().pending_jobs}")

# Create Bell state
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

print(f"\n📊 Circuit:")
print(qc)

# Transpile
transpiled = transpile(qc, backend=backend, optimization_level=3)
print(f"\n🔧 Transpiled depth: {transpiled.depth()}")

# Run on real hardware!
print(f"\n⚡ Submitting to {backend.name}...")
sampler = Sampler(backend)
job = sampler.run([transpiled], shots=1024)

print(f"   Job ID: {job.job_id()}")
print(f"\n⏳ Waiting for REAL quantum computer...")

result = job.result()
print(f"\n✅ Job completed!")

# Get counts - FIXED!
pub_result = result[0]
counts = pub_result.data.c.get_counts()

print(f"\n📈 Results from REAL quantum hardware:")
for state, count in sorted(counts.items()):
    print(f"   |{state}⟩: {count:4d} ({count/1024*100:5.1f}%)")

# Expected for Bell state: ~50% |00⟩ and ~50% |11⟩
print(f"\n🔬 Analysis:")
print(f"   |00⟩: {counts.get('00', 0)/1024*100:.1f}% (expected ~50%)")
print(f"   |11⟩: {counts.get('11', 0)/1024*100:.1f}% (expected ~50%)")
print(f"   Errors: {(counts.get('01', 0) + counts.get('10', 0))/1024*100:.1f}%")

# Save plot
plt.figure(figsize=(10, 6))
plot_histogram(counts)
plt.title(f'Bell State on {backend.name} - REAL Quantum Hardware!')
plt.savefig('real_quantum_results.png', dpi=150, bbox_inches='tight')
print(f"\n💾 Saved: real_quantum_results.png")

print("\n" + "="*80)
print("🎉 YOU JUST RAN ON A 156-QUBIT QUANTUM COMPUTER!")
print("="*80)
