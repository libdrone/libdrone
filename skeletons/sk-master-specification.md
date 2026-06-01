---
id: sk-master-specification
title: "Master Specification"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 8.architect
  - 7.contributor
  - 1.builder
platform:
  - pro
lang: en
licence: CC BY-SA 4.0
---

## Summary

The Master Specification is the single authoritative reference for the
libdrone Pro V2.4.6/V2.4.7 platform: what it is, what it must do, what
it must weigh, what must pass before maiden flight, and what the IFF
architecture commits to at the platform level. All specific values that
are not hard design decisions live in the Variables file — the Master Spec
states the principles and acceptance criteria; the atoms provide the depth.

---

## Concept

### Mission and philosophy

libdrone Pro serves three concurrent roles: cinematic surveillance (1080p60
digital FPV, pilot-controlled), high-intensity skatepark chase (low-speed
A2 compliance mode), and air quality mapping (SEN66 payload, GPS-tagged data).
These are not three separate builds — they are the same platform reconfigured
by payload swap and profile selection.

The underlying philosophy is "Spitfire aero-logic": shell as skin (PETG/PCCF
sandwich absorbs and distributes crash energy), four rods as spar (pre-tensioned
CF rods carry structural load through all five layers). → [[sandwich-structure]]
and → [[cf-rod-architecture]] explain the engineering. → [[failure-hierarchy]]
explains the crash energy management sequence.

The design target is jello-free 6-inch flight. → [[vibration-isolation-theory]]
and → [[floating-motor-mounts]] are the primary mechanisms. → [[imu-gyroscope]]
explains what the IMU needs from the frame. → [[rpm-filter]] explains what the
firmware does with what the frame provides.

### Single source of truth: the Variables file

All parametric dimensions, mass targets, and performance thresholds are defined
in the Variables file (→ [[variable-table-values]]). The Master Specification does
not restate them. Any question of the form "what is the target mass?" or "what is
the rod diameter?" has one answer: the Variables file. Everything else is a copy
that may be wrong.

### CAD architecture

The FreeCAD parametric model generates all geometry from the Variables spreadsheet.
→ [[freecad-document-setup]] covers the setup procedure. → [[parametric-modelling-philosophy]]
explains why parametric design is the correct approach for a community build
platform. → [[variable-table-structure]] explains the organisation of the variable
namespace.

### Acceptance targets

The platform is accepted for maiden flight when all of the following pass:

**Mass**: bare dry mass (no payload, no battery) within the target/gate in the
Variables file. With battery: within EASA A2 limit (< 900g total).

**Structural**: rod joints show zero play by hand feel (primary criterion).
T-lock tabs fully seated, zero lateral play in sandwich. Acoustic test: all four
rods ring at 2.2–2.6 kHz. Above 2.6 kHz before zero play: stop and investigate.
Motor mount passive covers contact arm head only at O-ring bosses.

**Electronics**: GPS ≥ 8 satellites outdoors within 90 seconds (cold start).
All motors spin correct direction in Betaflight Motors tab. OSD visible with
correct telemetry fields. Conformal coating applied and cured on FC, ESC,
and GPS module.

**Compliance**: low-speed mode calibrated ≤ 4.8 m/s in flight. Operator e-ID
label on frame. Crash readiness: 2 spare arm shaft sets + O-ring spares in field bag.

**IFF readiness** (for operational deployments): IR strobe mounted and operational.
Remote ID module broadcasting. If CoT output is configured: blue icon confirmed
on ATAK tablet before deployment.

### Material strategy

→ [[material-selection-philosophy]] covers the full rationale for each material
choice. The summary: PCCF for stiffness and structural layers, PETG for arms
and accessories (controlled ductile fracture in crashes), ASA for bumpers
(UV stability), TPU for motor mount pads (vibration isolation), silicone
O-rings for floating mount isolation. All materials are available from Prusa.shop
or standard filament suppliers. No exotic or single-source materials.

### Maintenance schedule

→ [[scheduled-maintenance]] contains the full interval table. The Master
Specification states only the philosophy: libdrone is a machine under continuous
maintenance. Airworthiness is maintained by scheduled inspection and interval-based
replacement, not by "it worked last time." The O-ring replacement interval (every
20–30 flight hours) is the most important — functional degradation precedes
visible failure.

### Software stack

→ [[sk-electronics-deep-dive]] and → [[sk-complete-build-guide]] cover the full
software stack narrative. The platform-level commitments:

Betaflight 4.5 on MATEKH743 target. AM32 ESC firmware. ELRS 250 Hz LBT.
HDZero digital FPV. EdgeTX on TX16S MKII. All firmware is open source.
Configuration is applied via CLI diff to a known-clean base flash — no
manual GUI configuration that cannot be reproduced from the diff. All
configuration backed up to repository before maiden.

### IFF architecture

→ [[iff-architecture]] covers the full five-layer implementation. The platform-level
commitments:

The ESP32-S3 is optional but prepared on all platforms: dedicated mount point,
pre-wired UART stub to FC, 5V power tap. Deploying an ESP32-S3 is a field-
installable operation requiring no airframe modification.

The platform does not implement any nation-specific IFF protocol at hardware level.
The GX12-7 Connector B GPIO reservation and ESP32-S3 firmware architecture
accommodate any national defence IFF requirement through a module and firmware
update — no airframe change.

For contested environments: the ESP32-S3 firmware implements a hardware kill
switch that simultaneously disables WiFi, Remote ID, and CoT output while leaving
flight operations unaffected. → [[operational-security]] for the full EMCON protocol.

---

## Reference

### Acceptance checklist summary

| Category | Gate | Reference |
|---|---|---|
| Mass | Variables file targets | [[variable-table-values]] |
| Rod joint | Zero play by hand | [[cf-rod-architecture]] |
| Acoustic | 2.2–2.6 kHz ring | [[cf-rod-architecture]] |
| Motor mount | O-ring contact only | [[floating-motor-mounts]] |
| GPS | ≥8 sats before maiden | [[betaflight-gps-rescue]] |
| Conformal coating | Applied and cured | [[conformal-coating]] |
| Low-speed calibration | ≤4.8 m/s verified | [[betaflight-profiles]] |
| Crash readiness | Spares on shelf | [[corrective-maintenance]] |

---

## Procedure

### Using the Master Specification

The Master Specification is a reference and decision record, not a build guide.
Use → [[sk-complete-build-guide]] for the step-by-step build sequence. Use this
document when: making a design decision that affects acceptance criteria,
understanding the platform-level IFF commitments, or verifying that a proposed
change is consistent with the platform philosophy.

---

## Rationale

The V2.4.6 Master Specification (612 lines) combined acceptance criteria,
variable table references, CAD recipes, and IFF architecture in a single
document that was difficult to update consistently. The 3.0.0 skeleton
delegates everything with a single source of truth (Variables, atoms,
IFF doc) and retains only the platform-level commitments and acceptance
gates that belong in a specification document.

---

## Connections

requires: []
related:
  - [[sk-complete-build-guide]]
  - [[sk-electronics-deep-dive]]
  - [[sk-security-operations-guide]]
leads_to:
  - [[sk-complete-build-guide]]
