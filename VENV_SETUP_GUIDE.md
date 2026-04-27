# 🐍 Python Virtual Environment Setup Guide

## Quick Reference Card

```bash
# ACTIVATE (Most Important!)
source quantum_env/bin/activate

# DEACTIVATE
deactivate

# CHECK IF ACTIVE
echo $VIRTUAL_ENV

📋 Table of Contents

[What is a Virtual Environment?](#what-is-a-virtual-environment)
[Initial Setup](#initial-setup)
[Daily Usage](#daily-usage)
[Package Management](#package-management)
[Troubleshooting](#troubleshooting)
[Compatibility](#compatibility)


🤔 What is a Virtual Environment?
A virtual environment is an isolated Python environment that:

✅ Keeps project dependencies separate
✅ Prevents version conflicts
✅ Allows different Python versions per project
✅ Makes projects portable and reproducible

Our venv: quantum_env (located in project root)

🚀 Initial Setup
First Time Setup (Already Done!)
# Navigate to project
cd ~/advancegeofencing

# Create virtual environment
python3 -m venv quantum_env

# Activate it
source quantum_env/bin/activate

# Install dependencies
pip install -r requirements.txtInsert at cursor
Verify Installation
# Should show path inside quantum_env
which python
# Output: /data/data/com.termux/files/home/advancegeofencing/quantum_env/bin/python

# Should show path inside quantum_env
which pip
# Output: /data/data/com.termux/files/home/advancegeofencing/quantum_env/bin/pip

# Check Python version
python --version

# List installed packages
pip listInsert at cursor

💼 Daily Usage
Every Time You Work on the Project
# 1. Navigate to project directory
cd ~/advancegeofencing

# 2. Activate virtual environment
source quantum_env/bin/activate

# You should see (quantum_env) in your prompt:
# (quantum_env) ~/advancegeofencing $

# 3. Now you can run scripts
./src/spin_enhanced.py
python src/interference_enhanced.py

# 4. When done, deactivate
deactivateInsert at cursor
Visual Indicators
ACTIVATED:
(quantum_env) ~/advancegeofencing $
              ^^^^^^^^^^^^^ This prefix shows venv is activeInsert at cursor
NOT ACTIVATED:
~/advancegeofencing $
No prefix = venv NOT activeInsert at cursor
Quick Check Script
# Create a quick check script
cat > check_venv.sh << 'EOF'
#!/bin/bash
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Virtual environment ACTIVE"
    echo "📍 Location: $VIRTUAL_ENV"
    echo "🐍 Python: $(which python)"
else
    echo "❌ Virtual environment NOT active"
    echo "💡 Run: source quantum_env/bin/activate"
fi
EOF

chmod +x check_venv.sh

# Use it anytime
./check_venv.shInsert at cursor

📦 Package Management
Installing New Packages
# Make sure venv is active first!
source quantum_env/bin/activate

# Install a package
pip install package_name

# Install specific version
pip install package_name==1.2.3

# Install from requirements.txt
pip install -r requirements.txt

# Update requirements.txt after installing
pip freeze > requirements.txtInsert at cursor
Checking Installed Packages
# List all packages
pip list

# Show specific package info
pip show qiskit

# Check for outdated packages
pip list --outdatedInsert at cursor
Updating Packages
# Update a specific package
pip install --upgrade package_name

# Update pip itself
pip install --upgrade pipInsert at cursor

🔧 Troubleshooting
Problem: "Command not found" when running scripts
Solution:
# Activate venv first!
source quantum_env/bin/activate

# Then run script
./src/spin_enhanced.pyInsert at cursor
Problem: "ModuleNotFoundError: No module named 'qiskit'"
Solution:
# 1. Activate venv
source quantum_env/bin/activate

# 2. Install missing package
pip install qiskit

# 3. Or reinstall all requirements
pip install -r requirements.txtInsert at cursor
Problem: Forgot if venv is active
Solution:
# Check environment variable
echo $VIRTUAL_ENV

# If empty, activate it
source quantum_env/bin/activateInsert at cursor
Problem: Wrong Python version
Solution:
# Check which Python is being used
which python
python --version

# Should point to quantum_env/bin/python
# If not, activate venv
source quantum_env/bin/activateInsert at cursor
Problem: Need to recreate venv
Solution:
# 1. Deactivate if active
deactivate

# 2. Remove old venv
rm -rf quantum_env

# 3. Create new venv
python3 -m venv quantum_env

# 4. Activate
source quantum_env/bin/activate

# 5. Reinstall packages
pip install -r requirements.txtInsert at cursor

🔄 Compatibility
Python Version
# Our venv uses Python 3.13
python --version
# Python 3.13.xInsert at cursor
Termux Compatibility
✅ Works on Termux (Android)

Virtual environments work perfectly on Termux
No special configuration needed
Same commands as Linux

Package Compatibility
Installed Packages:

✅ qiskit - Quantum computing framework
✅ numpy - Numerical computing
✅ matplotlib - Plotting (if needed)
✅ Custom packages (aer_simulator.py)

Known Issues:

Some packages may need compilation
Use pip install --no-binary :all: if needed


📝 Best Practices
DO ✅
# Always activate before working
source quantum_env/bin/activate

# Keep requirements.txt updated
pip freeze > requirements.txt

# Use relative imports in scripts
from aer_simulator import AerSimulator

# Deactivate when done
deactivateInsert at cursor
DON'T ❌
# Don't run scripts without activating venv
./src/spin_enhanced.py  # ❌ (if venv not active)

# Don't install packages globally
sudo pip install qiskit  # ❌

# Don't commit venv to git
git add quantum_env/  # ❌ (already in .gitignore)

# Don't delete venv accidentally
rm -rf quantum_env  # ❌ (unless recreating)Insert at cursor

🎯 Common Workflows
Starting a Work Session
cd ~/advancegeofencing
source quantum_env/bin/activate
./check_venv.sh  # Verify
# Start coding!Insert at cursor
Running Tests
source quantum_env/bin/activate
python -m pytest tests/
# or
./src/spin_enhanced.pyInsert at cursor
Adding New Dependencies
source quantum_env/bin/activate
pip install new_package
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Add new_package dependency"Insert at cursor
Sharing Project
# Other person clones repo
git clone https://github.com/n3xion3301/advancegeofencing.git
cd advancegeofencing

# They create their own venv
python3 -m venv quantum_env
source quantum_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Ready to go!Insert at cursor

🆘 Emergency Commands
# If everything is broken, start fresh:

# 1. Deactivate
deactivate

# 2. Backup requirements
cp requirements.txt requirements.txt.backup

# 3. Remove venv
rm -rf quantum_env

# 4. Recreate
python3 -m venv quantum_env
source quantum_env/bin/activate

# 5. Reinstall
pip install -r requirements.txt

# 6. Test
python -c "import qiskit; print('✅ Qiskit works!')"Insert at cursor

📚 Additional Resources

[Python venv documentation](https://docs.python.org/3/library/venv.html)
[Pip documentation](https://pip.pypa.io/)
[Qiskit installation guide](https://qiskit.org/documentation/getting_started.html)


🎓 Quick Quiz
Before running any script, ask yourself:

❓ Am I in the project directory? → cd ~/advancegeofencing
❓ Is venv activated? → source quantum_env/bin/activate
❓ Do I see (quantum_env) in prompt? → Should see it
❓ Are packages installed? → pip list

If all YES → You're ready to code! 🚀

📌 Bookmark This!
Most Important Commands:
# ACTIVATE (memorize this!)
source quantum_env/bin/activate

# CHECK
echo $VIRTUAL_ENV

# DEACTIVATE
deactivateInsert at cursor

Created by: n3xion3301
Project: Advanced Geofencing with Quantum Computing
Last Updated: 2026-04-24

💡 Pro Tip: Create an alias in your shell config:
# Add to ~/.bashrc or ~/.zshrc
alias qenv='cd ~/advancegeofencing && source quantum_env/bin/activate'

# Then just type:
qenvInsert at cursor
