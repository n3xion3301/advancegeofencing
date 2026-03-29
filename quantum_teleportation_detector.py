#!/usr/bin/env python3
"""
🌌 Quantum Teleportation + Camera Integration
Teleport quantum states detected by camera
"""

import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

try:
    import sys
    sys.path.append('src')
    from quantum_camera_detector import QuantumCameraDetector
    CAMERA_AVAILABLE = True
except ImportError:
    CAMERA_AVAILABLE = False
    print("⚠️  Camera detector not available")

try:
    import relativistic_physics
    RUST_PHYSICS = True
except ImportError:
    RUST_PHYSICS = False
    print("⚠️  Rust physics not available")


class QuantumTeleportationSystem:
    """Quantum teleportation with camera integration"""
    
    def __init__(self):
        self.backend = Aer.get_backend('qasm_simulator')
        if CAMERA_AVAILABLE:
            self.camera = QuantumCameraDetector()
    
    def create_teleportation_circuit(self, theta=np.pi/4, phi=0):
        """
        Create quantum teleportation circuit
        theta, phi: parameters for initial state preparation
        """
        qc = QuantumCircuit(3, 2)
        
        # STEP 1: Prepare state to teleport on q0
        qc.rx(theta, 0)
        if phi != 0:
            qc.rz(phi, 0)
        qc.barrier()
        
        # STEP 2: Create Bell Pair (q1, q2)
        qc.h(1)
        qc.cx(1, 2)
        qc.barrier()
        
        # STEP 3: Bell State Measurement (q0, q1)
        qc.cx(0, 1)
        qc.h(0)
        qc.barrier()
        
        # STEP 4: Measure
        qc.measure([0, 1], [0, 1])
        qc.barrier()
        
        # STEP 5: Bob's corrections
        qc.cx(1, 2)
        qc.cz(0, 2)
        
        return qc
    
    def teleport_quantum_state(self, theta, phi=0, shots=1024):
        """Execute teleportation"""
        
        print(f"\n⚛️ QUANTUM TELEPORTATION")
        print(f"Initial State: θ={theta:.3f}, φ={phi:.3f}")
        
        qc = self.create_teleportation_circuit(theta, phi)
        
        print("\n📊 Circuit:")
        print(qc.draw())
        
        # Execute
        job = execute(qc, self.backend, shots=shots)
        result = job.result()
        counts = result.get_counts()
        
        print(f"\n📈 Results ({shots} shots):")
        for state, count in sorted(counts.items()):
            print(f"  {state}: {count} ({count/shots*100:.1f}%)")
        
        return counts
    
    def teleport_from_camera_detection(self, image_path=None):
        """
        Teleport quantum state based on camera detection
        Maps quantum score to rotation angle
        """
        
        if not CAMERA_AVAILABLE:
            print("❌ Camera not available")
            return None
        
        print("\n📷 CAMERA-BASED QUANTUM TELEPORTATION\n")
        
        # Capture or analyze
        if image_path:
            score, signatures = self.camera.analyze_frame(image_path)
        else:
            image_path = self.camera.capture_frame()
            if not image_path:
                print("❌ Capture failed")
                return None
            score, signatures = self.camera.analyze_frame(image_path)
        
        print(f"Image: {image_path}")
        print(f"Quantum Score: {score:.3f}")
        print(f"Signatures: {len(signatures)}")
        
        # Map score to quantum state parameters
        theta = score * np.pi  # 0 to π
        phi = len(signatures) * np.pi / 10  # Based on signature count
        
        print(f"\nMapped to quantum state:")
        print(f"  θ = {theta:.3f} rad ({theta*180/np.pi:.1f}°)")
        print(f"  φ = {phi:.3f} rad ({phi*180/np.pi:.1f}°)")
        
        # Teleport!
        counts = self.teleport_quantum_state(theta, phi)
        
        # Relativistic analysis if available
        if RUST_PHYSICS and score > 0:
            velocity = 0.9 + score * 0.09  # Map to high velocity
            particle = relativistic_physics.RelativisticParticle(velocity, 1.0)
            
            print(f"\n🚀 Relativistic Analysis:")
            print(f"  Velocity: {velocity:.3f}c")
            try:
                gamma = particle.calculate_lorentz_factor()
                print(f"  Lorentz Factor: {gamma:.3f}")
                print(f"  Time Dilation: {gamma:.3f}x")
            except:
                pass
        
        return counts
    
    def visualize_results(self, counts):
        """Visualize teleportation results"""
        plot_histogram(counts)
        plt.title("Quantum Teleportation Results")
        plt.savefig('quantum_teleportation_results.png')
        print("\n💾 Saved: quantum_teleportation_results.png")


def demo():
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        🌌 QUANTUM TELEPORTATION SYSTEM 🌌                 ║
║                                                           ║
║   Teleport quantum states detected by camera             ║
║   Powered by Qiskit + Rust Physics                       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    system = QuantumTeleportationSystem()
    
    print("\n1. Basic teleportation (π/4 rotation)")
    print("2. Custom teleportation")
    print("3. Teleport from camera detection")
    print("4. Exit")
    
    choice = input("\nChoice: ").strip()
    
    if choice == '1':
        counts = system.teleport_quantum_state(np.pi/4)
        system.visualize_results(counts)
    
    elif choice == '2':
        theta = float(input("Enter θ (radians): "))
        phi = float(input("Enter φ (radians): "))
        counts = system.teleport_quantum_state(theta, phi)
        system.visualize_results(counts)
    
    elif choice == '3':
        image = input("Image path (or Enter to capture): ").strip()
        counts = system.teleport_from_camera_detection(image if image else None)
        if counts:
            system.visualize_results(counts)
    
    elif choice == '4':
        print("\n✨ Goodbye! ✨")


if __name__ == "__main__":
    demo()
