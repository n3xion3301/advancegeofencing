#!/bin/bash

echo "🧪 TESTING ALL GEOFENCING TOOLS"
echo "================================"
echo ""

# Test counter
PASSED=0
FAILED=0

test_command() {
    local name="$1"
    local cmd="$2"
    
    echo -n "Testing $name... "
    if eval "$cmd" > /dev/null 2>&1; then
        echo "✅ PASS"
        ((PASSED++))
    else
        echo "❌ FAIL"
        ((FAILED++))
    fi
}

test_file() {
    local name="$1"
    local file="$2"
    
    echo -n "Checking $name... "
    if [ -f "$file" ]; then
        echo "✅ EXISTS"
        ((PASSED++))
    else
        echo "❌ MISSING"
        ((FAILED++))
    fi
}

test_python_script() {
    local name="$1"
    local script="$2"
    
    echo -n "Testing $name... "
    if python -m py_compile "$script" 2>/dev/null; then
        echo "✅ VALID"
        ((PASSED++))
    else
        echo "❌ SYNTAX ERROR"
        ((FAILED++))
    fi
}

echo "📋 PART 1: TERMUX API TOOLS"
echo "----------------------------"
test_command "termux-location" "which termux-location"
test_command "termux-notification" "termux-notification --help"
test_command "termux-camera-photo" "which termux-camera-photo"
test_command "termux-vibrate" "which termux-vibrate"
echo ""

echo "📋 PART 2: CONFIGURATION FILES"
echo "-------------------------------"
test_file "zones.json" "config/zones.json"
test_file "telegram_config.json" "config/telegram_config.json"
echo ""

echo "📋 PART 3: PYTHON SCRIPTS"
echo "-------------------------"
test_python_script "geofence_monitor.py" "src/geofence_monitor.py"
test_python_script "android_location.py" "src/android_location.py"
test_python_script "telegram_notifier.py" "src/telegram_notifier.py"
test_python_script "geofence_background_service.py" "src/geofence_background_service.py"
test_python_script "outdoor_geofence_service.py" "src/outdoor_geofence_service.py"
echo ""

echo "📋 PART 4: SHELL SCRIPTS"
echo "------------------------"
test_file "start-geofence-service.sh" "start-geofence-service.sh"
test_file "start-outdoor-service.sh" "start-outdoor-service.sh"
test_file "stop-all-services.sh" "stop-all-services.sh"
test_file "status-all-services.sh" "status-all-services.sh"
echo ""

echo "📋 PART 5: DIRECTORIES"
echo "----------------------"
for dir in logs photos videos config src; do
    echo -n "Checking $dir/... "
    if [ -d "$dir" ]; then
        echo "✅ EXISTS"
        ((PASSED++))
    else
        echo "❌ MISSING"
        ((FAILED++))
    fi
done
echo ""

echo "📋 PART 6: FUNCTIONAL TESTS"
echo "---------------------------"

# Test location
echo -n "Testing GPS location... "
if termux-location 2>/dev/null | grep -q "latitude"; then
    echo "✅ WORKING"
    ((PASSED++))
else
    echo "❌ FAILED"
    ((FAILED++))
fi

# Test zones config
echo -n "Testing zones.json validity... "
if python -c "import json; json.load(open('config/zones.json'))" 2>/dev/null; then
    echo "✅ VALID JSON"
    ((PASSED++))
else
    echo "❌ INVALID JSON"
    ((FAILED++))
fi

# Test telegram config
echo -n "Testing telegram_config.json validity... "
if python -c "import json; json.load(open('config/telegram_config.json'))" 2>/dev/null; then
    echo "✅ VALID JSON"
    ((PASSED++))
else
    echo "❌ INVALID JSON"
    ((FAILED++))
fi

# Test geofence monitor import
echo -n "Testing GeofenceMonitor import... "
if python -c "from src.geofence_monitor import GeofenceMonitor" 2>/dev/null; then
    echo "✅ IMPORTS OK"
    ((PASSED++))
else
    echo "❌ IMPORT FAILED"
    ((FAILED++))
fi

# Test android location import
echo -n "Testing AndroidLocationProvider import... "
if python -c "from src.android_location import AndroidLocationProvider" 2>/dev/null; then
    echo "✅ IMPORTS OK"
    ((PASSED++))
else
    echo "❌ IMPORT FAILED"
    ((FAILED++))
fi

# Test telegram notifier import
echo -n "Testing TelegramNotifier import... "
if python -c "from src.telegram_notifier import TelegramNotifier" 2>/dev/null; then
    echo "✅ IMPORTS OK"
    ((PASSED++))
else
    echo "❌ IMPORT FAILED"
    ((FAILED++))
fi

echo ""
echo "================================"
echo "📊 TEST RESULTS"
echo "================================"
echo "✅ PASSED: $PASSED"
echo "❌ FAILED: $FAILED"
echo "📈 TOTAL:  $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 ALL TESTS PASSED! READY TO PUSH! 🚀"
    exit 0
else
    echo "⚠️  SOME TESTS FAILED! FIX BEFORE PUSHING!"
    exit 1
fi
