---
id: pre-flight-check
title: "Pre-flight check"
version: 2.0.0
date: 2026-05-31
author: jsa
status: released
scope: libdrone
topic:
  - safety-regulations
personas:
  - 2.operator
  - 1.builder
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The pre-flight check is the structured process run before every flight: inspect
the aircraft, verify the electronics, confirm the site and the pilot are ready,
and only then arm. It exists because memory is unreliable under pre-flight
pressure and an airborne failure is almost always worse than a delayed takeoff.
The process is built around explicit go/no-go gates — a small set of conditions
that must be true to fly — and is executed against the printable
[[preflight-checklist]]. The maiden flight extends the same process into a
first data-collection event rather than a celebration.

---

## Concept

### Why a check, not experience

Experienced pilots have accidents from skipped steps more often than beginners
do from unfamiliarity. The pre-flight check exists because memory is unreliable
under pre-flight pressure, because a missed step is invisible until something
goes wrong, and because the consequences of airborne failures are almost always
worse than the consequences of a delayed takeoff. The check removes memory from
the sequence: the pilot executes a fixed list rather than recalling one.

This is the same principle as the coupon test in manufacturing — a few minutes
of ground verification prevents a failure that is far more expensive in the air.
The check is a *process*; the [[preflight-checklist]] is the artefact that
process runs against.

### The maiden flight as a measurement event

The first flight of a new build is not a performance. It is a data-collection
event. Blackbox records the gyro signal, RPM filter performance, and motor
outputs; post-flight inspection checks T-lock engagement, motor mount O-ring
condition, and screws. The maiden answers a single question — how does this
specific build actually fly, and where are its weak points — and every
deviation from expectation is information, not failure.

---

## Reference

### Go/no-go acceptance criteria

These are the hard gates. If any is not met, the aircraft does not fly until it
is resolved. They are the subset of the full [[preflight-checklist]] that admits
no discretion:

| Gate | Condition to fly |
|---|---|
| GPS fix | ≥ 8 satellites acquired before arming (home point records at arm) |
| Battery | Resting voltage ≥ 24.0 V (fresh 6S pack), no swelling or deformation |
| Failsafe | GPS Rescue confirmed active (requires the GPS gate above) |
| RC link | RSSI / link quality good; transmitter powered before the aircraft |
| Structure | All 4 T-locks seated with no play; no visible frame or prop damage |
| Airspace | Authorisation confirmed for the site and altitude; two landing zones |
| Pilot | Not fatigued, impaired, or distracted |

Everything else on the checklist is a verification step; the seven gates above
are the conditions that turn a no-go into a go.

### The checklist itself

The complete, printable step-by-step sequence — site, structure, electronics,
powered verification, and pilot readiness — is maintained as a separate
artefact: [[preflight-checklist]]. Print it or keep it on the phone; this
article explains the why and the gates, the checklist is what you tick.

---

## Procedure

### Maiden flight sequence (extended pre-flight)

1. Complete the full [[preflight-checklist]].
2. Arm in an open area, minimum 20 m from all people and obstacles.
3. Hover at 1 m altitude for 30 seconds. Listen for unusual sounds. Confirm the
   aircraft holds position without significant drift.
4. Verify OSD battery voltage drops normally (0.2–0.4 V at hover).
5. Land. Immediately feel all four motor housings — should be warm, not hot.
6. Press each arm laterally — T-lock tabs should show no movement.
7. Check motor mount O-rings — visibly compressed, not cracked.
8. Reconnect to Betaflight Configurator. Download Blackbox.
9. Review the gyro spectrum in Blackbox Explorer — confirm the RPM filter is
   removing motor harmonics and the noise floor is below −40 dB in the
   0–200 Hz range.
10. If all checks pass, the maiden is complete. Proceed to normal flights.

---

## Rationale

### Why transmitter on before aircraft

If the aircraft is powered before the transmitter is connected, it sees no RC
signal and immediately enters failsafe. For a drone configured with GPS Rescue,
this can trigger unexpected GPS Rescue activation on the ground before the pilot
has any control. Transmitter first ensures the RC link is established before the
flight controller initialises its control loop. This is why "transmitter before
aircraft" is a gate, not a preference.

### Why GPS fix is a hard gate for arming

GPS Rescue cannot function without a home point, and the home point is recorded
only at arm time. Arming without a GPS fix silently disables GPS Rescue for the
entire flight. If the RC link is then lost over urban terrain, there is no
automatic return. This is not theoretical — it is a documented accident cause in
FPV operations, and it is why the GPS gate is non-negotiable rather than
advisory.

---

## Connections

requires: []
related:
  - [[lipo-batteries]]
  - [[legal-and-regulatory]]
  - [[betaflight-gps-rescue]]
  - [[failure-hierarchy]]
  - [[scheduled-maintenance]]
  - [[post-flight-check]]
leads_to:
  - [[preflight-checklist]]
