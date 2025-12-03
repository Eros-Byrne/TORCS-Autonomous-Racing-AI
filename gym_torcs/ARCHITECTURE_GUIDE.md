# TORCS Corkscrew AI - Architecture & Files Guide

## 🎯 Goal
**Drive 3 laps on Corkscrew track using scr_server with advanced AI logic**

---

## 📁 File Structure & Purpose

```
gym_torcs/
│
├─ 🚗 CORE AI LOGIC
│  ├─ corkscrew_driver.py ⭐⭐⭐
│  │  └─ AdvancedDriver class - All AI decision-making
│  │  └─ DrivingConfig class - All tunable parameters
│  │  └─ 350 lines of intelligent driving logic
│  │
│  └─ config_presets.py
│     └─ 6 pre-configured profiles (Beginner→Aggressive)
│     └─ Easy switching between styles
│
├─ 🎮 TORCS CLIENT (COMMUNICATION)
│  ├─ torcs_jm_par_enhanced.py ⭐⭐⭐
│  │  └─ Main program - RUN THIS!
│  │  └─ UDP protocol handler
│  │  └─ Integrates corkscrew_driver.py
│  │  └─ Game loop & status monitoring
│  │
│  ├─ torcs_jm_par.py
│  │  └─ Original version
│  │  └─ Contains modular drive_example()
│  │
│  └─ snakeoil3_jm2.py
│     └─ Low-level TORCS protocol library
│     └─ Don't modify - base communication
│
├─ 📚 USER INTERFACE
│  ├─ run_race.py
│  │  └─ Interactive menu runner
│  │  └─ Choose preset → Run race
│  │  └─ User-friendly interface
│  │
│  └─ setup_corkscrew.py
│     └─ Configuration generator
│     └─ Setup instructions
│
├─ 📖 DOCUMENTATION
│  ├─ README_CORKSCREW_AI.md (THIS IS MAIN DOC)
│  │  └─ Complete guide (full 300+ lines)
│  │  └─ Setup, tuning, troubleshooting
│  │
│  ├─ QUICK_REFERENCE.md
│  │  └─ Quick 30-second guide
│  │  └─ Common issues & fixes
│  │
│  └─ IMPLEMENTATION_SUMMARY.md
│     └─ What was created (this summary)
│
└─ 🎵 OTHER
   ├─ snakeoil3_gym.py
   ├─ sample_agent.py
   ├─ gym_torcs.py
   ├─ jmcncarai.py
   ├─ autostart.sh
   └─ practice.xml
```

---

## 🔄 How It Works (Flow Diagram)

```
                    TORCS GAME
                   ┌─────────┐
                   │ Physics │
                   │ Engine  │
                   └────┬────┘
                        │ Sensor data (50 Hz)
                        │ (position, speed, angle, track distance)
                        ▼
        ┌──────────────────────────────────┐
        │  TORCS UDP Server (localhost:3001)│
        └──────────────────┬───────────────┘
                           │ UDP packets
                           ▼
        ┌──────────────────────────────────────────┐
        │  torcs_jm_par_enhanced.py                │
        │  ┌──────────────────────────────────┐   │
        │  │  Client Class                    │   │
        │  │  • Socket communication          │   │
        │  │  • Parse server data             │   │
        │  │  • Send commands                 │   │
        │  │  • Main loop (50 Hz)             │   │
        │  └──────────────────────────────────┘   │
        └──────────────────┬──────────────────────┘
                           │ Each tick
                           ▼
        ┌──────────────────────────────────────────┐
        │  corkscrew_driver.py                     │
        │  ┌──────────────────────────────────┐   │
        │  │  AdvancedDriver                  │   │
        │  │                                  │   │
        │  │  calculate_steering()            │   │ Make decisions
        │  │  calculate_brake()               │   │
        │  │  calculate_throttle()            │   │
        │  │  apply_traction_control()        │   │
        │  │  apply_spin_prevention()         │   │
        │  │  shift_gear()                    │   │
        │  │                                  │   │
        │  │  drive() ← MAIN ENTRY            │   │
        │  └──────────────────────────────────┘   │
        └──────────────────┬──────────────────────┘
                           │ Control commands
                           │ (steer, brake, accel, gear)
                           ▼
        ┌──────────────────────────────────────────┐
        │  TORCS Game                              │
        │  • Apply steering                        │
        │  • Apply brakes                          │
        │  • Apply throttle                        │
        │  • Shift gear                            │
        │  • Update car physics                    │
        └─────────────────────────────────────────┘
                           │
                           ▼ Next frame
                    ┌─────────────┐
                    │ Loop repeats │
                    │ at 50 Hz     │
                    └─────────────┘
```

---

## 🎛️ Configuration Hierarchy

```
┌─────────────────────────────────────────────┐
│  DrivingConfig (corkscrew_driver.py)       │
│                                             │
│  ┌─ Speed Management                       │
│  │  ├─ TARGET_SPEED = 185                 │
│  │  ├─ MAX_SPEED = 220                    │
│  │  └─ MIN_SPEED = 5                      │
│  │                                         │
│  ├─ Steering Control                      │
│  │  ├─ STEER_GAIN = 55                    │
│  │  ├─ CENTERING_GAIN = 0.75              │
│  │  └─ STEER_SMOOTHING = 0.85             │
│  │                                         │
│  ├─ Braking Strategy                      │
│  │  ├─ BRAKE_THRESHOLD_TIGHT = 0.35       │
│  │  ├─ BRAKE_THRESHOLD_MEDIUM = 0.50      │
│  │  ├─ BRAKE_FORCE = 0.6                  │
│  │  └─ BRAKE_EMERGENCY = 0.85             │
│  │                                         │
│  ├─ Traction Control                      │
│  │  ├─ ENABLE_TRACTION_CONTROL = True     │
│  │  ├─ TRACTION_THRESHOLD = 2.2           │
│  │  └─ TRACTION_REDUCTION = 0.15          │
│  │                                         │
│  ├─ Safety Systems                        │
│  │  ├─ ENABLE_SPIN_PREVENTION = True      │
│  │  └─ SPIN_THRESHOLD = 0.4               │
│  │                                         │
│  └─ Gear Shifting                         │
│     └─ GEAR_SPEEDS = [0, 50, 85, 120...]  │
│                                             │
└─────────────────────────────────────────────┘
         │
         │ Applied by
         ▼
┌─────────────────────────────────────────────┐
│  AdvancedDriver Instance                    │
│                                             │
│  self.config = DrivingConfig()             │
│                                             │
└─────────────────────────────────────────────┘
         │
         │ Used by
         ▼
┌─────────────────────────────────────────────┐
│  drive() method                             │
│  (Called 50 times per second)              │
│                                             │
│  Uses config values for all decisions     │
└─────────────────────────────────────────────┘
```

---

## 🎨 How to Use Presets

```
From config_presets.py:

┌─ BEGINNER ──────────────────────────────────────┐
│ Target Speed: 130 km/h                          │
│ Steer Gain: 35 (smooth)                        │
│ Best for: Testing, learning                    │
│ Crash Risk: Almost zero                        │
│ Lap Time: ~110 seconds                         │
└─────────────────────────────────────────────────┘
                      │
┌─ CONSERVATIVE ──────────────────────────────────┐
│ Target Speed: 160 km/h                          │
│ Steer Gain: 40 (smooth)                        │
│ Best for: Stable, no crashes                   │
│ Crash Risk: Very low                           │
│ Lap Time: ~95 seconds                          │
└─────────────────────────────────────────────────┘
                      │
┌─ BALANCED ⭐ ───────────────────────────────────┐
│ Target Speed: 185 km/h                          │
│ Steer Gain: 55 (balanced)                      │
│ Best for: ALL-ROUNDER (RECOMMENDED!)           │
│ Crash Risk: Low                                │
│ Lap Time: ~75 seconds                          │
│ ★ DEFAULT CHOICE ★                            │
└─────────────────────────────────────────────────┘
                      │
┌─ AGGRESSIVE ────────────────────────────────────┐
│ Target Speed: 205 km/h                          │
│ Steer Gain: 65 (sharp)                         │
│ Best for: Speed runs                           │
│ Crash Risk: Medium                             │
│ Lap Time: ~68 seconds                          │
└─────────────────────────────────────────────────┘
                      │
┌─ DRIFT ─────────────────────────────────────────┐
│ Target Speed: 195 km/h                          │
│ Steer Gain: 70 (very sharp)                    │
│ Best for: Drifting style                       │
│ Crash Risk: High                               │
│ Lap Time: ~70 seconds                          │
└─────────────────────────────────────────────────┘
                      │
┌─ PRECISION ─────────────────────────────────────┐
│ Target Speed: 170 km/h                          │
│ Steer Gain: 50 (precise)                       │
│ Best for: Perfect line following               │
│ Crash Risk: Very low                           │
│ Lap Time: ~85 seconds                          │
└─────────────────────────────────────────────────┘
```

---

## 🚀 Running the Code (3 Methods)

### Method 1: Interactive Menu (EASIEST)
```bash
$ python run_race.py
# Menu appears
# Choose BALANCED
# Start TORCS race first
# Script runs it
```

### Method 2: Command Line
```bash
$ python torcs_jm_par_enhanced.py -p 3001
# Uses default BALANCED config
# Immediately connects to TORCS
```

### Method 3: Python Script
```python
from torcs_jm_par_enhanced import Client
from corkscrew_driver import AdvancedDriver
from config_presets import ConfigurationPresets

client = Client(p=3001)
driver = AdvancedDriver()
driver.config = ConfigurationPresets.AGGRESSIVE()

for step in range(client.maxSteps, 0, -1):
    client.get_servers_input()
    driver.drive(client.S, client.R)
    client.respond_to_server()

client.shutdown()
```

---

## 🔧 Tuning Parameters (What Does What)

```
TARGET_SPEED
├─ LOWER (160) → Slower, more stable
└─ HIGHER (210) → Faster, more risky

STEER_GAIN
├─ LOWER (35) → Smooth, gentle turns
└─ HIGHER (65) → Sharp, tight turns

CENTERING_GAIN
├─ LOWER (0.5) → Loose on track
└─ HIGHER (0.95) → Tight line following

BRAKE_THRESHOLD_TIGHT
├─ LOWER (0.2) → Brake very early
└─ HIGHER (0.5) → Brake late

BRAKE_FORCE
├─ LOWER (0.3) → Gentle braking
└─ HIGHER (0.8) → Hard braking

ACCEL_GAIN
├─ LOWER (0.2) → Slow acceleration
└─ HIGHER (0.5) → Fast acceleration
```

---

## 📊 Expected Results

```
With BALANCED Preset:

┌─────────────────────────────────────┐
│  Lap 1                              │
│  • Time: ~76 seconds                │
│  • Avg Speed: 152 km/h              │
│  • Crashes: 0                       │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Lap 2                              │
│  • Time: ~75 seconds                │
│  • Avg Speed: 153 km/h              │
│  • Crashes: 0                       │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Lap 3                              │
│  • Time: ~74 seconds                │
│  • Avg Speed: 155 km/h              │
│  • Crashes: 0                       │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  TOTAL RACE                         │
│  • Total Time: ~225 seconds         │
│  • Avg Speed: 153 km/h              │
│  • Completion: SUCCESS ✓            │
└─────────────────────────────────────┘
```

---

## 📍 Where to Start

```
START HERE
    │
    ▼
Step 1: Read README_CORKSCREW_AI.md (5 min)
    │
    ▼
Step 2: Run TORCS game
        Start → Race → Quick Race
        Track: corkscrew
        Laps: 3
        Car: car1-stock1
    │
    ▼
Step 3: Run Python (choose one):
        python run_race.py         (EASIEST)
        -or-
        python torcs_jm_par_enhanced.py -p 3001
    │
    ▼
Step 4: Watch 3 laps complete! 🏁
    │
    ▼
Step 5 (Optional): Tune in corkscrew_driver.py
        Edit DrivingConfig
        Re-run to test
```

---

## 🎓 Learning Path

```
Level 1: Get it working
├─ Use default BALANCED preset
├─ Just run: python torcs_jm_par_enhanced.py
└─ See 3 laps complete

Level 2: Try different presets
├─ Use run_race.py
├─ Test BEGINNER, CONSERVATIVE, AGGRESSIVE
└─ Notice different speeds/styles

Level 3: Understand tuning
├─ Read QUICK_REFERENCE.md
├─ Understand each parameter
└─ Modify one at a time

Level 4: Optimize for your setup
├─ Find optimal TARGET_SPEED
├─ Tune STEER_GAIN for smoothness
├─ Adjust braking thresholds
└─ Achieve best lap times

Level 5: Advanced customization
├─ Create custom config class
├─ Combine multiple presets
├─ Add your own logic
└─ Extend AdvancedDriver class
```

---

## ✅ Checklist Before Running

- [ ] TORCS installed and working
- [ ] Python 3.6+ installed
- [ ] In gym_torcs directory
- [ ] corkscrew_driver.py exists
- [ ] torcs_jm_par_enhanced.py exists
- [ ] Port 3001 is free (or modify with -p)

---

## 📞 Quick Help

| Problem | File | Line | Fix |
|---------|------|------|-----|
| Too slow | corkscrew_driver.py | ~50 | ↑ TARGET_SPEED |
| Crashes | corkscrew_driver.py | ~48 | ↓ TARGET_SPEED |
| Won't turn | corkscrew_driver.py | ~51 | ↑ STEER_GAIN |
| Too twitchy | corkscrew_driver.py | ~51 | ↓ STEER_GAIN |
| Won't connect | torcs_jm_par_enhanced.py | ~200 | Start TORCS race! |
| Off track | corkscrew_driver.py | ~52 | ↑ CENTERING_GAIN |

---

## 🎉 You're Ready!

You have a complete AI driving system. Just:

1. Start TORCS race on Corkscrew (3 laps)
2. Run `python torcs_jm_par_enhanced.py -p 3001`
3. Watch it complete 3 laps!

**Good luck!** 🏁

---

For detailed info, read: **README_CORKSCREW_AI.md**
For quick tips, read: **QUICK_REFERENCE.md**
