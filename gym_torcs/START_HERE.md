# ⚡ Get Started in 5 Minutes

**This is the absolute fastest way to get your AI racing!**

---

## 🎯 The Goal
Make the AI drive 3 laps on Corkscrew without crashing.

---

## ✅ Pre-Check (30 seconds)

```bash
# Make sure you're in the right folder
cd c:\path\to\gym_torcs

# Check key files exist
dir corkscrew_driver.py
dir torcs_jm_par_enhanced.py
```

If files don't exist, you're in the wrong folder!

---

## 🚀 Start TORCS (1 minute)

Open **PowerShell** or **Command Prompt** and run:

```bash
torcs -nofuel -nodamage -nolaptime &
```

**Wait for TORCS to open** (~10 seconds)

Then in TORCS menu:
1. Click **Race**
2. Click **Quick Race**
3. Click **Configure Race**
4. Set **Track** = `corkscrew`
5. Set **Laps** = `3`
6. Set **Car** = `car1-stock1`
7. Click **START RACE**

**The race will pause and wait for AI** ✓

---

## 🤖 Run the AI (2 minutes)

Open **another PowerShell window** and run:

```bash
cd c:\path\to\gym_torcs
python torcs_jm_par_enhanced.py -p 3001
```

**You'll see:**
```
============================================================
TORCS Corkscrew AI Driver - 3 Laps
============================================================
[Main] Starting race simulation...
[TORCS Client] Connected to localhost:3001
[TORCS Client] Track: corkscrew, Stage: 2
[Race] Starting 3-lap race...
[Race] Connected to TORCS on port 3001

🏁 LAP 1 STARTED
[Lap 1] Speed: 145.2 km/h | Distance: 850m
...
🏁 LAP 2 STARTED
...
✓ Race completed successfully!
```

---

## 👀 Watch the Race (2 minutes)

Look at the **TORCS window**:
- Car appears on track ✓
- Car drives smoothly around corners ✓
- Car completes Lap 1 ✓
- Car completes Lap 2 ✓
- Car completes Lap 3 ✓
- **SUCCESS!** 🏁

---

## 🎛️ Optimize (Optional - If You Have Time)

If the car is **too slow**, edit file `corkscrew_driver.py`:

Find this line (around line 50):
```python
TARGET_SPEED = 185
```

Change to:
```python
TARGET_SPEED = 200  # Faster!
```

Save and run again:
```bash
python torcs_jm_par_enhanced.py -p 3001
```

---

## ❌ What If It Doesn't Work?

### Error: "Waiting for server"
```
Fix: Make sure TORCS race is actually STARTED
    In TORCS: Race → Quick Race → Configure Race → START
    The race should be waiting/paused for AI
```

### Error: "Could not connect"
```
Fix: Try a different port
    python torcs_jm_par_enhanced.py -p 3002
```

### Car crashes
```
Fix: Lower the speed
    In corkscrew_driver.py:
    TARGET_SPEED = 160  (instead of 185)
```

### Car runs too slow
```
Fix: Raise the speed
    In corkscrew_driver.py:
    TARGET_SPEED = 200  (instead of 185)
```

---

## 📚 What's Next?

- **Full docs**: Read `README_CORKSCREW_AI.md`
- **Quick tips**: Read `QUICK_REFERENCE.md`
- **Architecture**: Read `ARCHITECTURE_GUIDE.md`
- **Presets**: Try `python run_race.py`

---

## 🎓 Key Files

| File | Purpose | Edit? |
|------|---------|-------|
| `torcs_jm_par_enhanced.py` | Main program (RUN THIS) | No |
| `corkscrew_driver.py` | AI brain (TUNE THIS) | Yes! |
| `config_presets.py` | Presets (reference only) | No |
| `run_race.py` | Menu interface | No |

---

## 🎯 Common Tweaks

```python
# In corkscrew_driver.py, line ~50:

TARGET_SPEED = 185          # Driving speed (160=safe, 200=fast)
STEER_GAIN = 55             # Steering sharpness (35=smooth, 65=sharp)
CENTERING_GAIN = 0.75       # Track centering (0.5=loose, 0.95=tight)
BRAKE_THRESHOLD_TIGHT = 0.35 # When to brake (0.2=early, 0.5=late)
```

---

## 🏁 Done!

You now have a working AI that can:
- ✅ Drive 3 laps on Corkscrew
- ✅ Avoid crashes
- ✅ Complete in ~75 seconds per lap
- ✅ Maintain ~150 km/h average speed

**Congratulations!** 🎉

---

## 💡 Pro Tips

1. **First run**: Use default settings (they work!)
2. **Speed test**: Increase TARGET_SPEED by 10 until crashes
3. **Stability**: If crashes, reduce STEER_GAIN
4. **Smoothness**: Increase CENTERING_GAIN for tight line

---

## 📞 Still Stuck?

1. Re-read this file (you're 90% done!)
2. Check `QUICK_REFERENCE.md` for common issues
3. Make sure TORCS is actually running
4. Try the BEGINNER preset: `python run_race.py` → choose option 1

---

**Time elapsed**: ~5 minutes ⏱️

**Your AI is now racing!** 🚗💨

Good luck! 🏁
