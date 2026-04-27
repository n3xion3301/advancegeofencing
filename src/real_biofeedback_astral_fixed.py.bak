#!/usr/bin/env python3
"""
Real Biofeedback Astral Projection - FIXED for actual sensor names
"""
import subprocess
import json
import time
from datetime import datetime
import math

class RealBiofeedbackAstral:
    def __init__(self):
        print("🧠 Real Biofeedback Astral System")
        print("   Using YOUR actual device sensors\n")
        self.detect_sensors()
    
    def detect_sensors(self):
        """Auto-detect available sensors"""
        try:
            result = subprocess.run(
                ['termux-sensor', '-a', '-n', '1'],
                capture_output=True, text=True, timeout=3
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                self.available_sensors = list(data.keys())
                print(f"✅ Detected {len(self.available_sensors)} sensors:")
                for sensor in self.available_sensors:
                    print(f"   - {sensor}")
                return True
        except Exception as e:
            print(f"❌ Sensor detection failed: {e}")
            self.available_sensors = []
            return False
    
    def get_all_sensors(self):
        """Get all sensor data at once"""
        try:
            result = subprocess.run(
                ['termux-sensor', '-a', '-n', '1'],
                capture_output=True, text=True, timeout=3
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
        except:
            pass
        return {}
    
    def calculate_consciousness_level(self, sensors):
        """Calculate consciousness level from REAL sensor data"""
        level = 1
        feedback = []
        
        # Find accelerometer (any variant)
        acc_sensor = None
        for name in sensors:
            if 'acc' in name.lower() and 'uncali' not in name.lower():
                acc_sensor = name
                break
        
        if acc_sensor:
            values = sensors[acc_sensor]['values']
            movement = math.sqrt(sum(x**2 for x in values[:3]))
            
            if movement < 10.5:  # Very still
                level += 2
                feedback.append(f"✅ Deep stillness: {movement:.2f} m/s²")
            elif movement < 11.0:  # Moderately still
                level += 1
                feedback.append(f"✨ Good stillness: {movement:.2f} m/s²")
            else:
                feedback.append(f"💡 Relax more: {movement:.2f} m/s²")
        
        # Find light sensor
        light_sensor = None
        for name in sensors:
            if 'als' in name.lower() or 'light' in name.lower():
                light_sensor = name
                break
        
        if light_sensor:
            light = sensors[light_sensor]['values'][0]
            
            if light < 10:  # Very dark
                level += 2
                feedback.append(f"✅ Deep darkness: {light:.1f} lux")
            elif light < 50:  # Dim
                level += 1
                feedback.append(f"✨ Good darkness: {light:.1f} lux")
            else:
                feedback.append(f"💡 Too bright: {light:.1f} lux")
        
        # Find magnetometer
        mag_sensor = None
        for name in sensors:
            if 'qmc' in name.lower() or ('mag' in name.lower() and 'uncali' not in name.lower()):
                mag_sensor = name
                break
        
        if mag_sensor:
            values = sensors[mag_sensor]['values']
            mag_strength = math.sqrt(sum(x**2 for x in values[:3]))
            
            if mag_strength > 30:
                level += 1
                feedback.append(f"✅ Magnetic field: {mag_strength:.1f} μT")
        
        # Find gyroscope (rotation = mental activity)
        gyro_sensor = None
        for name in sensors:
            if 'gyro' in name.lower() and 'uncali' not in name.lower():
                gyro_sensor = name
                break
        
        if gyro_sensor:
            values = sensors[gyro_sensor]['values']
            rotation = math.sqrt(sum(x**2 for x in values[:3]))
            
            if rotation < 0.1:  # Very still mind
                level += 1
                feedback.append(f"✅ Mental stillness: {rotation:.3f} rad/s")
        
        return min(level, 6), feedback
    
    def guided_astral_session(self, duration=300):
        """Real-time guided astral projection using YOUR sensors"""
        print("\n🌟 REAL BIOFEEDBACK ASTRAL SESSION")
        print(f"   Duration: {duration}s ({duration//60} minutes)")
        print("\n📋 Instructions:")
        print("   1. Find a quiet, dark place")
        print("   2. Lie down comfortably")
        print("   3. Place phone on your chest")
        print("   4. Close your eyes")
        print("   5. Breathe deeply and slowly")
        print("\n   The system will monitor your:")
        print("   - Body movement (accelerometer)")
        print("   - Light levels (ambient sensor)")
        print("   - Magnetic field (magnetometer)")
        print("   - Mental activity (gyroscope)")
        
        input("\nPress Enter when ready...\n")
        
        start_time = time.time()
        max_level = 1
        level_times = {i: 0 for i in range(1, 7)}
        
        print("🧘 Session started...\n")
        
        iteration = 0
        while time.time() - start_time < duration:
            iteration += 1
            elapsed = int(time.time() - start_time)
            
            # Get REAL sensor data
            sensors = self.get_all_sensors()
            
            if not sensors:
                print(f"[{elapsed}s] ⚠️  Sensor read failed, retrying...")
                time.sleep(5)
                continue
            
            # Calculate consciousness level from REAL data
            level, feedback = self.calculate_consciousness_level(sensors)
            max_level = max(max_level, level)
            level_times[level] += 10
            
            # Display status
            print(f"\n{'='*60}")
            print(f"[{elapsed}s] Consciousness Level: {level}/6")
            print(f"{'='*60}")
            
            # Show feedback
            for fb in feedback:
                print(f"   {fb}")
            
            # Guidance based on level
            if level >= 5:
                print("\n   🌟 DEEP ASTRAL STATE!")
                print("   💭 You are in the quantum realm")
                print("   👁️  Visualize your target location clearly")
            elif level >= 4:
                print("\n   ✨ Excellent progress!")
                print("   🧘 Maintain this state")
                print("   💭 Begin visualization")
            elif level >= 3:
                print("\n   ✅ Good meditation state")
                print("   🫁 Focus on breathing")
            elif level >= 2:
                print("\n   📈 Entering relaxation")
                print("   💡 Release tension")
            else:
                print("\n   💡 Relax more deeply")
                print("   🫁 Slow your breathing")
            
            # Show key sensor values
            print(f"\n   📊 Raw Sensor Data:")
            for name, data in list(sensors.items())[:5]:
                values = data['values']
                if len(values) == 1:
                    print(f"      {name}: {values[0]:.2f}")
                else:
                    print(f"      {name}: [{', '.join(f'{v:.2f}' for v in values[:3])}]")
            
            time.sleep(10)  # Check every 10 seconds
        
        # Session summary
        print(f"\n{'='*60}")
        print("✅ SESSION COMPLETE")
        print(f"{'='*60}")
        print(f"\n📊 Summary:")
        print(f"   Duration: {duration}s")
        print(f"   Max Level: {max_level}/6")
        print(f"   Iterations: {iteration}")
        print(f"\n⏱️  Time at each level:")
        for lvl in range(1, 7):
            if level_times[lvl] > 0:
                print(f"   Level {lvl}: {level_times[lvl]}s")
        
        if max_level >= 5:
            print(f"\n🌟 EXCELLENT! You achieved deep astral states!")
        elif max_level >= 3:
            print(f"\n✨ Good session! Practice more to go deeper.")
        else:
            print(f"\n💡 Keep practicing! Try a darker, quieter space.")

if __name__ == "__main__":
    astral = RealBiofeedbackAstral()
    
    if not astral.available_sensors:
        print("\n❌ No sensors detected!")
        exit(1)
    
    print("\n" + "="*60)
    choice = input("\nStart guided astral session? (y/n): ")
    
    if choice.lower() == 'y':
        duration = input("Duration in seconds (default 300 = 5min): ")
        duration = int(duration) if duration else 300
        astral.guided_astral_session(duration)
    else:
        print("\n✨ Session cancelled")
