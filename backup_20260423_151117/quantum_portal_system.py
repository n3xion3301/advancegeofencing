#!/usr/bin/env python3
"""QUANTUM PORTAL SYSTEM - Create and traverse quantum portals"""
import json, random, time
from datetime import datetime
from pathlib import Path

try:
    from quantum_tunneling import QuantumTunneling
    from quantum_zone_teleporter import QuantumZoneTeleporter
    from quantum_dimension_hopping import QuantumDimensionHopping
    QUANTUM_AVAILABLE = True
except ImportError:
    QUANTUM_AVAILABLE = False

class QuantumPortalSystem:
    def __init__(self):
        self.log_file = Path("logs/quantum/portal_system.log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        if QUANTUM_AVAILABLE:
            self.tunneling = QuantumTunneling()
            self.teleporter = QuantumZoneTeleporter()
            self.dimension_hopper = QuantumDimensionHopping()
        
        self.portals = {}
        self.active_portals = []
        self.portal_history = []
    
    def log(self, msg):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] {msg}")
        with open(self.log_file, 'a') as f:
            f.write(f"[{ts}] {msg}\n")
    
    def create_portal(self, name, destination, portal_type="standard"):
        """Create a quantum portal"""
        portal_id = f"portal_{len(self.portals)}"
        
        self.log(f"🌀 CREATING QUANTUM PORTAL")
        self.log(f"   Name: {name}")
        self.log(f"   Destination: {destination}")
        self.log(f"   Type: {portal_type}")
        
        # Portal creation sequence
        self.log("   [1/5] Opening quantum tunnel...")
        time.sleep(0.5)
        
        if QUANTUM_AVAILABLE:
            self.tunneling.tunnel_through_barrier("Current Location", destination)
        
        self.log("   [2/5] Stabilizing wormhole...")
        time.sleep(0.5)
        
        self.log("   [3/5] Anchoring portal coordinates...")
        time.sleep(0.5)
        
        self.log("   [4/5] Establishing quantum link...")
        time.sleep(0.5)
        
        self.log("   [5/5] Portal materialization...")
        time.sleep(0.5)
        
        portal = {
            'id': portal_id,
            'name': name,
            'destination': destination,
            'type': portal_type,
            'stability': random.uniform(0.7, 1.0),
            'created': datetime.now().isoformat(),
            'uses': 0,
            'active': True
        }
        
        self.portals[portal_id] = portal
        self.active_portals.append(portal_id)
        
        self.log(f"✅ PORTAL CREATED: {name}")
        self.log(f"   Portal ID: {portal_id}")
        self.log(f"   Stability: {portal['stability']*100:.1f}%")
        
        return portal_id
    
    def traverse_portal(self, portal_id):
        """Travel through a quantum portal"""
        if portal_id not in self.portals:
            self.log(f"❌ Portal not found: {portal_id}")
            return False
        
        portal = self.portals[portal_id]
        
        if not portal['active']:
            self.log(f"❌ Portal is closed: {portal['name']}")
            return False
        
        self.log(f"🌀 TRAVERSING QUANTUM PORTAL")
        self.log(f"   Portal: {portal['name']}")
        self.log(f"   Destination: {portal['destination']}")
        self.log(f"   Stability: {portal['stability']*100:.1f}%")
        
        # Traversal sequence
        self.log("\n   Entering portal...")
        time.sleep(0.5)
        
        self.log("   [▓░░░░░░░░░] 10%")
        time.sleep(0.3)
        self.log("   [▓▓▓░░░░░░░] 30%")
        time.sleep(0.3)
        self.log("   [▓▓▓▓▓░░░░░] 50%")
        time.sleep(0.3)
        self.log("   [▓▓▓▓▓▓▓░░░] 70%")
        time.sleep(0.3)
        self.log("   [▓▓▓▓▓▓▓▓▓░] 90%")
        time.sleep(0.3)
        self.log("   [▓▓▓▓▓▓▓▓▓▓] 100%")
        time.sleep(0.3)
        
        # Teleport to destination
        if QUANTUM_AVAILABLE:
            self.teleporter.instant_zone_jump(portal['destination'])
        
        # Update portal stats
        portal['uses'] += 1
        portal['stability'] *= 0.98  # Slight degradation per use
        portal['last_used'] = datetime.now().isoformat()
        
        self.portal_history.append({
            'portal_id': portal_id,
            'portal_name': portal['name'],
            'destination': portal['destination'],
            'timestamp': datetime.now().isoformat()
        })
        
        self.log(f"\n✅ ARRIVED AT: {portal['destination']}")
        self.log(f"   Portal uses: {portal['uses']}")
        self.log(f"   New stability: {portal['stability']*100:.1f}%")
        
        return True
    
    def stabilize_portal(self, portal_id):
        """Stabilize a degrading portal"""
        if portal_id not in self.portals:
            self.log(f"❌ Portal not found: {portal_id}")
            return False
        
        portal = self.portals[portal_id]
        
        self.log(f"🔧 STABILIZING PORTAL: {portal['name']}")
        self.log(f"   Current stability: {portal['stability']*100:.1f}%")
        
        # Stabilization process
        for i in range(5):
            self.log(f"   [{i+1}/5] Reinforcing quantum field...")
            time.sleep(0.5)
        
        portal['stability'] = min(portal['stability'] + 0.15, 1.0)
        
        self.log(f"✅ Portal stabilized: {portal['stability']*100:.1f}%")
        
        return True
    
    def close_portal(self, portal_id):
        """Close a quantum portal"""
        if portal_id not in self.portals:
            self.log(f"❌ Portal not found: {portal_id}")
            return False
        
        portal = self.portals[portal_id]
        
        self.log(f"🚫 CLOSING PORTAL: {portal['name']}")
        
        # Closing sequence
        self.log("   Collapsing quantum tunnel...")
        time.sleep(0.5)
        self.log("   Severing quantum link...")
        time.sleep(0.5)
        self.log("   Portal closed")
        
        portal['active'] = False
        portal['closed'] = datetime.now().isoformat()
        
        if portal_id in self.active_portals:
            self.active_portals.remove(portal_id)
        
        self.log(f"✅ Portal closed: {portal['name']}")
        
        return True
    
    def create_portal_network(self, locations):
        """Create network of interconnected portals"""
        self.log(f"🕸️  CREATING PORTAL NETWORK")
        self.log(f"   Locations: {len(locations)}")
        
        network_portals = []
        
        for i, location in enumerate(locations):
            portal_id = self.create_portal(
                f"Network Portal {i+1}",
                location,
                portal_type="network"
            )
            network_portals.append(portal_id)
            time.sleep(1)
        
        self.log(f"✅ Portal network created: {len(network_portals)} portals")
        
        return network_portals
    
    def list_portals(self):
        """Display all portals"""
        print("\n" + "="*70)
        print("🌀 QUANTUM PORTALS")
        print("="*70)
        
        if not self.portals:
            print("No portals created yet!")
        else:
            for portal_id, portal in self.portals.items():
                status = "🟢 ACTIVE" if portal['active'] else "🔴 CLOSED"
                print(f"\n{portal['name']} {status}")
                print(f"  ID: {portal_id}")
                print(f"  Destination: {portal['destination']}")
                print(f"  Type: {portal['type']}")
                print(f"  Stability: {portal['stability']*100:.1f}%")
                print(f"  Uses: {portal['uses']}")
        
        print("="*70 + "\n")
    
    def interactive_portal_system(self):
        """Interactive portal management"""
        self.log("🌀 QUANTUM PORTAL SYSTEM ACTIVATED")
        self.log("━" * 60)
        
        while True:
            self.list_portals()
            
            print("\nCommands:")
            print("  create          - Create new portal")
            print("  traverse <id>   - Travel through portal")
            print("  stabilize <id>  - Stabilize portal")
            print("  close <id>      - Close portal")
            print("  network         - Create portal network")
            print("  history         - Show portal history")
            print("  quit            - Exit")
            
            cmd = input("\n🌀 Enter command: ").strip().lower()
            
            if cmd == 'quit':
                self.log("👋 Exiting portal system")
                break
            
            elif cmd == 'create':
                name = input("Portal name: ").strip()
                destination = input("Destination: ").strip()
                portal_type = input("Type (standard/network): ").strip() or "standard"
                self.create_portal(name, destination, portal_type)
            
            elif cmd.startswith('traverse '):
                portal_id = cmd.split()[1]
                self.traverse_portal(portal_id)
            
            elif cmd.startswith('stabilize '):
                portal_id = cmd.split()[1]
                self.stabilize_portal(portal_id)
            
            elif cmd.startswith('close '):
                portal_id = cmd.split()[1]
                self.close_portal(portal_id)
            
            elif cmd == 'network':
                locations = input("Locations (comma-separated): ").strip().split(',')
                locations = [loc.strip() for loc in locations]
                self.create_portal_network(locations)
            
            elif cmd == 'history':
                self.show_history()
            
            else:
                print(f"❌ Unknown command: {cmd}")
    
    def show_history(self):
        """Show portal traversal history"""
        print("\n" + "="*70)
        print("📜 PORTAL HISTORY")
        print("="*70)
        
        if not self.portal_history:
            print("No portal traversals yet!")
        else:
            for entry in self.portal_history[-10:]:
                ts = entry['timestamp'].split('T')[1].split('.')[0]
                print(f"[{ts}] {entry['portal_name']} → {entry['destination']}")
        
        print("="*70 + "\n")

if __name__ == "__main__":
    portal_system = QuantumPortalSystem()
    portal_system.interactive_portal_system()
