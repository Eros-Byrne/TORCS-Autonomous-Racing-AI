# TORCS Corkscrew AI Driver - 3 Lap Race

Advanced AI driving logic specifically optimized for the Corkscrew track in TORCS racing simulator.

## Overview

This package contains an intelligent autonomous driver for TORCS that can complete 3 laps on the challenging Corkscrew track without crashing. The AI uses advanced techniques including:

- **Adaptive Speed Management**: Dynamic target speeds based on track curvature
- **Intelligent Steering**: Smooth steering with automatic centering
- **Predictive Braking**: Brake force adjusted based on turn sharpness
- **Traction Control**: Prevent wheel spin during acceleration
- **Spin Prevention**: Recovery system for loss of control
- **Lap Tracking**: Monitor progress through 3 laps
- **Automatic Gear Shifting**: Optimized gearing for performance

## Files

### Core Files

1. **corkscrew_driver.py** (NEW)
   - Advanced AI driving logic
   - Configurable parameters
   - Adaptive behavior system
   - All driving intelligence in one place

2. **torcs_jm_par_enhanced.py** (NEW)
   - Main client application
   - Enhanced TORCS protocol handling
   - Better logging and monitoring
   - **Use this file to run the race**

3. **torcs_jm_par.py** (ORIGINAL)
   - Original modular driving logic
   - Reference implementation
   - Contains utility functions

### Configuration Files

4. **setup_corkscrew.py**
   - Race configuration generator
   - Setup instructions
   - Troubleshooting guide

### Support Files (Existing)

- snakeoil3_jm2.py: TORCS protocol library
- snakeoil3_gym.py: Gym interface
- practice.xml: Race configuration

## Quick Start

### Step 1: Prepare TORCS

```bash
# Start TORCS (in terminal/PowerShell)
cd c:\path\to\torcs
torcs -nofuel -nodamage -nolaptime &
```

### Step 2: Configure the Race

In TORCS menu:
1. Click **Race** → **Quick Race**
2. Configure:
   - **Track**: Select "corkscrew"
   - **Car**: Select "car1-stock1"
   - **Laps**: Set to 3
3. Click **Start Race** (the race will wait for AI connection)

### Step 3: Run the AI Driver

```bash
# Open another PowerShell/terminal in the gym_torcs folder
cd c:\path\to\gym_torcs

# Run the enhanced driver
python torcs_jm_par_enhanced.py -p 3001
```

### Step 4: Watch It Race!

The car will automatically:
- Connect to the TORCS race
- Complete 3 laps on Corkscrew
- Maintain speed on straights
- Brake appropriately for corners
- Recover from minor slides
- Finish the race

## Customization

Edit `corkscrew_driver.py` → `DrivingConfig` class to tune behavior:

```python
class DrivingConfig:
    # Speed Management
    TARGET_SPEED = 185              # Increase for faster, decrease for safety
    MAX_SPEED = 220                 # Upper speed limit
    
    # Steering Control
    STEER_GAIN = 55                 # Higher = more responsive steering
    CENTERING_GAIN = 0.75           # How hard to stay centered
    
    # Braking Strategy
    BRAKE_THRESHOLD_TIGHT = 0.35    # Threshold for tight corners
    BRAKE_FORCE = 0.6               # Normal braking force
    
    # Traction Control
    ENABLE_TRACTION_CONTROL = True  # Prevent wheel spin
    TRACTION_THRESHOLD = 2.2        # How much wheel spin allowed
```

### Tuning Guide

**Car runs too slow:**
- Increase `TARGET_SPEED` (165 → 185 → 200)
- Increase `ACCEL_GAIN` (0.35 → 0.40 → 0.45)

**Car crashes/drives off track:**
- Decrease `TARGET_SPEED` (185 → 170 → 160)
- Decrease `STEER_GAIN` (55 → 45 → 35)
- Increase `BRAKE_THRESHOLD_TIGHT` (0.35 → 0.45 → 0.55)

**Car has too much understeer (won't turn enough):**
- Increase `STEER_GAIN`
- Increase `CENTERING_GAIN` (0.75 → 0.85 → 0.95)

**Car slides out on exits:**
- Decrease `TARGET_SPEED`
- Increase `TRACTION_THRESHOLD` (2.2 → 2.5)
- Enable `ENABLE_SPIN_PREVENTION`

## How It Works

### Control System

1. **Steering** = f(angle, track_position)
   - Corrects for track curvature
   - Centers car on track
   - Smooth transitions to prevent abrupt changes

2. **Braking** = f(turn_sharpness, speed)
   - Harder brake for tighter curves
   - Emergency braking for extreme angles
   - Stability braking if off-track

3. **Acceleration** = f(current_speed, target_speed, wheel_spin)
   - Boost at low speeds
   - Proportional control at cruise
   - Traction control to prevent spin

4. **Gearing** = f(current_speed)
   - Automatic shift based on speed thresholds
   - Optimized for performance

### Track-Specific Features

The "Corkscrew" name comes from the track's spiral geometry. The AI handles this with:

- **Corkscrew Correction Factor**: 1.2× steering multiplier for tight sections
- **Aggressive Centering**: Keeps car in optimal racing line
- **Early Braking**: Anticipates sharp turns ahead

## Command Line Options

```bash
# Port (where TORCS is listening)
python torcs_jm_par_enhanced.py -p 3001

# Host (if TORCS on different machine)
python torcs_jm_par_enhanced.py -H 192.168.1.100

# Debug output (very verbose)
python torcs_jm_par_enhanced.py -d

# Custom track name
python torcs_jm_par_enhanced.py -t corkscrew

# Combine options
python torcs_jm_par_enhanced.py -p 3001 -t corkscrew -d
```

## Performance

Expected results with default settings:

- **Lap Time**: ~70-80 seconds per lap
- **Average Speed**: 140-160 km/h
- **Completion**: 3 laps without crashing
- **Fuel Used**: Minimal (depends on car)

Actual times depend on your hardware and TORCS physics settings.

## Troubleshooting

### "Waiting for server on 3001"

**Solution**: Make sure TORCS race is started and waiting:
1. In TORCS, go to Quick Race → Configure → Start Race
2. The race should be paused/waiting for AI connection
3. Then run the Python script

### Car won't move

**Solution**: 
- Check TORCS connection is active
- Verify port 3001 is free (or use -p option with different port)
- Check firewall isn't blocking localhost

### Car crashes immediately

**Solution**:
1. Reduce `TARGET_SPEED` to 160
2. Reduce `STEER_GAIN` to 40
3. Increase `BRAKE_THRESHOLD_TIGHT` to 0.45

### Car gets stuck on track

**Solution**:
- The AI has a 20-step recovery system
- If stuck longer than 6 seconds, it applies reverse + steering
- This usually frees the car; wait for recovery

### Inconsistent performance

**Solution**:
- TORCS physics quality affects results
- Physics settings in TORCS config file matter
- Try with "medium" physics for stability

## Architecture

```
TORCS Race Server (Physics Simulation)
         ↓↑ (UDP Port 3001)
   torcs_jm_par_enhanced.py
   (Protocol Handler, Main Loop)
         ↓↑
   AdvancedDriver (corkscrew_driver.py)
   (AI Decision Logic)
         ↓↑
   Control Outputs
   (Steering, Brake, Accel, Gear)
```

## Key Classes

### AdvancedDriver
Main AI class with all driving logic:
- `calculate_steering()` - Steering decisions
- `calculate_brake()` - Braking force
- `calculate_throttle()` - Acceleration
- `apply_traction_control()` - Wheel spin prevention
- `drive()` - Main entry point

### Client
TORCS protocol handler:
- Manages UDP connection
- Receives sensor data
- Sends control commands

### ServerState
Sensor data from TORCS:
- Position, speed, angle
- Track sensors
- Damage, fuel level
- Wheel speeds

## Advanced Features

### Lap Counting
Tracks progress through 3 laps:
```python
driver.lap_count  # Current lap (0, 1, 2, 3)
```

### Stuck Detection
Detects when car is stuck:
```python
stuck = driver.detect_stuck(S)  # True if stuck > 300 steps
```

### Adaptive Braking
Different brake thresholds for different curves:
- Tight: 0.35 radians
- Medium: 0.50 radians
- Sharp: 0.65 radians

### Emergency Braking
Automatic maximum braking for extreme situations:
- Angle > 0.8 radians
- Off-track (trackPos > 0.9)

## Notes

- All speeds are in km/h
- All angles are in radians
- Track sensors read ahead of car
- Steering limited to ±1.0 range
- Throttle and brake limited to 0-1 range

## Future Enhancements

Possible improvements:
- Machine learning for optimal parameters
- Fuel management for long races
- Damage-aware driving (avoid crashes)
- Dynamic difficulty scaling
- Multi-lap optimization
- Opponent avoidance

## References

- TORCS: http://torcs.sourceforge.net/
- SCR Server: http://scr.geccocompetitions.com/
- Snake Oil Library: Original by Chris X Edwards

## Support

For issues:
1. Check troubleshooting section above
2. Verify TORCS is running and race is started
3. Try reducing TARGET_SPEED and STEER_GAIN
4. Enable debug output (-d flag) to see sensor data

## License

See LICENSE file for terms.

---

**Version**: 1.0
**Last Updated**: 2025-01-01
**Python Version**: 3.6+
**TORCS Version**: 1.3.0+
