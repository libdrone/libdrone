---
id: print-production
title: "Print production run"
version: 1.0.0
date: 2026-04-13
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

The production print run prints all structural parts in a fixed sequence
governed by material and geometry. PCCF structural layers print first
(highest failure risk, requires hardened nozzle, longest cooling time).
PETG arm shafts follow (tallest parts, print vertical, 3.5 hours each).
ASA bumpers and PETG accessories complete the run. No part should be
assembled before all parts have been post-processed — epoxy wipe-coat
and heat-gun treatment are applied across all structural parts together.
Total print time: approximately 38 hours over 5 days. Post-processing
adds 2 hours. Coupon 8 (T-lock fit) must pass before any PCCF layer
is printed.

---

## Concept

### Why PCCF prints first

PCCF (polycarbonate carbon fibre) is the most demanding material in the
build: it requires a hardened nozzle (E3D ObXidian 0.6mm), a heated chamber
or enclosure, textured powder-coated bed with glue stick, and a strictly
tuned print profile. A PCCF print failure (delamination, warping, poor
layer adhesion) discovered on Day 8 after printing everything else in PETG
means reprinting the most critical structural component under time pressure.

Printing PCCF first — when attention is highest, settings are freshest, and
there is time to adjust and reprint — eliminates this risk. If PCCF fails,
the PETG parts have not been printed yet and nothing is wasted.

### Coupon 8 gates the production run

→ See [[coupon-validation]] for the full coupon procedure.

Coupon 8 (T-lock fit test) must pass before the first PCCF layer is printed.
The coupon is a 50mm section of X body with one T-slot, printed at production
settings. The arm tab must slide in with light hand pressure and show zero
lateral play when seated. If the coupon fails, adjust the T-slot variable
in FreeCAD and reprint the coupon — not the full X body layer.

### Post-processing sequence

All structural parts (X body layers, arm shafts) receive post-processing
after printing and before assembly:

1. **Heat-gun treatment** (250°C, 15 seconds per face) — fuses surface layers,
   improves interlayer adhesion, removes minor surface fuzz. Use FFP3 mask —
   PCCF dust is hazardous.
2. **Epoxy wipe-coat** (thin laminating epoxy) — applied to arm shafts and
   X body layers only. Not to tabs, mast, or bracket. Tape rod channels and
   motor bore before coating. Full cure before assembly.
3. **IPA wipe** — removes any release agent or contamination before assembly.

Post-process all parts before assembling any. Post-processing after assembly
is impractical.

---

## Reference

### Print sequence and durations

| Step | Part | Material | Orientation | Time | Notes |
|---|---|---|---|---|---|
| 3.1 | **Coupon 8** (T-lock gate) | PCCF | Flat | 30 min | Must pass before proceeding |
| 3.2 | PCCF X Body Base Layer ×2 | PCCF | Flat | 3.0 hrs | Cool to 60°C before removal |
| 3.3 | PCCF X Body Top Layer ×1 | PCCF | Flat | 1.5 hrs | Check stack holes and bracket holes |
| 3.4 | PETG Arm Tabs ×8 | PETG | Horizontal | 2.0 hrs | T-lock profile sharp; M2 holes clean |
| 3.5 | PETG Arm Shafts ×4 (build) | PETG | **Vertical** | 14.0 hrs | Rod channels clear; pinch slit clean |
| 3.6 | PETG Arm Shafts ×2 (spares) | PETG | **Vertical** | 7.0 hrs | Same settings as build shafts |
| 3.7 | ASA Bumpers ×8 + 4 spares | ASA | Flat | 1.5 hrs | ASA: warping risk, use enclosure |
| 3.8 | GPS/Camera Bracket ×1 | PETG | Flat | 1.5 hrs | MIPI channel clear; camera slot tilt correct |
| 3.9 | Sensor mast + cradle | PETG Natural | Vertical / Flat | 1.5 hrs | Only after Coupon 5 mast fit passes |
| **Total** | | | | **~32.5 print hrs** | + 2 hrs post-process |

### Quality checks by part

| Part | Check |
|---|---|
| PCCF X body layers | T-slot walls intact; rod channels clear and round; no delamination |
| Arm tabs | T-lock profile sharp; M2 screw holes clear; no warping |
| Arm shafts | Rod channels round and clear; pinch slit gap 0.3–0.5mm; bumper notch correct depth; dovetail groove present on bottom face |
| Bumpers | No warping; snap-fit geometry intact |
| GPS/Camera bracket | MIPI channel fully enclosed; camera slot tilt angle correct; GPS bracket flat |

---

## Procedure

### Production run start-up

1. Verify Coupon 8 has passed → T-lock fit confirmed at production settings.
2. Verify PCCF print profile is loaded: hardened 0.6mm nozzle, bed temp 100°C,
   ambient ≥ 25°C (enclosure or heated space required).
3. Apply glue stick to textured powder-coated sheet.
4. Print X Body Base Layer 1. Do not open enclosure until part cools to 60°C.
5. Inspect: T-slot walls, rod channels, no delamination. If fail — adjust
   settings and reprint before continuing.
6. Print X Body Base Layer 2. Inspect same.
7. Print X Body Top Layer. Inspect for bracket holes and stack holes in addition
   to standard checks.
8. Switch nozzle and profile to PETG for remaining parts.
9. Print arm tabs, arm shafts (vertical), bumpers, bracket in sequence.
10. Post-process all structural parts together: heat-gun, epoxy coat, IPA wipe.
11. Cure completely before beginning Phase 4 (airframe integration).

### Arm shaft vertical print guidance

Arm shafts print vertically (base down) to ensure the rod channels are
round and clean along their full length. Horizontal printing of arm shafts
creates layer lines perpendicular to the rod, which creates stress
concentrations along the shaft — not the intended failure direction.

The vertical print is tall (~250mm) and takes 3.5 hours per shaft. Print
with supports disabled — the geometry is self-supporting. Brim enabled
(10mm) to prevent warping on the first layer.

---

## Rationale

### Why spare arm shafts are printed in the production run

Arm shafts are the designed crash fuse — they are expected to fracture in
crashes. Printing spares during the production run uses the same settings,
the same spool of filament, and the same nozzle condition as the build
shafts. Printing spare shafts after the first crash — at an unknown point
in the future, with different spool remaining and potentially different
settings — risks producing shafts with different mechanical properties.
Two spare shafts add 7 hours of unattended print time to the production
run. They will be used.

---

## Connections

requires:
  - [[coupon-validation]]
  - [[print-profiles]]
  - [[stl-export-and-slicer-setup]]
related:
  - [[material-selection-philosophy]]
  - [[sandwich-structure]]
  - [[arm-shaft]]
leads_to:
  - [[airframe-integration]]
