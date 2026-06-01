---
id: airframe-integration
title: "Airframe integration"
version: 1.0.0
date: 2026-04-12
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

Airframe integration assembles the printed and purchased structural components
into a complete airframe ready for electronics installation. The sequence is
fixed: tabs into PCCF T-slots, CF rods through all five sandwich layers
simultaneously (self-aligning), sandwich bolts torqued, Platform fitted on
posts, arm shafts attached to tabs, floating motor mounts installed, GPS/camera
bracket mounted. EMC geometry must be verified before assembly begins — three
features enforce wire discipline physically, and missing geometry cannot be
retrofitted after assembly. Total duration: approximately 6 hours.

---

## Concept

### Why sequence is mandatory

The assembly sequence is not arbitrary. CF rods thread through all five layers
simultaneously — this is the alignment step. If any layer is out of position
when the rods are threaded, the error is locked in. Sandwich bolts torque
before arm shafts attach because the rod pre-tension is set by the rod-to-
channel fit in the PETG layer, not by bolt torque. Floating motor mounts
install before electronics to avoid having to work around wiring.

### EMC geometry gates

Three features in the printed parts enforce EMC wire discipline:

1. **Arm shaft dovetail groove** (bottom face) — twisted motor phase wires
   route here and are held by the active cover. Missing groove = no defined
   wire path = wires routed wherever they fit.
2. **Platform signal channel** (left, X = −20 mm) and **power channel**
   (right, X = +20 mm) — physical walls separate signal and power wiring.
   Missing channels = no separation = EMC compromise.
3. **Battery lead relief notch** — twisted battery leads drop through this
   notch to the ESC pads without a sharp bend. Missing notch = strained leads.

If any of these features are absent from printed parts, reprint before
proceeding. The EMC benefit is zero without the geometry.

---

## Reference

### Integration sequence

| Step | Action | Gate |
|---|---|---|
| 4.1 | Slide 8 arm tabs into T-slots of bottom PCCF layer. Stack middle and top PCCF. Thread 4 × 333 mm CF rods through all 5 layers simultaneously. Fit Platform on posts (3× M3). | Rods ring on acoustic ping test (2.2–2.6 kHz) |
| 4.2 | Install floating motor mounts: O-rings in counterbores, sleeves in bores, M3 × 20 mm screws, nyloc nuts captured in passive cover. | Torque 0.4–0.5 N·m; passive cover clears arm head except at O-ring bosses |
| 4.3 | Pinch slit M3 bolts: tighten until zero rod play by hand feel. | Acoustic check 2.2–2.6 kHz. Above 2.6 kHz before zero play = STOP, investigate |
| 4.4 | Install FC/ESC stack on X body top surface on standoffs. | Mechanical fit only at this stage — no wiring yet |
| 4.5 | Verify mast boss pad positions accessible. Test Coupon 5 mast base. | M3 screw in/out cleanly |
| 4.6 | Frame hand-twist check. | No visible flex |
| 4.7 | Connect arm shafts to tabs: 2× M2 per tab, 16 screws total. | Finger-tight — do not overtighten in PETG |
| 4.8 | Mount GPS/camera bracket at Platform nose (+50 mm, 2× M3). GPS arrow pointing forward, patch antenna clear sky view above bracket. VTX mounts separately in electronics zone (−104 to −133 mm). | Clear sky view from directly above GPS patch |
| 4.9 | Install battery strap through Platform rail slots. Test fit with 6S pack — side-slide RIGHT, seats against left endstop. | Battery fully seated, strap buckle accessible |

### Acoustic ping reference (CF rods)

| Sound | Interpretation |
|---|---|
| Clear ring, sustains > 0.5 s | Rod correctly pre-tensioned |
| Dull thud | Rod loose — check channel diameter (PETG core zone must be 2.1 mm) |
| Above 2.6 kHz before zero rod play | Over-tensioning risk — stop and investigate channel interference |

---

## Procedure

### CF rod threading (step 4.1 detail)

1. Stack all five layers in correct order on a flat surface: PETG bottom, 3×
   PCCF, PETG top. Align T-slots by eye — arm tabs should already be in the
   bottom PCCF layer before stacking the middle and top PCCF layers.
2. Thread Rod 1 from one end, guiding each layer into alignment as you push.
   The rod tip does the alignment work — let it find the channel on each layer.
3. Repeat for Rods 2, 3, 4. The fourth rod locks all layers simultaneously.
4. Verify all rod ends protrude equally from both ends of the sandwich.
5. Acoustic ping all four rods. All must ring.
6. Fit Platform on top: seat on the three M3 post pairs at Y = +39, −39, −148 mm.

### Floating motor mount installation (step 4.2 detail)

See [[floating-motor-mounts]] for the complete procedure. Key check: after all
four motors are installed, slide a 0.1 mm feeler gauge around the perimeter
of each passive cover. It should pass freely everywhere except at the O-ring
contact zones. Any direct contact = passive cover is touching the arm head = 
isolation is bypassed.

---

## Rationale

### Why rods thread all five layers simultaneously rather than layer-by-layer

Threading each layer separately means each layer's position is set independently.
Small angular errors between layers accumulate. Threading all five simultaneously
means each rod tip finds and aligns all layers as it passes through — the rods
enforce co-planarity by geometry. This is the mechanism that makes the assembly
self-aligning without measurement fixtures.

### Why arm shafts attach after sandwich bolts are torqued

The sandwich bolt torque sets the compression on the PCCF layers and the
pre-tension on the CF rods. If arm shafts were attached first, attaching the
shafts would constrain the T-slot position before the sandwich was fully
settled. Torquing the sandwich bolts with arm shafts attached risks
over-constraining the tab geometry.

---

## Connections

requires:
  - [[sandwich-structure]]
  - [[cf-rod-architecture]]
  - [[arm-shaft]]
  - [[floating-motor-mounts]]
  - [[coupon-validation]]
related:
  - [[failure-hierarchy]]
  - [[emc-noise-sources]]
  - [[power-signal-separation]]
leads_to:
  - [[electronics-installation]]
