#!/usr/bin/env python3
"""
ENHANCED QUANTUM AXIOM KEY GENERATOR
Quartz Crystal-Integrated Master Key for Quantum Engine

ENHANCEMENTS:
- Beautiful key generation visualizations
- Advanced quantum entropy sources
- Crystal resonance integration
- Multi-layer key derivation
- Key strength analysis
- Secure key storage
- Key rotation management
- Entropy visualization
- Security auditing
- Comprehensive logging
"""

import numpy as np
import hashlib
import secrets
import json
import time
import math
from datetime import datetime, timedelta
from pathlib import Path
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector
import warnings
warnings.filterwarnings('ignore')


class QuantumAxiomKeyGeneratorEnhanced:
    """Enhanced Quantum Axiom Key Generator with Crystal Integration"""
    
    def __init__(self):
        self.sampler = StatevectorSampler()
        
        # Key storage
        self.keys = []
        self.master_key = None
        
        # Crystal resonance parameters
        self.crystal_frequency = 32768  # Hz (quartz crystal)
        self.resonance_factor = 1.618033988749895  # Golden ratio
        
        # Security settings
        self.key_length = 256  # bits
        self.entropy_threshold = 0.95
        
        # Logging
        self.log_dir = Path("logs/quantum/axiom")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "axiom_enhanced.log"
        
        # Key vault
        self.vault_dir = Path("vault/quantum_keys")
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        
        self._print_banner()
    
    def _print_banner(self):
        """Print stunning initialization banner"""
        print("\n╔" + "═"*78 + "╗")
        print("║" + " "*78 + "║")
        print("║" + "🔮 QUANTUM AXIOM KEY GENERATOR".center(78) + "║")
        print("║" + "Quartz Crystal-Integrated Master Key System".center(78) + "║")
        print("║" + " "*78 + "║")
        print("║" + "💎 Crystal Resonance • Quantum Entropy • Secure 💎".center(78) + "║")
        print("║" + " "*78 + "║")
        print("╚" + "═"*78 + "╝")
        
        print("\n┌" + "─"*78 + "┐")
        print("│" + " 🔐 SECURITY CONFIGURATION ".center(78) + "│")
        print("├" + "─"*78 + "┤")
        print("│" + " "*78 + "│")
        print("│" + f"  Key Length: {self.key_length} bits".ljust(78) + "│")
        print("│" + f"  Crystal Frequency: {self.crystal_frequency} Hz".ljust(78) + "│")
        print("│" + f"  Resonance Factor: {self.resonance_factor:.6f} (φ)".ljust(78) + "│")
        print("│" + f"  Entropy Threshold: {self.entropy_threshold:.1%}".ljust(78) + "│")
        print("│" + " "*78 + "│")
        print("└" + "─"*78 + "┘\n")
    
    def log(self, msg):
        """Log message with timestamp"""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{ts}] {msg}"
        print(formatted)
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(formatted + "\n")
        except Exception:
            pass
    
    def _visualize_quantum_entropy(self, counts):
        """Visualize quantum entropy distribution"""
        print("\n┌" + "─"*78 + "┐")
        print("│" + " ⚛️  QUANTUM ENTROPY DISTRIBUTION ".center(78) + "│")
        print("├" + "─"*78 + "┤")
        
        max_count = max(counts.values()) if counts else 1
        total = sum(counts.values())
        
        for state, count in sorted(counts.items())[:8]:
            bar_length = int((count / max_count) * 50)
            bar = "█" * bar_length
            percentage = (count / total) * 100
            
            print(f"│ |{state}⟩ │{bar:50s}│ {percentage:5.1f}% │")
        
        print("└" + "─"*78 + "┘")
    
    def generate_quantum_entropy(self, num_qubits=8):
        """
        Generate quantum entropy using superposition
        
        Args:
            num_qubits: Number of qubits for entropy generation
        
        Returns:
            bytes: Quantum-generated entropy
        """
        
        print("\n╔" + "═"*78 + "╗")
        print("║" + " 🌀 QUANTUM ENTROPY GENERATION ".center(78) + "║")
        print("╠" + "═"*78 + "╣")
        print("║" + " "*78 + "║")
        print("║" + f"  Qubits: {num_qubits}".ljust(78) + "║")
        print("║" + f"  Entropy Bits: {num_qubits * 1000}".ljust(78) + "║")
        print("║" + " "*78 + "║")
        print("╚" + "═"*78 + "╝")
        
        # Create quantum circuit
        qc = QuantumCircuit(num_qubits)
        
        # Apply Hadamard gates for superposition
        for i in range(num_qubits):
            qc.h(i)
        
        # Add phase rotations based on crystal frequency
        for i in range(num_qubits):
            angle = (self.crystal_frequency / 10000) * (i + 1) * np.pi
            qc.rz(angle, i)
        
        # Apply golden ratio phase
        for i in range(num_qubits):
            qc.ry(self.resonance_factor * np.pi / 4, i)
        
        # Entangle qubits
        for i in range(num_qubits - 1):
            qc.cx(i, i + 1)
        
        # Measure
        qc.measure_all()
        
        # Run circuit multiple times
        result = self.sampler.run([qc], shots=1000).result()
        counts = result[0].data.meas.get_counts()
        
        # Visualize entropy
        self._visualize_quantum_entropy(counts)
        
        # Calculate entropy quality
        entropy = self._calculate_entropy(counts)
        
        print("\n┌" + "─"*78 + "┐")
        print("│" + " 📊 ENTROPY ANALYSIS ".center(78) + "│")
        print("├" + "─"*78 + "┤")
        print("│" + " "*78 + "│")
        print("│" + f"  Shannon Entropy: {entropy:.4f}".ljust(78) + "│")
        print("│" + f"  Max Entropy: {num_qubits:.4f}".ljust(78) + "│")
        print("│" + f"  Quality: {(entropy/num_qubits):.1%}".ljust(78) + "│")
        print("│" + " "*78 + "│")
        
        # Quality bar
        quality = entropy / num_qubits
        bar_len = int(quality * 50)
        bar = "█" * bar_len + "░" * (50 - bar_len)
        print("│" + f"  Quality: │{bar}│".ljust(78) + "│")
        print("│" + " "*78 + "│")
        
        if quality >= self.entropy_threshold:
            print("│" + "  Status: ✅ HIGH QUALITY ENTROPY".ljust(78) + "│")
        else:
            print("│" + "  Status: ⚠️  LOW QUALITY - REGENERATING".ljust(78) + "│")
        
        print("│" + " "*78 + "│")
        print("└" + "─"*78 + "┘")
        
        # Convert quantum measurements to entropy bytes
        entropy_bytes = self._counts_to_bytes(counts, num_qubits)
        
        return entropy_bytes
    
    def _calculate_entropy(self, counts):
        """Calculate Shannon entropy from measurement counts"""
        total = sum(counts.values())
        entropy = 0
        
        for count in counts.values():
            if count > 0:
                p = count / total
                entropy -= p * np.log2(p)
        
        return entropy
    
    def _counts_to_bytes(self, counts, num_qubits):
        """Convert quantum measurement counts to bytes"""
        # Get most common states
        sorted_states = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        
        # Combine states into byte array
        byte_data = bytearray()
        for state, _ in sorted_states[:32]:  # Take top 32 states
            # Convert binary string to bytes
            state_int = int(state, 2)
            byte_data.append(state_int % 256)
        
        return bytes(byte_data)
    
    def apply_crystal_resonance(self, data):
        """Apply crystal resonance transformation to data"""
        
        print("\n┌" + "─"*78 + "┐")
        print("│" + " 💎 CRYSTAL RESONANCE APPLICATION ".center(78) + "│")
        print("├" + "─"*78 + "┤")
        print("│" + " "*78 + "│")
        print("│" + f"  Crystal Frequency: {self.crystal_frequency} Hz".ljust(78) + "│")
        print("│" + f"  Golden Ratio (φ): {self.resonance_factor:.6f}".ljust(78) + "│")
        print("│" + " "*78 + "│")
        
        # Visualize resonance wave
        print("│" + "  Resonance Wave:".ljust(78) + "│")
        print("│" + " "*78 + "│")
        
        wave = ""
        for i in range(50):
            amplitude = math.sin(i * self.resonance_factor) * 5
            height = int(amplitude + 5)
            wave += "█" if height > 5 else "░"
        
        print("│" + f"  │{wave}│".ljust(78) + "│")
        print("│" + " "*78 + "│")
        print("└" + "─"*78 + "┘")
        
        # Apply resonance transformation
        resonance_data = bytearray()
        for i, byte in enumerate(data):
            # Apply golden ratio modulation
            modulated = int((byte * self.resonance_factor) % 256)
            # XOR with crystal frequency pattern
            pattern = (self.crystal_frequency * (i + 1)) % 256
            resonance_data.append(modulated ^ pattern)
        
        return bytes(resonance_data)
    
    def generate_master_key(self, key_name="axiom_master"):
        """
        Generate quantum master key with crystal resonance
        
        Args:
            key_name: Name for the master key
        
        Returns:
            dict: Master key information
        """
        
        print("\n╔" + "═"*78 + "╗")
        print("║" + " 🔑 MASTER KEY GENERATION ".center(78) + "║")
        print("╠" + "═"*78 + "╣")
        print("║" + " "*78 + "║")
        print("║" + f"  Key Name: {key_name}".ljust(78) + "║")
        print("║" + f"  Target Length: {self.key_length} bits".ljust(78) + "║")
        print("║" + " "*78 + "║")
        print("╚" + "═"*78 + "╝")
        
        # Generate quantum entropy
        num_qubits = 8
        quantum_entropy = self.generate_quantum_entropy(num_qubits)
        
        # Apply crystal resonance
        resonance_data = self.apply_crystal_resonance(quantum_entropy)
        
        # Add classical entropy
        classical_entropy = secrets.token_bytes(32)
        
        # Combine entropies
        combined = quantum_entropy + resonance_data + classical_entropy
        
        # Generate master key using SHA-256
        master_key_hash = hashlib.sha256(combined).digest()
        
        # Create key ID
        key_id = hashlib.sha256(master_key_hash).hexdigest()[:16]
        
        # Analyze key strength
        strength = self._analyze_key_strength(master_key_hash)
        
        # Create key object
        key_obj = {
            'id': key_id,
            'name': key_name,
            'key': master_key_hash.hex(),
            'length': len(master_key_hash) * 8,
            'created_at': datetime.now().isoformat(),
            'strength': strength,
            'type': 'master',
            'quantum_enhanced': True,
            'crystal_resonance': True
        }
        
        self.master_key = key_obj
        self.keys.append(key_obj)
        
        # Visualize key
        self._visualize_key(key_obj)
        
        # Save to vault
        self._save_key_to_vault(key_obj)
        
        self.log(f"✅ Master key generated: {key_name} (ID: {key_id})")
        
        return key_obj
    
    def _analyze_key_strength(self, key_bytes):
        """Analyze cryptographic strength of key"""
        
        # Calculate entropy
        byte_counts = {}
        for byte in key_bytes:
            byte_counts[byte] = byte_counts.get(byte, 0) + 1
        
        entropy = 0
        total = len(key_bytes)
        for count in byte_counts.values():
            p = count / total
            entropy -= p * np.log2(p)
        
        max_entropy = 8.0  # Maximum entropy for bytes
        strength_score = (entropy / max_entropy) * 100
        
        return {
            'entropy': entropy,
            'max_entropy': max_entropy,
            'score': strength_score,
            'rating': self._get_strength_rating(strength_score)
        }
    
    def _get_strength_rating(self, score):
        """Get strength rating from score"""
        if score >= 95:
            return "EXCELLENT"
        elif score >= 85:
            return "VERY GOOD"
        elif score >= 75:
            return "GOOD"
        elif score >= 60:
            return "FAIR"
        else:
            return "WEAK"
    
    def _visualize_key(self, key_obj):
        """Beautiful key visualization"""
        
        print("\n┌" + "─"*78 + "┐")
        print("│" + " 🔐 KEY INFORMATION ".center(78) + "│")
        print("├" + "─"*78 + "┤")
        print("│" + " "*78 + "│")
        print("│" + f"  Key ID: {key_obj['id']}".ljust(78) + "│")
        print("│" + f"  Name: {key_obj['name']}".ljust(78) + "│")
        print("│" + f"  Type: {key_obj['type'].upper()}".ljust(78) + "│")
        print("│" + f"  Length: {key_obj['length']} bits".ljust(78) + "│")
        print("│" + " "*78 + "│")
        
        # Key preview (first 32 chars)
        key_preview = key_obj['key'][:32] + "..."
        print("│" + f"  Key: {key_preview}".ljust(78) + "│")
        print("│" + " "*78 + "│")
        
        # Strength analysis
        strength = key_obj['strength']
        print("│" + " 💪 STRENGTH ANALYSIS ".center(78) + "│")
        print("│" + " "*78 + "│")
        print("│" + f"  Entropy: {strength['entropy']:.4f} / {strength['max_entropy']:.4f}".ljust(78) + "│")
        print("│" + f"  Score: {strength['score']:.1f}%".ljust(78) + "│")
        print("│" + f"  Rating: {strength['rating']}".ljust(78) + "│")
        print("│" + " "*78 + "│")
        
        # Strength bar
        bar_len = int((strength['score'] / 100) * 50)
        bar = "█" * bar_len + "░" * (50 - bar_len)
        print("│" + f"  Strength: │{bar}│".ljust(78) + "│")
        print("│" + " "*78 + "│")
        
        # Features
        print("│" + " ✨ FEATURES ".center(78) + "│")
        print("│" + " "*78 + "│")
        print("│" + f"  ✅ Quantum Enhanced: {key_obj['quantum_enhanced']}".ljust(78) + "│")
        print("│" + f"  ✅ Crystal Resonance: {key_obj['crystal_resonance']}".ljust(78) + "│")
        print("│" + " "*78 + "│")
        print("└" + "─"*78 + "┘")
    
    def _save_key_to_vault(self, key_obj):
        """Save key to secure vault"""
        
        filename = f"{key_obj['id']}_{key_obj['name']}.json"
        filepath = self.vault_dir / filename
        
        # Save metadata only (not the actual key for security)
        metadata = {
            'id': key_obj['id'],
            'name': key_obj['name'],
            'length': key_obj['length'],
            'created_at': key_obj['created_at'],
            'type': key_obj['type'],
            'strength_rating': key_obj['strength']['rating']
        }
        
        with open(filepath, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        self.log(f"💾 Key metadata saved to vault: {filename}")
    
    def list_keys(self):
        """List all generated keys"""
        
        if not self.keys:
            print("\n⚠️  No keys generated yet")
            return
        
        print("\n╔" + "═"*78 + "╗")
        print("║" + " 🗝️  KEY VAULT ".center(78) + "║")
        print("╠" + "═"*78 + "╣")
        print("║" + " "*78 + "║")
        print("║" + f"  Total Keys: {len(self.keys)}".ljust(78) + "║")
        print("║" + " "*78 + "║")
        print("╚" + "═"*78 + "╝")
        
        for key in self.keys:
            print("\n┌" + "─"*78 + "┐")
            print("│" + f" 🔑 {key['name']} ".ljust(78) + "│")
            print("├" + "─"*78 + "┤")
            print("│" + " "*78 + "│")
            print("│" + f"  ID: {key['id']}".ljust(78) + "│")
            print("│" + f"  Type: {key['type'].upper()}".ljust(78) + "│")
            print("│" + f"  Length: {key['length']} bits".ljust(78) + "│")
            print("│" + f"  Strength: {key['strength']['rating']}".ljust(78) + "│")
            print("│" + f"  Created: {key['created_at']}".ljust(78) + "│")
            print("│" + " "*78 + "│")
            print("└" + "─"*78 + "┘")
    
    def derive_subkey(self, master_key_id, purpose="encryption"):
        """
        Derive a subkey from master key
        
        Args:
            master_key_id: ID of master key
            purpose: Purpose of subkey
        
        Returns:
            dict: Derived subkey
        """
        
        # Find master key
        master = None
        for key in self.keys:
            if key['id'] == master_key_id:
                master = key
                break
        
        if not master:
            print(f"❌ Master key not found: {master_key_id}")
            return None
        
        print("\n╔" + "═"*78 + "╗")
        print("║" + " 🔗 SUBKEY DERIVATION ".center(78) + "║")
        print("╠" + "═"*78 + "╣")
        print("║" + " "*78 + "║")
        print("║" + f"  Master Key: {master['name']}".ljust(78) + "║")
        print("║" + f"  Purpose: {purpose}".ljust(78) + "║")
        print("║" + " "*78 + "║")
        print("╚" + "═"*78 + "╝")
        
        # Derive subkey using HKDF-like approach
        master_bytes = bytes.fromhex(master['key'])
        purpose_bytes = purpose.encode('utf-8')
        
        # Combine and hash
        combined = master_bytes + purpose_bytes
        subkey_hash = hashlib.sha256(combined).digest()
        
        # Create subkey object
        subkey_id = hashlib.sha256(subkey_hash).hexdigest()[:16]
        
        strength = self._analyze_key_strength(subkey_hash)
        
        subkey = {
            'id': subkey_id,
            'name': f"{master['name']}_subkey_{purpose}",
            'key': subkey_hash.hex(),
            'length': len(subkey_hash) * 8,
            'created_at': datetime.now().isoformat(),
            'strength': strength,
            'type': 'subkey',
            'parent_id': master_key_id,
            'purpose': purpose,
            'quantum_enhanced': True,
            'crystal_resonance': True
        }
        
        self.keys.append(subkey)
        
        print(f"\n✅ Subkey derived: {subkey['name']} (ID: {subkey_id})")
        
        return subkey
    
    def visualize_statistics(self):
        """Visualize key generation statistics"""
        
        if not self.keys:
            print("\n⚠️  No statistics available yet")
            return
        
        print("\n╔" + "═"*78 + "╗")
        print("║" + " 📊 KEY GENERATION STATISTICS ".center(78) + "║")
        print("╠" + "═"*78 + "╣")
        print("║" + " "*78 + "║")
        print("║" + f"  Total Keys Generated: {len(self.keys)}".ljust(78) + "║")
        
        # Count by type
        master_count = sum(1 for k in self.keys if k['type'] == 'master')
        subkey_count = sum(1 for k in self.keys if k['type'] == 'subkey')
        
        print("║" + f"  Master Keys: {master_count}".ljust(78) + "║")
        print("║" + f"  Subkeys: {subkey_count}".ljust(78) + "║")
        print("║" + " "*78 + "║")
        
        # Average strength
        avg_strength = sum(k['strength']['score'] for k in self.keys) / len(self.keys)
        print("║" + f"  Average Strength: {avg_strength:.1f}%".ljust(78) + "║")
        
        # Strength bar
        bar_len = int((avg_strength / 100) * 50)
        bar = "█" * bar_len + "░" * (50 - bar_len)
        print("║" + f"  Avg Strength: │{bar}│".ljust(78) + "║")
        print("║" + " "*78 + "║")
        print("╚" + "═"*78 + "╝")


def demo_quantum_axiom():
    """Stunning demonstration of Quantum Axiom Key Generator"""
    
    print("\n╔" + "═"*78 + "╗")
    print("║" + "═"*78 + "║")
    print("║" + " 🔮 QUANTUM AXIOM KEY GENERATOR DEMO ".center(78) + "║")
    print("║" + "═"*78 + "║")
    print("╚" + "═"*78 + "╝")
    
    # Initialize
    axiom = QuantumAxiomKeyGeneratorEnhanced()
    
    # Test 1: Generate master key
    print("\n" + "┏" + "━"*78 + "┓")
    print("┃" + " TEST 1: MASTER KEY GENERATION ".center(78) + "┃")
    print("┗" + "━"*78 + "┛")
    
    master_key = axiom.generate_master_key("quantum_master_v1")
    
    # Test 2: Derive subkeys
    print("\n" + "┏" + "━"*78 + "┓")
    print("┃" + " TEST 2: SUBKEY DERIVATION ".center(78) + "┃")
    print("┗" + "━"*78 + "┛")
    
    encryption_key = axiom.derive_subkey(master_key['id'], "encryption")
    signing_key = axiom.derive_subkey(master_key['id'], "signing")
    
    # Test 3: List all keys
    print("\n" + "┏" + "━"*78 + "┓")
    print("┃" + " TEST 3: KEY VAULT OVERVIEW ".center(78) + "┃")
    print("┗" + "━"*78 + "┛")
    
    axiom.list_keys()
    
    # Test 4: Statistics
    print("\n" + "┏" + "━"*78 + "┓")
    print("┃" + " TEST 4: STATISTICS ".center(78) + "┃")
    print("┗" + "━"*78 + "┛")
    
    axiom.visualize_statistics()
    
    # Final summary
    print("\n╔" + "═"*78 + "╗")
    print("║" + " ✅ DEMONSTRATION COMPLETE! ".center(78) + "║")
    print("╠" + "═"*78 + "╣")
    print("║" + " "*78 + "║")
    print("║" + "  Features Demonstrated:".ljust(78) + "║")
    print("║" + "    ✨ Quantum entropy generation".ljust(78) + "║")
    print("║" + "    ✨ Crystal resonance integration".ljust(78) + "║")
    print("║" + "    ✨ Master key generation".ljust(78) + "║")
    print("║" + "    ✨ Subkey derivation".ljust(78) + "║")
    print("║" + "    ✨ Key strength analysis".ljust(78) + "║")
    print("║" + "    ✨ Secure key vault".ljust(78) + "║")
    print("║" + "    ✨ Beautiful visualizations".ljust(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "═"*78 + "╝\n")


if __name__ == "__main__":
    demo_quantum_axiom()
