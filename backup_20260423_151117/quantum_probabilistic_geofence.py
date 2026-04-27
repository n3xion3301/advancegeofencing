"""
Quantum superposition for handling uncertain/fuzzy geofence boundaries
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
import numpy as np

class QuantumProbabilisticGeofence:
    def __init__(self):
        self.estimator = StatevectorEstimator()
    
    def calculate_boundary_probability(self, distance_from_center, radius, uncertainty=0.1):
        """
        Use quantum superposition to calculate probability of being inside geofence
        with fuzzy boundaries
        
        distance_from_center: meters from geofence center
        radius: geofence radius in meters
        uncertainty: boundary fuzziness factor (0-1)
        """
        # Normalize distance to 0-1 range
        normalized_distance = min(distance_from_center / (radius * (1 + uncertainty)), 1.0)
        
        # Create quantum circuit with rotation based on distance
        qc = QuantumCircuit(1)
        
        # Rotation angle determines probability
        # θ = 0 → definitely inside
        # θ = π → definitely outside
        theta = normalized_distance * np.pi
        
        qc.ry(theta, 0)
        
        # Measure in Z basis (|0⟩ = inside, |1⟩ = outside)
        observable = SparsePauliOp.from_list([("Z", 1)])
        
        job = self.estimator.run([(qc, observable)])
        result = job.result()
        expectation_value = result[0].data.evs
        
        # Convert expectation value to probability
        # E(Z) = P(0) - P(1) = 2*P(inside) - 1
        probability_inside = (expectation_value + 1) / 2
        
        return {
            'probability_inside': float(probability_inside),
            'probability_outside': float(1 - probability_inside),
            'distance': distance_from_center,
            'radius': radius,
            'uncertainty': uncertainty
        }
    
    def quantum_geofence_check(self, lat, lon, center_lat, center_lon, radius, uncertainty=0.1):
        """
        Quantum-enhanced geofence check with probabilistic boundaries
        """
        # Calculate distance (simplified Haversine)
        R = 6371000  # Earth radius in meters
        lat1, lon1 = np.radians(lat), np.radians(lon)
        lat2, lon2 = np.radians(center_lat), np.radians(center_lon)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        distance = R * c
        
        return self.calculate_boundary_probability(distance, radius, uncertainty)

# Example usage
if __name__ == "__main__":
    qgeofence = QuantumProbabilisticGeofence()
    
    # Test point near boundary
    result = qgeofence.quantum_geofence_check(
        lat=40.7128,
        lon=-74.0060,
        center_lat=40.7127,
        center_lon=-74.0059,
        radius=100,  # 100 meters
        uncertainty=0.2  # 20% fuzzy boundary
    )
    
    print("Quantum Geofence Check:")
    print(f"Probability Inside: {result['probability_inside']:.2%}")
    print(f"Probability Outside: {result['probability_outside']:.2%}")
    print(f"Distance: {result['distance']:.2f}m")
