---
id: bandit-variant
title: "Bandit variant"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: libdrone
topic:
  - resilience-community
personas:
  - 6.evaluator
  - 5.student
  - 4.workshop
platform:
  - bandit
lang: en
licence: CC BY-SA 4.0
---

## Summary

libdrone Bandit is the autonomous-capable variant of the libdrone family.
It shares the Core airframe geometry (220 mm wheelbase, 4-inch props, 4S XT30)
but replaces Betaflight with ArduPilot Copter, enabling GPS-guided flight
modes, MAVLink telemetry, and QGroundControl mission execution. Its primary
roles are operator training via a progressive flight-mode curriculum,
delivery of the civilian awareness programme, and light autonomous survey
missions including grid mapping, search-and-rescue pattern flights, and
agricultural transects.

---

## Concept

### What ArduPilot changes

The defining departure from the rest of the libdrone family is the flight
system. Betaflight — used on Pro and Core — is optimised for fast manual
flight; it has no autonomous mission executor. ArduPilot Copter is a full
autopilot stack: it can execute a pre-programmed waypoint mission without
continuous pilot input, stream telemetry to a ground control station, and
configure its failsafe behaviour around mission objectives rather than
simple return-to-home.

For Bandit's primary use case — teaching operators to understand autonomous
drone technology — this matters beyond capability. Flying a platform that
executes autonomous missions is qualitatively different from flying one that
requires continuous manual input. The training value is in experiencing the
automation, not in piloting skill alone.

### The training curriculum model

The six ArduPilot flight modes assigned to Bandit are not arbitrary. They
form a progression: Stabilize (manual rate control, no automation), through
AltHold (barometer-locked altitude), Loiter (GPS position hold), Auto
(waypoint mission execution), to RTL (autonomous return). Each mode adds one
layer of automation and one sensor dependency. A student who works through
the progression in order understands both the capability and the failure mode
at each layer — the same understanding that the awareness curriculum requires.
See → [[ardupilot-flight-modes]] for the full mode reference.

### The name

In aviation and military radio communication, "Bandit" is the brevity code
for a confirmed hostile aircraft. The awareness curriculum this platform
supports teaches operators to detect, classify, and respond to drone threats.
Flying the Bandit is how a student learns to think like the technology they
are learning to defend against. The name is a reminder that the training
platform and the threat platform are the same hardware.

---

## Reference

| Parameter | Value |
|---|---|
| Wheelbase | 220 mm (4-inch class) |
| Flight system | ArduPilot Copter ≥4.5 |
| FC | Matek H7A3-SLIM |
| ESC | SpeedyBee BLS 50A 30×30 |
| Motors | T-Motor Pacer P1804 3400KV |
| Battery | 4S 850 mAh XT30 |
| Flight time | ~12 min typical mission |
| GPS | Matek M8Q-5883 (mandatory) |
| Telemetry | MAVLink via ELRS ≥3.5 |
| GCS | QGroundControl |
| AUW target | 450–550 g |
| BOM cost | ~€219 (bulk ~€180) |
| EASA category | Open A2 |

**Shared SKUs with Core and Pro:** Matek H7A3-SLIM, Happymodel EP2 Nano,
3 mm CF rod stock, M2/M3 hardware.

---

## Procedure

<!-- not applicable — variant selection and setup are covered in
[[platform-selection]], [[ardupilot-commissioning]], and [[ardupilot-flight-modes]] -->

---

## Rationale

Bandit uses the Core-scale airframe (220 mm, 4S) rather than the Pro-scale
(330 mm, 6S) because the primary Bandit missions — survey grids, awareness
curriculum exercises, ATAK integration drills — do not require the Pro's
payload capacity or 6S performance envelope. A smaller, lighter platform
reduces BOM cost, reduces regulatory weight threshold risk, and is more
forgiving during the early phases of the training curriculum when the student
is still in Stabilize mode. The name and the mission are aligned: the Bandit
is the minimum platform that teaches what needs to be taught.

---

## Connections

requires:
  - [[platform-overview]]
  - [[ardupilot-copter]]
related:
  - [[platform-selection]]
  - [[core-variant]]
  - [[ardupilot-flight-modes]]
  - [[elrs-mavlink-mode]]
  - [[qgroundcontrol]]
  - [[iff-architecture]]
leads_to:
  - [[ardupilot-commissioning]]
  - [[ardupilot-flight-modes]]
