#!/usr/bin/env python3
"""
⚛️ Quantum Camera with Relativistic Physics Analysis
Combines quantum detection with Rust-powered physics
"""

import sys
import os
sys.path.append('src')

try:
    import relativistic_physics
    RUST_PHYSICS = True
except ImportError:
    RUST_PHYSICS = False
    print("⚠️  Rust physics not available")

from quantum_camera_detector import QuantumCameraDetector
from quantum_visualizer import QuantumVisualizer

class QuantumRelativisticDetector:
    """Quantum detector with relativistic analysis"""
    
    def __init__(self):
        self.detector = QuantumCameraDetector()
        self.visualizer = QuantumVisualizer()
        self.use_rust = RUST_PHYSICS
    
    def analyze_with_physics(self, image_path):
        """Analyze image with quantum + relativistic physics"""
        
        print("\n" + "="*60)
        print("⚛️ QUANTUM RELATIVISTIC ANALYSIS ⚛️")
        print("="*60)
        
        # Quantum detection
        score, signatures = self.detector.analyze_frame(image_path)
        
        print(f"\n📷 Image: {image_path}")
        print(f"🔬 Quantum Score: {score:.3f}")
        print(f"📊 Signatures: {len(signatures)}")
        
        if self.use_rust and score > 0:
            # Map to relativistic velocity
            if score < 0.7:
                velocity = score
            else:
                velocity = 0.9 + (score - 0.7) * 0.3
            
            print(f"\n🚀 Relativistic Mapping:")
            print(f"   Velocity: {velocity:.3f}c")
            
            # Create particle
            particle = relativistic_physics.RelativisticParticle(velocity, 1.0)
            
            try:
                gamma = particle.calculate_lorentz_factor()
                energy = particle.relativistic_energy()
                
                print(f"   Lorentz Factor: {gamma:.3f}")
                print(f"   Time Dilation: {gamma:.3f}x")
                print(f"   Energy: {energy:.3f}")
                
                # Classify detection strength
                if gamma > 4.0:
                    classification = "🔴 EXTREME (Ultra-relativistic)"
                elif gamma > 2.0:
                    classification = "🟠 HIGH (Highly relativistic)"
                elif gamma > 1.5:
                    classification = "🟡 MODERATE (Relativistic)"
                else:
                    classification = "🟢 LOW (Sub-relativistic)"
                
                print(f"\n   Classification: {classification}")
                
            except ValueError as e:
                print(f"   Special State: {e}")
        
        print("="*60)
        
        return score, signatures
    
    def capture_and_analyze(self):
        """Capture frame and analyze with physics"""
        
        print("\n📷 Capturing quantum frame...")
        image_path = self.detector.capture_frame()
        
        if image_path:
            return self.analyze_with_physics(image_path)
        else:
            print("❌ Capture failed")
            return None, None


def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ⚛️ QUANTUM RELATIVISTIC DETECTOR ⚛️                     ║
║                                                           ║
║   Quantum Detection + Rust Physics = Ultimate Analysis   ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    detector = QuantumRelativisticDetector()
    
    print("\n1. Capture and analyze")
    print("2. Analyze existing image")
    print("3. Exit")
    
    choice = input("\nChoice: ").strip()
    
    if choice == '1':
        detector.capture_and_analyze()
    
    elif choice == '2':
        image_path = input("Image path: ").strip()
        if os.path.exists(image_path):
            detector.analyze_with_physics(image_path)
        else:
            print("File not found")
    
    elif choice == '3':
        print("\n✨ Goodbye! ✨")


if __name__ == "__main__":
    main()
