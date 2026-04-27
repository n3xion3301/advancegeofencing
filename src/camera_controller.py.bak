import datetime
import os
from pathlib import Path

# Try to import OpenCV, but don't fail if it's not available
OPENCV_AVAILABLE = False
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    pass

class CameraController:
    def __init__(self, camera_index=0, output_dir='recordings'):
        self.camera_index = camera_index
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.is_recording = False
        self.video_writer = None
        self.opencv_available = OPENCV_AVAILABLE
        
        if not self.opencv_available:
            print("⚠️  OpenCV not available - camera features disabled")
        
    def start_recording(self, duration_seconds=30):
        """Start camera recording for specified duration"""
        if not self.opencv_available:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            placeholder = self.output_dir / f'breach_{timestamp}.txt'
            
            with open(placeholder, 'w') as f:
                f.write(f"Breach detected at {datetime.datetime.now()}\n")
                f.write("Camera recording unavailable (OpenCV not installed)\n")
            
            print(f"📝 Breach logged: {placeholder}")
            return str(placeholder)
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.output_dir / f'breach_{timestamp}.mp4'
        
        try:
            cap = cv2.VideoCapture(self.camera_index)
            
            if not cap.isOpened():
                print("❌ Camera not accessible")
                return None
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = 20.0
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            self.video_writer = cv2.VideoWriter(
                str(filename), fourcc, fps, (frame_width, frame_height)
            )
            
            self.is_recording = True
            start_time = datetime.datetime.now()
            
            print(f"🎥 Recording started: {filename}")
            
            while (datetime.datetime.now() - start_time).seconds < duration_seconds:
                ret, frame = cap.read()
                if ret:
                    timestamp_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cv2.putText(frame, timestamp_text, (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    self.video_writer.write(frame)
                else:
                    break
            
            self.stop_recording()
            cap.release()
            return str(filename)
            
        except Exception as e:
            print(f"❌ Recording error: {e}")
            return None
    
    def stop_recording(self):
        """Stop current recording"""
        if self.video_writer:
            self.video_writer.release()
            self.is_recording = False
            print("⏹️  Recording stopped")
