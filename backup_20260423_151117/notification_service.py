import requests
from datetime import datetime

class NotificationService:
    def __init__(self):
        # Configure your notification method
        self.webhook_url = None  # Add webhook URL if using Discord/Slack
        
    def send_alert(self, title, message):
        """Send breach alert notification"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        alert = f"[{timestamp}] {title}: {message}"
        
        print(f"🔔 {alert}")
        
        # Optional: Send to webhook
        if self.webhook_url:
            self._send_webhook(title, message)
    
    def _send_webhook(self, title, message):
        """Send notification via webhook"""
        payload = {
            "content": f"**{title}**\n{message}"
        }
        try:
            requests.post(self.webhook_url, json=payload)
        except Exception as e:
            print(f"Failed to send webhook: {e}")
