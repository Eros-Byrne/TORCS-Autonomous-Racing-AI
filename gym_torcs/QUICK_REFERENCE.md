# Quick Reference - TORCS Corkscrew AI

## 30-Second Start

```bash
# Terminal 1: Start TORCS
torcs -nofuel -nodamage -nolaptime &

# In TORCS: Race → Quick Race → Configure
# Track: corkscrew, Laps: 3, Start Race

# Terminal 2: Run AI
python torcs_jm_par_enhanced.py -p 3001

# Watch the car complete 3 laps!
```

## Key Controls

| File | What It Does |
|------|-------------|
| `corkscrew_driver.py` | **AI Brain** - Edit to tune behavior |
| `torcs_jm_par_enhanced.py` | **Main Program** - Run this! |
| `torcs_jm_par.py` | Original version with modular logic |

## Tuning in 30 Seconds

Edit `corkscrew_driver.py`, class `DrivingConfig`:

```python
# Faster driving
TARGET_SPEED = 200  # Default: 185

# Smoother cornering (less twitchy)
STEER_GAIN = 45  # Default: 55

# Better on curves
CENTERING_GAIN = 0.85  # Default: 0.75

# Brake earlier
BRAKE_THRESHOLD_TIGHT = 0.25  # Default: 0.35
```

## Common Issues & Fixes

| Problem | Fix |
|---------|-----|
| "Waiting for server" | Start race in TORCS first! |
| Car crashes | Lower TARGET_SPEED to 160 |
| Car too slow | Raise TARGET_SPEED to 200 |
| Won't turn enough | Raise STEER_GAIN to 60 |
| Slides on curves | Lower TARGET_SPEED by 20 |
| Gets stuck | Wait 20 sec, has recovery logic |

## Command Line

```bash
python torcs_jm_par_enhanced.py [options]

-p 3001              # Port (where TORCS listens)
-H localhost         # Host/IP address
-t corkscrew         # Track name
-d                   # Debug output
-h                   # Show help
```

## What Each Parameter Does

### Speed Control
- `TARGET_SPEED`: Sets target speed (km/h)
  - 160 = cautious/stable
  - 185 = balanced (default)
  - 210 = aggressive/fast

- `ACCEL_GAIN`: How fast to accelerate
  - Higher = faster response

- `ACCEL_DECAY`: How fast to brake (speed)
  - Higher = stronger braking

### Steering Control
- `STEER_GAIN`: Steering sensitivity
  - Lower (35) = smooth/conservative
  - Higher (60) = responsive/sharp

- `CENTERING_GAIN`: Keep car centered
  - Lower = less correction
  - Higher = more aggressive centering

### Braking Control
- `BRAKE_THRESHOLD_*`: When to brake
  - TIGHT: Sharp curves (tightest)
  - MEDIUM: Normal curves
  - SHARP: Extreme angles

- `BRAKE_FORCE`: How hard to brake
  - 0.3 = gentle
  - 0.6 = normal (default)
  - 0.85 = emergency

### Advanced Options
- `ENABLE_TRACTION_CONTROL`: Prevent wheel spin
- `ENABLE_SPIN_PREVENTION`: Stop spinouts
- `CORKSCREW_CORRECTION`: Extra steering for spiral geometry

## Expected Performance

With **default settings**:
- ✓ Completes 3 laps reliably
- ✓ Average lap time: 70-80 seconds
- ✓ Average speed: 140-160 km/h
- ✓ No crashes if track clear

## Physics Sensors Used

```
S['speedX']           # Forward speed
S['angle']            # Car angle vs track
S['trackPos']         # Position (-1=left, 0=center, 1=right)
S['track']            # Distance sensors (19 points ahead)
S['wheelSpinVel']     # Wheel rotation speeds
S['stucktimer']       # Stuck counter
S['distFromStart']    # Distance in lap
S['damage']           # Damage accumulation
```

## Control Commands Sent

```
R['steer']            # Steering (-1 to 1)
R['accel']            # Throttle (0 to 1)
R['brake']            # Braking (0 to 1)
R['gear']             # Gear (1-6)
R['clutch']           # Clutch (0 to 1)
```

## Monitoring Output

```
Lap: 1 | Speed: 145.2 km/h | Distance: 850m
Lap: 2 | Speed: 152.1 km/h | Distance: 2100m
Lap: 3 | Speed: 148.5 km/h | Distance: 3200m
```

## File Locations

```
gym_torcs/
├── corkscrew_driver.py           ← Edit this to tune!
├── torcs_jm_par_enhanced.py      ← Run this!
├── torcs_jm_par.py               ← Original version
├── snakeoil3_jm2.py              ← Protocol library
├── README_CORKSCREW_AI.md        ← Full documentation
├── QUICK_REFERENCE.md            ← This file
└── setup_corkscrew.py            ← Setup helper
```

## One-Minute Tuning Checklist

- [ ] Can it complete 3 laps? (If no: lower speed, brake earlier)
- [ ] Is it smooth? (If jittery: lower STEER_GAIN)
- [ ] Is it fast? (If slow: raise TARGET_SPEED, ACCEL_GAIN)
- [ ] Does it stay on track? (If off: raise CENTERING_GAIN)
- [ ] Does it crash? (If yes: lower all speeds/gains)

## When Everything Works

You should see:
1. Car appears in TORCS
2. Car drives smoothly around Corkscrew
3. Python shows lap counter increasing
4. 3 complete laps without crashes
5. Race finishes successfully

---

💡 **Pro Tip**: Start with defaults, increase speed 5 km/h at a time until crashes, then back off 20 km/h.

🎯 **Goal**: 3 laps completed ✓

🚗 **Happy Racing!**
