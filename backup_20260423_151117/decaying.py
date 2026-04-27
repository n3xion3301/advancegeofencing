"""
Quantum Decay Simulation
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
import numpy as np

class QuantumDecaySimulator:
    def __init__(self):
        self.sampler = StatevectorSampler()
    
    def simulate_decay(self, initial_state=1, decay_rate=0.1, time_steps=10):
        """Simulate quantum state decay"""
        results = []
        
        for t in range(time_steps):
            qc = QuantumCircuit(1)
            
            if initial_state == 1:
                qc.x(0)
            
            theta = decay_rate * t * np.pi
            qc.ry(theta, 0)
            qc.measure_all()
            
            job = self.sampler.run([qc], shots=100)
            result = job.result()
            counts = result[0].data.meas.get_counts()
            
            prob_excited = counts.get('1', 0) / 100
            
            results.append({
                'time': t,
                'probability': prob_excited,
                'counts': counts
            })
        
        return results
    
    def calculate_entropy(self, counts):
        """Calculate Shannon entropy"""
        total = sum(counts.values())
        entropy = 0
        
        for count in counts.values():
            if count > 0:
                p = count / total
                entropy -= p * np.log2(p)
        
        return entropy

if __name__ == "__main__":
    print("🔬 Quantum Decay Simulation\n")
    
    simulator = QuantumDecaySimulator()
    results = simulator.simulate_decay(initial_state=1, decay_rate=0.15, time_steps=10)
    
    print("Time Step | Probability |1⟩ | Entropy")
    print("-" * 45)
    
    for r in results:
        entropy = simulator.calculate_entropy(r['counts'])
        print(f"    {r['time']:2d}    |     {r['probability']:.3f}      | {entropy:.3f}")
    
    print("\n✅ Decay simulation complete!")
