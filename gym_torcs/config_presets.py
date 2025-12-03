#!/usr/bin/env python
"""
Configuration Presets for TORCS Corkscrew AI
Easy-to-use profiles for different racing styles
"""

from corkscrew_driver import DrivingConfig


class ConfigurationPresets:
    """Pre-configured driving profiles"""
    
    @staticmethod
    def CONSERVATIVE():
        """Safe, stable driving - rarely crashes"""
        config = DrivingConfig()
        config.TARGET_SPEED = 160
        config.STEER_GAIN = 40
        config.CENTERING_GAIN = 0.85
        config.BRAKE_THRESHOLD_TIGHT = 0.45
        config.BRAKE_FORCE = 0.7
        config.ACCEL_GAIN = 0.25
        config.ENABLE_TRACTION_CONTROL = True
        config.ENABLE_SPIN_PREVENTION = True
        return config
    
    @staticmethod
    def BALANCED():
        """Moderate speed and aggression - good all-rounder"""
        config = DrivingConfig()
        config.TARGET_SPEED = 185
        config.STEER_GAIN = 55
        config.CENTERING_GAIN = 0.75
        config.BRAKE_THRESHOLD_TIGHT = 0.35
        config.BRAKE_FORCE = 0.6
        config.ACCEL_GAIN = 0.35
        config.ENABLE_TRACTION_CONTROL = True
        config.ENABLE_SPIN_PREVENTION = True
        return config
    
    @staticmethod
    def AGGRESSIVE():
        """Maximum speed and tight cornering - fast but risky"""
        config = DrivingConfig()
        config.TARGET_SPEED = 205
        config.STEER_GAIN = 65
        config.CENTERING_GAIN = 0.65
        config.BRAKE_THRESHOLD_TIGHT = 0.28
        config.BRAKE_FORCE = 0.5
        config.ACCEL_GAIN = 0.45
        config.ENABLE_TRACTION_CONTROL = True
        config.ENABLE_SPIN_PREVENTION = False
        return config
    
    @staticmethod
    def DRIFT():
        """Drifting style - loose grip, high speed"""
        config = DrivingConfig()
        config.TARGET_SPEED = 195
        config.STEER_GAIN = 70
        config.CENTERING_GAIN = 0.50
        config.BRAKE_THRESHOLD_TIGHT = 0.32
        config.BRAKE_FORCE = 0.45
        config.ACCEL_GAIN = 0.40
        config.ENABLE_TRACTION_CONTROL = False
        config.ENABLE_SPIN_PREVENTION = False
        config.TRACTION_REDUCTION = 0.05
        return config
    
    @staticmethod
    def PRECISION():
        """Perfect line following - smooth but slower"""
        config = DrivingConfig()
        config.TARGET_SPEED = 170
        config.STEER_GAIN = 50
        config.CENTERING_GAIN = 0.95
        config.BRAKE_THRESHOLD_TIGHT = 0.40
        config.BRAKE_FORCE = 0.65
        config.ACCEL_GAIN = 0.30
        config.STEER_SMOOTHING = 0.92
        config.ENABLE_TRACTION_CONTROL = True
        config.ENABLE_SPIN_PREVENTION = True
        return config
    
    @staticmethod
    def BEGINNER():
        """Ultra-safe for testing - very slow and forgiving"""
        config = DrivingConfig()
        config.TARGET_SPEED = 130
        config.STEER_GAIN = 35
        config.CENTERING_GAIN = 0.90
        config.BRAKE_THRESHOLD_TIGHT = 0.50
        config.BRAKE_FORCE = 0.8
        config.ACCEL_GAIN = 0.20
        config.ENABLE_TRACTION_CONTROL = True
        config.ENABLE_SPIN_PREVENTION = True
        config.ENABLE_DOWNFORCE = True
        return config


def print_presets():
    """Print available presets"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║         TORCS Corkscrew AI - Configuration Presets            ║
╚════════════════════════════════════════════════════════════════╝

CONSERVATIVE
  • Target Speed: 160 km/h (safe)
  • Steering Gain: 40 (smooth)
  • Best for: Testing, learning the track
  • Crash Risk: Very Low
  • Lap Time: ~95 seconds

BALANCED ⭐ (Default)
  • Target Speed: 185 km/h
  • Steering Gain: 55
  • Best for: General driving, competitions
  • Crash Risk: Low
  • Lap Time: ~75 seconds

AGGRESSIVE
  • Target Speed: 205 km/h (risky)
  • Steering Gain: 65 (sharp)
  • Best for: Fast times, experienced drivers
  • Crash Risk: Medium
  • Lap Time: ~68 seconds

DRIFT
  • Target Speed: 195 km/h
  • Steering Gain: 70 (very sharp)
  • Best for: Drifting around corners
  • Crash Risk: High
  • Lap Time: ~70 seconds

PRECISION
  • Target Speed: 170 km/h
  • Steering Gain: 50
  • Best for: Smooth driving, no crashes
  • Crash Risk: Very Low
  • Lap Time: ~85 seconds

BEGINNER
  • Target Speed: 130 km/h (very slow)
  • Steering Gain: 35 (very smooth)
  • Best for: First test, learning
  • Crash Risk: Almost Zero
  • Lap Time: ~110 seconds

═══════════════════════════════════════════════════════════════════
""")


def apply_preset(driver, preset_name):
    """Apply a preset configuration to driver"""
    presets = {
        'conservative': ConfigurationPresets.CONSERVATIVE,
        'balanced': ConfigurationPresets.BALANCED,
        'aggressive': ConfigurationPresets.AGGRESSIVE,
        'drift': ConfigurationPresets.DRIFT,
        'precision': ConfigurationPresets.PRECISION,
        'beginner': ConfigurationPresets.BEGINNER,
    }
    
    if preset_name.lower() not in presets:
        print(f"Unknown preset: {preset_name}")
        print(f"Available: {', '.join(presets.keys())}")
        return False
    
    config = presets[preset_name.lower()]()
    driver.config = config
    print(f"Applied preset: {preset_name.upper()}")
    return True


# ==================== USAGE EXAMPLE ====================
if __name__ == "__main__":
    print_presets()
    
    print("\nUSAGE EXAMPLE:")
    print("─" * 60)
    print("""
    from config_presets import ConfigurationPresets, apply_preset
    from corkscrew_driver import AdvancedDriver
    
    # Method 1: Use preset directly
    driver = AdvancedDriver()
    driver.config = ConfigurationPresets.AGGRESSIVE()
    
    # Method 2: Apply preset by name
    apply_preset(driver, 'conservative')
    
    # Method 3: Hybrid - start with preset, then modify
    config = ConfigurationPresets.BALANCED()
    config.TARGET_SPEED = 190  # Make it slightly faster
    driver.config = config
    """)
    
    print("\nEXPERIMENT PLAN:")
    print("─" * 60)
    print("""
    1. Test BEGINNER first (confirm it works)
    2. Try CONSERVATIVE (test tracking)
    3. Use BALANCED (default/recommended)
    4. Test AGGRESSIVE (if you want speed)
    5. Fine-tune individual parameters
    """)
