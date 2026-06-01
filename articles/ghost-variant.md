---
id: ghost-variant
title: "Ghost variant"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: libdrone
topic:
  - resilience-community
personas:
  - 6.evaluator
  - 9.defense
  - 8.architect
platform:
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

libdrone Ghost is the quiet, long-endurance variant of the libdrone family.
Two engineering decisions define it: large low-KV motors driving 12-inch props
at low RPM reduce acoustic signature substantially compared to any other family
member, and Li-Ion 18650 batteries replace Li-Po for energy density over peak
power, yielding 30–45 minutes hover endurance. Ghost reuses the complete Bandit
electronics stack — ArduPilot, ELRS MAVLink, QGroundControl, mandatory ESP32-S3
IFF bridge — with a new laser-cut CF plate arm architecture scaled to the 12-inch
prop class.

---

## Concept

### The acoustic argument

The dominant noise source in a multirotor is propeller tip speed. Tip speed
equals RPM × π × diameter divided by 60. A larger disc area moving the same
mass of air requires less RPM for the same thrust — and lower RPM means lower
tip speed, which means substantially lower acoustic emission. A standard 6-inch
drone at 50 m produces approximately 65–70 dB(A) at the ground. Ghost at the
same altitude produces approximately 50–55 dB(A) — roughly half as loud to
the human ear. For operations where the drone's presence should not be obvious
to casual observers, this reduction is operationally significant.

This is not stealth in a technical sense. Ghost can still be detected by
attentive observers at close range. It is a meaningful reduction in the passive
acoustic detection range — the distance at which a drone's sound is the
first cue that it is present. See → [[acoustic-signature-design]] for the
physics derivation and design rationale.

### The Li-Ion choice

Ghost uses a 4S2P pack of 18650 cells rather than a LiPo pouch. Li-Ion cells
carry more energy per kilogram than LiPo at the cost of lower peak discharge
current. For a survey platform carrying large props at low RPM, peak current
demand is low — this is exactly the operating profile where Li-Ion's energy
density advantage materialises without the discharge rate becoming a constraint.
The result is 30–45 minutes of hover endurance from an ~436 g battery pack.
See → [[li-ion-batteries]] for chemistry and construction detail.

### CF plate arm architecture

Ghost's 12-inch prop class requires arm stiffness that 3D-printed PETG or
TPU cannot provide at the required span. Arms are laser-cut 2 mm carbon fibre
plate sandwiches — two plates per arm, clamping onto the existing 3 mm CF rod
system. This makes Ghost arms non-printable by the community but field-repairable
without tools: unclamp, slide, reclamp in under 15 minutes. See
→ [[cf-plate-arms]] for the DXF geometry and fabrication detail.

### IFF and ESP32-S3

The ESP32-S3 companion board is mandatory on Ghost. It runs three concurrent
firmware tasks: MAVLink-to-CoT bridge (feeding position and attitude to ATAK),
EASA Remote ID broadcast (WiFi NAN + BLE 5.0), and IFF GPIO interface for future
allied hardware modules. An EMCON kill switch on the body cuts all ESP32-S3 RF
emissions simultaneously — flight operations and the independent IR strobe are
unaffected. See → [[esp32-s3-companion]] and → [[iff-architecture]].

---

## Reference

| Parameter | Value |
|---|---|
| Wheelbase | ~540 mm (12-inch class) |
| Flight system | ArduPilot Copter ≥4.5 |
| Motors | T-Motor MN4108 480KV |
| Propellers | 12-inch folding |
| Battery | 4S2P Li-Ion 18650, ~6 000 mAh |
| Flight time | 30–45 min hover |
| Arm architecture | Laser-cut 2 mm CF plate (not 3D-printed) |
| ESP32-S3 | Mandatory — IFF + Remote ID |
| IR strobe | Mandatory — 850 nm, independent battery |
| AUW target | 1 200–1 400 g |
| BOM cost | ~€444 (bulk ~€380) |
| EASA category | Open A2 |

**Shared SKUs with Bandit:** Matek H7A3-SLIM, SpeedyBee BLS 50A, EP2 Nano,
Foxeer Predator Nano, Foxeer Reaper Nano V2, Matek M8Q-5883, 3 mm CF rods.

---

## Procedure

<!-- not applicable — setup follows the Bandit commissioning path;
see [[ardupilot-commissioning]] and [[cf-plate-arms]] for Ghost-specific steps -->

---

## Rationale

Ghost was designed to answer the question: what does the threat sound like from
eighty metres? The awareness curriculum (Bandit) teaches operators to detect
drones by sound. Ghost was designed to be the hardest platform in the family to
detect acoustically. Flying Ghost and then measuring its own detection range using
the Bandit awareness exercises closes the loop: the student learns to detect it,
then builds and flies it, and measures what they built. The platform is both the
answer and the instrument.

---

## Connections

requires:
  - [[platform-overview]]
  - [[bandit-variant]]
  - [[ardupilot-copter]]
related:
  - [[platform-selection]]
  - [[acoustic-signature-design]]
  - [[li-ion-batteries]]
  - [[cf-plate-arms]]
  - [[esp32-s3-companion]]
  - [[iff-architecture]]
  - [[operational-security]]
leads_to:
  - [[acoustic-signature-design]]
  - [[li-ion-batteries]]
  - [[cf-plate-arms]]
