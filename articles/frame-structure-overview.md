---
id: frame-structure-overview
title: "Frame structure overview"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - frame-structure
personas:
  - 1.builder
  - 4.workshop
  - 5.student
  - 6.evaluator
  - 7.contributor
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The libdrone V2.4.x airframe is a 330 mm wheelbase True-X quadrotor built as a
three-layer architecture: a five-layer printed sandwich body at the bottom, a
PETG platform layer in the middle carrying all electronics and connectors, and a
PETG lattice backplane on top carrying payload modules. Four carbon fibre rods
run continuously through all five sandwich layers, aligning the structure and
providing a pre-tensioned box-girder spine. Every dimension is driven by a
parametric variable table — no fixed numbers appear in the CAD model.

---

## Concept

### True-X geometry

A True-X frame places all four arms at equal 45° angles from the longitudinal
axis. Each motor sits at the corner of a square rotated 45° relative to the
body. The result is a frame that is symmetric in both roll and pitch: the moment
of inertia and motor-to-motor distance are identical on both axes. Handling
feels the same whether the drone pitches forward or rolls sideways.

The alternative, the stretched-X, displaces the front and rear motor pairs
further apart. This creates an asymmetry that must be compensated in the PID
tuning — roll and pitch feel different. libdrone uses True-X to keep the tuning
symmetric and to allow a single PID profile to apply correctly to both axes.

### Wheelbase

Wheelbase is measured motor-to-motor diagonally. At 330 mm the frame fits
6-inch propellers with a minimum 15 mm tip clearance — enough to protect
props during normal operation without making the frame unnecessarily large.
The 330 mm class is well characterised in the community: components, props,
and tooling are widely available and tested at this size.

### Three-layer architecture

The body separates structural, electrical, and payload functions into three
distinct layers that can be built, maintained, and replaced independently:

- **Sandwich body** — structural spine. Five printed layers, CF rod skeleton,
  arm attachments. Never removed in service.
- **Platform** — electronics carrier. Single PETG piece, 283 × 40/50 mm,
  sitting on top of the sandwich. Contains battery rails, wire channels,
  GX12 connector chimneys, fan slot. Removable if a complete electronics
  replacement is required.
- **Backplane** — payload carrier. Open PETG lattice, 187 × 50 mm, sitting
  on top of the platform. Carries payload masts and the Pi bay. Removable
  in 60 seconds without disturbing flight electronics.

### Arm design

Each arm is a two-piece printed assembly: a shaft printed vertically and two
tabs printed horizontally. The shaft carries the motor and the CF rod bending
load. The tabs engage T-slot pockets in the PCCF structural layers via a
T-profile mechanical lock — no adhesive, no heat-set inserts in PCCF. The
shaft attaches to the tabs via two M2 screws per tab, accessible from the
arm tip. The joint is designed so that the shaft can be replaced in the field
in under 5 minutes without disturbing the sandwich.

### Parametric model

Every dimension — core size, arm length, rod offset, layer thickness, motor
spacing — is a named variable in a FreeCAD spreadsheet. Changing the wheelbase
or adapting to a different prop size requires editing a handful of values; the
entire model rebuilds. This is the mechanism that allows community adaptation
without forks of the geometry files.

---

## Reference

### Key dimensions (V2.4.6)

| Parameter | Value | Variable name |
|---|---|---|
| Wheelbase | 330 mm | `#Wheelbase` |
| Prop size | 6 inch | — |
| Arm angle | 45° (True-X) | — |
| Sandwich height | 16 mm total | `#SandwichHeight` |
| Core size | see Variables | `#XBodyCoreSize` |
| Arm width | see Variables | `#XBodyArmWidth` |
| Arm length | see Variables | `#XBodyArmLength` |
| CF rod diameter | 2.0 mm OD | `#RodDia` |
| CF rod length | 333.0 mm | `#RodLength` |
| Rod channel diameter | 2.2 mm | `#RodDiaChannel` |
| Rod channel (core zone) | 2.1 mm | `#RodDiaChannelCore` |
| Sandwich bolt | M3 × 20 mm | — |
| Sandwich bolt torque | 0.3 N·m | — |

### Layer stack

| Layer | Material | Thickness | Function |
|---|---|---|---|
| 1 (bottom) | PETG | 3 mm | Impact face, rod interference fit |
| 2 | PCCF | 3 mm | Structural — T-slots |
| 3 | PCCF | 3 mm | Structural — T-slots |
| 4 | PCCF | 3 mm | Structural — T-slots |
| 5 (top) | PETG | 4 mm | Clean structural face, attachment holes |

### Mass budget (frame structural)

    hw_xbody_all_layers_target          = 52.0 g
    hw_arms_total_target                = 60.0 g   (shafts)
    hw_tabs_total_target                = 12.0 g
    hw_covers_total_target              = 36.0 g
    hw_bumpers_total_target             = 12.0 g
    hw_rod_cf_2mm_set4_weight_target    =  8.0 g
    hw_frame_structural_total_target    = 140.0 g  (gate)

### Prop clearance (330 mm wheelbase, 6-inch props)

Minimum tip clearance: 15 mm.
At 330 mm wheelbase the motor-to-motor distance along one arm axis is 233 mm.
Half of that is 116.5 mm from centre to motor. A 6-inch (152 mm diameter,
76 mm radius) prop tip sits at 116.5 + 76 = 192.5 mm from centre.
Adjacent prop tip distance check: adequate margin confirmed at V2.4.6 geometry.

---

## Procedure

<!-- not applicable — this is an overview article. For build procedures see
sandwich-structure (§ Assembly sequence) and arm-shaft (§ Arm installation). -->

---

## Rationale

### Why True-X and not stretched-X

Stretched-X frames are popular in racing because placing the front motors
further forward shifts the CG bias and makes the frame feel more responsive
in forward flight. libdrone is not a racing frame — it carries payloads and
is expected to behave predictably in all orientations. True-X symmetry
means a single tuned PID profile applies correctly to both roll and pitch
without cross-axis compensation. Symmetric maintenance: any arm is
interchangeable without re-tuning.

### Why 330 mm and not 250 mm or 450 mm

250 mm (5-inch) frames are lighter but cannot carry the payload mass budget
(up to 93 g for EASA Open A2 compliance) while remaining within thrust-to-weight
targets. 450 mm (7-inch) frames exceed the EASA Open A1 mass limit at 250 g
AUW and require a larger battery that offsets the efficiency gain. 330 mm
(6-inch) is the smallest class that satisfies the payload, thrust, and
regulatory constraints simultaneously.

### Why three separate layers instead of a monocoque

A single printed body with all features integrated would be lighter on paper
but has two practical problems: any damage to one zone requires replacing
the entire body; and features in different zones (structural sandwich,
electronics attachment, payload interface) have conflicting print orientation
requirements. Three layers allow each to be printed and replaced optimally.
The mass penalty is small; the maintenance benefit is large.

### Why no adhesive in the T-slot joint

Adhesive in a T-slot creates a permanent bond that turns the arm shaft from
a replaceable fuse into a structural member. If the arm is glued in, a crash
that would otherwise cost one printed shaft instead propagates force into the
T-slot, the PCCF layer, and potentially the electronics. The no-adhesive rule
is not a simplification — it is the mechanism that makes the failure hierarchy
work. → See [[failure-hierarchy]].

---

## Connections

requires: []
related:
  - [[cf-rod-architecture]]
  - [[floating-motor-mounts]]
leads_to:
  - [[sandwich-structure]]
  - [[arm-shaft]]
  - [[failure-hierarchy]]
  - [[zonal-stiffness]]
  - [[pre-tensioning]]
  - [[exact-constraint-design]]


[failure-hierarchy]: failure-hierarchy.md "Failure hierarchy"
[cf-rod-architecture]: cf-rod-architecture.md "Carbon fibre rod architecture"
[floating-motor-mounts]: floating-motor-mounts.md "Floating motor mounts"
[sandwich-structure]: sandwich-structure.md "Sandwich structure"
[arm-shaft]: arm-shaft.md "Arm shaft"
[zonal-stiffness]: zonal-stiffness.md "Zonal stiffness"
[pre-tensioning]: pre-tensioning.md "Pre-tensioning"
[exact-constraint-design]: exact-constraint-design.md "Exact constraint design"
