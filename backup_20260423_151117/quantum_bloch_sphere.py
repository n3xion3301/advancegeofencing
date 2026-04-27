#!/usr/bin/env python3
"""3D Bloch Sphere visualization"""
# Standard Quantum Computing Imports
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import Statevector
import warnings
import sys
import os
import json
from pathlib import Path
from datetime import datetime


from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Draw Bloch sphere
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))

ax.plot_surface(x, y, z, alpha=0.1, color='cyan')

# Add axes
ax.plot([0, 0], [0, 0], [-1.5, 1.5], 'k-', linewidth=2)
ax.plot([0, 1.5], [0, 0], [0, 0], 'r-', linewidth=2)
ax.plot([0, 0], [0, 1.5], [0, 0], 'g-', linewidth=2)

# Add quantum state vector
theta, phi = np.pi/4, np.pi/6
x_state = np.sin(theta) * np.cos(phi)
y_state = np.sin(theta) * np.sin(phi)
z_state = np.cos(theta)

ax.quiver(0, 0, 0, x_state, y_state, z_state,
          color='purple', arrow_length_ratio=0.1, linewidth=3)

ax.text(0, 0, 1.6, '|0⟩', fontsize=14, fontweight='bold')
ax.text(0, 0, -1.6, '|1⟩', fontsize=14, fontweight='bold')
ax.text(1.6, 0, 0, '|+⟩', fontsize=14, fontweight='bold')
ax.text(0, 1.6, 0, '|+i⟩', fontsize=14, fontweight='bold')

ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
ax.set_zlabel('Z', fontsize=12)
ax.set_title('Quantum Bloch Sphere', fontsize=16, fontweight='bold')

plt.savefig('bloch_sphere.png', dpi=150, bbox_inches='tight')
print("✅ Saved bloch_sphere.png!")
