---
id: freecad-parametric-scaling
title: "FreeCAD parametric scaling"
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
  - 7.contributor
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Parametric scaling in libdrone means changing the wheelbase variable in the
spreadsheet and having the frame geometry update automatically — arms grow
longer, the body expands, rod channels reposition — without touching individual
sketches. This works because every geometric dimension is an expression
referencing a spreadsheet cell rather than a hardcoded number. However, not
all variables scale with the wheelbase: electronics stack mounting patterns,
GX12 connector geometry, and battery connector clearances are fixed by hardware
and must be kept constant regardless of airframe scale. Understanding which
variables are frame-driven and which are electronics-driven is a prerequisite
for scaling the model without breaking it.

---

## Concept

### Two classes of variable

**Frame-driven variables** are geometric parameters that should change when
the wheelbase changes. Arm length, body width, rod channel spacing, mast
height — all of these are proportional to the airframe scale. If you double
the wheelbase from 220 mm to 440 mm, arm length roughly doubles, the body
widens, the rod spacing increases.

**Electronics-driven variables** are fixed by hardware constraints that do
not change with airframe scale. The FC stack mounting pattern is 30×30 mm on
all libdrone variants — a larger airframe does not get a larger FC. The GX12
chimney bore diameter is 14.5 mm regardless of airframe size. Battery connector
clearance is fixed by the connector geometry, not the frame size. Scaling these
variables with the wheelbase would produce a model where the FC holes are too
far apart for any real FC, or where the GX12 bore is so large the connector
falls through.

### The scaling sequence

Changing the wheelbase variable is not the first step — it is step four of
a validated sequence:

1. **Read the scaling notes in the Variables spreadsheet** before changing
   anything. The notes column on each variable identifies whether it is
   frame-driven, electronics-driven, or requires human judgement.
2. **Change only frame-driven variables** in proportion to the target scale.
   The wheelbase is the primary driver; derived variables (arm length, body
   width) will update automatically if their expressions are correct.
3. **Verify electronics-driven variables are unchanged.** Open the spreadsheet
   after the change and confirm that FC stack pattern, GX12 geometry, and
   connector clearances show their expected fixed values.
4. **Check items that require human judgement.** Some variables — GPS mast
   height, wall thickness, battery rail spacing — are not simple functions
   of wheelbase and require the designer to assess whether the scaled value
   is physically sensible. The Variables document flags these explicitly.
5. **Run the FreeCAD model** and inspect for sketch over-constraints or
   red geometry — indications that expressions evaluated to impossible values.

### What requires human judgement

Parametric scaling does not replace engineering judgement. Specifically:

- **Wall thickness** does not scale linearly with wheelbase. A body designed
  for 220 mm may use 2.0 mm walls adequately; at 440 mm wheelbase, the same
  wall thickness may be insufficient for the increased bending moment. Thickness
  should be reviewed, not blindly scaled.
- **Arm cross-section** — a wider arm at larger scale may be needed even
  though the spreadsheet variable scales the arm length but not the cross-section.
- **Battery rail spacing** — determined by the specific battery form factor,
  not the airframe size.
- **GPS mast height** — must clear the prop arc at the new prop size, which
  grows non-linearly with wheelbase.

---

## Reference

### Variable classification (selected)

| Variable | Class | Notes |
|---|---|---|
| `wb` (wheelbase) | Frame-driven | Primary scale driver |
| `arm_length` | Frame-driven | Derived from wheelbase |
| `body_width` | Frame-driven | Derived from wheelbase |
| `rod_spacing` | Frame-driven | Derived from body width |
| `fc_stack_pattern` | Electronics-driven | Fixed: 30×30 mm |
| `gx12_bore_dia` | Electronics-driven | Fixed: 14.5 mm |
| `xt30_clearance` | Electronics-driven | Fixed by connector |
| `wall_thickness` | Human judgement | Review at each scale |
| `arm_width` | Human judgement | Review at each scale |
| `gps_mast_height` | Human judgement | Must clear prop arc |

Full variable table: → [[variable-table-structure]] and → [[variable-table-values]].

---

## Procedure

### Scale the model to a new wheelbase

1. Open `LD_V245_Variables.FCMacro` in FreeCAD. Run the macro to populate
   the spreadsheet if starting from scratch. See → [[prep-and-parametrics]].
2. In the spreadsheet, change the `wb` cell to the target wheelbase.
3. Check all frame-driven variables: confirm they updated to proportional values.
4. Check all electronics-driven variables: confirm they remain at their
   fixed values (not scaled).
5. Identify all human-judgement variables. Evaluate each one for the new
   scale: is the wall thickness sufficient? Does the mast height clear the
   new prop size?
6. Resolve any red (failed) geometry in the Part Design bodies.
7. Run the assembly check. See → [[freecad-assembly-workbench]].
8. Print coupons at the new scale before committing to full production.
   See → [[coupon-validation]].

---

## Rationale

The frame-driven / electronics-driven classification was made explicit in
the Variables document after a scaling attempt that changed the GX12 chimney
bore in proportion to the wheelbase, producing a bore too large for the
connector. Labelling each variable with its class in the spreadsheet notes
column prevents this category error. The human-judgement category was added
because some builders interpreted "parametric" as meaning the model required
no judgement — which is incorrect and leads to geometrically consistent but
physically wrong designs.

---

## Connections

requires:
  - [[parametric-modelling-philosophy]]
  - [[prep-and-parametrics]]
  - [[variable-table-structure]]
related:
  - [[variable-table-values]]
  - [[freecad-document-setup]]
  - [[freecad-assembly-workbench]]
  - [[topological-naming-problem]]
leads_to:
  - [[freecad-assembly-workbench]]
  - [[coupon-validation]]
  - [[stl-export-and-slicer-setup]]
