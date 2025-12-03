#!/usr/bin/env python
"""
TORCS Corkscrew Track Configuration Script
Sets up the race configuration for 3 laps on Corkscrew track with scr_server.
"""

import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def get_race_config():
    """Generate race configuration for 3-lap Corkscrew race"""
    config = """<?xml version="1.0" encoding="UTF-8"?>
<params name="race engine">
    <!-- Race Configuration: Corkscrew Track - 3 Laps -->
    
    <!-- Drivers -->
    <section name="Drivers">
        <attnum name="Num" val="1"/>
        <attstr name="Name" val="SCR"/>
        <attstr name="Car name" val="car1-stock1"/>
        <attstr name="Module" val="scr_server"/>
        <attstr name="Host" val="localhost"/>
        <attnum name="Port" val="3001"/>
    </section>
    
    <!-- Track -->
    <section name="Track">
        <attstr name="Name" val="corkscrew"/>
        <attnum name="Laps" val="3"/>
        <attnum name="Distance" val="3000"/>
        <attnum name="Width" val="15"/>
    </section>
    
    <!-- Race Parameters -->
    <section name="Race">
        <attnum name="Type" val="2"/>  <!-- 2 = Quick Race -->
        <attnum name="Duration" val="1800"/>  <!-- 30 minutes -->
        <attnum name="Distance" val="0"/>
        <attstr name="Track" val="corkscrew"/>
        <attnum name="Laps" val="3"/>
        <attnum name="Fuel" val="100"/>
        <attnum name="Damage" val="0"/>
        <attnum name="Pit time" val="0"/>
        <attstr name="Category" val="free"/>
        <attnum name="Allowed damage" val="0"/>
        <attnum name="Light type" val="2"/>
        <attnum name="Time of day" val="0"/>
        <attnum name="Weather" val="1"/>
        <attnum name="Wind" val="0"/>
    </section>
    
    <!-- Network Settings for scr_server -->
    <section name="SCR">
        <attstr name="Host" val="127.0.0.1"/>
        <attnum name="Port" val="3001"/>
        <attnum name="Timeout" val="10"/>
        <attnum name="Max clients" val="1"/>
        <attstr name "Session name" val="corkscrew_3lap_race"/>
        <attnum name="Stage" val="2"/>  <!-- 0=warm-up, 1=qualifying, 2=race -->
    </section>
    
    <!-- Physics Parameters -->
    <section name="Physics">
        <attnum name="Friction" val="1.0"/>
        <attnum name="Restitution" val="0.3"/>
        <attnum name="Aerodynamics" val="1.0"/>
        <attnum name="Brake stiffness" val="1.0"/>
        <attnum name="Tire friction" val="1.0"/>
        <attnum name="Rolling resistance" val="1.0"/>
    </section>
    
</params>
"""
    return config


def create_config_file():
    """Create configuration file"""
    config_path = Path("practice.xml")
    
    with open(config_path, 'w') as f:
        f.write(get_race_config())
    
    print(f"[Config] Created race configuration: {config_path}")


def print_setup_instructions():
    """Print setup instructions"""
    print("""
╔═════════════════════════════════════════════════════════════════╗
║    TORCS Corkscrew AI Driver - Setup Instructions             ║
╚═════════════════════════════════════════════════════════════════╝

PREREQUISITES:
✓ TORCS installed and working
✓ Python 3.6+
✓ scr_server running in TORCS
✓ Corkscrew track available

STEP 1: Start TORCS
─────────────────────────────────────────────────────────────────
  1. Launch TORCS: torcs -nofuel -nodamage -nolaptime &
  2. Go to: Race → Quick Race → Configure Race
  3. Select: Track = "corkscrew"
  4. Select: Car = "car1-stock1" (or any stock car)
  5. Set: Number of laps = 3
  6. Start the race (it will wait for client connection)

STEP 2: Run the Python AI Driver
─────────────────────────────────────────────────────────────────
  Method 1 - Enhanced Version (Recommended):
  $ python torcs_jm_par_enhanced.py -p 3001

  Method 2 - Original Version:
  $ python torcs_jm_par.py -p 3001

  Method 3 - With Debugging:
  $ python torcs_jm_par_enhanced.py -p 3001 -d

STEP 3: Monitor the Race
─────────────────────────────────────────────────────────────────
  • Watch TORCS window for car movement
  • Python console shows lap count and speed
  • Race completes when all 3 laps are done

CONFIGURATION OPTIONS:
─────────────────────────────────────────────────────────────────
Edit 'corkscrew_driver.py' → DrivingConfig class:

  TARGET_SPEED = 185
    → Car's target speed (higher = faster, less stable)
  
  STEER_GAIN = 55
    → Steering sensitivity (higher = more responsive)
  
  CENTERING_GAIN = 0.75
    → How hard car tries to center on track
  
  BRAKE_THRESHOLD_TIGHT = 0.35
    → When to brake in sharp curves
  
  ENABLE_TRACTION_CONTROL = True
    → Prevent wheel spin on acceleration

TROUBLESHOOTING:
─────────────────────────────────────────────────────────────────
Problem: "Waiting for server"
  → Make sure TORCS race is actually started and waiting
  → Check port 3001 is available
  → Try different port: python torcs_jm_par_enhanced.py -p 3002

Problem: Car crashes or drives off track
  → Reduce TARGET_SPEED in DrivingConfig
  → Reduce STEER_GAIN to make steering less aggressive
  → Increase BRAKE_THRESHOLD values

Problem: Car runs too slow
  → Increase TARGET_SPEED
  → Increase STEER_GAIN for better cornering
  → Increase ACCEL_GAIN for faster acceleration

Problem: Car gets stuck
  → The AI has recovery logic, wait 20 seconds
  → Or restart the race and try different settings

FILES REFERENCE:
─────────────────────────────────────────────────────────────────
• corkscrew_driver.py
  → Advanced AI logic (editable configuration)

• torcs_jm_par_enhanced.py
  → Main client (run this!)

• torcs_jm_par.py
  → Original client (has modular drive logic)

• snakeoil3_jm2.py
  → Base TORCS protocol library

PERFORMANCE TIPS:
─────────────────────────────────────────────────────────────────
1. Start with default settings to verify it works
2. Record lap times after 3 laps
3. Gradually increase TARGET_SPEED (165 → 185 → 200)
4. Adjust BRAKE_THRESHOLD if crashes
5. Tune STEER_GAIN for smoother cornering

═════════════════════════════════════════════════════════════════
""")


if __name__ == "__main__":
    print("TORCS Corkscrew AI - Configuration Setup")
    print("=" * 60)
    
    # Create configuration file
    create_config_file()
    
    # Print instructions
    print_setup_instructions()
    
    print("\n✓ Setup complete! Follow the instructions above to start racing.")
