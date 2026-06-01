---
id: freecad-workbenches
title: "FreeCAD workbenches and modelling fundamentals"
version: 1.0.0
date: 2026-04-11
author: jsa
status: released
scope: libdrone
topic:
  - manufacturing
personas:
  - 1.builder
  - 4.workshop
  - 5.student
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

FreeCAD organises its tools into Workbenches — each one a set of tools for
a specific task. libdrone uses three: Spreadsheet for variables, Part Design
for solid modelling, and Assembly for fit verification. Understanding the
difference between a Sketch and a Feature, and knowing about the Topological
Naming problem, prevents the most common beginner mistakes before they happen.

---

## Concept

### The three fundamental ideas

**Sketches** are 2D drawings on a flat plane. You draw lines, rectangles,
arcs, and circles. You add dimensions to make them precise. A sketch is always
on a plane — the XY, XZ, or YZ base plane, or a datum plane you create.
A sketch that is fully constrained (every dimension and position is fixed)
is shown in green. Under-constrained sketches (blue elements remain) will
produce unpredictable results when you try to make them 3D.

**Features** are operations applied to sketches to produce or modify 3D
geometry. The most common:
- **Pad** — push a 2D sketch into the third dimension to create solid material
- **Pocket** — remove material by pushing a sketch into existing solid
- **Loft** — blend between two or more sketches on parallel planes

**The Model Tree** on the left side of the FreeCAD screen lists every sketch
and feature in order. It is the build history of the part. You can
double-click any item to go back and edit it. This is what makes parametric
modelling powerful — and what makes feature order important.

### The Topological Naming problem

FreeCAD has a known limitation: when you add, remove, or reorder features
in the model tree, references to specific faces and edges can silently break.
A pocket that was correctly placed on a face may detach and move to a different
face. FreeCAD 1.1 has substantially reduced this problem but has not eliminated
it entirely.

Two habits prevent most topological naming problems:
1. **Build in sequence.** Add features at the end of the tree. Never insert
   a feature early in the tree after later features already exist.
2. **Reference datum planes, not faces.** If a sketch needs to be at a specific
   height, create a datum plane at that height and attach the sketch to the
   datum plane — not to the face of an existing feature.

When the model does break (yellow warning triangles appear in the Model Tree):
open the warned feature, re-select the reference it lost, click OK.

### The three standard planes

Every new Body has three standard planes:
- **XY Plane** — flat, like a floor. Use for top-down profiles.
- **XZ Plane** — faces toward you, like a wall. Use for side profiles.
- **YZ Plane** — faces to the right. Use for front profiles.

libdrone parts are modelled with consistent axis orientation:
- X = left/right
- Y = forward/backward (nose = +Y)
- Z = up/down

---

## Reference

### Three workbenches used in libdrone

| Workbench | Purpose | When to switch |
|---|---|---|
| Spreadsheet | Create and edit the Variables spreadsheet | First — before any modelling |
| Part Design | Solid modelling: sketches, pads, pockets, lofts, fillets | All part modelling |
| Assembly | Bring parts together, verify fit, check clearances | After all parts are complete |

Switch workbench using the dropdown selector in the top toolbar. Switching
does not close or lose work.

### FreeCAD keyboard shortcuts (essential)

| Shortcut | Action |
|---|---|
| Ctrl+S | Save |
| Space | Toggle visibility of selected item |
| V, F | Fit all (view all geometry) |
| Numpad 0 | Home view |
| Numpad 2/4/6/8 | Rotate view |
| Escape | Exit current tool / close sketch |
| D, S | Toggle sketch solver display |

### Viewport navigation (CAD style)

| Action | Mouse |
|---|---|
| Rotate | Middle mouse button + drag |
| Pan | Middle mouse button + Ctrl + drag |
| Zoom | Scroll wheel |
| Select | Left click |
| Multi-select | Ctrl + left click |

---

## Procedure

### Creating a new Body

1. Switch to Part Design workbench.
2. Part Design menu → Body → Create Body.
   (Or: Model menu → Body.)
3. Rename immediately: right-click Body in Model Tree → Rename →
   type descriptive name (e.g. `Arm`, `X Body PCCF Base`) → Enter.
4. The Body is now active (shown in bold). All features created next belong to it.

### Creating a sketch on a base plane

1. Part Design → New Sketch (or toolbar icon).
2. Select the plane: click XY, XZ, or YZ in the Model Tree, or click a flat
   face in the viewport.
3. The Sketcher opens. Draw geometry using the Sketcher toolbar.
4. Add constraints: dimensions (D key), coincident, parallel, perpendicular.
5. Verify: all sketch elements are green (fully constrained).
6. Close sketch: Sketcher menu → Close Sketch, or close button in task panel.

### Creating a datum plane at a specific height

1. Part Design → Datum → Datum Plane.
2. In the task panel: Attachment mode → Translate → set Z offset to required height.
3. Rename the datum plane in the Model Tree with a descriptive label.
4. Attach future sketches to this datum plane — not to feature faces.

---

## Rationale

### Why three workbenches rather than one

FreeCAD's workbench architecture separates tools by workflow stage. This keeps
each workbench's toolbar uncluttered and reduces accidental tool activation.
The Spreadsheet workbench protects the variable table from accidental editing
during modelling. The Assembly workbench provides dedicated fit-check tools
that are not available in Part Design. The separation is a feature, not a
complexity cost.

### Why datum planes over face references

Face references are fragile — they depend on the internal face numbering that
FreeCAD uses, which can change when features are added. Datum planes are
stable geometry objects in the model tree with their own stable references.
The practice of using datum planes is the single most effective defence against
topological naming problems in complex models.

---

## Connections

requires:
  - [[freecad-document-setup]]
  - [[variable-table-structure]]
related:
  - [[topological-naming-problem]]
  - [[parametric-modelling-philosophy]]
  - [[freecad-assembly-workbench]]
leads_to:
  - [[coupon-validation]]
  - [[production-run-order]]
  - [[freecad-assembly-workbench]]
