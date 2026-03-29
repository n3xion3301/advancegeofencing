#!/usr/bin/env python3
"""
INTEGRATED Quantum Camera + Visualizer
Camera detects → Full physics visualization!
"""

import subprocess
import time
import numpy as np
from PIL import Image
from datetime import datetime
import json
import os
import sys

sys.path.append('src')

from camera_visualizer_bridge import CameraVisualizerBridge
from quantum_visualizer import QuantumVisualizer

class IntegratedQuantumSystem:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.bridge = CameraVisualizerBridge()
        self.visualizer = QuantumVisualizer()
        self.temp_photo = "temp_quantum_frame.jpg"
        self.detection_threshold = 0.7
        
    def strip_exif(self, image_path):
        """Strip EXIF data"""
        try:
            subprocess.run([
                'exiftool',
                '-all=',
                '-overwrite_original',
                image_path
            ], check=True, capture_output=True)
            return True
        except:
            return False
    
    def capture_frame(self):
        """Capture and strip EXIF"""
        try:
            subprocess.run([
                'termux-camera-photo',
                '-c', str(self.camera_id),
                self.temp_photo
            ], check=True, capture_output=True)
            
            self.strip_exif(self.temp_photo)
            return self.temp_photo
        except Exception as e:
            print(f"❌ Capture error: {e}")
            return None
    
    def analyze_frame(self, image_path):
        """Analyze for quantum signatures"""
        img = Image.open(image_path)
        img_array = np.array(img)
        
        quantum_score = 0.0
        signatures = []
        
        if len(img_array.shape) == 3:
            gray = np.mean(img_array, axis=2).astype(np.uint8)
        else:
            gray = img_array
        
        # Detection algorithms
        interference = self.detect_interference(gray)
        if interference > 0.5:
            quantum_score += 0.3
            signatures.append("interference_pattern")
        
        entanglement = self.detect_entanglement(img_array)
        if entanglement > 0.6:
            quantum_score += 0.25
            signatures.append("entanglement_correlation")
        
        superposition = self.detect_superposition(img_array)
        if superposition > 0.5:
            quantum_score += 0.2
            signatures.append("superposition_state")
        
        tunneling = self.detect_tunneling(gray)
        if tunneling > 0.4:
            quantum_score += 0.15
            signatures.append("tunneling_event")
        
        duality = self.detect_duality(gray)
        if duality > 0.5:
            quantum_score += 0.1
            signatures.append("wave_particle_duality")
        
        return quantum_score, signatures
    
    def detect_interference(self, gray):
        f_transform = np.fft.fft2(gray)
        f_shift = np.fft.fftshift(f_transform)
        magnitude = np.abs(f_shift)
        threshold = np.mean(magnitude) + 2 * np.std(magnitude)
        peaks = np.sum(magnitude > threshold)
        return min(peaks / 100.0, 1.0)
    
    def detect_entanglement(self, img_array):
        h, w = img_array.shape[:2]
        q1 = img_array[0:h//2, 0:w//2].flatten()
        q2 = img_array[0:h//2, w//2:w].flatten()
        corr = np.corrcoef(q1, q2)[0, 1]
        return abs(corr)
    
    def detect_superposition(self, img_array):
        if len(img_array.shape) == 3:
            unique = len(np.unique(img_array.reshape(-1, img_array.shape[2]), axis=0))
            return min(unique / 1000.0, 1.0)
        return 0.5
    
    def detect_tunneling(self, gray):
        grad_x = np.abs(np.diff(gray, axis=1))
        threshold = np.mean(grad_x) + np.std(grad_x)
        tunneling = np.sum(grad_x > threshold)
        return min(tunneling / (gray.size * 0.1), 1.0)
    
    def detect_duality(self, gray):
        grad_x = np.abs(np.diff(gray, axis=1))
        edge_density = np.sum(grad_x > 50) / gray.size
        variance = np.var(gray)
        return min(edge_density * variance / 1000, 1.0)

    
    def run_integrated_detection(self, show_all=False):
        """Run detection with full visualization"""
        print("\n" + "="*60)
        print("⚛️📷 INTEGRATED QUANTUM SYSTEM ACTIVE 📷⚛️")
        print("="*60)
        print("Camera → Detection → Full Visualization!")
        print(f"Camera ID: {self.camera_id}")
        print(f"Threshold: {self.detection_threshold}")
        print(f"Show all visualizations: {show_all}")
        print("\nPress Ctrl+C to stop\n")
        
        detection_count = 0
        
        try:
            while True:
                detection_count += 1
                print(f"\n📷 Detection #{detection_count} - Capturing...")
                
                image_path = self.capture_frame()
                
                if image_path:
                    quantum_score, signatures = self.analyze_frame(image_path)
                    
                    self.display_score(quantum_score, signatures)
                    
                    if quantum_score > self.detection_threshold or show_all:
                        print("\n🎉 TRIGGERING FULL VISUALIZATION! 🎉\n")
                        
                        entity = self.bridge.create_entity_from_detection(
                            quantum_score, signatures, image_path
                        )
                        
                        viz_list = self.bridge.get_visualization_list(signatures)
                        
                        self.show_visualizations(entity, viz_list, show_all)
                        
                        self.save_detection(image_path, quantum_score, signatures, entity)
                    
                    else:
                        print(f"\n📊 Score {quantum_score:.3f} below threshold")
                
                time.sleep(2.0)
                
        except KeyboardInterrupt:
            print("\n\n⚛️ System stopped")
            print(f"Total detections: {detection_count}")
    
    def display_score(self, score, signatures):
        """Display quantum score"""
        print("\n" + "─"*60)
        print(f"⚛️ QUANTUM SCORE: {score:.3f}")
        
        bar_length = 50
        filled = int(bar_length * score)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        if score < 0.3:
            status = "LOW"
        elif score < 0.7:
            status = "MEDIUM"
        else:
            status = "HIGH ⚡"
        
        print(f"[{bar}] {status}")
        
        if signatures:
            print("\n✓ Signatures:")
            for sig in signatures:
                print(f"  • {sig}")
        print("─"*60)
    
    def show_visualizations(self, entity, viz_list, show_all=False):
        """Show quantum visualizations"""
        print("\n" + "╔" + "═"*58 + "╗")
        print("║" + " "*15 + "🌌 QUANTUM VISUALIZATIONS 🌌" + " "*15 + "║")
        print("╚" + "═"*58 + "╝\n")
        
        if show_all:
            print("🔥 SHOWING MULTIPLE VISUALIZATIONS! 🔥\n")
            
            self.visualizer.quantum_state(entity)
            self.visualizer.wave_function(entity)
            self.visualizer.superposition(entity)
            self.visualizer.quantum_entanglement(entity)
            self.visualizer.quantum_tunneling(entity)
            self.visualizer.double_slit_experiment(entity)
            
            print("\n✨ Showing 6 core visualizations...")
            
        else:
            print(f"📊 Showing {len(viz_list)} relevant visualizations:\n")
            
            for viz_name in viz_list[:5]:
                if hasattr(self.visualizer, viz_name):
                    method = getattr(self.visualizer, viz_name)
                    method(entity)
    
    def save_detection(self, image_path, score, signatures, entity):
        """Save detection with privacy"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        os.makedirs("quantum_integrated", exist_ok=True)
        
        img = Image.open(image_path)
        filename = f"quantum_integrated/quantum_{timestamp}.jpg"
        img.save(filename, "JPEG", quality=95, exif=b'')
        self.strip_exif(filename)
        
        data = {
            "timestamp": timestamp,
            "quantum_score": float(score),
            "signatures": signatures,
            "entity": entity,
            "privacy": "EXIF_STRIPPED"
        }
        
        json_file = f"quantum_integrated/quantum_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n💾 Saved: {filename}")


def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ⚛️📷 INTEGRATED QUANTUM CAMERA + VISUALIZER 📷⚛️        ║
║                                                           ║
║        Camera Detection → Full Physics Visualization     ║
║              80+ Quantum Phenomena Available!            ║
║                   EXIF Data Stripped!                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    print("\nSelect mode:")
    print("1. Auto mode (visualize when quantum detected)")
    print("2. Show ALL mode (visualize every capture)")
    print("3. Single shot + full visualization")
    
    choice = input("\nChoice (1-3): ").strip() or "1"
    
    print("\nCamera:")
    print("0. Back camera")
    print("1. Front camera")
    camera_id = int(input("Camera ID (0-1): ").strip() or "0")
    
    system = IntegratedQuantumSystem(camera_id=camera_id)
    
    if choice == "1":
        print("\n🎯 Auto mode: Will visualize when quantum score > 0.7")
        system.run_integrated_detection(show_all=False)
        
    elif choice == "2":
        print("\n🔥 Show ALL mode: Every capture gets full visualization!")
        system.run_integrated_detection(show_all=True)
        
    elif choice == "3":
        print("\n📸 Single shot with full visualization...")
        image_path = system.capture_frame()
        if image_path:
            score, sigs = system.analyze_frame(image_path)
            system.display_score(score, sigs)
            
            entity = system.bridge.create_entity_from_detection(score, sigs, image_path)
            viz_list = system.bridge.get_visualization_list(sigs)
            
            print("\n🌌 Showing full visualization...")
            system.show_visualizations(entity, viz_list, show_all=True)
            system.save_detection(image_path, score, sigs, entity)
    
    print("\n✨ Integrated system complete! ✨\n")

if __name__ == "__main__":
    main()
