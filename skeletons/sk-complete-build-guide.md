---
id: sk-complete-build-guide
title: "Complete Build Guide"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 1.builder
platform:
  - pro
lang: en
licence: CC BY-SA 4.0
---

## Summary

After following this guide, the builder has a flyable, calibrated libdrone Pro
with Blackbox enabled, maiden flight logged, and the build documented. This
skeleton is the direct replacement for the V2.4.6 WBS — it is the complete
builder traversal from Day 0 to maiden, navigating through the atoms in the
correct sequence with the connecting rationale.

---

## Concept

### Before you begin

The build takes approximately 25–30 hours of active work over 10–14 days —
primarily waiting for prints and AliExpress delivery, not continuous effort.
The most important thing to do first is read this entire guide before touching
any component. Surprises on Day 12 are caused by information not absorbed on
Day 0.

→ [[prep-and-parametrics]] explains why documentation assembly and FreeCAD
variable entry come before any physical work. The parametric model is the
single source of truth: one wrong variable propagates silently into every
printed part. Read → [[variable-table-values]] and keep it open throughout.

### Phase 0 — Procurement

Order on Day 1 without exception. AliExpress takes 10–15 days; that window is
the printing window. → [[procurement]] contains the full BOM with MoSCoW priority
ratings, supplier links, and a day-by-day order sequence. The most critical
item to order first: O-rings, motors, capacitors, MR30 connectors. Czech hobby
suppliers (HobbyDrone.cz, RCStudio.cz) should be ordered the same day.

### Phase 1 — Coupons and structural validation

Before printing a single production part, validate the critical fits.
→ [[coupon-validation]] explains the coupon system: small test prints that
verify geometry before committing to a 4-hour structural print. Coupon 8
(T-lock fit) gates the entire PCCF production run. Coupon 8b (rod interference
fit) gates the pinch bolt adjustment. Do not skip the coupons — they exist
because the geometry is tight and printer calibration varies.

### Phase 2 — Production print run

→ [[print-production]] covers the full printing sequence: PCCF layers first
(highest failure risk, requires hardened nozzle), then PETG arm shafts
(vertical orientation, 3.5 hours each), then bumpers and accessories.
Total: approximately 38 print hours over 5 days. → [[print-profiles]] contains
the PrusaSlicer settings that matter. → [[stl-export-and-slicer-setup]] covers
the FreeCAD export workflow before slicing begins.

The post-processing step — heat-gun treatment and epoxy wipe-coat on all
structural PCCF and PETG parts — runs after all parts are printed and before
assembly begins. Do not skip: it seals surface porosity and significantly
improves delamination resistance.

### Phase 3 — Airframe integration

→ [[airframe-integration]] is the Phase 4 assembly sequence. The order is fixed
and matters: tabs into T-slots, then CF rods through all five layers
simultaneously (they self-align), then Platform on posts, then motor mounts,
then acoustic ring verification.

Understanding why each step happens in this order requires → [[sandwich-structure]]
(the composite geometry), → [[cf-rod-architecture]] (why simultaneous threading
is the alignment mechanism), and → [[floating-motor-mounts]] (the O-ring
isolation system that the entire vibration strategy depends on).

Three EMC geometry features must be verified in FreeCAD before printing the
Platform — → [[power-signal-separation]] explains what they are and why missing
geometry cannot be retrofitted after assembly.

### Phase 4 — Electronics installation

→ [[electronics-installation]] is the Phase 5 wiring sequence. Read it fully
before soldering anything, because every wire must be routed to its final
position before the FC/ESC stack is bolted down.

The EMC rules govern every routing decision. → [[star-grounding]] (one ground
point, no loops), → [[twisted-pairs]] (motor phase wires, battery leads, I2C
pairs), → [[capacitor-placement-emc]] (1000µF directly on ESC pads, no pigtail
wire), → [[power-signal-separation]] (LEFT channel for signal, RIGHT for power).

Conformal coating is mandatory before first power-on — → [[conformal-coating]]
explains the application sequence and why it must happen after all soldering
is complete.

For the payload connectors: → [[gx12-connector-standard]] covers the D-D bore
that prevents rotation, the double-nut retention, and why all 12 wires must be
soldered to the FC before the Platform top layer is placed.

### Phase 5 — Software commissioning

→ [[software-commissioning]] is the Phase 6 configuration sequence. The order
of layers is fixed: EdgeTX transmitter model first, then Betaflight, then AM32
ESC, then HDZero VTX and goggles.

The Betaflight configuration is applied via CLI diff, not manual GUI entry —
→ [[betaflight-setup]] contains the exact diff and the UART assignment table.
→ [[betaflight-profiles]] covers the two PID profiles (standard and low-speed
A2 compliance). → [[betaflight-gps-rescue]] covers the GPS Rescue configuration
— particularly the return altitude, which must be set for each new deployment
site. → [[edgetx-model]] covers the TX16S model setup and switch assignments.

The low-speed mode calibration is an outdoor step that cannot be done on the
bench: → [[betaflight-profiles]] explains the calibration procedure. Target:
GPS speed ≤ 4.8 m/s at full throttle.

Commit a complete configuration backup to the repository before the maiden.

### Phase 6 — Acceptance validation and maiden flight

→ [[acceptance-validation]] is the gate before the maiden. Hard gates: mass
budget within EASA A2 limit, GPS fix ≥ 8 satellites, motor directions correct.
If any hard gate fails, do not proceed.

→ [[maiden-flight]] treats the first flight as a measurement event, not a
celebration. Phase 1 is hover-only at 1m for 30 seconds. After landing:
feel the motors, check the T-locks, download Blackbox. Phase 2 expands to
slow circuits and a GPS Rescue test only after Phase 1 inspection confirms
the build is within spec.

→ [[blackbox-analysis]] is the final step: open the Blackbox trace in the
Explorer, verify the gyro noise floor is below −40 dB, verify the RPM filter
is removing motor harmonics, verify the time trace shows 1–2 oscillation
cycles settling after sharp inputs. The maiden Blackbox is the reference
baseline for every future diagnostic.

---

## Reference

### Build phase summary

| Phase | Key article | Duration | Gate |
|---|---|---|---|
| 0 — Prep & procurement | [[prep-and-parametrics]], [[procurement]] | Day 0–1 | AliExpress ordered |
| 1 — Coupons | [[coupon-validation]] | Day 2–4 | Coupon 8 T-lock pass |
| 2 — Print production | [[print-production]], [[print-profiles]] | Day 5–10, ~38 hrs | All parts post-processed |
| 3 — Airframe integration | [[airframe-integration]] | Day 11–14, ~6 hrs | Acoustic ring 2.2–2.6 kHz |
| 4 — Electronics installation | [[electronics-installation]] | Day 15–18, ~10 hrs | Conformal coat cured |
| 5 — Software commissioning | [[software-commissioning]] | Day 19–23, ~6 hrs | Config backup committed |
| 6 — Acceptance + maiden | [[acceptance-validation]], [[maiden-flight]] | Day 24–25 | Blackbox review complete |

---

## Procedure

### How to use this guide

This is not a step-by-step instruction set — each linked atom contains the
detailed steps. This guide provides the sequence and the rationale for that
sequence. Before starting each phase: read the linked atom completely. Then
execute. Do not read and execute simultaneously for the first time.

---

## Rationale

The WBS (V2.4.6) was a single document containing all build phases. Every
specification, torque value, and wiring rule lived in that document. When a
specification changed, the WBS had to change. This skeleton delegates all
specifications to atoms — this document provides only the sequence and
context. A changed O-ring specification propagates to the floating-motor-mounts
atom; this skeleton does not need to change.

---

## Connections

requires: []
related:
  - [[sk-engineering-101]]
  - [[sk-workshop-handout]]
  - [[sk-operations-manual]]
leads_to:
  - [[sk-operations-manual]]
