#!/usr/bin/env python3
"""
Fix for GPS timeout in zone wizard
Adds fallback options and better error handling
"""

import subprocess
import json
import time

def get_location_with_fallback(timeout=15):
    """Get location with multiple fallback methods"""
    
    # Method 1: Try termux-location with longer timeout
    print("📡 Attempting GPS fix (this may take 15-30 seconds)...")
    try:
        result = subprocess.run(
            ['termux-location', '-p', 'gps', '-r', 'last'],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)
            if 'latitude' in data and 'longitude' in data:
                return {
                    'latitude': data['latitude'],
                    'longitude': data['longitude'],
                    'accuracy': data.get('accuracy', 'unknown'),
                    'method': 'gps'
                }
    except subprocess.TimeoutExpired:
        print("⏱️  GPS timeout, trying network location...")
    except Exception as e:
        print(f"⚠️  GPS error: {e}")
    
    # Method 2: Try network-based location
    try:
        result = subprocess.run(
            ['termux-location', '-p', 'network'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)
            if 'latitude' in data and 'longitude' in data:
                return {
                    'latitude': data['latitude'],
                    'longitude': data['longitude'],
                    'accuracy': data.get('accuracy', 'unknown'),
                    'method': 'network'
                }
    except Exception as e:
        print(f"⚠️  Network location error: {e}")
    
    # Method 3: Manual entry fallback
    print("\n📍 Automatic location failed. Manual entry:")
    print("Tip: You can get coordinates from Google Maps")
    
    try:
        lat = float(input("Enter latitude: ").strip())
        lon = float(input("Enter longitude: ").strip())
        return {
            'latitude': lat,
            'longitude': lon,
            'accuracy': 'manual',
            'method': 'manual'
        }
    except ValueError:
        print("❌ Invalid coordinates")
        return None

if __name__ == "__main__":
    loc = get_location_with_fallback()
    if loc:
        print(f"\n✓ Location: {loc['latitude']}, {loc['longitude']}")
        print(f"  Method: {loc['method']}, Accuracy: {loc['accuracy']}")
    else:
        print("❌ Could not get location")
