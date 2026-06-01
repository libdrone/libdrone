---
id: cf-plate-arms
title: "CF plate arms"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: libdrone
topic:
  - manufacturing
personas:
  - 1.builder
  - 8.architect
platform:
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

CF plate arms are the structural arm architecture used on Ghost. Where Pro,
Bandit, and Core use 3D-printed polymer arms that clamp onto CF rods, Ghost
uses arms fabricated from 2 mm 3K carbon fibre flat sheet — two plates per
arm, sandwiching and clamping onto the existing 3 mm CF rod system. This
architecture provides the structural stiffness required to carry 12-inch
propellers at the 540 mm wheelbase without the arm flex that would cause
vibration at low RPM. Arms are not 3D-printable by the community but are
field-repairable without tools: unclamp, slide new plates on, reclamp.
Fabrication uses the same DXF workflow as the rest of the libdrone system.

---

## Concept

### Why not print at this scale

The 3D-printed arm architecture used on smaller variants works because
the arm length (from rod clamp to motor mount) is short enough that PETG
or PC-CF provides adequate stiffness. Ghost's 12-inch prop class requires
an arm length of approximately 190–210 mm from body centre to motor centre.
At this span, printed polymer arms flex enough under the gyroscopic precession
loads of a 12-inch propeller to produce measurable vibration — the same
vibration that couples into the IMU and degrades flight controller stability.

Flat carbon fibre plate resists bending in its plane. A 2 mm 3K CF plate at
37 mm width and 210 mm length is approximately 15× stiffer in bending than
an equivalent PETG arm cross-section. The stiffness allows Ghost's low-RPM
propulsion to produce a clean vibration profile.

### The two-plate sandwich

Each Ghost arm is two identical CF plates, one above and one below the CF rod.
M3 bolts through both plates and the rod clamp recess provide clamping force
that locks the arm geometry. The 3 mm CF rod runs through a semi-circular
channel cut into the inner face of each plate; the clamping force around the
rod replaces the printed rod channel used on polymer arms.

Using two identical plates reduces the DXF complexity to a single profile cut
eight times (four arms × two plates). The plates are interchangeable — no
left/right distinction. See → [[cf-rod-architecture]] for the rod system that
Ghost shares with the rest of the family.

### Field repair

Arm replacement on Ghost requires no tools beyond an M3 hex driver. Procedure:
loosen the M3 clamp bolts on the damaged arm, slide the plates off the rod,
slide replacement plates on, retighten. Replacement takes under 15 minutes in
the field. Plate stock is flat sheet — it can be carried as pre-cut spares
or fabricated from a DXF file at any laser cutting service.

---

## Reference

| Parameter | Value |
|---|---|
| Plate material | 2 mm 3K carbon fibre woven sheet |
| Plates per arm | 2 (top + bottom, identical) |
| Plate width | ~37 mm (varies by arm station) |
| Arm length | ~210 mm (body centre to motor centre) |
| Rod interface | 3 mm CF rod semi-circular channel |
| Fabrication | Laser cutting or waterjet from DXF |
| DXF file | `ghost_arm.dxf` (planned — see Ghost §18) |
| Clamp fasteners | M3 × 10 mm, 3 per arm position |
| Finish | Raw CF; no coating required |

**Mass estimate:** 8 plates × ~15 g = ~120 g total arm structure.

**Fabrication note:** Ghost arm DXF is planned but not yet produced as of
v0.2. Plates can be hand-cut from 2 mm CF sheet using the geometry in Ghost
Spec §6 as a reference until the DXF is available.

---

## Procedure

### Install a CF plate arm on Ghost

1. Cut 2 plates per arm from 2 mm CF sheet to the `ghost_arm.dxf` profile.
   Deburr all edges with 220-grit sandpaper.
2. Slide one plate below and one above the CF rod at the arm station.
3. Align the semi-circular rod channels around the rod.
4. Insert M3 × 10 mm bolts through the plate stack and rod clamp holes.
5. Apply Loctite 243 to bolt threads. Torque to 0.5 N·m.
6. Mount motor to the motor-end plate holes using M3 × 8 mm bolts with
   nylon washers to protect the CF surface.
7. Verify arm is perpendicular to the body axis (measure motor-to-motor
   diagonal to confirm geometry).

### Replace a damaged arm in the field

1. Remove motor from the damaged arm (4× M3 bolts).
2. Loosen arm clamp bolts (3× M3 per arm position).
3. Slide damaged plates off the CF rod.
4. Slide replacement plates onto rod. Retighten clamp bolts.
5. Reinstall motor. Verify geometry before flight.

---

## Rationale

The two-plate identical profile was chosen over a single thicker plate
or a machined arm because it eliminates the top/bottom distinction and
reduces the number of unique parts to one. A single 2 mm plate would need
to be 3–4 mm thick to achieve equivalent bending stiffness, increasing
mass and cost. A machined arm offers no stiffness advantage over flat plate
for the loads on Ghost, while costing significantly more and requiring a
machine shop rather than a laser cutter.

---

## Connections

requires:
  - [[cf-rod-architecture]]
  - [[frame-structure-overview]]
related:
  - [[ghost-variant]]
  - [[sandwich-structure]]
  - [[floating-motor-mounts]]
  - [[stl-export-and-slicer-setup]]
leads_to:
  - [[ghost-variant]]
  - [[acoustic-signature-design]]
