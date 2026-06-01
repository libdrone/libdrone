---
id: scaling-libdrone
title: "Scaling libdrone to a new frame size"
version: 1.0.0
date: 2026-04-11
author: jsa
status: released
scope: libdrone
topic:
  - cad-parametric
personas:
  - 7.contributor
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

libdrone is designed to scale from 5-inch to 10-inch and beyond. The same
architecture — sandwich X body, platform, backplane, dual GX12-7 payload
interface — works at any wheelbase because most geometry is parametrically
derived from the wheelbase variable. However, not everything scales
automatically. Prop clearance, battery rail dimensions, EASA category, and
motor/ESC selection all require explicit human judgement at every new scale.
The payload interface is deliberately scale-independent — a payload built for
libdrone 6 plugs into libdrone 10 without modification.

---

## Concept

### Frame-driven vs electronics-driven geometry

Scaling intuition says "bigger frame = bigger everything." This is wrong for
libdrone. The frame geometry scales. The electronics geometry does not.

**Frame-driven variables** are derived from wheelbase. When wheelbase grows,
the arms get longer, the X body core gets larger, the rod length changes.
These variables cascade automatically through the parametric model.

**Electronics-driven variables** are set by the components, not the frame.
A 10-inch libdrone uses the same Matek H7A3-SLIM FC, the same Pilotix 75A ESC,
the same GX12-7 connectors, the same HDZero VTX. The platform that carries
them does not grow with the frame. The platform is long enough to fit the
electronics — and that length is independent of how big the arms are.

The critical insight: when scaling from 6-inch to 10-inch, the arms grow by
roughly 70 mm each. The platform stays approximately the same length.

### Payload interface scale-independence

The dual GX12-7 connector standard is deliberately fixed at all scales:
- Connector geometry: identical
- Boss pad M3 spacing (20 mm): identical
- Backplane post spacing: follows electronics zone, not frame size

A payload built for libdrone 6 plugs into libdrone 10 without modification.
This is the core commercial and community argument for the platform: builders
invest in payloads once and run them on any frame size. Breaking this
compatibility requires a version bump of the payload interface standard, not
a routine scale change.

### What requires human judgement

Parametric models can propagate known relationships. They cannot make decisions
that require new calculations:

**Prop clearance** — the platform width at the arm root zones must give
sufficient clearance between the prop disc and the platform edge. This depends
on prop diameter, arm angle, and platform width. At every new scale, this
geometry must be calculated from scratch. The V2.4.6 values (40 mm narrow /
50 mm electronics) are correct for 330 mm wheelbase and 6-inch props only.

**Battery selection** — a larger frame carries a larger battery. Battery rail
dimensions are set by the physical battery dimensions. Update `BattRailInnerWidth`,
`BattLength`, `BattWidth`, `BattHeight` after selecting the battery for the
new scale.

**EASA category** — all-up weight determines regulatory category. Recalculate
AUW at every scale. A 10-inch libdrone will almost certainly exceed the 900 g
Open A2 boundary and operate as A3.

---

## Reference

### Variables that change at new scale

| Variable | Driver | Action |
|---|---|---|
| `Wheelbase` | Frame size | Change this first — cascades to arm and rod variables |
| `ArmShaftLength` | Wheelbase + hub geometry | Recalculate from new wheelbase geometry |
| `RodLength` | Wheelbase | Recalculate; verify in Assembly (Box-in-Box check) |
| `PlatformAttachPostY` | Electronics layout | Verify — may need adjustment if electronics layout changes |
| `PlatformWidthNarrow` | Prop clearance | Recalculate from prop diameter and arm angle |
| `PlatformWidthElec` | Electronics + prop clearance | Recalculate — may differ from narrow width |
| `BattRailInnerWidth` | Battery choice | Update for new battery dimensions |
| `BattLength`, `BattWidth`, `BattHeight` | Battery choice | Update for new battery |

### Variables that do not change at new scale

`PlatformLength`, `StackPattern`, `GX12PositionY`, `MIPIChannelWidth`,
`FanSlotDim`, `GX12BossDia`, `GX12ChimneyOD`, `GX12ChimneyBoreFlatFlat`,
`MastBossSpacing`, `MastBossSpacingY`

---

## Procedure

### Scaling sequence

1. Duplicate the `.FCStd` file. Rename:
   `libdrone_[size]inch_V10.FCStd`
2. Open the Variables spreadsheet. Change `Wheelbase` only.
3. Recalculate prop clearance manually from new wheelbase and prop diameter.
   Adjust `PlatformWidthNarrow` if needed. Adjust `PlatformWidthElec`
   only if the electronics zone prop clearance is affected.
4. Recalculate `ArmShaftLength` from new wheelbase geometry.
5. Update `RodLength` (verify exact value in Assembly — Box-in-Box check).
6. Choose battery for new frame size. Update all battery rail variables.
7. Recalculate mass budget. Verify EASA category at estimated AUW.
8. Select motor and ESC for new frame size. Update mass budget.
9. Run full Assembly verification:
   - Rod clearance check (Box-in-Box)
   - Corner post check
   - Chimney clearance check
10. Print coupons before any production parts. Fit tests are more critical
    at a new scale than at an iterated known scale.

---

## Rationale

### Why payload interface is fixed at all scales

A scalable hardware platform that requires payload redesign at every scale
has no commercial advantage over a single-scale platform. The GX12-7 interface
was chosen and dimensioned to be compatible with the physical scale range of
libdrone (5–12 inch). Fixing it creates the ecosystem compounding effect:
each new payload adds value to all past and future frame scales simultaneously.

### Why platform length is electronics-driven

The instinct is to scale everything with the frame. But the platform exists to
carry specific electronics — a FC with a known bolt pattern, a GPS module of
known size, a VTX of known dimensions. These do not change with frame size.
A 10-inch frame with a stretched platform wastes weight and moves the battery
CG position without serving any engineering purpose. The platform length is
derived from the electronics layout, not the frame.

---

## Connections

requires:
  - [[parametric-modelling-philosophy]]
  - [[variable-table-structure]]
related:
  - [[freecad-document-setup]]
  - [[frame-structure-overview]]
  - [[payload-architecture]]
leads_to:
  - [[freecad-workbenches]]
