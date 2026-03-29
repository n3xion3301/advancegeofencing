#!/usr/bin/env python3
"""
🌌 QUANTUM GEOFENCE INTEGRATION 🗺️
Connects quantum camera, geofencing, and entity detection
"""

import sys
import os
import time
import json
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.append('src')

# Import all subsystems
try:
    from quantum_camera_detector import QuantumCameraDetector
    from quantum_visualizer import QuantumVisualizer
    from camera_visualizer_bridge import CameraVisualizerBridge
    print("✅ Quantum camera modules loaded")
except ImportError as e:
    print(f"⚠️ Quantum camera: {e}")

try:
    from geofence_monitor import GeofenceMonitor
    from android_location import AndroidLocation
    print("✅ Geofencing modules loaded")
except ImportError as e:
    print(f"⚠️ Geofencing: {e}")

try:
    from entity_zone_monitor import EntityZoneMonitor
    from wifi_entity_detector import WiFiEntityDetector
    print("✅ Entity detection modules loaded")
except ImportError as e:
    print(f"⚠️ Entity detection: {e}")

try:
    from telegram_notifier import TelegramNotifier
    print("✅ Telegram notifier loaded")
except ImportError as e:
    print(f"⚠️ Telegram: {e}")


class QuantumGeofenceIntegration:
    """Integrated quantum geofencing system"""
    
    def __init__(self):
        print("\n🌌 Initializing Quantum Geofence Integration...")
        
        # Create directories
        self.setup_directories()
        
        # Initialize subsystems
        self.quantum_detector = None
        self.visualizer = None
        self.bridge = None
        self.geofence = None
        self.entity_monitor = None
        self.telegram = None
        
        # Integration state
        self.current_zone = "unknown"
        self.quantum_mode = "auto"  # auto, manual, off
        self.entity_tracking = True
        self.last_detection = None
        
        # Load config
        self.load_config()
        
    def setup_directories(self):
        """Create necessary directories"""
        dirs = [
            'quantum_integrated',
            'quantum_integrated/detections',
            'quantum_integrated/logs',
            'quantum_integrated/events'
        ]
        for d in dirs:
            Path(d).mkdir(parents=True, exist_ok=True)
    
    def load_config(self):
        """Load integration configuration"""
        config_file = 'config/integration_config.json'
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        else:
            # Default config
            self.config = {
                "quantum_on_zone_entry": True,
                "quantum_on_entity_detected": True,
                "auto_visualize_threshold": 0.7,
                "telegram_notifications": True,
                "zones": {
                    "home": {
                        "quantum_mode": "auto",
                        "entity_tracking": True
                    },
                    "outside": {
                        "quantum_mode": "manual",
                        "entity_tracking": False
                    }
                }
            }
            self.save_config()
    
    def save_config(self):
        """Save configuration"""
        os.makedirs('config', exist_ok=True)
        with open('config/integration_config.json', 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def initialize_quantum_camera(self):
        """Initialize quantum camera subsystem"""
        try:
            self.quantum_detector = QuantumCameraDetector()
            self.visualizer = QuantumVisualizer()
            self.bridge = CameraVisualizerBridge()
            print("✅ Quantum camera initialized")
            return True
        except Exception as e:
            print(f"❌ Quantum camera init failed: {e}")
            return False
    
    def initialize_geofencing(self):
        """Initialize geofencing subsystem"""
        try:
            self.geofence = GeofenceMonitor()
            print("✅ Geofencing initialized")
            return True
        except Exception as e:
            print(f"❌ Geofencing init failed: {e}")
            return False
    
    def initialize_entity_detection(self):
        """Initialize entity detection subsystem"""
        try:
            self.entity_monitor = EntityZoneMonitor()
            print("✅ Entity detection initialized")
            return True
        except Exception as e:
            print(f"❌ Entity detection init failed: {e}")
            return False
    
    def initialize_telegram(self):
        """Initialize Telegram notifications"""
        try:
            self.telegram = TelegramNotifier()
            print("✅ Telegram initialized")
            return True
        except Exception as e:
            print(f"❌ Telegram init failed: {e}")
            return False
    
    def on_zone_change(self, old_zone, new_zone):
        """Handle zone change event"""
        print(f"\n🗺️ Zone changed: {old_zone} → {new_zone}")
        
        self.current_zone = new_zone
        
        # Update settings based on zone
        if new_zone in self.config['zones']:
            zone_config = self.config['zones'][new_zone]
            self.quantum_mode = zone_config.get('quantum_mode', 'auto')
            self.entity_tracking = zone_config.get('entity_tracking', True)
        
        # Trigger quantum detection on zone entry?
        if self.config.get('quantum_on_zone_entry', False):
            if self.quantum_mode == 'auto':
                print("📷 Auto-triggering quantum detection...")
                self.trigger_quantum_detection(reason=f"zone_entry:{new_zone}")
        
        # Log event
        self.log_event('zone_change', {
            'old_zone': old_zone,
            'new_zone': new_zone,
            'timestamp': datetime.now().isoformat()
        })
        
        # Notify
        if self.telegram and self.config.get('telegram_notifications'):
            self.telegram.send_message(
                f"🗺️ Zone Change\n"
                f"From: {old_zone}\n"
                f"To: {new_zone}\n"
                f"Quantum Mode: {self.quantum_mode}"
            )
    
    def on_entity_detected(self, entity_data):
        """Handle entity detection event"""
        print(f"\n👁️ Entity detected: {entity_data.get('name', 'Unknown')}")
        
        # Trigger quantum detection?
        if self.config.get('quantum_on_entity_detected', False):
            if self.quantum_mode == 'auto':
                print("📷 Auto-triggering quantum detection...")
                self.trigger_quantum_detection(
                    reason=f"entity_detected:{entity_data.get('name')}"
                )
        
        # Log event
        self.log_event('entity_detected', entity_data)
        
        # Notify
        if self.telegram and self.config.get('telegram_notifications'):
            self.telegram.send_message(
                f"👁️ Entity Detected\n"
                f"Name: {entity_data.get('name')}\n"
                f"Zone: {self.current_zone}\n"
                f"Type: {entity_data.get('type', 'unknown')}"
            )
    
    def trigger_quantum_detection(self, reason="manual"):
        """Trigger quantum camera detection"""
        if not self.quantum_detector:
            print("❌ Quantum detector not initialized")
            return None
        
        print(f"\n⚛️ Triggering quantum detection (reason: {reason})")
        
        try:
            # Capture and analyze
            image_path = self.quantum_detector.capture_frame()
            if not image_path:
                print("❌ Capture failed")
                return None
            
            score, signatures = self.quantum_detector.analyze_frame(image_path)
            
            print(f"Quantum Score: {score:.3f}")
            print(f"Signatures: {len(signatures)}")
            
            # Create entity
            entity = self.bridge.create_entity_from_detection(
                score, signatures, image_path
            )
            
            # Visualize if threshold met
            if score >= self.config.get('auto_visualize_threshold', 0.7):
                print("\n🌌 Showing visualizations...")
                viz_list = self.bridge.get_visualization_list(signatures)
                for viz_name in viz_list[:5]:  # Show top 5
                    if hasattr(self.visualizer, viz_name):
                        getattr(self.visualizer, viz_name)(entity)
            
            # Save detection
            detection_data = {
                'timestamp': datetime.now().isoformat(),
                'reason': reason,
                'zone': self.current_zone,
                'quantum_score': score,
                'signatures': signatures,
                'image_path': image_path,
                'entity': entity
            }
            
            self.save_detection(detection_data)
            self.last_detection = detection_data
            
            # Notify
            if self.telegram and score >= 0.7:
                self.telegram.send_message(
                    f"⚛️ Quantum Detection!\n"
                    f"Score: {score:.3f}\n"
                    f"Zone: {self.current_zone}\n"
                    f"Signatures: {len(signatures)}\n"
                    f"Reason: {reason}"
                )
            
            return detection_data
            
        except Exception as e:
            print(f"❌ Detection error: {e}")
            return None
    
    def save_detection(self, detection_data):
        """Save detection data"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"quantum_integrated/detections/detection_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(detection_data, f, indent=2, default=str)
        
        print(f"💾 Saved: {filename}")
    
    def log_event(self, event_type, event_data):
        """Log integration event"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"quantum_integrated/events/event_{timestamp}.json"
        
        event = {
            'type': event_type,
            'timestamp': datetime.now().isoformat(),
            'data': event_data
        }
        
        with open(filename, 'w') as f:
            json.dump(event, f, indent=2, default=str)
    
    def run_integrated_monitoring(self):
        """Run integrated monitoring loop"""
        print("\n🚀 Starting integrated monitoring...")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                # Simulated monitoring loop
                # In real implementation, this would check geofence, entities, etc.
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring...")
                print(f"  Zone: {self.current_zone}")
                print(f"  Quantum Mode: {self.quantum_mode}")
                print(f"  Entity Tracking: {self.entity_tracking}")
                
                time.sleep(10)
                
        except KeyboardInterrupt:
            print("\n\n⏹️ Stopping integrated monitoring...")


def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🌌 QUANTUM GEOFENCE INTEGRATION 🗺️                     ║
║                                                           ║
║   Quantum Camera + Geofencing + Entity Detection         ║
║              All Systems Connected!                      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    integration = QuantumGeofenceIntegration()
    
    print("\nInitializing subsystems...")
    integration.initialize_quantum_camera()
    integration.initialize_geofencing()
    integration.initialize_entity_detection()
    integration.initialize_telegram()
    
    print("\n" + "="*60)
    print("INTEGRATION MENU")
    print("="*60)
    print("1. Run integrated monitoring")
    print("2. Trigger quantum detection (manual)")
    print("3. Simulate zone change")
    print("4. Simulate entity detection")
    print("5. View last detection")
    print("6. Configure integration")
    print("7. Exit")
    print("="*60)
    
    while True:
        choice = input("\nChoice (1-7): ").strip()
        
        if choice == '1':
            integration.run_integrated_monitoring()
        
        elif choice == '2':
            integration.trigger_quantum_detection(reason="manual_trigger")
        
        elif choice == '3':
            old_zone = integration.current_zone
            new_zone = input("Enter new zone: ").strip()
            integration.on_zone_change(old_zone, new_zone)
        
        elif choice == '4':
            entity_name = input("Enter entity name: ").strip()
            integration.on_entity_detected({
                'name': entity_name,
                'type': 'wifi',
                'timestamp': datetime.now().isoformat()
            })
        
        elif choice == '5':
            if integration.last_detection:
                print("\n📊 Last Detection:")
                print(json.dumps(integration.last_detection, indent=2, default=str))
            else:
                print("No detections yet")
        
        elif choice == '6':
            print("\n⚙️ Configuration:")
            print(json.dumps(integration.config, indent=2))
            print("\nEdit config/integration_config.json to modify")
        
        elif choice == '7':
            print("\n✨ Goodbye! ✨")
            break


if __name__ == "__main__":
    main()
