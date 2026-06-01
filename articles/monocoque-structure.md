---
id: monocoque-structure
title: "Monocoque structure"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: generic
topic:
  - manufacturing
personas:
  - 5.student
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

A monocoque structure carries loads through its outer skin rather than through
an internal skeleton. The skin is the structure — remove it and the load path
disappears. A sandwich structure is a specific type of monocoque: two stiff
face sheets separated by a core, working together to resist bending loads far
more efficiently than either face sheet alone. libdrone's body uses a
PETG-PCCF sandwich that behaves as a monocoque panel — the body shell is
the primary load-carrying element, not internal ribs or posts. Understanding
this principle explains why wall thickness and layer orientation matter more
than infill percentage in the body panels.

---

## Concept

### Skin-bearing vs skeleton-bearing

A conventional framed structure — a truss, a space frame — carries loads
through discrete members: beams, columns, and diagonal braces. The skin
between members is non-structural; it can be removed without affecting the
load path. Aircraft fuselages of this type used external fabric over a wood
or metal frame. The frame is the structure; the skin is the cover.

A monocoque reverses this. The skin is curved or sandwich-stiffened to resist
buckling, and it carries the axial, bending, and shear loads directly. Remove
the skin and there is nothing left. Early aircraft monocoques used plywood
shells; modern aircraft use aluminium or carbon fibre shells with stringers
to prevent buckling. The weight saving over a framed structure is significant
— the skin that was dead weight in a framed structure now does structural work.

### Why sandwich is a monocoque

A flat panel fails in bending at very low load because its second moment of
area is small. A sandwich panel with the same total thickness but with two
face sheets separated by a light core has a second moment of area many times
larger — the core separates the face sheets, putting more material far from
the neutral axis where it resists bending most effectively.

For libdrone's PETG-PCCF sandwich, the PCCF layers are the face sheets (stiff,
high modulus) and the PETG layers are the core (lower modulus but continuous).
The sandwich resists bending loads that would crack a single-material panel
of the same mass. See → [[sandwich-structure]] for the specific layup and
geometry.

### Monocoque and printed geometry

FDM printing produces quasi-monocoque parts by default: the perimeter walls
are solid and stiff; the infill is sparse. The perimeter walls are the face
sheets of a thin sandwich; the sparse infill is the core. This is why
increasing perimeter count (wall thickness) improves part stiffness much more
than increasing infill percentage — the perimeters are the structural elements,
not the infill. A 3-perimeter PETG part with 15% infill is significantly
stiffer in bending than a 2-perimeter part with 40% infill of the same mass.

For body panels that carry the full frame load, libdrone specifies 4 perimeters
minimum. The infill provides compressive resistance (buckling prevention) but
is secondary to the perimeter walls.

---

## Reference

| Structure type | Load path | libdrone application |
|---|---|---|
| Framed | Internal skeleton members | — (not used) |
| Monocoque (thin shell) | Outer skin | Arm cross-section |
| Sandwich monocoque | Face sheets + core | Body top/bottom panels |
| FDM quasi-monocoque | Perimeter walls + sparse infill | All printed parts |

**Key print parameters for monocoque behaviour:**

| Parameter | Minimum | Recommended |
|---|---|---|
| Perimeters (body panels) | 3 | 4 |
| Perimeters (arms) | 3 | 4 |
| Top/bottom solid layers | 3 | 4 |
| Infill (body) | 15% | 25% |
| Infill (arms) | 20% | 25–40% |

---

## Procedure

<!-- not applicable — monocoque behaviour is designed in at print time
through perimeter count and material selection; see [[print-profiles]]
for the specific parameters and [[coupon-validation]] for validation -->

---

## Rationale

The decision to use a sandwich monocoque for the libdrone body rather than
an internal-rib design (which is common in hobby-grade printed frames) is
driven by the specific load case: distributed bending from the CF rod
pre-tension and the battery weight. An internal-rib design resists point loads
well but distributes bending loads poorly across a panel — the panel skins
delaminate from the ribs under cyclic bending. A sandwich monocoque distributes
bending loads across the full panel area and is better suited to the rod
pre-tension load case.

---

## Connections

requires:
  - [[frame-structure-overview]]
  - [[sandwich-structure]]
related:
  - [[zonal-stiffness]]
  - [[pre-tensioning]]
  - [[pccf]]
  - [[petg]]
  - [[print-profiles]]
leads_to:
  - [[sandwich-structure]]
  - [[zonal-stiffness]]
