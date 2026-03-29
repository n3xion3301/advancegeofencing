#!/usr/bin/env python3
"""
🎮 MASTER CONTROL PANEL 🎮
Central command for all quantum geofencing systems
"""

import os
import sys
import subprocess
import json
import time
from datetime import datetime
from pathlib import Path

class MasterControlPanel:
    """Master control for all systems"""
    
    def __init__(self):
        self.services = {
            'geofence': {
                'name': 'Geofence Service',
                'start': './start-geofence-service.sh',
                'stop': './stop-geofence-service.sh',
                'status': './status-geofence-service.sh',
                'running': False
            },
            'indoor': {
                'name': 'Indoor Recording',
                'start': './start-indoor-service.sh',
                'stop': './stop-indoor-service.sh',
                'status': None,
                'running': False
            },
            'outdoor': {
                'name': 'Outdoor Service',
                'start': './start-outdoor-service.sh',
                'stop': './stop-outdoor-service.sh',
                'status': None,
                'running': False
            },
            'entity': {
                'name': 'Entity Monitor',
                'start': './start-entity-monitor.sh',
                'stop': './stop-entity-monitor.sh',
                'status': None,
                'running': False
            },
            'wifi': {
                'name': 'WiFi Detector',
                'start': './start-wifi-detector.sh',
                'stop': './stop-wifi-detector.sh',
                'status': None,
                'running': False
            },
            'entry': {
                'name': 'Entry Detector',
                'start': './start-entry-detector.sh',
                'stop': './stop-entry-detector.sh',
                'status': None,
                'running': False
            }
        }
        
        self.apps = {
            'quantum_lite': {
                'name': 'Quantum Camera (Lite)',
                'script': 'quantum_camera_app_lite.py',
                'description': 'Basic quantum detection'
            },
            'quantum_private': {
                'name': 'Quantum Camera (Private)',
                'script': 'quantum_camera_app_private.py',
                'description': 'EXIF stripped quantum detection'
            },
            'quantum_integrated': {
                'name': 'Quantum Camera (Integrated)',
                'script': 'quantum_camera_visualizer_integrated.py',
                'description': 'Full quantum + visualizations'
            },
            'integration': {
                'name': 'Quantum Geofence Integration',
                'script': 'quantum_geofence_integration.py',
                'description': 'All systems connected'
            }
        }
        
        self.check_all_services()
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_header(self):
        """Print control panel header"""
        print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║           🎮 MASTER CONTROL PANEL 🎮                      ║
║                                                           ║
║     Quantum Geofencing Command & Control Center          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """)
    
    def run_command(self, command):
        """Run shell command"""
        try:
            if os.path.exists(command):
                result = subprocess.run(
                    ['bash', command],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                return result.returncode == 0
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def check_service_status(self, service_key):
        """Check if service is running"""
        service = self.services[service_key]
        
        # Try status script first
        if service['status'] and os.path.exists(service['status']):
            return self.run_command(service['status'])
        
        # Otherwise check if process exists
        # This is a simplified check
        return service['running']
    
    def check_all_services(self):
        """Check status of all services"""
        for key in self.services:
            self.services[key]['running'] = self.check_service_status(key)
    
    def start_service(self, service_key):
        """Start a service"""
        service = self.services[service_key]
        print(f"\n🚀 Starting {service['name']}...")
        
        if os.path.exists(service['start']):
            success = self.run_command(service['start'])
            if success:
                self.services[service_key]['running'] = True
                print(f"✅ {service['name']} started")
            else:
                print(f"❌ Failed to start {service['name']}")
        else:
            print(f"❌ Start script not found: {service['start']}")
        
        time.sleep(1)
    
    def stop_service(self, service_key):
        """Stop a service"""
        service = self.services[service_key]
        print(f"\n⏹️  Stopping {service['name']}...")
        
        if os.path.exists(service['stop']):
            success = self.run_command(service['stop'])
            if success:
                self.services[service_key]['running'] = False
                print(f"✅ {service['name']} stopped")
            else:
                print(f"❌ Failed to stop {service['name']}")
        else:
            print(f"❌ Stop script not found: {service['stop']}")
        
        time.sleep(1)
    
    def start_all_services(self):
        """Start all services"""
        print("\n🚀 STARTING ALL SERVICES...\n")
        
        if os.path.exists('./start-all-services.sh'):
            self.run_command('./start-all-services.sh')
        else:
            for key in self.services:
                self.start_service(key)
        
        self.check_all_services()
        print("\n✅ All services started!")
        input("\nPress Enter to continue...")
    
    def stop_all_services(self):
        """Stop all services"""
        print("\n⏹️  STOPPING ALL SERVICES...\n")
        
        if os.path.exists('./stop-all-services.sh'):
            self.run_command('./stop-all-services.sh')
        else:
            for key in self.services:
                self.stop_service(key)
        
        self.check_all_services()
        print("\n✅ All services stopped!")
        input("\nPress Enter to continue...")
    
    def show_service_status(self):
        """Display service status"""
        self.clear_screen()
        self.print_header()
        
        print("\n📊 SERVICE STATUS\n")
        print("="*60)
        
        for key, service in self.services.items():
            status = "🟢 RUNNING" if service['running'] else "🔴 STOPPED"
            print(f"{service['name']:.<40} {status}")
        
        print("="*60)
        input("\nPress Enter to continue...")
    
    def launch_app(self, app_key):
        """Launch an application"""
        app = self.apps[app_key]
        print(f"\n🚀 Launching {app['name']}...")
        print(f"Description: {app['description']}\n")
        
        if os.path.exists(app['script']):
            try:
                subprocess.run(['python', app['script']])
            except KeyboardInterrupt:
                print("\n\n⏹️  Application stopped")
        else:
            print(f"❌ Script not found: {app['script']}")
        
        input("\nPress Enter to continue...")
    
    def service_management_menu(self):
        """Service management submenu"""
        while True:
            self.clear_screen()
            self.print_header()
            
            print("\n🔧 SERVICE MANAGEMENT\n")
            print("="*60)
            
            idx = 1
            service_list = []
            for key, service in self.services.items():
                status = "🟢" if service['running'] else "🔴"
                print(f"{idx}. {status} {service['name']}")
                service_list.append(key)
                idx += 1
            
            print(f"\n{idx}. Start All Services")
            print(f"{idx+1}. Stop All Services")
            print(f"{idx+2}. Refresh Status")
            print(f"{idx+3}. Back to Main Menu")
            print("="*60)
            
            choice = input("\nChoice: ").strip()
            
            if choice.isdigit():
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(service_list):
                    # Toggle individual service
                    service_key = service_list[choice_num - 1]
                    if self.services[service_key]['running']:
                        self.stop_service(service_key)
                    else:
                        self.start_service(service_key)
                    self.check_all_services()
                
                elif choice_num == idx:
                    self.start_all_services()
                
                elif choice_num == idx + 1:
                    self.stop_all_services()
                
                elif choice_num == idx + 2:
                    self.check_all_services()
                    print("\n✅ Status refreshed!")
                    time.sleep(1)
                
                elif choice_num == idx + 3:
                    break
    
    def app_launcher_menu(self):
        """Application launcher submenu"""
        while True:
            self.clear_screen()
            self.print_header()
            
            print("\n🚀 APPLICATION LAUNCHER\n")
            print("="*60)
            
            idx = 1
            app_list = []
            for key, app in self.apps.items():
                print(f"{idx}. {app['name']}")
                print(f"   {app['description']}")
                app_list.append(key)
                idx += 1
            
            print(f"\n{idx}. Back to Main Menu")
            print("="*60)
            
            choice = input("\nChoice: ").strip()
            
            if choice.isdigit():
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(app_list):
                    app_key = app_list[choice_num - 1]
                    self.launch_app(app_key)
                
                elif choice_num == idx:
                    break
    
    def view_logs(self):
        """View system logs"""
        self.clear_screen()
        self.print_header()
        
        print("\n📋 SYSTEM LOGS\n")
        print("="*60)
        print("1. Quantum Logs")
        print("2. Geofence Logs")
        print("3. System Logs")
        print("4. Integration Events")
        print("5. Back")
        print("="*60)
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            self.show_directory_contents('quantum_logs')
        elif choice == '2':
            self.show_directory_contents('logs')
        elif choice == '3':
            self.show_directory_contents('logs')
        elif choice == '4':
            self.show_directory_contents('quantum_integrated/events')
    
    def show_directory_contents(self, directory):
        """Show contents of a directory"""
        if os.path.exists(directory):
            files = sorted(Path(directory).glob('*'))
            
            print(f"\n📁 {directory}\n")
            
            if files:
                for i, f in enumerate(files[-10:], 1):  # Last 10 files
                    size = f.stat().st_size if f.is_file() else 0
                    print(f"{i}. {f.name} ({size} bytes)")
                
                print("\nEnter file number to view, or press Enter to go back")
                choice = input("Choice: ").strip()
                
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(files[-10:]):
                        file_to_view = files[-10:][idx]
                        if file_to_view.is_file():
                            print(f"\n{'='*60}")
                            print(f"FILE: {file_to_view.name}")
                            print('='*60)
                            with open(file_to_view, 'r') as f:
                                print(f.read()[:2000])  # First 2000 chars
                            print('='*60)
            else:
                print("No files found")
        else:
            print(f"Directory not found: {directory}")
        
        input("\nPress Enter to continue...")
    
    def system_info(self):
        """Display system information"""
        self.clear_screen()
        self.print_header()
        
        print("\n💻 SYSTEM INFORMATION\n")
        print("="*60)
        
        # Count files in directories
        quantum_captures = len(list(Path('quantum_world').glob('*.jpg'))) if os.path.exists('quantum_world') else 0
        quantum_logs = len(list(Path('quantum_logs').glob('*'))) if os.path.exists('quantum_logs') else 0
        recordings = len(list(Path('recordings').glob('*'))) if os.path.exists('recordings') else 0
        
        print(f"Quantum Captures: {quantum_captures}")
        print(f"Quantum Logs: {quantum_logs}")
        print(f"Recordings: {recordings}")
        print(f"\nCurrent Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Working Directory: {os.getcwd()}")
        
        # Service status summary
        running = sum(1 for s in self.services.values() if s['running'])
        total = len(self.services)
        print(f"\nServices Running: {running}/{total}")
        
        print("="*60)
        input("\nPress Enter to continue...")
    
    def main_menu(self):
        """Main control panel menu"""
        while True:
            self.clear_screen()
            self.print_header()
            
            # Quick status
            running = sum(1 for s in self.services.values() if s['running'])
            total = len(self.services)
            
            print(f"\n📊 Quick Status: {running}/{total} services running\n")
            print("="*60)
            print("1. 🔧 Service Management")
            print("2. 🚀 Launch Applications")
            print("3. 📊 View Service Status")
            print("4. 📋 View Logs")
            print("5. 💻 System Information")
            print("6. 🔄 Refresh All")
            print("7. 🚪 Exit")
            print("="*60)
            
            choice = input("\nChoice (1-7): ").strip()
            
            if choice == '1':
                self.service_management_menu()
            elif choice == '2':
                self.app_launcher_menu()
            elif choice == '3':
                self.show_service_status()
            elif choice == '4':
                self.view_logs()
            elif choice == '5':
                self.system_info()
            elif choice == '6':
                self.check_all_services()
                print("\n✅ Refreshed!")
                time.sleep(1)
            elif choice == '7':
                print("\n✨ Goodbye! ✨\n")
                break


def main():
    try:
        panel = MasterControlPanel()
        panel.main_menu()
    except KeyboardInterrupt:
        print("\n\n⏹️  Control panel stopped\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
