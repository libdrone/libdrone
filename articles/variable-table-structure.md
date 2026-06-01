---
id: variable-table-structure
title: "Variable table structure"
version: 1.0.0
date: 2026-04-11
author: jsa
status: released
scope: libdrone
topic:
  - cad-parametric
personas:
  - 1.builder
  - 7.contributor
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The libdrone variable table is a FreeCAD Spreadsheet containing all parametric
dimensions for the V2.4.x frame. It is divided into 13 geometry sections
covering every aspect of frame geometry from wheelbase down to cable channel
dimensions. Every variable has a named alias — the alias is how sketches
reference it. The fastest way to populate the spreadsheet is the FCMacro,
which creates all variables in under a minute. Never type a dimension in a
sketch that already exists as a variable.

---

## Concept

### Aliases and references

FreeCAD Spreadsheet cells have two values: the cell address (B3, B4...) and
an optional alias (a human-readable name). When a sketch dimension references
`=Variables.ArmWidth`, FreeCAD looks up the alias `ArmWidth` in the spreadsheet
named `Variables` and substitutes the value. If `ArmWidth` changes, every
sketch dimension that references it updates automatically.

Aliases must be set manually on each cell — they are not inferred from the
adjacent label column. The macro handles this for all variables in the table.

### The 13 geometry sections

The variable table is organised into sections matching the drone's physical
architecture. Sections are ordered from large to small — global frame geometry
first, fine detail last. This mirrors the recommended modelling sequence.

---

## Reference

### Variable table sections

| #   | Section                                 | Key variables                                                                                                                                                        |
| --- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Frame geometry                          | `Wheelbase`, `ArmAngle`, `HubRadius`                                                                                                                                 |
| 2   | Arm geometry                            | `ArmWidth`, `ArmHeight`, `ArmShaftLength`, `PinchSlitWidth`                                                                                                          |
| 3   | Rod architecture                        | `RodDia`, `RodDiaChannel`, `RodDiaChannelCore`, `RodLength`, `RodHeightOuter`, `RodHeightInner`                                                                      |
| 4   | Sandwich body geometry                  | `XBodyLength`, `XBodyWidth`, `LayerHeight`, `SandwichBoltPattern`                                                                                                    |
| 5   | Tab geometry                            | `TabWidth`, `TabHeight`, `TabLength`, `TabLockWidth`, `TabClearance`                                                                                                 |
| 6   | Motor mount geometry                    | `MotorBoltPattern`, `MotorBoreDia`, `OringBossDia`, `OringBossHeight`, `CounterboreDia`, `CounterboreDepth`                                                          |
| 7   | Cable management geometry               | `MR30ChannelWidth`, `MR30ChannelDepth`, `DovetailWidth`, `CableGrooveDepth`                                                                                          |
| 8   | Battery spoiler                         | *(removed V2.4.6 — section retained as deprecated placeholder)*                                                                                                      |
| 9   | GX12-7 dual payload connector geometry  | `GX12BossDia`, `GX12ChimneyOD`, `GX12ChimneyDepth`, `GX12ChimneyBoreFlatFlat`, `GX12BoreFullDia`, `GX12WireSlotW`, `GX12WireSlotH`, `GX12PositionX`, `GX12PositionY` |
| 9b  | Battery rail geometry                   | `BattRailInnerWidth`, `BattRailHeight`, `BattLength`, `BattWidth`, `BattHeight`, `EndstopWallThick`                                                                  |
| 10  | Mast interface geometry                 | `MastBaseDim`, `MastBossDia`, `MastBossHeight`, `MastBossSpacing`                                                                                                    |
| 11  | GPS/camera bracket geometry             | `BracketHeight`, `BracketWidth`, `GPSPocketDia`, `CameraTiltRange`                                                                                                   |
| 12  | Assembly offsets and clearances         | `StackPattern`, `PropClearanceMin`, `StackHeight`                                                                                                                    |
| 13  | Platform geometry                       | `PlatformLength`, `PlatformWidthNarrow`, `PlatformWidthElec`, `MIPIChannelWidth`, `FanSlotDim`, `AttachPostDia`, `AttachPostSpacingY`                                |
| 14  | Backplane geometry                      | `BackplaneLength`, `BackplaneWidth`, `LatticeBeamWidth`, `GX12BackplanePositionY`                                                                                    |
| 15  | Pi Bay and companion interface geometry | `PiBayLength`, `PiBayWidth`, `PiBayHeight`                                                                                                                           |

### Frame-driven vs electronics-driven variables

**Frame-driven** — change when wheelbase changes:
`Wheelbase`, `ArmShaftLength`, `RodLength`, `PlatformAttachPostY`

**Electronics-driven** — stay constant across scales:
`PlatformLength`, `StackPattern`, `GX12PositionY`, `MIPIChannelWidth`,
`FanSlotDim`, `BatteryDims`

**Payload-interface** — scale-independent by design:
`GX12BossDia`, `GX12ChimneyOD`, `GX12ChimneyBoreFlatFlat`, `MastBossSpacing`

### The FCMacro

`LD_V343_Variables.FCMacro` creates the complete Variables spreadsheet with
all aliases set in one execution. This is the recommended method — manual
cell-by-cell entry is error-prone and takes 30–45 minutes.

Macro file location:
- macOS: `~/Library/Preferences/FreeCAD/Macro/`
- Linux Flatpak: confirm via Tools → Macros (path shown in dialog)
- Windows: `%APPDATA%\FreeCAD\Macro\`

After execution, verify the spreadsheet appears in the Model Tree named
`Variables`. Spot-check three aliases: open a cell in column B, check that
Properties → Alias shows the expected name.

### Reference in sketches

All variable references use the prefix `Variables.`:
    =Variables.ArmWidth        → resolves to current ArmWidth value
    =Variables.RodDiaChannel   → resolves to current RodDiaChannel value

Never type the numeric value directly. If the alias prefix is missing,
FreeCAD cannot find the variable and the sketch dimension will be unsatisfied.

---

## Procedure

### Manual variable entry (if not using macro)

1. Switch to Spreadsheet workbench.
2. Create Spreadsheet → rename to `Variables`.
3. For each variable: type name in column A, value in column B.
4. Right-click column B cell → Properties → Alias → type variable name → OK.
5. Save (Ctrl+S) after every 10 entries.
6. After all entries: verify count matches the reference table above.

---

## Rationale

### Why section 8 is retained as deprecated

Removing the battery spoiler section entirely from the variable table would
shift all subsequent section numbers, breaking references in existing macros,
documentation, and contributor notes that reference section numbers. The
deprecated placeholder costs nothing and preserves continuity.

### Why two separate platform width variables

`PlatformWidthNarrow` (40 mm) covers the arm root zones where prop clearance
is tightest. `PlatformWidthElec` (50 mm) covers the electronics zone where
the wider width accommodates the GX12 chimneys and fan slot. A single width
variable would either constrain the electronics zone unnecessarily or violate
prop clearance at the arm roots. At new scales, both values must be recalculated
independently — they do not scale together.

---

## Connections

requires:
  - [[parametric-modelling-philosophy]]
  - [[freecad-document-setup]]
related:
  - [[scaling-libdrone]]
  - [[freecad-workbenches]]
leads_to:
  - [[freecad-document-setup]]
  - [[scaling-libdrone]]


[parametric-modelling-philosophy]: parametric-modelling-philosophy.md "Parametric modelling philosophy"
[freecad-document-setup]: freecad-document-setup.md "FreeCAD document setup"
[scaling-libdrone]: scaling-libdrone.md "Scaling libdrone to a new frame size"
[freecad-workbenches]: freecad-workbenches.md "FreeCAD workbenches and modelling fundamentals"
