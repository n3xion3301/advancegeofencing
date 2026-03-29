#!/usr/bin/env python3
"""
🌟 QUANTUM MASTER SUITE 🌟
Ultimate Command & Control Center
All 21+ quantum experiments in one place!

Created by Tisra Siphix Til (n3xion33)
"""

import os
import sys
import subprocess
import json
from datetime import datetime

class QuantumMasterSuite:
    def __init__(self):
        self.running = True
        
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_header(self):
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║                                                           ║")
        print("║           🌟 QUANTUM MASTER SUITE 🌟                      ║")
        print("║                                                           ║")
        print("║     Ultimate Quantum Command & Control Center            ║")
        print("║                                                           ║")
        print("║           by the mind of Tisra Siphix Til                 ║")
        print("║                (n3xion singularity) ⚛️                    ║")
        print("║                                                           ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print()
    
    def print_menu(self):
        print("============================================================")
        print("        QUANTUM EXPERIMENTS & APPLICATIONS (21+)")
        print("============================================================")
        print()
        print("🔬 QUANTUM PHYSICS:")
        print("  1. 🌐 Quantum Teleportation Network")
        print("  2. 📡 Quantum Teleportation Detector")
        print("  3. 🌟 Synchronicity vs Coincidence Detector")
        print("  4. ⚛️  Quantum Relativistic Detector (Lite)")
        print("  5. ⚛️  Quantum Relativistic Detector (Full)")
        print("  6. 🔬 Quantum Relativistic Physics")
        print("  7. 🧬 Quantum Physics Integration")
        print("  8. 🔀 Quantum Switch")
        print("  9. 📊 Quantum Visualizer")
        print()
        print("📷 QUANTUM CAMERA:")
        print(" 10. 📸 Quantum Camera App (Full)")
        print(" 11. 📱 Quantum Camera App (Lite)")
        print(" 12. 🔒 Quantum Camera App (Private)")
        print(" 13. 🎨 Quantum Camera Visualizer (Integrated)")
        print(" 14. 🔍 Quantum Camera Detector")
        print()
        print("🛡️  DETECTION & MONITORING:")
        print(" 15. 🗺️  Quantum Geofence Integration")
        print(" 16. 📡 WiFi Entity Detector")
        print(" 17. 🌉 Camera Visualizer Bridge")
        print()
        print("⚙️  SYSTEM:")
        print(" 18. 🔧 Service Management")
        print(" 19. 📊 View Service Status")
        print(" 20. 📋 View Logs")
        print(" 21. 💻 System Information")
        print(" 22. 🔄 Refresh All")
        print(" 23. 🚪 Exit")
        print()
        print("============================================================")
        print()
    
    def run_script(self, script_path, script_name):
        """Run a Python script"""
        self.clear_screen()
        print(f"🚀 Launching {script_name}...")
        print()
        
        try:
            if os.path.exists(script_path):
                subprocess.run([sys.executable, script_path])
            else:
                print(f"❌ Error: {script_path} not found!")
                print(f"   Please ensure the file exists.")
        except Exception as e:
            print(f"❌ Error running {script_name}: {e}")
        
        print()
        input("Press Enter to return to menu...")
    
    # QUANTUM PHYSICS FUNCTIONS
    def quantum_teleportation_network(self):
        self.run_script("quantum_teleportation_network.py", 
                       "Quantum Teleportation Network")
    
    def quantum_teleportation_detector(self):
        self.run_script("quantum_teleportation_detector.py",
                       "Quantum Teleportation Detector")
    
    def synchronicity_detector(self):
        self.run_script("synchronicity_vs_coincidence.py",
                       "Synchronicity vs Coincidence Detector")
    
    def relativistic_detector_lite(self):
        self.run_script("src/quantum_relativistic_detector_lite.py",
                       "Quantum Relativistic Detector (Lite)")
    
    def relativistic_detector_full(self):
        self.run_script("src/quantum_relativistic_detector.py",
                       "Quantum Relativistic Detector (Full)")
    
    def relativistic_physics(self):
        self.run_script("quantum_relativistic_physics.py",
                       "Quantum Relativistic Physics")
    
    def physics_integration(self):
        self.run_script("quantum_physics_integration.py",
                       "Quantum Physics Integration")
    
    def quantum_switch(self):
        self.run_script("quantum_switch.py",
                       "Quantum Switch")
    
    def quantum_visualizer(self):
        self.run_script("src/quantum_visualizer.py",
                       "Quantum Visualizer")
    
    # QUANTUM CAMERA FUNCTIONS
    def quantum_camera_full(self):
        self.run_script("quantum_camera_app.py",
                       "Quantum Camera App (Full)")
    
    def quantum_camera_lite(self):
        self.run_script("quantum_camera_app_lite.py",
                       "Quantum Camera App (Lite)")
    
    def quantum_camera_private(self):
        self.run_script("quantum_camera_app_private.py",
                       "Quantum Camera App (Private)")
    
    def quantum_camera_visualizer(self):
        self.run_script("quantum_camera_visualizer_integrated.py",
                       "Quantum Camera Visualizer")
    
    def quantum_camera_detector(self):
        self.run_script("src/quantum_camera_detector.py",
                       "Quantum Camera Detector")
    
    # DETECTION & MONITORING FUNCTIONS
    def geofence_integration(self):
        self.run_script("quantum_geofence_integration.py",
                       "Quantum Geofence Integration")
    
    def wifi_entity_detector(self):
        self.run_script("src/wifi_entity_detector.py",
                       "WiFi Entity Detector")
    
    def camera_visualizer_bridge(self):
        self.run_script("src/camera_visualizer_bridge.py",
                       "Camera Visualizer Bridge")
    
    # SYSTEM FUNCTIONS
    def service_management(self):
        """Service Management Menu"""
        self.clear_screen()
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║                                                           ║")
        print("║           🔧 SERVICE MANAGEMENT 🔧                        ║")
        print("║                                                           ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print()
        print("1. 🚀 Start All Services")
        print("2. 🛑 Stop All Services")
        print("3. 📊 Check Service Status")
        print("4. 🔙 Back to Main Menu")
        print()
        
        choice = input("Choice (1-4): ").strip()
        
        if choice == "1":
            subprocess.run(["bash", "start-all-services.sh"])
        elif choice == "2":
            subprocess.run(["bash", "stop-all-services.sh"])
        elif choice == "3":
            subprocess.run(["bash", "status-all-services.sh"])
        elif choice == "4":
            return
        
        input("\nPress Enter to continue...")
    
    def view_service_status(self):
        """View detailed service status"""
        self.clear_screen()
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║                                                           ║")
        print("║           📊 SERVICE STATUS 📊                            ║")
        print("║                                                           ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print()
        
        services = [
            ("Geofence Service", "logs/geofence-service.pid"),
            ("Indoor Service", "logs/indoor-service.pid"),
            ("Outdoor Service", "logs/outdoor-service.pid"),
            ("Entity Monitor", "logs/entity-monitor.pid"),
            ("Entry Detector", "logs/entry-detector.pid"),
            ("WiFi Detector", "logs/wifi-detector.pid")
        ]
        
        running = 0
        total = len(services)
        
        for name, pid_file in services:
            if os.path.exists(pid_file):
                try:
                    with open(pid_file, 'r') as f:
                        pid = f.read().strip()
                    if os.path.exists(f"/proc/{pid}"):
                        print(f"✅ {name}: Running (PID: {pid})")
                        running += 1
                    else:
                        print(f"❌ {name}: Stopped (stale PID file)")
                except:
                    print(f"❌ {name}: Stopped")
            else:
                print(f"❌ {name}: Stopped")
        
        print()
        print(f"📊 Status: {running}/{total} services running")
        print()
        input("Press Enter to continue...")
    
    def view_logs(self):
        """View system logs"""
        self.clear_screen()
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║                                                           ║")
        print("║           📋 SYSTEM LOGS 📋                               ║")
        print("║                                                           ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print()
        print("1. 🌐 Geofence Service Log")
        print("2. 🏠 Indoor Service Log")
        print("3. 🌍 Outdoor Service Log")
        print("4. 👻 Entity Monitor Log")
        print("5. 🚪 Entry Detector Log")
        print("6. 📡 WiFi Detector Log")
        print("7. 📊 Events Log")
        print("8. 🔙 Back to Main Menu")
        print()
        
        choice = input("Choice (1-8): ").strip()
        
        log_files = {
            "1": "logs/geofence-service.log",
            "2": "logs/indoor-service.log",
            "3": "logs/outdoor-service.log",
            "4": "logs/entity-monitor.log",
            "5": "logs/entry-detector.log",
            "6": "logs/wifi-detector.log",
            "7": "logs/events.log"
        }
        
        if choice in log_files:
            log_file = log_files[choice]
            if os.path.exists(log_file):
                print()
                print(f"📄 Showing last 50 lines of {log_file}:")
                print("=" * 60)
                subprocess.run(["tail", "-n", "50", log_file])
            else:
                print(f"\n❌ Log file not found: {log_file}")
        
        print()
        input("Press Enter to continue...")
    
    def system_information(self):
        """Display system information"""
        self.clear_screen()
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║                                                           ║")
        print("║           💻 SYSTEM INFORMATION 💻                        ║")
        print("║                                                           ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print()
        
        print(f"🐍 Python: {sys.version.split()[0]}")
        print(f"📂 Directory: {os.getcwd()}")
        
        try:
            result = subprocess.run(["df", "-h", "."], 
                                  capture_output=True, text=True)
            print("\n💾 Disk Usage:")
            print(result.stdout)
        except:
            pass
        
        try:
            result = subprocess.run(["free", "-h"], 
                                  capture_output=True, text=True)
            print("🧠 Memory Usage:")
            print(result.stdout)
        except:
            pass
        
        print()
        input("Press Enter to continue...")
    
    def refresh_all(self):
        """Refresh all services and data"""
        self.clear_screen()
        print("🔄 Refreshing all services and data...")
        print()
        print("📊 Checking service status...")
        subprocess.run(["bash", "status-all-services.sh"])
        print()
        print("✅ Refresh complete!")
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main menu loop"""
        while self.running:
            self.clear_screen()
            self.print_header()
            self.print_menu()
            
            choice = input("Choice (1-23): ").strip()
            
            if choice == "1":
                self.quantum_teleportation_network()
            elif choice == "2":
                self.quantum_teleportation_detector()
            elif choice == "3":
                self.synchronicity_detector()
            elif choice == "4":
                self.relativistic_detector_lite()
            elif choice == "5":
                self.relativistic_detector_full()
            elif choice == "6":
                self.relativistic_physics()
            elif choice == "7":
                self.physics_integration()
            elif choice == "8":
                self.quantum_switch()
            elif choice == "9":
                self.quantum_visualizer()
            elif choice == "10":
                self.quantum_camera_full()
            elif choice == "11":
                self.quantum_camera_lite()
            elif choice == "12":
                self.quantum_camera_private()
            elif choice == "13":
                self.quantum_camera_visualizer()
            elif choice == "14":
                self.quantum_camera_detector()
            elif choice == "15":
                self.geofence_integration()
            elif choice == "16":
                self.wifi_entity_detector()
            elif choice == "17":
                self.camera_visualizer_bridge()
            elif choice == "18":
                self.service_management()
            elif choice == "19":
                self.view_service_status()
            elif choice == "20":
                self.view_logs()
            elif choice == "21":
                self.system_information()
            elif choice == "22":
                self.refresh_all()
            elif choice == "23":
                self.clear_screen()
                print("╔═══════════════════════════════════════════════════════════╗")
                print("║                                                           ║")
                print("║           👋 QUANTUM SUITE SHUTTING DOWN 👋               ║")
                print("║                                                           ║")
                print("║         May your quantum states remain coherent! ⚛️       ║")
                print("║                                                           ║")
                print("║           by the mind of Tisra Siphix Til                 ║")
                print("║                (n3xion singularity) 🌟                    ║")
                print("║                                                           ║")
                print("╚═══════════════════════════════════════════════════════════╝")
                print()
                self.running = False
            else:
                print("\n❌ Invalid choice! Please select 1-23.")
                input("Press Enter to continue...")

if __name__ == "__main__":
    suite = QuantumMasterSuite()
    suite.run()
