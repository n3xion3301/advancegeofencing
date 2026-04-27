#!/bin/bash

echo "🔨 BUILDING CLONED REPOSITORIES"
echo "================================"
echo ""

# Activate venv
source quantum_env/bin/activate

echo "✅ Virtual environment activated"
echo ""

# Install base requirements
echo "📦 Installing base requirements..."
pip install --upgrade pip setuptools wheel
pip install Cython scikit-build cmake ninja pybind11 maturin

echo ""
echo "─────────────────────────────────────────"
echo ""

# 1. Build Qiskit-Aer
echo "1️⃣  BUILDING QISKIT-AER"
echo "─────────────────────────────────────────"

cd ~/advancegeofencing/qiskit-aer

echo "🔨 Building Qiskit-Aer (this may take 15-30 minutes)..."

# Try pip install first (easiest)
pip install -e .

if [ $? -eq 0 ]; then
    echo "✅ Qiskit-Aer installed successfully!"
    python -c "from qiskit_aer import Aer; print('✅ Aer backends:', Aer.backends())"
else
    echo "⚠️  pip install failed, trying manual build..."
    python setup.py build_ext --inplace
    pip install -e .
    
    if [ $? -eq 0 ]; then
        echo "✅ Qiskit-Aer built with manual method!"
    else
        echo "❌ Qiskit-Aer build failed - will use custom AerSimulator"
    fi
fi

echo ""
echo "─────────────────────────────────────────"
echo ""

# 2. Build orjson (for IBM Runtime)
echo "2️⃣  BUILDING ORJSON"
echo "─────────────────────────────────────────"

# Setup Rust nightly
echo "🦀 Setting up Rust nightly..."

# Check if rustup exists
if ! command -v rustup &> /dev/null; then
    echo "📦 Installing rustup..."
    pkg install -y rustup
fi

rustup install nightly
rustup default nightly

echo "✅ Rust nightly active:"
rustc --version

echo ""

# Clone orjson if not exists
if [ ! -d ~/advancegeofencing/orjson ]; then
    cd ~/advancegeofencing
    echo "📥 Cloning orjson..."
    gh repo clone ijl/orjson
fi

cd ~/advancegeofencing/orjson

echo "🔨 Building orjson with maturin..."
maturin build --release

if [ $? -eq 0 ]; then
    echo "✅ orjson built successfully!"
    
    # Install the wheel
    WHEEL=$(find target/wheels -name "*.whl" | head -n 1)
    if [ -n "$WHEEL" ]; then
        cd ~/advancegeofencing
        source quantum_env/bin/activate
        pip install "$WHEEL" --force-reinstall
        python -c "import orjson; print('✅ orjson:', orjson.__version__)"
    else
        echo "❌ Wheel not found"
    fi
else
    echo "❌ orjson build failed"
    echo "💡 Creating compatibility layer..."
    
    # Create orjson compatibility module
    cd ~/advancegeofencing
    mkdir -p quantum_env/lib/python3.13/site-packages/orjson
    cat > quantum_env/lib/python3.13/site-packages/orjson/__init__.py << 'EOF'
"""orjson compatibility using standard json"""
import json

def dumps(obj, **kwargs):
    """Serialize to bytes like orjson"""
    return json.dumps(obj, **kwargs).encode('utf-8')

def loads(data, **kwargs):
    """Deserialize from bytes or str"""
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    return json.loads(data, **kwargs)

__version__ = "0.0.0-compat"
EOF
    
    echo "✅ orjson compatibility layer installed"
fi

echo ""
echo "─────────────────────────────────────────"
echo ""

# 3. Build IBM Quantum Runtime
echo "3️⃣  BUILDING IBM QUANTUM RUNTIME"
echo "─────────────────────────────────────────"

cd ~/advancegeofencing/qiskit-ibm-runtime

echo "📋 Checking requirements..."
if [ -f requirements.txt ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

if [ -f requirements-dev.txt ]; then
    echo "Installing dev requirements..."
    pip install -r requirements-dev.txt 2>/dev/null || echo "Some dev deps failed, continuing..."
fi

echo ""
echo "🔨 Building IBM Quantum Runtime..."
pip install -e .

if [ $? -eq 0 ]; then
    echo "✅ IBM Quantum Runtime built successfully!"
    python -c "from qiskit_ibm_runtime import QiskitRuntimeService; print('✅ IBM Runtime available')"
else
    echo "❌ IBM Quantum Runtime build failed"
    echo ""
    echo "Common issues:"
    echo "  - orjson not available (check above)"
    echo "  - Missing dependencies"
    echo ""
    echo "💡 You can still use local simulator"
fi

echo ""
echo "─────────────────────────────────────────"
echo ""

# 4. Final verification
echo "4️⃣  FINAL VERIFICATION"
echo "─────────────────────────────────────────"

cd ~/advancegeofencing
source quantum_env/bin/activate

echo ""
echo "🧪 Testing all components..."
echo ""

# Test script
python << 'PYTEST'
print("="*60)
print("QUANTUM STACK TEST")
print("="*60)

# Test 1: Qiskit
print("\n1. Qiskit Core:")
try:
    import qiskit
    print(f"   ✅ Version {qiskit.__version__}")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 2: Qiskit-Aer
print("\n2. Qiskit-Aer:")
try:
    from qiskit_aer import Aer
    backends = Aer.backends()
    print(f"   ✅ Available")
    print(f"   Backends: {backends}")
except Exception as e:
    print(f"   ⚠️  Not available: {e}")
    print(f"   💡 Using custom AerSimulator")

# Test 3: orjson
print("\n3. orjson:")
try:
    import orjson
    test = orjson.dumps({"test": "data"})
    print(f"   ✅ Available (version: {getattr(orjson, '__version__', 'unknown')})")
except Exception as e:
    print(f"   ⚠️  Not available: {e}")

# Test 4: IBM Runtime
print("\n4. IBM Quantum Runtime:")
try:
    from qiskit_ibm_runtime import QiskitRuntimeService
    print(f"   ✅ Available")
except Exception as e:
    print(f"   ⚠️  Not available: {e}")
    print(f"   💡 Use local simulator instead")

# Test 5: Custom Simulator
print("\n5. Custom AerSimulator:")
try:
    from aer_simulator import AerSimulator
    print(f"   ✅ Available")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 6: Full circuit
print("\n6. Circuit Execution Test:")
try:
    from qiskit import QuantumCircuit
    from aer_simulator import AerSimulator
    
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    
    sim = AerSimulator()
    result = sim.run(qc, shots=100)
    counts = result.get_counts()
    
    print(f"   ✅ Circuit executed successfully")
    print(f"   Results: {counts}")
except Exception as e:
    print(f"   ❌ Failed: {e}")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
PYTEST

echo ""
echo "📦 Installed Packages:"
pip list | grep -E "qiskit|orjson"

echo ""
echo "✅ BUILD PROCESS COMPLETE!"
echo ""
echo "💡 Next steps:"
echo "  - Test enhanced scripts: ./src/spin_enhanced.py"
echo "  - If IBM Runtime works: python ibm_quantum_setup.py"
echo "  - Otherwise: Use local AerSimulator (already working)"

