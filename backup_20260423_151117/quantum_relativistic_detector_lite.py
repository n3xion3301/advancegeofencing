#!/usr/bin/env python3
"""
⚛️ Quantum Relativistic Detector (Camera-Optional)
Works without camera if cv2 fails
"""

import sys
import os

# Try to import camera, but don't fail if it's not available
try:
    from quantum_camera_detector import QuantumCameraDetector
    CAMERA_AVAILABLE = True
except ImportError as e:
    CAMERA_AVAILABLE = False
    print(f"⚠️  Camera not available: {e}")
    print("    Running in analysis-only mode")

try:
    import relativistic_physics
    RUST_PHYSICS = True
    print("✅ Rust physics loaded")
except ImportError:
    RUST_PHYSICS = False
    print("⚠️  Rust physics not available")


class QuantumRelativisticDetector:
    """Quantum detector with relativistic analysis (camera-optional)"""
    
    def __init__(self):
        if CAMERA_AVAILABLE:
            self.detector = QuantumCameraDetector()
        else:
            self.detector = None
        self.use_rust = RUST_PHYSICS
    
    def analyze_with_physics(self, quantum_score, signatures_count=0):
        """Analyze quantum score with relativistic physics"""
        
        print("\n" + "="*60)
        print("⚛️ QUANTUM RELATIVISTIC ANALYSIS ⚛️")
        print("="*60)
        
        print(f"\n🔬 Quantum Score: {quantum_score:.3f}")
        print(f"📊 Signatures: {signatures_count}")
        
        if self.use_rust and quantum_score > 0:
            # Map to relativistic velocity
            if quantum_score < 0.7:
                velocity = quantum_score
            else:
                velocity = 0.9 + (quantum_score - 0.7) * 0.3
            
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


def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ⚛️ QUANTUM RELATIVISTIC DETECTOR (LITE) ⚛️              ║
║                                                           ║
║   Relativistic Physics Analysis (Camera-Optional)        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    detector = QuantumRelativisticDetector()
    
    if not detector.use_rust:
        print("\n❌ Rust physics not available!")
        print("   Build it: cd rust_physics && maturin build --release")
        return
    
    print("\n📊 MANUAL QUANTUM SCORE ANALYSIS\n")
    print("Enter quantum scores to analyze (0.0 to 1.0)")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            score_input = input("Quantum Score: ").strip()
            
            if score_input.lower() in ['quit', 'exit', 'q']:
                print("\n✨ Goodbye! ✨")
                break
            
            score = float(score_input)
            
            if 0 <= score <= 1:
                detector.analyze_with_physics(score)
            else:
                print("⚠️  Score must be between 0.0 and 1.0")
        
        except ValueError:
            print("⚠️  Invalid input. Enter a number between 0.0 and 1.0")
        except KeyboardInterrupt:
            print("\n\n✨ Goodbye! ✨")
            break


if __name__ == "__main__":
    main()
