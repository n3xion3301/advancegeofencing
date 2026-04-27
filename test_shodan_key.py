#!/usr/bin/env python3
import json
import shodan

# Read the config
with open('config/shodan_api.json', 'r') as f:
    config = json.load(f)
    api_key = config.get('api_key')
    
print(f"API Key from config: {api_key}")
print(f"Key length: {len(api_key) if api_key else 0}")
print(f"Key starts with: {api_key[:10] if api_key else 'None'}...")

# Test the key
try:
    api = shodan.Shodan(api_key)
    info = api.info()
    print(f"\n✓ API Key is VALID!")
    print(f"Plan: {info.get('plan', 'Unknown')}")
    print(f"Query credits: {info.get('query_credits', 0)}")
    print(f"Scan credits: {info.get('scan_credits', 0)}")
except shodan.APIError as e:
    print(f"\n❌ API Key ERROR: {e}")
    print("\nPossible issues:")
    print("1. Invalid API key")
    print("2. Key has extra spaces/quotes")
    print("3. Free tier limitations")
    print("\nGet your key from: https://account.shodan.io/")
except Exception as e:
    print(f"\n❌ Error: {e}")
