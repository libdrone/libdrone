---
id: material-selection-philosophy
title: "Material selection philosophy"
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
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

libdrone uses three materials — PETG, PCCF, and ASA — each assigned to the
function it performs best. No single material is best at everything. The design
rule is: match the material to the mechanical demand of the zone, not to
convenience or cost. Using the wrong material in the wrong zone produces a
drone that fails unpredictably rather than at the designed weak point.

---

## Concept

### Right material, right zone

Every material has a characteristic combination of stiffness, toughness, thermal
resistance, printability, and cost. These properties trade off against each other
— a stiffer material is typically more brittle, a tougher material typically
deflects more under load. The goal is not to find the best material overall but
to assign materials so each zone gets the property it needs most.

**Stiffness** resists deformation under load. High stiffness is needed where
dimensional precision must be maintained — the structural core of the X body,
where rod channels and T-slot positions are fixed geometry.

**Toughness** absorbs energy without fracturing. High toughness is needed at
crash contact zones — arm shafts, tabs, the bottom X body layer — where
impact energy must be absorbed and dissipated rather than transmitted into
the structural core.

**UV and thermal stability** matter for externally exposed surfaces that see
weather and sunlight continuously. UV degradation causes surface cracking and
embrittlement over time; thermal creep under sustained load causes dimensional
change.

### The weakest link is a design tool

The arm shaft is deliberately the weakest structural element. This is not a
deficiency — it is a controlled failure point. A drone that breaks predictably
at the cheapest, fastest-to-reprint part is more maintainable than one that
breaks unpredictably at an expensive or difficult-to-replace component.

The material assignment reinforces this: PETG arm shafts sacrifice before PCCF
X body layers, which sacrifice before the electronics. The failure sequence is
designed in, not left to chance.

---

## Reference

| Zone | Material | Primary property required | Part examples |
|---|---|---|---|
| Structural core | PCCF | Stiffness, dimensional stability | X body layers 2–4 |
| Crash contact / fuse | PETG | Toughness, impact absorption | Arm shafts, tabs, X body bottom layer |
| External exposure | ASA | UV stability, surface hardness | Bumpers |
| Functional structural | PETG | Toughness + printability | GPS bracket, platform, backplane |

---

## Procedure

<!-- not applicable -->

---

## Rationale

### Why not use one material throughout

A single-material frame forces a compromise — either everything is stiff and
brittle (PCCF throughout: expensive, crash-catastrophic, hard to repair) or
everything is tough and compliant (PETG throughout: structurally inadequate for
the rod channel dimensional requirements).

The three-material approach assigns the optimal material to each function at the
cost of managing three filament types and three print profiles. The maintenance
burden is justified by the performance and repairability gains.

### Why PCCF for the structural core specifically

The X body rod channels and T-slot pockets are precision geometry. Rod channel
diameter is 2.2 mm for the PCCF layers — any dimensional creep changes the
rod preload and the assembly alignment. PCCF's low thermal expansion coefficient
and high stiffness maintain these dimensions across operating temperatures.
PETG would creep under the sustained compressive load of the pre-tensioned rods.

### Why not use carbon fibre composite (CFC) plate

CFC plate is stiffer and lighter than printed PCCF but cannot be produced in
a 3D printing facility, requires cutting tools, and cannot carry the complex
3D geometry (rod channels, T-slot pockets, counterbores) that the X body layers
require. PCCF printed parametrically gives 90% of CFC's stiffness at full
geometric freedom and zero external fabrication dependency.

---

## Connections

requires: []
related:
  - [[petg]]
  - [[pccf]]
  - asa
  - [[cf-rod-architecture]]
  - [[failure-hierarchy]]
leads_to:
  - [[petg]]
  - [[pccf]]
  - asa
