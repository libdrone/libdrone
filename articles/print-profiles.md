---
id: print-profiles
title: "Print profiles"
version: 1.0.0
date: 2026-04-11
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

Every libdrone part has its own print profile tuned to its material, function,
and orientation. Arm shafts are printed vertically at 0.15 mm layers with
8 perimeters because inter-layer strength and fine surface detail matter. X body
PCCF layers are printed flat at 0.20 mm with 40% infill because area coverage
and dimensional stability matter more than fine detail. Using the wrong profile
for a part wastes filament or produces a structurally inadequate result.

---

## Concept

### Why parts need different profiles

Print profiles are not just about quality — they are about function. The key
variables are:

**Layer height** — thinner layers give more surface detail and better layer
adhesion on overhangs but increase print time. Structural parts that are loaded
in the Z axis (perpendicular to layers) need thinner layers. Flat structural
parts need fewer, heavier layers.

**Perimeters** — more perimeters mean more material at the part boundary, which
directly increases wall strength and impact resistance. Crash-sacrificial parts
(arm shafts) need many perimeters. Structural flat parts (X body layers) need
fewer because their strength is governed by layer count and infill.

**Infill** — determines internal density. Higher infill increases mass and
compressive strength. Most parts use grid infill for predictable load paths.
Gyroid infill is an alternative for parts that need good multi-directional
strength with lower mass.

**Orientation** — the most critical setting. Layer lines must be oriented so
the strongest axis (along-layer) aligns with the primary load direction.
A vertically printed arm shaft has layers perpendicular to the bending load —
maximum strength. A horizontally printed arm shaft has layers parallel to the
bending load — minimal delamination resistance.

---

## Reference

### Hardware requirements

| Item | Specification |
|---|---|
| Nozzle | 0.6 mm hardened steel — mandatory for all parts |
| Spare nozzle | Keep one in reserve — PCCF and PETG-CF are abrasive |
| Print sheet | Satin or textured PEI |
| Glue stick | Mandatory for PCCF; not required for PETG, PETG-CF, or ASA |

### Arm shaft — PETG (primary crash element)

| Setting | Value |
|---|---|
| Layer height | 0.15 mm |
| Perimeters | 8 |
| Infill | 30% Grid |
| Solid layers top/bottom | 6 / 6 |
| Brim | 5 mm |
| Orientation | **VERTICAL — mandatory** |
| Nozzle temp | 255°C |
| Bed temp | 85°C |
| Cooling | 30–40% |
| Extrusion multiplier | 0.96–0.98 |

Critical notes: disable "Thick Bridges" for counterbore surfaces.
Verify MR30 wire channel is not filled with support material.
Drop test from 1 m: pass = flex/mark, fail = crack/delamination.

### Arm tab — PETG

| Setting | Value |
|---|---|
| Layer height | 0.20 mm |
| Perimeters | 4 |
| Infill | 30% Grid |
| Orientation | Horizontal (flat) |
| Nozzle temp | 255°C |
| Bed temp | 85°C |

### Arm cover passive — PETG-CF

| Setting | Value |
|---|---|
| Layer height | 0.20 mm |
| Perimeters | 4 |
| Infill | 30% Grid |
| Orientation | Flat |
| Nozzle temp | 270–280°C |
| Bed temp | 85°C |
| Respirator | FFP3 mandatory — carbon fibre particles |

### Arm cover active — PETG

Same settings as arm tab. Orientation: flat.

### X body PCCF layers (×3 identical)

| Setting | Value |
|---|---|
| Layer height | 0.20 mm |
| Perimeters | 4 |
| Infill | 40% Grid or Gyroid |
| Solid layers top/bottom | 5 / 5 |
| Orientation | Flat |
| Nozzle temp | 290–300°C |
| Bed temp | 110°C |
| Enclosure | Required — door closed >40°C |
| Cooling | 0% |
| Glue stick | Mandatory on PEI |

### X body PETG top layer

| Setting | Value |
|---|---|
| Layer height | 0.20 mm |
| Perimeters | 4 |
| Infill | 30% Grid |
| Orientation | Flat, face-up |
| Nozzle temp | 255°C |
| Bed temp | 85°C |
| Supports | Required inside GX12 chimney bores |

After print: install 2 × M3 heat-set inserts in mast boss pads at 200–210°C.
Do this before epoxy wipe — epoxy in threads ruins them.

### Platform — PETG

| Setting | Value |
|---|---|
| Layer height | 0.20 mm |
| Perimeters | 4 minimum |
| Infill | 30% Grid |
| Orientation | Flat, face-up |
| Nozzle temp | 255°C |
| Bed temp | 85°C |
| Supports | Required inside both GX12 chimney bores |
| Print time | ~3.5 hours |

After print: remove chimney bore supports with a pick — do NOT ream with
a round drill (destroys anti-rotation flats). Verify Coupon 10 criteria
against full Platform before proceeding.

### Backplane — PETG Natural

| Setting | Value |
|---|---|
| Layer height | 0.20 mm |
| Perimeters | 4 |
| Infill | 65% open area (lattice — designed in geometry, not slicer infill) |
| Orientation | Flat, face-up |
| Supports | None |
| Print time | ~1 hour |

### GPS/camera bracket — PETG Natural

Flat, standard PETG settings. Print coupon 9 first.

### ASA bumpers (×4 + spares)

| Setting | Value |
|---|---|
| Layer height | 0.20 mm |
| Perimeters | 4 |
| Infill | 30% Grid |
| Orientation | Flat |
| Nozzle temp | 255°C |
| Bed temp | 95°C |
| Enclosure | Strongly recommended |
| Cooling | 10–20% |

### Mass targets by part

| Part | Target mass |
|---|---|
| Arm shaft (×4) | 15.0 g each / 60.0 g total |
| Arm tab (×8) | — |
| X body PETG bottom (×1) | 7.0 g |
| X body PCCF layers (×3) | 9.0 g each / 27.0 g total |
| X body PETG top (×1) | 18.0 g |
| Platform (×1) | 60.0 g |
| Backplane (×1) | 7.0 g |
| Full printed structure + rods + isolation + bolts | 265.0 g |

---

## Procedure

<!-- See production-run-order for sequencing. This article covers settings only. -->

### Extrusion multiplier calibration

Before any production print:
1. Print Coupon 1 (four test bores: 2.05, 2.10, 2.15, 2.20 mm).
2. Measure each bore with calipers.
3. Adjust extrusion multiplier until the 2.20 mm bore measures 2.20 ± 0.05 mm.
4. Record the multiplier (typically 0.96–0.98 for PETG).
5. Apply this multiplier to all PETG profiles before production.

---

## Rationale

### Why 8 perimeters on arm shafts

The arm shaft is a sacrificial fuse — it must absorb crash energy by
deforming, not by fracturing at the first layer boundary. Eight perimeters
creates a solid, continuous wall of PETG with no weak inter-perimeter bonds
that would cause premature delamination. The shaft deforms plastically rather
than splitting.

### Why 0% cooling on PCCF

Polycarbonate inter-layer adhesion depends on the top layer of material staying
above glass transition temperature long enough for the new layer to fuse with
it. Cooling fans quench the surface before fusion is complete, creating weak
layer boundaries that fail under structural load. PCCF with 0% cooling produces
significantly stronger parts despite the slight reduction in overhangs quality —
and the X body layers have no complex overhangs.

---

## Connections

requires:
  - [[petg]]
  - [[pccf]]
  - asa
  - [[freecad-document-setup]]
related:
  - [[coupon-validation]]
  - [[production-run-order]]
  - [[stl-export-and-slicer-setup]]
leads_to:
  - [[coupon-validation]]
  - [[production-run-order]]
