#!/usr/bin/env python3
import os
import re

files_to_fix = [
    'quantum_teleportation_detector.py',
    'quantum_teleportation_network.py',
    'src/quantum_erasure.py',
    'src/quantum_chromodynamics.py',
    'src/quantum_cloning.py',
    'src/quantum_vacuum_energy.py',
    'src/quantum_field_theory.py',
    'src/upgrade_qiskit_scripts.py',
    'src/decaying.py',
    'quantum_axiom_key.py'
]

def fix_file(filepath):
    """Replace qiskit-aer references with IBM Runtime equivalents"""
    if not os.path.exists(filepath):
        print(f"Skipping {filepath} - file not found")
        return False
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # Replace old Aer imports
    content = re.sub(
        r'from qiskit import QuantumCircuit, Aer, execute',
        'from qiskit import QuantumCircuit\nfrom qiskit_ibm_runtime import QiskitRuntimeService, Sampler',
        content
    )
    
    # Replace AerSimulator import
    content = re.sub(
        r'from qiskit_aer import AerSimulator',
        'from qiskit_ibm_runtime import QiskitRuntimeService',
        content
    )
    
    # Replace Aer.get_backend usage
    content = re.sub(
        r"Aer\.get_backend\(['\"]qasm_simulator['\"]\)",
        'service.backend("ibmq_qasm_simulator")',
        content
    )
    
    # Replace AerSimulator() instantiation
    content = re.sub(
        r'AerSimulator\(\)',
        'service.backend("ibmq_qasm_simulator")',
        content
    )
    
    # Replace execute() with Sampler
    content = re.sub(
        r'execute\(([^,]+),\s*backend',
        r'sampler = Sampler(backend)\njob = sampler.run(\1',
        content
    )
    
    # Add service initialization if not present and we made changes
    if content != original and 'QiskitRuntimeService()' not in content:
        # Find first function or class definition
        match = re.search(r'(def |class )', content)
        if match:
            insert_pos = match.start()
            service_init = '\n# Initialize IBM Quantum Runtime Service\nservice = QiskitRuntimeService(channel="ibm_quantum")\n\n'
            content = content[:insert_pos] + service_init + content[insert_pos:]
    
    if content != original:
        # Backup original
        backup_path = filepath + '.bak'
        with open(backup_path, 'w') as f:
            f.write(original)
        
        # Write fixed version
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"✓ Fixed: {filepath} (backup: {backup_path})")
        return True
    else:
        print(f"- No changes needed: {filepath}")
        return False

# Fix all files
print("Fixing qiskit-aer references...\n")
fixed_count = 0

for filepath in files_to_fix:
    if fix_file(filepath):
        fixed_count += 1

print(f"\n{'='*50}")
print(f"Total files fixed: {fixed_count}/{len(files_to_fix)}")
print(f"{'='*50}")
print("\nBackup files created with .bak extension")
print("Review changes and delete backups when satisfied")
