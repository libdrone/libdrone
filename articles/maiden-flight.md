---
id: maiden-flight
title: "Maiden flight"
version: 1.0.1
date: 2026-05-31
author: jsa
status: released
scope: libdrone
topic:
  - piloting-operations
personas:
  - 1.builder
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The maiden flight is a structured measurement event, not a demonstration.
Its purpose is to collect Blackbox data, verify structural behaviour under
load, confirm motor balance, and validate the low-speed calibration. The
sequence is: hover only at 1m for 30 seconds, land, inspect motors and
mounts, download Blackbox, review gyro spectrum. Only after the Blackbox
review confirms the build is within spec does the flight programme expand
to normal operations. Every deviation from expectation is information —
log it, not explain it away.

---

## Concept

### What the maiden answers

A maiden flight does not answer "does the drone fly?" — the acceptance
validation already confirmed it should. The maiden answers:

- **How does this specific build fly?** Motor balance, PID response, gyro
  noise floor. These are properties of the assembled hardware, not the design.
- **Where are the weak points?** Vibration level, motor temperature, T-lock
  engagement under dynamic load.
- **Is the Blackbox logging correctly?** The maiden is the first real
  confirmation that data collection infrastructure works.
- **Is the low-speed calibration accurate?** GPS speed at full throttle in
  SB position 1 (low-speed) must be ≤ 4.8 m/s under actual flight conditions
  with actual payload weight.

### Maiden as the first flight in a data series

Every subsequent flight builds on the maiden baseline. If the maiden Blackbox
shows an elevated noise floor at 200–400 Hz, all future Blackbox recordings
should show the same profile — if a later flight shows a higher floor, something
has changed in the hardware. The maiden establishes the reference.

---

## Reference

### Maiden flight sequence

**Pre-maiden (site)**
- Open outdoor site, minimum 20m from people and obstacles
- Confirm GPS fix ≥ 8 satellites before arming
- Confirm transmitter on before battery connected
- Confirm Blackbox logging active (flash indicator in OSD)

**Hover sequence (Phase 1)**
1. Arm. Apply throttle smoothly to ~40% — observe lift-off.
2. Hover at 1m altitude for 30 seconds. Listen for abnormal sounds.
3. Observe stability: should hold position without significant drift.
4. Land. Disarm. Do not continue until Phase 1 inspection is complete.

**Post-hover inspection**
5. Feel all 4 motor housings: warm is acceptable (35–55°C), hot is not (>65°C).
6. Press each arm laterally: no play or movement at T-lock.
7. Check all motor mount passive covers: not cracking or displaced.
8. Verify no unexpected vibration marks on the Platform (contact traces, fretting).

**If Phase 1 passes — expand flight programme**
9. Fly a slow circuit at 5–10m altitude, gentle inputs.
10. Perform a GPS Rescue test: fly 30m out, 15m altitude, activate SE switch.
    Verify return-to-home. Recover via SE switch release.
11. Low-speed calibration check: full throttle straight pass in SB position 1,
    read GPS speed in OSD. Must be ≤ 4.8 m/s.
12. Land. Download Blackbox.

**Post-maiden Blackbox review**
13. Open Blackbox Explorer. Gyro spectrum analyser view.
14. Check noise floor in 0–200Hz range: should be below −40 dB.
15. Check for motor RPM harmonic peaks: should be absent (RPM filter working).
16. Check gyro time trace for a sharp input segment: 1–2 oscillation cycles
    to settle = correctly tuned. 3+ cycles = P too high or D too low.
17. Log all findings in build record.

---

## Procedure

### If motor is hot after hover

Motor temperature above 65°C after a 30-second hover at low throttle
indicates a problem. Stop. Do not continue maiden.

Investigate in this order:
1. Verify motor direction is correct for that motor position
2. Verify propeller is seated fully and nut is torqued
3. Verify MR30 connector is fully mated (not partially inserted)
4. Review Blackbox motor output for that motor — if significantly higher than
   others, the motor is working harder to compensate for an issue elsewhere

### If GPS Rescue does not activate

If SE switch does not trigger GPS Rescue:
1. Verify satellite count was ≥ 8 at arm time (GPS Rescue disabled if < 8 at arm)
2. Verify GPS Rescue is enabled in Betaflight Failsafe tab
3. Verify SE switch channel assignment in Betaflight Modes tab

Do not operate the drone in environments where GPS Rescue is operationally
required until this is resolved.

---

## Rationale

### Why hover-only for Phase 1

Aggressive manoeuvring on the maiden flight provides no additional information
beyond the hover — the Blackbox gyro spectrum and motor balance are visible
in hover data. Aggressive manoeuvring adds crash risk before the baseline is
established. Phase 1 hover-only is conservative by design; the flight
programme expands only after the build is confirmed structurally and
electronically within spec.

---

## Connections

requires:
  - [[acceptance-validation]]
  - [[betaflight-setup]]
  - [[betaflight-gps-rescue]]
related:
  - [[blackbox-analysis]]
  - [[pid-tuning-rate-profile]]
  - [[scheduled-maintenance]]
leads_to:
  - [[blackbox-analysis]]
  - [[scheduled-maintenance]]
