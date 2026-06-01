---
id: cf-rod-architecture
title: "Carbon fibre rod architecture"
version: 1.0.0
date: 2026-04-11
author: jsa
status: released
scope: libdrone
topic:
  - frame-structure
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

Four 2 mm carbon fibre rods run continuously through all five sandwich layers,
forming a box-girder spine. They serve two simultaneous purposes: structural
pre-tensioning that stiffens the sandwich without fasteners, and assembly
alignment that registers all five layers to each other during build. Rod
pre-tension is verified by acoustic ping — a correctly tensioned rod rings
when tapped.

---

## Concept

### Pre-tensioning and stiffness

A stack of flat layers bolted together has inter-layer shear resistance only
where the bolts engage. Between bolt positions, layers can micro-shift relative
to each other under vibration and load. CF rods held in tension by the sandwich
compression they create apply a distributed clamping force across the full rod
length — every point along the rod resists inter-layer shear, not just the
bolt positions.

This is the same principle as a pre-stressed concrete beam: the pre-compression
delays the onset of tensile failure and dramatically increases effective stiffness
under bending loads.

### Assembly alignment

The rods pass through channels in every layer at precisely defined positions
and heights. When rods are threaded through all five layers during assembly,
they enforce angular and translational alignment. A misaligned layer cannot
be bolted in place — the rods prevent it. This makes correct alignment the
path of least resistance during assembly, not the result of careful measurement.

### Box-girder geometry

Four rods at four distinct heights (+5.0, +2.0, −2.0, −5.0 mm from the
sandwich centreline) form a rectangular cross-section in the YZ plane. This
geometry resists bending in all directions — a single rod or two coplanar
rods would resist bending in one plane but not the perpendicular plane.

The front and rear arms are inverted relative to the left and right arms, which
reverses the rod height sign — this is what allows four continuous rods to pass
through all five layers despite the arms approaching the X body from different
directions.

---

## Reference

### Rod specification

| Parameter | Value |
|---|---|
| Material | Carbon fibre, unidirectional or woven, round section |
| Diameter | 2.0 mm OD |
| Cut length | 333.0 mm |
| Quantity per drone | 4 |
| Mass per rod | ~2.0 g |
| Total mass (set of 4) | ~8.0 g |
| Supplier | Carbonrods.cz (primary) |

### Channel geometry

| Layer | Channel diameter | Fit type |
|---|---|---|
| PCCF layers (×3) | 2.2 mm | Sliding fit |
| PETG bottom layer | 2.1 mm (core zone) / 2.2 mm (outer) | Interference fit at core |
| PETG top layer | 2.2 mm | Sliding fit |

### Rod heights in sandwich

| Position | Height from centreline |
|---|---|
| Rod 1 (outer, FR/RR arms) | +5.0 mm |
| Rod 2 (inner, FR/RR arms) | +2.0 mm |
| Rod 3 (inner, LF/LR arms) | −2.0 mm |
| Rod 4 (outer, LF/LR arms) | −5.0 mm |

### Tension verification — acoustic ping procedure

After assembly, tap each rod with a fingernail or small tool.
- **Pass:** clear ring tone, sustains for >0.5 seconds
- **Fail:** dull thud — rod is slack, re-check channel interference fit
  and rod cut length

---

## Procedure

### Threading rods during assembly

1. Lay all five X body layers in correct order: PETG bottom, PCCF ×3, PETG top.
2. Align layers by eye — T-slot pockets should stack cleanly.
3. Thread Rod 1 through the outer channel from the arm side. Use the rod tip
   to guide each layer into alignment as you thread.
4. Repeat for Rods 2, 3, 4. The fourth rod locks the assembly alignment.
5. Verify all rod ends protrude equally from both ends of the sandwich.
6. Perform acoustic ping on each rod. All four must ring.

### Rod replacement

1. Slacken sandwich bolts — do not remove.
2. Slide old rod out from one end.
3. Clean channel with compressed air if necessary.
4. Slide new rod in. Re-tension sandwich bolts to spec.
5. Verify acoustic ping.

---

## Rationale

### Why 2 mm diameter specifically

At 330 mm wheelbase, 2 mm rods provide adequate pre-tension force without
requiring excessive press-fit force in the PETG interference zone. Larger
diameters (3 mm) would require proportionally larger channel walls, increasing
the X body layer mass. Smaller diameters (1.5 mm) provide insufficient
pre-tension at this length and are prone to permanent set.

### Why four rods rather than two or six

Two rods provide good pre-tension but only a planar box-girder — poor
torsional resistance. Six rods add mass and complexity without proportional
structural gain at this scale. Four rods at the calculated heights form the
minimum geometry for effective three-dimensional pre-tensioning of the sandwich.

### Why continuous rods rather than segment-and-pin

Segmented rod systems (shorter rods with connecting pins at the X body) allow
modular arm replacement but introduce compliance at the joint. Continuous rods
eliminate all mid-span compliance and serve as the assembly alignment tool — a
benefit that segment-and-pin cannot provide.

---

## Connections

requires:
  - [[sandwich-structure]]
  - [[material-selection-philosophy]]
related:
  - [[pccf]]
  - [[petg]]
  - [[frame-structure-overview]]
  - [[cf-plate-arms]]
leads_to:
  - [[airframe-integration]]
  - [[cf-plate-arms]]
