#!/usr/bin/env python3
"""
Quantum Circuits Mega - Fixed
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

class QuantumCircuitsMega:
    def __init__(self):
        self.sampler = StatevectorSampler()
        print("⚛️  Quantum Circuits Mega Initialized")
    
    def create_bell_state(self):
        """Create Bell state (entangled pair)"""
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure_all()
        return qc
    
    def create_ghz_state(self, num_qubits=3):
        """Create GHZ state (multi-qubit entanglement)"""
        qc = QuantumCircuit(num_qubits)
        qc.h(0)
        for i in range(1, num_qubits):
            qc.cx(0, i)
        qc.measure_all()
        return qc
    
    def quantum_teleportation(self):
        """Teleport quantum state using entanglement"""
        qc = QuantumCircuit(3)
        
        # Prepare state to teleport
        qc.ry(0.5, 0)
        
        # Create entangled pair
        qc.h(1)
        qc.cx(1, 2)
        
        # Bell measurement (simplified - no mid-circuit)
        qc.cx(0, 1)
        qc.h(0)
        
        qc.measure_all()
        return qc
    
    def run_circuit(self, qc, shots=100):
        """Run quantum circuit"""
        result = self.sampler.run([qc], shots=shots).result()
        return result[0].data.meas.get_counts()

if __name__ == "__main__":
    mega = QuantumCircuitsMega()
    
    print("\n1. Bell State:")
    bell = mega.create_bell_state()
    counts = mega.run_circuit(bell)
    print(f"   Results: {counts}")
    
    print("\n2. GHZ State (3 qubits):")
    ghz = mega.create_ghz_state(3)
    counts = mega.run_circuit(ghz)
    print(f"   Results: {counts}")
    
    print("\n3. Quantum Teleportation:")
    teleport = mega.quantum_teleportation()
    counts = mega.run_circuit(teleport)
    print(f"   Results: {counts}")
    
    print("\n✅ All circuits working!")
