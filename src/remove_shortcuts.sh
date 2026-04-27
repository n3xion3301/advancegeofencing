#!/bin/bash
echo "🗑️  Removing shortcuts without extensions..."

# Remove shortcuts (files that have a .py equivalent)
for pyfile in *.py; do
    shortname="${pyfile%.py}"
    if [ -f "$shortname" ] && [ "$shortname" != "$pyfile" ]; then
        rm "$shortname"
        echo "  ✅ Removed: $shortname"
    fi
done

echo ""
echo "✅ All shortcuts removed!"
echo "📝 Use tab completion with .py extension:"
echo "   ./par[TAB] -> ./parallel_universe_detector.py"
echo "   ./ann[TAB] -> ./annealing.py"
