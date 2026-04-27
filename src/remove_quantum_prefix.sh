#!/bin/bash
echo "🔄 Removing 'quantum_' prefix from all files..."

# Backup first
backup_dir="../backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"
cp *.py "$backup_dir/" 2>/dev/null
echo "✅ Backup: $backup_dir"

# Rename all quantum_*.py files
for file in quantum_*.py; do
    if [ -f "$file" ]; then
        newname="${file#quantum_}"
        mv "$file" "$newname"
        echo "  ✅ $file -> $newname"
    fi
done

# Make all executable
chmod +x *.py *.sh

echo ""
echo "✅ Done! All 'quantum_' prefixes removed"
echo ""
echo "Now you can run:"
ls -1 *.py | head -10 | sed 's/^/  .\//g'
