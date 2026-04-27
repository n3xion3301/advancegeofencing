#!/usr/bin/env python3
"""
Astronomical Supernatural Amplifier
Detects celestial events that amplify supernatural activity
"""
from datetime import datetime, timezone
import math

try:
    from astral import LocationInfo
    from astral.sun import sun
    from astral.moon import phase
    ASTRAL_AVAILABLE = True
except:
    ASTRAL_AVAILABLE = False
    print("⚠️  astral not installed yet")

class AstronomicalAmplifier:
    def __init__(self, lat=40.7128, lon=-74.0060):
        self.lat = lat
        self.lon = lon
        print(f"🌌 Astronomical Amplifier Initialized")
        print(f"   Location: {lat:.4f}, {lon:.4f}")
    
    def get_moon_phase(self):
        """Get current moon phase (0-28 days)"""
        if not ASTRAL_AVAILABLE:
            # Fallback calculation
            now = datetime.now(timezone.utc)
            days_since_new = (now.toordinal() - 730120) % 29.53
            return days_since_new
        
        return phase(datetime.now(timezone.utc))
    
    def calculate_moon_power(self):
        """Calculate supernatural power from moon phase"""
        moon_phase = self.get_moon_phase()
        
        # Full moon = maximum power
        # New moon = minimum power
        if moon_phase < 7:  # New moon
            power = 0.3 + (moon_phase / 7) * 0.4
            phase_name = "Waxing Crescent"
        elif moon_phase < 14:  # First quarter to full
            power = 0.7 + ((moon_phase - 7) / 7) * 0.3
            phase_name = "Waxing Gibbous"
        elif moon_phase < 15:  # Full moon
            power = 1.0
            phase_name = "🌕 FULL MOON"
        elif moon_phase < 22:  # Waning
            power = 0.7 + ((22 - moon_phase) / 7) * 0.3
            phase_name = "Waning Gibbous"
        else:  # Dark moon
            power = 0.3 + ((29.53 - moon_phase) / 7) * 0.4
            phase_name = "Waning Crescent"
        
        return {
            'phase': moon_phase,
            'phase_name': phase_name,
            'power_multiplier': power,
            'is_full_moon': 13 <= moon_phase <= 16
        }
    
    def get_solar_position(self):
        """Get sun position (dawn/dusk amplification)"""
        now = datetime.now()
        hour = now.hour + now.minute / 60
        
        # Dawn (5-7am) and Dusk (5-7pm) = high supernatural
        if 5 <= hour <= 7:
            return {
                'period': '🌅 DAWN',
                'power_multiplier': 1.3,
                'description': 'Veil between worlds is thin'
            }
        elif 17 <= hour <= 19:
            return {
                'period': '🌆 DUSK', 
                'power_multiplier': 1.3,
                'description': 'Twilight hour - supernatural peak'
            }
        elif 0 <= hour <= 4:
            return {
                'period': '🌙 WITCHING HOUR',
                'power_multiplier': 1.5,
                'description': 'Maximum supernatural activity'
            }
        elif 12 <= hour <= 14:
            return {
                'period': '☀️ NOON',
                'power_multiplier': 0.7,
                'description': 'Supernatural activity diminished'
            }
        else:
            return {
                'period': 'Day/Night',
                'power_multiplier': 1.0,
                'description': 'Normal supernatural levels'
            }
    
    def calculate_total_amplification(self):
        """Calculate total supernatural amplification"""
        moon = self.calculate_moon_power()
        solar = self.get_solar_position()
        
        # Combine moon and solar effects
        total_multiplier = moon['power_multiplier'] * solar['power_multiplier']
        
        # Special events
        special_bonus = 0
        events = []
        
        if moon['is_full_moon']:
            special_bonus += 0.5
            events.append("🌕 Full Moon Bonus")
        
        if solar['period'] == '🌙 WITCHING HOUR':
            special_bonus += 0.3
            events.append("🌙 Witching Hour Bonus")
        
        if moon['is_full_moon'] and solar['period'] == '🌙 WITCHING HOUR':
            special_bonus += 0.5
            events.append("⚡ RARE: Full Moon + Witching Hour!")
        
        total_multiplier += special_bonus
        
        return {
            'moon': moon,
            'solar': solar,
            'total_multiplier': total_multiplier,
            'special_events': events,
            'supernatural_level': min(total_multiplier * 10, 10)
        }
    
    def display_status(self):
        """Display current astronomical supernatural status"""
        amp = self.calculate_total_amplification()
        
        print("\n🌌 ASTRONOMICAL SUPERNATURAL STATUS")
        print("="*60)
        
        print(f"\n🌙 Moon:")
        print(f"   Phase: {amp['moon']['phase_name']}")
        print(f"   Day: {amp['moon']['phase']:.1f}/29.5")
        print(f"   Power: {amp['moon']['power_multiplier']:.1%}")
        
        print(f"\n☀️ Solar:")
        print(f"   Period: {amp['solar']['period']}")
        print(f"   Power: {amp['solar']['power_multiplier']:.1%}")
        print(f"   {amp['solar']['description']}")
        
        if amp['special_events']:
            print(f"\n⚡ SPECIAL EVENTS:")
            for event in amp['special_events']:
                print(f"   {event}")
        
        print(f"\n🔮 TOTAL AMPLIFICATION: {amp['total_multiplier']:.2f}x")
        print(f"⚡ Supernatural Level: {amp['supernatural_level']:.1f}/10")
        
        if amp['total_multiplier'] >= 2.0:
            print(f"\n🌟 EXTREME AMPLIFICATION!")
            print(f"   Perfect time for astral projection")
        elif amp['total_multiplier'] >= 1.5:
            print(f"\n✨ HIGH AMPLIFICATION")
            print(f"   Excellent supernatural conditions")
        elif amp['total_multiplier'] >= 1.0:
            print(f"\n💫 NORMAL CONDITIONS")
        else:
            print(f"\n💡 LOW AMPLIFICATION")
            print(f"   Wait for better celestial alignment")
        
        return amp

if __name__ == "__main__":
    amp = AstronomicalAmplifier()
    amp.display_status()
