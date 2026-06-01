---
id: corrective-maintenance
title: "Corrective maintenance"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - piloting-operations
personas:
  - 2.operator
  - 1.builder
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Corrective maintenance repairs known damage or component failure. Unlike
scheduled maintenance (interval-based), corrective maintenance is triggered
by a finding from the post-flight check or post-crash inspection. The most
common corrective tasks are arm shaft replacement (5 minutes), propeller
replacement (2 minutes), and motor mount O-ring replacement (15 minutes).
The arm shaft is designed to fracture on impact — finding a fractured shaft
is a success of the failure hierarchy, not a build defect.

---

## Concept

### The failure hierarchy as maintenance guidance

libdrone's failure hierarchy deliberately routes crash energy toward the arm
shaft first, protecting the electronics and PCCF layers. When a crash occurs,
the arm shaft is expected to fracture. This is the design working correctly.
Corrective maintenance after a crash therefore focuses on the arm shaft and
motor before inspecting anything deeper.

The hierarchy: bumpers (absorb first impact) → arm shaft (fracture fuse) →
motor (bend or strip threads before transmitting force to PCCF) → PCCF layer
(last resort — structural damage here grounds the drone for full inspection).

A crash where only the arm shaft fractured is a best-case outcome. A crash
where the PCCF layer cracked requires more thorough inspection and is a more
serious airworthiness event.

---

## Reference

### Common corrective tasks and time estimates

| Task | Trigger | Time |
|---|---|---|
| Prop replacement | Any chip, crack, or deformation | 2 min |
| Arm shaft replacement | Lateral play at T-lock, visible fracture | 5 min |
| Motor mount O-ring replacement | Cracking, deformation, or post-crash | 15 min |
| Motor replacement | Non-spinning, hot, or damaged bearing | 20 min |
| Capacitor replacement | Visible damage, cracked body | 30 min (resolder) |
| Conformal coating repair | Chip or peeling after crash or repair | 30 min + 24h cure |

### Arm shaft replacement procedure

1. Remove battery. Disarm. Remove props on the affected arm.
2. Disconnect MR30 motor connector.
3. Remove 2× M2 screws at the arm tab (accessible from the arm root).
4. Slide the arm shaft out of the T-slot along the arm axis.
5. Inspect the T-slot walls for cracking. Run a finger along the inside of
   each wall. Any crack felt or visible → do not reuse this T-slot. Ground
   the drone and consult the repair procedure for PCCF layer replacement.
6. Print a replacement arm shaft (PETG, standard profiles, ~20 minutes).
7. Slide new shaft into T-slot. Verify tab seats fully with no rocking.
8. Install 2× M2 screws finger-tight + 1/4 turn.
9. Reconnect MR30. Install new props on this arm.
10. Acoustic ping: tap the CF rods — all should ring. A rod that thuds has
    loosened — tighten the pinch bolt.

### Motor mount O-ring replacement

→ See [[scheduled-maintenance]] for the complete O-ring replacement procedure.
Corrective replacement after a crash follows the same procedure.

After corrective O-ring replacement, always re-torque the motor mount screws
(0.4–0.5 N·m cross-pattern) and verify the passive cover does not contact
the arm head except at the O-ring contact zones.

### Prop replacement

1. Remove the prop nut (CCW prop = CW nut thread; CW prop = CCW nut thread).
2. Pull the prop straight off the motor shaft.
3. Inspect the motor shaft for bending: roll it on a flat surface.
   Any wobble = bent shaft = motor replacement required.
4. Fit new prop. Torque nut to 0.8–1.0 N·m. Verify prop seated fully.
5. Run balance check on magnetic balancer before first post-replacement flight.

---

## Procedure

### Post-crash triage sequence

Run in this order — stop at the first hard finding:

1. **Props** — visual inspect all 4. Replace any damaged prop before anything else.
2. **Arm shafts** — press each arm laterally. Any play = fractured shaft.
   Replace before continuing.
3. **Motor mount O-rings** — inspect for tearing or displacement on the
   affected arm. If torn: replace before continuing.
4. **CF rods** — acoustic ping all 4. Dull sound = loosened rod. Tighten
   pinch bolt.
5. **T-slot walls** — run finger inside the T-slot of any arm that experienced
   the crash impact. Any crack = ground the drone.
6. **Electronics** — visual inspect all connectors, capacitor, and solder
   joints on the FC and ESC. Any loose joint or dislodged component — address
   before powering on.
7. **Conformal coating** — if any chip or crack in the coating over the FC or
   ESC, repair before next flight in humid conditions.

---

## Rationale

### Why arm shaft replacement does not require special tools

The T-lock system was designed for field-replaceable arms with no tools beyond
a 1.5mm hex key (for the M2 screws). A repair kit for field deployment is:
two pre-printed spare arm shafts, an M2 hex key, four spare props, and four
M5 prop nuts. Total mass: ~80g. A drone grounded by a fractured arm at a
deployment site can be airborne again in under 10 minutes.

---

## Connections

requires:
  - [[failure-hierarchy]]
  - [[arm-shaft]]
  - [[floating-motor-mounts]]
related:
  - [[scheduled-maintenance]]
  - [[post-flight-check]]
  - [[coupon-validation]]
leads_to:
  - [[scheduled-maintenance]]
