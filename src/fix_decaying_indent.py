with open('decaying.py', 'r') as f:
    lines = f.readlines()

# Backup
with open('decaying.py.bak', 'w') as f:
    f.writelines(lines)

# Fix indentation issues
fixed_lines = []
for i, line in enumerate(lines):
    # If line 36 is a function definition without body
    if i > 0 and lines[i-1].strip().endswith(':') and not line.strip().startswith(('"""', '#', 'pass')):
        # Check if current line is a docstring
        if line.strip().startswith('"""'):
            # Ensure proper indentation (4 spaces more than function def)
            indent = len(lines[i-1]) - len(lines[i-1].lstrip())
            fixed_lines.append(' ' * (indent + 4) + line.lstrip())
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

with open('decaying.py', 'w') as f:
    f.writelines(fixed_lines)

print("✓ Fixed indentation in decaying.py")
