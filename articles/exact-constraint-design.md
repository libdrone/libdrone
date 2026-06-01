---
id: exact-constraint-design
title: "Exact constraint design"
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
  - 1.builder
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Exact constraint design is a structural principle that states each degree
of freedom in a joint should be constrained exactly once. Under-constraining
a joint allows unintended movement; over-constraining it introduces internal
stress from manufacturing tolerance mismatches. In libdrone's 3D-printed
frame, over-constraint — most commonly from redundant contact surfaces
or too many fasteners at a single joint — causes printed parts to crack at
the over-constrained point during assembly or under thermal cycling. Identifying
and eliminating over-constraint is a design step, not an assembly step.

---

## Concept

### Degrees of freedom

A rigid body in three dimensions has six degrees of freedom: three translational
(X, Y, Z) and three rotational (roll, pitch, yaw). A joint constrains some
of these; the remaining unconstrained DOFs allow the bodies to move relative
to each other. A fully constrained joint eliminates all six DOFs.

Exact constraint means: to eliminate N degrees of freedom, use exactly N
independent constraint contacts. Six contacts for a fully constrained joint.
Fewer contacts leave DOFs unconstrained — the part can move. More contacts
over-constrain — the part cannot accommodate manufacturing variation between
the contact points and will be stressed or cracked by the attempt.

### Over-constraint in printed joints

Consider a sandwich panel bolted to the arm with four bolts in a rectangular
pattern. The four bolt holes in the panel and the four threaded inserts in
the arm must be positioned with sub-millimetre accuracy to avoid over-constraint.
If the holes are 0.2 mm off-pitch relative to the inserts, the bolts cannot
all be inserted without deflecting the panel — introducing stress at assembly.
With two bolts, the panel floats to accommodate tolerances; with four bolts,
it cannot.

The solution in libdrone is to use the minimum number of fasteners that
correctly constrains the joint, and to design the remaining contacts as
slip surfaces that locate but do not bind. The body tab-and-slot system
locates the arm assembly radially (two DOFs constrained by the slot geometry)
with the rod providing the third translational constraint and the arm bolt
providing the rotational lock. Each constraint is independent.

### Under-constraint and drift

Under-constraining is the opposite failure: a joint with too few contacts
will drift under repeated loading. An arm that is press-fit on the rod but
not rotationally constrained will slowly rotate under propeller torque,
changing the motor angle. The libdrone pinch slit design constrains rotation
by clamping the rod in a slit whose width is smaller than the rod diameter —
adding rotational constraint after the rod channel provides radial constraint.
Each constraint is added to close a specific DOF, not added in bulk.

---

## Reference

| libdrone joint | DOFs constrained | Constraint mechanism |
|---|---|---|
| Rod in arm channel | Radial (2 translational) | Interference fit bore |
| Arm rotation on rod | Rotational (1) | Pinch slit clamp |
| Arm axial position | Axial (1 translational) | Arm tab in body slot |
| Motor position | All (6) | 4× M3 bolts on 16 mm pattern |
| Sandwich panel | All (6) | 6-bolt pattern + surface contact |

---

## Procedure

### Diagnose over-constraint during assembly

1. Attempt dry assembly without fasteners. Parts that locate correctly
   and sit flat under their own weight are correctly constrained.
2. Insert fasteners in opposite pairs (diagonal for bolt patterns). If
   any fastener requires more than finger-tight force before other fasteners
   are inserted, the pattern is over-constrained for the printed tolerance.
3. If over-constraint is detected, identify which fastener is the redundant
   constraint (the one that cannot insert freely) and replace the fixed hole
   with a slot that allows the part to float in one direction.

---

## Rationale

Exact constraint principles were adopted from precision instrument design
(Whitworth's principle, Maxwell's criteria) where over-constraint is a known
source of measurement error and part failure. In FDM printing, tolerances
of ±0.2 mm are routine — significantly looser than machined parts. This makes
over-constraint a greater practical risk in printed assemblies than in
machined assemblies, where tighter tolerances can absorb the redundant
constraints without stress. Applying exact constraint analysis explicitly
to libdrone's joint design is one of the primary reasons the frame
can be printed on consumer printers without failure.

---

## Connections

requires:
  - [[frame-structure-overview]]
  - [[six-degrees-of-freedom]]
related:
  - [[pre-tensioning]]
  - [[sandwich-structure]]
  - [[cf-rod-architecture]]
  - [[arm-shaft]]
  - [[print-profiles]]
leads_to:
  - [[pre-tensioning]]
  - [[coupon-validation]]
