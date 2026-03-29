#!/usr/bin/env python3
"""Integrate Rust physics with quantum camera"""

import relativistic_physics

def analyze_quantum_score(score):
    """Map quantum detection score to relativistic velocity"""
    
    # Map score to velocity
    if score < 0.7:
        velocity = score
    else:
        # High scores = ultra-relativistic
        velocity = 0.9 + (score - 0.7) * 0.3
    
    print(f"\n⚛️ QUANTUM DETECTION ANALYSIS")
    print(f"Quantum Score: {score:.3f}")
    print(f"Mapped Velocity: {velocity:.3f}c\n")
    
    particle = relativistic_physics.RelativisticParticle(velocity, 1.0)
    print(particle.get_analysis())
    
    return particle

# Test with different quantum scores
print("="*60)
analyze_quantum_score(0.5)   # Moderate detection
print("="*60)
analyze_quantum_score(0.85)  # High detection
print("="*60)
analyze_quantum_score(0.95)  # Extreme detection
print("="*60)
