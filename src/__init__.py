#!/usr/bin/env python3
"""
ENHANCED Quantum Geofencing Package
Advanced quantum-powered location tracking and geofencing system

Author: n3xion3301
Version: 2.0.0 (Enhanced)
"""

__version__ = "2.0.0-enhanced"
__author__ = "n3xion3301"
__license__ = "MIT"

# Try relative imports first (when used as package)
# Fall back to direct imports (when used standalone)
try:
    from .activity_detector_enhanced import ActivityDetectorEnhanced
    from .android_location_enhanced import AndroidLocationProviderEnhanced
    from .analytics_enhanced import QuantumAnalyticsEnhanced
    from .ai_integration_enhanced import QuantumAIEnhanced
    from .annealing_enhanced import QuantumAnnealingEnhanced
    from .entanglement_enhanced import QuantumEntanglementEnhanced
    from .superposition_enhanced import QuantumSuperpositionEnhanced
    from .wave_collapse_enhanced import WaveCollapseEnhanced
    from .tunneling_enhanced import QuantumTunnelingEnhanced
    from .interference_enhanced import QuantumInterferenceEnhanced
    from .geofence_monitor_enhanced import GeofenceMonitorEnhanced
    from .hardware_geofence_enhanced import HardwareGeofenceEnhanced
    from .hawking_radiation_enhanced import HawkingRadiationEnhanced
    from .vacuum_energy_enhanced import VacuumEnergyEnhanced
    from .time_dilation_enhanced import TimeDilationEnhanced
    from .parallel_universe_detector_enhanced import ParallelUniverseDetectorEnhanced
    from .parallel_universe_navigator_enhanced import ParallelUniverseNavigatorEnhanced
    from .portal_system_enhanced import PortalSystemEnhanced
    from .teleportation_enhanced import QuantumTeleportationEnhanced
    from .aer_simulator_enhanced import AerSimulatorEnhanced
except ImportError:
    # Standalone mode - imports will be done on-demand
    pass

__all__ = [
    'ActivityDetectorEnhanced',
    'AndroidLocationProviderEnhanced',
    'QuantumAnalyticsEnhanced',
    'QuantumAIEnhanced',
    'QuantumAnnealingEnhanced',
    'QuantumEntanglementEnhanced',
    'QuantumSuperpositionEnhanced',
    'WaveCollapseEnhanced',
    'QuantumTunnelingEnhanced',
    'QuantumInterferenceEnhanced',
    'GeofenceMonitorEnhanced',
    'HardwareGeofenceEnhanced',
    'HawkingRadiationEnhanced',
    'VacuumEnergyEnhanced',
    'TimeDilationEnhanced',
    'ParallelUniverseDetectorEnhanced',
    'ParallelUniverseNavigatorEnhanced',
    'PortalSystemEnhanced',
    'QuantumTeleportationEnhanced',
    'AerSimulatorEnhanced',
]


def print_banner():
    """Print package banner"""
    print("╔" + "═"*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "⚛️  QUANTUM GEOFENCING PACKAGE".center(78) + "║")
    print("║" + f"Version {__version__}".center(78) + "║")
    print("║" + " "*78 + "║")
    print("║" + "Advanced Quantum-Powered Location Tracking".center(78) + "║")
    print("║" + " "*78 + "║")
    print("║" + f"Author: {__author__}".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "═"*78 + "╝")


def get_version():
    """Get package version"""
    return __version__


def list_modules():
    """List all available enhanced modules"""
    print("\n" + "="*80)
    print("📦 AVAILABLE ENHANCED MODULES".center(80))
    print("="*80)
    
    categories = {
        "🔬 Core Systems": [
            'ActivityDetectorEnhanced',
            'AndroidLocationProviderEnhanced',
            'QuantumAnalyticsEnhanced',
            'QuantumAIEnhanced',
            'QuantumAnnealingEnhanced',
        ],
        "⚛️ Quantum Mechanics": [
            'QuantumEntanglementEnhanced',
            'QuantumSuperpositionEnhanced',
            'WaveCollapseEnhanced',
            'QuantumTunnelingEnhanced',
            'QuantumInterferenceEnhanced',
        ],
        "📡 Geofencing": [
            'GeofenceMonitorEnhanced',
            'HardwareGeofenceEnhanced',
        ],
        "🌌 Advanced Physics": [
            'HawkingRadiationEnhanced',
            'VacuumEnergyEnhanced',
            'TimeDilationEnhanced',
        ],
        "🌀 Dimensional Systems": [
            'ParallelUniverseDetectorEnhanced',
            'ParallelUniverseNavigatorEnhanced',
            'PortalSystemEnhanced',
            'QuantumTeleportationEnhanced',
        ],
        "🛠️ Utilities": [
            'AerSimulatorEnhanced',
        ]
    }
    
    for category, modules in categories.items():
        print(f"\n{category}")
        print("-" * 80)
        for module in modules:
            print(f"  ✨ {module}")
    
    print("\n" + "="*80)
    print(f"Total: {len(__all__)} enhanced modules available")
    print("="*80 + "\n")


# Only auto-print if run directly
if __name__ == "__main__":
    print_banner()
    print(f"\n✅ Quantum Geofencing Package v{__version__}")
    print(f"📦 {len(__all__)} enhanced modules available")
    print("\n💡 Available functions:")
    print("  • get_version() - Get package version")
    print("  • list_modules() - List all modules")
    print("  • print_banner() - Display banner\n")
    list_modules()
