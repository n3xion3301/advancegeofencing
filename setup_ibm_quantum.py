#!/usr/bin/env python3
"""IBM Quantum Setup and Test"""
from qiskit_ibm_runtime import QiskitRuntimeService

print("="*80)
print("IBM QUANTUM CONNECTION TEST")
print("="*80)

try:
    # Connect using saved credentials
    service = QiskitRuntimeService(channel='ibm_quantum_platform')
    
    print("\n✅ Connected to IBM Quantum!")
    
    # Get available backends
    backends = service.backends()
    
    print(f"\n📡 Available Quantum Backends: {len(backends)}")
    print("-"*80)
    
    for backend in backends[:5]:  # Show first 5
        status = backend.status()
        
        print(f"\n🖥️  {backend.name}")
        print(f"   Qubits: {backend.num_qubits}")
        print(f"   Status: {'🟢 Online' if status.operational else '🔴 Offline'}")
        print(f"   Pending jobs: {status.pending_jobs}")
    
    print("\n" + "="*80)
    print("✅ CONNECTED TO REAL QUANTUM HARDWARE!")
    print("="*80)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
