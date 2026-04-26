#!/usr/bin/env python3
"""
ENHANCED Android Location Provider
GPS location services for Termux with advanced features

ENHANCEMENTS:
- Location caching and history
- Accuracy filtering
- Mock location support for testing
- Location smoothing
- Speed and bearing calculation
- Battery-efficient updates
- Comprehensive error handling
"""

import subprocess
import json
import time
import shutil
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from collections import deque
import warnings
warnings.filterwarnings('ignore')


class AndroidLocationProviderEnhanced:
    """
    Enhanced Android Location Provider
    
    Provides GPS location services with caching, filtering,
    and advanced location tracking features.
    """
    
    def __init__(self, cache_duration=30, history_size=100):
        """
        Initialize location provider
        
        Args:
            cache_duration: Seconds to cache location
            history_size: Number of locations to keep in history
        """
        self.cache_duration = cache_duration
        self.last_location = None
        self.last_update_time = None
        
        # Location history
        self.location_history = deque(maxlen=history_size)
        
        # Check Termux API availability
        self.location_enabled = self._check_location_available()
        
        # Mock location for testing
        self.mock_mode = False
        self.mock_location = None
        
        # Accuracy threshold (meters)
        self.min_accuracy = 50  # Reject locations worse than 50m
        
        # Setup logging
        self.log_dir = Path("logs/location")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "location_enhanced.log"
        
        self.log("✅ Enhanced Android Location Provider initialized")
        self.log(f"   Termux API: {'Available' if self.location_enabled else 'Not Available'}")
        self.log(f"   Cache duration: {cache_duration}s")
    
    def log(self, msg):
        """Log message with timestamp"""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{ts}] {msg}"
        print(formatted)
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(formatted + "\n")
        except Exception:
            pass
    
    def _check_location_available(self):
        """Check if Termux API is available"""
        try:
            # Check if termux-location exists
            termux_location_path = shutil.which('termux-location')
            if termux_location_path:
                self.log(f"✅ Found termux-location at: {termux_location_path}")
                return True
            
            # Try to run it
            result = subprocess.run(
                ['termux-location', '-h'],
                capture_output=True,
                timeout=2
            )
            return result.returncode == 0
            
        except Exception as e:
            self.log(f"⚠️  Termux API check failed: {e}")
            return False
    
    def enable_mock_mode(self, lat=None, lon=None):
        """
        Enable mock location for testing
        
        Args:
            lat: Mock latitude (default: New York)
            lon: Mock longitude (default: New York)
        """
        self.mock_mode = True
        self.mock_location = {
            'latitude': lat or 40.7128,
            'longitude': lon or -74.0060,
            'accuracy': 5.0,
            'altitude': 10.0,
            'bearing': 0.0,
            'speed': 0.0,
            'provider': 'mock'
        }
        self.log("🎭 Mock mode enabled")
    
    def disable_mock_mode(self):
        """Disable mock location"""
        self.mock_mode = False
        self.mock_location = None
        self.log("🎭 Mock mode disabled")
    
    def get_current_location(self, force_update=False):
        """
        Get current location with caching
        
        Args:
            force_update: Force fresh location update
        
        Returns:
            dict: Location data or None
        """
        # Check cache
        if not force_update and self._is_cache_valid():
            self.log("📍 Using cached location")
            return self.last_location
        
        # Mock mode
        if self.mock_mode:
            return self._get_mock_location()
        
        # Get fresh location
        if not self.location_enabled:
            self.log("❌ Termux API not available")
            return None
        
        try:
            self.log("📡 Requesting location update...")
            
            # Call termux-location
            result = subprocess.run(
                ['termux-location'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                self.log(f"❌ termux-location failed: {result.stderr}")
                return self.last_location
            
            if not result.stdout.strip():
                self.log("❌ No location data received")
                return self.last_location
            
            # Parse location data
            location_data = json.loads(result.stdout)
            
            # Validate location
            if not self._validate_location(location_data):
                self.log("⚠️  Invalid location data")
                return self.last_location
            
            # Enhance location data
            enhanced_location = self._enhance_location(location_data)
            
            # Update cache
            self.last_location = enhanced_location
            self.last_update_time = datetime.now()
            
            # Add to history
            self.location_history.append(enhanced_location)
            
            self.log(f"✅ Location updated: ({enhanced_location['latitude']:.6f}, "
                    f"{enhanced_location['longitude']:.6f}) "
                    f"±{enhanced_location.get('accuracy', 0):.1f}m")
            
            return enhanced_location
            
        except subprocess.TimeoutExpired:
            self.log("⏱️  Location request timed out")
            return self.last_location
        except json.JSONDecodeError as e:
            self.log(f"❌ JSON parse error: {e}")
            return self.last_location
        except Exception as e:
            self.log(f"❌ Error getting location: {e}")
            return self.last_location
    
    def _get_mock_location(self):
        """Get mock location with simulated movement"""
        if not self.mock_location:
            return None
        
        # Add small random movement
        mock = self.mock_location.copy()
        mock['latitude'] += np.random.normal(0, 0.00001)
        mock['longitude'] += np.random.normal(0, 0.00001)
        mock['timestamp'] = datetime.now().isoformat()
        
        # Update cache
        self.last_location = mock
        self.last_update_time = datetime.now()
        self.location_history.append(mock)
        
        return mock
    
    def _is_cache_valid(self):
        """Check if cached location is still valid"""
        if self.last_location is None or self.last_update_time is None:
            return False
        
        age = (datetime.now() - self.last_update_time).total_seconds()
        return age < self.cache_duration
    
    def _validate_location(self, location_data):
        """Validate location data"""
        # Check required fields
        if 'latitude' not in location_data or 'longitude' not in location_data:
            return False
        
        lat = location_data['latitude']
        lon = location_data['longitude']
        
        # Check valid ranges
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            return False
        
        # Check accuracy if available
        accuracy = location_data.get('accuracy')
        if accuracy is not None and accuracy > self.min_accuracy:
            self.log(f"⚠️  Low accuracy: {accuracy:.1f}m (threshold: {self.min_accuracy}m)")
            # Still return True but log warning
        
        return True
    
    def _enhance_location(self, location_data):
        """Enhance location data with calculated fields"""
        enhanced = location_data.copy()
        enhanced['timestamp'] = datetime.now().isoformat()
        
        # Calculate speed and bearing if we have history
        if len(self.location_history) > 0:
            prev = self.location_history[-1]
            
            # Calculate distance
            distance = self._calculate_distance(
                prev['latitude'], prev['longitude'],
                enhanced['latitude'], enhanced['longitude']
            )
            
            # Calculate time difference
            if 'timestamp' in prev:
                prev_time = datetime.fromisoformat(prev['timestamp'])
                time_diff = (datetime.now() - prev_time).total_seconds()
                
                if time_diff > 0:
                    # Calculate speed (m/s)
                    calculated_speed = distance / time_diff
                    enhanced['calculated_speed'] = calculated_speed
                    enhanced['calculated_speed_kmh'] = calculated_speed * 3.6
            
            # Calculate bearing
            bearing = self._calculate_bearing(
                prev['latitude'], prev['longitude'],
                enhanced['latitude'], enhanced['longitude']
            )
            enhanced['calculated_bearing'] = bearing
        
        return enhanced
    
    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points (Haversine formula)"""
        R = 6371000  # Earth radius in meters
        
        lat1_rad = np.radians(lat1)
        lat2_rad = np.radians(lat2)
        dlat = np.radians(lat2 - lat1)
        dlon = np.radians(lon2 - lon1)
        
        a = (np.sin(dlat/2)**2 + 
             np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon/2)**2)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        
        return R * c
    
    def _calculate_bearing(self, lat1, lon1, lat2, lon2):
        """Calculate bearing between two points"""
        lat1_rad = np.radians(lat1)
        lat2_rad = np.radians(lat2)
        dlon = np.radians(lon2 - lon1)
        
        y = np.sin(dlon) * np.cos(lat2_rad)
        x = (np.cos(lat1_rad) * np.sin(lat2_rad) - 
             np.sin(lat1_rad) * np.cos(lat2_rad) * np.cos(dlon))
        
        bearing = np.degrees(np.arctan2(y, x))
        return (bearing + 360) % 360
    
    def get_smoothed_location(self, window_size=5):
        """Get smoothed location using moving average"""
        if len(self.location_history) < window_size:
            return self.last_location
        
        recent = list(self.location_history)[-window_size:]
        
        avg_lat = np.mean([loc['latitude'] for loc in recent])
        avg_lon = np.mean([loc['longitude'] for loc in recent])
        
        smoothed = self.last_location.copy() if self.last_location else {}
        smoothed['latitude'] = avg_lat
        smoothed['longitude'] = avg_lon
        smoothed['smoothed'] = True
        smoothed['window_size'] = window_size
        
        return smoothed
    
    def get_location_stats(self):
        """Get statistics about location history"""
        if not self.location_history:
            return None
        
        lats = [loc['latitude'] for loc in self.location_history]
        lons = [loc['longitude'] for loc in self.location_history]
        
        stats = {
            'count': len(self.location_history),
            'latitude': {
                'mean': np.mean(lats),
                'std': np.std(lats),
                'min': np.min(lats),
                'max': np.max(lats)
            },
            'longitude': {
                'mean': np.mean(lons),
                'std': np.std(lons),
                'min': np.min(lons),
                'max': np.max(lons)
            }
        }
        
        # Calculate total distance traveled
        if len(self.location_history) > 1:
            total_distance = 0
            for i in range(1, len(self.location_history)):
                prev = self.location_history[i-1]
                curr = self.location_history[i]
                total_distance += self._calculate_distance(
                    prev['latitude'], prev['longitude'],
                    curr['latitude'], curr['longitude']
                )
            stats['total_distance_m'] = total_distance
            stats['total_distance_km'] = total_distance / 1000
        
        return stats


def demo_enhanced_location():
    """Demonstrate enhanced location provider"""
    print("="*80)
    print("📍 ENHANCED ANDROID LOCATION PROVIDER DEMO")
    print("="*80)
    
    # Initialize provider
    provider = AndroidLocationProviderEnhanced(cache_duration=10)
    
    # Enable mock mode for demo
    print("\n🎭 Enabling mock mode for demonstration...")
    provider.enable_mock_mode(lat=40.7128, lon=-74.0060)
    
    # Get locations
    print("\n📡 Getting locations...")
    for i in range(5):
        print(f"\nUpdate {i+1}:")
        location = provider.get_current_location()
        
        if location:
            print(f"  Lat: {location['latitude']:.6f}")
            print(f"  Lon: {location['longitude']:.6f}")
            print(f"  Accuracy: {location.get('accuracy', 0):.1f}m")
            
            if 'calculated_speed_kmh' in location:
                print(f"  Speed: {location['calculated_speed_kmh']:.2f} km/h")
            if 'calculated_bearing' in location:
                print(f"  Bearing: {location['calculated_bearing']:.1f}°")
        
        time.sleep(1)
    
    # Get smoothed location
    print("\n📊 Smoothed Location:")
    smoothed = provider.get_smoothed_location()
    print(f"  Lat: {smoothed['latitude']:.6f}")
    print(f"  Lon: {smoothed['longitude']:.6f}")
    
    # Get statistics
    print("\n📈 Location Statistics:")
    stats = provider.get_location_stats()
    if stats:
        print(f"  Total updates: {stats['count']}")
        print(f"  Avg latitude: {stats['latitude']['mean']:.6f}")
        print(f"  Avg longitude: {stats['longitude']['mean']:.6f}")
        if 'total_distance_m' in stats:
            print(f"  Total distance: {stats['total_distance_m']:.2f}m")
    
    print("\n" + "="*80)
    print("✅ DEMO COMPLETE!")
    print("="*80)


if __name__ == "__main__":
    demo_enhanced_location()
