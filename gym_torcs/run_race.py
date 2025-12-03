#!/usr/bin/env python
"""
TORCS Corkscrew AI - Easy Runner Script
Choose preset, configure, and run your AI driver with one command!
"""

import sys
import os
from pathlib import Path


def print_menu():
    """Print main menu"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║    TORCS Corkscrew AI Runner - Easy Configuration           ║
╚═══════════════════════════════════════════════════════════════╝

Please choose your racing profile:

  1) BEGINNER      - Ultra safe, very slow (130 km/h)
  2) CONSERVATIVE  - Safe, smooth (160 km/h)
  3) BALANCED ⭐   - Default, recommended (185 km/h)
  4) AGGRESSIVE    - Fast, risky (205 km/h)
  5) DRIFT         - Drifting style (195 km/h)
  6) PRECISION     - Perfect line (170 km/h)
  
  0) CUSTOM        - Edit config_presets.py yourself

  Q) QUIT          - Exit

═══════════════════════════════════════════════════════════════
""")


def print_instructions():
    """Print race setup instructions"""
    print("""
BEFORE RUNNING THE AI:
══════════════════════════════════════════════════════════════

Step 1: Start TORCS
  $ torcs -nofuel -nodamage -nolaptime &

Step 2: In TORCS Menu
  • Click: Race → Quick Race → Configure Race
  • Track: Select "corkscrew"
  • Car: Select "car1-stock1" (any stock car works)
  • Laps: Set to "3"
  • Click: START RACE (race will wait for AI connection)

Step 3: This Script Will Run the AI

Press ENTER when ready to start the AI...
""")


def generate_runner_script(preset_name):
    """Generate a one-time runner for the chosen preset"""
    
    script_content = f'''#!/usr/bin/env python
"""Auto-generated runner for {preset_name.upper()} preset"""

import sys
sys.path.insert(0, '.')

from torcs_jm_par_enhanced import Client
from corkscrew_driver import AdvancedDriver
from config_presets import ConfigurationPresets

if __name__ == "__main__":
    print(f"Starting race with {preset_name.upper()} configuration...")
    
    # Create client and driver
    C = Client(p=3001)
    driver = AdvancedDriver()
    
    # Apply preset
    driver.config = ConfigurationPresets.{preset_name.upper()}()
    print(f"Configuration applied: {preset_name.upper()}")
    print(f"Target Speed: {{driver.config.TARGET_SPEED}} km/h")
    print(f"Steering Gain: {{driver.config.STEER_GAIN}}")
    
    print("\\n[Main] Starting race...")
    print("[Main] Press Ctrl+C to stop\\n")
    
    step_count = 0
    try:
        for step in range(C.maxSteps, 0, -1):
            C.get_servers_input()
            driver.drive(C.S, C.R)
            C.respond_to_server()
            step_count += 1
            
            if step_count % 500 == 0:
                speed = C.S.d.get('speedX', 0)
                lap = driver.lap_count
                dist = C.S.d.get('distFromStart', 0)
                print(f"\\r[Lap {{lap}}] Speed: {{speed:.1f}} km/h | Distance: {{dist:.0f}}m ", 
                      end='', flush=True)
        
        C.shutdown()
        print("\\n[Main] Race completed successfully!")
        
    except KeyboardInterrupt:
        print("\\n[Main] User interrupted")
        C.shutdown()
    except Exception as e:
        print(f"\\n[Main] Error: {{e}}")
        C.shutdown()
        raise
'''
    
    return script_content


def run_race(preset_name):
    """Run the race with the chosen preset"""
    print(f"\nStarting race with {preset_name.upper()} preset...")
    print("=" * 60)
    
    # Import dynamically
    try:
        from torcs_jm_par_enhanced import Client
        from corkscrew_driver import AdvancedDriver
        from config_presets import ConfigurationPresets
    except ImportError as e:
        print(f"Error: Could not import required modules: {e}")
        print("Make sure you're in the gym_torcs directory!")
        return False
    
    try:
        # Create client and driver
        C = Client(p=3001)
        driver = AdvancedDriver()
        
        # Apply preset
        preset_func = getattr(ConfigurationPresets, preset_name.upper(), None)
        if preset_func:
            driver.config = preset_func()
            print(f"✓ Configuration: {preset_name.upper()}")
            print(f"  • Target Speed: {driver.config.TARGET_SPEED} km/h")
            print(f"  • Steering Gain: {driver.config.STEER_GAIN}")
            print(f"  • Brake Threshold: {driver.config.BRAKE_THRESHOLD_TIGHT}")
        else:
            print(f"Warning: Preset {preset_name} not found, using defaults")
        
        print("\n[Race] Starting 3-lap race...")
        print("[Race] Connected to TORCS on port 3001\n")
        
        step_count = 0
        last_lap = -1
        last_print = 0
        
        for step in range(C.maxSteps, 0, -1):
            C.get_servers_input()
            driver.drive(C.S, C.R)
            C.respond_to_server()
            step_count += 1
            
            # Print lap changes
            if driver.lap_count != last_lap:
                last_lap = driver.lap_count
                print(f"\n🏁 LAP {last_lap} STARTED")
            
            # Print status every 10 seconds
            if step_count - last_print >= 500:
                last_print = step_count
                speed = C.S.d.get('speedX', 0)
                lap = driver.lap_count
                dist = C.S.d.get('distFromStart', 0)
                print(f"[Lap {lap}] Speed: {speed:.1f} km/h | Distance: {dist:.0f}m")
        
        C.shutdown()
        print("\n✓ Race completed successfully!")
        print(f"Total steps: {step_count}")
        print(f"Final lap: {driver.lap_count}")
        return True
        
    except KeyboardInterrupt:
        print("\n\n⚠ User interrupted the race")
        C.shutdown()
        return False
    except ConnectionRefusedError:
        print("\n✗ Error: Could not connect to TORCS")
        print("  Make sure TORCS is running and the race is started!")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        C.shutdown()
        return False


def main():
    """Main menu loop"""
    print("\n" * 2)
    
    # Print welcome
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║      Welcome to TORCS Corkscrew AI Runner v1.0              ║")
    print("║     3-Lap Race on Corkscrew Track with Advanced AI          ║")
    print("╚═══════════════════════════════════════════════════════════════╝\n")
    
    presets = {
        '1': 'beginner',
        '2': 'conservative',
        '3': 'balanced',
        '4': 'aggressive',
        '5': 'drift',
        '6': 'precision',
    }
    
    while True:
        print_menu()
        choice = input("Enter choice (1-6, 0, Q): ").strip().upper()
        
        if choice == 'Q':
            print("\nGoodbye! 👋")
            sys.exit(0)
        
        elif choice == '0':
            print("\nCustom mode: Edit config_presets.py to customize settings")
            print("Then run: python torcs_jm_par_enhanced.py -p 3001")
            input("Press ENTER to return to menu...")
            continue
        
        elif choice in presets:
            print_instructions()
            input()
            
            preset = presets[choice]
            print(f"\n{'='*60}")
            print(f"Configuration: {preset.upper()}")
            print(f"{'='*60}\n")
            
            success = run_race(preset)
            
            print("\n" + "="*60)
            if success:
                print("Race finished! Return to menu to try another preset.")
            print("="*60)
            input("\nPress ENTER to continue...")
        
        else:
            print("\n✗ Invalid choice. Please try again.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
        sys.exit(0)
