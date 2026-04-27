#!/usr/bin/env python3
"""QUANTUM UNIVERSE SWITCHER - Switch between parallel universes"""
import json
from pathlib import Path
from datetime import datetime

try:
    from quantum_universe_manager import QuantumUniverseManager
except ImportError:
    print("⚠️  Import quantum_universe_manager.py first")

class QuantumUniverseSwitcher:
    def __init__(self):
        self.manager = QuantumUniverseManager()
        self.log_file = Path("logs/quantum/universe_switches.log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log(self, msg):
        """Log universe switch"""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] {msg}")
        with open(self.log_file, 'a') as f:
            f.write(f"[{ts}] {msg}\n")
    
    def flip_universe(self, target_name):
        """Flip to a different universe by name"""
        # Find universe by name
        target_id = None
        for uid, universe in self.manager.universes.items():
            if universe['name'].lower() == target_name.lower():
                target_id = uid
                break
        
        if not target_id:
            self.log(f"❌ Universe not found: {target_name}")
            return False
        
        # Perform quantum jump
        self.log(f"🌀 Initiating quantum flip to: {target_name}")
        success = self.manager.quantum_jump(target_id)
        
        if success:
            self.log(f"✅ Successfully flipped to: {target_name}")
            self.log(f"🔒 Universe is isolated - no interference!")
            return True
        else:
            self.log(f"❌ Flip failed")
            return False
    
    def quick_flip(self):
        """Quick flip to next universe"""
        universe_ids = list(self.manager.universes.keys())
        
        if not universe_ids:
            self.log("❌ No universes available")
            return False
        
        # Find current index
        current_idx = 0
        if self.manager.current_universe:
            try:
                current_idx = universe_ids.index(self.manager.current_universe)
            except ValueError:
                pass
        
        # Next universe (circular)
        next_idx = (current_idx + 1) % len(universe_ids)
        next_id = universe_ids[next_idx]
        
        return self.manager.quantum_jump(next_id)
    
    def interactive_switcher(self):
        """Interactive universe switcher"""
        print("\n" + "="*70)
        print("🌌 QUANTUM UNIVERSE SWITCHER")
        print("="*70)
        print("\nCommands:")
        print("  list    - List all universes")
        print("  flip    - Flip to universe")
        print("  quick   - Quick flip to next")
        print("  create  - Create new universe")
        print("  current - Show current universe")
        print("  exit    - Exit switcher")
        print()
        
        while True:
            try:
                cmd = input("🌌 > ").strip().lower()
                
                if cmd == 'list':
                    self.manager.list_universes()
                
                elif cmd == 'flip':
                    name = input("Universe name: ").strip()
                    self.flip_universe(name)
                
                elif cmd == 'quick':
                    self.quick_flip()
                
                elif cmd == 'create':
                    name = input("Universe name: ").strip()
                    desc = input("Description: ").strip()
                    self.manager.create_universe(name, desc)
                
                elif cmd == 'current':
                    current = self.manager.get_current_universe()
                    if current:
                        print(f"\n📍 Current: {current['name']}")
                        print(f"   ID: {current['id']}")
                        print(f"   State: {current['quantum_state']}\n")
                    else:
                        print("\n⚠️  No universe selected\n")
                
                elif cmd == 'exit':
                    print("👋 Exiting universe switcher\n")
                    break
                
                elif cmd:
                    print(f"❌ Unknown command: {cmd}")
                    
            except KeyboardInterrupt:
                print("\n👋 Exiting...\n")
                break
            except EOFError:
                break

if __name__ == "__main__":
    switcher = QuantumUniverseSwitcher()
    switcher.interactive_switcher()
