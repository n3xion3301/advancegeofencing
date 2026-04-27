#!/usr/bin/env python3
"""Quantum Visualizer - Working Version for Camera Integration"""

class QuantumVisualizer:
    def __init__(self):
        self.entity_count = 0
    
    def quantum_state(self, entity):
        print("\n╔════════════════════════════════════════╗")
        print("║       🌀 QUANTUM STATE 🌀              ║")
        print("╚════════════════════════════════════════╝")
        print(f"Entity: {entity.get('name', 'Unknown')}")
        print(f"Quantum Score: {entity.get('quantum_score', 0):.3f}")
        print(f"Type: {entity.get('type', 'unknown')}")
    
    def wave_function(self, entity):
        print("\n╔════════════════════════════════════════╗")
        print("║       🌊 WAVE FUNCTION 🌊              ║")
        print("╚════════════════════════════════════════╝")
        print("ψ(x,t) = A·e^(i(kx-ωt))")
        print("Probability: |ψ|² ")
    
    def superposition(self, entity):
        print("\n╔════════════════════════════════════════╗")
        print("║       ⚡ SUPERPOSITION ⚡               ║")
        print("╚════════════════════════════════════════╝")
        print("|ψ⟩ = α|0⟩ + β|1⟩")
        print("Multiple states simultaneously!")
    
    def quantum_entanglement(self, entity):
        print("\n╔════════════════════════════════════════╗")
        print("║    🔗 QUANTUM ENTANGLEMENT 🔗          ║")
        print("╚════════════════════════════════════════╝")
        print("|ψ⟩ = (|↑↓⟩ - |↓↑⟩)/√2")
        print("Spooky action at a distance!")
    
    def quantum_tunneling(self, entity):
        print("\n╔════════════════════════════════════════╗")
        print("║     🚇 QUANTUM TUNNELING 🚇            ║")
        print("╚════════════════════════════════════════╝")
        print("Barrier penetration probability")
        print("Particles can pass through barriers!")
    
    def double_slit_experiment(self, entity):
        print("\n╔════════════════════════════════════════╗")
        print("║     🎯 DOUBLE SLIT EXPERIMENT 🎯       ║")
        print("╚════════════════════════════════════════╝")
        print("Wave-particle duality demonstration")
        print("Interference pattern observed!")
    
    def wave_interference(self, entity):
        print("\n╔════════════════════════════════════════╗")
        print("║     〰️ WAVE INTERFERENCE 〰️            ║")
        print("╚════════════════════════════════════════╝")
        print("Constructive and destructive interference")
    
    def bell_inequality(self, entity):
        print("\n╔════════════════════════════════════════╗")
        print("║     🔔 BELL INEQUALITY 🔔              ║")
        print("╚════════════════════════════════════════╝")
        print("Quantum mechanics violates local realism!")
    
    def schrodinger_cat(self, entity):
        print("\n╔════════════════════════════════════════╗")
        print("║     🐱 SCHRODINGER'S CAT 🐱            ║")
        print("╚════════════════════════════════════════╝")
        print("Alive AND dead until observed!")
    
    def wave_particle_duality(self, entity):
        print("\n╔════════════════════════════════════════╗")
        print("║   🌊⚛️ WAVE-PARTICLE DUALITY ⚛️🌊      ║")
        print("╚════════════════════════════════════════╝")
        print("Both wave and particle properties!")

