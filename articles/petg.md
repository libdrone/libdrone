---
id: petg
title: "PETG — properties and libdrone use"
version: 1.0.0
date: 2026-04-11
author: jsa
status: released
scope: libdrone
topic:
  - materials
personas:
  - 1.builder
  - 2.operator
  - 5.student
  - 7.contributor
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

PETG (polyethylene terephthalate glycol) is the primary structural filament for
libdrone's crash-contact zones. It is tough, absorbs impact energy without
fracturing, and is easy to post-process. It is used for arm shafts, arm tabs,
the X body bottom layer, GPS bracket, platform, and backplane. Its lower
stiffness relative to PCCF is a feature in crash zones, not a deficiency.

---

## Concept

### Why toughness matters at crash contact zones

When a drone impacts a surface, kinetic energy must go somewhere. A stiff,
brittle material transmits that energy into the structure behind it — which
either absorbs it by fracturing or transmits it further into the electronics.
A tough material absorbs energy locally through controlled deformation, limiting
the energy that reaches the structural core and electronics.

PETG is viscoelastic — under sudden impact it deforms rather than fractures.
The arm shaft bends, the tab yields, the bottom X body layer compresses. Each
deformation event absorbs energy and slows the crash progression. The PCCF
structural core, which cannot absorb impact gracefully, is protected.

### Print orientation and layer strength

PETG arm shafts are printed vertically — standing on the pinch bolt end.
This places print layers perpendicular to the primary bending load at the
hub junction. Inter-layer adhesion in the bending direction is maximised.
A horizontally printed arm shaft would have layers parallel to the bending
load, making delamination the primary failure mode rather than controlled
flexure.

This is one of the most critical print decisions in the entire build. An
incorrectly oriented arm shaft fails at a fraction of the design load.

### Interference fit capability

PETG deforms elastically under moderate compressive stress. The rod channels
in the X body PETG bottom layer are printed at 2.1 mm diameter rather than
the standard 2.2 mm, creating a controlled interference fit with the 2.0 mm
CF rods. The rod is pressed in — the PETG holds it in radial compression
without additional bosses or fasteners. PCCF layers use 2.2 mm channels
because PCCF is too brittle to tolerate the compressive stress of an
interference fit without risk of micro-cracking.

---

## Reference

### Material properties

| Property | Value | Notes |
|---|---|---|
| Print temperature (nozzle) | 255°C | Standard PETG range |
| Bed temperature | 85°C | Textured PEI — no glue stick required |
| Enclosure | Door closed ~30°C ambient | Reduces warping and layer splitting |
| Cooling | 30–40% | Partial cooling preserves layer adhesion |
| Creep threshold | ~60°C sustained load | Above this, dimensional creep occurs |
| Nozzle | 0.6 mm hardened steel | Recommended for all PETG in this build |
| Moisture sensitivity | Moderate | Dry at 65°C for 4 hours if previously opened |

### Key print settings (arm shaft — primary crash element)

| Setting | Value |
|---|---|
| Layer height | 0.15 mm |
| Perimeters | 8 |
| Infill | 30% Grid |
| Solid layers | 6 top / 6 bottom |
| Brim | 5 mm |
| Orientation | **VERTICAL — mandatory** |

### Rod channel interference fit

| Channel | Diameter | Where used |
|---|---|---|
| Standard | 2.2 mm | PCCF layers — sliding fit |
| Interference | 2.1 mm | PETG bottom layer only — press fit |

If 2.1 mm grips too tightly after coupon validation: open Variables,
increase `RodDiaChannelCore` to 2.15 mm. If still too tight: 30 seconds
with a 2 mm drill bit in the printed channel. Never apply this to PCCF.

### Parts by use

| Part | Orientation | Qty per drone |
|---|---|---|
| Arm shaft | Vertical — mandatory | 4 (+ 2 spares recommended) |
| Arm tab | Horizontal | 8 |
| Arm cover active | Horizontal | 4 |
| X body PETG bottom | Flat | 1 |
| X body PETG top | Flat | 1 |
| GPS/camera bracket | Flat | 1 |
| Platform | Flat, face-up | 1 |
| Backplane | Flat, face-up | 1 |

### Drop test — arm shaft acceptance

Drop from 1 m onto a hard floor.
- **Pass:** flex, surface mark, bounce, rattle
- **Fail:** crack or delamination → re-dry filament or adjust temperature

---

## Procedure

### Drying PETG

1. Check spool condition — fresh sealed spool needs no drying.
2. Previously opened spool: dry in food dehydrator or filament dryer at 65°C for 4 hours.
3. Print immediately after drying — do not leave on a humid bench overnight.
4. Signs of wet filament: popping sounds during print, rough surface finish, poor layer adhesion.

---

## Rationale

### Why PETG and not PLA for crash zones

PLA is brittle at drone operating temperatures and in cold weather. A winter
crash with PLA arms produces catastrophic fracture rather than controlled
deformation. PETG maintains toughness across the operating temperature range
of libdrone (−10°C to +40°C ambient). PLA is explicitly excluded from
crash-contact zones.

### Why not ABS or ASA for crash zones

ABS and ASA are tougher than PLA but require more demanding print conditions
(high enclosure temperature, high bed adhesion) and warp more readily on
large flat prints. Their advantage — UV stability — is not required for
internal structural parts. PETG is easier to print reliably across a range
of printer calibrations, which matters for community reproducibility.

### Why PETG for the platform and backplane

The platform and backplane are not crash-contact parts but they are
functionally complex. PETG's ease of post-processing (drilling, reaming,
heat-set insert installation) makes it the right choice. PCCF's brittleness
would make post-processing operations (heat-set inserts in mast boss pads,
support removal from GX12 chimney bores) risky.

---

## Connections

requires:
  - [[material-selection-philosophy]]
related:
  - [[pccf]]
  - asa
  - [[failure-hierarchy]]
  - [[arm-shaft]]
  - [[sandwich-structure]]
  - [[coupon-validation]]
leads_to:
  - [[pccf]]
