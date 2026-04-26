#!/usr/bin/env python3
"""
Integrate Astronomical Amplification with Supernatural Geofencing - FIXED
"""
from supernatural_containment_geofence import SupernaturalContainmentSystem
from astronomical_supernatural_amplifier import AstronomicalAmplifier
import time
from datetime import datetime

class AstroSupernaturalSystem(SupernaturalContainmentSystem):
    def __init__(self):
        super().__init__()
        self.astro = AstronomicalAmplifier(self.gps.simulator.current_lat, 
                                           self.gps.simulator.current_lon)
        print("🌌 Astronomical amplification integrated!")
    
    def monitor_supernatural_activity(self, interval=10, duration=300):
        """Enhanced monitoring with astronomy"""
        print("\n🌌 ASTRO-SUPERNATURAL MONITORING")
        print("="*60)
        
        # Show current astronomical status
        astro_status = self.astro.display_status()
        
        input("\nPress Enter to start monitoring...\n")
        
        start_time = time.time()
        iteration = 0
        max_supernatural = 0.0
        
        try:
            while time.time() - start_time < duration:
                iteration += 1
                elapsed = int(time.time() - start_time)
                
                print(f"\n{'='*60}")
                print(f"🔄 Iteration {iteration} - [{elapsed}s / {duration}s]")
                print(f"{'='*60}")
                
                # Get current location
                location = self.gps.get_current_location()
                
                if location:
                    print(f"📍 Location: {location['lat']:.6f}, {location['lon']:.6f}")
                    
                    # Check zone status
                    inside_zones = self.check_zone_status(location)
                    
                    # Get sensor data
                    sensor_data = self.astral.get_all_sensors()
                    
                    # Get astronomical amplification
                    astro_amp = self.astro.calculate_total_amplification()
                    
                    if inside_zones:
                        # INSIDE SUPERNATURAL ZONE
                        print(f"\n🔮 INSIDE SUPERNATURAL ZONE(S):")
                        
                        for iz in inside_zones:
                            zone = iz['zone']
                            print(f"\n   Zone: {zone.name}")
                            print(f"   Distance from center: {iz['distance']:.1f}m")
                            print(f"   Depth inside: {iz['depth']:.1f}m")
                            print(f"   Field strength: {iz['strength']:.1%}")
                            print(f"   Power level: {zone.power_level}/10")
                            print(f"   Astral amplification: {zone.astral_amplification}x")
                        
                        # Calculate base supernatural level
                        base_level = super().calculate_supernatural_level(inside_zones, sensor_data)
                        
                        # Apply astronomical amplification
                        supernatural_level = base_level * astro_amp['total_multiplier']
                        max_supernatural = max(max_supernatural, supernatural_level)
                        
                        print(f"\n⚡ SUPERNATURAL ACTIVITY:")
                        print(f"   Base level: {base_level:.1f}/10")
                        print(f"   Astro multiplier: {astro_amp['total_multiplier']:.2f}x")
                        print(f"   🌟 TOTAL: {supernatural_level:.1f}/10")
                        
                        # Show astronomical contributions
                        print(f"\n🌌 Astronomical Factors:")
                        print(f"   🌙 Moon: {astro_amp['moon']['phase_name']} ({astro_amp['moon']['power_multiplier']:.1%})")
                        print(f"   ☀️  Solar: {astro_amp['solar']['period']} ({astro_amp['solar']['power_multiplier']:.1%})")
                        
                        if astro_amp['special_events']:
                            print(f"\n⚡ SPECIAL CELESTIAL EVENTS:")
                            for event in astro_amp['special_events']:
                                print(f"   {event}")
                        
                        if supernatural_level >= 8.0:
                            print(f"\n   🌟 EXTREME supernatural activity!")
                            print(f"   🔮 Astral projection HIGHLY amplified")
                        elif supernatural_level >= 5.0:
                            print(f"\n   ✨ HIGH supernatural activity")
                            print(f"   🧘 Consciousness expansion active")
                        
                        # Activate barrier
                        if not self.barrier_active:
                            primary_zone = inside_zones[0]['zone']
                            self.activate_barrier(primary_zone)
                            self.current_zone = primary_zone
                        
                        print(f"\n🛡️  CONTAINMENT STATUS:")
                        print(f"   Barrier: 🟢 ACTIVE")
                        print(f"   ✅ Supernatural phenomena CONTAINED")
                        
                        if not self.inside_zone:
                            print(f"\n🚪 ENTERED SUPERNATURAL ZONE")
                            self.inside_zone = True
                    
                    else:
                        # OUTSIDE ALL ZONES
                        print(f"\n🌍 OUTSIDE ALL SUPERNATURAL ZONES")
                        print(f"   Supernatural activity: 0.0/10")
                        print(f"   ❌ No amplification (even with {astro_amp['total_multiplier']:.2f}x astro boost)")
                        
                        if self.inside_zone:
                            print(f"\n🚪 EXITED SUPERNATURAL ZONE")
                            self.deactivate_barrier()
                            self.inside_zone = False
                    
                    # Show sensor status
                    if sensor_data:
                        consciousness_level, feedback = self.astral.calculate_consciousness_level(sensor_data)
                        print(f"\n🧠 Consciousness Level: {consciousness_level}/6")
                        for fb in feedback[:2]:
                            print(f"   {fb}")
                
                print(f"\n⏳ Next check in {interval}s...")
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped")
        
        # Summary
        print(f"\n{'='*60}")
        print("📊 SESSION SUMMARY")
        print(f"{'='*60}")
        print(f"Duration: {int(time.time() - start_time)}s")
        print(f"Iterations: {iteration}")
        print(f"Max supernatural level: {max_supernatural:.1f}/10")

if __name__ == "__main__":
    import sys
    
    system = AstroSupernaturalSystem()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'monitor':
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        duration = int(sys.argv[3]) if len(sys.argv) > 3 else 120
        system.monitor_supernatural_activity(interval, duration)
    else:
        system.list_zones()
        print("\nRun: python3 integrate_astronomy.py monitor 10 120")
