---
id: parametric-modelling-philosophy
title: "Parametric modelling philosophy"
version: 1.0.0
date: 2026-04-11
author: jsa
status: released
scope: libdrone
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

libdrone uses parametric CAD — every dimension in every part is driven by a
named variable in a central spreadsheet. Changing one variable (for example,
wheelbase) cascades into all dependent dimensions automatically. This means
the entire frame can be scaled to a different size by changing a handful of
numbers, without manually editing geometry. It also means the model has a
single source of truth: the Variables spreadsheet. If a dimension is wrong,
fix it in the spreadsheet — never by editing geometry directly.

---

## Concept

### What parametric modelling is

In non-parametric CAD, you draw dimensions as fixed numbers: "this wall is
3 mm thick." If you want to change it, you find the sketch, change the
number, and hope nothing else breaks.

In parametric CAD, you draw dimensions as references to named variables:
"this wall is `=Variables.WallThick`." The variable lives in one place. When
you change `WallThick` from 3 to 4, every wall in every part that references
that variable updates simultaneously.

The model becomes a function: input is the variable table, output is the
complete geometry. Change the inputs, the outputs update.

### Why this matters for libdrone specifically

libdrone is designed to scale from 5-inch to 10-inch and beyond. The same
architecture — sandwich X body, platform, backplane, dual GX12-7 payload
interface — must work at any wheelbase. Without parametric modelling, each
new scale is a complete re-draw. With parametric modelling, most of a new
scale emerges from changing a few frame-driven variables.

It also matters for community reproducibility. A builder who wants to
adjust arm width, wall thickness, or rod channel diameter for their printer's
calibration changes one or two variables rather than hunting through fifteen
sketches. The adjustment is auditable: the git history shows exactly what
was changed and when.

### The single source of truth principle

No dimension in any part should be typed as a fixed number if it is also
expressed as a variable in the spreadsheet. If `ArmWidth` appears in the
spreadsheet, then any sketch dimension equal to arm width must reference
`=Variables.ArmWidth`, not the number 26. A hardcoded dimension that
duplicates a variable is a silent consistency risk — if the variable changes,
the hardcoded dimension does not.

This principle extends to the documentation: the Variables document
(`LD_-_Variables_v246.md`) is the canonical source for all geometry values.
The Hardware Reference and Master Specification reference the variable names,
not the values.

---

## Reference

<!-- not applicable — this is a philosophy article; specifics in variable-table-structure -->

---

## Procedure

<!-- not applicable -->

---

## Rationale

### Why FreeCAD rather than Onshape or Fusion 360

FreeCAD runs locally — no account, no cloud, no subscription, no terms of
service that can be changed unilaterally. The `.FCStd` file format is
open and version-controllable. A model made today will open in FreeCAD in
20 years without any commercial dependency. This aligns directly with the
FOSS philosophy of the libdrone platform.

Onshape and Fusion 360 are more polished tools with better topological naming
robustness. They are not used because they create a commercial lock-in
incompatible with a platform designed to be independently reproducible by
communities who may not have institutional software budgets.

### Why a spreadsheet-based variable system rather than a dedicated parameter manager

FreeCAD's native parameter manager (as of 1.1) has stability limitations with
complex models. A Spreadsheet workbench document, properly structured with
aliases, is simple, readable, exportable as CSV, and has been validated across
the full libdrone V2.4.x model. It works. The macro (`LD_V343_Variables.FCMacro`)
creates the entire spreadsheet in seconds — the overhead of setup is near zero.

---

## Connections

requires: []
related:
  - [[variable-table-structure]]
  - [[freecad-document-setup]]
  - [[scaling-libdrone]]
  - [[open-source-philosophy]]
  - [[freecad-parametric-scaling]]
leads_to:
  - [[variable-table-structure]]
  - [[freecad-document-setup]]
  - [[freecad-parametric-scaling]]
