---
id: pccf
title: "PCCF — properties and libdrone use"
version: 1.0.0
date: 2026-04-11
author: jsa
status: released
scope: libdrone
topic:
  - materials
personas:
  - 1.builder
  - 5.student
  - 7.contributor
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

PCCF (polycarbonate carbon fibre composite — Prusa PC-CF in libdrone's BOM)
is the stiffest printable material in the libdrone stack. It is used exclusively
for the three structural X body layers where dimensional stability matters most.
It requires a hardened steel nozzle, high print temperature, an enclosed
printer, and a glue stick on the bed. It is abrasive, brittle under impact, and
must never be used in crash-contact zones.

---

## Concept

### Why stiffness matters in the structural core

The X body sandwich carries the rod channels and T-slot pockets that define
the drone's geometry. Rod channels must hold their diameter under the
compressive preload of the pre-tensioned CF rods. T-slot pocket walls must
maintain their geometry under the lateral loads of tab engagement. Any
dimensional change in these features changes the rod preload, the structural
assembly alignment, or the tab engagement — all of which degrade structural
performance.

PCCF's extremely high stiffness and low thermal expansion coefficient (the
carbon fibre reinforcement constrains thermal movement) keep these dimensions
stable across the operating temperature range. Under sustained load it does
not creep. Under temperature variation it does not expand or contract enough
to change critical fits.

### Why brittleness is acceptable in the structural core

PCCF fractures rather than deforms under impact. This is acceptable — even
desirable — in the structural core because the core is not designed to absorb
crash energy. It is designed to survive while the designated fuse elements
(arm shafts, tabs) absorb energy in front of it. If the failure hierarchy
works correctly, crash energy is consumed before it reaches the PCCF layers.

If the PCCF layers do fracture, they fracture cleanly — which means the
failure is visible and the replacement decision is unambiguous. A PETG layer
might deform invisibly and continue to carry load at reduced capacity; PCCF
either survives intact or breaks clearly.

### Carbon fibre abrasion

The carbon fibre in PCCF is chopped short-strand, distributed throughout the
matrix. It is highly abrasive to brass nozzles — a standard brass 0.4 mm
nozzle will wear significantly within a single print. A 0.6 mm hardened
steel nozzle is mandatory. Keep a spare — PCCF and PETG-CF together will
exhaust a nozzle faster than PETG alone.

---

## Reference

### Material properties

| Property | Value | Notes |
|---|---|---|
| Print temperature (nozzle) | 290–300°C | Higher than standard PC; verify with spool datasheet |
| Bed temperature | 110°C | PEI sheet; glue stick mandatory |
| Enclosure | Required — door closed, >40°C ambient | Without enclosure: layer delamination and warping |
| Cooling | 0% | No part cooling — maintains inter-layer adhesion |
| Nozzle | 0.6 mm hardened steel — mandatory | Brass nozzles wear within one print |
| Moisture sensitivity | High | Dry at 80°C for 6 hours if any doubt; PCCF is hygroscopic |

### Key print settings (X body PCCF layers)

| Setting | Value |
|---|---|
| Layer height | 0.20 mm |
| Perimeters | 4 |
| Infill | 40% Grid or Gyroid |
| Solid layers | 5 top / 5 bottom |
| Orientation | Flat — all three identical layers |
| Glue stick | Mandatory on PEI |

### X body PCCF layer specification

| Parameter | Value |
|---|---|
| Quantity | 3 identical layers (layers 2, 3, 4 of sandwich) |
| Thickness | 3 mm each |
| Mass target | 9.0 g each / 27.0 g total |
| Rod channel diameter | 2.2 mm (sliding fit — not interference) |
| Coupon required | Coupon 8 (T-lock fit) — must pass before full production |

### What PCCF must not touch

- **Interference fit rod channels** — use 2.2 mm, not 2.1 mm; brittle matrix
  cannot tolerate radial compression stress
- **Post-processing with Dremel** — PCCF chips and cracks; any reaming
  operation risks micro-fractures
- **Heat-set inserts** — PCCF is too stiff and too brittle; heat-set inserts
  go in PETG top layer only
- **Crash-contact zones** — arm shafts, tabs, bottom layer must be PETG

---

## Procedure

### Drying PCCF

1. Dry at 80°C for 6 hours minimum before any print.
2. Print immediately — PCCF re-absorbs moisture quickly in humid conditions.
3. Signs of wet PCCF: surface bubbling, voids in perimeters, poor layer fusion.
4. Never print PCCF with a spool that has been open for more than 48 hours
   without re-drying.

### Bed preparation

1. Clean PEI sheet with IPA — 99% isopropyl alcohol, lint-free cloth.
2. Apply thin even layer of glue stick to the full print area.
3. Heat bed to 110°C before starting print.
4. Do not remove part until bed has cooled to below 50°C — PCCF contracts
   on cooling and releases cleanly if allowed to cool fully.

---

## Rationale

### Why Prusa PC-CF specifically

Prusa PC-CF is validated at the print settings documented here on a Prusa
CoreOne+ printer. Generic PCCF filaments vary in carbon fibre loading, matrix
viscosity, and moisture sensitivity. Using an unvalidated PCCF risks print
failure on the most difficult parts of the build. Once a reliable alternative
is validated with documented settings, it may be added to the approved
materials list.

### Why 0.6 mm nozzle rather than 0.4 mm

A 0.4 mm nozzle limits the minimum feature size but increases the number of
perimeter passes required for a given wall thickness. For PCCF, which must
not be reprocessed, a failed print from nozzle clogging mid-layer wastes
expensive material. The 0.6 mm nozzle provides larger melt throughput, lower
pressure build-up, and longer service life against abrasion. The slight
reduction in maximum feature resolution is irrelevant at the X body's
minimum feature sizes (smallest feature: 2.2 mm rod channel wall).

---

## Connections

requires:
  - [[material-selection-philosophy]]
related:
  - [[petg]]
  - [[sandwich-structure]]
  - [[cf-rod-architecture]]
  - [[coupon-validation]]
  - [[print-profiles]]
leads_to:
  - asa
