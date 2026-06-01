---
id: acceptance-validation
title: "Acceptance validation"
version: 1.1.0
date: 2026-06-01
author: jsa
status: released
scope: libdrone
topic:
  - manufacturing
personas:
  - 1.builder
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Acceptance validation is the final gate between software commissioning and the
maiden flight. It runs a structured battery of ground checks — mass budget,
regulatory readiness, structural checks, electronics verification — to confirm
that the build is within design specification before anything leaves the ground.
A failed gate is information, not failure. Every deviation found on the ground
costs minutes to fix. The same deviation found in the air costs the drone.

---

## Concept

### Gates vs checks

The acceptance validation distinguishes two types of verification:

**Hard gates** — the build must not proceed to maiden if these fail. Examples:
AUW exceeds the planned operating weight limit, GPS fix cannot reach 8
satellites, motor directions are wrong. These are not warnings.

**Soft checks** — deviations should be logged and investigated but may not
prevent the maiden under controlled conditions. Examples: OSD battery voltage
reads 0.3V low vs. multimeter (investigate but probably a scale factor error,
not a build defect).

The validation sequence runs hard gates first. If any hard gate fails, stop.

### The maiden flight as a measurement event

The maiden flight is not a performance or a celebration. It is the first
data collection event for this specific build. Blackbox records the gyro
signal, RPM filter performance, and motor balance. Post-maiden visual
inspection checks structural behaviour under load. Every deviation from
expectation is information.

---

## Reference

### Acceptance gate sequence

**Mass budget (hard gate)**

- Weigh bare frame (no payload, no battery): must be within 10g of target
- Weigh with battery and with payload: must be within the weight limit you are
  operating to (your weight class has regulatory implications — see
  [[legal-and-regulatory]])

If AUW exceeds your planned weight limit — resolve before flying.

**Regulatory readiness (hard gate)**

- Operator registration / ID as applicable (see [[legal-and-regulatory]])
- Pilot competency as applicable for the planned operation
- Airspace authorisation confirmed for planned site (DroneMap)
- Insurance as applicable
- GPS Rescue return altitude set for local terrain

**Structural checks**

- All 4 props: no cracks, chips, or looseness. Balanced.
- All 4 arm T-locks: press each arm laterally — no play
- All 6 sandwich bolts: present, hand-tight + 1/4 turn
- All 4 CF rods: acoustic ping confirms ring tone
- Motor mount passive covers: no direct contact with arm head

**Electronics verification (bench, battery connected)**

- Battery voltage on OSD matches multimeter ±0.2V
- GPS fix ≥ 8 satellites within 90 seconds (cold start outdoors)
- All 4 motors spin in correct direction (Motors tab, props removed)
- BiDShot RPM readout showing for all 4 motors
- Blackbox enabled: device shows available flash space
- RC link: all sticks show correct direction in Receiver tab
- GPS Rescue manually tested at low altitude before operational use

---

## Procedure

### Acceptance validation run

1. **Mass gate.** Weigh on calibrated scale. Record all-up weights (bare frame,
   with battery, with payload if fitted). Compare against gates above.
   If any gate fails: do not proceed to maiden. Investigate cause.

2. **Regulatory gate.** Confirm operator ID and any required competency and
   insurance per [[legal-and-regulatory]]. Confirm airspace at planned
   maiden site. If any missing: do not proceed to maiden.

3. **Structural inspection.** Physical inspection of all items in the
   structural checks list. Any prop defect: replace immediately. Any arm
   T-lock play: reseat tab and re-torque arm screws.

4. **Electronic bench verification.** Battery connected, transmitter on first.
   Work through electronics verification list in order. Log any deviation.

5. **Pre-maiden briefing.** If flying with observers:
   - Confirm 20m safety perimeter will be maintained
   - Identify two emergency landing zones
   - Confirm communication method if GPS Rescue activates

6. **Ready for maiden.** All hard gates passed, all deviations logged.
   Proceed to [[maiden-flight]].

---

## Rationale

### Why structural checks run after electronics

If electronics verification reveals a hard gate failure (wrong motor
direction, no GPS lock), the build returns to commissioning regardless of
structural state. Doing structural checks first wastes time if electronics
would fail anyway. Electronics verification is faster and more likely to
find issues — run it first.

---

## Connections

requires:
  - [[software-commissioning]]
  - [[electronics-installation]]
related:
  - [[legal-and-regulatory]]
  - [[pre-flight-check]]
  - [[lipo-batteries]]
  - [[failure-hierarchy]]
leads_to:
  - [[maiden-flight]]
