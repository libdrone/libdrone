---
id: sk-variant-specs
title: "Platform Variant Specifications"
version: 2.1.0
date: 2026-05-12
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 6.evaluator
  - 8.architect
  - 1.builder
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

After reading this document, the evaluator or architect can understand
the technical differentiators between all six libdrone variants and select
the correct platform for their application. Each variant has a dedicated
concept atom — this skeleton provides comparative context and routes to the
right depth. For the procurement decision itself, read → [[platform-selection]]
first.

---

## Concept

### The family architecture

All libdrone variants share a design philosophy: open hardware, FOSS firmware,
EU-origin components where possible, zero cloud dependency, field-repairable.
What varies is frame geometry, motor scale, battery chemistry, flight system,
and primary mission profile.

The variants are not a product line — they are a platform family. An institution
operating Pro and Bandit benefits from shared spare parts (FC, ELRS receiver,
GX12 connectors), shared documentation, and shared pilot skills. The closer
the variants, the lower the operational overhead of running multiple.

---


## Concept: Pro

Pro is the reference platform — the 6-inch, 6S variant around which the GX12-7
payload interface standard and the full five-layer airframe architecture were
designed. Where the other variants adapt or extend the Pro baseline, Pro
defines what that baseline is. It carries the most capable payload interface
in the family, the highest performance power system, and the digital FPV stack.
It is the correct platform when payload capacity, 6S performance, and the
full GX12 ecosystem matter more than flight time or cost.

Full concept, specifications, and payload interface detail: → [[pro-variant]]

---

## Concept: Bandit

Bandit is the autonomous-capable training and light-survey variant. The
fundamental departure from the rest of the family is the flight system:
Betaflight is replaced with ArduPilot Copter, enabling GPS-guided flight modes,
MAVLink telemetry, and QGroundControl mission execution. A pre-programmed
survey grid runs without continuous pilot input. The awareness curriculum this
platform supports teaches operators to think like the technology they are
learning to understand.

Full concept, specifications, and mission types: → [[bandit-variant]]

For the ArduPilot ecosystem that defines Bandit: → [[ardupilot-copter]] and
→ [[ardupilot-flight-modes]]

---

## Concept: Ghost

Ghost is the quiet, long-endurance variant. Two engineering decisions define
it: large low-KV motors driving 12-inch props at low RPM reduce the acoustic
signature by approximately 10 dB(A) compared to Pro — roughly half as loud to
the human ear. Li-Ion 18650 batteries replace Li-Po for energy density over
peak power, enabling 30–45 minute endurance. Ghost reuses the complete Bandit
electronics stack and adds mandatory ESP32-S3 IFF and Remote ID.

Full concept, specifications, and mission profile: → [[ghost-variant]]

The acoustic design rationale: → [[acoustic-signature-design]]
The Li-Ion battery architecture: → [[li-ion-batteries]]
The CF plate arm system: → [[cf-plate-arms]]

---

## Concept: Core

Core is the educational variant. 4-inch props, 4S power, under 250 g AUW
places it in EASA Open A1 — students fly with minimum regulatory friction.
Core is deliberately stripped: no GX12 payload interface, no digital FPV,
no PC-CF arms. What remains is everything needed to teach FPV piloting and
drone construction with direct skill transfer to Pro and Bandit: same Matek
H7A3-SLIM, same Betaflight, same ELRS/EdgeTX stack.

Full concept and educational rationale: → [[core-variant]]

---

## Concept: SCRAP

SCRAP is the entry-level practice build — 3-inch props, 4S, ~130 mm wheelbase,
sub-250 g. It is not a mission platform: there is no GX12-7 payload interface
and no PC-CF arms. Its purpose is to give a new builder something real to
construct and fly before committing the time and material cost of a Core or
Pro build. Crash damage is cheap to repair; the arms are integral to the frame
and print in under an hour. The electronics stack — Betaflight, ELRS, EdgeTX —
is identical to Core, so every skill transfers without relearning. SCRAP feeds
Core design decisions through real crash experience: what breaks, what doesn't,
what the builder was actually confused by.

Full concept, build sequence, and BOM: → [[scrap-variant]]

Build guide: → [[sk-scrap-build-guide]]

---

## Concept: Wing

Wing is the fixed-wing survey companion. Fixed-wing is categorically more
efficient for area coverage than multirotor — a single Wing sortie covers
what would take 8–10 Pro battery cycles. The primary initial application is
wildlife population survey at dawn and dusk using thermal imaging for Czech
hunting associations. Wing shares the GX12-7 dual payload standard with all
other payload-equipped variants — the same thermal payload works on Pro and
Wing without modification.

Full concept and airframe options: → [[wing-variant]]

The fixed-wing efficiency argument: → [[fixed-wing-fundamentals]]
The survey workflow: → [[wildlife-survey-operations]]

---

## Reference

### Family comparison table

| Parameter | Pro | Bandit | Ghost | Core | SCRAP | Wing |
|---|---|---|---|---|---|---|
| Wheelbase | 330mm | 220mm | ~540mm | ~160mm | ~130mm | 2122mm span |
| Prop size | 6-inch | 4-inch | 12-inch | 4-inch | 3-inch | Fixed-wing |
| Battery | 6S LiPo | 4S LiPo | 4S Li-Ion | 4S LiPo | 4S LiPo | 4S LiPo |
| Flight time | 12–15 min | ~12 min | 30–45 min | ~10 min | ~5 min | 45–75 min |
| Flight system | Betaflight | ArduPilot | ArduPilot | Betaflight | Betaflight | ArduPilot |
| ATAK native | MSP bridge | ✓ MAVLink | ✓ MAVLink | — | — | ✓ MAVLink |
| GX12 payload | ✓ | ✓ | ✓ | — | — | ✓ |
| LCM-1 ready | ✓ | ✓ | ✓ | — | — | ✓ |
| EASA category | A2 | A2 | A2 | A1 | A1 | A2+ |
| Arms | PC-CF printed | TPU printed | CF plate | PETG printed | Integral frame | Fixed wing |
| Status | Released | Released | Pre-design | Released | Released | Concept |
| BOM cost | ~€380 | ~€219 | ~€444 | ~€180 | ~€90 | TBD |

---

## Procedure

### Variant selection guidance

→ [[platform-selection]] provides the full decision matrix against operational
scenarios. The short version:

- Autonomous GPS missions, ATAK integration, awareness curriculum → **Bandit**
- Long endurance, low acoustic signature, EMCON operations → **Ghost**
- FPV pilot education, drone construction teaching → **Core**
- First build, crash-proof practice, minimal cost entry → **SCRAP**
- Large-area thermal survey, wildlife monitoring → **Wing**
- Payload research, commercial operations, 6S performance → **Pro**

---

## Rationale

Version 2.0.0 of this skeleton strips the inline specification prose that
existed in v1.0.0 for each variant. That content now lives in dedicated
variant atoms ([[bandit-variant]], [[ghost-variant]], [[core-variant]],
[[wing-variant]]). The skeleton's role is comparative context and routing —
not specification. Any fact that belongs to a specific variant belongs in
that variant's atom, not here.

Version 2.1.0 adds SCRAP as the sixth variant following the addition of
[[scrap-variant]] and [[sk-scrap-build-guide]] to the corpus (2026-05-10).

---

## Connections

requires:
  - [[platform-overview]]
  - [[pro-variant]]
  - [[bandit-variant]]
  - [[ghost-variant]]
  - [[core-variant]]
  - [[scrap-variant]]
  - [[wing-variant]]
related:
  - [[platform-selection]]
  - [[ardupilot-copter]]
  - [[acoustic-signature-design]]
  - [[fixed-wing-fundamentals]]
  - [[sk-platform-brief]]
  - [[sk-bandit-awareness-curriculum]]
leads_to:
  - [[platform-selection]]
  - [[pro-variant]]
  - [[bandit-variant]]
  - [[ghost-variant]]
  - [[core-variant]]
  - [[scrap-variant]]
  - [[wing-variant]]
