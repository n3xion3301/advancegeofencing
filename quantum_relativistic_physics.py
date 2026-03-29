#!/usr/bin/env python3
"""⚛️ Quantum Relativistic Physics - Python Interface"""

try:
    import relativistic_physics
    RUST_AVAILABLE = True
    print("✅ Rust physics engine loaded!")
except ImportError:
    RUST_AVAILABLE = False
    print("⚠️  Rust not available")

def demo():
    if not RUST_AVAILABLE:
        print("Module not found!")
        return
    
    print("\n" + "="*60)
    print("⚛️ RELATIVISTIC PHYSICS DEMO ⚛️")
    print("="*60 + "\n")
    
    # 1. Electron at 0.9c
    print("1️⃣  ELECTRON AT 0.9c\n")
    electron = relativistic_physics.create_electron(0.9)
    print(electron.get_analysis())
    
    # 2. Proton at 0.5c
    print("\n2️⃣  PROTON AT 0.5c\n")
    proton = relativistic_physics.create_proton(0.5)
    print(proton.get_analysis())
    
    # 3. Photon
    print("\n3️⃣  PHOTON (Light Speed)\n")
    photon = relativistic_physics.create_photon()
    print(photon.get_analysis())
    
    # 4. Tachyon
    print("\n4️⃣  TACHYON AT 1.5c (Superluminal!)\n")
    tachyon = relativistic_physics.create_tachyon(1.5)
    print(tachyon.get_analysis())
    
    # 5. Ultra-relativistic particle
    print("\n5️⃣  ULTRA-RELATIVISTIC AT 0.99c\n")
    ultra = relativistic_physics.create_electron(0.99)
    print(ultra.get_analysis())
    
    print("="*60)
    print("✨ Demo complete! ✨")
    print("="*60)

if __name__ == "__main__":
    demo()
