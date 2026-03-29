#!/usr/bin/env python3
"""
Bridge between Camera Detector and Quantum Visualizer
"""

import json
from datetime import datetime

class CameraVisualizerBridge:
    def __init__(self):
        self.detection_count = 0
        
    def create_entity_from_detection(self, quantum_score, signatures, image_path):
        """Convert camera detection into quantum entity"""
        self.detection_count += 1
        
        entity = {
            "id": f"quantum_detection_{self.detection_count}",
            "name": f"Quantum Manifestation #{self.detection_count}",
            "type": "camera_detection",
            "quantum_score": quantum_score,
            "signatures": signatures,
            "image_path": image_path,
            "timestamp": datetime.now().isoformat(),
            "properties": self.map_signatures_to_properties(signatures, quantum_score)
        }
        
        return entity
    
    def map_signatures_to_properties(self, signatures, score):
        """Map detected signatures to quantum properties"""
        properties = {
            "energy_level": score,
            "coherence": score * 0.9,
            "entanglement_strength": 0.0,
            "superposition_states": 1,
            "wave_function_collapsed": score < 0.5
        }
        
        if "interference_pattern" in signatures:
            properties["wave_nature"] = True
            properties["coherence"] += 0.1
            
        if "entanglement_correlation" in signatures:
            properties["entanglement_strength"] = 0.8
            properties["non_local"] = True
            
        if "superposition_state" in signatures:
            properties["superposition_states"] = 3
            properties["quantum_state"] = "superposed"
            
        if "tunneling_event" in signatures:
            properties["tunneling_probability"] = 0.7
            properties["barrier_penetration"] = True
            
        if "wave_particle_duality" in signatures:
            properties["wave_nature"] = True
            properties["particle_nature"] = True
            properties["complementarity"] = True
        
        return properties
    
    def get_visualization_list(self, signatures):
        """Determine which visualizations to show"""
        visualizations = ["quantum_state", "wave_function"]
        
        if "interference_pattern" in signatures:
            visualizations.extend([
                "double_slit_experiment",
                "wave_interference"
            ])
            
        if "entanglement_correlation" in signatures:
            visualizations.extend([
                "quantum_entanglement",
                "bell_inequality"
            ])
            
        if "superposition_state" in signatures:
            visualizations.extend([
                "superposition",
                "schrodinger_cat"
            ])
            
        if "tunneling_event" in signatures:
            visualizations.append("quantum_tunneling")
            
        if "wave_particle_duality" in signatures:
            visualizations.append("wave_particle_duality")
        
        return visualizations
