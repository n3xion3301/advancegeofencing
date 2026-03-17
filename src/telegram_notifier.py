import requests
import os
from datetime import datetime

class TelegramNotifier:
    def __init__(self, bot_token=None, chat_id=None):
        self.bot_token = bot_token or os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = chat_id or os.getenv('TELEGRAM_CHAT_ID')
        
        if self.bot_token and self.chat_id:
            self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
            self.enabled = True
            print("✅ Telegram notifications enabled")
        else:
            self.enabled = False
            print("⚠️  Telegram not configured")
    
    def send_message(self, message, parse_mode='Markdown'):
        """Send text message"""
        if not self.enabled:
            return False
            
        url = f"{self.base_url}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': parse_mode
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Telegram send failed: {e}")
            return False
    
    def send_location(self, latitude, longitude, title="Breach Location"):
        """Send location pin"""
        if not self.enabled:
            return False
            
        # Send venue (location with title)
        url = f"{self.base_url}/sendVenue"
        payload = {
            'chat_id': self.chat_id,
            'latitude': latitude,
            'longitude': longitude,
            'title': title,
            'address': f"Lat: {latitude:.6f}, Lon: {longitude:.6f}"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Telegram location send failed: {e}")
            return False
    
    def send_file(self, file_path, caption=None):
        """Send file (video, photo, document)"""
        if not self.enabled:
            return False
            
        url = f"{self.base_url}/sendDocument"
        
        try:
            with open(file_path, 'rb') as file:
                files = {'document': file}
                data = {
                    'chat_id': self.chat_id,
                    'caption': caption or f"File: {os.path.basename(file_path)}"
                }
                response = requests.post(url, files=files, data=data, timeout=30)
                return response.status_code == 200
        except Exception as e:
            print(f"❌ Telegram file send failed: {e}")
            return False
    
    def send_breach_alert(self, location, accuracy, speed, breach_count):
        """Send formatted breach alert"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        message = f"""
🚨 *GEOFENCE BREACH DETECTED* 🚨

*Breach #{breach_count}*
📅 Time: `{timestamp}`
📍 Location: `{location[0]:.6f}, {location[1]:.6f}`
🎯 Accuracy: ±{accuracy:.1f}m
🏃 Speed: {speed:.1f}m/s

⚠️ Someone entered your residence area!
"""
        
        # Send message
        self.send_message(message)
        
        # Send location pin
        self.send_location(location[0], location[1], f"Breach #{breach_count}")
