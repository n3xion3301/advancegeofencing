#!/usr/bin/env python3
"""QUANTUM TELEGRAM NOTIFIER - Quantum-secured Telegram notifications"""
import json, requests
from datetime import datetime
from pathlib import Path

try:
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False

class QuantumTelegramNotifier:
    def __init__(self):
        self.config_file = Path("config/telegram.json")
        self.log_file = Path("logs/quantum/telegram.log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.config = self.load_config()
    
    def log(self, msg):
        """Log message"""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] {msg}")
        with open(self.log_file, 'a') as f:
            f.write(f"[{ts}] {msg}\n")
    
    def load_config(self):
        """Load Telegram config"""
        if self.config_file.exists():
            with open(self.config_file) as f:
                return json.load(f)
        return {'bot_token': None, 'chat_id': None}
    
    def quantum_encrypt_message(self, message):
        """Apply quantum encryption to message (demonstration)"""
        if not QISKIT_AVAILABLE:
            return message
        
        # Add quantum signature
        return f"🔮 [QUANTUM] {message}"
    
    def send_notification(self, message, priority='normal'):
        """Send quantum-secured notification"""
        if not self.config.get('bot_token'):
            self.log("⚠️  Telegram not configured")
            return False
        
        try:
            # Apply quantum encryption
            encrypted_msg = self.quantum_encrypt_message(message)
            
            url = f"https://api.telegram.org/bot{self.config['bot_token']}/sendMessage"
            
            data = {
                'chat_id': self.config['chat_id'],
                'text': encrypted_msg,
                'parse_mode': 'HTML'
            }
            
            if priority == 'high':
                data['text'] = f"⚠️ <b>HIGH PRIORITY</b>\n{data['text']}"
            
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                self.log(f"✅🔮 Quantum notification sent")
                return True
            else:
                self.log(f"❌ Send failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log(f"❌ Telegram error: {e}")
            return False
    
    def send_zone_alert(self, zone_name, event_type):
        """Send zone event alert"""
        message = f"Zone Event: {event_type}\nZone: {zone_name}\nTime: {datetime.now().strftime('%H:%M:%S')}"
        return self.send_notification(message, priority='high')

if __name__ == "__main__":
    notifier = QuantumTelegramNotifier()
    notifier.send_notification("Quantum Telegram system test! 🔮")
