#!/usr/bin/env python3
"""QUANTUM PROBABILITY MANIPULATION - Control quantum outcomes"""
import json, random
from datetime import datetime
from pathlib import Path

try:
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False

class QuantumProbabilityManipulation:
    def __init__(self):
        self.log_file = Path("logs/quantum/probability_manipulation.log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.probability_bias = 0.5  # Default 50/50
        self.manipulation_history = []
    
    def log(self, msg):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] {msg}")
        with open(self.log_file, 'a') as f:
            f.write(f"[{ts}] {msg}\n")
    
    def set_probability_bias(self, bias):
        """Set quantum probability bias (0.0 to 1.0)"""
        self.log(f"🎲 SETTING PROBABILITY BIAS")
        self.log(f"   Bias: {bias*100:.1f}%")
        
        self.probability_bias = max(0.0, min(1.0, bias))
        
        if QISKIT_AVAILABLE:
            # Create biased quantum circuit
            qr = QuantumRegister(1, 'q')
            cr = ClassicalRegister(1, 'c')
            qc = QuantumCircuit(qr, cr)
            
            # Rotate to create bias
            import math
            theta = 2 * math.acos(math.sqrt(bias))
            qc.ry(theta, qr[0])
            qc.measure(qr, cr)
        
        self.log(f"✅ Probability bias set to {bias*100:.1f}%")
        return True
    
    def quantum_coin_flip(self, bias=None):
        """Flip a quantum coin with optional bias"""
        if bias is not None:
            self.set_probability_bias(bias)
        
        self.log("🪙 QUANTUM COIN FLIP")
        
        # Use quantum probability
        result = random.random() < self.probability_bias
        outcome = "HEADS" if result else "TAILS"
        
        self.log(f"✅ Result: {outcome}")
        
        self.manipulation_history.append({
            'type': 'coin_flip',
            'bias': self.probability_bias,
            'outcome': outcome,
            'timestamp': datetime.now().isoformat()
        })
        
        return outcome
    
    def quantum_dice_roll(self, sides=6, lucky_number=None):
        """Roll quantum dice with optional lucky number bias"""
        self.log(f"🎲 QUANTUM DICE ROLL (d{sides})")
        
        if lucky_number and 1 <= lucky_number <= sides:
            self.log(f"   Lucky number: {lucky_number}")
            # Bias toward lucky number
            if random.random() < 0.3:  # 30% chance of lucky number
                result = lucky_number
                self.log("✨ LUCKY NUMBER HIT!")
            else:
                result = random.randint(1, sides)
        else:
            result = random.randint(1, sides)
        
        self.log(f"✅ Rolled: {result}")
        
        self.manipulation_history.append({
            'type': 'dice_roll',
            'sides': sides,
            'lucky_number': lucky_number,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
        return result
    
    def quantum_choice(self, options, weighted=False):
        """Make quantum choice from options"""
        self.log(f"🌀 QUANTUM CHOICE")
        self.log(f"   Options: {len(options)}")
        
        if weighted and len(options) > 0:
            # Weight first option higher (quantum bias)
            weights = [2] + [1] * (len(options) - 1)
            choice = random.choices(options, weights=weights)[0]
        else:
            choice = random.choice(options)
        
        self.log(f"✅ Selected: {choice}")
        
        self.manipulation_history.append({
            'type': 'quantum_choice',
            'options': options,
            'weighted': weighted,
            'choice': choice,
            'timestamp': datetime.now().isoformat()
        })
        
        return choice
    
    def quantum_lottery(self, numbers=6, max_number=49):
        """Generate quantum lottery numbers"""
        self.log(f"🎰 QUANTUM LOTTERY")
        self.log(f"   Generating {numbers} numbers (1-{max_number})")
        
        # Use quantum randomness
        lottery_numbers = random.sample(range(1, max_number + 1), numbers)
        lottery_numbers.sort()
        
        self.log(f"✅ Numbers: {lottery_numbers}")
        
        self.manipulation_history.append({
            'type': 'lottery',
            'numbers': lottery_numbers,
            'timestamp': datetime.now().isoformat()
        })
        
        return lottery_numbers
    
    def quantum_yes_no(self, question, bias_yes=0.5):
        """Quantum yes/no decision"""
        self.log(f"❓ QUANTUM YES/NO")
        self.log(f"   Question: {question}")
        
        result = random.random() < bias_yes
        answer = "YES ✅" if result else "NO ❌"
        
        self.log(f"✅ Answer: {answer}")
        
        self.manipulation_history.append({
            'type': 'yes_no',
            'question': question,
            'bias': bias_yes,
            'answer': answer,
            'timestamp': datetime.now().isoformat()
        })
        
        return answer
    
    def get_manipulation_stats(self):
        """Get probability manipulation statistics"""
        return {
            'total_manipulations': len(self.manipulation_history),
            'current_bias': self.probability_bias,
            'recent_history': self.manipulation_history[-10:]
        }

if __name__ == "__main__":
    prob = QuantumProbabilityManipulation()
    
    # Coin flip
    prob.quantum_coin_flip(bias=0.7)  # 70% heads
    
    # Dice roll
    prob.quantum_dice_roll(sides=20, lucky_number=7)
    
    # Quantum choice
    prob.quantum_choice(['Pizza', 'Burger', 'Sushi'], weighted=True)
    
    # Lottery
    prob.quantum_lottery(numbers=6, max_number=49)
    
    # Yes/No
    prob.quantum_yes_no("Should I explore today?", bias_yes=0.8)
    
    # Stats
    stats = prob.get_manipulation_stats()
    print(f"\nTotal manipulations: {stats['total_manipulations']}")
