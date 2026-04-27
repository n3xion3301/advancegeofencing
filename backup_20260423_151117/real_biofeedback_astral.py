#!/usr/bin/env python3
"""
Real Biofeedback Astral Projection
Uses actual device sensors to create immersive experience
"""
import subprocess
import json
import time
from datetime import datetime

class RealBiofeedbackAstral:
    def __init__(self):
        print("🧠 Real Biofeedback Astral System")
        print("   Using actual device sensors\n")
    
    def get_sensor_data(self):
        """Get real sensor data from device"""
        sensors = {}
        
        # Accelerometer (movement/vibration)
        try:
            result = subprocess.run(
                ['termux-sensor', '-s', 'accelerometer', '-n', '1'],
                capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                sensors['accelerometer'] = data['accelerometer']['values']
        except: pass
        
        # Light sensor (ambient energy)
        try:
            result = subprocess.run(
                ['termux-sensor', '-s', 'light', '-n', '1'],
                capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                sensors['light'] = data['light']['values'][0]
        except: pass
        
        # Magnetic field (electromagnetic field)
        try:
            result = subprocess.run(
                ['termux-sensor', '-s', 'magnetic_field', '-n', '1'],
                capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                sensors['magnetic'] = data['magnetic_field']['values']
        except: pass
        
        # Proximity (nearby objects/energy)
        try:
            result = subprocess.run(
                ['termux-sensor', '-s', 'proximity', '-n', '1'],
                capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                sensors['proximity'] = data['proximity']['values'][0]
        except: pass
        
        return sensors
    
    def calculate_consciousness_level(self, sensors):
        """Calculate consciousness level from real sensor data"""
        level = 1
        
        # Stillness = higher consciousness (low accelerometer)
        if 'accelerometer' in sensors:
            movement = sum(abs(x) for x in sensors['accelerometer'])
            if movement < 1.0:
                level += 1
                print(f"   ✅ Body stillness detected: {movement:.3f}")
        
        # Darkness = deeper meditation (low light)
        if 'light' in sensors:
            if sensors['light'] < 10:
                level += 1
                print(f"   ✅ Darkness detected: {sensors['light']:.1f} lux")
        
        # Magnetic field variations = energy sensitivity
        if 'magnetic' in sensors:
            mag_strength = sum(abs(x) for x in sensors['magnetic'])
            if mag_strength > 30:
                level += 1
                print(f"   ✅ Magnetic field: {mag_strength:.1f} μT")
        
        # Proximity = isolation
        if 'proximity' in sensors:
            if sensors['proximity'] > 5:
                level += 1
                print(f"   ✅ Isolation detected: {sensors['proximity']:.1f} cm")
        
        return min(level, 6)
    
    def guided_astral_session(self, duration=300):
        """Real-time guided astral projection using sensors"""
        print("\n🌟 REAL BIOFEEDBACK ASTRAL SESSION")
        print(f"   Duration: {duration}s ({duration//60} minutes)")
        print("\n📋 Instructions:")
        print("   1. Find a quiet, dark place")
        print("   2. Lie down or sit comfortably")
        print("   3. Place phone on your chest or nearby")
        print("   4. Close your eyes and breathe deeply")
        print("   5. Follow the guidance\n")
        
        input("Press Enter when ready...")
        
        start_time = time.time()
        max_level = 1
        
        print("\n🧘 Session started...\n")
        
        while time.time() - start_time < duration:
            elapsed = int(time.time() - start_time)
            
            # Get real sensor data
            sensors = self.get_sensor_data()
            
            # Calculate consciousness level
            level = self.calculate_consciousness_level(sensors)
            max_level = max(max_level, level)
            
            # Provide feedback
            print(f"\n[{elapsed}s] Consciousness Level: {level}/6")
            
            if level >= 4:
                print("   🌟 Deep state achieved!")
                print("   💭 Visualize your target location...")
            elif level >= 2:
                print("   ✨ Good progress, keep relaxing...")
            else:
                print("   💡 Relax more, reduce movement...")
            
            # Show sensor readings
            if sensors:
                print(f"   📊 Sensors: {len(sensors)} active")
            
            time.sleep(10)  # Check every 10 seconds
        
        print(f"\n✅ SESSION COMPLETE")
        print(f"   Max consciousness level: {max_level}/6")
        print(f"   Duration: {duration}s")

if __name__ == "__main__":
    astral = RealBiofeedbackAstral()
    
    # Quick sensor test
    print("🔬 Testing sensors...\n")
    sensors = astral.get_sensor_data()
    
    if sensors:
        print("✅ Available sensors:")
        for sensor, value in sensors.items():
            print(f"   {sensor}: {value}")
    else:
        print("⚠️  No sensors available")
        print("   Install: pkg install termux-api")
    
    print("\n" + "="*50)
    choice = input("\nStart guided session? (y/n): ")
    
    if choice.lower() == 'y':
        duration = input("Duration in seconds (default 300): ")
        duration = int(duration) if duration else 300
        astral.guided_astral_session(duration)
