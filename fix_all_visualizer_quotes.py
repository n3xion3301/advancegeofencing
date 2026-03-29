#!/usr/bin/env python3
"""Fix ALL quote issues in quantum_visualizer.py"""

import re

print("Reading quantum_visualizer.py...")
with open('src/quantum_visualizer.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("Fixing quote issues...")

# Strategy: For lines with print("║ ... that contain nested quotes
# We'll use raw strings or escape inner quotes

lines = content.split('\n')
fixed_lines = []
fixes_made = 0

for i, line in enumerate(lines):
    original_line = line
    
    # Pattern: print("║ ... "text" ... "║")
    # This has nested quotes that break syntax
    
    if 'print("║' in line and line.count('"') > 4:
        # This line likely has nested quotes
        # Strategy: Use single quotes for outer, double for inner
        # OR escape the inner quotes
        
        # Find the print statement
        match = re.match(r'^(\s*)print\("(.*?)"\)$', line)
        if match:
            indent = match.group(1)
            content_part = match.group(2)
            
            # If content has unescaped quotes, escape them
            if '"' in content_part and not '\\"' in content_part:
                # Escape all inner quotes
                content_part = content_part.replace('"', '\\"')
                line = f'{indent}print("{content_part}")'
                fixes_made += 1
    
    fixed_lines.append(line)

print(f"Made {fixes_made} fixes")

# Write back
print("Writing fixed file...")
with open('src/quantum_visualizer.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(fixed_lines))

print("✅ All quote issues fixed!")
print("\nTesting syntax...")

import subprocess
result = subprocess.run(['python3', '-m', 'py_compile', 'src/quantum_visualizer.py'], 
                       capture_output=True, text=True)

if result.returncode == 0:
    print("✅ File compiles successfully!")
else:
    print("⚠️ Still has issues:")
    print(result.stderr[:500])
