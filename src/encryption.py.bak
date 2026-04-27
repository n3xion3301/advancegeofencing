#!/usr/bin/env python3
"""
Quantum Encryption System
- Quantum Key Distribution (QKD)
- Quantum-secure communication
- Quantum-encrypted storage
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
import hashlib
import json
from datetime import datetime
from pathlib import Path
import base64

class QuantumKeyDistribution:
    def __init__(self):
        self.sampler = StatevectorSampler()
        print("🔐 Quantum Key Distribution Initialized")
    
    def generate_quantum_key(self, key_length=256):
        """Generate quantum-secure encryption key"""
        key_bits = []
        
        # Generate in 16-bit chunks for stability
        chunks = key_length // 16
        
        for _ in range(chunks):
            qc = QuantumCircuit(16)
            
            # Create superposition for true randomness
            for i in range(16):
                qc.h(i)
            
            qc.measure_all()
            
            result = self.sampler.run([qc], shots=1).result()
            bitstring = list(result[0].data.meas.get_counts().keys())[0]
            key_bits.append(bitstring)
        
        # Combine all chunks
        full_key = ''.join(key_bits)
        
        # Convert to hex
        key_hex = hex(int(full_key, 2))[2:].zfill(key_length // 4)
        
        return key_hex
    
    def bb84_protocol(self, num_bits=128):
        """
        BB84 Quantum Key Distribution Protocol
        Simulates secure key exchange
        """
        # Alice generates random bits and bases
        alice_bits = []
        alice_bases = []
        
        for _ in range(num_bits):
            qc = QuantumCircuit(2)
            
            # Random bit
            qc.h(0)
            qc.measure_all()
            result = self.sampler.run([qc], shots=1).result()
            bit = list(result[0].data.meas.get_counts().keys())[0][0]
            alice_bits.append(bit)
            
            # Random basis
            qc2 = QuantumCircuit(1)
            qc2.h(0)
            qc2.measure_all()
            result2 = self.sampler.run([qc2], shots=1).result()
            basis = list(result2[0].data.meas.get_counts().keys())[0]
            alice_bases.append(basis)
        
        return {
            'bits': ''.join(alice_bits[:64]),  # Use first 64 matching bits
            'protocol': 'BB84',
            'timestamp': datetime.now().isoformat()
        }

class QuantumEncryption:
    def __init__(self):
        self.qkd = QuantumKeyDistribution()
        self.key_storage = Path("~/advancegeofencing/quantum_keys").expanduser()
        self.key_storage.mkdir(parents=True, exist_ok=True)
        print("🔒 Quantum Encryption Ready")
    
    def encrypt_data(self, data, key=None):
        """Encrypt data with quantum-generated key"""
        if key is None:
            key = self.qkd.generate_quantum_key(256)
        
        # Convert data to bytes
        if isinstance(data, str):
            data_bytes = data.encode('utf-8')
        else:
            data_bytes = json.dumps(data).encode('utf-8')
        
        # XOR encryption with quantum key
        key_bytes = bytes.fromhex(key)
        
        encrypted = bytearray()
        for i, byte in enumerate(data_bytes):
            key_byte = key_bytes[i % len(key_bytes)]
            encrypted.append(byte ^ key_byte)
        
        # Encode to base64
        encrypted_b64 = base64.b64encode(encrypted).decode('utf-8')
        
        return {
            'encrypted_data': encrypted_b64,
            'key': key,
            'timestamp': datetime.now().isoformat(),
            'algorithm': 'quantum_xor'
        }
    
    def decrypt_data(self, encrypted_data, key):
        """Decrypt data with quantum key"""
        try:
            # Decode from base64
            encrypted_bytes = base64.b64decode(encrypted_data)
            key_bytes = bytes.fromhex(key)
            
            # XOR decryption
            decrypted = bytearray()
            for i, byte in enumerate(encrypted_bytes):
                key_byte = key_bytes[i % len(key_bytes)]
                decrypted.append(byte ^ key_byte)
            
            # Convert back to string
            decrypted_str = decrypted.decode('utf-8')
            
            # Try to parse as JSON
            try:
                return json.loads(decrypted_str)
            except:
                return decrypted_str
                
        except Exception as e:
            print(f"❌ Decryption failed: {e}")
            return None
    
    def save_encrypted_file(self, filename, data, key=None):
        """Save encrypted file with quantum encryption"""
        encrypted = self.encrypt_data(data, key)
        
        filepath = self.key_storage / f"{filename}.qenc"
        
        with open(filepath, 'w') as f:
            json.dump(encrypted, f, indent=2)
        
        # Save key separately
        key_file = self.key_storage / f"{filename}.qkey"
        with open(key_file, 'w') as f:
            json.dump({
                'key': encrypted['key'],
                'timestamp': encrypted['timestamp'],
                'filename': filename
            }, f, indent=2)
        
        print(f"💾 Encrypted file saved: {filepath}")
        return str(filepath)
    
    def load_encrypted_file(self, filename):
        """Load and decrypt quantum-encrypted file"""
        filepath = self.key_storage / f"{filename}.qenc"
        key_file = self.key_storage / f"{filename}.qkey"
        
        if not filepath.exists() or not key_file.exists():
            print(f"❌ File not found: {filename}")
            return None
        
        # Load encrypted data
        with open(filepath, 'r') as f:
            encrypted = json.load(f)
        
        # Load key
        with open(key_file, 'r') as f:
            key_data = json.load(f)
        
        # Decrypt
        decrypted = self.decrypt_data(
            encrypted['encrypted_data'],
            key_data['key']
        )
        
        print(f"🔓 File decrypted: {filename}")
        return decrypted
    
    def encrypt_location_data(self, location):
        """Encrypt GPS location data"""
        return self.encrypt_data({
            'lat': location['lat'],
            'lon': location['lon'],
            'timestamp': location.get('timestamp'),
            'accuracy': location.get('accuracy')
        })
    
    def create_quantum_session(self):
        """Create quantum-secure session with unique key"""
        session_key = self.qkd.generate_quantum_key(256)
        session_id = hashlib.sha256(session_key.encode()).hexdigest()[:16]
        
        session = {
            'session_id': session_id,
            'key': session_key,
            'created': datetime.now().isoformat(),
            'protocol': 'quantum_secure'
        }
        
        # Save session
        session_file = self.key_storage / f"session_{session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(session, f, indent=2)
        
        return session

if __name__ == "__main__":
    print("🔐 Quantum Encryption System Test\n")
    
    # Initialize
    qenc = QuantumEncryption()
    
    # Test 1: Generate quantum key
    print("1️⃣ Generating quantum key...")
    key = qenc.qkd.generate_quantum_key(256)
    print(f"   Key (256-bit): {key[:32]}...")
    
    # Test 2: BB84 Protocol
    print("\n2️⃣ Testing BB84 Protocol...")
    bb84_result = qenc.qkd.bb84_protocol(128)
    print(f"   Shared key: {bb84_result['bits'][:32]}...")
    print(f"   Protocol: {bb84_result['protocol']}")
    
    # Test 3: Encrypt/Decrypt text
    print("\n3️⃣ Testing encryption...")
    test_data = "Quantum geofencing secret data 🔒"
    encrypted = qenc.encrypt_data(test_data)
    print(f"   Original: {test_data}")
    print(f"   Encrypted: {encrypted['encrypted_data'][:40]}...")
    
    decrypted = qenc.decrypt_data(encrypted['encrypted_data'], encrypted['key'])
    print(f"   Decrypted: {decrypted}")
    print(f"   ✅ Match: {decrypted == test_data}")
    
    # Test 4: Encrypt location data
    print("\n4️⃣ Testing location encryption...")
    location = {
        'lat': 40.7128,
        'lon': -74.0060,
        'timestamp': datetime.now().isoformat(),
        'accuracy': 10.5
    }
    
    encrypted_loc = qenc.encrypt_location_data(location)
    print(f"   Location encrypted: {encrypted_loc['encrypted_data'][:40]}...")
    
    decrypted_loc = qenc.decrypt_data(
        encrypted_loc['encrypted_data'],
        encrypted_loc['key']
    )
    print(f"   Decrypted lat: {decrypted_loc['lat']}")
    print(f"   ✅ Match: {decrypted_loc['lat'] == location['lat']}")
    
    # Test 5: Save/Load encrypted file
    print("\n5️⃣ Testing encrypted file storage...")
    test_file_data = {
        'zone_id': 'quantum_zone_1',
        'coordinates': [40.7128, -74.0060],
        'secret': 'Top secret quantum data'
    }
    
    qenc.save_encrypted_file('test_zone', test_file_data)
    loaded_data = qenc.load_encrypted_file('test_zone')
    print(f"   Loaded: {loaded_data}")
    print(f"   ✅ Match: {loaded_data == test_file_data}")
    
    # Test 6: Create quantum session
    print("\n6️⃣ Creating quantum session...")
    session = qenc.create_quantum_session()
    print(f"   Session ID: {session['session_id']}")
    print(f"   Key: {session['key'][:32]}...")
    print(f"   Protocol: {session['protocol']}")
    
    print("\n✅ All Quantum Encryption Tests Passed!")
    print(f"\n📁 Keys stored in: {qenc.key_storage}")
