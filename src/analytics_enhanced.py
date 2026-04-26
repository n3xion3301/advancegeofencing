#!/usr/bin/env python3
"""
ENHANCED QUANTUM ANALYTICS
Real-time quantum system analytics with advanced visualization

ENHANCEMENTS:
- Real-time monitoring dashboard
- Statistical analysis and trends
- Performance metrics
- Export to multiple formats (JSON, CSV)
- Anomaly detection
- Predictive analytics
- Visual charts and graphs
"""

import json
import csv
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, deque
import warnings
warnings.filterwarnings('ignore')


class QuantumAnalyticsEnhanced:
    """
    Enhanced Quantum Analytics System
    
    Tracks, analyzes, and visualizes quantum system performance
    with real-time monitoring and predictive capabilities.
    """
    
    def __init__(self, history_size=1000):
        """
        Initialize analytics system
        
        Args:
            history_size: Maximum number of events to keep in memory
        """
        # Setup logging
        self.log_dir = Path("logs/quantum")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "analytics_enhanced.log"
        
        # Metrics tracking
        self.metrics = {
            'quantum_jumps': 0,
            'teleportations': 0,
            'superpositions': 0,
            'entanglements': 0,
            'wave_collapses': 0,
            'zones_tracked': 0,
            'measurements': 0,
            'circuit_executions': 0,
            'errors': 0
        }
        
        # Event history
        self.analytics_data = deque(maxlen=history_size)
        
        # Time-series data for trends
        self.time_series = defaultdict(list)
        
        # Performance metrics
        self.performance_metrics = {
            'avg_execution_time': [],
            'success_rate': [],
            'error_rate': []
        }
        
        # Anomaly detection
        self.anomaly_threshold = 3.0  # Standard deviations
        self.anomalies = []
        
        self.log("✅ Enhanced Quantum Analytics initialized")
        self.log(f"   History size: {history_size}")
    
    def log(self, msg):
        """Log message with timestamp"""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{ts}] {msg}"
        print(formatted)
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(formatted + "\n")
        except Exception as e:
            print(f"⚠️  Logging error: {e}")
    
    def track_event(self, event_type, details=None, execution_time=None):
        """
        Track quantum event with enhanced metadata
        
        Args:
            event_type: Type of event
            details: Additional event details
            execution_time: Time taken to execute (seconds)
        """
        # Update metrics
        if event_type in self.metrics:
            self.metrics[event_type] += 1
        
        # Create event record
        event = {
            'type': event_type,
            'details': details or {},
            'timestamp': datetime.now().isoformat(),
            'execution_time': execution_time
        }
        
        # Add to history
        self.analytics_data.append(event)
        
        # Update time series
        hour = datetime.now().hour
        self.time_series[event_type].append({
            'hour': hour,
            'timestamp': datetime.now().isoformat()
        })
        
        # Track performance
        if execution_time is not None:
            self.performance_metrics['avg_execution_time'].append(execution_time)
        
        # Check for anomalies
        if execution_time is not None:
            self._check_anomaly(event_type, execution_time)
        
        self.log(f"📊 Tracked: {event_type}")
        
        return event
    
    def _check_anomaly(self, event_type, value):
        """Detect anomalous events using statistical analysis"""
        recent_values = [
            e.get('execution_time', 0) 
            for e in self.analytics_data 
            if e['type'] == event_type and e.get('execution_time') is not None
        ]
        
        if len(recent_values) < 10:
            return False
        
        mean = np.mean(recent_values)
        std = np.std(recent_values)
        
        if std > 0:
            z_score = abs((value - mean) / std)
            
            if z_score > self.anomaly_threshold:
                anomaly = {
                    'event_type': event_type,
                    'value': value,
                    'mean': mean,
                    'std': std,
                    'z_score': z_score,
                    'timestamp': datetime.now().isoformat()
                }
                self.anomalies.append(anomaly)
                self.log(f"⚠️  ANOMALY DETECTED: {event_type} (z-score: {z_score:.2f})")
                return True
        
        return False
    
    def get_metrics(self):
        """Get current metrics summary"""
        total_events = sum(self.metrics.values())
        
        summary = {
            'total_events': total_events,
            'metrics': self.metrics.copy(),
            'events_in_history': len(self.analytics_data),
            'anomalies_detected': len(self.anomalies)
        }
        
        # Calculate rates
        if self.performance_metrics['avg_execution_time']:
            summary['avg_execution_time'] = np.mean(
                self.performance_metrics['avg_execution_time']
            )
        
        return summary
    
    def get_trends(self, event_type=None, hours=24):
        """
        Analyze trends over time
        
        Args:
            event_type: Specific event type or None for all
            hours: Number of hours to analyze
        
        Returns:
            dict: Trend analysis
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        if event_type:
            events = [
                e for e in self.analytics_data 
                if e['type'] == event_type and 
                datetime.fromisoformat(e['timestamp']) > cutoff_time
            ]
        else:
            events = [
                e for e in self.analytics_data 
                if datetime.fromisoformat(e['timestamp']) > cutoff_time
            ]
        
        if not events:
            return {'error': 'No events in time range'}
        
        # Count by hour
        hourly_counts = defaultdict(int)
        for event in events:
            hour = datetime.fromisoformat(event['timestamp']).hour
            hourly_counts[hour] += 1
        
        # Calculate trend
        hours_list = sorted(hourly_counts.keys())
        counts_list = [hourly_counts[h] for h in hours_list]
        
        if len(counts_list) > 1:
            # Simple linear regression
            x = np.array(range(len(counts_list)))
            y = np.array(counts_list)
            slope = np.polyfit(x, y, 1)[0]
            trend = 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable'
        else:
            trend = 'insufficient_data'
        
        return {
            'event_type': event_type or 'all',
            'time_range_hours': hours,
            'total_events': len(events),
            'hourly_distribution': dict(hourly_counts),
            'trend': trend,
            'avg_per_hour': len(events) / hours
        }
    
    def get_performance_report(self):
        """Generate comprehensive performance report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'metrics': self.get_metrics(),
            'performance': {}
        }
        
        # Execution time statistics
        if self.performance_metrics['avg_execution_time']:
            exec_times = self.performance_metrics['avg_execution_time']
            report['performance']['execution_time'] = {
                'mean': float(np.mean(exec_times)),
                'median': float(np.median(exec_times)),
                'std': float(np.std(exec_times)),
                'min': float(np.min(exec_times)),
                'max': float(np.max(exec_times))
            }
        
        # Event type distribution
        event_counts = defaultdict(int)
        for event in self.analytics_data:
            event_counts[event['type']] += 1
        
        report['event_distribution'] = dict(event_counts)
        
        # Recent anomalies
        report['recent_anomalies'] = self.anomalies[-10:]
        
        return report
    
    def export_to_json(self, filename=None):
        """Export analytics data to JSON"""
        if filename is None:
            filename = self.log_dir / f"analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'metrics': self.metrics,
            'events': list(self.analytics_data),
            'anomalies': self.anomalies,
            'performance_report': self.get_performance_report()
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        self.log(f"💾 Exported to: {filename}")
        return filename
    
    def export_to_csv(self, filename=None):
        """Export events to CSV"""
        if filename is None:
            filename = self.log_dir / f"analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='') as f:
            if self.analytics_data:
                # Get all possible fields
                fieldnames = set()
                for event in self.analytics_data:
                    fieldnames.update(event.keys())
                    if 'details' in event and isinstance(event['details'], dict):
                        fieldnames.update(event['details'].keys())
                
                fieldnames = sorted(fieldnames)
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for event in self.analytics_data:
                    row = event.copy()
                    if 'details' in row and isinstance(row['details'], dict):
                        row.update(row['details'])
                        del row['details']
                    writer.writerow(row)
        
        self.log(f"💾 Exported to CSV: {filename}")
        return filename
    
    def visualize_metrics(self):
        """Create text-based visualization of metrics"""
        print("\n" + "="*80)
        print("📊 QUANTUM ANALYTICS DASHBOARD")
        print("="*80)
        
        # Metrics overview
        print("\n📈 METRICS OVERVIEW")
        print("-" * 80)
        
        max_count = max(self.metrics.values()) if self.metrics.values() else 1
        
        for metric, count in sorted(self.metrics.items(), key=lambda x: x[1], reverse=True):
            bar_length = int((count / max_count) * 50) if max_count > 0 else 0
            bar = '█' * bar_length
            print(f"{metric:25s} {bar:50s} {count:6d}")
        
        # Performance metrics
        if self.performance_metrics['avg_execution_time']:
            print("\n⚡ PERFORMANCE METRICS")
            print("-" * 80)
            exec_times = self.performance_metrics['avg_execution_time']
            print(f"Average Execution Time: {np.mean(exec_times):.4f}s")
            print(f"Median Execution Time:  {np.median(exec_times):.4f}s")
            print(f"Min Execution Time:     {np.min(exec_times):.4f}s")
            print(f"Max Execution Time:     {np.max(exec_times):.4f}s")
        
        # Recent anomalies
        if self.anomalies:
            print("\n⚠️  RECENT ANOMALIES")
            print("-" * 80)
            for anomaly in self.anomalies[-5:]:
                print(f"  {anomaly['event_type']}: z-score={anomaly['z_score']:.2f}")
        
        print("\n" + "="*80 + "\n")
    
    def reset_metrics(self):
        """Reset all metrics and data"""
        self.metrics = {k: 0 for k in self.metrics}
        self.analytics_data.clear()
        self.time_series.clear()
        self.performance_metrics = {k: [] for k in self.performance_metrics}
        self.anomalies.clear()
        
        self.log("🔄 Metrics reset")


def demo_enhanced_analytics():
    """Demonstrate enhanced quantum analytics"""
    print("="*80)
    print("📊 ENHANCED QUANTUM ANALYTICS DEMO")
    print("="*80)
    
    # Initialize analytics
    analytics = QuantumAnalyticsEnhanced()
    
    # Simulate various quantum events
    print("\n📍 Simulating quantum events...")
    
    events = [
        ('quantum_jumps', 0.05),
        ('teleportations', 0.12),
        ('superpositions', 0.03),
        ('entanglements', 0.08),
        ('wave_collapses', 0.04),
        ('measurements', 0.02),
        ('circuit_executions', 0.15),
    ]
    
    for i in range(50):
        event_type, base_time = events[i % len(events)]
        # Add some randomness
        exec_time = base_time + np.random.normal(0, 0.01)
        exec_time = max(0.001, exec_time)  # Ensure positive
        
        analytics.track_event(
            event_type,
            details={'iteration': i},
            execution_time=exec_time
        )
    
    # Add an anomaly
    analytics.track_event('teleportations', execution_time=0.5)  # Unusually slow
    
    # Show dashboard
    analytics.visualize_metrics()
    
    # Get trends
    print("📈 Trend Analysis (Last 24 hours)")
    print("-" * 80)
    trends = analytics.get_trends('teleportations', hours=24)
    for key, value in trends.items():
        print(f"  {key}: {value}")
    
    # Performance report
    print("\n📊 Performance Report")
    print("-" * 80)
    report = analytics.get_performance_report()
    print(f"Total Events: {report['metrics']['total_events']}")
    if 'execution_time' in report['performance']:
        perf = report['performance']['execution_time']
        print(f"Avg Execution Time: {perf['mean']:.4f}s")
        print(f"Std Deviation: {perf['std']:.4f}s")
    
    # Export data
    print("\n💾 Exporting Data")
    print("-" * 80)
    json_file = analytics.export_to_json()
    csv_file = analytics.export_to_csv()
    print(f"JSON: {json_file}")
    print(f"CSV: {csv_file}")
    
    print("\n" + "="*80)
    print("✅ DEMO COMPLETE!")
    print("="*80)


if __name__ == "__main__":
    demo_enhanced_analytics()
