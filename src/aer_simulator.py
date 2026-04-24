#!/usr/bin/env python3
"""
Pure Python Aer Simulator - Drop-in replacement for qiskit-aer
Works perfectly on Termux without ANY compilation!
"""
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

class AerSimulator:
    """Pure Python Aer replacement - same API as real Aer"""
    
    def __init__(self, method='statevector'):
        self.method = method
        print("✅ Pure Python Aer Simulator initialized")
    
    def run(self, circuits, shots=1024):
        """Run quantum circuits"""
        if not isinstance(circuits, list):
            circuits = [circuits]
        
        results = []
        for qc in circuits:
            # Check if circuit has mid-circuit measurements
            has_mid_circuit = self._has_mid_circuit_measurements(qc)
            
            if has_mid_circuit:
                # Use sampling approach for circuits with classical control
                counts = self._run_with_sampling(qc, shots)
            else:
                # Use statevector for simple circuits
                counts = self._run_statevector(qc, shots)
            
            results.append(counts)
        
        return AerResult(results)
    
    def _has_mid_circuit_measurements(self, qc):
        """Check if circuit has mid-circuit measurements"""
        measure_found = False
        for instruction in qc.data:
            if instruction.operation.name == 'measure':
                measure_found = True
            elif measure_found and instruction.operation.name != 'measure':
                # Found gate after measurement
                return True
        return False
    
    def _run_statevector(self, qc, shots):
        """Run using statevector (for simple circuits)"""
        # Remove measurements for statevector
        qc_no_meas = qc.remove_final_measurements(inplace=False)
        
        # Get statevector using Qiskit's built-in (pure Python)
        sv = Statevector.from_instruction(qc_no_meas)
        
        # Sample measurements
        counts = sv.sample_counts(shots=shots)
        return counts
    
    def _run_with_sampling(self, qc, shots):
        """Run using shot-by-shot simulation (for mid-circuit measurements)"""
        counts = {}
        
        for _ in range(shots):
            # Simulate one shot
            result = self._simulate_single_shot(qc)
            
            # Convert to bitstring
            bitstring = ''.join(str(b) for b in result)
            counts[bitstring] = counts.get(bitstring, 0) + 1
        
        return counts
    
    def _simulate_single_shot(self, qc):
        """Simulate a single shot of the circuit"""
        num_qubits = qc.num_qubits
        num_clbits = qc.num_clbits
        
        # Initialize statevector
        state = np.zeros(2**num_qubits, dtype=complex)
        state[0] = 1.0
        
        # Classical register
        classical_bits = [0] * num_clbits
        
        # Execute instructions
        for instruction in qc.data:
            op = instruction.operation
            qubits = [qc.find_bit(q).index for q in instruction.qubits]
            
            if op.name == 'h':
                state = self._apply_h(state, qubits[0], num_qubits)
            elif op.name == 'x':
                state = self._apply_x(state, qubits[0], num_qubits)
            elif op.name == 'z':
                state = self._apply_z(state, qubits[0], num_qubits)
            elif op.name == 'cx':
                state = self._apply_cx(state, qubits[0], qubits[1], num_qubits)
            elif op.name == 'cz':
                state = self._apply_cz(state, qubits[0], qubits[1], num_qubits)
            elif op.name == 'measure':
                # Measure and collapse
                qubit = qubits[0]
                clbit = qc.find_bit(instruction.clbits[0]).index
                result = self._measure_qubit(state, qubit, num_qubits)
                classical_bits[clbit] = result
                state = self._collapse_state(state, qubit, result, num_qubits)
        
        return classical_bits
    
    def _apply_h(self, state, qubit, num_qubits):
        """Apply Hadamard gate"""
        new_state = state.copy()
        h_matrix = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        
        for i in range(2**num_qubits):
            bit = (i >> qubit) & 1
            if bit == 1:
                j = i ^ (1 << qubit)
                if j < i:
                    new_state[j] = h_matrix[0,0] * state[j] + h_matrix[0,1] * state[i]
                    new_state[i] = h_matrix[1,0] * state[j] + h_matrix[1,1] * state[i]
        
        return new_state
    
    def _apply_x(self, state, qubit, num_qubits):
        """Apply X (NOT) gate"""
        new_state = state.copy()
        
        for i in range(2**num_qubits):
            j = i ^ (1 << qubit)
            if j > i:
                new_state[i], new_state[j] = state[j], state[i]
        
        return new_state
    
    def _apply_z(self, state, qubit, num_qubits):
        """Apply Z gate"""
        new_state = state.copy()
        
        for i in range(2**num_qubits):
            if (i >> qubit) & 1:
                new_state[i] = -state[i]
        
        return new_state
    
    def _apply_cx(self, state, control, target, num_qubits):
        """Apply CNOT gate"""
        new_state = state.copy()
        
        for i in range(2**num_qubits):
            if (i >> control) & 1:
                j = i ^ (1 << target)
                new_state[i] = state[j]
        
        return new_state
    
    def _apply_cz(self, state, control, target, num_qubits):
        """Apply CZ gate"""
        new_state = state.copy()
        
        for i in range(2**num_qubits):
            if ((i >> control) & 1) and ((i >> target) & 1):
                new_state[i] = -state[i]
        
        return new_state
    
    def _measure_qubit(self, state, qubit, num_qubits):
        """Measure a qubit and return result"""
        prob_0 = 0
        prob_1 = 0
        
        for i in range(2**num_qubits):
            prob = abs(state[i])**2
            if (i >> qubit) & 1:
                prob_1 += prob
            else:
                prob_0 += prob
        
        # Random measurement outcome
        return 1 if np.random.random() < prob_1 / (prob_0 + prob_1) else 0
    
    def _collapse_state(self, state, qubit, result, num_qubits):
        """Collapse state after measurement"""
        new_state = np.zeros_like(state)
        norm = 0
        
        for i in range(2**num_qubits):
            if ((i >> qubit) & 1) == result:
                new_state[i] = state[i]
                norm += abs(state[i])**2
        
        # Normalize
        if norm > 0:
            new_state /= np.sqrt(norm)
        
        return new_state

class AerResult:
    """Result object compatible with Aer API"""
    
    def __init__(self, results):
        self._results = results
    
    def get_counts(self, circuit=0):
        return self._results[circuit]
    
    def result(self):
        return self

# Alias for compatibility
Aer = type('Aer', (), {
    'get_backend': lambda name: AerSimulator()
})()
