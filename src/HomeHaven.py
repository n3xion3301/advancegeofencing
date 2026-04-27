#!/usr/bin/env python3 n3xion3301
"""
Geofencing Script for Home Monitoring
Detects when objects/people enter your home geofence zone
Records timestamps and optionally captures data
"""

import math
import json
import time
from datetime import datetime
from typing import Tuple, Dict, List
import os
import sys

# For GPS on Termux, you may need: pkg install gpsd python-gps
# Or use your phone's built-in location services

class GeoFence:
    """
    A simple geofencing system for monitoring a defined area
    """

    def __init__(self, center_lat: float, center_lon: float, radius_meters: float):
        """
        Initialize geofence with center coordinates and radius

        Args:
            center_lat: Center latitude (your home)
            center_lon: Center longitude (your home)
            radius_meters: Radius of geofence in meters
        """
        self.center_lat = center_lat
        self.center_lon = center_lon
        self.radius_meters = radius_meters
        self.detection_log = []
        self.inside_zone = False
        self.entry_time = None

    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two coordinates using Haversine formula
        Returns distance in meters
        """
        R = 6371000  # Earth radius in meters

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
        c = 2 * math.asin(math.sqrt(a))

        distance = R * c
        return distance

    def is_inside(self, lat: float, lon: float) -> bool:
        """
        Check if coordinates are inside geofence
        """
        distance = self.haversine_distance(self.center_lat, self.center_lon, lat, lon)
        return distance <= self.radius_meters

    def check_location(self, lat: float, lon: float, device_id: str = "UNKNOWN") -> Dict:
        """
        Check location and detect entry/exit events
        """
        is_inside = self.is_inside(lat, lon)
        distance = self.haversine_distance(self.center_lat, self.center_lon, lat, lon)

        event = {
            "timestamp": datetime.now().isoformat(),
            "latitude": lat,
            "longitude": lon,
            "device_id": device_id,
            "distance_from_center": round(distance, 2),
            "event_type": None
        }

        # Detect entry
        if is_inside and not self.inside_zone:
            event["event_type"] = "ENTRY"
            self.inside_zone = True
            self.entry_time = datetime.now()
            print(f"🚨 ENTRY DETECTED at {event['timestamp']}")
            print(f"   Location: {lat}, {lon}")
            print(f"   Distance from center: {distance:.2f}m")

        # Detect exit
        elif not is_inside and self.inside_zone:
            event["event_type"] = "EXIT"
            self.inside_zone = False
            duration = (datetime.now() - self.entry_time).total_seconds()
            event["duration_inside"] = round(duration, 2)
            print(f"🚪 EXIT DETECTED at {event['timestamp']}")
            print(f"   Duration inside: {duration:.2f}s")

        # Still inside
        elif is_inside and self.inside_zone:
            event["event_type"] = "INSIDE"

        # Still outside
        else:
            event["event_type"] = "OUTSIDE"

        self.detection_log.append(event)
        return event

    def save_log(self, filename: str = "geofence_log.json"):
        """Save detection log to file"""
        with open(filename, 'w') as f:
            json.dump(self.detection_log, f, indent=2)
        print(f"✅ Log saved to {filename}")

    def get_stats(self) -> Dict:
        """Get statistics about detections"""
        entries = [e for e in self.detection_log if e["event_type"] == "ENTRY"]
        exits = [e for e in self.detection_log if e["event_type"] == "EXIT"]

        return {
            "total_events": len(self.detection_log),
            "entries": len(entries),
            "exits": len(exits),
            "currently_inside": self.inside_zone
        }


# Example usage with simulated location data
def main():
    """
    Main function - demonstrating geofence usage
    """

    # Configure your home location here
    HOME_LAT = 40.7128  # Replace with your home latitude
    HOME_LON = -74.0060  # Replace with your home longitude
    GEOFENCE_RADIUS = 100  # 100 meters radius

    print("=" * 60)
    print("🏠 HOME GEOFENCING SYSTEM")
    print("=" * 60)
    print(f"Home Location: {HOME_LAT}, {HOME_LON}")
    print(f"Geofence Radius: {GEOFENCE_RADIUS}m")
    print("=" * 60)

    # Initialize geofence
    geofence = GeoFence(HOME_LAT, HOME_LON, GEOFENCE_RADIUS)

    # Simulated location data (replace with real GPS data)
    test_locations = [
        (40.7128, -74.0060, "Device1"),      # At center
        (40.71285, -74.0060, "Device1"),     # ~5m away (ENTRY)
        (40.71290, -74.0060, "Device2"),     # ~20m away (INSIDE)
        (40.71300, -74.0060, "Device1"),     # ~80m away (INSIDE)
        (40.71315, -74.0060, "Device1"),     # ~150m away (EXIT)
        (40.71320, -74.0060, "Device1"),     # ~200m away (OUTSIDE)
    ]

    print("\n📍 Processing location data...\n")

    for lat, lon, device_id in test_locations:
        event = geofence.check_location(lat, lon, device_id)
        time.sleep(1)  # Simulate delay between readings
        print()

    # Print statistics
    print("\n" + "=" * 60)
    print("📊 STATISTICS")
    print("=" * 60)
    stats = geofence.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")

    # Save log
    geofence.save_log()


if __name__ == "__main__":

