---
id: ardupilot-autotune
title: "ArduPilot Autotune"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: generic
topic:
  - firmware-autopilot
personas:
  - 1.builder
  - 2.operator
platform:
  - bandit
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

ArduPilot Autotune is an automated PID tuning procedure that characterises
the aircraft's dynamic response by applying a series of controlled input pulses
in AltHold, then calculates optimal rate and attitude PID values from the
measured response. On Bandit and Ghost, Autotune should be run after the first
stable hover confirms the aircraft is airworthy, and before the first autonomous
mission. Default PIDs on a new build are conservative — sufficient for a calm
hover but not for confident autonomous mission execution in wind. Autotune
produces platform-specific values that replace the defaults. The result is
stored in EEPROM and survives power cycles.

---

## Concept

### What Autotune measures

Autotune works by commanding rapid attitude changes on a single axis and
measuring how the aircraft responds. For each axis (roll, pitch, yaw), it
applies step inputs of increasing magnitude and observes the overshoot and
settling time. From these measurements, it derives:

- **Rate P:** how aggressively the aircraft responds to a rate error
- **Rate I:** how aggressively accumulated rate error is corrected
- **Rate D:** how aggressively rate overshoot is damped
- **Angle P:** how aggressively the aircraft responds to an attitude error

The characterisation is specific to the physical aircraft — mass, motor
response time, prop inertia, frame stiffness. A value that is optimal for a
450 g Bandit is not optimal for a 1 360 g Ghost. Autotune must be run
separately on each build.

### Autotune vs Betaflight manual tuning

Betaflight PID tuning relies on the pilot flying specific manoeuvres and
interpreting blackbox logs. Autotune requires no pilot skill beyond maintaining
stable AltHold during the procedure — the aircraft tunes itself. This makes
Autotune accessible to builders who are not experienced tuners, which is
correct for the workshop context where Bandit is built and flown by students.

The trade-off is that Autotune optimises for stability and smoothness rather
than maximum agility. For survey and training missions, this is appropriate.

---

## Reference

**Required conditions before Autotune:**
- Aircraft hovers stably in AltHold (altitude holds without pilot correction)
- GPS lock confirmed (HDOP < 2.0, ≥ 6 satellites)
- Wind below 5 m/s
- Open area with 30 m clear radius
- Battery at full charge (procedure takes 5–15 min; partial battery may abort)

**Key parameters:**
    AUTOTUNE_AGGR,0.1    ; Aggressiveness 0.05–0.1; start at 0.1 for Bandit
    AUTOTUNE_AXES,7      ; Tune all axes (roll + pitch + yaw)

**RC channel assignment:** One RC channel must be assigned AUTOTUNE
(RCx_OPTION=17) before the procedure. A 2-position switch on the TX16S
is standard. Autotune activates when this switch is toggled in AltHold;
it deactivates (and saves) when the switch is toggled back and the aircraft
is landed and disarmed.

---

## Procedure

### Running Autotune on Bandit or Ghost

1. Assign AUTOTUNE to a spare RC channel: set RCx_OPTION=17 for the chosen
   channel. Confirm the switch is in the OFF position before arming.
2. Take off in AltHold. Climb to 15 m minimum. Confirm stable altitude hold.
3. Move to open airspace — 30 m clear radius.
4. Toggle the Autotune switch ON. The aircraft will begin making rapid
   roll inputs. **Do not touch the sticks** during tuning — only use
   sticks if the aircraft drifts into an unsafe position. The procedure is
   working if the aircraft makes deliberate, repetitive roll/pitch pulses.
5. Wait until the aircraft switches to pitch tuning, then yaw tuning.
   Each axis takes 2–5 minutes. QGC will display "AutoTune: Pitch" etc.
6. When all three axes are complete, QGC displays "AutoTune: Success."
7. **Land without disarming.** Toggle the Autotune switch OFF to revert
   to the test tune values temporarily. Disarm. Power cycle.
8. Power on again — the tuned values are saved in EEPROM. Confirm by
   checking RATE_RLL_P, RATE_PIT_P, etc. in QGC parameters.
9. Test-hover in AltHold with the new tune before first Auto mission.

**If Autotune aborts:** battery low, excessive wind, or loss of GPS lock
will abort. Recharge, wait for calmer conditions, and retry. Do not fly
an Auto mission on default PIDs.

---

## Rationale

Autotune is a mandatory pre-mission step on Bandit and Ghost rather than an
optional optimisation because the default ArduPilot PIDs are conservative
enough to produce sluggish attitude response in wind — adequate for a stable
hover but not for maintaining consistent survey altitude over terrain
variations or wind gusts. A survey mission flown on default PIDs on a first
build produces altitude errors that degrade survey quality. Running Autotune
first costs 15 minutes and eliminates a class of mission failure.

---

## Connections

```yaml
requires:
  - [[ardupilot-copter]]
  - [[ardupilot-commissioning]]
  - [[closed-loop-control]]
related:
  - [[pid-tuning-rate-profile]]
  - [[ardupilot-flight-modes]]
  - [[blackbox-analysis]]
leads_to:
  - [[qgroundcontrol]]
  - [[maiden-flight]]
```
