---
id: production-run-order
title: "Production run order"
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

The production run order sequences parts to respect coupon gate dependencies
and minimise the cost of failure. Four coupons are mandatory gates — if any
fail, only that coupon needs reprinting before proceeding, not downstream
production parts. The sequence also respects practical logistics: the longest
PCCF prints run first to establish the dimensional baseline while other
coupons are still printing.

Total print time: approximately 50 hours over 6–7 days for a complete
single-drone production run.

---

## Concept

### Why order matters

Parts have dependencies:
- X body PCCF layers cannot be produced until Coupon 8 (T-lock fit) passes.
  A failed PCCF layer wastes ~1.8 hours per layer (×3 = 5.5 hours total).
- Platform cannot be produced until Coupons 10 and 11 pass.
  A failed Platform wastes ~3.5 hours.
- Arm shafts should follow X body completion so the epoxy rod-sealing
  sequence can run continuously.

Running coupons first, then production parts in dependency order, reduces
the maximum wasted print time in any failure scenario.

---

## Reference

### Production sequence

| Step | Part | Qty | Est. time | Gate dependency |
|---|---|---|---|---|
| 1 | PETG Natural calibration coupons (1–3) | — | ~1 h | None |
| 2 | Coupon 8 — T-lock fit | 1 tab + 1 X body section | ~1 h | **GATE: must pass before step 3** |
| 3 | X body PCCF layers | 3 | ~5.5 h total | Coupon 8 pass |
| 4 | X body PETG top layer | 1 | ~1.5 h | None (parallel with coupons) |
| — | Install heat-set inserts in mast boss pads | — | ~15 min | After step 4 print |
| 5a | Coupon 10 — GX12-7 chimney bore | 1 block | ~45 min | **GATE: must pass before step 5c** |
| 5b | Coupon 11 — battery rail slide | 1 section | ~1 h | **GATE: must pass before step 5c** |
| 5c | Platform | 1 | ~3.5 h | Coupons 10 + 11 pass |
| — | Remove chimney bore supports; verify connector fit + battery slide on full Platform | — | ~30 min | After step 5c |
| 6 | Backplane lattice | 1 | ~1 h | None |
| 7 | Arm tabs | 8 | ~2 h total | None |
| — | Dry-fit all tabs into T-slots; verify T-lock before continuing | — | ~15 min | After step 7 |
| 8 | Arm shafts — primary set | 4 | ~14 h total (3.5 h each) | Coupon 8b pass |
| 9 | Arm shafts — spares | 2 | ~7 h total | |
| 10 | Arm cover passive — PETG-CF | 4 | ~3 h total | Coupon 6 pass (FFP3 respirator mandatory) |
| 11 | Arm cover active — PETG | 4 | ~2 h total | Coupon 7 pass |
| 12 | ASA bumpers | 8 + 4 spares | ~1.5 h | Coupon 4 pass |
| 13 | GPS/camera bracket | 1 | ~1 h | Coupon 9 pass |
| 14 | Sensor mast + cradle | 1 set | ~1.5 h | Coupon 5 pass |

### Post-production — mandatory steps before assembly

| Step | Action |
|---|---|
| Inspect all parts | Check for layer delamination, stringing, under-extrusion |
| Weigh all parts | Compare against mass targets in print-profiles |
| X body layers | Epoxy wipe on rod channels (thin application, correct any gaps) |
| Arm shafts | Epoxy rod channels at crossings — see airframe-integration |
| Platform | Support removal from GX12 chimney bores; verify connector and battery tests |
| Arm tabs | Dry-fit T-lock in all X body layer slots before epoxy |

### Coupon 8b gate — arm shafts

Before printing arm shaft production run: print Coupon 8b (rod interference
fit in PETG). This is separate from the T-lock Coupon 8 because the
interference fit tolerance is independent of the T-slot clearance.

---

## Procedure

### Managing parallel runs

Steps 3, 4, and 6 can overlap with the later coupon prints (5a, 5b) if
you have one printer:
- Run step 3 (PCCF layers) on days 1–2 if printer is available overnight.
- Run step 4 (PETG top) as a daytime print while you review PCCF results.
- Run coupons 10 and 11 before starting Platform — not before X body.

If you have two printers: PCCF layers and arm coupons can run in parallel.

### Epoxy log

Record every epoxy application:
- Date and time
- Part and location
- Mass before and after (epoxy delta)
- Maximum permitted deltas: shaft 1.0 g, tab 0.5 g, X body layer 1.5 g,
  full frame total 8.0 g

---

## Rationale

### Why arm shafts are step 8 rather than step 2

Arm shafts are long vertical prints requiring 3.5 hours each with no
opportunity for early failure detection. If the T-lock coupon (step 2)
reveals a variable adjustment that also affects rod channel geometry,
arm shaft reprinting may be required. Starting shafts after the X body
dimensional baseline is confirmed avoids this risk.

### Why PCCF layers are step 3 rather than later

PCCF layers are the longest single batch print in the sequence. Starting
them as early as possible (after Coupon 8 passes) keeps the critical path
short. If a PCCF layer fails mid-print, there is time to diagnose and
reprint within the production window without extending the overall schedule.

---

## Connections

requires:
  - [[coupon-validation]]
  - [[print-profiles]]
related:
  - [[stl-export-and-slicer-setup]]
  - [[airframe-integration]]
leads_to:
  - [[stl-export-and-slicer-setup]]
  - [[airframe-integration]]
