---
id: variable-table-values
title: "Variable table values"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - cad-parametric
personas:
  - 1.builder
  - 4.workshop
  - 7.contributor
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

This article is the authoritative value reference for the libdrone V2.4.6
parametric variable table. It lists every variable across all 15 sections,
with its alias name, current value, and purpose. Use it to verify a populated
spreadsheet, to manually enter a missing variable, or to understand what a
variable controls before changing it. For how the variable system works —
alias syntax, FreeCAD Spreadsheet mechanics, and the FCMacro — see
[[variable-table-structure]].

---

## Concept

### Derived values and chain dependencies

Some variables are derived from others. FreeCAD computes them automatically
when the driving variables are set. Key chains to understand:

**Sandwich height chain:**
    SandwichHeight = PETGBotLayerThick + 3 × PCCFLayerThick + PETGTopLayerThick
                  = 3 + 9 + 4 = 16 mm
    ArmHeight = SandwichHeight = 16 mm   (arm shaft must equal sandwich height)
    TabThick  = SandwichHeight = 16 mm   (tab fills full slot height)

**Rod channel chain:**
    RodDia            = 2.0 mm   (physical rod)
    RodDiaChannel     = 2.2 mm   (clearance — PCCF and PETG non-core zones)
    RodDiaChannelCore = 2.1 mm   (interference fit — PETG bottom layer core zone only)

The 0.1 mm interference (RodDiaChannel − RodDiaChannelCore) is intentional.
PETG deforms elastically and grips the rod. PCCF would crack — PCCF layers
always use the clearance value.

**GX12 D-D bore chain:**
    GX12BodyFlatFlat       = 10.60 mm  (physically measured on connector body)
    GX12ChimneyBoreFlatFlat = 10.80 mm  (+ 0.20 mm print clearance)
    GX12BodyOD             = 11.67 mm  (physically measured)
    GX12ChimneyBoreOD      = 11.87 mm  (+ 0.20 mm print clearance)

The bore is a D-D profile (two arcs + two parallel flats), not a round hole.
If only a round bore is used, the connector spins when payloads are plugged in.

### What changes when wheelbase changes

If `Wheelbase` is edited to adapt the frame to a different prop size,
these variables need independent recalculation — they do not scale
automatically from Wheelbase:

- `ArmShaftLength` — verify in FreeCAD Assembly (rod clearance at arm tip)
- `RodLength` — verify in FreeCAD Assembly (rod must not protrude past arm tip)
- `PlatformLength` — electronics layout is fixed; does not scale with frame
- `GX12_PositionY` — connector position is fixed relative to electronics
- `BattZoneFront` / `BattZoneRear` — battery dimensions are fixed

Wheelbase directly drives: arm angle geometry, prop clearance. Everything else
must be re-verified independently. → See [[scaling-libdrone]].

---

## Reference

### [1] Frame geometry

| Alias | Value | Description |
|---|---|---|
| `Wheelbase` | 330.0 mm | Diagonal motor-to-motor distance (True-X) |
| `StackPattern` | 30.5 mm | FC/ESC square mounting pattern (M3) |
| `WallThick` | 2.0 mm | Nominal shell wall thickness |

### [2] Arm geometry

| Alias | Value | Description |
|---|---|---|
| `ArmWidth` | 26.0 mm | Arm shaft width |
| `ArmHeight` | 16.0 mm | Arm shaft height — must equal SandwichHeight |
| `MotorHeadWidth` | 35.0 mm | Motor mount head width |
| `MotorHeadHeight` | 18.0 mm | Motor mount head height |
| `MotorHeadTaper` | 20.0 mm | Loft transition length motor head → shaft |
| `PinchSlit` | 0.5 mm | Slit width for rod pre-tension clamp |
| `CoverScrewDia` | 2.0 mm | M2 screw clearance for arm covers |
| `ArmShaftLength` | 125.0 mm | Shaft length from tab junction to motor head |

⚠ Verify `ArmShaftLength` in FreeCAD Assembly after any wheelbase change —
CF rods must not protrude past the arm shaft outer face.

### [3] Rod architecture

| Alias | Value | Description |
|---|---|---|
| `RodDia` | 2.0 mm | Carbon rod outer diameter (physical) |
| `RodDiaChannel` | 2.2 mm | Printed rod channel (clearance — PCCF layers + PETG non-core) |
| `RodDiaChannelCore` | 2.1 mm | Rod channel in PETG core zone (interference fit — PETG bottom only) |
| `RodOffsetOuter` | 5.0 mm | Rod channel centre Z offset — outer pair |
| `RodOffsetInner` | 2.0 mm | Rod channel centre Z offset — inner pair |

**Rod Z positions by arm orientation:**
- FL/RL arms (normal): +5.0 mm and +2.0 mm
- FR/RR arms (inverted): −5.0 mm and −2.0 mm

Rod cut length: 333.0 mm (derived from 258 mm at 255 mm wheelbase — confirm
in FreeCAD Assembly at current wheelbase before cutting rods).

### [4] Sandwich body geometry

| Alias | Value | Description |
|---|---|---|
| `SandwichHeight` | 16.0 mm | Total sandwich height (derived — see chain above) |
| `PCCFLayerThick` | 3.0 mm | Thickness of each PCCF structural layer (×3) |
| `PETGBotLayerThick` | 3.0 mm | PETG bottom layer — impact face |
| `PETGTopLayerThick` | 4.0 mm | PETG top layer — structural surface |
| `MIPIChannelDepth` | 1.5 mm | MIPI cable channel depth (Platform — not X body) |
| `MIPIChannelWidth` | 16.0 mm | MIPI cable channel width |
| `RodDiaChannelCore` | 2.1 mm | Rod channel (interference fit, PETG bottom core zone only) |
| `XBodyArmWidth` | 40.0 mm | Width of X body arm zone at tab junction |
| `XBodyCoreSize` | 60.0 mm | Central core square side length |
| `XBodyArmLength` | 35.0 mm | Length of X body arm extension from core edge |
| `SandwichBoltDia` | 3.3 mm | M3 clearance through-hole — all sandwich layers |
| `SandwichBoltCornerOffset` | 18.0 mm | Corner bolt offset from body centre on X and Y axes |
| `SandwichBoltNoseTailY` | 22.0 mm | Y offset for nose and tail perimeter bolts |

**Derived — sandwich bolt pattern:**
- 6 bolts total
- 4 corner bolts at (±18, ±18 mm)
- 1 nose bolt at (0, +22 mm)
- 1 tail bolt at (0, −22 mm)

**Layer stack (bottom → top):** PETG 3 mm / PCCF 3 mm / PCCF 3 mm / PCCF 3 mm / PETG 4 mm

V2.4.6 note: `MIPIChannelDepth` and `MIPIChannelWidth` describe Platform geometry,
not X body top layer. The X body PETG top layer is a clean structural surface.

### [5] Tab geometry

| Alias | Value | Description |
|---|---|---|
| `TabLength` | 20.0 mm | Tab engagement depth inside sandwich |
| `TabWidth` | 22.0 mm | Tab width |
| `TabThick` | 16.0 mm | Tab thickness = SandwichHeight (fills full slot height) |
| `TabLockWidth` | 8.0 mm | T-lock extension width |
| `TabLockDepth` | 4.0 mm | T-lock extension depth into sandwich |
| `TabScrewDia` | 2.0 mm | M2 screw clearance — shaft-to-tab connection |
| `TabScrewSpacing` | 10.0 mm | Centre-to-centre M2 screw spacing |

T-slot clearance: T-slot pocket width = `TabWidth + 0.2 mm` per side (clearance fit).
Verify against Coupon 8 print before committing to X body PCCF layers.
Adjust `TabClearance` variable if coupon shows tight or sloppy fit.

### [6] Motor mount geometry

| Alias | Value | Description |
|---|---|---|
| `MotorBoreDia` | 6.5 mm | Through-bore for M3 screws + silicone sleeves |
| `ORingCBoreDia` | 7.0 mm | O-ring counterbore diameter |
| `ORingCBoreDepth` | 1.5 mm | O-ring counterbore depth |
| `ORingRimHeight` | 0.5 mm | Lateral rim height preventing O-ring migration |
| `ORingRimWall` | 0.5 mm | Rim wall thickness |

Derived: `ORingRimOD = ORingCBoreDia + 2 × ORingRimWall = 8.0 mm`

### [7] Cable management geometry

V2.4.6 note: All cable management features have moved from the X body PETG top
layer into the Platform. These variables now describe Platform geometry.

| Alias | Value | Description |
|---|---|---|
| `CablePortDia` | 5.5 mm | Strain relief port in motor head side wall |
| `CableGrooveWidth` | 4.5 mm | Arm shaft dovetail cable groove width at surface |
| `CableGrooveDepth` | 2.0 mm | Arm shaft dovetail cable groove depth |
| `CableGrooveAngle` | 8° | Arm shaft dovetail wall angle |
| `WireChannelWidth` | 4.0 mm | Platform wire routing channel width |
| `WireChannelDepth` | 1.0 mm | Platform wire routing channel depth |
| `WireChannelOffset` | 20.0 mm | Channel centreline offset from body centreline |
| `BattLeadNotchWidth` | 8.0 mm | Battery lead relief notch width |
| `BattLeadNotchDepth` | 4.0 mm | Battery lead relief notch depth |
| `FanWidth` | 30.0 mm | Cooling fan body width (Gdstime 3010) |
| `FanDepth` | 10.0 mm | Cooling fan body depth |
| `FanSlotWidth` | 30.0 mm | Fan slot width in Platform rear shroud |
| `FanSlotHeight` | 35.0 mm | Fan slot height |
| `FanSlotPosY` | −138.0 mm | Fan front face position from body centre |
| `FanSlotWall` | 1.5 mm | Minimum wall either side of fan slot |

### [8] Battery spoiler — DEPRECATED (V2.4.6)

Section 8 is retired. All `#Spoiler` variables are removed. Do not reference
in CAD. The always-on fan replaces spoiler function. Section retained as
deprecated placeholder to preserve section numbering continuity.

### [9] GX12-7 dual payload connector geometry

Polarity: drone side = GX12-7 male panel mount (pins face upward toward payload).
Payload side = GX12-7 female cable mount.

**Shared geometry (both connectors identical):**

| Alias | Value | Description |
|---|---|---|
| `GX12NominalDia` | 12.0 mm | GX12 nominal designation — not the actual body OD |
| `GX12BodyFlatFlat` | 10.60 mm | Male body flat-to-flat (physically measured) |
| `GX12BodyOD` | 11.67 mm | Male body full OD at threaded collar (physically measured) |
| `GX12ChimneyBoreFlatFlat` | 10.80 mm | Chimney bore flat-to-flat = GX12BodyFlatFlat + 0.2 mm |
| `GX12ChimneyBoreOD` | 11.87 mm | Chimney bore full diameter = GX12BodyOD + 0.2 mm |
| `GX12BossDia` | 14.0 mm | Raised boss outer diameter on Platform |
| `GX12BossHeight` | 3.0 mm | Boss height above Platform surface |
| `GX12BodyLengthBelow` | 25.0 mm | Male body length below mounting surface |
| `GX12CapHeight` | 10.0 mm | Dust cap height above Platform surface |
| `GX12ChimneyOD` | 18.0 mm | Chimney outer diameter |
| `GX12ChimneyHeight` | 25.0 mm | Chimney height below Platform |
| `GX12ChimneyWall` | 3.0 mm | Chimney wall thickness — PETG |
| `GX12WireExitWidth` | 6.0 mm | Wire exit slot width at chimney base |
| `GX12WireExitHeight` | 4.0 mm | Wire exit slot height at chimney base |

**Chimney bore profile — D-D shape (critical for anti-rotation):**

The bore is NOT a round hole. In FreeCAD Sketcher:
1. Draw circle diameter `GX12ChimneyBoreOD` (11.87 mm)
2. Add two parallel lines at ±(`GX12ChimneyBoreFlatFlat` / 2) = ±5.40 mm from centre
3. Trim circle arcs outside those lines

Result: D-D profile that prevents connector rotation. Print Coupon 10 and
verify fit before printing the full Platform. Adjust `GX12ChimneyBoreFlatFlat`
by ±0.1 mm if coupon is tight or sloppy.

**Position variables:**

| Alias | Value | Description |
|---|---|---|
| `GX12A_PositionX` | −25.0 mm | Connector A (left, signal channel side) |
| `GX12B_PositionX` | +25.0 mm | Connector B (right, power channel side) |
| `GX12_PositionY` | −66.0 mm | Both connectors — mid-electronics zone |
| `GX12_CentreToCentre` | 50.0 mm | A to B centre-to-centre |
| `GX12_OuterGap` | 32.0 mm | Clear gap between chimney outer walls |

**Vibration retention:** single nut insufficient. Use double nut + Loctite 243
blue (medium strength) on outer nut thread.

### [9b] Battery rail geometry

Reference battery: Tattu 150C-1800mAh-6S-XT60 — 78 × 40 × 53 mm (L×W×H).
Battery centred on X body core: front edge +39 mm, rear edge −39 mm.
Battery exits RIGHT. Endstop wall on LEFT end.

| Alias | Value | Description |
|---|---|---|
| `BattLength` | 78.0 mm | Reference battery length (nose-to-tail) |
| `BattWidth` | 40.0 mm | Reference battery width (side-to-side) |
| `BattHeight` | 53.0 mm | Reference battery height (vertical) |
| `BattRailInnerWidth` | 41.0 mm | Rail inner width = BattWidth + 1 mm tolerance |
| `BattRailHeight` | 53.0 mm | Rail height = BattHeight |
| `BattRailWall` | 3.0 mm | Rail wall thickness — PETG |
| `BattRailOuter` | 47.0 mm | Rail outer width = BattRailInnerWidth + 2× BattRailWall |
| `BattStrapSlotWidth` | 20.0 mm | Lateral strap slot width in rail top face |
| `BattStrapSlotDepth` | 3.0 mm | Lateral strap slot depth |

Verify rail fit with Coupon 11 before printing full Platform. Adjust
`BattRailInnerWidth` by +0.5 mm if coupon slides too tightly.

### [10] Mast interface geometry

| Alias | Value | Description |
|---|---|---|
| `MastInsertOD` | 4.6 mm | Heat-set insert bore diameter |
| `MastBossDia` | 9.0 mm | Mast boss outer diameter |
| `MastBossHeight` | 7.0 mm | Mast boss height (5 mm insert + 2 mm margin) |
| `MastSpacing` | 20.0 mm | Mount hole centre-to-centre spacing |

Note: with Pi bay fitted (always), effective mast mounting surface is
6 mm above Backplane surface. Mast height references are unchanged — the
bay height is accounted for in the stack geometry.

### [11] GPS / camera bracket geometry

V2.4.6: bracket carries GPS (top) + camera (middle) only. VTX has moved
to the Platform electronics zone. Camera tilt is field-adjustable via
two-bolt arc-slot mechanism (0°–30°).

| Alias | Value | Description |
|---|---|---|
| `BracketWidth` | 26.0 mm | Bracket width |
| `BracketMountDia` | 3.0 mm | M3 clearance — bracket-to-Platform mounting |
| `BracketMountSpacing` | 20.0 mm | M3 hole spacing at bracket base |
| `BracketCamTiltMin` | 0° | Minimum camera tilt (terrain mapping) |
| `BracketCamTiltMax` | 30° | Maximum camera tilt (acro/skating) |
| `BracketCamTiltDefault` | 15° | Default tilt |
| `BracketPivotSpacing` | 20.0 mm | Pivot bolt to slot bolt distance |
| `BracketArcRadius` | 20.0 mm | Arc slot radius = BracketPivotSpacing |
| `BracketSlotWidth` | 3.3 mm | Arc slot width (M3 clearance) |
| `BracketSlotArcLength` | 10.5 mm | Arc slot length (covers full 30° range) |
| `BracketIndexSpacing` | 5° | Visual index mark spacing on bracket face |

Camera plate: 26 mm × 22 mm × 4 mm. Camera slot: 19 × 19 mm (HDZero ±0.5 mm).
MIPI cable (225 mm) runs nose-to-tail through Platform MIPI channel.
Camera-to-VTX distance: ~198 mm. Service loop: ~26 mm.

### [12] Assembly offsets and clearances

| Parameter | Value | Description |
|---|---|---|
| Rod entry chamfer | 0.5 mm × 45° | At rod channel entries on all layers |
| Tab T-lock clearance | 0.2 mm per side | Slide fit into T-slot |
| Motor passive cover gap | air gap required | Cover contacts arm head ONLY via O-ring bosses |
| Minimum prop clearance | 15 mm | Prop tip to any Platform feature |

### [13] Platform geometry (V2.4.6)

Three-layer architecture: X body sandwich (structural) / Platform (electronics) / Backplane (payloads).

Platform has stepped width: 40 mm in battery and nose zone; 50 mm from
Y = −44 mm (electronics zone front) to tail.

All Y positions measured from X body centre. Positive = nose. Negative = tail.

| Alias | Value | Description |
|---|---|---|
| `PlatformLength` | 283.0 mm | Total Platform length |
| `PlatformWidthNarrow` | 40.0 mm | Width — battery zone and nose |
| `PlatformWidthElec` | 50.0 mm | Width — electronics zone |
| `PlatformStepY` | −44.0 mm | Y position where width steps out |
| `PlatformThick` | 3.0 mm | Platform base plate thickness |
| `PlatformNose` | +110.0 mm | Platform nose tip from body centre |
| `PlatformTail` | −173.0 mm | Platform tail tip from body centre |
| `PlatformAttachSpacing` | 20.0 mm | M3 screw spacing — Platform to X body |
| `BattZoneFront` | +39.0 mm | Battery front edge from body centre |
| `BattZoneRear` | −39.0 mm | Battery rear edge from body centre |
| `ElecZoneFront` | −44.0 mm | Electronics zone front (ESC front) |
| `ElecZoneRear` | −89.0 mm | Electronics zone rear (ESC rear) |
| `BuckZoneRear` | −99.0 mm | Buck converter rear edge |
| `VTXZoneFront` | −104.0 mm | VTX front edge |
| `VTXZoneRear` | −133.0 mm | VTX rear edge |
| `FanZoneFront` | −138.0 mm | Fan front face |
| `FanZoneRear` | −148.0 mm | Fan rear face / exhaust point |
| `AntennaPos` | −153.0 mm | ELRS antenna position from body centre |
| `BracketZoneFront` | +110.0 mm | Camera/GPS bracket nose tip |
| `BracketZoneRear` | +50.0 mm | Camera/GPS bracket base / Platform nose start |

**Prop clearance at tightest point (electronics zone, 50 mm width):**
Motor at Y = −116.7 mm → 15.7 mm clearance per side. This is above the
15 mm design minimum but has zero headroom. Verify in FreeCAD cross-section
view BEFORE printing the Platform. If CAD reads < 15 mm, reduce
`PlatformWidthElec` from 50 mm to 48 mm.

### [14] Backplane geometry

| Alias | Value | Description |
|---|---|---|
| `BackplaneNose` | +39.0 mm | Backplane nose edge = battery front edge |
| `BackplaneTail` | −148.0 mm | Backplane tail edge = fan rear face |
| `BackplaneLength` | 187.0 mm | Total backplane length |
| `BackplaneWidth` | 50.0 mm | Backplane width = PlatformWidthElec |
| `BackplaneBeamWidth` | 3.0 mm | Lattice beam width |
| `BackplaneBeamThick` | 1.5 mm | Lattice beam thickness (height above Platform) |
| `BackplaneRibSpacing` | 20.0 mm | Transverse rib centre-to-centre |
| `BackplaneFill` | 35% | Approximate material fill (~65% open area) |
| `BackplanePostDia` | 6.0 mm | Attachment post outer diameter |
| `BackplanePostHeight` | 54.0 mm | Post height = BattRailHeight + 1 mm |
| `BackplaneAttachDia` | 3.0 mm | M3 clearance hole at each post base |
| `BackplaneGX12BossOD` | 18.0 mm | Boss ring OD around GX12 hole in lattice |
| `BackplaneGX12BossThick` | 3.0 mm | Boss ring wall thickness |

**Attachment post positions (3 pairs, integral to Platform):**
- Post pair A: Y = +39 mm (battery front)
- Post pair B: Y = −39 mm (battery rear)
- Post pair C: Y = −148 mm (fan rear / backplane tail)

Battery zone right side is fully open — no lattice beam in RIGHT edge
between Y = +39 and Y = −39 mm. Battery exits RIGHT under open lattice.

Fan exhaust zone (Y = −138 to −148 mm): no lattice — fully open for exhaust.

### [15] Pi bay and companion interface geometry

Pi bay is mandatory on every build across all platforms. Empty bay uses a
printed cover plate. Pi Zero 2W installs in 15 minutes when ordered.

| Alias | Value | Description |
|---|---|---|
| `PiBayInternalWidth` | 72.0 mm | Pi bay internal width |
| `PiBayInternalLength` | 38.0 mm | Pi bay internal length |
| `PiBayInternalHeight` | 6.0 mm | Pi bay internal height |
| `PiBayWall` | 2.0 mm | Pi bay wall thickness |
| `PiBayStandoffSpacingX` | 58.0 mm | Pi Zero 2W hole spacing — X axis |
| `PiBayStandoffSpacingY` | 23.0 mm | Pi Zero 2W hole spacing — Y axis |
| `PiBayStandoffDia` | 2.5 mm | M2.5 standoff mounting holes |
| `PiBayHarnessSlot` | 8.0 mm | JST-SH cable entry slot width |
| `PiZeroWidth` | 65.0 mm | Pi Zero 2W PCB width (reference) |
| `PiZeroLength` | 30.0 mm | Pi Zero 2W PCB length (reference) |
| `PiZeroHeight` | 5.0 mm | Pi Zero 2W maximum component height (reference) |
| `CompanionHarnessWires` | 4 | Wire count: 5V, GND, FC_TX, FC_RX |
| `CompanionHarnessAWG` | 28 | Wire gauge |
| `CompanionHeaderType` | JST-SH | 4-pin, 1 mm pitch |
| `CompanionUART` | UART6 | Reserved permanently — never reassign |
| `CompanionBaudRate` | 921600 | MAVLink2 (ArduPilot) / MSP (Betaflight) |

Pi bay raises the payload mast surface by `PiBayInternalHeight` (6 mm) above
the Backplane surface. Mast height references account for this. Bay is fitted
on all builds.

---

## Procedure

### Verifying the populated spreadsheet against this article

1. Open the FreeCAD document. Double-click `Variables` in the Model Tree.
2. For each section in this article, spot-check 2–3 values against the cell
   in column B. Click the cell — Properties panel shows the alias name.
3. Verify alias name matches exactly (case-sensitive). A mismatched alias
   means no sketch that references that variable name will resolve correctly.
4. Pay particular attention to: `RodDiaChannelCore` (2.1 mm, not 2.2 mm),
   `GX12ChimneyBoreFlatFlat` (10.80 mm, not 10.60 mm — different from BodyFlatFlat),
   `SandwichBoltCornerOffset` (18.0 mm, not 20.0 mm — older docs say 20 mm).
5. If any value is wrong: double-click the cell, edit the value, press Enter.
   All sketch dimensions referencing that alias update automatically.

### Critical first-print adjustments (adjust these variables from coupon results before full build)

| Coupon | Variable to adjust | Direction |
|---|---|---|
| Coupon 8 — T-slot fit | `TabWidth` or `TabClearance` | Too tight: reduce TabWidth by 0.1 mm |
| Coupon 8b — Rod interference | `RodDiaChannelCore` | Too tight: increase by 0.05 mm |
| Coupon 10 — GX12 D-D bore | `GX12ChimneyBoreFlatFlat` | Too tight: increase by 0.1 mm |
| Coupon 11 — Battery rail | `BattRailInnerWidth` | Too tight: increase by 0.5 mm |

→ See [[coupon-validation]] for full pass/fail criteria and measurement procedure.

---

## Rationale

### Why SandwichBoltCornerOffset is 18 mm and not 20 mm

Some earlier documents (including the V2.4.5 Master Specification draft) used
20 mm as the corner bolt offset. The FreeCAD Cookbook, which is the more
precise source, uses 18 mm — measured from the actual model geometry rather
than the approximate stated value. 18 mm is the adopted value. All new builds
and all PCCF layer prints use 18 mm. Do not use 20 mm.

### Why the GX12 bore values are physically measured and not nominal

GX12 connectors are manufactured to a nominal 12 mm designation, but the
actual body dimensions vary by supplier. The values in section [9] (10.60 mm
flat-to-flat, 11.67 mm OD) were physically measured on the parts sourced for
V2.4.6. A different supplier batch may require different clearance values.
Always print Coupon 10 first. The 0.20 mm clearance applied to both flat-flat
and OD values is a starting point, not a guarantee.

### Why PiBayInternalHeight matters for payload design

Every payload mast height calculation must include the 6 mm Pi bay height.
A mast designed to sit at 40 mm above the Backplane surface will actually sit
at 46 mm above the Platform surface (40 + 6). Payload designers who omit this
will produce connector geometry that is out of reach. The Pi bay is permanent;
it is not removed for payload swaps.

---

## Connections

requires:
  - [[variable-table-structure]]
related:
  - [[frame-structure-overview]]
  - [[sandwich-structure]]
  - [[cf-rod-architecture]]
  - [[scaling-libdrone]]
  - [[coupon-validation]]
leads_to:
  - [[freecad-document-setup]]


[variable-table-structure]: variable-table-structure.md "Variable table structure"
[scaling-libdrone]: scaling-libdrone.md "Scaling libdrone to a new frame size"
[coupon-validation]: coupon-validation.md "Coupon validation"
[frame-structure-overview]: frame-structure-overview.md "Frame structure overview"
[sandwich-structure]: sandwich-structure.md "Sandwich structure"
[cf-rod-architecture]: cf-rod-architecture.md "Carbon fibre rod architecture"
[freecad-document-setup]: freecad-document-setup.md "FreeCAD document setup"


[variable-table-structure]: variable-table-structure.md "Variable table structure"

[variable-table-structure]: variable-table-structure.md "Variable table structure"
