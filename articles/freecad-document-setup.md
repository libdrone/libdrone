---
id: freecad-document-setup
title: "FreeCAD document setup"
version: 1.0.0
date: 2026-04-11
author: jsa
status: released
scope: libdrone
topic:
  - cad-parametric
personas:
  - 1.builder
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Before modelling any part, a correctly configured FreeCAD document must exist
with the Variables spreadsheet populated and the global preferences set.
This is done once per build. Skipping or rushing this step creates hard-to-debug
problems later — missing aliases cause sketch dimensions to fail silently,
and wrong units or navigation settings cost hours of confusion. The entire
setup takes under ten minutes using the FCMacro.

---

## Concept

### Why setup before modelling

FreeCAD preferences (navigation style, units, decimal places) affect how
the model behaves during editing. Wrong settings do not break the model but
they make it significantly harder to use — CAD navigation feels wrong,
dimensions show in incorrect units, and the sketcher solver gives misleading
messages.

The Variables spreadsheet must exist before any sketch references a variable.
A sketch that references `=Variables.ArmWidth` on a document that has no
Variables spreadsheet generates a broken reference that is annoying to fix
retroactively. Create the spreadsheet first, model second.

---

## Reference

### Required FreeCAD version

FreeCAD 1.1 stable — download from https://www.freecad.org/downloads.php

FreeCAD 1.0 is also compatible but 1.1 has improved topological naming
resistance. Do not use nightly/development builds — they may introduce
instability mid-build.

### Preference settings — set once after install

| Preference location | Setting | Value |
|---|---|---|
| Edit → Preferences → Display → Navigation | Navigation style | CAD |
| Edit → Preferences → Display → Navigation | Zoom at cursor | Checked |
| Edit → Preferences → General → Units | Unit system | Standard (mm/kg/s) |
| Edit → Preferences → General → Units | Number of decimals | 3 |

### Document structure

One `.FCStd` file contains the entire drone model:

    Variables          ← Spreadsheet (create first)
    Body: Arm
    Body: Arm Tab
    Body: Arm Cover Active
    Body: Arm Cover Passive
    Body: X Body PCCF Base
    Body: X Body PETG Bottom
    Body: X Body PETG Top
    Body: Platform
    Body: Backplane
    Body: GPS Camera Bracket
    Body: Camera Tilt Plate
    Body: ASA Bumper
    Assembly

### Macro locations by OS

| OS | Macro folder |
|---|---|
| macOS | `~/Library/Preferences/FreeCAD/Macro/` |
| Linux Flatpak | Confirm via Tools → Macros → read path shown in dialog |
| Linux native | `~/.FreeCAD/Macro/` |
| Windows | `%APPDATA%\FreeCAD\Macro\` |

⚠ FreeCAD 1.1 Flatpak may use a versioned subfolder:
`~/.var/app/org.freecad.FreeCAD/data/FreeCAD/1.1/Macro/`
Always confirm the actual path via the dialog before copying macros.

---

## Procedure

### First-time FreeCAD setup

1. Download and install FreeCAD 1.x from https://www.freecad.org/downloads.php
2. Launch FreeCAD.
3. Linux Flatpak only: run once in terminal:
   `flatpak override org.freecad.FreeCAD --filesystem=home`
4. Set navigation style: Edit → Preferences → Display → Navigation →
   Navigation style: **CAD** → Zoom at cursor: **checked** → OK.
5. Set units: Edit → Preferences → General → Units →
   Unit system: **Standard (mm/kg/s)** → Decimals: **3** → OK.
6. Close and reopen FreeCAD to confirm preferences applied.

### Creating the document

1. File → New (Ctrl+N).
2. File → Save As → navigate to your libdrone project folder.
3. Name: `LD_V34.FCStd` (or your preferred version identifier).
4. Click Save.
5. Ctrl+S immediately — FreeCAD does not autosave.

### Installing and running the Variables macro

1. Locate your FreeCAD Macro folder (see table above).
2. Copy `LD_V343_Variables.FCMacro` into that folder.
3. In FreeCAD: Tools → Macros.
4. Select `LD_V343_Variables` from the list.
5. Click Execute.
6. The `Variables` spreadsheet appears in the Model Tree.
7. Double-click Variables to open it — verify rows and aliases are present.
8. Spot-check: click cell B1 → Properties → confirm Alias shows `Wheelbase`.
9. Ctrl+S to save.

### Verifying the spreadsheet

The spreadsheet should contain:
- Column A: variable names (human-readable labels)
- Column B: values (with aliases set — shown in Properties panel)
- No empty alias cells in column B

If any alias is missing: right-click the cell → Properties → Alias → type
the variable name exactly → OK. Variable names are case-sensitive.

### Save discipline

FreeCAD has no autosave. Establish this habit immediately:
- Ctrl+S every 10–15 minutes during active modelling
- File → Save a Copy before any major edit session
  Name the copy with a version suffix: `LD_V34_pre-xbody.FCStd`
- This is your restore point if topology breaks

---

## Rationale

### Why CAD navigation style specifically

FreeCAD supports multiple navigation styles (Blender, Inventor, OpenCascade,
CAD). The CAD style matches the mouse button conventions used in most
professional CAD software and in the FreeCAD Cookbook instructions. Using a
different style means every pan/zoom/rotate instruction in the Cookbook
maps to different mouse buttons, creating friction during the build.

### Why 3 decimal places

libdrone dimensions range from 2.1 mm (rod channel interference fit) to
333 mm (rod length). Three decimal places gives 0.001 mm resolution — more
than sufficient for 3D printing, which has a practical resolution of ~0.05 mm.
Two decimal places is adequate but can cause rounding artefacts when variables
are used in chains of calculations. Four decimal places adds no practical
precision and clutters the dimension display.

---

## Connections

requires:
  - [[parametric-modelling-philosophy]]
related:
  - [[variable-table-structure]]
  - [[freecad-workbenches]]
  - [[topological-naming-problem]]
leads_to:
  - [[variable-table-structure]]
  - [[freecad-workbenches]]


[parametric-modelling-philosophy]: parametric-modelling-philosophy.md "Parametric modelling philosophy"
[variable-table-structure]: variable-table-structure.md "Variable table structure"
[freecad-workbenches]: freecad-workbenches.md "FreeCAD workbenches and modelling fundamentals"
[topological-naming-problem]: topological-naming-problem.md "Topological naming problem"
