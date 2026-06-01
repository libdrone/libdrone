---
id: sandwich-structure
title: "Sandwich structure"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - frame-structure
personas:
  - 1.builder
  - 4.workshop
  - 5.student
  - 7.contributor
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The libdrone X body is a five-layer printed sandwich: PETG bottom, three PCCF
structural layers, PETG top, bonded only by four CF rods and eight M3 bolts —
no adhesive. The PCCF layers carry all structural load in bending and
compression. The PETG layers are the impact face at the bottom and the clean
attachment surface at the top. Four CF rods thread continuously through all
five layers, simultaneously aligning them during assembly and pre-tensioning
the structure in compression. The T-slot pockets in the PCCF layers engage arm
tabs via a mechanical T-profile lock; arm shafts are replaceable without
disturbing the sandwich.

---

## Concept

### Why a sandwich and not a flat plate

A classic flat-plate frame is a continuous surface: impact force from one arm
propagates across the full plate into all other arms and into the electronics
without interruption. The sandwich introduces a deliberate discontinuity.
The X body has gaps between the arm extension zones — force must pass through
a narrow transition at the junction with the core. Energy dissipates along
the transition length instead of propagating freely.

In aerospace sandwich panels, the face sheets carry bending loads while the
core carries shear. In libdrone the PCCF layers are both the core and the
structural face — they are stiff enough to carry bending directly. The PETG
layers serve different functions (impact absorption at bottom, clean surface
at top) rather than acting as sandwich face sheets in the classical sense.

### Pre-tensioning via CF rods

Threading CF rods through all five layers and pressing them into the
interference-fit channels in the PETG bottom layer places the core zone
under slight radial compression. The sandwich is held in tension by the
rod-to-channel fit. A pre-tensioned joint transmits load immediately with
no slack — there is no micro-movement before the joint activates. For the
gyroscope this means frame flex that would otherwise appear as vibration
noise cannot occur: geometry is locked by the rods under load.

The rod fit in the PCCF layers uses a standard 2.2 mm channel (clearance fit
for a 2.0 mm rod). Only the PETG bottom layer uses 2.1 mm (interference fit).
PCCF is too brittle for interference fit — an over-tight channel in PCCF risks
micro-cracking the channel wall on rod insertion.

### T-slot arm attachment

Each PCCF layer carries four T-slot pockets, one per arm, cut at 45° through
the arm extension zone. A T-profile tab printed as part of the arm slides into
the slot from the outside — the T-lock prevents the tab from pulling out under
lateral load or crash impact. No adhesive is used. The tab is captive in the
slot by geometry alone. This allows arm shafts to be field-replaced in minutes
without opening the sandwich.

### Minimum wall rule

Every hole or slot in the sandwich weakens the structure globally, not just
locally. The minimum wall retained between any two features (T-slot, rod
channel, bolt hole, lightening pocket) is 3.0 mm — equal to the diameter of
the largest fastener. Violating this rule in any layer risks crack propagation
under crash load.

---

## Reference

### Layer specification

| Layer | Material | Thickness | Target mass | Key features |
|---|---|---|---|---|
| 1 — PETG bottom | PETG | 3 mm | 7.0 g | Rod interference fit (2.1 mm channels), M3 nut capture pockets, impact face |
| 2 — PCCF mid-lower | PCCF | 3 mm | 9.0 g | T-slot pockets, rod channels (2.2 mm), sandwich bolt holes |
| 3 — PCCF mid-centre | PCCF | 3 mm | 9.0 g | T-slot pockets, rod channels (2.2 mm), sandwich bolt holes |
| 4 — PCCF mid-upper | PCCF | 3 mm | 9.0 g | T-slot pockets, rod channels (2.2 mm), sandwich bolt holes |
| 5 — PETG top | PETG | 4 mm | 18.0 g | Stack pattern, platform attachment holes, clean structural surface |

Total sandwich: 16 mm height, 52.0 g target.

### Rod positions

Four CF rods at fixed Z offsets. The offset pair (outer/inner) is mirrored
between front/rear arms and left/right arms so that rods trace an X through
the core:

| Position | Z offset |
|---|---|
| Outer pair | +5.0 mm and +2.0 mm (FL/RR arm side) |
| Mirrored | −5.0 mm and −2.0 mm (FR/RL arm side) |

The four distinct heights (+5, +2, −2, −5 mm) ensure each rod occupies a unique
Z plane across all five layers. Channels must align across all layers — the rod
serves as an assembly alignment tool as well as a structural element.

### Fasteners

| Fastener | Qty | Specification | Torque |
|---|---|---|---|
| Sandwich bolts | 8 | M3 × 20 mm stainless, through all 5 layers | 0.3 N·m |
| Sandwich nuts | 8 | M3 hex, captured in PETG bottom layer pockets | — |

Bolt pattern: 8 bolts total. Four corner positions at (±18, ±18 mm) and four
axis positions at (0, ±22 mm) and (±22, 0 mm) — confirmed V2.4.5 pattern.
Torque: firm but not crushing. Over-torquing the PCCF layers causes micro-cracking
around the bolt holes.

### T-slot geometry

| Parameter | Value |
|---|---|
| Slot width | `#TabWidth + 0.2 mm` clearance per side |
| Slot depth | `#TabLength` from outer edge inward |
| T-lock height | matches tab T-extension |
| Engagement depth | 20 mm minimum |
| Minimum wall to adjacent feature | 3.0 mm |

---

## Procedure

### Assembly sequence (sandwich only)

1. Insert all 8 arm tabs (2 per arm) into T-slots in the bottom PCCF layer.
   Slide from the outside. Verify the T-lock is fully engaged — there should
   be zero lateral play.
2. Place the centre PCCF layer. Align rod channels and sandwich bolt holes.
3. Place the top PCCF layer. Align all features.
4. Thread all four CF rods through the entire five-layer stack simultaneously.
   Insert from the PETG bottom layer side (interference fit end). A firm press
   is normal at the 2.1 mm section. Use a smooth-ended rod pusher — do not
   hammer. The rods align all layers as a single operation.
5. Place the PETG top layer. Align stack holes and platform attachment holes.
6. Insert M3 hex bolts from below. Thread into captured nuts in the PETG
   bottom layer. Tighten in a cross pattern to 0.3 N·m — firm, not crushing.
7. Connect arm shafts to tabs: 2 × M2 × 6 mm screws per tab, 4 screws per arm,
   16 screws total. Access from the arm shaft tip face.

### Post-crash inspection

1. Inspect the PETG bottom layer for cracks at the rod channel exits and at
   the M3 nut capture pockets.
2. Inspect each T-slot for cracking at the T-lock transition. Any cracking
   in the T-slot zone means the PCCF layer must be replaced.
3. Check all rod channels for visible gap (rod working loose). Re-press if needed.
4. Re-torque sandwich bolts to 0.3 N·m if any movement is felt.

---

## Rationale

### Why three PCCF layers and not one thick PCCF plate

Three 3 mm layers can each be printed in the optimal orientation (flat on the
bed) without print-time dimensional penalties. A single 9 mm PCCF layer would
require either tall-side printing (anisotropic weakness in the bending plane)
or special slicing that produces lower interlaminar strength. Three layers also
allow the T-slot pockets to be distributed in depth across all three, so the
tab engages over the full 9 mm of PCCF depth rather than a shallow 3 mm bite.

### Why PETG bottom and not PCCF bottom

The bottom layer is the first contact surface in a hard landing or crash.
PCCF is stiff but brittle — it shatters under sharp impact. PETG is tough and
absorbs impact energy through controlled deformation. A deformed PETG bottom
layer can be replaced cheaply; a shattered PCCF bottom layer would propagate
crack energy into the T-slot zone. Deliberately using a tougher material at
the impact face is the correct engineering choice.

Analogy: a shoe sole is rubber (tough) not steel (stiff).

### Why no adhesive

Adhesive between sandwich layers would increase peel strength slightly but
would make the sandwich permanent. The current design allows individual layers
to be replaced — if a single PCCF layer cracks, only that layer is reprinted.
Adhesive bonding would turn a three-hour repair into a full structural rebuild.
More critically, adhesive in the T-slot would make the arm tabs permanent,
eliminating field replaceability. → See [[failure-hierarchy]].

### Why 4 mm PETG top layer instead of 3 mm

The top layer carries the platform attachment screws (M3 countersunk) and the
FC/ESC stack standoffs. 3 mm leaves insufficient thread engagement for M3 in
PETG. 4 mm provides 4 full threads of engagement in a clean-hole printed bore.

---

## Connections

requires:
  - [[frame-structure-overview]]
related:
  - [[cf-rod-architecture]]
  - [[arm-shaft]]
  - [[failure-hierarchy]]
  - [[petg]]
  - [[pccf]]
  - [[monocoque-structure]]
  - [[zonal-stiffness]]
leads_to:
  - [[airframe-integration]]
  - [[monocoque-structure]]
