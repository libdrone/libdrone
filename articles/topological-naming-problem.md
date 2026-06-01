---
id: topological-naming-problem
title: "Topological naming problem"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - cad-parametric
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

The topological naming problem (TNP) is a failure mode in parametric CAD where
a model feature that references a face, edge, or vertex by an automatically
assigned internal ID breaks when an earlier feature in the model tree is
modified. The referenced face changes its ID because the geometry regenerated,
but the downstream feature still holds the old ID — the reference becomes
stale and the model fails to rebuild. FreeCAD is particularly affected.
The mitigation is a modelling discipline: always reference named datums
(planes, lines, points) rather than geometry faces, and order the model tree
to minimise cascading dependencies.

---

## Concept

### How parametric CAD identifies geometry

In a parametric model, every face, edge, and vertex of the solid is assigned
an internal identifier — a topological name — that other features can reference.
"Pad the face marked Edge42" or "Mirror across the plane that is Face7."
The model tree is a sequence of operations, each consuming references to the
geometry produced by earlier operations.

The problem arises because these IDs are not stable. When any feature earlier
in the tree changes — a sketch dimension, a pad depth, an array count — the
solid is regenerated from scratch. Faces that were created in one order may be
created in a different order after the change. The IDs reassign. A downstream
feature holding a reference to the old ID now points to a different face,
or to nothing.

### What a TNP failure looks like

The model turns red and stops rebuilding. Affected features show an error:
"Shape is null" or "Face not found." The error propagates down the tree:
every feature that depended on the broken reference also fails, even if those
features themselves were not changed. A single variable edit at the top of the
tree can break dozens of features in a complex model.

In FreeCAD specifically, the TNP is a known architectural issue. FreeCAD 1.0
introduced a topological naming algorithm that substantially mitigates it for
new models, but the problem can still appear in certain modelling patterns,
particularly when features reference geometry created by Boolean operations
or arrays.

### Why datums are the solution

A datum is an explicit geometric construction — a plane, a line, a point —
that does not depend on the topology of any solid. It depends only on:
- Other datums, or
- Parameters from the variable spreadsheet.

A datum plane defined as "offset 15 mm from the XY plane" is stable regardless
of how any solid changes. A feature that references this datum plane rather
than a solid face will survive any model change that does not move the datum
itself.

The rule is: **reference datums, not solid faces.** Every attachment, mirror,
pocket, and pad should reference a datum plane or datum axis as its reference
geometry. Solid faces are used only for the initial sketch placement — once a
sketch is attached to a datum, it no longer needs a face.

### Model tree ordering

A secondary mitigation is controlling the order of operations in the model tree.
Features near the top of the tree have fewer dependencies and are less likely
to change ID when earlier features change. Specifically:

- **All datums first.** Every datum plane, datum axis, and datum point belongs
  at the top of the tree, immediately after the parameter spreadsheet. They
  must never be interspersed between solid features.
- **Sketches reference datums, not faces.** Map-mode attachment uses a datum
  plane as the reference, not "the top face of the previous pad."
- **Bodies are independent.** In a multi-body model, each body's features
  should reference that body's own datums, not faces of a different body.
  Cross-body face references are a common TNP source in assembly models.

---

## Reference

### TNP risk by feature type

| Feature type | TNP risk | Mitigation |
|---|---|---|
| Sketch attached to datum plane | None | — already mitigated |
| Sketch attached to solid face | High | Attach to datum plane instead |
| Mirror feature referencing datum plane | None | — |
| Mirror feature referencing solid face | High | Create datum plane first |
| Linear/polar pattern | Medium | Use datum axis as direction reference |
| Boolean fusion/cut | Medium | Ensure result body has own datums before downstream features |
| Chamfer / fillet | High (modifies topology) | Place last; no downstream references |
| Pocket in parametrically-driven part | Medium | Reference sketch dimensions, not resulting faces |

### FreeCAD 1.1 notes

FreeCAD 1.1 (used in libdrone CAD workflow) includes the Realthunder topological
naming mitigation merged into the mainline. New models built with 1.1 are
substantially less affected than models built with 0.19 or earlier. However:

- The mitigation is not a complete solution — it applies to Part Design bodies
  but not to all workbenches equally.
- Models migrated from earlier FreeCAD versions may still carry fragile face
  references from the original build.
- The libdrone parametric model is built from scratch in 1.1 with datum-first
  discipline — no migrated legacy references.

For version-specific UI steps for creating datum planes and setting sketch
attachment in FreeCAD 1.1, see [[freecad-ui-110]].

---

## Procedure

### Creating a datum plane in FreeCAD 1.1

1. With the active Body selected in the model tree, open Part Design workbench.
2. Part Design → Datum → Create a datum plane (or keyboard shortcut — see
   [[freecad-ui-110]]).
3. In the Attachment dialog, set Mode to a stable reference: "XY/XZ/YZ plane"
   or "Offset from plane" with a datum or base plane as reference.
4. Enter the offset value — reference a spreadsheet alias (`=Variables.LayerOffset`)
   rather than a typed number.
5. Click OK. The datum appears in the tree above all solid features.
6. Rename it immediately (right-click → Rename). A name like `DatumTopFace`
   is always preferable to `DatumPlane` or `DatumPlane001`.

### Attaching a sketch to a datum plane

1. Select the target datum plane in the model tree.
2. Part Design → New Sketch. FreeCAD attaches the sketch to the selected datum.
3. Verify in the sketch's Map Mode property: it should show the datum plane name,
   not a face reference like `Face7`.

### Diagnosing a TNP failure

1. The red features in the tree identify the broken references. Start from
   the topmost red feature — that is the root cause.
2. Edit that feature's attachment or reference. Replace any face or edge
   reference with a datum reference.
3. If no datum exists for that geometry, create one first, then update the reference.
4. Recompute the model (Edit → Refresh). Cascading errors should clear once
   the root reference is fixed.

---

## Rationale

### Why this article is in cad-parametric and not freecad-ui

The TNP is a conceptual problem in parametric modelling, not a UI procedure.
Understanding why it occurs and how to prevent it applies to any parametric
CAD tool — SolidWorks, Fusion 360, and Inventor all have variants of the same
problem. The solution (datum-first discipline, stable reference hierarchy) is
a modelling practice, not a menu click.

The UI-specific steps for creating datum planes in FreeCAD 1.1 are in
[[freecad-ui-110]]. This article explains the reasoning that makes those steps
necessary.

### Why libdrone models are built datum-first from the start

A model can be retrofitted to use datum references after the fact, but it
is significantly more work than building datum-first from the beginning. Every
broken reference must be individually diagnosed and repaired. On a model with
hundreds of features, this is a days-long effort. The libdrone CAD architecture
enforces datum-first as a constraint, not a recommendation, so that the model
remains stable as the variable table evolves across design iterations.

---

## Connections

requires: []
related:
  - [[freecad-document-setup]]
  - [[freecad-workbenches]]
  - [[variable-table-structure]]
leads_to:
  - [[freecad-ui-110]]
  - [[parametric-modelling-philosophy]]
