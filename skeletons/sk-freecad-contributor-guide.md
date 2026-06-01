---
id: sk-freecad-contributor-guide
title: "FreeCAD Contributor Guide"
version: 1.0.0
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

This guide is for someone who knows FreeCAD and wants to contribute the
parametric model for libdrone. It assumes Part Design and Assembly Workbench
competence — it does not teach FreeCAD. What it provides is a complete
project brief: what parts need modelling, what constraints are non-negotiable,
what the validation gates are, and how to contribute back. Start here, not
at the builder guide.

---

## Concept

### Why FreeCAD specifically

FreeCAD is not an arbitrary tool choice. The mission of libdrone is to
empower communities worldwide — municipalities, volunteer SAR groups,
university research labs — to build, repair, and adapt their own platforms
without vendor permission or software licence costs. That mission requires
design files that are parametric, fully open, and runnable on any operating
system without a paywall.

FreeCAD is the only CAD tool that satisfies all three conditions. A community
in Czech Republic, a university lab in South Korea, or a civil protection
group in the Baltics all need to open the file, change the wheelbase for a
different prop size, and print the result. That is only possible with
parametric open files and no proprietary tooling in the chain. FreeCAD is
the answer to all three requirements simultaneously.

### What the model needs to produce

The libdrone frame is a 330 mm True-X quadrotor with a 5-layer sandwich
structure (PETG-PCCF-PCCF-PCCF-PETG), carbon fibre rod architecture, and a
standardised GX12-7 dual payload interface on the sealed top surface. Every
dimension is driven by a central spreadsheet of ~90 named variables.

The CAD deliverable is a set of Part Design bodies, an Assembly for fit
verification, and STL exports ready for PrusaSlicer. The geometry is fully
specified in → [[variable-table-values]]. This is implementation work against
a clear specification — not open-ended design work.

### The parametric variable system

All geometry derives from a single FreeCAD Spreadsheet named `Variables`.
Every sketch dimension must reference a spreadsheet variable using the
`=Variables.AliasName` syntax — no hardcoded numbers anywhere. This is what
makes the model community-usable: changing the wheelbase propagates through
the entire model automatically.

The macro `hardware/LD_V300_Variables.FCMacro` creates the complete spreadsheet
with all aliases in one run. → [[variable-table-structure]] explains the 15
sections and the two variable classes (frame-driven vs electronics-driven).
→ [[variable-table-values]] is the authoritative value reference with tolerances
and critical notes.

**Frame-driven variables** change when the wheelbase changes (arm length,
body width, rod spacing). **Electronics-driven variables** stay fixed regardless
of airframe scale (FC stack pattern, GX12 connector geometry, battery
dimensions). Never scale electronics-driven variables with the wheelbase.

### Non-negotiable modelling constraints

These constraints are engineering requirements, not preferences. Every one
has a documented rationale in the corpus.

**GX12 chimney bore — D-D profile, not round.**
Each GX12-7 connector bore must be a D-D shape (two arcs + two parallel
flats). A round bore allows the connector to rotate and back off the retention
nut under vibration. The D-D profile prevents rotation. → [[gx12-connector-standard]]
The FreeCAD Sketcher construction: draw a circle of `GX12ChimneyBoreOD`
diameter, add two parallel lines at ±(`GX12ChimneyBoreFlatFlat` / 2) from
centre, trim the arcs outside those lines. Print Coupon 10 to validate fit
before printing the full Platform.

**Rod channels — two diameters, two zones.**
The PETG bottom layer uses `RodDiaChannelCore` (2.1 mm) — an interference fit
that grips the rod and provides pre-tension. All other layers use
`RodDiaChannel` (2.2 mm) — clearance fit. Using the wrong diameter in the
wrong layer either prevents rod insertion or eliminates the pre-tension that
gives the sandwich its stiffness. → [[cf-rod-architecture]]

**Arm shaft — vertical print orientation.**
The arm shaft must be exported for vertical printing (motor head up or down).
Layers perpendicular to the bending load axis. This is the print orientation
decision, not a modelling decision — document it in the STL export list.
→ [[arm-shaft]]

**Platform wire channels — EMC geometry.**
The Platform has two wire routing channels: left side (Y = −20 mm) for signal
wires, right side (Y = +20 mm) for power wires. These channels are not cosmetic
— they enforce the physical separation that prevents motor switching noise
from coupling into GPS and FC signals. → [[power-signal-separation]]
If these features are missing from the Platform, the build will fly but will
have degraded GPS performance and noisy Blackbox traces.

**Tab geometry — T-lock clearance.**
The arm tab T-lock must have `TabClearance` (0.2 mm per side) of clearance
in the T-slot pocket. Too tight: tabs cannot be inserted without force,
risking PCCF damage. Too loose: lateral play at the arm root degrades frame
stiffness. Print Coupon 8 to validate fit on your specific printer before
printing full PCCF layers. → [[coupon-validation]]

**Pi bay — mandatory on all builds.**
The Pi bay (72 × 38 × 6 mm internal) is integral to the Platform and must
be present on every build. It raises the payload mast surface by 6 mm above
the Backplane surface. All mast height calculations must account for this.
A Platform without the Pi bay is not a valid libdrone Platform.
→ [[variable-table-values]] Section 15.

---

## Reference

### Parts list and FreeCAD body map

| Part | Body name | Material | Qty | Critical constraints |
|---|---|---|---|---|
| Arm shaft | `Body_ArmShaft` | PETG | 4 + 2 spare | Vertical print; pinch slit present; rod channels at correct Z offsets |
| Arm tab | `Body_ArmTab` | PETG | 8 | T-lock clearance per Coupon 8; thickness = SandwichHeight exactly |
| Arm cover active | `Body_ArmCoverActive` | PETG | 4 | Dovetail groove; MR30 cable pass-through |
| Arm cover passive | `Body_ArmCoverPassive` | PETG-CF | 4 | O-ring boss geometry; motor nyloc pockets |
| X body PCCF layer | `Body_XBodyPCCF` | PCCF | 3 | Rod channels clearance; T-slot pockets; sandwich bolt pattern |
| X body PETG bottom | `Body_XBodyPETGBottom` | PETG | 1 | Rod channels interference fit (2.1 mm); sandwich bolt pattern |
| X body PETG top | `Body_XBodyPETGTop` | PETG | 1 | Clean structural surface; no cable features |
| Platform | `Body_Platform` | PETG | 1 | GX12 D-D bores; wire channels; Pi bay; battery rail; fan slot |
| Backplane | `Body_Backplane` | PETG | 1 | Lattice geometry; GX12 holes; attachment post bosses |
| GPS / camera bracket | `Body_GPSBracket` | PETG | 1 | Arc slot for camera tilt (0–30°); GPS pocket; bracket mount holes |
| Camera tilt plate | `Body_CameraTiltPlate` | PETG | 1 | Camera slot 19×19 mm (HDZero ±0.5 mm) |
| ASA bumper | `Body_Bumper` | ASA | 4 + 4 spare | Geometry-compensated hollow tip; UV-stable |

### Recommended modelling sequence

Model in this order — each part provides geometry references for the next,
and the sequence follows the physical assembly order:

1. **Variable spreadsheet** — run the macro, verify all aliases, spot-check
   three values. Do not model anything until this is clean.
2. **X body PETG bottom** — establishes the sandwich Z origin and rod channel
   interference geometry. The reference part for all other sandwich layers.
3. **X body PCCF layers** (all three identical) — rod channel clearance, T-slot
   pockets, sandwich bolt pattern. Coupon 8 and 8b must pass before printing.
4. **X body PETG top** — clean structural surface. No cable features in V2.4.6.
5. **Arm tab** — T-lock geometry, thickness must equal SandwichHeight exactly.
6. **Arm shaft** — rod channels matching body Z offsets, pinch slit, motor
   head bore pattern, dovetail groove, MR30 strain relief.
7. **Arm cover active** — dovetail fit over arm shaft, MR30 pass-through.
8. **Arm cover passive** — O-ring boss geometry, motor nyloc pockets.
9. **ASA bumper** — arm tip geometry.
10. **Platform** — the most complex part. GX12 D-D bores, Pi bay, battery
    rail, wire channels, fan slot, mast bosses. Coupons 10 and 11 must pass
    before printing.
11. **Backplane** — lattice geometry, attachment post boss rings, GX12 holes.
12. **GPS / camera bracket** — arc slot mechanism, GPS and camera pockets.
13. **Camera tilt plate** — camera slot, pivot hole, arc slot companion.
14. **Assembly** — verify rod clearance, backplane engagement, GPS mast height.
15. **STL export** — correct orientation per part, 0.01 mm deviation.

### Coupon gates — do not skip

Four coupons are critical-path. Print and pass them before the production
parts they protect:

| Coupon | Tests | Blocks |
|---|---|---|
| 8 — T-lock fit | Tab slides into T-slot: light hand pressure, zero lateral play | All PCCF layers and arm tabs |
| 8b — Rod interference | 2.1 mm channel grips 2 mm CF rod firmly | PETG bottom layer |
| 10 — GX12 D-D bore | Connector fits, does not rotate, nut threads, wire bundle passes | Platform |
| 11 — Battery rail | Battery slides in and out cleanly, strap passes | Platform |

Full coupon specifications and adjustment instructions: → [[coupon-validation]]

### Assembly checks

After modelling all parts, build the Assembly and verify:

1. **Rod clearance** — CF rod paths do not intersect the FC/ESC stack footprint
2. **Backplane boss engagement** — boss rings seat fully on Platform chimney posts
3. **GPS mast height** — mast top ≥ 10 mm above prop tip arc in side view

→ [[freecad-assembly-workbench]]

### STL export

→ [[stl-export-and-slicer-setup]] contains the complete export list, deviation
setting (0.01 mm), and correct print orientation per part. The arm shaft
orientation (vertical) is the most critical — wrong orientation produces a
structurally deficient part regardless of all other settings.

---

## Procedure

### Getting started

1. Install FreeCAD 1.1 stable: https://www.freecad.org/downloads.php
2. Clone or download the repo: https://github.com/libdrone/libdrone
3. Copy `hardware/LD_V300_Variables.FCMacro` to your FreeCAD Macro folder:
   - macOS: `~/Library/Preferences/FreeCAD/Macro/`
   - Linux native: `~/.FreeCAD/Macro/`
   - Linux Flatpak: `~/.var/app/org.freecad.FreeCAD/data/FreeCAD/1.1/Macro/`
   - Windows: `%APPDATA%\FreeCAD\Macro\`
4. Create a new FreeCAD document. Tools → Macros → Run `LD_V300_Variables`.
5. Verify the Variables spreadsheet appears with all aliases populated.
6. Set preferences once: CAD navigation, mm/kg/s units, 3 decimal places.
   → [[freecad-document-setup]]

### If you get stuck on the geometry

Every part has a reference article in the corpus with the engineering rationale
behind its geometry. If a dimension or feature seems arbitrary, read the article
— it almost certainly explains why. Key articles:

- Frame overview: → [[frame-structure-overview]]
- Sandwich structure and layer order: → [[sandwich-structure]]
- CF rod architecture and Z offsets: → [[cf-rod-architecture]]
- Arm shaft as structural fuse: → [[arm-shaft]]
- GX12 connector standard: → [[gx12-connector-standard]]
- Floating motor mount O-ring geometry: → [[floating-motor-mounts]]

If the article doesn't answer the question, open a GitHub issue — it may be
a documentation gap worth filling.

### Contributing back

A zip file with the `.FCStd` and exported STLs is a perfectly valid first
contribution. Open a GitHub issue at https://github.com/libdrone/libdrone
and attach the files, or describe your approach and ask for a review before
investing significant time.

For the full contribution workflow: → [[contributing-guide]]

All contributed CAD work is released under CERN OHL-S v2. Your payload
designs are yours — the copyleft applies only to modifications of the
platform hardware itself.

---

## Rationale

The existing FreeCAD skeleton (→ [[sk-freecad-build-guide]]) is written for
a builder learning FreeCAD while building libdrone. It explains FreeCAD
concepts, references the Cookbook for click-maps, and guides someone through
the learning process. An experienced FreeCAD contributor does not need that
— they need a project brief: what to build, what constraints to respect, and
where to find the specification. This skeleton provides that brief without
the learning scaffolding.

Separating the two audiences also future-proofs the corpus: as FreeCAD
versions change, the click-map content (freecad-ui-110, the Cookbook) needs
updating, but this contributor brief remains stable because it references
engineering constraints, not UI interactions.

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
leads_to:
  - [[contributing-guide]]
  - [[freecad-assembly-workbench]]
  - [[stl-export-and-slicer-setup]]
