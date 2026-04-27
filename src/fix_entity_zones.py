#!/usr/bin/env python3
import json
from pathlib import Path

# Fix the entity_zones.json file
config_file = Path("config/entity_zones.json")
config_file.parent.mkdir(parents=True, exist_ok=True)

default_zones = {
    "creative_studio": {
        "lat": 37.7749,
        "lon": -122.4194,
        "radius": 50,
        "description": "Creative Studio - High entity activity",
        "entity_type": "creative_muse"
    },
    "meditation_room": {
        "lat": 37.7750,
        "lon": -122.4195,
        "radius": 30,
        "description": "Meditation Room - Spiritual entities",
        "entity_type": "spiritual_guide"
    },
    "library_corner": {
        "lat": 37.7751,
        "lon": -122.4196,
        "radius": 40,
        "description": "Library Corner - Knowledge entities",
        "entity_type": "knowledge_keeper"
    }
}

with open(config_file, 'w') as f:
    json.dump(default_zones, f, indent=2)

print("✅ Fixed entity_zones.json!")
