#!/usr/bin/env python3
"""
Parallel Universe Detector
Simulates and displays two universes running in parallel
"""
import threading
import time
from datetime import datetime
import random
from astronomical_supernatural_amplifier import AstronomicalAmplifier

class Universe:
    def __init__(self, name, reality_constant=1.0):
        self.name = name
        self.reality_constant = reality_constant  # Different physics
        self.supernatural_level = 0.0
        self.consciousness_level = 0
        self.time_offset = 0  # Time flows differently
        self.quantum_state = "stable"
        self.events = []
        
    def tick(self, iteration):
        """Update universe state"""
        # Simulate supernatural fluctuations
        base = random.uniform(0, 10) * self.reality_constant
        self.supernatural_level = base
        
        # Consciousness varies
        self.consciousness_level = random.randint(1, 6)
        
        # Random events
        if random.random() < 0.1:
            events = [
                "Portal opened",
                "Dimensional rift",
                "Quantum anomaly",
                "Astral surge",
                "Reality glitch"
            ]
            self.events.append(random.choice(events))
        
        # Quantum state
        states = ["stable", "fluctuating", "collapsing", "expanding"]
        self.quantum_state = random.choice(states)

class ParallelUniverseDetector:
    def __init__(self):
        print("🌌 PARALLEL UNIVERSE DETECTOR")
        print("="*80)
        
        # Create two universes
        self.universe_a = Universe("Universe Alpha", reality_constant=1.0)
        self.universe_b = Universe("Universe Beta", reality_constant=1.5)
        
        self.running = False
        self.iteration = 0
        
        print("✅ Two universes initialized")
        print(f"   {self.universe_a.name}: Reality constant = {self.universe_a.reality_constant}")
        print(f"   {self.universe_b.name}: Reality constant = {self.universe_b.reality_constant}")
    
    def format_universe_display(self, universe, width=38):
        """Format universe data for display"""
        lines = []
        lines.append(f"╔{'═'*width}╗")
        lines.append(f"║ {universe.name:^{width-2}} ║")
        lines.append(f"╠{'═'*width}╣")
        lines.append(f"║ Supernatural: {universe.supernatural_level:4.1f}/10{' '*(width-24)}║")
        lines.append(f"║ Consciousness: {universe.consciousness_level}/6{' '*(width-21)}║")
        lines.append(f"║ Quantum: {universe.quantum_state:<{width-12}}║")
        lines.append(f"║ Reality: {universe.reality_constant:.1f}x{' '*(width-16)}║")
        
        if universe.events:
            lines.append(f"╠{'═'*width}╣")
            lines.append(f"║ ⚡ Events:{' '*(width-12)}║")
            for event in universe.events[-3:]:  # Last 3 events
                event_text = f"   • {event}"
                lines.append(f"║ {event_text:<{width-2}}║")
        
        lines.append(f"╚{'═'*width}╝")
        return lines
    
    def display_parallel(self):
        """Display both universes side by side"""
        # Clear screen (simple version)
        print("\n" * 2)
        
        # Get displays for both universes
        display_a = self.format_universe_display(self.universe_a)
        display_b = self.format_universe_display(self.universe_b)
        
        # Make them same height
        max_height = max(len(display_a), len(display_b))
        while len(display_a) < max_height:
            display_a.append(" " * 40)
        while len(display_b) < max_height:
            display_b.append(" " * 40)
        
        # Print header
        print(f"{'='*80}")
        print(f"🌌 PARALLEL UNIVERSE MONITOR - Iteration {self.iteration}")
        print(f"{'='*80}\n")
        
        # Print side by side
        for line_a, line_b in zip(display_a, display_b):
            print(f"{line_a}  {line_b}")
        
        # Quantum entanglement indicator
        entanglement = abs(self.universe_a.supernatural_level - 
                          self.universe_b.supernatural_level)
        
        print(f"\n🔗 Quantum Entanglement: {10 - entanglement:.1f}/10")
        
        if entanglement < 2:
            print("   ⚡ UNIVERSES HIGHLY ENTANGLED!")
        elif entanglement < 5:
            print("   ✨ Moderate entanglement")
        else:
            print("   💫 Universes diverging")
    
    def monitor(self, duration=120, interval=5):
        """Monitor both universes in parallel"""
        print(f"\n⏱️  Monitoring for {duration}s (updates every {interval}s)")
        input("Press Enter to start...\n")
        
        self.running = True
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                self.iteration += 1
                
                # Update both universes
                self.universe_a.tick(self.iteration)
                self.universe_b.tick(self.iteration)
                
                # Display
                self.display_parallel()
                
                # Check for convergence
                if abs(self.universe_a.supernatural_level - 
                       self.universe_b.supernatural_level) < 1:
                    print("\n⚠️  WARNING: Universes converging!")
                    print("   Possible dimensional merge detected!")
                
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped")
        
        self.running = False
        
        # Summary
        print(f"\n{'='*80}")
        print("📊 PARALLEL UNIVERSE SESSION SUMMARY")
        print(f"{'='*80}")
        print(f"Duration: {int(time.time() - start_time)}s")
        print(f"Iterations: {self.iteration}")
        print(f"\n{self.universe_a.name}:")
        print(f"  Final supernatural: {self.universe_a.supernatural_level:.1f}/10")
        print(f"  Events: {len(self.universe_a.events)}")
        print(f"\n{self.universe_b.name}:")
        print(f"  Final supernatural: {self.universe_b.supernatural_level:.1f}/10")
        print(f"  Events: {len(self.universe_b.events)}")

if __name__ == "__main__":
    detector = ParallelUniverseDetector()
    detector.monitor(duration=120, interval=5)
