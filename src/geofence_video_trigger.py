#!/usr/bin/env python3
"""
Integration: Quantum Astral Vision + Geofence System
Auto-triggers recording on geofence events
"""

from quantum_astral_vision import QuantumAstralVision
from quantum_geofence_integration import QuantumGeofenceSystem
import json

class GeofenceVideoTrigger:
    def __init__(self):
        self.vision = QuantumAstralVision()
        self.geofence = QuantumGeofenceSystem()
        print("🎬 Geofence Video Trigger System Ready")
    
    def on_zone_entry(self, location_data, zone_config):
        """Triggered when entering a geofence zone"""
        print(f"\n🚪 Zone Entry Detected: {zone_config['zone_id']}")
        
        # Quantum analysis
        analysis = self.geofence.full_quantum_analysis(location_data, zone_config)
        
        # Check if recording should trigger
        boundary_prob = analysis['quantum_analysis']['boundary']['probability_inside']
        
        if boundary_prob > 0.7:
            print("📹 High probability - triggering Astral Vision recording...")
            
            zone_data = {
                'zone_id': zone_config['zone_id'],
                'lat': location_data['lat'],
                'lon': location_data['lon'],
                'activity_level': boundary_prob
            }
            
            recording = self.vision.quantum_enhanced_recording(zone_data, duration=15)
            
            if recording:
                # Combine quantum analysis with recording metadata
                recording['quantum_analysis'] = analysis
                
                # Save combined report
                report_file = f"reports/astral_vision_report_{recording['timestamp']}.json"
                with open(report_file, 'w') as f:
                    json.dump(recording, f, indent=2)
                
                print(f"📊 Full report saved: {report_file}")
                return recording
        
        return None
    
    def on_zone_exit(self, location_data, zone_config):
        """Triggered when exiting a geofence zone"""
        print(f"\n🚶 Zone Exit Detected: {zone_config['zone_id']}")
        
        # Quick photo on exit
        photo = self.vision.capture_photo()
        
        return {
            'event': 'zone_exit',
            'zone_id': zone_config['zone_id'],
            'photo': photo,
            'timestamp': location_data.get('timestamp')
        }

# Example usage
if __name__ == "__main__":
    trigger = GeofenceVideoTrigger()
    
    # Simulate zone entry
    location = {
        'lat': 40.7128,
        'lon': -74.0060,
        'user_id': 'user_123',
        'signal_strength': 0.9
    }
    
    zone = {
        'zone_id': 'home_zone',
        'center_lat': 40.7127,
        'center_lon': -74.0059,
        'radius': 100,
        'security_level': 0.85,
        'active_zones': [True, True, False]
    }
    
    result = trigger.on_zone_entry(location, zone)
    
    if result:
        print("\n✨ Astral Vision Event Complete!")
        print(f"Video: {result.get('video')}")
        print(f"Photo: {result.get('photo')}")
