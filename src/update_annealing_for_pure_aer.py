#!/usr/bin/env python3
"""Update annealing.py to use Pure Python Aer"""
import re

with open('annealing.py', 'r') as f:
    content = f.read()

# Replace Aer import
content = re.sub(
    r'from aer_simulator import Aer',
    'from aer_simulator import AerSimulator as Aer',
    content
)

# Replace Aer.get_backend
content = re.sub(
    r"Aer\.get_backend\(['\"].*?['\"]\)",
    'Aer()',
    content
)

with open('annealing.py', 'w') as f:
    f.write(content)

print("✅ annealing.py updated to use Pure Python Aer!")
