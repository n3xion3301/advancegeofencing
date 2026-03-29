import json

with open('src/wifi_entity_detector.py', 'r') as f:
    content = f.read()

old_code = """    with open('config/my_networks.json', 'r') as f:
        filter_networks = json.load(f)['networks']"""

new_code = """    with open('config/my_networks.json', 'r') as f:
        my_nets = json.load(f)['my_networks']
        filter_networks = my_nets.get('ssids', []) + my_nets.get('keywords', [])"""

content = content.replace(old_code, new_code)

with open('src/wifi_entity_detector.py', 'w') as f:
    f.write(content)

print("✅ Fixed!")
