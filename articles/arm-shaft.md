---
id: arm-shaft
title: "Arm shaft"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - frame-structure
personas:
  - 1.builder
  - 2.operator
  - 4.workshop
  - 5.student
  - 7.contributor
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The arm shaft is the weakest structural element in the libdrone frame —
deliberately so. It is a PETG part printed vertically, carrying the motor
head at its tip and two arm tabs at its root. In a crash, the shaft fractures
predictably at the bending cross-section before the T-slot, the PCCF layers,
or the electronics can be damaged. Replacement requires no tools beyond a
2 mm hex key and takes under 5 minutes in the field. This field-replaceability
is the mechanism that keeps crash cost low and fleet uptime high.

---

## Concept

### The arm as a structural fuse

An electrical fuse is deliberately the weakest element in a circuit. When
overloaded, it fails at a known location in a known way, protecting everything
downstream. The arm shaft applies the same principle mechanically. Its
cross-section is sized so that it fails in bending before the tabs, the T-slots,
or the X body core can absorb the crash energy.

The sequence is: **shaft fractures → tab stays → T-slot intact → X body intact
→ electronics alive**. This is not an accident — it is the design intent.
For the sequence to hold, the shaft must be the correct weakest link:
strong enough to carry normal flight loads, weak enough to fracture in a
representative crash before the next element in the chain yields.

### Why PETG and why vertical printing

PETG is tough — it absorbs impact energy through plastic deformation rather
than shattering. A fractured PETG shaft leaves a clean break at the failure
point. PCCF in the same geometry would shatter into multiple fragments,
potentially driving debris into the motor bearings or prop arc.

Vertical printing means the print layers are perpendicular to the main bending
load axis — each layer is oriented to carry tension or compression rather than
shear between layers. This is the strongest orientation for a loaded cantilever.
The result is a shaft that is as strong as possible in normal flight, but still
fails before the PCCF structure, because PETG itself is less stiff than PCCF.

### Split shaft-and-tab design

The arm is two parts: shaft and tabs. They are printed separately in the
orientations optimal for each:

- **Shaft:** printed vertically (layers perpendicular to bending axis). Long,
  thin, loads in bending.
- **Tabs:** printed horizontally (flat on bed). Short, wide, loads in
  compression and shear within the T-slot.

Separating the two parts means each can be printed optimally and replaced
independently. A crashed shaft does not require discarding the tabs (which
are unlikely to be damaged, since the shaft failed first).

---

## Reference

### Geometry

| Parameter | Value | Variable |
|---|---|---|
| Shaft length | ~125 mm (shaft body + motor head) | — |
| Print orientation | Vertical | — |
| Motor head | M3 × 20 mm bolt pattern | — |
| Tab count per arm | 2 | — |
| Rod channels | 2 per shaft, matching sandwich Z offsets | `#RodDiaChannel` |
| Pinch slit | Present — allows rod to be pressed in | — |
| MR30 strain relief | Integral in shaft body | — |

### Mass

    hw_arm_shaft_petg_single_target     = 15.0 g
    hw_arm_shaft_petg_4x_target         = 60.0 g

### Tab geometry

| Parameter | Value | Variable |
|---|---|---|
| T-profile width | `#TabWidth` | see Variables |
| T-profile length | `#TabLength` | see Variables |
| Engagement depth | 20 mm minimum | — |
| Thickness | must equal `#SandwichHeight` | see Variables |
| Screws to shaft | 2 × M2 × 6 mm per tab | — |

    hw_arm_tab_petg_single_target       = 1.5 g
    hw_arm_tab_petg_8x_target           = 12.0 g

### Arm cover — passive (PETG-CF)

The passive cover sits over the arm head and captures the M3 nyloc nuts for
the floating motor mount screws. It must not contact the arm head surface
directly — only through the O-ring bosses. Mass 5.0 g each.

    hw_cover_passive_pccf_single_target = 5.0 g
    hw_cover_passive_pccf_4x_target     = 20.0 g

**FFP3 respirator mandatory when printing PETG-CF (passive cover).**

### Arm cover — active (PETG)

The active cover protects the MR30 motor connector and cable run along the
arm. Retained by dovetail groove and two M2 screws. Removable for motor
connector service.

    hw_cover_active_petg_single_target  = 4.0 g
    hw_cover_active_petg_4x_target      = 16.0 g

### Bumpers (ASA)

Hollow, geometry-compensated sacrificial tip bumpers fit the arm shaft tip.
ASA is specified for UV resistance and thermal stability — bumpers are
externally exposed. They are the first point of ground contact in a landing,
absorbing impact before the arm shaft sees significant bending load.

    hw_bumper_asa_single_target         = 3.0 g
    hw_bumper_asa_4x_target             = 12.0 g

---

## Procedure

### Initial arm installation

1. Verify tab T-profile dimensions against a test T-slot cut in scrap PCCF
   before installing into the sandwich. Tab should slide in without force and
   lock without play. See [[coupon-validation]].
2. Slide both tabs into the T-slot pockets of the bottom PCCF layer, from the
   outside edge. Verify the T-lock is fully engaged — zero lateral play.
3. Proceed with sandwich assembly. → See [[sandwich-structure]].
4. After the sandwich bolts are torqued, attach the arm shaft to its tabs:
   align rod channels, press shaft over the tab bodies, and drive 2 × M2 × 6 mm
   screws into each tab through the shaft side-face holes. Access from the
   arm tip. Torque: finger-tight plus 1/8 turn — do not crush PETG.
5. Fit the active cover (dovetail + 2 × M2 screws).
6. Route MR30 motor connector through the active cover before fitting motor.
7. Fit bumper over arm tip.

### Field shaft replacement (post-crash)

1. Remove motor: undo 4 × M3 motor mount screws. Disconnect MR30 connector.
2. Remove active cover (2 × M2 screws + dovetail release).
3. Remove passive cover (motor mount nyloc nuts exposed after motor removal).
4. Undo 2 × M2 screws in each tab (4 screws total). Slide shaft off tabs.
5. Slide new shaft over tabs. Drive M2 screws. Reinstall covers, motor, bumper.
6. Inspect both tabs for cracking at the T-lock root. If cracking is visible,
   replace the tab. → Tab replacement requires opening the sandwich.

### Tab replacement (rare — crash beyond shaft fracture)

1. Remove arm shaft as above.
2. Loosen all 8 sandwich bolts. Do not fully remove — keep rods engaged.
3. Separate the bottom PCCF layer slightly to release the T-lock.
4. Slide damaged tab outward. Slide new tab inward and engage T-lock.
5. Reassemble sandwich in order. Re-torque bolts to 0.3 N·m.

---

## Rationale

### Why not a carbon fibre arm

Carbon fibre arms are stiffer and lighter for the same cross-section. They
also shatter on impact and are not field-printable. A crashed CF arm requires
sourcing a replacement part — days of downtime. A crashed PETG arm requires
a 2-hour print from filament that is always on-site. For an operational platform
used in field conditions, replaceability dominates over marginal stiffness gain.

### Why the shaft and not the tabs as the fuse

The tabs engage 20 mm deep into the PCCF T-slot and are loaded in shear and
compression by the T-profile. They are inherently stiffer and stronger in the
crash load path than the shaft, which is loaded in bending over a 100+ mm
unsupported length. The shaft fails in bending before the tabs fail in shear —
this is the natural load path, not an arbitrary design choice.

Tabs are also more expensive to replace than shafts: tab replacement requires
partially disassembling the sandwich. Shafts replace without touching the core.
Making tabs the fuse would increase crash repair cost and time.

### Why PETG and not ASA or PLA for the shaft

ASA is UV-stable and used for externally-exposed cosmetic parts (bumpers) but
has lower impact toughness than PETG at low temperatures. PLA is too brittle
and too temperature-sensitive — a PLA shaft in direct summer sun could creep
under sustained load. PETG provides the best combination of toughness,
temperature resistance, and ease of printing for the shaft function.

---

## Connections

requires:
  - [[frame-structure-overview]]
related:
  - [[sandwich-structure]]
  - [[failure-hierarchy]]
  - [[floating-motor-mounts]]
  - [[petg]]
  - asa
leads_to:
  - [[airframe-integration]]
  - [[scheduled-maintenance]]


[coupon-validation]: coupon-validation.md "Coupon validation"
[sandwich-structure]: sandwich-structure.md "Sandwich structure"
[frame-structure-overview]: frame-structure-overview.md "Frame structure overview"
[failure-hierarchy]: failure-hierarchy.md "Failure hierarchy"
[floating-motor-mounts]: floating-motor-mounts.md "Floating motor mounts"
[petg]: petg.md "PETG — properties and libdrone use"
[airframe-integration]: airframe-integration.md "Airframe integration"
[scheduled-maintenance]: scheduled-maintenance.md "Scheduled maintenance"
