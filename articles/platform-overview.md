---
id: platform-overview
title: "Platform overview"
version: 1.1.0
date: 2026-06-01
author: jsa
status: released
scope: libdrone
topic:
  - resilience-community
personas:
  - 6.evaluator
  - 5.student
  - 7.contributor
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

libdrone is an open-source aerial payload platform designed in the Czech
Republic, licensed under CERN OHL-S v2, and deployable by anyone with a
consumer 3D printer and basic soldering skills. It is not a consumer product.
It is open infrastructure — a flying platform with a documented payload
interface that any sensor, camera, or instrument can attach to without
modifying the drone. The platform family covers civilian situational awareness
(Bandit, autonomous), research and mapping (Pro, manual), training (Core),
reduced-emissions operations (Ghost), and fixed-wing endurance (Wing). A
complete Pro build with goggles costs approximately 34,000 CZK (~€1,400) and
is repairable in the field in under 10 minutes.

---

## Concept

### The distinction that matters: drone vs platform

A drone with a sensor is a single-purpose tool. When the sensor changes, the
drone must be modified. When the drone is updated, the sensor integration must
be reworked. Each combination is a custom project.

A platform with a payload interface is infrastructure. The interface is defined
once. Any payload built to the interface works on any compliant platform,
regardless of version or manufacturer. An institution that invests in developing
an air quality payload can also use it on a radiation survey drone, a mapping
drone, or a future platform — without electrical rework.

libdrone made this shift deliberately. The top surface of every platform is a
standardised electrical and mechanical interface. The drone does not know or
care what payload is fitted. The payload does not know or care which platform
version it is flying on. This is what makes the platform extensible.

### The supply chain gap nobody filled

Before libdrone, three options existed for aerial sensing:

- **DJI and commercial platforms**: extraordinary hardware, closed software,
  proprietary payload interfaces, cloud-dependent data pipelines, Chinese
  supply chain.
- **Academic platforms**: genuinely open, but €10,000–50,000 and requiring
  institutional procurement.
- **Racing FPV drones**: cheap and community-supported, but built to crash —
  no payload concept, no GPS-assisted navigation, no structured data output.

None of these serve a Czech municipality, a university research group, a
community preparedness group, or a component vendor that needs a reference
platform for their hardware. libdrone fills this gap at €1,400 with a full
documentation stack, a documented payload standard, and zero cloud dependency.

---

## Reference

### Platform family

| Variant | Flight system | Primary use | Status |
|---|---|---|---|
| **Pro** | Betaflight, 6S | Research, mapping, payload operations | Released |
| **Bandit** | ArduPilot, 6S | Autonomous missions, ATAK integration | Released |
| **Core** | Betaflight, 4S | Training, education, backup | Released |
| **Ghost** | Betaflight, 6S | Reduced-emissions, security-sensitive | Released |
| **Wing** | ArduPilot/INAV, fixed-wing | Long-endurance, area coverage | In development |

### Key specifications (Pro / Bandit)

| Parameter | Value |
|---|---|
| Wheelbase | 330 mm True-X |
| Propellers | 6-inch HQProp |
| Dry mass | ~410 g |
| AUW with battery | ~720–760 g |
| Weight class | over 250 g — regulatory implications, see [[legal-and-regulatory]] |
| Flight time (cruise) | 12–15 min |
| Flight time (with payload) | 10–12 min |
| Payload capacity | 80–150 g |
| Build cost (single frame, no goggles) | ~18,000 CZK |
| Build cost (with HDZero Goggle 2) | ~34,000 CZK |
| Arm replacement time | < 5 min, no tools |
| Payload swap time | < 60 s |

### Documentation and licensing

| Item | Licence |
|---|---|
| Hardware designs | CERN OHL-S v2 (strongly reciprocal) |
| Documentation | CC BY-SA 4.0 |
| Betaflight firmware | GPL v3 |
| ExpressLRS | GPL v3 |
| AM32 ESC firmware | MIT |
| Payload designs | Your licence — not subject to CERN OHL-S |

---

## Procedure

<!-- not applicable — this is an overview article -->

---

## Rationale

### Why CERN OHL-S and not permissive hardware licensing

CERN OHL-S v2 is strongly reciprocal: modifications to libdrone hardware must
be released under the same licence. This protects the commons. A community
that has invested in building documentation, tooling, and reference builds
around a platform should not find that a vendor has forked the design, improved
it, and closed the improvements. The copyleft ensures that improvements flow
back. Payload designs — which are separate from the platform — carry no licence
obligation. Your payload IP stays yours.

---

## Connections

requires: []
related:
  - [[civilian-preparedness]]
  - [[foss-principles]]
  - [[legal-and-regulatory]]
  - [[gx12-connector-standard]]
leads_to:
  - [[resilience-use-cases]]
  - [[bom-summary]]
  - [[bandit-variant]]
  - [[ghost-variant]]
  - [[core-variant]]
  - [[wing-variant]]
  - [[pro-variant]]
