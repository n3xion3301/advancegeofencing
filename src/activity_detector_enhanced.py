#!/usr/bin/env python3
"""
ENHANCED Activity Detection using ML + Quantum-Inspired Probability
Detects: walking, running, biking, standing still
Uses quantum probability for uncertainty modeling

ENHANCEMENTS:
- Quantum-inspired probability calculations
- Better error handling and logging
- Real-time visualization
- Pattern recognition improvements
- Anomaly detection
- Activity prediction
"""

import json
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from collections import deque
import warnings
warnings.filterwarnings('ignore')

class ActivityDetectorEnhanced:
    """
    Enhanced Activity Detector with Quantum-Inspired Probability
    
    Uses quantum superposition concepts to model activity uncertainty
    and transition probabilities between different activity states.
    """
    
    def __init__(self, history_size=20):
        """Initialize the enhanced activity detector"""
        self.speed_history = deque(maxlen=history_size)
        self.acceleration_history = deque(maxlen=history_size)
        self.activity_history = deque(maxlen=50)
        
        # Create logs directory
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        self.activity_log = self.log_dir / "activities_enhanced.json"
        
        # Activity thresholds (m/s)
        self.THRESHOLDS = {
            'STANDING': 0.5,
            'WALKING': 2.0,
            'RUNNING': 4.0,
            'BIKING': 8.0,
            'VEHICLE': 15.0
        }
        
        # Activity emojis
        self.EMOJIS = {
            'STANDING': '🧍',
            'WALKING_STEADY': '🚶',
            'WALKING_VARIED': '🚶‍♂️',
            'RUNNING': '🏃',
            'BIKING': '🚴',
            'VEHICLE': '🚗',
            'UNKNOWN': '❓'
        }
        
        # Quantum-inspired probability states
        self.activity_probabilities = {}
        
        print("✅ Enhanced Activity Detector initialized")
        print(f"   History size: {history_size}")
        print(f"   Log file: {self.activity_log}")
    
    def calculate_quantum_probability(self, speed, variance):
        """
        Calculate quantum-inspired probability distribution over activities
        
        Uses superposition concept: activity is in multiple states simultaneously
        until "measured" (classified)
        """
        probabilities = {}
        
        # Calculate probability for each activity state
        for activity, threshold in self.THRESHOLDS.items():
            # Gaussian probability centered at threshold
            prob = np.exp(-((speed - threshold) ** 2) / (2 * (variance + 0.1)))
            probabilities[activity] = prob
        
        # Normalize probabilities (quantum measurement collapse)
        total = sum(probabilities.values())
        if total > 0:
            probabilities = {k: v/total for k, v in probabilities.items()}
        
        return probabilities
    
    def detect_activity(self, speed, accuracy=None):
        """
        Detect current activity with quantum-inspired probability
        
        Args:
            speed: Current speed in m/s
            accuracy: GPS accuracy in meters (optional)
        
        Returns:
            dict: Activity classification with probabilities
        """
        try:
            # Add to history
            self.speed_history.append(speed)
            
            # Need minimum history
            if len(self.speed_history) < 5:
                return {
                    'activity': 'UNKNOWN',
                    'emoji': self.EMOJIS['UNKNOWN'],
                    'confidence': 0.0,
                    'speed': speed,
                    'probabilities': {}
                }
            
            # Calculate statistics
            avg_speed = np.mean(list(self.speed_history))
            speed_variance = np.var(list(self.speed_history))
            speed_std = np.std(list(self.speed_history))
            
            # Calculate quantum probabilities
            probabilities = self.calculate_quantum_probability(avg_speed, speed_variance)
            
            # Determine most likely activity
            activity = max(probabilities, key=probabilities.get)
            confidence = probabilities[activity]
            
            # Refine classification based on variance
            if activity == 'WALKING':
                if speed_variance < 0.5:
                    activity = 'WALKING_STEADY'
                else:
                    activity = 'WALKING_VARIED'
            
            # Get emoji
            emoji = self.EMOJIS.get(activity, '❓')
            
            # Create result
            result = {
                'activity': activity,
                'emoji': emoji,
                'confidence': float(confidence),
                'speed': float(speed),
                'avg_speed': float(avg_speed),
                'variance': float(speed_variance),
                'std_dev': float(speed_std),
                'probabilities': {k: float(v) for k, v in probabilities.items()},
                'timestamp': datetime.now().isoformat(),
                'accuracy': accuracy
            }
            
            # Add to history
            self.activity_history.append(result)
            
            # Log activity
            self._log_activity(result)
            
            return result
            
        except Exception as e:
            print(f"❌ Error detecting activity: {e}")
            return {
                'activity': 'ERROR',
                'emoji': '⚠️',
                'confidence': 0.0,
                'speed': speed,
                'error': str(e)
            }
    
    def predict_next_activity(self):
        """Predict next activity based on history patterns"""
        if len(self.activity_history) < 10:
            return None
        
        # Get recent activities
        recent = [a['activity'] for a in list(self.activity_history)[-10:]]
        
        # Count transitions
        transitions = {}
        for i in range(len(recent) - 1):
            current = recent[i]
            next_act = recent[i + 1]
            key = f"{current}->{next_act}"
            transitions[key] = transitions.get(key, 0) + 1
        
        # Find most common transition from current activity
        if recent:
            current = recent[-1]
            possible = {k: v for k, v in transitions.items() if k.startswith(current)}
            if possible:
                most_likely = max(possible, key=possible.get)
                predicted = most_likely.split('->')[1]
                confidence = possible[most_likely] / sum(possible.values())
                return {
                    'predicted': predicted,
                    'confidence': confidence,
                    'emoji': self.EMOJIS.get(predicted, '❓')
                }
        
        return None
    
    def detect_anomaly(self, speed):
        """Detect anomalous activity patterns"""
        if len(self.speed_history) < 10:
            return False
        
        # Calculate z-score
        mean = np.mean(list(self.speed_history))
        std = np.std(list(self.speed_history))
        
        if std > 0:
            z_score = abs((speed - mean) / std)
            return z_score > 3.0  # 3 sigma rule
        
        return False
    
    def get_activity_summary(self):
        """Get summary of recent activities"""
        if not self.activity_history:
            return "No activity data"
        
        recent = list(self.activity_history)[-20:]
        
        # Count activities
        counts = {}
        for activity in recent:
            act = activity['activity']
            counts[act] = counts.get(act, 0) + 1
        
        # Calculate percentages
        total = len(recent)
        summary = []
        for act, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            pct = (count / total) * 100
            emoji = self.EMOJIS.get(act, '❓')
            summary.append(f"{emoji} {act}: {pct:.1f}%")
        
        return "\n".join(summary)
    
    def _log_activity(self, result):
        """Log activity to file"""
        try:
            # Load existing log
            if self.activity_log.exists():
                with open(self.activity_log, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = []
            
            # Append new result
            log_data.append(result)
            
            # Keep only last 1000 entries
            log_data = log_data[-1000:]
            
            # Save
            with open(self.activity_log, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            print(f"⚠️  Warning: Could not log activity: {e}")
    
    def visualize_activity_distribution(self):
        """Create text-based visualization of activity distribution"""
        if not self.activity_history:
            return "No data to visualize"
        
        recent = list(self.activity_history)[-50:]
        
        # Count activities
        counts = {}
        for activity in recent:
            act = activity['activity']
            counts[act] = counts.get(act, 0) + 1
        
        # Create bar chart
        max_count = max(counts.values()) if counts else 1
        
        print("\n" + "="*60)
        print("📊 ACTIVITY DISTRIBUTION (Last 50 samples)")
        print("="*60)
        
        for act, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            emoji = self.EMOJIS.get(act, '❓')
            bar_length = int((count / max_count) * 40)
            bar = '█' * bar_length
            pct = (count / len(recent)) * 100
            print(f"{emoji} {act:20s} {bar:40s} {count:3d} ({pct:5.1f}%)")
        
        print("="*60 + "\n")


def demo_enhanced_detector():
    """Demonstrate the enhanced activity detector"""
    print("="*80)
    print("🚀 ENHANCED ACTIVITY DETECTOR DEMO")
    print("="*80)
    
    detector = ActivityDetectorEnhanced()
    
    # Simulate different activities
    print("\n📍 Simulating activity detection...\n")
    
    activities = [
        ("Standing still", 0.2, 10),
        ("Walking", 1.5, 15),
        ("Running", 3.5, 10),
        ("Biking", 6.0, 15),
        ("In vehicle", 12.0, 10),
    ]
    
    for activity_name, base_speed, samples in activities:
        print(f"\n{activity_name}:")
        print("-" * 40)
        
        for i in range(samples):
            # Add some noise
            speed = base_speed + np.random.normal(0, 0.3)
            speed = max(0, speed)  # No negative speeds
            
            result = detector.detect_activity(speed, accuracy=5.0)
            
            if i % 5 == 0:  # Print every 5th sample
                print(f"  {result['emoji']} {result['activity']:20s} "
                      f"Speed: {result['speed']:5.2f} m/s "
                      f"Confidence: {result['confidence']:5.1%}")
    
    # Show summary
    print("\n" + "="*80)
    print("📈 ACTIVITY SUMMARY")
    print("="*80)
    print(detector.get_activity_summary())
    
    # Show visualization
    detector.visualize_activity_distribution()
    
    # Predict next activity
    prediction = detector.predict_next_activity()
    if prediction:
        print(f"🔮 Predicted next activity: {prediction['emoji']} {prediction['predicted']} "
              f"(confidence: {prediction['confidence']:.1%})")
    
    print("\n" + "="*80)
    print("✅ DEMO COMPLETE!")
    print("="*80)


if __name__ == "__main__":
    demo_enhanced_detector()
