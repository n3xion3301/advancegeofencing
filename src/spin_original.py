#!/usr/bin/env python3
"""
🌀 QUANTUM SPIN
Particle spin states and measurements
"""
# Standard Quantum Computing Imports
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from aer_simulator import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import Statevector
import warnings
import sys
import os
import json
from pathlib import Path
from datetime import datetime


from quantum_helpers import get_real_quantum_backend, run_quantum_circuit, format_quantum_output
from datetime import datetime

class QuantumSpin:
    def __init__(self):
        self.operator = "n3xion3301"
        self.hbar = 1.054571817e-34  # Reduced Planck constant

    def demonstrate_spin(self):
        """Demonstrate quantum spin-1/2 particle"""
        print("\n" + "="*70)
        print("🌀 QUANTUM SPIN".center(70))
        print("Spin-1/2 Particle States".center(70))
        print("="*70)
        print(f"Operator: {self.operator}".center(70))
        print("="*70)

        print("\n⚛️ Spin-1/2 Particle:")
        print(f"   ℏ = {self.hbar:.3e} J·s")
        print(f"   Spin quantum number: s = 1/2")
        print(f"   Magnetic quantum number: m_s = ±1/2")

        # Spin states
        print("\n🔼 Spin States:")
        print("   |↑⟩ = Spin-up   (m_s = +1/2)")
        print("   |↓⟩ = Spin-down (m_s = -1/2)")

        # Superposition
        theta = np.pi/4  # 45 degrees
        alpha = np.cos(theta/2)
        beta = np.sin(theta/2)

        print(f"\n🌊 Superposition State:")
        print(f"   |ψ⟩ = {alpha:.3f}|↑⟩ + {beta:.3f}|↓⟩")

        # Measurement probabilities
        prob_up = alpha**2
        prob_down = beta**2

        print(f"\n📊 Measurement Probabilities:")
        print(f"   P(↑) = {prob_up*100:.1f}%")
        print(f"   P(↓) = {prob_down*100:.1f}%")

        # Simulate measurement
        measurement = "↑" if np.random.rand() < prob_up else "↓"

        print(f"\n🔬 Measurement Result: |{measurement}⟩")
        print(f"   State collapsed to {'spin-up' if measurement == '↑' else 'spin-down'}!")

        # Stern-Gerlach
        print("\n🧲 Stern-Gerlach Experiment:")
        print("   Magnetic field splits beam into two paths")
        print("   Proves quantization of angular momentum!")

        print("\n" + "="*70)
        print("✅ Quantum spin demonstrated!")
        print("="*70)

def main():
    spin = QuantumSpin()
    spin.demonstrate_spin()
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
