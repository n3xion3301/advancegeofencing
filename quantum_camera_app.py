#!/usr/bin/env python3
"""
Quantum Camera App for Android (Termux)
Real-time quantum manifestation detection
"""

import subprocess
import time
import cv2
import numpy as np
from pathlib import Path
import sys
sys.path.append('src')
from quantum_camera_detector import QuantumCameraDetector

class QuantumCameraApp:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.detector = QuantumCameraDetector()
        self.temp_photo = "temp_quantum_frame.jpg"
        self.running = False
        
    def capture_frame(self):
        """Capture frame using termux-camera-photo"""
        try:
            # Capture photo
            subprocess.run([
                'termux-camera-photo',
                '-c', str(self.camera_id),
                self.temp_photo
            ], check=True, capture_output=True)
            
            # Read the image
            frame = cv2.imread(self.temp_photo)
            return frame
        except Exception as e:
            print(f"❌ Camera capture error: {e}")
            return None
    
    def run_detection_loop(self, interval=2.0):
        """Run continuous quantum detection"""
        print("\n" + "="*60)
        print("⚛️  QUANTUM CAMERA DETECTOR ACTIVE  ⚛️")
        print("="*60)
        print(f"Camera ID: {self.camera_id}")
        print(f"Detection threshold: {self.detector.detection_threshold}")
        print(f"Capture interval: {interval}s")
        print("\nPress Ctrl+C to stop\n")
        
        self.running = True
        frame_count = 0
        quantum_detections = 0
        
        try:
            while self.running:
                frame_count += 1
                print(f"\n📷 Frame {frame_count} - Capturing...")
                
                # Capture frame
                frame = self.capture_frame()
                
                if frame is not None:
                    # Analyze for quantum signatures
                    quantum_score, signatures = self.detector.analyze_frame(frame)
                    
                    # Display results
                    self.display_results(quantum_score, signatures)
                    
                    # Save if quantum detected
                    if quantum_score > self.detector.detection_threshold:
                        quantum_detections += 1
                        print(f"\n🎉 QUANTUM MANIFESTATION DETECTED! 🎉")
                        self.detector.save_quantum_event(frame, quantum_score, signatures)
                    
                    # Stats
                    detection_rate = (quantum_detections / frame_count) * 100
                    print(f"\n📊 Stats: {quantum_detections}/{frame_count} quantum events ({detection_rate:.1f}%)")
                
                # Wait before next capture
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n⚛️ Quantum detection stopped by user")
            self.running = False
        
        # Final stats
        print("\n" + "="*60)
        print("FINAL STATISTICS")
        print("="*60)
        print(f"Total frames analyzed: {frame_count}")
        print(f"Quantum events detected: {quantum_detections}")
        print(f"Detection rate: {(quantum_detections/frame_count)*100:.1f}%")
        print("="*60)
    
    def display_results(self, quantum_score, signatures):
        """Display detection results in terminal"""
        print("\n" + "─"*60)
        print(f"⚛️  QUANTUM SCORE: {quantum_score:.3f}")
        print("─"*60)
        
        # Visual bar
        bar_length = 50
        filled = int(bar_length * quantum_score)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        if quantum_score < 0.3:
            color = "\033[94m"  # Blue
            status = "LOW"
        elif quantum_score < 0.7:
            color = "\033[93m"  # Yellow
            status = "MEDIUM"
        else:
            color = "\033[91m"  # Red
            status = "HIGH"
        
        print(f"{color}[{bar}] {status}\033[0m")
        
        # Signatures detected
        if signatures:
            print("\n✓ Quantum Signatures Detected:")
            for sig in signatures:
                print(f"  • {sig}")
        else:
            print("\n○ No quantum signatures detected")
        
        print("─"*60)
    
    def single_shot_detection(self):
        """Capture and analyze single frame"""
        print("\n⚛️ Single-shot quantum detection...")
        
        frame = self.capture_frame()
        if frame is not None:
            quantum_score, signatures = self.detector.analyze_frame(frame)
            self.display_results(quantum_score, signatures)
            
            if quantum_score > self.detector.detection_threshold:
                print("\n🎉 QUANTUM DETECTED!")
                self.detector.save_quantum_event(frame, quantum_score, signatures)
            
            return quantum_score, signatures
        return 0.0, []

def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        ⚛️  QUANTUM CAMERA DETECTOR v1.0  ⚛️               ║
║                                                           ║
║     Detect quantum manifestations in real-time!          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Choose mode
    print("\nSelect mode:")
    print("1. Continuous detection (recommended)")
    print("2. Single-shot detection")
    print("3. Burst mode (5 rapid captures)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    # Choose camera
    print("\nSelect camera:")
    print("0. Back camera")
    print("1. Front camera")
    camera_id = int(input("Enter camera ID (0-1): ").strip() or "0")
    
    app = QuantumCameraApp(camera_id=camera_id)
    
    if choice == "1":
        interval = float(input("Capture interval in seconds (default 2.0): ").strip() or "2.0")
        app.run_detection_loop(interval=interval)
    
    elif choice == "2":
        app.single_shot_detection()
    
    elif choice == "3":
        print("\n⚡ Burst mode: 5 rapid captures")
        for i in range(5):
            print(f"\nCapture {i+1}/5...")
            app.single_shot_detection()
            time.sleep(0.5)
    
    print("\n✨ Quantum detection complete! ✨\n")

if __name__ == "__main__":
    main()
