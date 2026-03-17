import subprocess
import json

class NetworkDetector:
    def __init__(self):
        self.available = self._check_available()
    
    def _check_available(self):
        """Check if network APIs are available"""
        try:
            subprocess.run(['termux-wifi-connectioninfo'], 
                         capture_output=True, timeout=2)
            return True
        except:
            return False
    
    def get_wifi_info(self):
        """Get current WiFi connection info"""
        try:
            result = subprocess.run(
                ['termux-wifi-connectioninfo'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return {
                    'ssid': data.get('ssid', 'Unknown'),
                    'bssid': data.get('bssid', 'Unknown'),
                    'ip': data.get('ip', 'Unknown'),
                    'rssi': data.get('rssi', 0),
                    'frequency': data.get('frequency_mhz', 0),
                    'link_speed': data.get('link_speed_mbps', 0)
                }
        except:
            pass
        return None
    
    def scan_wifi_networks(self):
        """Scan for nearby WiFi networks"""
        try:
            result = subprocess.run(
                ['termux-wifi-scaninfo'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                networks = json.loads(result.stdout)
                return networks[:5]  # Return top 5 strongest
        except:
            pass
        return []
    
    def get_cellular_info(self):
        """Get cellular network info"""
        try:
            result = subprocess.run(
                ['termux-telephony-cellinfo'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                if data:
                    cell = data[0]
                    return {
                        'type': cell.get('type', 'Unknown'),
                        'registered': cell.get('registered', False),
                        'strength': cell.get('strength', 0)
                    }
        except:
            pass
        return None
    
    def get_network_summary(self):
        """Get complete network summary"""
        summary = {
            'wifi': self.get_wifi_info(),
            'cellular': self.get_cellular_info(),
            'nearby_networks': self.scan_wifi_networks()
        }
        return summary
