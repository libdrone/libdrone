---
id: sk-workshop-handout
title: "Workshop Participant Handout"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

After completing the workshop series, the participant has built a flying
libdrone from components, understands why each design decision was made, and
can maintain and repair their build independently. This handout is the
condensed guide for workshop participants — it complements the instructor's
delivery, not replaces it.

---

## Concept

### Why you are building this and not buying it

→ [[why-build-a-drone]] answers this directly. The short version: a drone you
built is transparent — you understand every layer, you can repair every
failure mode, and you are not dependent on a vendor's continued support. A
bought drone is a black box. The build is not the price of admission; the
build is the point.

The workshop uses libdrone specifically because every design decision has a
documented rationale. When the instructor says "we use floating motor mounts
with O-ring isolators" — that is not an arbitrary choice. → [[floating-motor-mounts]]
explains the vibration isolation physics and why silicone O-rings at 40–50
Shore A are the correct damping material.

### Session 1 — Understanding the frame

Before printing or assembling anything, understand what you are building and
why it is shaped the way it is.

The five-layer sandwich (PETG-PCCF-PCCF-PCCF-PETG) is not aesthetic — it is
a specific engineering choice. → [[sandwich-structure]] explains why this
combination outperforms a pure carbon fibre frame for community builders:
printable, repairable, tolerates non-expert assembly. The carbon fibre rods
through all five layers provide the stiffness; the printed layers provide the
geometry and the crash energy distribution.

The failure hierarchy is the most important design principle to internalise
before your first crash (and you will crash). → [[failure-hierarchy]] explains
the deliberate sequence: bumper absorbs first impact, arm shaft fractures
and absorbs crash energy, electronics survive. A fractured arm shaft after
a crash is a success, not a failure. You replace a 20g piece of PETG in five
minutes and fly again.

### Session 2 — Frame assembly

→ [[coupon-validation]] happens before printing production parts. Coupon 8
verifies the T-lock fit at your printer's calibration — the arm tab must
slide into the T-slot with light hand pressure and zero lateral play. If it
doesn't fit, the variable is adjusted in FreeCAD, not filed or forced.

→ [[airframe-integration]] is the assembly sequence. The order matters: tabs
into T-slots, all five layers on the CF rods simultaneously (they self-align),
sandwich bolts, Platform on posts. The acoustic ring test after rod threading
confirms correct pre-tension: tap each rod, listen for a clear ring at
2.2–2.6 kHz. A dull thud means the rod is loose.

### Session 3 — Electronics installation

→ [[electronics-installation]] is the wiring session. The EMC rules are not
bureaucratic — they are the reason the drone will fly smoothly and the GPS
will have a stable fix.

The three rules in practice: (1) all grounds to the ESC pad, nothing else
(→ [[star-grounding]]); (2) motor phase wires twisted together 1 twist per
15mm (→ [[twisted-pairs]]); (3) signal wires left of centre, power wires right
(→ [[power-signal-separation]]). Violating these rules produces a flying drone
that works until it doesn't — intermittent GPS drift, vibration in the video,
noisy Blackbox traces.

Conformal coating is mandatory before first power-on. → [[conformal-coating]]
explains why: electronics are designed for dry conditions; a skatepark has
dew, rain, and condensation. The coating takes 30 minutes to apply and 24
hours to cure.

### Session 4 — Software commissioning

→ [[software-commissioning]] is the configuration session. The sequence is
fixed: EdgeTX model first (→ [[edgetx-model]]), then Betaflight (→ [[betaflight-setup]]),
then AM32 ESC, then HDZero VTX (→ [[digital-fpv]]).

After configuration: verify motor directions in the Betaflight Motors tab
with props removed. Verify all channels respond correctly in the Receiver tab
while moving each stick. Verify GPS fix ≥ 8 satellites outdoors before arming.

### Session 5 — Acceptance validation and first flight

→ [[acceptance-validation]] is the checklist between commissioning and flight.
Weigh the drone. Confirm e-ID label is on the frame. Confirm airspace is clear.

→ [[first-flight]] is the supervised first flight sequence: hover at 1m for
30 seconds, land and inspect, then a slow circuit with the instructor, then
a GPS Rescue demonstration. The GPS Rescue demonstration is not optional —
you need to have seen GPS Rescue activate deliberately before you ever
experience it in an uncontrolled situation.

After the first flight: → [[blackbox-analysis]] with the instructor. You will
see your drone's gyro spectrum for the first time. A clean build looks like
this: noise floor below −40 dB in the 0–200 Hz range, no sharp peaks at
motor RPM harmonics.

### Continuing from here

The workshop gave you a flyable drone. → [[scheduled-maintenance]] tells you
how to keep it airworthy. → [[piloting-progression]] maps the skill development
from hover to FPV orientation to emergency procedures. → [[pre-flight-check]]
is the discipline that separates safe operators from ones who get lucky.

---

## Reference

### Workshop sessions and key articles

| Session | Content | Key articles |
|---|---|---|
| 1 | Why build, frame design | [[why-build-a-drone]], [[sandwich-structure]], [[failure-hierarchy]] |
| 2 | Assembly | [[coupon-validation]], [[airframe-integration]], [[floating-motor-mounts]] |
| 3 | Electronics | [[electronics-installation]], [[star-grounding]], [[conformal-coating]] |
| 4 | Software | [[software-commissioning]], [[betaflight-setup]], [[edgetx-model]] |
| 5 | First flight | [[acceptance-validation]], [[first-flight]], [[blackbox-analysis]] |
| Post-workshop | Ongoing | [[scheduled-maintenance]], [[piloting-progression]], [[pre-flight-check]] |

---

## Procedure

### Pre-workshop preparation (if time permits)

Read → [[sandwich-structure]], → [[failure-hierarchy]], and → [[lipo-batteries]]
before Session 1. Understanding the frame philosophy and LiPo safety rules
before you handle either component is time well spent.

---

## Rationale

The workshop handout exists because the Complete Build Guide is too long for
a workshop context. Workshop participants need the narrative arc and the "why"
behind each step — not the full technical depth of every atom. This skeleton
provides that narrative at workshop depth, with links to the full depth for
participants who want to go further.

---

## Connections

requires: []
related:
  - [[sk-complete-build-guide]]
  - [[sk-engineering-101]]
leads_to:
  - [[sk-complete-build-guide]]
  - [[sk-operations-manual]]
