---
id: freecad-assembly-workbench
title: "FreeCAD Assembly workbench"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: libdrone
topic:
  - cad-parametric
personas:
  - 1.builder
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The FreeCAD Assembly workbench (Assembly 4 in FreeCAD 0.21; integrated
Assembly in FreeCAD 1.0+) assembles separately modelled parts into a single
document for fit verification, clearance checking, and export. In the
libdrone workflow, assembly serves one function: confirming that printed
parts fit together before committing to a full production run. Key checks
are box-in-box rod clearance, backplane corner post alignment, and GPS
mast vertical clearance above the prop plane. Assembly does not replace
physical coupon testing but catches modelling errors that coupons cannot.

---

## Concept

### Assembly as verification, not design

In the libdrone parametric workflow, parts are designed individually in the
Part Design workbench, driven by the central spreadsheet variables. The
assembly is the proof that the variables are internally consistent — that
the rod channel positions in the arm match the rod channel positions in the
body, that the GX12 chimney height clears the backplane boss, that the GPS
mast does not intersect the prop arc.

This is different from an assembly-first workflow where geometry is created
in context of other parts. libdrone parts are fully defined by their own
sketches and the spreadsheet — the assembly is the final check, not the
origin of dimensions.

### Joint types in FreeCAD Assembly

FreeCAD's Assembly workbench constrains parts relative to each other using
joints. The relevant joint types for libdrone:

**Fixed joint**: eliminates all 6 DOFs between two parts. Used to place the
body at the origin — one part in every assembly must be fixed as the reference.

**Cylindrical joint**: constrains 4 DOFs, leaving rotation and translation
along a single axis free. Used to represent the CF rod in its channel —
the rod can slide along its axis and rotate, but cannot translate radially.
This correctly models the pre-tensioned rod fit.

**Planar joint**: constrains 3 DOFs (one translation + two rotations), leaving
translation in a plane free. Used for the backplane resting on the attachment
posts — it can slide in the XY plane until the bolt holes align.

After joints are applied, parts that are correctly constrained should snap
to their geometric position without residual DOFs. A part that "floats" after
jointing has unconstrained DOFs — check which joint is missing.

### What to check in the libdrone assembly

**Rod clearance (box-in-box):** The CF rods must clear the electronics stack
inside the body. In top view, verify the rod paths do not intersect any
component footprint. The rods run diagonally through the body corners; the
clearance to the FC stack edges is typically 1–2 mm and is the tightest
tolerance in the assembly.

**Backplane corner post engagement:** The backplane's boss rings must seat
fully on the platform's chimney posts. Check that the boss ring inner diameter
matches the chimney post outer diameter and that the seating depth is correct.

**GPS mast height:** In side view, verify the GPS mast top (compass position)
is above the prop plane by the design margin (≥10 mm above prop tip arc).

---

## Reference

**FreeCAD version note:** In FreeCAD 1.0+, the Assembly workbench is integrated
into the main application. In FreeCAD 0.21, install the Assembly 4 add-on via
the Add-on Manager. The joint names differ slightly between versions but the
concepts are the same.

**Assembly file organisation:**

      libdrone.FCStd
      └── Assembly
         ├── body_top.FCStd (linked)
         ├── body_bottom.FCStd (linked)
         ├── arm_×4.FCStd (linked)
         ├── platform.FCStd (linked)
         ├── backplane.FCStd (linked)
         └── gps_mast.FCStd (linked)

Use linked parts (File → Link) rather than copying geometry into the assembly
document. Linked parts update automatically when the source file changes —
a dimension change in `arm.FCStd` propagates to the assembly on next open.

---

## Procedure

### Create the libdrone assembly

1. Open a new FreeCAD document. Switch to Assembly workbench.
2. Insert the body bottom as the fixed reference part: Insert → Link →
   select `body_bottom.FCStd`. Apply a Fixed joint to the world origin.
3. Insert the arm: Insert → Link → select `arm.FCStd`. Apply a Cylindrical
   joint between the arm's rod channel axis and the body's rod channel axis.
   Repeat for all four arms.
4. Insert the body top. Apply a Planar joint between the body top's
   sandwich surface and the body bottom's mating surface.
5. Insert the platform. Apply appropriate joints to the attachment post
   geometry.
6. Insert the backplane. Apply joints to the chimney posts.
7. Run the solver (Solve in the Assembly toolbar). All parts should
   snap to their constrained positions.
8. Perform clearance checks: toggle visibility of individual parts to inspect
   rod paths, backplane engagement, and mast height.

---

## Rationale

The assembly step was added to the libdrone workflow after two production runs
where modelling errors (a rod channel 0.3 mm off-position, a chimney post
0.5 mm too short) were not detected until physical assembly. Both errors
required reprinting the affected parts. Assembly verification in FreeCAD
costs 30 minutes; reprinting a body panel costs 4–6 hours. The assembly
step is mandatory before any production run of more than two units.

---

## Connections

requires:
  - [[freecad-document-setup]]
  - [[freecad-workbenches]]
  - [[prep-and-parametrics]]
related:
  - [[topological-naming-problem]]
  - [[arm-shaft]]
  - [[coupon-validation]]
  - [[freecad-parametric-scaling]]
  - [[stl-export-and-slicer-setup]]
leads_to:
  - [[coupon-validation]]
  - [[stl-export-and-slicer-setup]]


[freecad-document-setup]: freecad-document-setup.md "FreeCAD document setup"
[freecad-workbenches]: freecad-workbenches.md "FreeCAD workbenches and modelling fundamentals"
[prep-and-parametrics]: prep-and-parametrics.md "Prep and parametrics"
[topological-naming-problem]: topological-naming-problem.md "Topological naming problem"
[arm-shaft]: arm-shaft.md "Arm shaft"
[coupon-validation]: coupon-validation.md "Coupon validation"
[freecad-parametric-scaling]: freecad-parametric-scaling.md "FreeCAD parametric scaling"
[stl-export-and-slicer-setup]: stl-export-and-slicer-setup.md "STL export and slicer setup"
