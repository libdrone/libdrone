---
id: sk-freecad-contributor-guide
title: "FreeCAD Contributor Guide"
version: 2.0.0
date: 2026-06-02
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 7.contributor
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

This guide is for an experienced FreeCAD user who wants to contribute the
parametric CAD model for libdrone. It does not teach FreeCAD. What it provides
is a complete engineering brief: what the platform is, what each part must do,
what the geometry constraints are, how the parametric system works, what the
validation gates are, and how to contribute back.

If you can model a parametric assembly in FreeCAD Part Design and Assembly
Workbench, this document gives you everything you need to start. Read it fully
before opening FreeCAD.

The repo: **https://github.com/libdrone/libdrone**

---

## Concept

### What you are building

libdrone is a 330 mm True-X quadrotor designed as an open aerial payload
platform. It is not a racing drone. It carries sensors, cameras, and
instruments for institutional users — municipalities, civil protection agencies,
university research groups — who need aerial sensing without cloud dependency,
vendor lock-in, or proprietary data pipelines.

The frame has three structural layers stacked vertically:

    +-------------------------------------------------+
    |  BACKPLANE (payload carrier -- open lattice)    |  top
    +-------------------------------------------------+
    |  PLATFORM (electronics carrier -- PETG)         |  middle
    +-------------------------------------------------+
    |  X BODY SANDWICH (structural spine)             |  bottom
    |  5 layers: PETG / PCCF / PCCF / PCCF / PETG    |
    +-------------------------------------------------+

Four arms attach to the X body sandwich via T-slot joints. Each arm carries
one motor. Two GX12-7 aviation connectors on the sealed Platform top surface
are the payload interface -- any sensor payload connects here.

### Why FreeCAD specifically

FreeCAD is not an arbitrary choice. The mission of libdrone is to empower
communities worldwide -- municipalities, SAR groups, university labs -- to
build, repair, and adapt their own platform without vendor permission or a
software licence cost. A community in Czech Republic, a university in South
Korea, or a civil protection group in the Baltics must be able to open the
file, change the wheelbase for a different prop size, and print the result.
That requires parametric files, open tooling, and no paywall. FreeCAD is the
only CAD tool that satisfies all three simultaneously.

### How the parametric system works

Every dimension in every part is a reference to a named variable in a central
FreeCAD Spreadsheet called `Variables`. No sketch contains a typed number --
every dimension uses `=Variables.AliasName` syntax. The macro
`hardware/LD_V300_Variables.FCMacro` creates the complete spreadsheet with
all ~90 aliases in one run.

Two variable classes:

**Frame-driven variables** scale when the wheelbase changes. Examples:
`ArmShaftLength`, `XBodyCoreSize`, `XBodyArmLength`. If you change `Wheelbase`
from 330 mm to 280 mm, these propagate automatically.

**Electronics-driven variables** stay fixed regardless of airframe scale.
Examples: `StackPattern` (30.5 mm FC mount), `GX12ChimneyBoreOD` (11.87 mm),
`BattWidth` (40 mm). These are driven by component dimensions, not frame
geometry. Never scale them with wheelbase.

See [[variable-table-structure]] for the full variable organisation.
See [[variable-table-values]] for all 90 variables with tolerances and critical
notes. Read this before modelling anything.

---

## Reference

### Parts list -- what needs to be modelled

| Body name | Material | Qty | Print orientation |
|---|---|---|---|
| Body_XBodyPETGBottom | PETG | 1 | Flat on bed |
| Body_XBodyPCCF | PCCF | 3 (identical) | Flat on bed |
| Body_XBodyPETGTop | PETG | 1 | Flat on bed |
| Body_ArmTab | PETG | 8 (2 per arm) | Flat on bed |
| Body_ArmShaft | PETG | 4 + 2 spare | **Vertical -- critical** |
| Body_ArmCoverActive | PETG | 4 | Flat on bed |
| Body_ArmCoverPassive | PETG-CF | 4 | Flat on bed |
| Body_Bumper | ASA | 4 + 4 spare | Flat on bed |
| Body_Platform | PETG | 1 | Flat on bed |
| Body_Backplane | PETG | 1 | Flat on bed |
| Body_GPSBracket | PETG | 1 | Flat on bed |
| Body_CameraTiltPlate | PETG | 1 | Flat on bed |

**The arm shaft must be printed vertically.** Layers perpendicular to the
bending load axis. Wrong orientation produces a structurally deficient part
regardless of all other settings.

---

### Part-by-part engineering brief

#### X body PETG bottom layer

The bottom face of the entire sandwich. First ground contact in a crash.

**What it must do:** absorb impact without shattering; provide rod interference
fit in the core zone; capture M3 sandwich nuts; form the lower T-slot wall.

**Critical geometry:**

Rod channels in the core zone use `RodDiaChannelCore` = **2.1 mm**
(interference fit). This grips the 2.0 mm CF rod and pre-tensions the
sandwich. If you use the clearance value (2.2 mm) here the sandwich has
no pre-tension and will vibrate.

Rod channels in the arm zones (outside the core) use `RodDiaChannel` = 2.2 mm
(clearance fit). Do NOT use interference fit in arm zones.

M3 hex nut capture pockets: 6 positions -- 4 corners at
(+/-SandwichBoltCornerOffset, +/-SandwichBoltCornerOffset) = (+/-18, +/-18 mm)
and 2 axis positions at (0, +/-SandwichBoltNoseTailY) = (0, +/-22 mm).
Use 18 mm for the corner offset. Some earlier documents say 20 mm -- that
is wrong.

T-slot pockets at 45 degrees in each arm extension zone. Slot width =
`TabWidth + TabClearance` = 22.0 + 0.2 = 22.2 mm per side. Engagement
depth = `TabLength` = 20 mm.

Layer thickness: `PETGBotLayerThick` = 3 mm.

Material: PETG. Do NOT print in PCCF -- PCCF shatters on ground impact.

**Why PETG and not PCCF at the bottom:** PCCF is stiff but brittle -- it
shatters under sharp impact and would propagate crack energy into the T-slot
zone above it. PETG deforms rather than shatters. Think of a shoe sole:
rubber (tough) not steel (stiff). See [[sandwich-structure]].

**Print coupon before printing:** Coupon 8 validates T-slot fit. Print it,
verify the arm tab slides in with light hand pressure and zero lateral play.
Adjust `TabClearance` if needed. Do not print the full layer until Coupon 8
passes. See [[coupon-validation]].

---

#### X body PCCF layers (x3, identical)

The structural spine of the frame. Three identical layers stacked vertically.

**What they must do:** carry all bending loads from the arms; provide T-slot
engagement over full PCCF depth; maintain dimensional stability under motor
vibration.

**Critical geometry:**

All rod channels: `RodDiaChannel` = **2.2 mm** (clearance fit only -- never
interference fit in PCCF; the material would micro-crack).

T-slot pockets at 45 degrees: same width and depth as PETG bottom layer.
Must align exactly across all three PCCF layers when stacked -- this is what
the CF rods enforce during assembly.

Sandwich bolt through-holes: M3 clearance = `SandwichBoltDia` = 3.3 mm.
Same 6-position pattern as PETG bottom.

Layer thickness: `PCCFLayerThick` = 3 mm each.

X body plan shape: central core `XBodyCoreSize` x `XBodyCoreSize` = 60 x 60 mm
square, with four arm extensions `XBodyArmWidth` x `XBodyArmLength` =
40 x 35 mm projecting at 45 degrees.

**Minimum wall rule:** 3.0 mm minimum wall retained between any two features
(T-slot, rod channel, bolt hole). Violating this risks crack propagation
under crash load.

---

#### X body PETG top layer

The clean structural top surface of the sandwich. Electronics and the Platform
attach here.

**What it must do:** provide FC/ESC stack mounting holes (`StackPattern` =
30.5 mm square M3); provide Platform attachment holes; present a flat,
feature-free top surface.

**Critical geometry:**

Layer thickness: `PETGTopLayerThick` = **4 mm** -- not 3 mm. The extra
millimetre provides 4 full threads of M3 engagement for the stack standoffs.
Using 3 mm here strips threads under vibration.

Same bolt pattern and rod channels as all other layers (clearance fit
2.2 mm everywhere in this layer).

No cable management features in V2.4.6. The top layer is deliberately clean.
All cable routing has moved to the Platform.

Platform attachment hole pattern: `PlatformAttachSpacing` = 20 mm.

---

#### Arm tab (x8 -- 2 per arm)

The joint between the arm shaft and the sandwich structure.

**What it must do:** engage the T-slot over full depth; lock against lateral
pull-out via the T-profile; transmit arm bending loads into the PCCF sandwich.

**Critical geometry:**

Tab thickness = `TabThick` = `SandwichHeight` = **16 mm exactly**. If the
tab is thinner than the sandwich height it has slop in the slot. If thicker
it will not enter the slot.

Tab width = `TabWidth` = 22 mm (adjust from Coupon 8 result).

T-lock: `TabLockWidth` x `TabLockDepth` = 8 x 4 mm extension that hooks
behind the T-slot shoulder. This prevents pull-out under crash load.

Engagement depth `TabLength` = 20 mm minimum.

Two M2 screw holes for shaft attachment: `TabScrewDia` = 2.0 mm clearance,
`TabScrewSpacing` = 10 mm centre-to-centre.

Print orientation: flat on bed (loads are in shear and compression, not bending).

---

#### Arm shaft (x4 + 2 spare)

The arm from tab junction to motor head. Deliberately the weakest structural
element -- a fuse that fails before anything more expensive does.

**What it must do:** carry the motor; route CF rods from sandwich to arm tip;
manage motor phase cables; fracture predictably at the bending cross-section
in a crash, before tabs, PCCF layers, or electronics are damaged.

**Critical geometry:**

Length: `ArmShaftLength` = 125 mm from tab junction face to motor head
outer face. Verify in Assembly that CF rods do not protrude past the arm tip.

Cross-section: `ArmWidth` x `ArmHeight` = 26 x 16 mm. Height must equal
`SandwichHeight` = 16 mm exactly.

Rod channels: two per shaft at Z offsets `RodOffsetOuter` = 5.0 mm and
`RodOffsetInner` = 2.0 mm (for FL/RR arm orientation). FR/RL arms use
-5.0 mm and -2.0 mm. Use clearance fit `RodDiaChannel` = 2.2 mm throughout.

Pinch slit: `PinchSlit` = 0.5 mm wide, running axially along the shaft at
each rod channel. This allows slight elastic deflection that grips the rod
after insertion.

Motor head: `MotorHeadWidth` x `MotorHeadHeight` = 35 x 18 mm. Four M3
through-bores at motor bolt pattern. Counterbores for O-ring seat:
`ORingCBoreDia` = 7.0 mm, `ORingCBoreDepth` = 1.5 mm, with lateral rim
`ORingRimHeight` = 0.5 mm preventing O-ring migration.

Loft transition from motor head to shaft: `MotorHeadTaper` = 20 mm.

Dovetail cable groove on BOTTOM face of shaft (not top):
`CableGrooveWidth` = 4.5 mm, `CableGrooveDepth` = 2.0 mm,
`CableGrooveAngle` = 8 degrees. Motor phase wires run in this groove under
the active cover. **Wrong face = wires on wrong side after assembly.**

Strain relief port in motor head side wall: `CablePortDia` = 5.5 mm.

MR30 connector pocket in shaft body for motor connector retention.

Two M2 tab attachment holes per tab face: `CoverScrewDia` = 2.0 mm,
`TabScrewSpacing` = 10 mm. Accessible from arm tip.

**Print orientation: vertical (motor head up or down). This is mandatory.**
Layers must be perpendicular to the bending load axis. A horizontally-printed
shaft has interlaminar shear planes aligned with the crash force -- it will
delaminate rather than fracture cleanly. See [[arm-shaft]].

---

#### Arm cover -- active (x4, PETG)

Protective cover over the motor cable run along the arm bottom face.

**Critical geometry:**

Dovetail profile matches shaft groove: `CableGrooveWidth` = 4.5 mm,
`CableGrooveDepth` = 2.0 mm, angle `CableGrooveAngle` = 8 degrees.

MR30 cable pass-through slot at motor end.

Two M2 retention screws: `CoverScrewDia` = 2.0 mm clearance.

---

#### Arm cover -- passive (x4, PETG-CF)

Sits over the motor head and captures the M3 nyloc nuts for the floating
motor mount.

**Critical geometry:**

O-ring boss geometry: `ORingCBoreDia` = 7.0 mm, `ORingCBoreDepth` = 1.5 mm,
rim height `ORingRimHeight` = 0.5 mm, rim wall `ORingRimWall` = 0.5 mm.
The rim prevents O-ring migration laterally.

Air gap between cover inner face and motor head top face -- cover must NOT
make flat contact. The motor floats on O-rings only.

M3 nyloc capture pockets at motor bolt pattern.

**FFP3 respirator mandatory when printing PETG-CF.**

---

#### ASA bumpers (x4 + 4 spare)

Sacrificial hollow tip covers at the arm shaft tips.

Geometry-compensated hollow tip matching arm shaft profile. ASA only --
PETG degrades under sustained UV and heat.

---

#### Platform

The most complex part. Electronics carrier, battery rail, GX12 payload
interface, cooling fan slot, wire routing, Pi bay.

**Overall dimensions:**

Length: `PlatformLength` = 283 mm (nose to tail).
Width: stepped -- `PlatformWidthNarrow` = 40 mm at nose and battery zone;
`PlatformWidthElec` = 50 mm from `PlatformStepY` = -44 mm to tail.
Thickness: `PlatformThick` = 3 mm base plate.
All Y positions measured from X body centre. Positive = nose. Negative = tail.

**Zone layout (nose to tail):**

| Zone | Y range | Content |
|---|---|---|
| Bracket base | +110 to +50 mm | GPS/camera bracket attachment |
| Battery | +39 to -39 mm | Battery rails, strap slots, endstop |
| Electronics front | -44 to -89 mm | ESC, FC stack |
| Buck zone | -89 to -99 mm | 5V buck converter |
| VTX zone | -104 to -133 mm | Video transmitter |
| Fan zone | -138 to -148 mm | Gdstime 3010 cooling fan |
| Antenna | -153 mm | ELRS antenna exit |

**GX12 dual connectors -- most critical feature of the entire platform:**

Both GX12-7 male panel-mount connectors sit at `GX12_PositionY` = -66 mm
(mid-electronics zone), centred on the Platform width axis.

Connector A (signal): `GX12A_PositionX` = -25 mm (left side).
Connector B (power): `GX12B_PositionX` = +25 mm (right side).
Centre-to-centre: `GX12_CentreToCentre` = 50 mm.

**The chimney bore is NOT a round hole. It is a D-D profile.**

In FreeCAD Sketcher, for each connector:
1. Draw circle, diameter `GX12ChimneyBoreOD` = 11.87 mm
2. Add two parallel lines at +/-(GX12ChimneyBoreFlatFlat / 2) = +/-5.40 mm from centre
3. Trim the circle arcs outside those lines
4. Result: two arcs joined by two parallel flat segments

This D-D shape prevents the connector from rotating and backing off its
retention nut under vibration. A round bore looks adequate but will fail in
the field after the first payload swap. See [[gx12-connector-standard]].

Each connector also needs:
- Raised boss on Platform surface: `GX12BossDia` = 14 mm, `GX12BossHeight` = 3 mm
- Chimney below Platform: `GX12ChimneyOD` = 18 mm, `GX12ChimneyHeight` = 25 mm,
  wall `GX12ChimneyWall` = 3 mm
- Wire exit slot at chimney base: 6 x 4 mm

**Print Coupon 10 and verify GX12 fit before printing the full Platform.**
Adjust `GX12ChimneyBoreFlatFlat` by +/-0.1 mm if coupon is tight or sloppy.

**EMC wire channels -- non-negotiable:**

Two wire routing channels run nose-to-tail on the Platform underside:
- LEFT channel (signal wires -- GPS, FC, I2C, UART): centreline at Y = -20 mm
- RIGHT channel (power wires -- battery leads, ESC power): centreline at Y = +20 mm
- Both: `WireChannelWidth` = 4.0 mm, `WireChannelDepth` = 1.0 mm

These channels enforce physical separation of signal and power wiring. Motor
switching noise couples capacitively into adjacent wires -- proximity is the
mechanism, separation is the fix. If these features are omitted, the build
will fly but will have degraded GPS performance and noisy Blackbox traces.
See [[power-signal-separation]].

**Battery rail:**

Reference battery: Tattu 1800mAh 6S, 78 x 40 x 53 mm (L x W x H).
Battery centred on X body core. Exits RIGHT. Endstop wall on LEFT.

Rail inner width: `BattRailInnerWidth` = 41 mm (= BattWidth + 1 mm tolerance).
Rail height: `BattRailHeight` = 53 mm.
Rail wall: `BattRailWall` = 3 mm.
Strap slots: `BattStrapSlotWidth` = 20 mm, `BattStrapSlotDepth` = 3 mm.
Battery lead relief notch at RIGHT end: 8 x 4 mm.

**Print Coupon 11 and verify battery fit before printing full Platform.**

**Cooling fan slot:**

Gdstime 3010 fan (30 x 30 x 10 mm) at tail.
Slot: `FanSlotWidth` x `FanSlotHeight` = 30 x 35 mm.
Fan front face at `FanZoneFront` = -138 mm.
Minimum wall either side of slot: `FanSlotWall` = 1.5 mm.

**MIPI cable channel:**

Central nose-to-tail channel for camera MIPI cable.
`MIPIChannelDepth` = 1.5 mm, `MIPIChannelWidth` = 16 mm.
Runs from bracket zone rear (+50 mm) to VTX zone (-133 mm). Fully enclosed.

**Pi bay:**

Mandatory on every Platform build. A Pi Zero 2W companion computer installs
here. Empty bay uses a printed cover plate.

Internal: `PiBayInternalWidth` x `PiBayInternalLength` x `PiBayInternalHeight`
= 72 x 38 x 6 mm.
Wall: `PiBayWall` = 2 mm.
Standoff holes: M2.5 at `PiBayStandoffSpacingX` x `PiBayStandoffSpacingY`
= 58 x 23 mm.
JST-SH harness entry slot: `PiBayHarnessSlot` = 8 mm.

**The Pi bay raises the payload mast surface by 6 mm** above the Backplane
surface. Every payload mast height must account for this. A 40 mm mast above
the Backplane surface actually sits 46 mm above the Platform surface.

**Prop clearance check -- verify before printing:**

At 50 mm electronics zone width, the motor at Y = -116.7 mm leaves 15.7 mm
clearance per side to the Platform edge. This is above the 15 mm minimum but
has zero headroom. Verify in FreeCAD cross-section before printing. If the
CAD reads less than 15 mm, reduce `PlatformWidthElec` from 50 to 48 mm.

---

#### Backplane

Open PETG lattice sitting on top of the Platform. Payload modules attach here.

**Overall dimensions:**

Length: `BackplaneLength` = 187 mm (nose +39 mm to tail -148 mm).
Width: `BackplaneWidth` = 50 mm (= PlatformWidthElec).

**Lattice geometry:**

Beam width: `BackplaneBeamWidth` = 3 mm.
Beam thickness: `BackplaneBeamThick` = 1.5 mm.
Transverse rib spacing: `BackplaneRibSpacing` = 20 mm.
Target fill: approx 35% (65% open area).

**Attachment posts (3 pairs, integral to Platform, Backplane bolts to them):**

Post pair A: Y = +39 mm (battery front).
Post pair B: Y = -39 mm (battery rear).
Post pair C: Y = -148 mm (fan rear / backplane tail).
Post OD: `BackplanePostDia` = 6 mm, height: `BackplanePostHeight` = 54 mm.
M3 clearance holes at each post base: `BackplaneAttachDia` = 3 mm.

**Open zones (no lattice):**

RIGHT edge between Y = +39 and -39 mm: battery exits RIGHT, lattice must
not block this opening.
Fan exhaust zone Y = -138 to -148 mm: fully open for airflow.

**GX12 holes in lattice:**

Two holes at same X/Y as Platform GX12 positions.
Boss rings around each hole: `BackplaneGX12BossOD` = 18 mm,
`BackplaneGX12BossThick` = 3 mm.
GX12 connector heads protrude through these holes to the payload mast surface.

---

#### GPS / camera bracket

Forward nose bracket carrying the GPS module (top) and camera (middle).
VTX has moved to the Platform in V2.4.6 -- bracket carries GPS and camera only.

**Critical geometry:**

Width: `BracketWidth` = 26 mm.
Base mount holes: M3 at `BracketMountSpacing` = 20 mm spacing.
Camera tilt mechanism: two-bolt arc-slot, 0-30 degrees, field-adjustable.
- Pivot bolt to slot bolt: `BracketPivotSpacing` = 20 mm
- Arc slot radius = 20 mm, width = 3.3 mm (M3 clearance)
- Arc slot length = 10.5 mm (covers full 30 degree range)
- Index marks every 5 degrees on bracket face
- Default tilt: 15 degrees
GPS pocket at top of bracket for u-blox M10 or equivalent.
Camera slot: 19 x 19 mm (HDZero +/-0.5 mm).

---

### Coupon validation gates -- print these before the parts they protect

| Coupon | Tests | Blocks | Variable to adjust |
|---|---|---|---|
| 8 -- T-slot fit | Tab slides in: light pressure, zero play | All PCCF layers, arm tabs | TabWidth, TabClearance |
| 8b -- Rod interference | 2.1 mm channel grips 2 mm rod firmly | PETG bottom layer | RodDiaChannelCore |
| 10 -- GX12 D-D bore | Connector fits, does not rotate, nut threads | Platform | GX12ChimneyBoreFlatFlat |
| 11 -- Battery rail | Battery slides in/out cleanly, strap passes | Platform | BattRailInnerWidth |

See [[coupon-validation]] for full pass/fail criteria and measurement procedure.

---

### Assembly checks

After all parts are modelled, build the Assembly and verify:

1. Rod clearance -- CF rod paths do not intersect FC/ESC stack footprint
2. Prop clearance -- Platform edge at electronics zone is >= 15 mm from
   prop tip arc in top view. Motor at Y = -116.7 mm, 6-inch prop radius = 76 mm
3. Backplane post engagement -- post rings seat fully on Platform chimney bosses
4. GX12 protrusion -- connector heads protrude cleanly through Backplane holes
5. Pi bay height -- mast surface is 6 mm above Backplane surface

See [[freecad-assembly-workbench]].

---

## Procedure

### Getting started (six steps)

1. Install FreeCAD 1.1 stable: https://www.freecad.org/downloads.php
2. Clone or download the repo: https://github.com/libdrone/libdrone
3. Copy `hardware/LD_V300_Variables.FCMacro` to your FreeCAD Macro folder:
   - macOS: ~/Library/Preferences/FreeCAD/Macro/
   - Linux native: ~/.FreeCAD/Macro/
   - Linux Flatpak: ~/.var/app/org.freecad.FreeCAD/data/FreeCAD/1.1/Macro/
   - Windows: %APPDATA%\FreeCAD\Macro\
4. Create a new FreeCAD document. Run Tools > Macros > LD_V300_Variables > Execute
5. Verify the Variables spreadsheet appears. Spot-check:
   B2 alias = Wheelbase, B7 alias = ArmWidth, B17 alias = RodDia
6. Set document preferences once: mm/kg/s units, 3 decimal places, CAD navigation.
   See [[freecad-document-setup]]

### Recommended modelling sequence

Model in this order. Each part provides geometry references for the next.

1. Variable spreadsheet -- verify all aliases before any geometry
2. X body PETG bottom -- establishes Z origin and rod interference geometry
3. X body PCCF layers (all three identical) -- rod clearance, T-slots, bolts
4. X body PETG top -- clean surface, stack holes
5. Arm tab -- T-lock, thickness = SandwichHeight
6. Arm shaft -- rods, pinch slit, motor head, dovetail groove
7. Arm cover active -- dovetail fit, MR30 pass-through
8. Arm cover passive -- O-ring boss, nyloc pockets
9. ASA bumper -- tip geometry
10. Platform -- GX12 bores, Pi bay, battery rail, wire channels, fan slot
11. Backplane -- lattice, post bosses, GX12 holes
12. GPS / camera bracket -- arc slot, GPS and camera pockets
13. Assembly -- prop clearance, backplane engagement, GX12 protrusion
14. STL export -- correct orientation per part, 0.01 mm deviation

### Three modelling habits that matter

Name every feature as you create it. ArmProfile, PinchSlit, RodChannelLeft --
not Sketch002, Pocket003. The model tree must be self-documenting.

Fully constrain every sketch before closing it. Yellow/white = underconstrained
= geometry drifts when variables change. Only close on green "Fully constrained."

Use `=Variables.AliasName` for every dimension. Never type a number. A typed
number is a hardcoded constant that breaks when variables change.

### Recovering from topological naming errors

FreeCAD's topological naming problem can cause features to detach from their
reference geometry when upstream features change. See [[topological-naming-problem]].

If you see red cells or error dialogs on recompute:
1. Ctrl+Z to undo the last change
2. If undo fails: open the backup copy from before the edit
3. Find the first red item in the Model Tree -- that is the breakage point
4. Re-apply the constraint or reference using current geometry
5. Do not rename features mid-model -- this compounds TNP errors

### Contributing back

A zip file with the .FCStd and exported STLs is a valid first contribution.
Open a GitHub issue at https://github.com/libdrone/libdrone and attach the
files, or describe your approach and ask for a review before investing
significant time.

For the full PR workflow: see [[contributing-guide]]

All contributed CAD work is released under CERN OHL-S v2. Your payload
designs are yours -- the copyleft applies only to modifications of the
platform hardware.

---

## Rationale

This guide exists because the existing FreeCAD skeleton (sk-freecad-build-guide)
is written for someone learning FreeCAD while building libdrone -- it references
a Cookbook for click sequences and guides a novice through the learning process.
An experienced FreeCAD contributor does not need that. They need the engineering
specification: what each part must achieve, what the non-negotiable constraints
are, and where to find the authoritative numbers. This guide provides exactly
that, without the learning scaffolding.

Separating the two documents also future-proofs the corpus: UI-specific content
(click paths, dialog names) changes between FreeCAD versions; engineering
constraints do not. This guide will remain accurate regardless of whether the
community is using FreeCAD 1.1 or 1.5.

---

## Connections

requires:
  - [[variable-table-values]]
  - [[variable-table-structure]]
related:
  - [[sk-freecad-build-guide]]
  - [[contributing-guide]]
  - [[coupon-validation]]
  - [[frame-structure-overview]]
  - [[sandwich-structure]]
  - [[arm-shaft]]
  - [[gx12-connector-standard]]
  - [[power-signal-separation]]
leads_to:
  - [[contributing-guide]]
  - [[freecad-assembly-workbench]]
  - [[stl-export-and-slicer-setup]]
