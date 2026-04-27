#!/usr/bin/env python3
"""
n3xion Camera (GrapheneOS Camera) Python Wrapper
"""
import subprocess
import json
import os
from datetime import datetime
from pathlib import Path

class N3xionCamera:
    def __init__(self):
        self.package_name = "app.grapheneos.camera"
        self.photo_activity = f"{self.package_name}/.ui.activities.CaptureActivity"
        self.video_activity = f"{self.package_name}/.ui.activities.VideoCaptureActivity"
        self.output_dir = Path("~/advancegeofencing/n3xion_captures").expanduser()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🎥 n3xion Camera (GrapheneOS) Initialized")
    
    def capture_photo(self, camera_id=0, metadata=None):
        """Capture photo using GrapheneOS camera"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"n3xion_photo_{timestamp}.jpg"
        
        try:
            subprocess.run([
                'am', 'start',
                '-n', self.photo_activity,
                '--ei', 'android.intent.extras.CAMERA_FACING', str(camera_id),
                '--es', 'output', str(filename)
            ], check=True)
            
            import time
            time.sleep(3)
            
            if metadata:
                metadata_file = filename.with_suffix('.json')
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
            
            print(f"📸 Photo: {filename}")
            return str(filename)
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def record_video(self, duration=10, camera_id=0, metadata=None):
        """Record video using GrapheneOS camera"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"n3xion_video_{timestamp}.mp4"
        
        try:
            subprocess.run([
                'am', 'start',
                '-n', self.video_activity,
                '--ei', 'android.intent.extras.CAMERA_FACING', str(camera_id),
                '--ei', 'android.intent.extras.DURATION_LIMIT', str(duration),
                '--es', 'output', str(filename)
            ], check=True)
            
            import time
            time.sleep(duration + 3)
            
            if metadata:
                metadata_file = filename.with_suffix('.json')
                metadata['duration'] = duration
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
            
            print(f"🎥 Video: {filename}")
            return str(filename)
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def dual_camera_capture(self, metadata=None):
        """Capture from both cameras"""
        back = self.capture_photo(camera_id=0, metadata=metadata)
        front = self.capture_photo(camera_id=1, metadata=metadata)
        
        return {
            'back_camera': back,
            'front_camera': front,
            'timestamp': datetime.now().isoformat()
        }

if __name__ == "__main__":
    camera = N3xionCamera()
    
    metadata = {
        'quantum_trigger': True,
        'location': {'lat': 40.7128, 'lon': -74.0060}
    }
    
    photo = camera.capture_photo(metadata=metadata)
    print(f"✅ Captured: {photo}")
