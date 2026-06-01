---
id: sk-platform-brief
title: "Platform Brief"
version: 1.1.0
date: 2026-06-01
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 6.evaluator
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

After reading this brief, the evaluator can explain what libdrone is,
why it is different from consumer and commercial alternatives, and whether
it is appropriate for their institution's deployment context. Learning
objective: recommend libdrone for further evaluation or conclude it is
not the right fit — either outcome is useful.

---

## Concept

### The problem this platform solves

Flood. Chemical spill. Power outage at night. Three streets away, you cannot
see what is happening. This is an information problem. For the first time in
history, it has a €1,400 answer that fits in a backpack — but only if someone
builds the right platform.

No existing option fills this gap cleanly. Commercial drones (DJI) are
closed software, cloud-dependent data pipelines, and Chinese supply chain.
Academic platforms are open but require institutional procurement at €10,000–50,000.
Racing FPV drones are cheap but have no payload concept and no structured
data output. → [[platform-overview]] maps this gap precisely.

libdrone is the EU civilian reference implementation: open-source, locally
repairable, zero cloud dependency, documented payload interface, community-
level cost.

### What the platform is

A 330mm True-X quadrotor, 6-inch propellers, approximately 720–760g all-up
with battery — a weight class with regulatory implications (see
[[legal-and-regulatory]]). 12–15 minutes endurance.
Built from 3D-printed PETG and PCCF structural layers — the frame costs €16
in filament. Electronics are commercially available components with documented
alternatives.

The airframe is not the product. The payload standard is the product.

Two GX12-7 aviation connectors on the sealed top surface give any payload
access to: regulated power (5V, 2A), GPS coordinates (57,600 baud NMEA,
10 Hz), bidirectional communications (UART + I2C), radio-controlled switching,
and OSD overlay in the pilot's goggles. → [[gx12-connector-standard]],
→ [[payload-electrical-interface]], → [[payload-software-protocol]] define
the complete interface.

### Why this is the right platform for your context

→ [[platform-overview]] gives the full variant family overview. The evaluator
question is: which variant, and why?

**For community preparedness and municipal deployment**: Pro platform.
Manually piloted, GPS-assisted, field-repairable in under 10 minutes,
operates fully offline. → [[civilian-preparedness]] and → [[resilience-use-cases]]
map the 15 use cases from everyday training to active flood response.

**For autonomous survey and ATAK integration**: Bandit platform. ArduPilot
firmware, waypoint missions, full MAVLink telemetry for tactical network
integration. → [[iff-architecture]] covers the ATAK CoT pathway.

**For training and education**: Core platform. Under 250g, lighter-touch
regulatory treatment, lower consequence per crash.

### The regulatory picture

→ [[legal-and-regulatory]] is the single source of truth for the regulatory
picture. The headline for an evaluator: a self-built libdrone is a
privately-built UAS, which places a Pro (over 250 g) in EASA subcategory A3 in
the Open Category (far from people) — urban and near-people operations run
through the Specific Category. Read it there and decide what fits your context.

### The cost picture

→ [[bom-summary]] contains the full cost breakdown. Single-frame build with
goggles: approximately 34,000 CZK (~€1,400). Second frame incremental cost:
approximately 7,000 CZK. Sensor payload (air quality mast): approximately
2,650 CZK additional.

Maintenance consumables: O-ring sets approximately every 20–30 flight hours.
Arm shafts (the crash fuse) print from filament stock at <€1 each in 20
minutes. No service contract, no proprietary spares, no cloud subscription.

### What partnership looks like

libdrone is a nonprofit open-hardware project. It does not sell drones —
it publishes the design. An institution can build from the documentation,
commission a local builder to produce units, or attend a workshop to train
their own builders.

Institutional partnerships with component vendors, resellers, or workshop
providers are welcomed. → [[foss-principles]] explains the CERN OHL-S v2
copyleft that governs modifications to the hardware design — your payload
designs are your IP, not subject to the copyleft.

---

## Reference

### Quick reference for evaluators

| Question | Article |
|---|---|
| What does it do? | [[platform-overview]], [[resilience-use-cases]] |
| What does it cost? | [[bom-summary]] |
| What are the regulations? | [[legal-and-regulatory]] |
| How is it maintained? | [[scheduled-maintenance]] |
| What payloads exist? | [[payload-sdk]], [[payload-integration]] |
| How does it fit into a preparedness programme? | [[community-deployment]] |
| Is the platform auditable / open? | [[foss-stack-libdrone]], [[foss-principles]] |

---

## Procedure

### Recommended evaluator reading sequence

1. [[platform-overview]] — 5 minutes, the thirty-second version plus variant family
2. [[resilience-use-cases]] — 10 minutes, the 15 use cases and sensor decision thresholds
3. [[bom-summary]] — 5 minutes, cost structure and supplier map
4. [[legal-and-regulatory]] — 5 minutes, the regulatory picture and what applies
5. [[community-deployment]] — 5 minutes, what your group needs before a crisis

Total: approximately 30 minutes to a confident procurement recommendation.

---

## Rationale

The Platform Brief is a Type B conversion skeleton: every paragraph moves the
evaluator toward a decision. It does not contain specifications (those are
in atoms), only the information needed to decide whether to proceed. An
evaluator who finishes this brief should know whether libdrone fits their
context — yes or no — not have more questions than they started with.

---

## Connections

requires: []
related:
  - [[sk-community-resilience-guide]]
  - [[sk-municipal-emergency-guide]]
  - [[sk-university-programme-proposal]]
leads_to:
  - [[sk-community-resilience-guide]]
