---
id: sk-freecad-build-guide
title: "FreeCAD Build Guide"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 1.builder
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

After following this guide, the builder has a complete, validated FreeCAD
parametric model of their specific libdrone configuration, with all parts
ready to export for slicing. This skeleton is the 3.0.0 replacement for the
V2.4.6 FreeCAD Cookbook — a 2,083-line step-by-step guide. The skeleton
provides the arc; the atoms provide the reference; the Cookbook provides
the detailed click-map for each modelling operation.

**This guide requires the V2.4.6 FreeCAD Cookbook open on your second screen.**
The Cookbook contains FreeCAD-version-specific UI interactions (menu paths,
dialog names, constraint tools) that change between FreeCAD versions. This
skeleton provides the conceptual structure and decision points; the Cookbook
provides the exact click sequence.

---

## Concept

### Why parametric before printing

→ [[parametric-modelling-philosophy]] explains the fundamental principle: every
dimension of every part traces back to a single named variable. Before any
modelling begins, every variable in → [[variable-table-values]] must be entered
into the FreeCAD spreadsheet and the model must update cleanly. An incorrect
variable produces incorrect geometry in every part that depends on it — and
the error is silent until you try to print and assemble.

The parametric approach also means that scaling the platform — changing the
wheelbase for a 5-inch or 8-inch build — is a variable edit, not a redesign.
→ [[variable-table-structure]] covers the variable organisation. → [[freecad-parametric-scaling]] explains the two-variable classes (frame-driven vs electronics-driven) and the scaling sequence — which variables change when the wheelbase changes and which must stay fixed regardless of airframe scale. The Cookbook's Scaling Philosophy section is the source material for that atom.

### FreeCAD orientation

→ [[freecad-ui-110]] covers the FreeCAD 1.1-specific interface elements: where
the workbench selector is, how to set CAD navigation mode, the macro path
for Flatpak Linux installs. → [[freecad-workbenches]] explains the workbenches
you will use: Spreadsheet (variable entry), Part Design (solid bodies), Part
(boolean operations), Assembly.

→ [[freecad-document-setup]] covers the one-time global setup: units (mm/kg/s,
3 decimal places), navigation style (CAD), zoom at cursor. Do this before
creating any geometry.

### Robust modelling discipline

Before touching any sketch or extrusion, internalize three habits from the Cookbook:

**Name every feature as you create it.** A Model Tree reading "Sketch002,
Pocket003, Mirror004" is a debugging nightmare. A Model Tree reading
"ArmProfile, PinchSlit, RodChannelLeft" is self-documenting.

**Fully constrain every sketch before closing it.** Underconstrained sketches
(shown in yellow/white) produce geometry that drifts when variables change.
The sketch must show "Fully constrained" in green before you close it.

**Use `=Variables.VariableName` for every dimension.** Never type a number
directly into a dimension dialog. Always reference the spreadsheet variable.
This is what makes the model parametric. A typed number is a hardcoded
constant that breaks when variables change.

---

## Reference

### Modelling sequence and atom map

| Part | Cookbook part | Key reference |
|---|---|---|
| Variable entry | Part 0 | [[variable-table-values]], [[freecad-document-setup]] |
| FreeCAD orientation | Parts 1–2 | [[freecad-ui-110]], [[freecad-workbenches]] |
| Arm shaft | Part 5 | [[arm-shaft]] (geometry decisions and rationale) |
| X body sandwich layers | Part 6 | [[sandwich-structure]], [[cf-rod-architecture]] |
| Platform | Part 7 | [[power-signal-separation]] (three-zone EMC geometry) |
| Backplane | Part 8 | [[lcm1-spec]] (Pi bay geometry) |
| Assembly & clearance check | Part 12 | [[freecad-assembly-workbench]] (joint types, rod clearance, backplane engagement) |
| GPS/camera bracket | Part 9 | [[flight-controller-hardware]] (mounting positions) |
| ASA bumpers | Part 10 | [[failure-hierarchy]] (energy absorption geometry) |
| Coupons | Part 11 | [[coupon-validation]] (what each coupon tests) |
| Assembly | Part 12 | [[sandwich-structure]] (layer order), [[cf-rod-architecture]] |
| Export for printing | Part 13 | [[stl-export-and-slicer-setup]] |
| Linux Flatpak notes | Part 14 | [[freecad-ui-110]] |

### Pre-modelling checklist

Before opening FreeCAD:

1. Variables file open: → [[variable-table-values]]
2. FreeCAD 1.1 installed (Flatpak or native)
3. Macro file (`LD_V343_Variables.FCMacro`) copied to macro path
4. Second screen ready for the Cookbook

### Variable entry gate

After running the macro and entering all variables:

- Open every Part Studio in the Model Tree
- Confirm no red cells in the Spreadsheet
- Confirm "Recomputed" or "Up to date" for all bodies — no yellow warning icons
- Spot-check three critical dimensions against the Variables file:
  - `ArmBoreOD` (motor bore): should match `MotorBoreOD + MotorBoreClearance`
  - `GX12ChimneyBore`: should show D-shape, not round circle
  - `TSlotWidth`: should match `ArmTabWidth + TSlotClearance`

If any check fails: fix the variable first, then remodel. Do not proceed with incorrect variables.

### Part-by-part decision gates

**Arm shaft (Part 5)**
Before padding: confirm the dovetail groove is on the BOTTOM face, not top.
The dovetail routes motor phase wires for EMC separation — wrong face means
wires will be on the wrong side after assembly.

**Platform (Part 7)**
Three features are EMC requirements. Before exporting Platform STL, confirm:
- LEFT wire channel present (signal zone): Y = −20mm
- RIGHT wire channel present (power zone): Y = +20mm
- MIPI centreline channel fully enclosed (camera cable route)

If any feature is missing: do not proceed to production print. → [[power-signal-separation]]
explains why these features cannot be retrofitted after printing.

**GX12 chimney bores (Part 7)**
Each GX12-7 connector bore must have a D-D profile (flat on one side), not a
round circle. The D-D prevents the connector from rotating and backing off the
retention nut. → [[gx12-connector-standard]] explains the rotation prevention
requirement. If the bore is round: check the `GX12ChimneyFlat` variable.

---

## Procedure

### Session setup for each modelling session

1. Open FreeCAD document — do not open from a backup; open the current saved version
2. Check for any yellow warning icons in the Model Tree — resolve before editing
3. `File → Save a Copy` before any major edit (creates a restore point)
4. Ctrl+S after completing each Part Studio successfully

### Recovering from a broken model

FreeCAD's topological naming problem (→ [[topological-naming-problem]]) can
cause features to detach from their reference geometry when upstream features
change. Symptoms: red cells in Model Tree, error dialogs on recompute.

Recovery sequence:
1. Ctrl+Z to undo the last change
2. If undo is not possible: open the backup copy from before the edit
3. Identify which feature broke (the first red item in the tree)
4. Re-apply the constraint or reference using the current geometry
5. Do not rename features mid-model — this compounds TNP errors

---

## Rationale

The FreeCAD Cookbook (V2.4.6) is 2,083 lines of step-by-step UI click maps
that are necessarily version-specific — the menu paths and dialog layouts
change between FreeCAD versions. This skeleton separates the stable conceptual
content (modelling sequence, decision gates, EMC geometry requirements) from
the version-specific click maps in the Cookbook. When FreeCAD 1.2 releases,
only the UI atom ([[freecad-ui-110]]) and the Cookbook need updating, not this
skeleton.

---

## Connections

requires: []
related:
  - [[sk-complete-build-guide]]
  - [[sk-hardware-reference]]
  - [[sk-master-specification]]
leads_to:
  - [[sk-complete-build-guide]]
