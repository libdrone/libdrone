---
id: wing-variant
title: "Wing variant"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: libdrone
topic:
  - resilience-community
personas:
  - 6.evaluator
  - 2.operator
  - 8.architect
platform:
  - wing
lang: en
licence: CC BY-SA 4.0
---

## Summary

libdrone Wing is the fixed-wing survey companion to the libdrone family.
Where all other family members are multirotors, Wing is a flying-wing or
conventional fixed-wing airframe running ArduPilot Plane, carrying the
standard GX12-7 dual payload interface, and optimised for large-area coverage
at extended endurance — 45–75 minutes per sortie. The primary initial
application is wildlife population survey at dawn and dusk using a thermal
imaging payload, with the Czech hunting associations as the first operational
customer. Wing is concept and pre-design stage as of v0.1; the electronics
stack is specified but the airframe is not yet selected or built.

---

## Concept

### Why fixed-wing for survey

A multirotor holds position by continuously vectoring thrust against gravity —
efficient for hover, inefficient for covering ground. A fixed-wing generates
lift from forward motion; the energy cost of covering area drops dramatically
compared to a multirotor on the same battery. A Wing covering 50 hectares in
one 45-minute sortie would require eight to ten Pro battery cycles to replicate.
For survey missions where area coverage matters more than hover capability,
fixed-wing is the correct choice. See → [[fixed-wing-fundamentals]] for the
efficiency physics.

### The wildlife survey application

Czech hunting associations face regulatory pressure to demonstrate quantified
wildlife population data. Manual ground counts are incomplete and cannot produce
GPS-referenced evidence. Helicopter surveys cost thousands of euros per hour.
Wing provides a third path: an autonomous grid survey at 40–60 m AGL, timed for
the dawn or dusk thermal window when animal-to-ground thermal contrast is maximum,
producing a GPS-tagged detection log and a printable report. The service model is
not hardware sales — it is delivering that report to the association contact. The
hardware enables the service.

### Shared payload standard

Wing carries the GX12-7 dual payload interface — the same physical and electrical
standard as Pro, Bandit, and Ghost. A thermal imaging payload designed for Wing
plugs into Pro's backplane without modification, and vice versa. One payload
library serves all platforms. This cross-platform compatibility is the primary
reason for maintaining the GX12 standard across a family member that has
otherwise different mechanical architecture. See → [[gx12-connector-standard]].

### Airframe status

Wing does not prescribe a single airframe. Three candidates are identified —
Skywalker X8 (2122 mm span, recommended primary), Finwing Penguin (1400 mm,
survey-dedicated), Mini Talon V2 (1300 mm, lower cost POC) — with selection
driven by budget, regulatory AUW threshold, and thermal payload capacity. The
electronics stack (H7A3-WING, ELRS, ESP32-S3, MAVLink) is fixed regardless
of airframe selection.

---

## Reference

| Parameter | Value |
|---|---|
| Platform type | Flying wing or conventional fixed-wing |
| Reference airframe | Skywalker X8 (2122 mm span) |
| Flight system | ArduPilot Plane |
| FC | Matek H7A3-WING |
| Battery | 4S LiPo (size airframe-dependent) |
| Endurance | 45–75 min (airframe-dependent) |
| Survey altitude | 40–60 m AGL |
| Payload capacity | ~800 g belly bay (X8) |
| Payload interface | Dual GX12-7 (mandatory) |
| ESP32-S3 | Mandatory — IFF + Remote ID + detection logging |
| Primary mission | Thermal wildlife survey |
| EASA category | A2 or Specific (AUW-dependent) |
| Status | Concept / pre-design — not yet built |

---

## Procedure

<!-- not applicable — airframe selection and build are open points;
see [[ardupilot-plane]], [[thermal-imaging-payload]], [[wildlife-survey-operations]]
for mission-specific procedures -->

---

## Rationale

Wing exists because the GX12 payload standard created a thermal imaging payload
that needed more than one airframe to justify its development cost. A thermal
payload designed for Pro's backplane is worth more if it can also fly on a
fixed-wing platform covering ten times the area per sortie. The wildlife survey
application was identified as the fastest path to a paying customer for the
thermal payload — a specific, quantified need, a customer who cannot currently
meet it, and a deliverable (the report) that the customer understands. Wing is
the minimum platform to deliver that report.

---

## Connections

requires:
  - [[platform-overview]]
  - [[fixed-wing-fundamentals]]
related:
  - [[platform-selection]]
  - [[gx12-connector-standard]]
  - [[ardupilot-plane]]
  - [[thermal-imaging-payload]]
  - [[wildlife-survey-operations]]
  - [[esp32-s3-companion]]
  - [[iff-architecture]]
leads_to:
  - [[ardupilot-plane]]
  - [[thermal-imaging-payload]]
  - [[wildlife-survey-operations]]
