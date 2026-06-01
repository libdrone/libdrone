---
id: coupon-validation
title: "Coupon validation"
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
  - 7.contributor
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Coupons are small test prints that validate critical fit geometry before
committing to full production parts. Every printer has slightly different
dimensional accuracy. Coupons find the calibration offset for your specific
printer and filament before a 5-hour print reveals the problem. Four coupons
are critical-path — do not print the X body layers, platform, or arm shafts
until these four pass. Skipping coupons trades 2–4 hours of coupon time for
a potential 20+ hours of wasted production prints.

---

## Concept

### Why printers produce dimensionally inaccurate parts

Fused deposition modelling (FDM) printing has several sources of dimensional
error: extrusion multiplier (how much plastic is actually extruded vs commanded),
thermal expansion of the filament during deposition, layer cooling contraction,
and bed adhesion forces that pull the bottom layers outward.

These errors are consistent for a given printer, filament, and settings —
which means they can be characterised and compensated. Coupons are the
characterisation step. Once you know your printer prints 2.2 mm channels as
2.1 mm, you can adjust the variable to compensate before printing the full part.

### Which coupons are critical-path

A coupon is critical-path if a production print that fails its test cannot be
reworked and must be reprinted from scratch. The critical-path coupons are:

- **Coupon 8** — T-lock fit. Fails: X body PCCF layers and arm tabs must both
  be reprinted. Potential waste: 8+ hours.
- **Coupon 8b** — Rod interference fit in PETG bottom layer. Fails: PETG
  bottom layer must be reprinted.
- **Coupon 10** — GX12-7 chimney D-D bore. Fails: full Platform print must
  be reprinted. Platform is the most complex and longest print.
- **Coupon 11** — Battery rail slide test. Fails: full Platform print must
  be reprinted.

---

## Reference

### Complete coupon list

| # | Name | Parts tested | Critical path |
|---|---|---|---|
| 1 | Rod fit (PETG Natural) | 2.05/2.1/2.15/2.2 mm bore block | No — calibration only |
| 2 | Pinch slit | Arm shaft section + M3 + 2 mm rod | No |
| 3 | Motor head | Full-scale motor head with counterbores + MR30 channel | No |
| 4 | ASA bumper | Full bumper | No |
| 5 | Sensor mast base | 20×20 mm base footprint | No |
| 6 | Arm cover passive | O-ring boss section + nyloc pocket | No |
| 7 | Dovetail groove fit | 50 mm shaft section + active cover section | No |
| **8** | **T-lock fit** | **One arm tab + X body layer section with T-slot** | **YES** |
| **8b** | **Rod interference fit** | **30 mm cube with 2.1 mm channel** | **YES** |
| 9 | GPS bracket fit | Bracket camera and GPS pocket top section | No |
| **10** | **GX12-7 chimney bore** | **30×30×30 mm block with D-D bore + chimney** | **YES** |
| **11** | **Battery rail slide** | **100 mm rail section both rails + base plate** | **YES** |

### Coupon 8 — T-lock fit

**Print:** One full arm tab + 50 mm section of X body PCCF layer with
one T-slot pocket. Same wall thickness and settings as production.

| Test | Pass criteria |
|---|---|
| Slide tab into T-slot | Light hand pressure only |
| Lateral play when seated | Zero |

**Adjust:** If binds → open Variables → increase `TabClearance` by 0.1 mm
→ reprint. If play → decrease `TabClearance` by 0.1 mm → reprint.

**Do not print full X body PCCF layers until Coupon 8 passes.**

### Coupon 8b — Rod interference fit

**Print:** 30 mm cube with one 2.1 mm channel through it. PETG only.

| Test | Pass criteria |
|---|---|
| Thread 2 mm CF rod by hand | Grips firmly, requires light push, does not fall through |

**Adjust:** Too tight → increase `RodDiaChannelCore` to 2.15 mm.
Too loose → decrease to 2.05 mm.

### Coupon 10 — GX12-7 chimney D-D bore

**Print:** 30×30×30 mm block with:
- Ø14 mm boss, 3 mm proud
- D-D bore: 11.87 mm full diameter, 10.80 mm flat-to-flat (anti-rotation flats required)
- Ø18 mm OD chimney, 25 mm deep
- 6×4 mm wire exit slot at chimney base

| Test | Pass criteria |
|---|---|
| GX12-7 MALE body slides into D-D bore | Fits without binding |
| Connector body in bore | Does NOT rotate (flats grip) |
| Panel nut | Threads fully without cross-threading |
| Wire exit slot | 6-wire bundle (6×28 AWG) passes through |
| Support removal | Clean — no torn walls inside chimney bore |

**Adjust:** Connector rotates → decrease `GX12ChimneyBoreFlatFlat` by 0.1 mm.
Connector binds → increase `GX12ChimneyBoreFlatFlat` by 0.1 mm.

**Note:** Do not use a round drill to clear the D-D bore — it destroys the
anti-rotation flats. Use a pick for support removal only.

**Do not print full Platform until Coupon 10 passes all five tests.**

### Coupon 11 — Battery rail slide test

**Print:** 100 mm section of both rails with 10 mm base plate.
Battery reference: 78×40×53 mm. Rail inner width: 41 mm. Rail height: 53 mm.
Include: endstop wall, lateral strap slots.

| Test | Pass criteria |
|---|---|
| Battery slides in from right | Seats against endstop cleanly with no binding |
| Battery slides out | Releases with light hand pressure, no snagging |
| 25 mm strap through strap slots | Passes cleanly |

**Adjust:** Binding → increase `BattRailInnerWidth` by 0.2 mm.

**Do not print full Platform until Coupon 11 passes all three tests.**

---

## Procedure

### Coupon print sequence

1. Print PETG Natural coupons 1–3 (~1 hour). Tune extrusion multiplier.
2. Print Coupon 8 (T-lock fit) (~1 hour). Must pass before X body production.
3. Print Coupon 8b (rod interference) (~20 min). Must pass before PETG bottom layer.
4. Print Coupon 10 (GX12 chimney) (~45 min). Must pass before Platform.
5. Print Coupon 11 (battery rail) (~1 hour). Must pass before Platform.
6. Print remaining coupons 4–7, 9 in parallel with early production parts.

---

## Rationale

### Why coupons rather than adjusting after first production print

A failed X body PCCF layer represents ~5.5 hours of print time and ~40 g of
expensive PCCF filament. A failed Platform represents ~3.5 hours and significant
PETG. Coupon 8 represents ~1 hour of print time. The expected value of skipping
Coupon 8 is strongly negative — the probability of a fit failure multiplied by
the cost of reprinting far exceeds the cost of the coupon itself.

The coupon philosophy generalises: any critical-path geometric feature that
depends on printer calibration requires a coupon before production.

### Why adjust variables rather than reworking the print

Post-processing PCCF (drilling, reaming) risks micro-fractures. Post-processing
PETG is possible but introduces inconsistency — a Dremel-opened channel will
not match the surface finish of a printed channel and may not hold rod tension
uniformly. Variable adjustment followed by reprint produces a more reliable
result than mechanical rework, and the adjusted variable becomes the baseline
for future builds.

---

## Connections

requires:
  - [[variable-table-structure]]
  - [[print-profiles]]
related:
  - [[production-run-order]]
  - [[pccf]]
  - [[petg]]
  - [[cf-rod-architecture]]
leads_to:
  - [[production-run-order]]
