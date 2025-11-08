# Keyboard Controls Guide

## Available Commands

### During Operation:

| Key | Action | Description |
|-----|--------|-------------|
| **L** | Lock Toggle | Turn auto-tracking ON/OFF |
| **C** | Center | Return servos to default position (90°, 90°) |
| **Q** | Quit | Exit the program |

---

## Lock Toggle (L Key)

### When Auto-Lock is ON (default):
- System automatically locks to the first person detected
- Follows that person until they disappear for >2 seconds
- Status shows: `LOCKED ID:X` or `SEARCHING`

Press **L** to:
- Unlock from current target
- Disable auto-locking
- Status changes to: `MANUAL MODE (Lock OFF)`

### When Auto-Lock is OFF (manual mode):
- System will NOT lock onto people
- Can freely center servos with **C** key
- Status shows: `MANUAL MODE (Lock OFF)`

Press **L** to:
- Re-enable auto-locking
- Will lock to next person detected
- Status returns to: `SEARCHING`

---

## Center Button (C Key)

### When Unlocked:
- Press **C** to center servos
- Servos move to: Pan=90°, Tilt=90°
- Sweep position also resets
- Useful for:
  - Starting from neutral position
  - Manual camera adjustment
  - Resetting after tracking

### When Locked to Target:
- **C** key is disabled
- Message: "Cannot center - locked to target"
- Must press **L** first to unlock
- This prevents accidental interruption of tracking

---

## Usage Scenarios

### Scenario 1: Normal Operation
1. Start system (auto-lock ON by default)
2. System detects and locks to first person
3. Tracks person automatically
4. Person leaves → unlocks after 2 seconds → resumes sweep

### Scenario 2: Manual Control
1. Press **L** to disable auto-lock
2. System enters manual mode (no tracking)
3. Press **C** to center camera
4. Press **L** again when ready to resume tracking

### Scenario 3: Switch Targets
1. System locked to Person A
2. Press **L** to unlock
3. Wait for Person B to be detected
4. System automatically locks to Person B

### Scenario 4: Demonstration Mode
1. Press **L** to disable auto-lock
2. People can walk by without being tracked
3. Press **C** to center between demonstrations
4. Press **L** to resume normal operation

---

## Visual Indicators

### Status Display (Top Left):
- `SEARCHING` - Looking for a person to track
- `LOCKED ID:123 (2.3s)` - Tracking person 123 for 2.3 seconds
- `MANUAL MODE (Lock OFF)` - Auto-tracking disabled

### Bounding Boxes:
- **Green box (thick)** - Locked target being tracked
- **Blue boxes (thin)** - Other detected people (ignored)

### Servo Angles:
- Displayed as: `Pan: 90.0  Tilt: 90.0`
- Updates in real-time

---

## Tips

### Smooth Operation:
- Use **C** to reset position before starting tracking
- Center position gives servos maximum range of motion

### Testing:
- Press **L** to disable tracking while testing servo limits
- Use **C** to return to safe position

### Performance:
- Manual mode (Lock OFF) still runs detection
- No performance difference between modes
- Only tracking behavior changes

### Safety:
- **C** button blocked when locked prevents accidents
- Always unlock first with **L** if you need to center

---

## Console Messages

You'll see these messages when pressing keys:

```
[TRACK] Manually unlocked from target ID: 5
[TRACK] Auto-lock DISABLED - Press 'L' to enable

[TRACK] Auto-lock ENABLED - Will lock to next person detected

[SERVO] Centering to default position...

[SERVO] Cannot center - locked to target. Press 'L' to unlock first.
```

---

## Quick Reference Card

**Want to stop tracking?** → Press **L**  
**Want to center camera?** → Press **C** (if unlocked)  
**Want to resume tracking?** → Press **L** again  
**Want to quit?** → Press **Q**

---

**Default State**: Auto-lock ON, servos centered at 90°/90°
