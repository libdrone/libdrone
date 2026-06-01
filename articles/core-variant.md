---
id: core-variant
title: "Core variant"
version: 1.1.0
date: 2026-06-01
author: jsa
status: released
scope: libdrone
topic:
  - resilience-community
personas:
  - 5.student
  - 4.workshop
  - 6.evaluator
platform:
  - core
lang: en
licence: CC BY-SA 4.0
---

## Summary

libdrone Core is the educational variant of the libdrone family. It shares
the Matek H7A3-SLIM flight controller, ELRS receiver, and Betaflight firmware
stack with Pro, scaled down to a 4-inch, 4S airframe printed in PETG rather
than PC-CF. The defining design decision is deliberate reduction: Core removes
every capability not needed for FPV piloting education and drone construction
teaching. Its under-250 g all-up weight target has regulatory implications that
give students maximum flight access with minimum constraint — see
[[legal-and-regulatory]]. A student who builds
and flies Core acquires directly transferable skills — same firmware, same radio
protocol, same flight modes — when stepping up to Pro or Bandit.

---

## Concept

### Deliberate stripping

Core is not a smaller Pro. It is a stripped Pro — every capability that
increases build complexity, BOM cost, or regulatory weight without contributing
to the educational objective has been removed. No HDZero digital video (analog
is cheaper, more goggle-compatible for group sessions). No PC-CF arms (PETG is
printable on any school-grade printer). No 6S power system (4S reduces handling
risk and BOM cost).

What is retained is everything that makes the platform educationally valid:
the same FC so Betaflight skills transfer directly, the same ELRS protocol so
radio skills transfer, the same EdgeTX model structure, and the same GX12-7
dual payload interface so a payload built on Core flies on Pro and Bandit
without modification. Students learn the real interface from day one — not
a simplified substitute.

### The sub-250 g threshold

Keeping AUW below 250 g is a deliberate design constraint, not a coincidence:
it is the weight threshold with the lightest-touch regulatory treatment, which
matters practically for educational deployments in school yards, at events, and
during workshops. What that treatment is, and where it applies, is in
→ [[legal-and-regulatory]] — read it and decide for yourself.

### Skill transfer path

Core → Pro is the intended progression for pilots. Core → Bandit is the
intended progression for operators moving into autonomous flight. The shared
hardware (H7A3, ELRS) and shared firmware (Betaflight) make both transitions
a configuration change rather than a relearning. The 30×30 stack geometry,
the prop-tightening procedure, the Betaflight rate profiles — all identical.
The investment in learning Core compounds.

---

## Reference

| Parameter | Value |
|---|---|
| Wheelbase | ~160 mm (4-inch class) |
| Flight system | Betaflight |
| FC | Matek H7A3-SLIM |
| ESC | SpeedyBee BLS 50A 30×30 |
| Motors | T-Motor Pacer P1804 3400KV |
| Battery | 4S 850 mAh XT30 |
| AUW target | < 250 g |
| Print material | PETG |
| Video | Analog (Foxeer Predator Nano + Reaper Nano V2) |
| Payload interface | Dual GX12-7 A/B (mandatory, fully wired) |
| BOM cost | ~€180 |
| Weight target | sub-250 g (regulatory implications — see [[legal-and-regulatory]]) |

**Shared SKUs with Pro and Bandit:** Matek H7A3-SLIM, Happymodel EP2 Nano,
3 mm CF rods, M2/M3 hardware.

---

## Procedure

<!-- not applicable — build and commissioning follow the Pro path with
PETG print settings; see [[print-profiles]] and [[betaflight-setup]] -->

---

## Rationale

The choice of analog video over HDZero is the most questioned cost-saving
decision in Core. Digital FPV provides better image quality and latency. For
an educational platform, however, the goal is not image quality — it is that
every student in the room can watch a live feed. Box goggles with analog
receivers cost €30–50 and are universally available. HDZero goggles cost
€150–200 and require the HDZero ecosystem. Analog keeps the workshop barrier
low. When a student transitions to personal equipment for their own builds,
they make their own video system choice — Core does not pre-select it for them.

---

## Connections

requires:
  - [[platform-overview]]
related:
  - [[platform-selection]]
  - [[bandit-variant]]
  - [[legal-and-regulatory]]
  - [[betaflight-setup]]
  - [[print-profiles]]
  - [[petg]]
leads_to:
  - [[betaflight-setup]]
  - [[platform-selection]]
