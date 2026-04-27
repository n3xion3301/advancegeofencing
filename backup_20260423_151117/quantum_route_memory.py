#!/usr/bin/env python3
"""QUANTUM ROUTE MEMORY - Save & teleport to favorite routes instantly"""
import json, time
from datetime import datetime
from pathlib import Path

try:
    from quantum_zone_teleporter import QuantumZoneTeleporter
    from quantum_tunneling import QuantumTunneling
    QUANTUM_AVAILABLE = True
except ImportError:
    QUANTUM_AVAILABLE = False

class QuantumRouteMemory:
    def __init__(self):
        self.log_file = Path("logs/quantum/route_memory.log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.routes_file = Path("data/quantum_routes.json")
        self.routes_file.parent.mkdir(parents=True, exist_ok=True)
        
        if QUANTUM_AVAILABLE:
            self.teleporter = QuantumZoneTeleporter()
            self.tunneling = QuantumTunneling()
        
        self.routes = self.load_routes()
        self.teleport_history = []
    
    def log(self, msg):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] {msg}")
        with open(self.log_file, 'a') as f:
            f.write(f"[{ts}] {msg}\n")
    
    def load_routes(self):
        """Load saved routes"""
        if self.routes_file.exists():
            with open(self.routes_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_routes(self):
        """Save routes to file"""
        with open(self.routes_file, 'w') as f:
            json.dump(self.routes, f, indent=2)
        self.log(f"💾 Saved {len(self.routes)} routes")
    
    def save_route(self, key, name, location, coordinates=None):
        """Save a teleportation route with hotkey"""
        route = {
            'name': name,
            'location': location,
            'coordinates': coordinates,
            'saved': datetime.now().isoformat(),
            'teleport_count': 0
        }
        
        self.routes[key] = route
        self.save_routes()
        
        self.log(f"🗺️  ROUTE SAVED!")
        self.log(f"   Key: [{key}]")
        self.log(f"   Name: {name}")
        self.log(f"   Location: {location}")
        return True
    
    def teleport_to_route(self, key):
        """Teleport to saved route by key"""
        if key not in self.routes:
            self.log(f"❌ Route [{key}] not found!")
            return False
        
        route = self.routes[key]
        
        self.log(f"⚡ QUANTUM TELEPORTATION VIA ROUTE [{key}]")
        self.log(f"   Destination: {route['name']}")
        self.log(f"   Location: {route['location']}")
        
        # Quantum tunnel to destination
        if QUANTUM_AVAILABLE:
            self.tunneling.tunnel_through_barrier("Current", route['location'])
            self.teleporter.instant_zone_jump(route['location'])
        
        # Update teleport count
        route['teleport_count'] += 1
        route['last_teleport'] = datetime.now().isoformat()
        self.save_routes()
        
        # Log history
        self.teleport_history.append({
            'key': key,
            'route': route['name'],
            'timestamp': datetime.now().isoformat()
        })
        
        self.log(f"✅ TELEPORTED to {route['name']}!")
        self.log(f"   Times visited: {route['teleport_count']}")
        return True
    
    def list_routes(self):
        """Display all saved routes"""
        print("\n" + "="*70)
        print("🗺️  QUANTUM ROUTE MEMORY")
        print("="*70)
        
        if not self.routes:
            print("No routes saved yet!")
        else:
            for key, route in self.routes.items():
                print(f"\n[{key}] {route['name']}")
                print(f"    Location: {route['location']}")
                print(f"    Teleports: {route['teleport_count']}")
                if 'last_teleport' in route:
                    print(f"    Last visit: {route['last_teleport']}")
        
        print("="*70 + "\n")
    
    def interactive_teleport(self):
        """Interactive route teleportation"""
        self.log("🌌 QUANTUM ROUTE TELEPORTER ACTIVATED")
        self.log("━" * 60)
        
        while True:
            self.list_routes()
            
            print("\nCommands:")
            print("  [key]  - Teleport to route")
            print("  save   - Save new route")
            print("  list   - Show all routes")
            print("  history - Show teleport history")
            print("  quit   - Exit")
            
            cmd = input("\n🌀 Enter command: ").strip().lower()
            
            if cmd == 'quit':
                self.log("👋 Exiting route teleporter")
                break
            
            elif cmd == 'save':
                key = input("Hotkey (1-9, a-z): ").strip()
                name = input("Route name: ").strip()
                location = input("Location: ").strip()
                
                self.save_route(key, name, location)
            
            elif cmd == 'list':
                self.list_routes()
            
            elif cmd == 'history':
                self.show_history()
            
            elif cmd in self.routes:
                self.teleport_to_route(cmd)
                time.sleep(2)
            
            else:
                print(f"❌ Unknown command or route: {cmd}")
    
    def show_history(self):
        """Show teleportation history"""
        print("\n" + "="*70)
        print("📜 TELEPORTATION HISTORY")
        print("="*70)
        
        if not self.teleport_history:
            print("No teleportations yet!")
        else:
            for entry in self.teleport_history[-10:]:  # Last 10
                ts = entry['timestamp'].split('T')[1].split('.')[0]
                print(f"[{ts}] [{entry['key']}] → {entry['route']}")
        
        print("="*70 + "\n")
    
    def get_mayhem_stats(self):
        """Get all your quantum mayhem statistics"""
        total_teleports = sum(r['teleport_count'] for r in self.routes.values())
        
        stats = {
            'total_routes': len(self.routes),
            'total_teleports': total_teleports,
            'total_history': len(self.teleport_history),
            'favorite_route': None
        }
        
        # Find most used route
        if self.routes:
            favorite = max(self.routes.items(), key=lambda x: x[1]['teleport_count'])
            stats['favorite_route'] = {
                'key': favorite[0],
                'name': favorite[1]['name'],
                'count': favorite[1]['teleport_count']
            }
        
        return stats

if __name__ == "__main__":
    route_memory = QuantumRouteMemory()
    
    # Example: Save some routes
    route_memory.save_route('1', 'Home Base', 'Home Zone', {'lat': 0, 'lon': 0})
    route_memory.save_route('2', 'Work HQ', 'Work Zone', {'lat': 1, 'lon': 1})
    route_memory.save_route('3', 'Gym', 'Gym Zone', {'lat': 2, 'lon': 2})
    
    # Start interactive mode
    route_memory.interactive_teleport()
