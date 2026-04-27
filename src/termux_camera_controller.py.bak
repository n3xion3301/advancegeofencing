import subprocess
import datetime
import time
import os
from pathlib import Path

class TermuxCameraController:
    def __init__(self, camera_id=0, output_dir='recordings'):
        self.camera_id = camera_id
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.camera_available = self._check_camera_available()
        
    def _check_camera_available(self):
        """Check if Termux camera API is available"""
        try:
            result = subprocess.run(
                ['termux-camera-info'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print("✅ Camera API available")
                return True
            return False
        except Exception as e:
            print(f"⚠️  Camera API not available: {e}")
            return False
    
    def take_photo(self, filename=None):
        """Take a single photo"""
        if not self.camera_available:
            print("❌ Camera not available")
            return None
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        if not filename:
            filename = self.output_dir / f'breach_photo_{timestamp}.jpg'
        
        try:
            result = subprocess.run(
                ['termux-camera-photo', '-c', str(self.camera_id), str(filename)],
                capture_output=True,
                timeout=10
            )
            
            if result.returncode == 0 and os.path.exists(filename):
                file_size = os.path.getsize(filename) / 1024
                print(f"📸 Photo saved: {filename} ({file_size:.1f} KB)")
                return str(filename)
            else:
                print(f"❌ Photo failed: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Photo error: {e}")
            return None
    
    def take_burst_photos(self, count=3, interval=1):
        """Take multiple photos in sequence"""
        photos = []
        
        print(f"📸 Taking {count} photos with {interval}s interval...")
        
        for i in range(count):
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            filename = self.output_dir / f'breach_burst_{timestamp}.jpg'
            
            photo = self.take_photo(filename)
            if photo:
                photos.append(photo)
            
            if i < count - 1:
                time.sleep(interval)
        
        print(f"✅ Captured {len(photos)}/{count} photos")
        return photos
    
    def start_recording(self, duration_seconds=30):
        """Main recording method - takes burst photos"""
        if not self.camera_available:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            placeholder = self.output_dir / f'breach_{timestamp}.txt'
            with open(placeholder, 'w') as f:
                f.write(f"Breach detected at {datetime.datetime.now()}\n")
                f.write("Camera recording unavailable\n")
            print(f"📝 Breach logged: {placeholder}")
            return str(placeholder)
        
        results = {
            'photos': [],
            'timestamp': datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        }
        
        # Take burst photos
        print("📸 Taking burst photos...")
        results['photos'] = self.take_burst_photos(count=5, interval=2)
        
        return results
