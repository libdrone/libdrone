---
id: procurement
title: "Procurement"
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

Procurement is the longest lead-time step in the build. AliExpress orders take
10–15 days — place them on Day 1 without exception. Electronics from Czech
hobby suppliers (HobbyDrone, RCStudio) take 7–10 days. Local hardware is
available within 24 hours. A two-frame build with goggles costs approximately
34,000 CZK; a single-frame build approximately 18,000 CZK. Nothing in the BOM
is sourced from a single-vendor proprietary supply chain — every component has
documented alternatives.

---

## Concept

### MoSCoW priority in the BOM

Every item in the shopping list carries a MoSCoW rating: Must (build impossible
without it), Should (quality or safety impact), Could (workflow comfort, not
critical), Won't (consciously deferred). "Won't" is as important as "Must" —
an explicit decision not to buy something prevents scope creep. The sensor
payload (SEN66, ESP32-S3) is "Won't" relative to the flight build. Buy the
sensor payload when the drone is flying reliably.

### Lead time governs the order

Order in this sequence on Day 1: AliExpress first (10–15 days), Czech hobby
suppliers second (7–10 days), Prusa.shop (next-day), local hardware (same day).
Printing and coupon validation (Phase 2) run in parallel with the AliExpress
wait — waiting idle is a planning error.

---

## Reference

### Must-have electronics

| Item | Source | Notes |
|---|---|---|
| Matek H7A3-SLIM FC | AliExpress | H7 class required for RPM filter |
| Pilotix 75A AM32 4-in-1 ESC 6S | HobbyDrone.cz | AM32 open firmware |
| HDZero Freestyle V2 VTX + camera | HobbyDrone.cz | Includes MIPI cable |
| HDZero Goggle 2 | HobbyDrone.cz | Analog fallback for Core |
| BrotherHobby Avenger V2 2507 1750KV ×4 | AliExpress | |
| Matek M10Q-5883 GPS/compass | AliExpress | |
| RadioMaster RP2 ELRS receiver | HobbyDrone.cz | Bind before fitting |
| HQProp 6×3×3 PC tri-blade ×8 | AliExpress | 4× CW + 4× CCW |
| HQProp 6×2.5×3 PC tri-blade ×8 | AliExpress | Low-pitch alternate |
| M5 prop nuts CW+CCW ×8 | AliExpress | 5mm shaft — required |
| Tattu R-Line V3 1800mAh 6S XT60 ×3 | AliExpress | |
| XL4015 buck converter | Laskakit.cz | 9–12V for VTX |
| TVS diode SMBJ28A ×5 | AliExpress | SMBJ28A only |
| Panasonic 1000µF 35V low-ESR cap | AliExpress | ESR <0.1Ω at 100kHz |
| 100µF MLCC ceramic cap ×5 | AliExpress | FC 5V secondary filter |
| VIFLY ShortSaver V2 | AliExpress | First power-on protection |

### Must-have mechanical and consumables

| Item | Source | Notes |
|---|---|---|
| Silicone O-rings ID4/OD7/CS1.5 ×50 | AliExpress | 40–50 Shore A |
| Silicone tubing OD6/ID4 500mm | AliExpress | Motor mount sleeves |
| Super Lube 52004 grease | AliExpress | O-ring lubrication |
| MR30 connector pairs ×15 | AliExpress | Motor connectors |
| M3 × 30mm brass standoffs ×17 | Laskakit.cz | FC/ESC stack |
| M3 × 20mm stainless ×24 | Screw kit | Motor mount screws |
| M3 nyloc nuts ×24 | Screw kit | Motor mount |
| Loctite 243 | local | Pinch bolts only — not motor screws |
| Electrolube HPA200H 200ml aerosol | Farnell CZ | Acrylic conformal coating |
| Electrolube UltraSolve 200ml | Farnell CZ | Coating remover for rework |
| TDK clip-on ferrite 3.5mm ×10 | AliExpress | VTX power wire |

### Total cost reference

| Configuration | Estimated |
|---|---|
| Single-frame build (no goggles) | ~18,000 CZK |
| Two-frame build with HDZero Goggle 2 | ~34,000 CZK |
| + Sensor payload (SEN66 mast) | +2,650 CZK |

---

## Procedure

### Day 1 procurement sequence

1. Place AliExpress order: O-rings, silicone tubing, MR30 connectors,
   capacitors, ferrite beads, motors, batteries, hardware kits, conformal
   coating, ferrites. Select tracked shipping.
2. Place HobbyDrone.cz / RCStudio.cz order: FC, ESC, VTX + camera, goggles,
   GPS, ELRS receiver, props.
3. Place Prusa.shop order if filament or nozzle stock is low.
4. Source locally same day: M3/M2 screw assortment, Loctite 243, cable ties.
5. Order Electrolube HPA200H + UltraSolve from Farnell CZ or RS Components CZ.
6. While waiting for AliExpress: begin Phase 0 (parametrics) and Phase 2
   (coupon printing). Do not wait idle.

### Receiving verification

1. Check every package against the BOM line item. Count quantities.
2. Capacitors: verify Panasonic FM or low-Z markings — reject generic unmarked.
3. O-rings: verify shore hardness on listing (40–50A). Reject if unlisted.
4. Motors: spin by hand — smooth, no cogging. Inspect shaft for straightness.
5. Props: inspect for moulding defects. Any chip or flash — discard.
6. Log all items received. Note any substitutions or shortfalls.

---

## Rationale

### Why Day 1 for AliExpress regardless of build readiness

The 10–15 day transit window is independent of readiness. Placing the order
early buys time — if the order is delayed, the build is not blocked. Placing it
late compounds all other delays. The cost of ordering Day 1 is zero.

---

## Connections

requires: []
related:
  - [[lipo-batteries]]
  - [[floating-motor-mounts]]
  - [[conformal-coating]]
leads_to:
  - [[prep-and-parametrics]]
  - [[coupon-validation]]
