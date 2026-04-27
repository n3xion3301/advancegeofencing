#!/bin/bash

echo "======================================================================="
echo "           🔬 QUANTUM GEOFENCING SYSTEM TEST SUITE"
echo "======================================================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Use Termux-compatible temp directory
TEMP_DIR="$HOME/advancegeofencing/.test_output"
mkdir -p "$TEMP_DIR"

passed=0
failed=0
skipped=0

test_script() {
    local script=$1
    local description=$2
    
    echo -n "Testing: $description ... "
    
    if [ ! -f "$script" ]; then
        echo -e "${YELLOW}SKIPPED${NC} (file not found)"
        ((skipped++))
        return
    fi
    
    if timeout 10 python "$script" > "$TEMP_DIR/test_output.txt" 2>&1; then
        echo -e "${GREEN}PASSED${NC}"
        ((passed++))
    else
        echo -e "${RED}FAILED${NC}"
        echo "  Error output:"
        tail -5 "$TEMP_DIR/test_output.txt" | sed 's/^/    /'
        ((failed++))
    fi
}

echo "📦 Core Quantum Modules"
echo "-----------------------------------------------------------------------"
test_script "quantum_helpers.py" "Quantum Helper Functions"
test_script "test_local_quantum.py" "Local Quantum Simulator"
test_script "quantum_experiment.py" "Basic Quantum Experiment"

echo ""
echo "🔐 Quantum Security & Cryptography"
echo "-----------------------------------------------------------------------"
test_script "src/quantum_random_generator.py" "Quantum Random Number Generator"

echo ""
echo "🌐 Quantum Geofencing Features"
echo "-----------------------------------------------------------------------"
test_script "src/quantum_zone_entanglement.py" "Quantum Zone Correlation"
test_script "src/quantum_probabilistic_geofence.py" "Probabilistic Geofencing"
test_script "src/quantum_tunneling_detector.py" "Quantum Tunneling Detection"

echo ""
echo "🎯 Quantum Integration"
echo "-----------------------------------------------------------------------"
test_script "src/quantum_geofence_integration.py" "Full Quantum Geofence System"

echo ""
echo "📹 Quantum Astral Vision"
echo "-----------------------------------------------------------------------"
echo -n "Testing: Quantum Astral Vision (import test) ... "
if [ -f "src/quantum_astral_vision.py" ]; then
    if python -c "import sys; sys.path.insert(0, 'src'); from quantum_astral_vision import QuantumAstralVision; print('OK')" > "$TEMP_DIR/test_output.txt" 2>&1; then
        echo -e "${GREEN}PASSED${NC}"
        ((passed++))
    else
        echo -e "${RED}FAILED${NC}"
        tail -3 "$TEMP_DIR/test_output.txt" | sed 's/^/    /'
        ((failed++))
    fi
else
    echo -e "${YELLOW}SKIPPED${NC}"
    ((skipped++))
fi

echo ""
echo "⚛️  Quantum Physics Modules"
echo "-----------------------------------------------------------------------"
test_script "src/quantum_erasure.py" "Quantum Erasure"
test_script "src/quantum_chromodynamics.py" "Quantum Chromodynamics"
test_script "src/quantum_cloning.py" "Quantum Cloning"
test_script "src/quantum_vacuum_energy.py" "Quantum Vacuum Energy"
test_script "src/quantum_field_theory.py" "Quantum Field Theory"
test_script "src/decaying.py" "Quantum Decay Simulation"

echo ""
echo "📊 Quantum Visualization"
echo "-----------------------------------------------------------------------"
test_script "quantum_visualization_demo.py" "Quantum Visualization Demo"
test_script "quantum_superposition_demo.py" "Quantum Superposition Demo"

echo ""
echo "======================================================================="
echo "                         TEST SUMMARY"
echo "======================================================================="
echo -e "${GREEN}Passed:${NC}  $passed"
echo -e "${RED}Failed:${NC}  $failed"
echo -e "${YELLOW}Skipped:${NC} $skipped"
echo "-----------------------------------------------------------------------"

total=$((passed + failed))
if [ $total -gt 0 ]; then
    percentage=$((passed * 100 / total))
    echo "Success Rate: $percentage%"
fi

echo "======================================================================="

# Cleanup
rm -rf "$TEMP_DIR"

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED!${NC}"
    exit 0
else
    echo -e "${RED}❌ SOME TESTS FAILED${NC}"
    exit 1
fi
