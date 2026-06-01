---
id: prep-and-parametrics
title: "Prep and parametrics"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - manufacturing
personas:
  - 1.builder
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Prep and parametrics is Phase 0 of the build — the configuration work that
must complete before any printing begins. It has two parts: assembling the
documentation set (offline copies of all reference documents), and entering
all variables into FreeCAD to generate a valid parametric model. The variable
entry step is the single most important accuracy gate in the entire build.
Every dimension in every printed part traces back to a variable. One wrong
variable propagates silently into dozens of parts and will not be caught until
structural validation — by which point hours of printing are wasted.

---

## Concept

### Why parametrics before printing

libdrone's frame is fully parametric — all geometry derives from variables in
a single spreadsheet. The spreadsheet is not a convenience; it is the
single source of truth. Printing any part before the variable table is verified
means printing from unknown geometry. The arm bore diameter, the T-slot width,
the rod channel diameter, the GX12 chimney bore — every dimension with a
tolerance interaction — is set here.

The FreeCAD variable entry session is boring, methodical work that takes
30–60 minutes. It prevents 4–8 hours of wasted prints. Do not skip or rush it.

### Offline documentation set

In a build environment that may lack internet access (workshop, field facility),
all reference documents must be locally available. Required documents:

- Master Specification (structural and geometry reference)
- Variables file (the canonical source for all parametric values)
- FreeCAD Cookbook (step-by-step CAD instructions)
- WBS (work breakdown — the build sequence)
- Software doc (firmware configuration)
- Shopping list
- Regulatory doc

Print and laminate critical single-page references (wiring diagram, motor
direction layout, UART assignment table) before the build begins.

---

## Reference

### Variable entry sequence

Enter variables in this order to avoid dependency errors in FreeCAD:

1. Frame geometry variables (arm length, wheelbase, rod diameter)
2. Sandwich geometry (layer heights, bolt pattern)
3. Motor mount variables (bore diameter, counterbore, screw positions)
4. Platform geometry (zone positions, MIPI channel, GX12 chimney)
5. GX12 connector variables (chimney bore, boss OD, chimney depth)
6. Hardware variables (standoff height, screw sizes)

All values come from `LD_-_Variables_v246.md` only. Do not use values from
memory, from older build notes, or from other documents. → See
[[variable-table-values]] for the complete reference.

### FreeCAD document setup

→ See [[freecad-document-setup]] for the complete procedure.

Key checkpoints:
- Spreadsheet populates with no red cells after macro runs
- All Part Studios show green (no unsatisfied constraints)
- Arm bore diameter matches `ArmShaftOD + ArmShaftClearance` exactly
- GX12 chimney bore shows D-D profile, not round hole

---

## Procedure

### Phase 0 sequence

1. **Assemble documentation set.** Download or confirm local copies of all
   reference documents. Open `LD_-_Variables_v246.md` — this is the source for
   all variable values.
2. **Open FreeCAD.** Run `LD_V245_Variables.FCMacro` to create the variable
   spreadsheet. Verify all sections populate.
3. **Enter all variables.** Work through each section of the Variables file in
   order. For each variable: read the value from the Variables file, enter it
   into the FreeCAD spreadsheet cell exactly as listed. Do not deviate.
4. **Verify model updates.** After all variables are entered, trigger a
   model rebuild. All Part Studios must show no red cells and no unsatisfied
   constraints.
5. **Print and laminate** the one-page critical references:
   - Motor direction and numbering diagram
   - UART assignment table
   - Wiring EMC zone diagram (power channel left / signal channel right)
6. **Procurement check.** Confirm AliExpress order is placed (or already in
   transit). If not placed — place it now before proceeding.

---

## Rationale

### Why documentation assembly is a build step

Documentation that lives only in the cloud is unavailable when the network is
down, when the repository is unreachable, or when working in a facility without
internet. Physical laminated references survive workshop conditions (dust, oil,
solvents) where a laptop screen or tablet is impractical. The 20 minutes spent
assembling and printing the documentation set will save at minimum one trip
back to a computer mid-build.

---

## Connections

requires:
  - [[variable-table-values]]
  - [[freecad-document-setup]]
related:
  - [[coupon-validation]]
  - [[parametric-modelling-philosophy]]
leads_to:
  - [[coupon-validation]]
  - [[print-profiles]]
