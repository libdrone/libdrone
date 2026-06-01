---
id: sk-ardupilot-operator-guide
title: "ArduPilot Operator Guide"
version: 1.0.0
date: 2026-04-15
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 2.operator
  - 4.workshop
  - 1.builder
platform:
  - bandit
  - ghost
  - wing
lang: en
licence: CC BY-SA 4.0
---

## Summary

After reading this guide, an operator can commission, configure, and fly any
ArduPilot-based libdrone platform — Bandit, Ghost, or Wing. The guide covers
the full sequence from firmware flash to autonomous mission, with platform-
specific notes where the three variants diverge. Learning objective: the
operator can execute a complete survey mission in QGroundControl with correct
failsafe configuration, and can diagnose the most common commissioning failures.

---

## Concept

### Why ArduPilot is different

libdrone Pro and Core run Betaflight — a firmware optimised for fast manual
flight, configured in minutes, tuned by blackbox analysis. Bandit, Ghost,
and Wing run ArduPilot — a full autopilot stack designed for autonomous
mission execution, GPS-guided flight modes, and MAVLink integration with
ground control systems and tactical networks.

The operational model is different. A Betaflight pilot configures the drone
once and then flies manually, with GPS Rescue as a background failsafe. An
ArduPilot operator plans a mission in QGroundControl, uploads it, arms in
Loiter, switches to Auto, and monitors from the ground while the aircraft
executes the plan. Intervention is available but not expected.

→ [[ardupilot-copter]] explains this distinction in full — understanding why
ArduPilot exists and what it enables is more important than memorising its
parameter names.

### The commissioning order matters

ArduPilot commissioning has strict dependencies. Each step assumes the
previous one is complete:

1. Flash correct firmware target for the platform
2. Configure ELRS MAVLink mode (UART2) — without this, RC calibration fails silently
3. Configure GPS and compass (UART3) — without this, Loiter refuses to arm
4. Calibrate sensors (accelerometer, compass, RC) — in that order
5. Set failsafe parameters — before any flight, including bench tests
6. Motor test — props off, confirm correct spin directions
7. Autotune — before first autonomous mission

Skipping or reordering steps produces failures that are difficult to diagnose.
→ [[ardupilot-commissioning]] walks each step with the exact parameter values.

---

## Reference

### Platform differences at commissioning

| Step | Bandit | Ghost | Wing |
|---|---|---|---|
| Firmware target | MatekH7A3 (Copter) | MatekH7A3 (Copter) | MatekH7A3-WING (Plane) |
| UART2 protocol | MAVLink2 (RC+telemetry) | ← same | ← same |
| UART3 | GPS (M8Q) | ← same | GPS (M10Q) |
| Battery failsafe | LiPo thresholds | Li-Ion thresholds | LiPo thresholds |
| Autotune | Required | Required | TECS calibration |
| GCS | QGroundControl | ← same | QGroundControl |

---

## Procedure

### ELRS MAVLink mode — the critical first step

Before any other commissioning, ELRS MAVLink mode must be configured.
The H7A3-SLIM ships with SERIAL2_PROTOCOL=23 (RCIN). This must be changed to
SERIAL2_PROTOCOL=2 (MAVLink2). RC channels travel inside the MAVLink stream —
leaving the protocol on RCIN produces a drone with no radio control.

→ [[elrs-mavlink-mode]] explains the mechanism and provides the complete
parameter set. Verify the fix: connect QGroundControl and confirm that moving
TX16S sticks produces live channel inputs in the Radio Calibration screen.

### Sensor calibration sequence

1. **Accelerometer** (6-position): hold each face of the drone toward the
   ground in sequence per QGC prompts. Level matters — do this on a flat
   surface with the drone at its flight orientation.
2. **Compass**: rotate the drone through all axes until QGC confirms. Perform
   this away from ferrous objects and motor current. The external QMC5883L
   on the GPS mast is the only compass used (COMPASS_USE2=0 disables the
   internal FC compass).
3. **RC**: move all sticks and switches through full range. Verify mode
   switches produce correct mode names in QGC.

→ [[ardupilot-commissioning]] has the full parameter reference.
→ [[barometer-magnetometer]] explains why compass isolation matters.

### Flight mode progression

→ [[ardupilot-flight-modes]] maps the six modes and their sensor dependencies.
The training sequence for new Bandit operators:

**Phase 1 — Stabilize**: manual rate control, IMU only. No GPS, no baro.
Fly this until you understand what "no automation" feels like.

**Phase 2 — AltHold**: barometer-locked altitude. Practice transitions
between Stabilize and AltHold until mode switching is instinctive.

**Phase 3 — Loiter**: GPS position hold. Verify GPS lock (HDOP < 2.0,
≥ 8 satellites) before entering Loiter. Practice recovering to Loiter
from manual modes.

**Phase 4 — Auto**: mission execution. Upload a test mission in QGC — a
simple square at 20m AGL — before attempting a real survey. Confirm RTL
on mission completion.

Practice RTL deliberately at low altitude before the first deployment.
→ [[ardupilot-failsafe]] explains what triggers it and how to verify it.

### Autotune — mandatory before first survey mission

Default ArduPilot PIDs are too conservative for reliable survey flight in
wind. Run Autotune before any Auto mission:

1. Arm in AltHold, climb to 15m minimum
2. Activate Autotune switch — aircraft makes rapid roll/pitch pulses
3. Wait for all three axes (roll, pitch, yaw) — approximately 10 minutes
4. Land without disarming, toggle Autotune off, disarm, power cycle
5. Values saved to EEPROM — verify with a calm hover before first survey

→ [[ardupilot-autotune]] has the full procedure and abort criteria.

### Mission planning in QGroundControl

→ [[qgroundcontrol]] covers the full workflow. Key checks before switching
to Auto:

- Mission visible in Plan view, flight path covers intended area
- RTL or Land waypoint at end of mission
- GPS lock confirmed in Fly view (green icon, HDOP < 1.5)
- Battery voltage above 15.5V (4S LiPo) or 14.4V (Ghost Li-Ion)

→ [[ardupilot-failsafe]] for battery and RC link failsafe settings — set
before first flight, verify on bench before first field deployment.

---

## Rationale

This skeleton was created because the existing → [[sk-operations-manual]]
covers Pro/Betaflight operations. ArduPilot platforms have a different
operational model — different commissioning sequence, different flight mode
logic, different failsafe architecture, and different mission planning workflow.
Merging them into one skeleton would require extensive conditionals. A
dedicated ArduPilot skeleton is cleaner and serves the operator of Bandit,
Ghost, and Wing without requiring them to filter through Betaflight content.

---

## Connections

requires:
  - [[ardupilot-copter]]
  - [[ardupilot-commissioning]]
  - [[ardupilot-flight-modes]]
  - [[ardupilot-failsafe]]
  - [[elrs-mavlink-mode]]
  - [[qgroundcontrol]]
related:
  - [[ardupilot-autotune]]
  - [[bandit-variant]]
  - [[ghost-variant]]
  - [[wing-variant]]
  - [[ardupilot-plane]]
  - [[sk-operations-manual]]
  - [[sk-variant-specs]]
leads_to:
  - [[ardupilot-autotune]]
  - [[qgroundcontrol]]
  - [[maiden-flight]]
