with open('src/wifi_entity_detector.py', 'r') as f:
    content = f.read()

# Find the telegram.send_message call and change the message format
old_msg = '''                result = telegram.send_message(
                    f"🚨 ENTITY AT {zone['name']}!\\n\\n"
                    f"👻 {zone['entity']}\\n"
                    f"📡 WiFi: {entity['ssid']}\\n"
                    f"🔍 BSSID: {entity['bssid']}\\n"
                    f"📶 {entity['signal']} dBm\\n"
                    f"📏 {distance:.1f}m from door\\n"
                    f"⏰ {datetime.now().strftime('%H:%M:%S')}"
                )'''

new_msg = '''                msg = (
                    f"🚨 ENTITY AT {zone['name']}!\\n\\n"
                    f"👻 {zone['entity']}\\n"
                    f"📡 WiFi: {entity['ssid']}\\n"
                    f"🔍 BSSID: {entity['bssid']}\\n"
                    f"📶 {entity['signal']} dBm\\n"
                    f"📏 {distance:.1f}m from door\\n"
                    f"⏰ {datetime.now().strftime('%H:%M:%S')}"
                )
                result = telegram.send_message(msg, parse_mode=None)'''

content = content.replace(old_msg, new_msg)

with open('src/wifi_entity_detector.py', 'w') as f:
    f.write(content)

print("✅ Fixed Telegram message format!")
