#!/usr/bin/env python3
"""
Activity Detection using ML
Detects: walking, running, biking, standing still
"""

import json
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from collections import deque

class ActivityDetector:
    def __init__(self):
        self.speed_history = deque(maxlen=20)
        self.acceleration_history = deque(maxlen=20)
        self.activity_log = Path("logs/activities.json")
        
        # Activity thresholds (m/s)
        self.STANDING = 0.5
        self.WALKING = 2.0
        self.RUNNING = 4.0
        self.BIKING = 8.0
        
    def detect_activity(self, speed, accuracy):
        """Detect current activity based on speed and patterns"""
        
        self.speed_history.append(speed)
        
        if len(self.speed_history) < 5:
            return "UNKNOWN"
        
        avg_speed = np.mean(list(self.speed_history))
        speed_variance = np.var(list(self.speed_history))
        
        # Detect activity type
        if avg_speed < self.STANDING:
            activity = "STANDING"
            emoji = "🧍"
        elif avg_speed < self.WALKING:
            if speed_variance < 0.5:
                activity = "WALKING_STEADY"
                emoji = "🚶"
            else:
                activity = "WALKING_VARIED"
                emoji = "🚶‍♂️"
        elif avg_speed < self.RUNNING:
            activity = "RUNNING"
            emoji = "🏃"
        elif avg_speed < self.BIKING:
            activity = "BIKING"
            emoji = "🚴"
        else:
            activity = "VEHICLE"
            emoji = "🚗"
        
        # Log activity
        self._log_activity(activity, avg_speed, speed_variance)
        
        return f"{emoji} {activity}"
    
    def predict_geofence_crossing(self, current_pos, geofence_center, radius, speed, bearing):
        """Predict if user will cross geofence in next 5 minutes"""
        
        if speed < 0.5:
            return False, 0
        
        # Calculate distance to geofence
        from math import radians, cos, sin, asin, sqrt, atan2, degrees
        
        lat1, lon1 = radians(current_pos[0]), radians(current_pos[1])
        lat2, lon2 = radians(geofence_center[0]), radians(geofence_center[1])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        distance = 6371000 * c  # meters
        
        # Calculate bearing to geofence
        y = sin(dlon) * cos(lat2)
        x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
        target_bearing = degrees(atan2(y, x))
        
        # Check if heading towards geofence
        bearing_diff = abs(target_bearing - bearing)
        if bearing_diff > 180:
            bearing_diff = 360 - bearing_diff
        
        # If heading towards geofence (within 45 degrees)
        if bearing_diff < 45:
            time_to_cross = (distance - radius) / speed
            if 0 < time_to_cross < 300:  # Within 5 minutes
                return True, int(time_to_cross)
        
        return False, 0
    
    def categorize_session(self, route_data):
        """Auto-categorize playtime session"""
        
        total_distance = route_data.get('total_distance', 0)
        duration = route_data.get('duration_minutes', 0)
        avg_speed = total_distance / (duration * 60) if duration > 0 else 0
        
        # Categorize based on patterns
        if total_distance < 100:
            category = "SHORT_PLAY"
            emoji = "⚡"
        elif total_distance < 500:
            category = "NEIGHBORHOOD_EXPLORE"
            emoji = "🏘️"
        elif total_distance < 2000:
            category = "ADVENTURE"
            emoji = "🗺️"
        else:
            category = "EPIC_JOURNEY"
            emoji = "🌍"
        
        # Add activity type
        if avg_speed > 3:
            category += "_ACTIVE"
        else:
            category += "_CASUAL"
        
        return f"{emoji} {category}"
    
    def _log_activity(self, activity, speed, variance):
        """Log activity to file"""
        
        activities = []
        if self.activity_log.exists():
            activities = json.loads(self.activity_log.read_text())
        
        activities.append({
            "timestamp": datetime.now().isoformat(),
            "activity": activity,
            "speed": round(speed, 2),
            "variance": round(variance, 2)
        })
        
        # Keep last 1000 entries
        activities = activities[-1000:]
        
        self.activity_log.write_text(json.dumps(activities, indent=2))
    
    def get_activity_stats(self, hours=24):
        """Get activity statistics for last N hours"""
        
        if not self.activity_log.exists():
            return {}
        
        activities = json.loads(self.activity_log.read_text())
        cutoff = datetime.now() - timedelta(hours=hours)
        
        recent = [a for a in activities 
                  if datetime.fromisoformat(a['timestamp']) > cutoff]
        
        if not recent:
            return {}
        
        # Calculate stats
        activity_counts = {}
        for a in recent:
            act = a['activity']
            activity_counts[act] = activity_counts.get(act, 0) + 1
        
        total_time = len(recent) * 10  # Assuming 10 sec intervals
        
        return {
            "total_activities": len(recent),
            "duration_minutes": total_time // 60,
            "breakdown": activity_counts,
            "most_common": max(activity_counts, key=activity_counts.get)
        }

if __name__ == "__main__":
    # Test
    detector = ActivityDetector()
    
    # Simulate walking
    for speed in [1.2, 1.5, 1.3, 1.4, 1.6]:
        activity = detector.detect_activity(speed, 5.0)
        print(f"Speed: {speed} m/s → {activity}")
    
    # Test prediction
    current = (36.007155, -88.417490)
    geofence = (36.008000, -88.418000)
    will_cross, eta = detector.predict_geofence_crossing(
        current, geofence, 100, 1.5, 45
    )
    print(f"\nWill cross: {will_cross}, ETA: {eta}s")
