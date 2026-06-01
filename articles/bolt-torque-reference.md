---
id: bolt-torque-reference
title: "Bolt torque reference"
version: 1.0.0
date: 2026-04-15
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

Every fastener in the libdrone frame has a specified torque. Under-torquing
allows micro-movement that loosens joints and transmits vibration. Over-torquing
crushes printed material, strips threads, or pre-stresses parts past their
design limit. The most dangerous fastener in the build is the M3 sandwich bolt
— it holds the entire five-layer body together, and over-torquing it cracks
PCCF layers. This article is the single reference for all libdrone fastener
torques. Consult it during initial assembly and whenever any bolt is touched
during maintenance.

---

## Concept

### Why printed materials need lower torques than metal

A bolt torqued into metal compresses a stiff, elastic material — the
compression stores energy and maintains clamping force indefinitely. A bolt
torqued into a printed PETG or PCCF bore compresses a viscoelastic material
that creeps slowly under sustained load. This means:

1. Over-torquing produces immediate cracking — the printed walls around
   the hole cannot sustain the hoop stress.
2. Even correct torques experience some relaxation over time — check and
   re-torque at the maintenance intervals in → [[scheduled-maintenance]].
3. Loctite 243 (medium strength) on fasteners into printed plastic
   compensates for relaxation without preventing future removal.

The torques below assume standard M2/M3/M5 steel bolts into printed PETG
or PCCF without threaded inserts, unless otherwise noted.

---

## Reference

### Master fastener torque table

| Fastener | Location | Torque | Notes |
|---|---|---|---|
| M5 prop nut | Motor shaft | Snug + ¼ turn | Tighten in motor spin direction; do not over-torque shaft |
| M3 motor screws | Into passive cover + nyloc nut | 0.4–0.5 N·m | See → [[floating-motor-mounts]] |
| M3 sandwich bolts | Through all 5 X body layers | 0.3 N·m | Do NOT exceed — crushes PCCF |
| M3 pinch slit bolt | Arm rod clamp | Gradual tighten until rod play gone | Check acoustic ping after — see → [[pre-tensioning]] |
| M3 GPS mast screws | Into backplane boss pads | 0.3 N·m | |
| M3 payload mast screws | Into platform boss pads | 0.3 N·m | Finger-tight + ¼ turn acceptable |
| M3 GX12 chimney lock | Connector lock ring | Finger-tight only | Screw-lock — do not use tools |
| M2 shaft-to-tab screws | Arm shaft onto tabs | Finger-tight + ¼ turn | 4 screws per arm; do not crush PETG |
| M2 active/passive cover screws | Arm covers | Finger-tight + ⅛ turn | These are short — strip easily |

### Loctite application

Apply Loctite 243 to all fasteners that thread into printed plastic:
M3 sandwich bolts, M2 shaft-to-tab screws, M3 pinch slit bolts. Do not
apply to M5 prop nuts (must be removable for prop changes) or GX12 lock
rings (field-removable connectors).

Allow 20 minutes cure before applying torque. Full cure: 24 hours.

### Re-torque schedule

| Fastener group | First re-torque | Subsequent interval |
|---|---|---|
| Sandwich M3 | After first 5 flights | Every 20 flights |
| Motor M3 | After first 5 flights | Every 10 flights |
| Shaft-to-tab M2 | After first crash | Every 20 flights or any crash |
| Pinch slit M3 | After acoustic ping failure | As needed |

---

## Procedure

### Torque sandwich bolts correctly

1. Thread all 6 sandwich bolts finger-tight first — do not torque any
   individual bolt fully before the others are started.
2. Tighten in diagonal pairs to distribute compression evenly: 2 opposing
   corners → opposite 2 corners → front/rear pair.
3. Stop at 0.3 N·m on a torque driver. If a bolt feels significantly
   looser than the others at this torque, the threaded hole may be stripped —
   inspect before proceeding.
4. Verify no PCCF cracking visible at bolt holes under magnification.

### Check pinch slit torque

The pinch slit bolt has no fixed torque because it is set by feel:
tighten gradually, checking rod play after each quarter-turn. Rod play
is confirmed gone when the rod cannot rotate under 0.5 N·m applied
by hand. Do not continue past this point — further torque crushes the
slit walls. Verify with acoustic ping: → [[pre-tensioning]].

---

## Rationale

A consolidated torque reference was created because fastener torques were
previously scattered across DMOM §2.5.1, the arm-shaft atom Procedure section,
and the floating-motor-mounts Reference section. A builder assembling the frame
from scratch needed to consult three documents for complete torque coverage.
A single lookup table eliminates the risk of missed fasteners and gives workshop
participants a printable reference card for the build session.

---

## Connections

requires:
  - [[frame-structure-overview]]
related:
  - [[arm-shaft]]
  - [[floating-motor-mounts]]
  - [[sandwich-structure]]
  - [[pre-tensioning]]
  - [[scheduled-maintenance]]
  - [[corrective-maintenance]]
leads_to:
  - [[pre-tensioning]]
  - [[scheduled-maintenance]]
