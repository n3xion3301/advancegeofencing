"""
Quantum tunneling simulation for detecting unusual geofence penetrations
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
import numpy as np

class QuantumTunnelingDetector:
    def __init__(self):
        self.sampler = StatevectorSampler()
    
    def simulate_barrier_penetration(self, barrier_strength, energy_level):
        """
        Simulate quantum tunneling through geofence barrier
        
        barrier_strength: 0-1 (security level)
        energy_level: 0-1 (penetration attempt strength)
        
        Returns probability of successful penetration
        """
        qc = QuantumCircuit(2)
        
        # Qubit 0: barrier state
        # Qubit 1: penetration attempt
        
        # Initialize barrier
        barrier_angle = barrier_strength * np.pi
        qc.ry(barrier_angle, 0)
        
        # Initialize penetration attempt
        energy_angle = energy_level * np.pi
        qc.ry(energy_angle, 1)
        
        # Quantum tunneling interaction
        qc.cx(1, 0)  # Attempt affects barrier
        qc.h(0)      # Superposition allows tunneling
        qc.cx(0, 1)  # Barrier affects outcome
        
        qc.measure_all()
        
        result = self.sampler.run([qc], shots=1000).result()
        counts = result[0].data.meas.get_counts()
        
        # State '11' represents successful penetration
        penetration_count = counts.get('11', 0)
        tunneling_probability = penetration_count / 1000
        
        return {
            'tunneling_probability': tunneling_probability,
            'barrier_strength': barrier_strength,
            'energy_level': energy_level,
            'alert_level': 'HIGH' if tunneling_probability > 0.3 else 'NORMAL'
        }

# Example usage
if __name__ == "__main__":
    detector = QuantumTunnelingDetector()
    
    # Test different scenarios
    scenarios = [
        (0.9, 0.2),  # Strong barrier, weak attempt
        (0.5, 0.8),  # Medium barrier, strong attempt
        (0.3, 0.9),  # Weak barrier, very strong attempt
    ]
    
    for barrier, energy in scenarios:
        result = detector.simulate_barrier_penetration(barrier, energy)
        print(f"\nBarrier: {barrier:.1f}, Energy: {energy:.1f}")
        print(f"Tunneling Probability: {result['tunneling_probability']:.2%}")
        print(f"Alert Level: {result['alert_level']}")
