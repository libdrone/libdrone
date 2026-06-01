---
id: stl-export-and-slicer-setup
title: "STL export and slicer setup"
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
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

After completing all part bodies in FreeCAD, each body is exported as an STL
file and imported into PrusaSlicer. Correct part orientation in the slicer is
as important as the print profile settings — the arm shaft printed in the wrong
orientation produces a structurally deficient part regardless of all other
settings. This article covers export settings, the complete export list, and
correct orientation for each part.

---

## Concept

### Why orientation is a separate decision from modelling orientation

FreeCAD models parts in a design coordinate system — the arm shaft might be
modelled horizontally for convenience. PrusaSlicer prints in a physical
coordinate system — the build plate is Z=0 and gravity is down. The correct
print orientation for the arm shaft (vertical, motor head up) is a printing
decision, not a modelling decision. The two orientations are often different.
Every part must be explicitly oriented in the slicer before slicing.

---

## Reference

### FreeCAD STL export settings

| Setting | Value |
|---|---|
| Format | STL |
| Units | mm (verify — not inches) |
| Quality / Deviation | 0.01 mm |

### Export list

| Filename | Body | Qty to print | Notes |
|---|---|---|---|
| `Arm_Shaft.stl` | Arm | 4 + 2 spares | Same file for all copies |
| `Arm_Tab.stl` | Arm Tab | 8 | Same file for all copies |
| `Arm_Cover_Active.stl` | Arm Cover Active | 4 | |
| `Arm_Cover_Passive.stl` | Arm Cover Passive | 4 | PETG-CF — respirator |
| `X_Body_PCCF_Base.stl` | X Body PCCF Base | 3 | Layers 2, 3, 4 — identical |
| `X_Body_PETG_Bottom.stl` | X Body PETG Bottom | 1 | Layer 1 — impact face |
| `X_Body_PETG_Top.stl` | X Body PETG Top | 1 | Layer 5 — features surface |
| `Platform.stl` | Platform | 1 | Longest single print |
| `Backplane.stl` | Backplane | 1 | Lattice — no supports |
| `GPS_Camera_Bracket.stl` | GPS Camera Bracket | 1 | |
| `Camera_Tilt_Plate.stl` | Camera Tilt Plate | 1 | |
| `ASA_Bumper.stl` | ASA Bumper | 4 + 4 spares | |
| `Sensor_Mast.stl` | Sensor Mast | 1 (if fitting payload) | |

### Correct orientation per part in PrusaSlicer

| Part | Print orientation | Reason |
|---|---|---|
| Arm shaft | **Vertical — motor head up or down** | Layers perpendicular to bending load |
| Arm tab | Flat / horizontal | Large flat base, no strength orientation requirement |
| Arm cover active | Flat | Large flat part |
| Arm cover passive | Flat | Large flat part |
| X body PCCF layers | Flat on build plate | Maximum dimensional accuracy |
| X body PETG bottom | Flat on build plate | |
| X body PETG top | Flat, face-up | GX12 chimneys point downward into support |
| Platform | Flat, face-up | All features accessible; chimneys supported downward |
| Backplane | Flat, face-up | Lattice prints cleanly flat — no supports required |
| GPS camera bracket | Flat | |
| Camera tilt plate | Flat | |
| ASA bumpers | Flat | |

### PrusaSlicer import procedure

1. Open PrusaSlicer.
2. Select printer profile: PRUSA COREONE+.
3. Select filament profile matching the part material.
4. Drag and drop the STL file onto the build plate.
5. Right-click part on build plate → Orient → Place on Face → select correct face.
6. Verify orientation matches the table above.
7. Apply print profile settings from print-profiles article.
8. Slice and verify layer preview — check supports, infill, perimeter count.
9. Export G-code.

### Linux Flatpak specific notes

- Macro path: `~/.var/app/org.freecad.FreeCAD/data/FreeCAD/Macro/`
- Sandbox file access (run once): `flatpak override org.freecad.FreeCAD --filesystem=home`
- Sketcher visibility on dark themes: Preferences → Display → Colors → Sketcher → adjust

---

## Procedure

### Exporting a body from FreeCAD

1. In the Model Tree, click the Body you want to export.
2. Right-click → Export Mesh.
   (Alternative: File → Export with body selected.)
3. In the dialog:
   - Format: STL Mesh
   - Units: mm (verify this is not showing inches)
   - Deviation: 0.01 mm
4. Save to your `/stl/` output folder.
5. Repeat for every body.
6. Verify file sizes are non-zero and roughly proportional to part complexity.

---

## Rationale

### Why 0.01 mm deviation for STL export

STL format approximates curved surfaces with triangles. The deviation setting
controls how closely the triangulation follows the true surface. At 0.01 mm
deviation, the largest gap between a flat triangle and the true curved surface
is 0.01 mm — well below the resolution of any FDM printer. Coarser settings
(0.1 mm default) produce visible faceting on the arm shaft motor head curves
and O-ring counterbores.

### Why verify units at export

FreeCAD models in mm. Some FreeCAD installations default STL export to inches.
An arm shaft exported in inches and imported into PrusaSlicer (which assumes mm)
will appear 25.4× too large. Always verify the units field in the export dialog.

---

## Connections

requires:
  - [[freecad-workbenches]]
  - [[print-profiles]]
related:
  - [[coupon-validation]]
  - [[production-run-order]]
leads_to:
  - [[production-run-order]]
  - [[airframe-integration]]
