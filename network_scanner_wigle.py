#!/usr/bin/env python3
"""
Network Device Scanner with WiGLE API
Scans WiFi and Bluetooth devices using WiGLE.net database
"""

import subprocess
import json
from datetime import datetime
import math
import requests
import base64

def get_wigle_api():
    """Get WiGLE API credentials from config"""
    try:
        with open('config/wigle_api.json', 'r') as f:
            config = json.load(f)
            return config.get('api_name'), config.get('api_token')
    except:
        print("\n🔑 WiGLE API Setup")
        print("-" * 70)
        print("Get your free API key from: https://wigle.net/account")
        print("You need: API Name and API Token")
        api_name = input("Enter API Name: ").strip()
        api_token = input("Enter API Token: ").strip()
        
        if api_name and api_token:
            import os
            os.makedirs('config', exist_ok=True)
            with open('config/wigle_api.json', 'w') as f:
                json.dump({'api_name': api_name, 'api_token': api_token}, f)
            return api_name, api_token
        return None, None

def query_wigle_networks(lat, lon, api_name, api_token):
    """Query WiGLE for networks near location"""
    if not api_name or not api_token:
        return None
    
    try:
        # Create auth header
        auth_string = f"{api_name}:{api_token}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        
        headers = {
            'Authorization': f'Basic {auth_b64}',
            'Accept': 'application/json'
        }
        
        # Query nearby networks (within 0.01 degrees ~ 1km)
        url = 'https://api.wigle.net/api/v2/network/search'
        params = {
            'latrange1': lat - 0.01,
            'latrange2': lat + 0.01,
            'longrange1': lon - 0.01,
            'longrange2': lon + 0.01,
            'freenet': 'false',
            'paynet': 'false'
        }
        
        print(f"\n🔍 Querying WiGLE for networks near your location...")
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"  ⚠️  WiGLE API Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"  ❌ WiGLE Error: {e}")
        return None

def query_wigle_bluetooth(lat, lon, api_name, api_token):
    """Query WiGLE for Bluetooth devices near location"""
    if not api_name or not api_token:
        return None
    
    try:
        auth_string = f"{api_name}:{api_token}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        
        headers = {
            'Authorization': f'Basic {auth_b64}',
            'Accept': 'application/json'
        }
        
        # Query Bluetooth devices
        url = 'https://api.wigle.net/api/v2/bluetooth/search'
        params = {
            'latrange1': lat - 0.01,
            'latrange2': lat + 0.01,
            'longrange1': lon - 0.01,
            'longrange2': lon + 0.01
        }
        
        print(f"\n🔵 Querying WiGLE for Bluetooth devices...")
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"  ⚠️  WiGLE Bluetooth API Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"  ❌ WiGLE Bluetooth Error: {e}")
        return None

def get_public_ip():
    """Get public IP address"""
    try:
        result = subprocess.run(
            ['curl', '-s', 'https://api.ipify.org'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    return None

def scan_all_devices():
    """Comprehensive device scan with WiGLE"""
    print("\n" + "="*70)
    print("🔍 NETWORK DEVICE SCANNER WITH WIGLE")
    print("="*70)
    print(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    devices = {
        'timestamp': str(datetime.now()),
        'wifi': None,
        'location': None,
        'public_ip': None,
        'wigle_networks': None,
        'wigle_bluetooth': None,
        'at_home': None
    }
    
    # Get WiGLE API credentials
    api_name, api_token = get_wigle_api()
    
    # WiFi info
    print("\n📡 WiFi Information:")
    print("-" * 70)
    try:
        result = subprocess.run(
            ['termux-wifi-connectioninfo'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout:
            devices['wifi'] = json.loads(result.stdout)
            print(f"  SSID: {devices['wifi'].get('ssid', 'Unknown')}")
            print(f"  BSSID: {devices['wifi'].get('bssid', 'Unknown')}")
            print(f"  Local IP: {devices['wifi'].get('ip', 'Unknown')}")
            print(f"  Signal: {devices['wifi'].get('rssi', 'Unknown')} dBm")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Public IP
    print("\n🌐 Public IP Information:")
    print("-" * 70)
    public_ip = get_public_ip()
    if public_ip:
        devices['public_ip'] = public_ip
        print(f"  Public IP: {public_ip}")
    
    # Current location
    print("\n📍 Current Location:")
    print("-" * 70)
    
    try:
        result = subprocess.run(
            ['termux-location', '-p', 'gps', '-r', 'last'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout:
            devices['location'] = json.loads(result.stdout)
            print(f"  ✓ GPS Location acquired")
            print(f"  Latitude: {devices['location'].get('latitude'):.6f}")
            print(f"  Longitude: {devices['location'].get('longitude'):.6f}")
            print(f"  Accuracy: {devices['location'].get('accuracy')} meters")
    except:
        try:
            result = subprocess.run(
                ['termux-location', '-p', 'network'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0 and result.stdout:
                devices['location'] = json.loads(result.stdout)
                print(f"  ✓ Network Location acquired")
                print(f"  Latitude: {devices['location'].get('latitude'):.6f}")
                print(f"  Longitude: {devices['location'].get('longitude'):.6f}")
        except Exception as e:
            print(f"  ❌ Location failed: {e}")
    
    # Query WiGLE if we have location
    if devices['location'] and api_name and api_token:
        lat = devices['location']['latitude']
        lon = devices['location']['longitude']
        
        # Query WiFi networks
        wigle_data = query_wigle_networks(lat, lon, api_name, api_token)
        if wigle_data:
            devices['wigle_networks'] = wigle_data
            total = wigle_data.get('totalResults', 0)
            print(f"\n  ✓ Found {total} WiFi networks in WiGLE database")
            
            if total > 0:
                results = wigle_data.get('results', [])[:5]
                print(f"\n  Top 5 nearby networks:")
                for i, net in enumerate(results, 1):
                    print(f"    {i}. {net.get('ssid', 'Hidden')} - {net.get('netid', 'Unknown')}")
                    print(f"       Last seen: {net.get('lasttime', 'Unknown')}")
        
        # Query Bluetooth devices
        bt_data = query_wigle_bluetooth(lat, lon, api_name, api_token)
        if bt_data:
            devices['wigle_bluetooth'] = bt_data
            total = bt_data.get('totalResults', 0)
            print(f"\n  ✓ Found {total} Bluetooth devices in WiGLE database")
            
            if total > 0:
                results = bt_data.get('results', [])[:5]
                print(f"\n  Top 5 nearby Bluetooth devices:")
                for i, dev in enumerate(results, 1):
                    print(f"    {i}. {dev.get('name', 'Unknown')} - {dev.get('netid', 'Unknown')}")
                    print(f"       Last seen: {dev.get('lasttime', 'Unknown')}")
    
    # Check if at home
    if devices['location']:
        try:
            with open('config/home_location.json', 'r') as f:
                home_config = json.load(f)
                home_lat = home_config['coordinates']['latitude']
                home_lon = home_config['coordinates']['longitude']
                
                # Calculate distance
                R = 6371000
                lat1, lon1 = math.radians(home_lat), math.radians(home_lon)
                lat2, lon2 = math.radians(devices['location']['latitude']), math.radians(devices['location']['longitude'])
                
                dlat = lat2 - lat1
                dlon = lon2 - lon1
                
                a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                distance = R * c
                
                print(f"\n  Distance from home: {distance:.2f} meters")
                print(f"  Home: 208 Spring Street, Huntingdon, TN 38344")
                
                if distance <= 50:
                    print(f"  Status: ✅ AT HOME")
                    devices['at_home'] = True
                else:
                    print(f"  Status: ⚠️  AWAY FROM HOME ({distance:.0f}m away)")
                    devices['at_home'] = False
        except Exception as e:
            print(f"  ⚠️  Could not check home distance: {e}")
    
    # Save results
    print("\n" + "="*70)
    filename = f"device_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(devices, f, indent=2)
    
    print(f"✓ Results saved to: {filename}")
    
    # Summary
    print("\n📊 SCAN SUMMARY:")
    print("-" * 70)
    print(f"  WiFi: {devices['wifi'].get('ssid', 'Not connected') if devices['wifi'] else 'Not connected'}")
    print(f"  Public IP: {devices['public_ip'] if devices['public_ip'] else 'Unknown'}")
    print(f"  Location: {'Acquired' if devices['location'] else 'Failed'}")
    print(f"  At Home: {'✅ YES' if devices.get('at_home') else '⚠️  NO' if devices.get('at_home') == False else 'Unknown'}")
    print(f"  WiGLE Networks: {devices['wigle_networks'].get('totalResults', 0) if devices['wigle_networks'] else 'N/A'}")
    print(f"  WiGLE Bluetooth: {devices['wigle_bluetooth'].get('totalResults', 0) if devices['wigle_bluetooth'] else 'N/A'}")
    print("="*70)
    
    return devices

if __name__ == "__main__":
    scan_all_devices()
