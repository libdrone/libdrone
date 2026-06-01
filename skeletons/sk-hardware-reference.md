---
id: sk-hardware-reference
title: "Hardware Reference"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 1.builder
  - 8.architect
  - 7.contributor
platform:
  - pro
lang: en
licence: CC BY-SA 4.0
---

## Summary

The Hardware Reference is the component-level technical reference for
libdrone Pro V2.4.6: frame architecture, printed parts specification,
floating motor mount system, electronics layout on the Platform, connectors
and wiring topology, propeller selection, environmental reliability, and
mass budget. It is the 3.0.0 replacement for the V2.4.6 Hardware Reference
document — with all specifications delegated to atoms and the structure
providing navigation.

---

## Concept

### Architecture summary

libdrone Pro V2.4.6 is a 330mm True-X quadrotor with a five-layer
PETG-PCCF-PCCF-PCCF-PETG sandwich body on four 2.0mm CF rods, four PETG
arm shafts with T-lock attachment, and a sealed PETG Platform layer on top
that carries the electronics and payload interface. → [[sandwich-structure]]
explains the composite logic. → [[cf-rod-architecture]] explains the rod
pre-tension system.

The body is not the drone — the body is the chassis that other systems mount
to. The key insight of the V2.4.6 architecture: the electronics (FC, ESC,
VTX, GPS, receiver) mount to the sealed Platform layer, not to the sandwich.
The sandwich and Platform are separate; the Platform can be replaced without
touching the sandwich.

### Printed parts

The structural printed parts and their key geometry requirements are owned
by their respective atoms:

- **Arm shaft**: → [[arm-shaft]] — T-lock profile, rod channel, pinch slit,
  dovetail groove on bottom face for motor wire routing
- **Arm tab**: geometry defined by T-slot variables; mates arm shaft to PCCF layers
- **PCCF X-body layers** (3×): T-slots, rod channels, stack holes
- **PETG top/bottom layers**: rod channels, battery slot, foam pads
- **Platform**: three-zone wiring channels, MIPI centreline, GX12 chimneys,
  fan slot, battery rail — → [[power-signal-separation]] for the EMC geometry gates
- **Backplane**: Pi bay (LCM-1 ready), payload boss pads, fan mounting
- **GPS/camera bracket**: MIPI channel, camera slot, GPS mount above camera
- **Bumpers** (ASA): energy absorption at first impact point

All printed parts carry version numbers in the FreeCAD parametric model.
→ [[variable-table-values]] is the single source of truth for all dimensions.

### Floating motor mount system

→ [[floating-motor-mounts]] covers the complete system: O-ring specification
(ID 4.0mm, OD 7.0mm, CS 1.5mm, 40–50 Shore A silicone), sleeve specification,
assembly torque (0.4–0.5 N·m, cross-pattern), Super Lube 52004 lubrication,
and the passive cover clearance verification.

The isolation system is the most maintenance-critical component in the build.
→ [[scheduled-maintenance]] defines the replacement intervals. → [[vibration-isolation-theory]]
explains the physics that makes it effective.

### Electronics layout — Platform nose-to-tail

The Platform layer carries all electronics on a single plane. The Y-axis
positions (measured from body centre, Y+ = nose):

- GPS/camera bracket: nose (+50mm)
- ELRS receiver: +15 to +40mm, LEFT channel
- FC/ESC stack: centreline around Y=0
- GX12 connectors A+B: Y = −66mm (paired, X = ±25mm)
- VTX: −104 to −133mm electronics zone
- Fan: rear face slot
- Battery rail: Y = −39mm to −148mm, RIGHT side exit

All electronics positions are fixed by the Platform geometry — they are not
configurable. The Platform is the printed wiring board of the libdrone
architecture. → [[power-signal-separation]] explains the three-zone wire
routing that the Platform enforces physically.

### Connectors and wiring topology

→ [[gx12-connector-standard]] covers the dual GX12-7 payload interface.
→ [[sk-wiring-reference]] covers the complete wiring topology with gauge
specifications and routing rules. The critical connector types:

- **XT60**: battery to ESC — 12–14 AWG, twisted pair
- **MR30**: ESC to motors — pre-soldered pigtails, twist 3 phases per motor
- **JST-SH 4-pin**: companion harness (LCM-1 Pi bay to FC UART6)
- **GX12-7**: dual payload connectors — permanent panel mount, D-D bore

### Propeller selection

→ [[propellers]] covers the physics and selection criteria. The V2.4.6 standard
propellers:

- **HQProp 6×3×3 PC tri-blade**: standard set. Higher pitch, better performance
  in wind, standard mapping profile.
- **HQProp 6×2.5×3 PC tri-blade**: low-pitch alternate. Calm conditions, maximum
  flight time, lower motor temperature.
- **M5 flange nuts**: CW and CCW pairs for 5mm shaft. Required — standard M5
  nuts will undo in flight.

Rate Profile 1 is tuned for 6×3×3; Rate Profile 2 for 6×2.5×3.
→ [[betaflight-profiles]] covers the profile switching procedure.

### Environmental reliability

→ [[conformal-coating]] covers the moisture protection application. The V2.4.6
addition: the Thermal Retention Shroud (TRS) changes the coating specification
from permanent silicone to reworkable acrylic — → [[thermal-retention-shroud]]
explains why.

→ [[thermal-management-cooling]] covers the Gdstime 3010 fan specification and
always-on cooling strategy. → [[winter-protocol]] covers the sub-5°C operational
constraints.

### Mass budget

The target and gate masses are defined in → [[variable-table-values]]. They change
with configuration. The acceptance rule: if any mass target is missed, investigate
before maiden. Mass misses are usually wire routing issues, unexpected component
weights, or bracket geometry changes — all of which have implications beyond
just weight.

---

## Reference

### Component substitution guide

All critical components have documented alternatives. The substitution rule:
if the specified component is unavailable, consult → [[design-rationale-index]]
to understand which properties of the component are critical before selecting
a substitute.

| Component | Critical properties | Substitution risk |
|---|---|---|
| Matek H7A3-SLIM FC | H7 class, 6 UARTs, IMU moat | Medium — any BF-supported H7 board may work |
| Pilotix 75A AM32 ESC | AM32 firmware, BiDShot, 6S | Low — any AM32 4-in-1 6S unit |
| O-rings ID4/OD7/CS1.5 | 40–50 Shore A silicone | High — shore hardness is critical |
| CF rods 2.0mm | ±0.05mm tolerance | Medium — verify diameter with calipers |
| Panasonic FM 1000µF cap | ESR <0.1Ω at 100kHz | High — generic electrolytics fail this |

---

## Procedure

### Hardware Reference as a diagnostic tool

When something doesn't fit or behave as expected during build:
1. Check the Variables file for the correct dimension
2. Check the owning atom for the acceptance criterion
3. Check this skeleton's component substitution guide if a component is suspect
4. Check → [[design-rationale-index]] for the engineering rationale behind the specification

---

## Rationale

The V2.4.6 Hardware Reference (629 lines) was a comprehensive component-level
reference that duplicated much of the Master Specification and the WBS. The 3.0.0
skeleton provides the same navigational function — "what component, what specification,
what article" — while delegating all specifications to their owning atoms.

---

## Connections

requires: []
related:
  - [[sk-master-specification]]
  - [[sk-complete-build-guide]]
  - [[sk-wiring-reference]]
leads_to:
  - [[sk-master-specification]]
  - [[sk-complete-build-guide]]
