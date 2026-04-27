#!/usr/bin/env python3
"""
Network Device Scanner with Shodan API
Identifies devices on your network and checks Shodan for security info
"""

import subprocess
import json
import socket
from datetime import datetime
import shodan

def get_shodan_api():
    """Get Shodan API key from config or prompt"""
    try:
        with open('config/shodan_api.json', 'r') as f:
            config = json.load(f)
            return config.get('api_key')
    except:
        print("\n🔑 Shodan API Key Setup")
        print("-" * 60)
        print("Get your free API key from: https://account.shodan.io/")
        api_key = input("Enter Shodan API key: ").strip()
        
        if api_key:
            # Save for future use
            import os
            os.makedirs('config', exist_ok=True)
            with open('config/shodan_api.json', 'w') as f:
                json.dump({'api_key': api_key}, f)
            return api_key
        return None

def scan_with_shodan(ip_address, api_key):
    """Query Shodan for device information"""
    if not api_key:
        return None
    
    try:
        api = shodan.Shodan(api_key)
        
        print(f"\n🔍 Querying Shodan for {ip_address}...")
        host = api.host(ip_address)
        
        info = {
            'ip': host['ip_str'],
            'organization': host.get('org', 'Unknown'),
            'operating_system': host.get('os', 'Unknown'),
            'ports': host.get('ports', []),
            'vulnerabilities': host.get('vulns', []),
            'hostnames': host.get('hostnames', []),
            'domains': host.get('domains', []),
            'city': host.get('city', 'Unknown'),
            'country': host.get('country_name', 'Unknown'),
            'isp': host.get('isp', 'Unknown'),
            'last_update': host.get('last_update', 'Unknown')
        }
        
        return info
        
    except shodan.APIError as e:
        print(f"  ⚠️  Shodan API Error: {e}")
        return None
    except Exception as e:
        print(f"  ❌ Error: {e}")
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
    """Comprehensive device scan with Shodan"""
    print("\n" + "="*70)
    print("🔍 NETWORK DEVICE SCANNER WITH SHODAN")
    print("="*70)
    print(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    devices = {
        'timestamp': str(datetime.now()),
        'wifi': None,
        'location': None,
        'public_ip': None,
        'shodan_info': None
    }
    
    # Get Shodan API key
    shodan_api_key = get_shodan_api()
    
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
            print(f"  MAC Address: {devices['wifi'].get('mac', 'Unknown')}")
            print(f"  Signal: {devices['wifi'].get('rssi', 'Unknown')} dBm")
            print(f"  Speed: {devices['wifi'].get('link_speed', 'Unknown')} Mbps")
        else:
            print("  ⚠️  Not connected to WiFi")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Public IP
    print("\n🌐 Public IP Information:")
    print("-" * 70)
    public_ip = get_public_ip()
    if public_ip:
        devices['public_ip'] = public_ip
        print(f"  Public IP: {public_ip}")
        
        # Query Shodan for this IP
        if shodan_api_key:
            shodan_info = scan_with_shodan(public_ip, shodan_api_key)
            if shodan_info:
                devices['shodan_info'] = shodan_info
                
                print(f"\n  📊 Shodan Information:")
                print(f"     Organization: {shodan_info['organization']}")
                print(f"     ISP: {shodan_info['isp']}")
                print(f"     Location: {shodan_info['city']}, {shodan_info['country']}")
                print(f"     OS: {shodan_info['operating_system']}")
                print(f"     Open Ports: {shodan_info['ports']}")
                print(f"     Hostnames: {shodan_info['hostnames']}")
                
                if shodan_info['vulnerabilities']:
                    print(f"\n  ⚠️  VULNERABILITIES DETECTED:")
                    for vuln in shodan_info['vulnerabilities']:
                        print(f"     • {vuln}")
                else:
                    print(f"\n  ✓ No known vulnerabilities")
    else:
        print("  ⚠️  Could not determine public IP")
    
    # Current location
    print("\n📍 Current Location:")
    print("-" * 70)
    
    # Try GPS first
    print("Attempting GPS location...")
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
            print(f"  Latitude: {devices['location'].get('latitude', 'Unknown')}")
            print(f"  Longitude: {devices['location'].get('longitude', 'Unknown')}")
            print(f"  Accuracy: {devices['location'].get('accuracy', 'Unknown')} meters")
    except Exception as e:
        print(f"  ⚠️  GPS failed, trying network location...")
        
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
                print(f"  Latitude: {devices['location'].get('latitude', 'Unknown')}")
                print(f"  Longitude: {devices['location'].get('longitude', 'Unknown')}")
        except Exception as e:
            print(f"  ❌ Location failed: {e}")
    
    # Check if at home
    if devices['location']:
        import math
        
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
                    print(f"  Status: ⚠️  AWAY FROM HOME")
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
    print(f"  WiFi Connected: {'Yes - ' + devices['wifi'].get('ssid', 'Unknown') if devices['wifi'] else 'No'}")
    print(f"  Public IP: {devices['public_ip'] if devices['public_ip'] else 'Unknown'}")
    print(f"  Location: {'Acquired' if devices['location'] else 'Failed'}")
    print(f"  At Home: {'Yes' if devices.get('at_home') else 'No' if 'at_home' in devices else 'Unknown'}")
    print(f"  Shodan Scan: {'Complete' if devices['shodan_info'] else 'Not available'}")
    print("="*70)
    
    return devices

if __name__ == "__main__":
    scan_all_devices()
