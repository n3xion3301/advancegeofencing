import subprocess
import time

class HomeVideoRecorder:
    def __init__(self):
        pass
    
    def record_breach_moment(self):
        """Open camera app for manual recording"""
        print("📸 Opening camera app...")
        
        try:
            # Open Android camera app
            subprocess.run([
                'am', 'start', 
                '-a', 'app.grapheneos.camera/.ui.activities.VideoCaptureActivity'
            ])
            
            print("✅ Camera app opened - Press the red button!")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
