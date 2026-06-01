---
id: freecad-ui-110
title: "FreeCAD 1.1.x UI click map"
version: 1.0.0
date: 2026-04-11
author: jsa
status: released
scope: libdrone
topic:
  - freecad-ui
personas:
  - 1.builder
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

This article is a version-locked UI click map for FreeCAD 1.1.x. It documents
exact menu paths, dialog names, toolbar locations, and keyboard shortcuts for
every operation used in libdrone modelling. When FreeCAD changes its UI in a
future release, only this article needs updating — all geometry articles and
the FreeCAD skeleton document remain valid because they reference operations
by name, not by click path.

Use this article alongside the FreeCAD skeleton document. The skeleton tells
you what to do. This article tells you exactly where to click to do it.

**Verified against:** FreeCAD 1.1 stable (all platforms). macOS primary.

---

## Concept

<!-- not applicable -->

---

## Reference

### Screen layout — FreeCAD 1.1

    ┌─────────────────────────────────────────────────────────┐
    │  Menu bar: File  Edit  View  Tools  [Workbench menus]   │
    │  Toolbar row 1: [Workbench dropdown] [tool icons]       │
    ├──────────────┬──────────────────────────────────────────┤
    │              │                                          │
    │  Model Tree  │           3D Viewport                    │
    │  (left panel)│           (centre)                       │
    │              │                                          │
    │  Tasks panel │                                          │
    │  (appears    │                                          │
    │  below tree  │                                          │
    │  during ops) │                                          │
    ├──────────────┴──────────────────────────────────────────┤
    │  Status bar: coordinates / solver state / snap info     │
    └─────────────────────────────────────────────────────────┘

The **Workbench dropdown** is in the top toolbar, left side. In FreeCAD 1.1
it may show as a text label or an icon depending on your toolbar configuration.
If you cannot find it: View → Toolbars → Workbench → enable.

---

### A — First-time preferences

#### Set navigation style

    Edit → Preferences → Display → Navigation (tab)
      Navigation style: CAD
      Orbit style: Rounded Arcball (default in 1.1 — leave as is, or change to Trackball)
      ☑ Zoom at cursor
    Click OK

⚠ FreeCAD 1.1 introduced **Rounded Arcball** as the default orbit style.
If you opened Preferences and see Rounded Arcball already selected — this is
correct for 1.1. The Cookbook was written against an earlier default. CAD
navigation style still applies; only the orbit sub-style changed.

#### Set units

    Edit → Preferences → General → Units (tab)
      Unit system: Standard (mm/kg/s)
      Number of decimals: 3
    Click OK

---

### B — Macros

#### Find macro folder (do this first — path varies by OS and install method)

    Tools → Macros
      Read the "Macro path:" shown at the top of the dialog
      This is where to copy .FCMacro files
    Close

| OS / install | Typical path |
|---|---|
| macOS | `~/Library/Preferences/FreeCAD/Macro/` |
| Linux native | `~/.FreeCAD/Macro/` |
| Linux Flatpak 1.0 | `~/.var/app/org.freecad.FreeCAD/data/FreeCAD/Macro/` |
| Linux Flatpak 1.1 | `~/.var/app/org.freecad.FreeCAD/data/FreeCAD/1.1/Macro/` *(may vary — confirm via dialog)* |
| Windows | `%APPDATA%\FreeCAD\Macro\` |

#### Run a macro

    Tools → Macros
      Select macro name from list
    Click Execute

#### First-time Flatpak filesystem access (Linux only — run once in terminal)

    bash
    flatpak override org.freecad.FreeCAD --filesystem=home

---

### C — Documents

#### New document

    File → New    (Ctrl+N)

#### Save / Save As

    File → Save           Ctrl+S
    File → Save As        Ctrl+Shift+S
    File → Save a Copy    (use before major edits — creates a restore point)

⚠ FreeCAD has **no autosave**. Ctrl+S regularly. Save a Copy before any
session where you will make significant structural changes to the model.

---

### D — Workbench switching

    Workbench dropdown (top toolbar) → select workbench name

| Workbench | Used for |
|---|---|
| Spreadsheet | Creating and editing the Variables spreadsheet |
| Part Design | All solid modelling |
| Assembly | Fit verification and interference checking |

Switching workbench does not close or lose current work.

---

### E — Spreadsheet workbench

#### Create a spreadsheet

    Workbench → Spreadsheet
    Spreadsheet menu → Create Spreadsheet
    Model Tree: right-click "Spreadsheet" → Rename → type: Variables → Enter
    Double-click Variables to open the grid

#### Set an alias on a cell

    Right-click the cell (column B) → Properties
      Alias field: type the variable name exactly (case-sensitive)
    Click OK

#### Reference a variable in a sketch dimension

Type exactly: `=Variables.VariableName`
Example: `=Variables.ArmWidth`

The prefix `Variables.` is always required. No `#` prefix (that was the
Variables file notation — FreeCAD uses the spreadsheet name as prefix).

---

### F — Part Design workbench — bodies

#### Create a new Body

    Workbench → Part Design
    Part Design menu → Body → Create Body
      (alternative: Model menu → Body → Create Body)
    Model Tree: right-click the new Body → Rename → type name → Enter

The active Body is shown in **bold** in the Model Tree.
All features you create next belong to this Body.

#### Activate a different Body (if you have multiple)

    Model Tree: double-click the Body to activate it

---

### G — Part Design workbench — datum planes

#### Create a datum plane

    Part Design menu → Datum → Create a Datum Plane
      (alternative: Part Design toolbar → datum plane icon)

In the Attachment dialog:
      Select a reference (base plane, face, or another datum plane)
      Attachment mode: choose mode (Flat Face, XY/XZ/YZ Plane, etc.)
      Offset: type value in Z field to move the plane outward
      Click OK

**After creating:** rename immediately in the Model Tree.

    Model Tree: right-click datum plane → Rename → type descriptive name → Enter
    Example: DatumPlane_MotorHead, DatumPlane_RodTop

---

### H — Sketcher — creating sketches

#### Create a sketch on a base plane

    Model Tree: click the plane to select it (XY_Plane, XZ_Plane, or YZ_Plane)
    Sketch menu → New Sketch
      (alternative: Part Design toolbar → New Sketch icon)

Sketcher opens. Grid and axes appear in viewport.

#### Create a sketch on a datum plane

Model Tree: click the datum plane to select it
Sketch menu → New Sketch
  FreeCAD offers to use the selected plane → click OK

#### Create a sketch on a face (use sparingly — topological naming risk)

    Viewport: click the face to select it
    Sketch menu → New Sketch
      FreeCAD offers to use the selected face → click OK

Prefer datum planes over face references wherever possible.

#### Close a sketch

    Sketcher Tasks panel (left): click Close button
      (alternative: press Escape)
      (alternative: Sketch menu → Close Sketch)

---

### I — Sketcher — geometry tools

#### Rectangle (centred)

    Sketcher menu → Sketcher Geometries → Create Rectangle
      In the dropdown next to the tool: select Centered Rectangle
    Click once at origin (0,0) → move mouse → click to set approximate size

#### Circle

    Sketcher menu → Sketcher Geometries → Create Circle
    Click centre point → move mouse → click to set approximate radius

#### Sketch fillet (rounds 2D corners)

    Sketcher menu → Sketcher Geometries → Create Fillet
    Click a corner point (where two lines meet)
    Type radius value in the Tasks panel → Enter
    Repeat for each corner

*This is a 2D sketch fillet — different from Part Design 3D Fillet.*

#### Line

    Sketcher menu → Sketcher Geometries → Create Line
    Click start point → click end point → right-click to stop

---

### J — Sketcher — constraints

#### Dimension (generic — applies horizontal, vertical, or angular automatically)

    Sketcher menu → Sketcher Constraints → Constrain internal angle
      (or press D in Sketcher for dimension shortcut)
    Click the element to constrain
    Type value or formula in dialog → OK

#### Horizontal distance (X distance between two points)

    Sketcher menu → Sketcher Constraints → Constrain Horizontal Distance
    Click element or two points
    Type value or =Variables.Name → OK

#### Vertical distance (Y distance between two points)

    Sketcher menu → Sketcher Constraints → Constrain Vertical Distance
    Click element or two points
    Type value or =Variables.Name → OK

#### Coincident (two points or a point and origin share position)

    Select two points (Ctrl+click both)
    Sketcher menu → Sketcher Constraints → Constrain Coincident
      (alternative: press C)

#### Fully constrained check

A fully constrained sketch shows **all elements green**.
Status bar at bottom shows: `Fully constrained`

White or yellow elements are under-constrained — add more dimensions or
constraints until all turn green before closing the sketch.

---

### K — Part Design — features

#### Pad (push sketch into 3D)

    Model Tree: click the sketch to select it
    Part Design menu → Additive → Pad
      (alternative: Part Design toolbar → Pad icon)

    In Pad dialog:
      Type: Dimension
      Length: type value or =Variables.Name
      Symmetric: leave unchecked (pad in one direction only)
      Reversed: check if solid appears on wrong side
    Click OK

#### Pocket (remove material)

Model Tree: click the sketch to select it
    Part Design menu → Subtractive → Pocket

In Pocket dialog:
      Type: Through All  (for channels and holes that go full depth)
        — or —
      Type: Dimension → type depth value
      Reversed: check if cutting in wrong direction
    Click OK

#### Additive Loft (blend between two profiles)

    Part Design menu → Additive → Additive Loft

    In Loft dialog:
      Profile section → Add Section → click first sketch
      Add Section again → click second sketch
      Closed: unchecked
      Ruled: unchecked (smooth blend)
    Click OK

The two sketches must be on parallel planes at different positions.

#### Part Design Fillet (rounds 3D edges)

    Select edge(s) in viewport (Ctrl+click for multiple edges)
    Part Design menu → Fillet
      Size: type radius value
    Click OK

*This is the 3D edge fillet — different from Sketcher 2D fillet.*

#### Part Design Chamfer

    Select edge(s) in viewport
    Part Design menu → Chamfer
      Size: type chamfer size
    Click OK

---

### L — Fixing broken features

#### Yellow warning triangle in Model Tree

    Model Tree: click the warned feature
    Tasks panel: read what reference was lost
    Re-select the lost reference (face, edge, datum plane) in the viewport
    Click OK

This is the topological naming problem. It is normal. It is always fixable.
Do not delete and recreate — re-select the reference.

#### Sketch solver messages

    While in Sketcher:
    Sketch menu → Sketcher Preferences → General
      Solver messages: set to Full / Verbose

---

### M — Assembly workbench

#### Create an assembly

    Workbench → Assembly
    Assembly menu → Create Assembly
      (alternative: Assembly toolbar → Create Assembly icon)
    Model Tree: rename the assembly container

#### Insert a component (Body) into the assembly

    Assembly menu → Insert Component
      Navigate to the Body → select → Insert
      (alternative: drag a Body from the Model Tree into the Assembly container)

#### Create a fixed joint (anchors first part to world origin)

    Assembly menu → New Joint → Fixed Joint
    Select the Body to fix
    Click OK

#### Create a coincident joint (face-to-face flush)

    Assembly menu → New Joint → Coincident
    Select first face → select second face
    Click OK

#### Solve assembly (applies all joints)

    Assembly menu → Solve Assembly

#### Interference check

    Tools menu → Part → Check Geometry → Check for Intersections

#### Section cut view

    View menu → Standard Views → Section Cut
    Select plane: XY / XZ / YZ
    Adjust Z offset slider to desired height

---

### N — STL export

#### Export a single Body as STL

    Model Tree: right-click the Body → Export Mesh
      (alternative: select Body → File → Export)

    In export dialog:
      Format: STL Mesh
      Units: mm  ← verify — not inches
      Deviation: 0.01 mm
      
    Click Save

---

### O — Viewport navigation (CAD style)

| Action | Input |
|---|---|
| Rotate | Middle mouse button + drag |
| Pan | Middle mouse button + Ctrl + drag |
| Zoom | Scroll wheel |
| Fit all | V then F |
| Look at selected face | Select face → Numpad 0 |
| Front view | Numpad 1 |
| Top view | Numpad 7 |
| Toggle selected item visibility | Spacebar |

---

### P — Essential keyboard shortcuts

| Shortcut | Action |
|---|---|
| Ctrl+S | Save |
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |
| V, F | Fit all to view |
| Spacebar | Toggle selected item visibility |
| Escape | Exit current tool / close sketch |
| D | (Sketcher only) Dimension constraint |
| C | (Sketcher only) Coincident constraint |
| H | (Sketcher only) Horizontal constraint |
| V | (Sketcher only) Vertical constraint |
| P | (Sketcher only) Point on object constraint |

---

### Q — Common mistakes and fixes

| Mistake | Symptom | Fix |
|---|---|---|
| Sketch not closed | Pad/Pocket grayed out or fails | Open sketch → look for gaps at corners → close gap → re-close sketch |
| Under-constrained sketch | White/yellow elements in sketch | Add dimensions/constraints until all elements green |
| Topological naming failure | Yellow triangle in Model Tree | Click warned feature → re-select lost reference → OK |
| Sketch fillet vs Part Design fillet confusion | Wrong tool, unexpected result | 2D corners in sketch → Sketcher Fillet. 3D edges on finished solid → Part Design Fillet |
| Pad in wrong direction | Solid appears on wrong side | Check Reversed in Pad dialog |
| Variable reference not found | Dimension shows red / sketch broken | Verify prefix: `=Variables.Name` — check spelling and case |
| Wrong Body active | Feature added to wrong Body | Model Tree: double-click correct Body to activate it |
| STL exported in inches | Part 25.4× too large in slicer | Re-export: verify Units = mm in export dialog |
| Multiple Bodies, operations bleed across | Features appear in wrong Body | Always check which Body is bold (active) before creating features |

---

## Procedure

<!-- not applicable — this entire article is a procedural reference -->

---

## Rationale

### Why a separate UI article rather than UI steps in each geometry article

FreeCAD changes its menu structure, dialog names, and toolbar layouts between
releases. If UI clicks are embedded in geometry articles, every FreeCAD update
requires hunting through all affected articles to find and correct the stale
paths — typically while mid-build and under time pressure.

Isolating UI paths here means a FreeCAD release that moves a menu item
requires updating one article. All geometry articles and the skeleton document
remain unchanged. The versioning (freecad-ui-110, freecad-ui-120) makes it
clear which UI map applies and when a new one is needed.

### Why this is version-locked to 1.1.x

FreeCAD 1.0 shipped the Assembly workbench built-in. FreeCAD 1.1 changed
the default orbit style to Rounded Arcball and refined the Assembly joint
workflow. Future versions may move menus further. Each major UI change that
affects libdrone modelling steps warrants a new article. Minor patch releases
within 1.1.x are covered here unless they introduce breaking UI changes.

---

## Connections

requires: []
related:
  - [[freecad-document-setup]]
  - [[freecad-workbenches]]
  - [[parametric-modelling-philosophy]]
leads_to:
  - [[freecad-document-setup]]
  - [[variable-table-structure]]


[freecad-document-setup]: freecad-document-setup.md "FreeCAD document setup"
[freecad-workbenches]: freecad-workbenches.md "FreeCAD workbenches and modelling fundamentals"
[parametric-modelling-philosophy]: parametric-modelling-philosophy.md "Parametric modelling philosophy"
[variable-table-structure]: variable-table-structure.md "Variable table structure"
