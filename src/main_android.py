import time
import threading
import os
from pathlib import Path
from dotenv import load_dotenv
from geofence_monitor import GeofenceMonitor
from termux_camera_controller import TermuxCameraController
from telegram_notifier import TelegramNotifier
from route_learner import RouteLearner
from android_location import AndroidLocationProvider
from network_detector import NetworkDetector
from home_video_recorder import HomeVideoRecorder
from route_tracker import RouteTracker

load_dotenv()

class DualModeGeofencingSystem:
    def __init__(self):
        self.geofence = GeofenceMonitor()
        self.camera = TermuxCameraController()
        self.telegram = TelegramNotifier()
        self.location_provider = AndroidLocationProvider()
        self.network = NetworkDetector()
        self.video_recorder = HomeVideoRecorder()
        self.route_tracker = RouteTracker(max_points=1000)  # Track last 1000 points
        self.route_learner = RouteLearner()
        self.previous_location = None
        self.breach_count = 0
        self.away_mode = False
        self.away_threshold_meters = 200
        self.last_movement_time = time.time()
        self.stationary_threshold_seconds = 120  # 2 minutes
        self.last_learned_time = 0
        Path('logs').mkdir(exist_ok=True)
        Path('routes').mkdir(exist_ok=True)
        
    def log_event(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}\n"
        with open('logs/events.log', 'a') as f:
            f.write(log_message)
        print(log_message.strip())
    
    def handle_location_update(self, location_data):
        # Track route
        self.route_tracker.add_point(location_data)
        
        current_location = (location_data['latitude'], location_data['longitude'])
        accuracy = location_data.get('accuracy', 0)
        speed = location_data.get('speed', 0)
        
        distance = self.geofence.get_distance_from_center(current_location)
        is_inside = self.geofence.is_inside_geofence(current_location)
        
        if accuracy and accuracy > 100:
            self.log_event(f"⚠️  Low accuracy: {accuracy:.1f}m - skipping")
            return
        
        was_away = self.away_mode
        self.away_mode = distance > self.away_threshold_meters
        
        status = "🟢 HOME" if is_inside else "🔴 AWAY"
        mode_indicator = "🏠 AT HOME" if not self.away_mode else "✈️ AWAY MODE"
        
        # Get route stats
        stats = self.route_tracker.get_stats()
        route_info = ""
        if stats:
            route_info = f" | 📏 Walked: {stats['distance_meters']:.0f}m | ⏱️ {stats['duration_seconds']//60}min"
        
        self.log_event(
            f"📍 {status} | {mode_indicator} | Distance: {distance:.1f}m | "
            f"Lat: {current_location[0]:.6f}, Lon: {current_location[1]:.6f} | "
            f"Accuracy: ±{accuracy:.1f}m | Speed: {speed:.1f}m/s{route_info}"

        # Route Learning - Detect when stopped moving
        if speed < 0.5:  # Nearly stationary
            time_stationary = time.time() - self.last_movement_time
            if time_stationary > self.stationary_threshold_seconds:
                # Been stationary for 2+ minutes - trigger learning
                time_since_last_learn = time.time() - self.last_learned_time
                if time_since_last_learn > 300:  # Only learn every 5 min
                    stats = self.route_tracker.get_stats()
                    if stats and stats["distance_meters"] > 50:  # Meaningful route
                        self.log_event("🧠 Route learning triggered - analyzing pattern...")
                        route_data = self.route_tracker.get_current_route()
                        self.route_learner.learn_route(route_data)
                        self.last_learned_time = time.time()
                        self.log_event("✅ Route pattern learned and saved!")
        else:
            # Moving - reset stationary timer
            self.last_movement_time = time.time()

        
        if not was_away and self.away_mode:
            self.log_event("✈️ AWAY MODE ACTIVATED - Intruder detection enabled")
            # Save route when leaving
            route_file = self.route_tracker.save_route()
            self.log_event(f"💾 Route saved: {route_file}")
            
            if self.telegram.enabled:
                self.telegram.send_message("✈️ *AWAY MODE ACTIVE*\n\n🚨 Intruder detection enabled")
        
        if was_away and not self.away_mode:
            self.log_event("🏠 WELCOME HOME - Away mode deactivated")
            if self.telegram.enabled:
                self.telegram.send_message("🏠 *WELCOME HOME*\n\n✅ Away mode deactivated")
        
        # Check for geofence breach (crossing 50m boundary)
        if self.previous_location:
            if self.geofence.check_breach(current_location, self.previous_location):
                if self.away_mode:
                    # Away mode - intruder alert with photos
                    self.handle_intruder_breach(current_location, location_data)
                else:
                    # Home mode - open camera app for manual recording
                    self.handle_home_breach(current_location)
        
        self.previous_location = current_location
    
    def handle_home_breach(self, location):
        """Open camera app when crossing geofence at home"""
        self.log_event("🎥 GEOFENCE BREACH - Opening camera app!")
        
        # Save route snapshot at breach
        route_file = self.route_tracker.save_route()
        gpx_file = self.route_tracker.export_gpx()
        self.log_event(f"💾 Breach route saved: {route_file}")
        
        if self.telegram.enabled:
            stats = self.route_tracker.get_stats()
            route_text = ""
            if stats:
                route_text = f"\n📏 Distance walked: {stats['distance_meters']:.0f}m\n⏱️ Duration: {stats['duration_seconds']//60} min"
            
            self.telegram.send_message(
                f"🎥 *Geofence Breach Detected*\n\n"
                f"📍 Location: `{location[0]:.6f}, {location[1]:.6f}`\n"
                f"📅 Time: `{time.strftime('%Y-%m-%d %H:%M:%S')}`"
                f"{route_text}\n\n"
                f"📱 Camera app opened for manual recording"
            )
        
        # Open camera app
        self.video_recorder.record_breach_moment()
    
    def handle_intruder_breach(self, location, location_data):
        """Handle intruder detection when away"""
        # Check if this matches a known route pattern
        route_points = self.route_tracker.get_route()
        is_familiar = self.route_learner.is_similar_route(route_points) if route_points else False
        is_known_zone, zone = self.route_learner.is_normal_location(location)
        self.breach_count += 1
        accuracy = location_data.get('accuracy', 0)
        speed = location_data.get('speed', 0)
        
        network_info = self.network.get_network_summary() if self.network.available else None
        
        network_text = ""
        if network_info:
            wifi = network_info.get('wifi')
            cellular = network_info.get('cellular')
            
            if wifi and wifi.get('ssid') != '<unknown ssid>':
                network_text += f"\n📶 WiFi: `{wifi['ssid']}`"
                network_text += f"\n   Signal: {wifi['rssi']} dBm"
                network_text += f"\n   IP: `{wifi['ip']}`"
            
            if cellular:
                network_text += f"\n📱 Cellular: {cellular['type']}"
                network_text += f"\n   Signal: {cellular['strength']}%"
            
            nearby = network_info.get('nearby_networks', [])
            if nearby:
                network_text += f"\n\n📡 Nearby Networks:"
                for net in nearby[:3]:
                    network_text += f"\n   • {net.get('ssid', 'Hidden')} ({net.get('level', 0)} dBm)"
        
        # Adjust alert based on familiarity
        if is_familiar or is_known_zone:
            alert_level = "⚠️ *BREACH DETECTED - Familiar Pattern*"
            context = "Someone is following your usual route"
        else:
            alert_level = "🚨 *CRITICAL: UNKNOWN INTRUDER!*"
            context = "Unfamiliar movement pattern detected!"

        message = (
            f"{alert_level}\n\n"
            f"{context}\n\n"
            f"Someone entered your property while you're away!\n\n"
            f"*Breach #{self.breach_count}*\n"
            f"📅 Time: `{time.strftime('%Y-%m-%d %H:%M:%S')}`\n"
            f"📍 Location: `{location[0]:.6f}, {location[1]:.6f}`\n"
            f"🎯 Accuracy: ±{accuracy:.1f}m\n"
            f"🏃 Speed: {speed:.1f}m/s"
            f"{network_text}\n\n"
        )
        
        alert_type = "FAMILIAR BREACH" if (is_familiar or is_known_zone) else "UNKNOWN INTRUDER"
        self.log_event(f"🚨 {alert_type} - Breach #{self.breach_count}")
        
        if self.telegram.enabled:
            self.telegram.send_message(message)
            self.telegram.send_location(location[0], location[1], f"🚨 Intruder Breach #{self.breach_count}")
        
    
    def _capture_intruder_photos(self, location):
        """Capture 5 photos for intruder detection"""
        try:
            self.log_event("📸 Starting intruder photo capture...")
            results = self.camera.start_recording(duration_seconds=30)
            
            if isinstance(results, dict) and results.get('photos'):
                self.log_event(f"✅ Captured {len(results['photos'])} photos")
                
                if self.telegram.enabled:
                    for i, photo in enumerate(results['photos'], 1):
                        self.log_event(f"📤 Sending photo {i}/{len(results['photos'])}")
                        caption = f"🚨 INTRUDER - Photo {i}/{len(results['photos'])}"
                        self.telegram.send_file(photo, caption)
                        time.sleep(1)
                    
                    self.log_event("✅ All photos sent to Telegram")
            else:
                self.log_event(f"📝 Breach logged: {results}")
                
        except Exception as e:
            self.log_event(f"❌ Photo capture failed: {e}")
    
    def run(self):
        print("=" * 60)
        print("🌌 Dual Mode Geofence System with Route Tracking")
        print("=" * 60)
        
        self.log_event("System starting...")
        
        print("\n📱 Testing GPS access...")
        test_location = self.location_provider.get_current_location()
        
        if test_location:
            distance = self.geofence.get_distance_from_center(
                (test_location['latitude'], test_location['longitude'])
            )
            self.away_mode = distance > self.away_threshold_meters
            
            print(f"✅ GPS working!")
            print(f"   Latitude: {test_location['latitude']:.6f}")
            print(f"   Longitude: {test_location['longitude']:.6f}")
            print(f"   Distance from home: {distance:.1f}m")
            print(f"   Mode: {'✈️ AWAY' if self.away_mode else '🏠 HOME'}")
            
            if self.telegram.enabled:
                mode_status = "✈️ Away Mode" if self.away_mode else "🏠 Home Mode"
                startup_msg = f"""
🌌 *Dual Mode Geofence System Started*

📍 Current: `{test_location['latitude']:.6f}, {test_location['longitude']:.6f}`
🎯 Home: `{self.geofence.center[0]:.6f}, {self.geofence.center[1]:.6f}`
📏 Distance: {distance:.0f}m
🔔 Mode: {mode_status}
📸 Camera: ✅ Enabled
📶 Network: ✅ Enabled
🗺️ Route Tracking: ✅ Active

{'🚨 *INTRUDER ALERTS ACTIVE*' if self.away_mode else '🎥 *CAMERA PROMPT ON GEOFENCE BREACH*'}
"""
                self.telegram.send_message(startup_msg)
        else:
            print("❌ GPS not available!")
            return
        
        print("\n🔄 Starting continuous monitoring...")
        print("🎥 Camera app opens when crossing 50m geofence")
        print("🚨 Intruder detection when >200m away")
        print("🗺️ Route tracking active - saves on breach & away mode")
        print("Press Ctrl+C to stop\n")
        
        try:
            self.location_provider.start_continuous_tracking(
                self.handle_location_update, interval=5
            )
        except KeyboardInterrupt:
            self.log_event("System shutdown requested")
            
            # Learn from this session
            route_points = self.route_tracker.get_route()
            if route_points:
                self.route_learner.learn_from_route(route_points)
                self.log_event(f"🧠 Learned from {len(route_points)} GPS points")
                self.log_event(self.route_learner.get_zone_summary())
            
            # Save final route
            route_file = self.route_tracker.save_route()
            gpx_file = self.route_tracker.export_gpx()
            stats = self.route_tracker.get_stats()
            
            self.log_event(f"💾 Final route saved: {route_file}")
            self.log_event(f"💾 GPX exported: {gpx_file}")
            
            if stats:
                self.log_event(f"📊 Session stats: {stats['distance_meters']:.0f}m in {stats['duration_seconds']//60} min")
            
            if self.telegram.enabled:
                shutdown_msg = "🔴 *System Stopped*"
                if stats:
                    shutdown_msg += f"\n\n📊 Session Stats:\n📏 Distance: {stats['distance_meters']:.0f}m\n⏱️ Duration: {stats['duration_seconds']//60} min\n🚶 Avg Speed: {stats['avg_speed_mps']:.1f} m/s"
                self.telegram.send_message(shutdown_msg)
            
            print("\n👋 Shutting down...")

if __name__ == "__main__":
    system = DualModeGeofencingSystem()
    system.run()
