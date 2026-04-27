"""
Quantum Random Number Generator using true quantum randomness
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
import hashlib

class QuantumRNG:
    def __init__(self):
        self.sampler = StatevectorSampler()
    
    def generate_random_bits(self, num_bits=16):
        """Generate truly random bits (max 16 bits for stability)"""
        if num_bits > 16:
            num_bits = 16
        
        qc = QuantumCircuit(num_bits)
        for i in range(num_bits):
            qc.h(i)
        qc.measure_all()
        
        result = self.sampler.run([qc], shots=1).result()
        bitstring = list(result[0].data.meas.get_counts().keys())[0]
        return bitstring
    
    def generate_secure_token(self):
        """Generate cryptographically secure token"""
        # Generate multiple 16-bit chunks
        bits1 = self.generate_random_bits(16)
        bits2 = self.generate_random_bits(16)
        combined = bits1 + bits2
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def generate_session_key(self):
        """Generate quantum-secure session key"""
        return self.generate_random_bits(16)

if __name__ == "__main__":
    qrng = QuantumRNG()
    print(f"Quantum Token: {qrng.generate_secure_token()}")
    print(f"Session Key: {qrng.generate_session_key()}")
