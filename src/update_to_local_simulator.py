import os
import re

files = [
    "quantum_erasure.py",
    "quantum_chromodynamics.py", 
    "quantum_cloning.py",
    "quantum_vacuum_energy.py",
    "quantum_field_theory.py",
    "decaying.py"
]

for filename in files:
    if not os.path.exists(filename):
        continue
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # Replace runtime service with local simulator
    content = content.replace(
        'from qiskit_ibm_runtime import QiskitRuntimeService',
        'from qiskit.primitives import StatevectorSampler, StatevectorEstimator'
    )
    
    content = content.replace(
        'service = QiskitRuntimeService(channel="ibm_quantum")',
        '# Using local simulator - no API needed'
    )
    
    content = content.replace(
        'service.backend("ibmq_qasm_simulator")',
        'StatevectorSampler()'
    )
    
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"✓ Updated {filename}")

print("\nAll scripts now use local simulator!")
