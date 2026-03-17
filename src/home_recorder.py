import time
from pathlib import Path
import sys
sys.path.insert(0, '/data/data/com.termux/files/home/advancegeofencing/src')
from termux_camera_controller import TermuxCameraController

class HomeRecorder:
    def __init__(self):
        self.camera = TermuxCameraController(output_dir='quantum_world')
        Path('quantum_world').mkdir(exist_ok=True)
    
    def capture_quantum_moment(self):
        """Capture a photo of your quantum world"""
        if self.camera.camera_available:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f'quantum_world/parallel_{timestamp}.jpg'
            photo = self.camera.take_photo(filename)
            return photo
        return None
