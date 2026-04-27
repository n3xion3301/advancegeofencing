with open('quantum_axiom_key.py', 'r') as f:
    content = f.read()

# Replace IBM Runtime with local simulator
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

# Backup original
with open('quantum_axiom_key.py.bak', 'w') as f:
    f.write(open('quantum_axiom_key.py').read())

# Write fixed version
with open('quantum_axiom_key.py', 'w') as f:
    f.write(content)

print("✓ Fixed quantum_axiom_key.py")
