import requests
import os
import json
from datetime import datetime
from pathlib import Path

class TelegramNotifier:
    def __init__(self, bot_token=None, chat_id=None):
        config = self._load_config()
        
        self.bot_token = bot_token or config.get('bot_token') or os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = chat_id or config.get('chat_id') or os.getenv('TELEGRAM_CHAT_ID')

        if self.bot_token and self.chat_id:
            self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
            self.enabled = True
            print("✅ Telegram notifications enabled")
        else:
            self.enabled = False
    
    def _load_config(self):
        config_file = Path("config/telegram_config.json")
        if config_file.exists():
            return json.loads(config_file.read_text())
        return {}

    def send_message(self, message, parse_mode=None):
        """Send text message"""
        if not self.enabled:
            return False

        url = f"{self.base_url}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message
        }
        
        # Only add parse_mode if it's not None
        if parse_mode:
            payload['parse_mode'] = parse_mode

        try:
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Telegram error: {e}")
            return False

    def send_location(self, latitude, longitude, title="Breach Location"):
        if not self.enabled:
            return False

        url = f"{self.base_url}/sendVenue"
        payload = {
            'chat_id': self.chat_id,
            'latitude': latitude,
            'longitude': longitude,
            'title': title,
            'address': f"{latitude:.6f}, {longitude:.6f}"
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
        except:
            return False
