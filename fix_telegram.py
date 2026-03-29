import re

with open('src/wifi_entity_detector.py', 'r') as f:
    content = f.read()

# Replace the silent except with verbose error handling
old_code = '''            try:
                from telegram_notifier import TelegramNotifier
                telegram = TelegramNotifier()
                telegram.send_message(
                    f"🚨 ENTITY AT {zone['name']}!\\n\\n"
                    f"👻 {zone['entity']}\\n"
                    f"📡 WiFi: {entity['ssid']}\\n"
                    f"🔍 BSSID: {entity['bssid']}\\n"
                    f"📶 {entity['signal']} dBm\\n"
                    f"📏 {distance:.1f}m from door\\n"
                    f"⏰ {datetime.now().strftime('%H:%M:%S')}"
                )
            except:
                pass'''

new_code = '''            try:
                from telegram_notifier import TelegramNotifier
                telegram = TelegramNotifier()
                result = telegram.send_message(
                    f"🚨 ENTITY AT {zone['name']}!\\n\\n"
                    f"👻 {zone['entity']}\\n"
                    f"📡 WiFi: {entity['ssid']}\\n"
                    f"🔍 BSSID: {entity['bssid']}\\n"
                    f"📶 {entity['signal']} dBm\\n"
                    f"📏 {distance:.1f}m from door\\n"
                    f"⏰ {datetime.now().strftime('%H:%M:%S')}"
                )
                if result:
                    print("                    ✅ Telegram sent!")
                else:
                    print("                    ⚠️  Telegram failed")
            except Exception as e:
                print(f"                    ❌ Telegram error: {e}")'''

content = content.replace(old_code, new_code)

with open('src/wifi_entity_detector.py', 'w') as f:
    f.write(content)

print("✅ Updated Telegram integration!")
