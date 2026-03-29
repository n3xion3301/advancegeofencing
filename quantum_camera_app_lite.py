#!/usr/bin/env python3
"""
Quantum Camera App LITE - No OpenCV dependencies
Uses PIL/Pillow for image processing
"""

import subprocess
import time
import numpy as np
from PIL import Image
from datetime import datetime
import json
import os
from pathlib import Path

class QuantumCameraDetectorLite:
    def __init__(self):
        self.detection_threshold = 0.7
        
    def analyze_frame(self, image_path):
        """Analyze image for quantum signatures using PIL"""
        img = Image.open(image_path)
        img_array = np.array(img)
        
        quantum_score = 0.0
        signatures = []
        
        # Convert to grayscale
        if len(img_array.shape) == 3:
            gray = np.mean(img_array, axis=2).astype(np.uint8)
        else:
            gray = img_array
        
        # 1. INTERFERENCE PATTERNS (FFT analysis)
        interference = self.detect_interference(gray)
        if interference > 0.5:
            quantum_score += 0.3
            signatures.append("interference_pattern")
        
        # 2. ENTANGLEMENT (pixel correlations)
        entanglement = self.detect_entanglement(img_array)
        if entanglement > 0.6:
            quantum_score += 0.25
            signatures.append("entanglement_correlation")
        
        # 3. SUPERPOSITION (color diversity)
        superposition = self.detect_superposition(img_array)
        if superposition > 0.5:
            quantum_score += 0.2
            signatures.append("superposition_state")
        
        # 4. TUNNELING (sharp transitions)
        tunneling = self.detect_tunneling(gray)
        if tunneling > 0.4:
            quantum_score += 0.15
            signatures.append("tunneling_event")
        
        # 5. WAVE-PARTICLE DUALITY
        duality = self.detect_duality(gray)
        if duality > 0.5:
            quantum_score += 0.1
            signatures.append("wave_particle_duality")
        
        return quantum_score, signatures
    
    def detect_interference(self, gray):
        """Detect interference patterns using FFT"""
        f_transform = np.fft.fft2(gray)
        f_shift = np.fft.fftshift(f_transform)
        magnitude = np.abs(f_shift)
        
        threshold = np.mean(magnitude) + 2 * np.std(magnitude)
        peaks = np.sum(magnitude > threshold)
        
        return min(peaks / 100.0, 1.0)
    
    def detect_entanglement(self, img_array):
        """Detect correlations between image regions"""
        h, w = img_array.shape[:2]
        
        q1 = img_array[0:h//2, 0:w//2].flatten()
        q2 = img_array[0:h//2, w//2:w].flatten()
        q3 = img_array[h//2:h, 0:w//2].flatten()
        q4 = img_array[h//2:h, w//2:w].flatten()
        
        corr_12 = np.corrcoef(q1, q2)[0, 1]
        corr_34 = np.corrcoef(q3, q4)[0, 1]
        
        return np.mean([abs(corr_12), abs(corr_34)])
    
    def detect_superposition(self, img_array):
        """Detect multiple dominant states (colors)"""
        if len(img_array.shape) == 3:
            # Count unique colors
            unique_colors = len(np.unique(img_array.reshape(-1, img_array.shape[2]), axis=0))
            score = min(unique_colors / 1000.0, 1.0)
        else:
            # Grayscale - check histogram spread
            hist, _ = np.histogram(img_array, bins=50)
            peaks = np.sum(hist > np.max(hist) * 0.1)
            score = min(peaks / 10.0, 1.0)
        
        return score
    
    def detect_tunneling(self, gray):
        """Detect sharp transitions"""
        # Simple gradient using numpy
        grad_x = np.abs(np.diff(gray, axis=1))
        grad_y = np.abs(np.diff(gray, axis=0))
        
        threshold = np.mean(grad_x) + np.std(grad_x)
        tunneling_pixels = np.sum(grad_x > threshold)
        
        return min(tunneling_pixels / (gray.size * 0.1), 1.0)
    
    def detect_duality(self, gray):
        """Detect wave-particle duality"""
        # Edge density
        grad_x = np.abs(np.diff(gray, axis=1))
        edge_density = np.sum(grad_x > 50) / gray.size
        
        # Smoothness
        variance = np.var(gray)
        
        return min(edge_density * variance / 1000, 1.0)
    
    def save_quantum_event(self, image_path, quantum_score, signatures):
        """Save detected quantum event"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        os.makedirs("quantum_detections", exist_ok=True)
        
        # Copy image
        img = Image.open(image_path)
        filename = f"quantum_detections/quantum_{timestamp}.jpg"
        img.save(filename)
        
        # Save metadata
        metadata = {
            "timestamp": timestamp,
            "quantum_score": float(quantum_score),
            "signatures": signatures,
            "threshold": self.detection_threshold
        }
        
        json_file = f"quantum_detections/quantum_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"⚛️ Quantum event saved: {filename}")
        return filename

class QuantumCameraAppLite:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.detector = QuantumCameraDetectorLite()
        self.temp_photo = "temp_quantum_frame.jpg"
        self.running = False
        
    def capture_frame(self):
        """Capture frame using termux-camera-photo"""
        try:
            subprocess.run([
                'termux-camera-photo',
                '-c', str(self.camera_id),
                self.temp_photo
            ], check=True, capture_output=True)
            
            return self.temp_photo
        except Exception as e:
            print(f"❌ Camera capture error: {e}")
            return None
    
    def run_detection_loop(self, interval=2.0):
        """Run continuous quantum detection"""
        print("\n" + "="*60)
        print("⚛️  QUANTUM CAMERA DETECTOR LITE ACTIVE  ⚛️")
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
                
                image_path = self.capture_frame()
                
                if image_path:
                    quantum_score, signatures = self.detector.analyze_frame(image_path)
                    
                    self.display_results(quantum_score, signatures)
                    
                    if quantum_score > self.detector.detection_threshold:
                        quantum_detections += 1
                        print(f"\n🎉 QUANTUM MANIFESTATION DETECTED! 🎉")
                        self.detector.save_quantum_event(image_path, quantum_score, signatures)
                    
                    detection_rate = (quantum_detections / frame_count) * 100
                    print(f"\n📊 Stats: {quantum_detections}/{frame_count} quantum events ({detection_rate:.1f}%)")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n⚛️ Quantum detection stopped by user")
            self.running = False
        
        print("\n" + "="*60)
        print("FINAL STATISTICS")
        print("="*60)
        print(f"Total frames: {frame_count}")
        print(f"Quantum events: {quantum_detections}")
        print(f"Detection rate: {(quantum_detections/frame_count)*100:.1f}%")
        print("="*60)
    
    def display_results(self, quantum_score, signatures):
        """Display detection results"""
        print("\n" + "─"*60)
        print(f"⚛️  QUANTUM SCORE: {quantum_score:.3f}")
        print("─"*60)
        
        bar_length = 50
        filled = int(bar_length * quantum_score)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        if quantum_score < 0.3:
            color = "\033[94m"
            status = "LOW"
        elif quantum_score < 0.7:
            color = "\033[93m"
            status = "MEDIUM"
        else:
            color = "\033[91m"
            status = "HIGH"
        
        print(f"{color}[{bar}] {status}\033[0m")
        
        if signatures:
            print("\n✓ Quantum Signatures:")
            for sig in signatures:
                print(f"  • {sig}")
        else:
            print("\n○ No quantum signatures")
        
        print("─"*60)

def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║      ⚛️  QUANTUM CAMERA DETECTOR LITE v1.0  ⚛️            ║
║                                                           ║
║     Detect quantum manifestations in real-time!          ║
║              (Lightweight - No OpenCV!)                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    print("\nSelect mode:")
    print("1. Continuous detection")
    print("2. Single-shot")
    print("3. Burst mode (5 captures)")
    
    choice = input("\nChoice (1-3): ").strip() or "1"
    
    print("\nCamera:")
    print("0. Back camera")
    print("1. Front camera")
    camera_id = int(input("Camera ID (0-1): ").strip() or "0")
    
    app = QuantumCameraAppLite(camera_id=camera_id)
    
    if choice == "1":
        interval = float(input("Interval (seconds, default 2.0): ").strip() or "2.0")
        app.run_detection_loop(interval=interval)
    elif choice == "2":
        image_path = app.capture_frame()
        if image_path:
            score, sigs = app.detector.analyze_frame(image_path)
            app.display_results(score, sigs)
    elif choice == "3":
        for i in range(5):
            print(f"\nCapture {i+1}/5...")
            image_path = app.capture_frame()
            if image_path:
                score, sigs = app.detector.analyze_frame(image_path)
                app.display_results(score, sigs)
            time.sleep(0.5)
    
    print("\n✨ Complete! ✨\n")

if __name__ == "__main__":
    main()
