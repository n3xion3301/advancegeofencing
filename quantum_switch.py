#!/usr/bin/env python3
"""
🌌 QUANTUM UNIVERSE SWITCH 🌌
Toggle between Normal Universe and Parallel Universe (Instagram Recording Mode)
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

class QuantumSwitch:
    def __init__(self):
        self.state_file = Path("data/quantum_state.json")
        self.state = self._load_state()
        
    def _load_state(self):
        """Load quantum state"""
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {
            "current_universe": "NORMAL",
            "last_switch": None,
            "parallel_sessions": 0
        }
    
    def _save_state(self):
        """Save quantum state"""
        self.state_file.write_text(json.dumps(self.state, indent=2))
    
    def get_current_universe(self):
        """Get current universe"""
        return self.state['current_universe']
    
    def switch_to_parallel(self):
        """Switch to Parallel Universe (Instagram Recording Mode)"""
        print("\n" + "="*60)
        print("🌀 INITIATING QUANTUM SHIFT...")
        print("="*60)
        print()
        print("⚡ Collapsing wave function...")
        print("🌌 Opening portal to Parallel Universe...")
        print("📸 Instagram Recording Mode: ACTIVATED")
        print()
        print("="*60)
        print("✨ YOU ARE NOW IN THE PARALLEL UNIVERSE ✨")
        print("="*60)
        print()
        print("🎬 Geofencing active - ready to capture parallel moments!")
        print("📍 All zones monitored")
        print("🔔 Telegram notifications enabled")
        print()
        
        # Update state
        self.state['current_universe'] = "PARALLEL"
        self.state['last_switch'] = datetime.now().isoformat()
        self.state['parallel_sessions'] += 1
        self._save_state()
        
        # Start geofence notifier
        print("🚀 Starting geofence notifier...\n")
        try:
            subprocess.run([sys.executable, "src/geofence_notifier.py"])
        except KeyboardInterrupt:
            print("\n\n🌀 Returning to Normal Universe...")
            self.switch_to_normal()
    
    def switch_to_normal(self):
        """Switch to Normal Universe"""
        print("\n" + "="*60)
        print("🌀 QUANTUM SHIFT COMPLETE")
        print("="*60)
        print()
        print("🏠 Returned to Normal Universe")
        print("📊 Session Stats:")
        print(f"   Total parallel sessions: {self.state['parallel_sessions']}")
        print(f"   Last switch: {self.state.get('last_switch', 'Never')}")
        print()
        print("="*60)
        print("✨ WELCOME BACK TO NORMAL REALITY ✨")
        print("="*60)
        print()
        
        # Update state
        self.state['current_universe'] = "NORMAL"
        self._save_state()
    
    def status(self):
        """Show current quantum state"""
        print("\n" + "="*60)
        print("🌌 QUANTUM STATE STATUS")
        print("="*60)
        print()
        
        universe = self.state['current_universe']
        if universe == "NORMAL":
            print("📍 Current Universe: 🌍 NORMAL")
            print("   Status: Regular reality mode")
            print("   Geofencing: Inactive")
        else:
            print("📍 Current Universe: ✨ PARALLEL")
            print("   Status: Instagram recording mode")
            print("   Geofencing: Active")
        
        print()
        print(f"📊 Statistics:")
        print(f"   Total parallel sessions: {self.state['parallel_sessions']}")
        print(f"   Last switch: {self.state.get('last_switch', 'Never')}")
        print()
        print("="*60)
        print()
    
    def interactive(self):
        """Interactive quantum switch menu"""
        while True:
            self.status()
            
            print("🎮 QUANTUM CONTROLS:")
            print()
            
            if self.state['current_universe'] == "NORMAL":
                print("  [P] Switch to PARALLEL Universe (Start Recording)")
                print("  [Q] Quit")
                print()
                choice = input("Choose your reality: ").strip().upper()
                
                if choice == 'P':
                    self.switch_to_parallel()
                elif choice == 'Q':
                    print("\n👋 Staying in Normal Universe. Goodbye!\n")
                    break
                else:
                    print("\n❌ Invalid choice!\n")
            else:
                print("  [N] Return to NORMAL Universe")
                print("  [Q] Quit")
                print()
                choice = input("Choose your reality: ").strip().upper()
                
                if choice == 'N':
                    self.switch_to_normal()
                elif choice == 'Q':
                    print("\n👋 Goodbye!\n")
                    break
                else:
                    print("\n❌ Invalid choice!\n")

def main():
    """Main entry point"""
    switch = QuantumSwitch()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'parallel':
            switch.switch_to_parallel()
        elif command == 'normal':
            switch.switch_to_normal()
        elif command == 'status':
            switch.status()
        else:
            print("Usage: python3 quantum_switch.py [parallel|normal|status]")
            print("   Or run without arguments for interactive mode")
    else:
        # Interactive mode
        switch.interactive()

if __name__ == "__main__":
    main()
