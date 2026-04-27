import json
from qiskit_ibm_runtime import QiskitRuntimeService

# Load token from config file
with open('config/ibm_quantum_config.json', 'r') as f:
    config = json.load(f)

# Save credentials to Qiskit
QiskitRuntimeService.save_account(
    channel="ibm_quantum",
    token=config['ibm_quantum_token'],
    overwrite=True
)
print("IBM Quantum credentials saved successfully!")
