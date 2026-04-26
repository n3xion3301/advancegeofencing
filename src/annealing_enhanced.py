#!/usr/bin/env python3
"""
ENHANCED QUANTUM ANNEALING - VISUAL EDITION
Optimization with stunning visualizations
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.primitives import StatevectorSampler
from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class QuantumAnnealingEnhanced:
    def __init__(self):
        self.operator = "n3xion3301"
        self.sampler = StatevectorSampler()
        
        self.log_dir = Path("logs/quantum")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        print("❄️  Enhanced Quantum Annealing initialized")
    
    def solve_optimization(self, problem_size=10, method='quantum'):
        """Solve with amazing visuals"""
        
        # Header
        self._print_header()
        
        # Generate problem
        energy = self._generate_energy_landscape(problem_size)
        
        # Visualize landscape
        self._visualize_landscape(energy)
        
        # Solve
        if method == 'quantum':
            result = self._quantum_annealing(energy)
        else:
            result = self._simulated_annealing(energy)
        
        # Show results
        self._visualize_results(result, energy)
        
        return result
    
    def _print_header(self):
        """Print awesome header"""
        print("\n" + "╔" + "═"*78 + "╗")
        print("║" + " "*78 + "║")
        print("║" + "❄️  QUANTUM ANNEALING OPTIMIZATION".center(78) + "║")
        print("║" + "Harnessing Quantum Tunneling for Global Optimization".center(78) + "║")
        print("║" + " "*78 + "║")
        print("║" + f"Operator: {self.operator}".center(78) + "║")
        print("║" + f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(78) + "║")
        print("║" + " "*78 + "║")
        print("╚" + "═"*78 + "╝")
    
    def _generate_energy_landscape(self, size):
        """Generate rugged energy landscape"""
        landscape = np.random.rand(size) * 100
        
        # Add quadratic structure
        for i in range(size):
            landscape[i] += 0.1 * (i - size/2)**2
        
        return landscape
    
    def _visualize_landscape(self, energy):
        """Visualize energy landscape"""
        print("\n" + "┌" + "─"*78 + "┐")
        print("│" + " 🗻 ENERGY LANDSCAPE ".center(78) + "│")
        print("├" + "─"*78 + "┤")
        
        max_energy = np.max(energy)
        
        for i, e in enumerate(energy):
            bar_length = int((e / max_energy) * 50)
            bar = "█" * bar_length
            
            # Color coding
            if e == np.min(energy):
                marker = "🌟"  # Global minimum
            elif e < np.percentile(energy, 25):
                marker = "✨"  # Low energy
            else:
                marker = "  "
            
            print(f"│ State {i:2d} {marker} │{bar:50s}│ {e:6.2f} │")
        
        print("├" + "─"*78 + "┤")
        print(f"│ Global Minimum: {np.min(energy):6.2f} at State {np.argmin(energy)} ".ljust(79) + "│")
        print("└" + "─"*78 + "┘")
    
    def _quantum_annealing(self, energy_landscape):
        """Quantum annealing with visual progress"""
        problem_size = len(energy_landscape)
        num_qubits = int(np.ceil(np.log2(problem_size)))
        
        print("\n" + "┌" + "─"*78 + "┐")
        print("│" + " ⚛️  QUANTUM ANNEALING PROCESS ".center(78) + "│")
        print("├" + "─"*78 + "┤")
        
        # Parameters
        T_initial = 100.0
        T_final = 0.01
        steps = 50
        
        best_state = 0
        best_energy = energy_landscape[0]
        energy_history = []
        
        for step in range(steps):
            # Temperature
            t = step / steps
            T = T_initial * (T_final / T_initial) ** t
            
            # Progress bar
            progress = int((step / steps) * 40)
            bar = "█" * progress + "░" * (40 - progress)
            
            # Create quantum circuit
            qc = QuantumCircuit(num_qubits)
            
            # Superposition
            for i in range(num_qubits):
                qc.h(i)
            
            # Problem encoding
            for i in range(min(problem_size, 2**num_qubits)):
                angle = -energy_landscape[i] / 100 * np.pi * (1 - t)
                if num_qubits > 0:
                    qc.ry(angle, 0)
            
            # Entanglement
            for i in range(num_qubits - 1):
                qc.cx(i, i + 1)
            
            # Mixing
            mixing_angle = T / T_initial * np.pi / 4
            for i in range(num_qubits):
                qc.rx(mixing_angle, i)
            
            qc.measure_all()
            
            # Run
            result = self.sampler.run([qc], shots=100).result()
            counts = result[0].data.meas.get_counts()
            
            # Find best
            for state_str, count in counts.items():
                state = int(state_str, 2)
                if state < problem_size:
                    energy = energy_landscape[state]
                    if energy < best_energy:
                        best_energy = energy
                        best_state = state
            
            energy_history.append(best_energy)
            
            # Display progress
            if step % 5 == 0:
                temp_bar = self._get_temp_bar(T, T_initial)
                print(f"│ Step {step:3d}/50 │{bar}│ T:{temp_bar} E:{best_energy:6.2f} │")
        
        print("└" + "─"*78 + "┘")
        
        return {
            'best_state': int(best_state),
            'best_energy': float(best_energy),
            'global_minimum': float(np.min(energy_landscape)),
            'energy_history': energy_history,
            'success': abs(best_energy - np.min(energy_landscape)) < 1.0
        }
    
    def _get_temp_bar(self, T, T_max):
        """Temperature visualization"""
        ratio = T / T_max
        if ratio > 0.7:
            return "🔥🔥🔥"
        elif ratio > 0.4:
            return "🔥🔥 "
        elif ratio > 0.1:
            return "🔥  "
        else:
            return "❄️  "
    
    def _simulated_annealing(self, energy_landscape):
        """Classical simulated annealing"""
        problem_size = len(energy_landscape)
        
        print("\n" + "┌" + "─"*78 + "┐")
        print("│" + " 🌡️  SIMULATED ANNEALING PROCESS ".center(78) + "│")
        print("├" + "─"*78 + "┤")
        
        T_initial = 100.0
        T_final = 0.01
        steps = 1000
        
        current_state = np.random.randint(0, problem_size)
        current_energy = energy_landscape[current_state]
        
        best_state = current_state
        best_energy = current_energy
        energy_history = []
        
        for step in range(steps):
            t = step / steps
            T = T_initial * (T_final / T_initial) ** t
            
            # Propose new state
            new_state = np.random.randint(0, problem_size)
            new_energy = energy_landscape[new_state]
            
            # Accept or reject
            delta_E = new_energy - current_energy
            
            if delta_E < 0 or np.random.random() < np.exp(-delta_E / T):
                current_state = new_state
                current_energy = new_energy
                
                if current_energy < best_energy:
                    best_state = current_state
                    best_energy = current_energy
            
            energy_history.append(best_energy)
            
            # Display progress
            if step % 100 == 0:
                progress = int((step / steps) * 40)
                bar = "█" * progress + "░" * (40 - progress)
                temp_bar = self._get_temp_bar(T, T_initial)
                print(f"│ Step {step:4d}/1000 │{bar}│ T:{temp_bar} E:{best_energy:6.2f} │")
        
        print("└" + "─"*78 + "┘")
        
        return {
            'best_state': int(best_state),
            'best_energy': float(best_energy),
            'global_minimum': float(np.min(energy_landscape)),
            'energy_history': energy_history,
            'success': abs(best_energy - np.min(energy_landscape)) < 1.0
        }
    
    def _visualize_results(self, result, energy):
        """Show final results with visuals"""
        print("\n" + "╔" + "═"*78 + "╗")
        print("║" + " 🎯 OPTIMIZATION RESULTS ".center(78) + "║")
        print("╠" + "═"*78 + "╣")
        
        best_state = result['best_state']
        best_energy = result['best_energy']
        global_min = result['global_minimum']
        
        # Result details
        print("║" + " "*78 + "║")
        print("║" + f"  Best State Found: {best_state}".ljust(78) + "║")
        print("║" + f"  Best Energy: {best_energy:.4f}".ljust(78) + "║")
        print("║" + f"  Global Minimum: {global_min:.4f}".ljust(78) + "║")
        print("║" + " "*78 + "║")
        
        # Success indicator
        gap = abs(best_energy - global_min)
        if gap < 0.1:
            status = "🌟 PERFECT! Found global minimum!"
        elif gap < 1.0:
            status = "✅ EXCELLENT! Very close to optimum!"
        elif gap < 5.0:
            status = "👍 GOOD! Reasonable solution found"
        else:
            status = "⚠️  OK - Local minimum found"
        
        print("║" + f"  Status: {status}".ljust(78) + "║")
        print("║" + f"  Gap from optimum: {gap:.4f}".ljust(78) + "║")
        print("║" + " "*78 + "║")
        
        # Convergence graph
        print("╠" + "═"*78 + "╣")
        print("║" + " 📈 CONVERGENCE GRAPH ".center(78) + "║")
        print("╠" + "═"*78 + "╣")
        
        history = result['energy_history']
        self._plot_convergence(history)
        
        print("╚" + "═"*78 + "╝")
    
    def _plot_convergence(self, history):
        """ASCII convergence plot"""
        if not history:
            print("║" + "  No data to plot".ljust(78) + "║")
            return
        
        # Normalize for plotting
        min_e = min(history)
        max_e = max(history)
        
        if max_e == min_e:
            print("║" + "  Energy constant throughout".ljust(78) + "║")
            return
        
        # Plot 10 points
        step_size = max(1, len(history) // 10)
        
        for i in range(0, len(history), step_size):
            energy = history[i]
            
            # Normalize to 0-50 range
            normalized = int(((energy - min_e) / (max_e - min_e)) * 50)
            
            # Create bar
            bar = " " * normalized + "█"
            
            # Energy indicator
            if energy == min_e:
                marker = "🌟"
            elif energy < min_e + (max_e - min_e) * 0.2:
                marker = "✨"
            else:
                marker = "  "
            
            print(f"║ {i:4d} {marker}│{bar:52s}│{energy:6.2f} ║")
        
        print("║" + "─"*78 + "║")
        print("║" + f"  Min: {min_e:.2f}  Max: {max_e:.2f}  Final: {history[-1]:.2f}".ljust(78) + "║")


def demo_enhanced_annealing():
    """Demo with amazing visuals"""
    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + "═"*78 + "║")
    print("║" + "❄️  QUANTUM ANNEALING DEMONSTRATION".center(78) + "║")
    print("║" + "Advanced Optimization with Quantum Computing".center(78) + "║")
    print("║" + "═"*78 + "║")
    print("╚" + "═"*78 + "╝")
    
    annealer = QuantumAnnealingEnhanced()
    
    # Test 1: Quantum
    print("\n" + "┏" + "━"*78 + "┓")
    print("┃" + " TEST 1: QUANTUM ANNEALING ".center(78) + "┃")
    print("┗" + "━"*78 + "┛")
    
    result1 = annealer.solve_optimization(problem_size=8, method='quantum')
    
    # Test 2: Classical
    print("\n" + "┏" + "━"*78 + "┓")
    print("┃" + " TEST 2: SIMULATED ANNEALING ".center(78) + "┃")
    print("┗" + "━"*78 + "┛")
    
    result2 = annealer.solve_optimization(problem_size=8, method='classical')
    
    # Comparison
    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + " 🏆 FINAL COMPARISON ".center(78) + "║")
    print("╠" + "═"*78 + "╣")
    print("║" + " "*78 + "║")
    print("║" + "  Quantum Annealing:".ljust(78) + "║")
    print("║" + f"    Best Energy: {result1['best_energy']:.4f}".ljust(78) + "║")
    print("║" + f"    Success: {'✅' if result1['success'] else '❌'}".ljust(78) + "║")
    print("║" + " "*78 + "║")
    print("║" + "  Simulated Annealing:".ljust(78) + "║")
    print("║" + f"    Best Energy: {result2['best_energy']:.4f}".ljust(78) + "║")
    print("║" + f"    Success: {'✅' if result2['success'] else '❌'}".ljust(78) + "║")
    print("║" + " "*78 + "║")
    
    # Winner
    if result1['best_energy'] < result2['best_energy']:
        winner = "🏆 Quantum Annealing WINS!"
    elif result2['best_energy'] < result1['best_energy']:
        winner = "🏆 Simulated Annealing WINS!"
    else:
        winner = "🤝 TIE!"
    
    print("║" + f"  {winner}".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "═"*78 + "╝")
    
    print("\n" + "✅ DEMONSTRATION COMPLETE!")


if __name__ == "__main__":
    demo_enhanced_annealing()
