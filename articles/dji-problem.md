---
id: dji-problem
title: "The DJI problem"
version: 1.1.0
date: 2026-06-01
author: jsa
status: released
scope: libdrone
topic:
  - open-source-philosophy
  - resilience-community
personas:
  - 6.evaluator
  - 5.student
  - 2.operator
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

DJI makes excellent drones. That is not the problem. The problem is that
every DJI flight routes data through servers outside EU jurisdiction, every
DJI payload runs on a closed interface, and every DJI operator is dependent
on a Chinese company's continued goodwill for the platform's continued
function. For a hobbyist, this is an acceptable trade-off. For a Czech
municipality doing flood assessment, a Baltic civil defence group, a NATO-
adjacent research institution, or any organisation where data sovereignty
is a procurement requirement — it is not acceptable at all.

This article explains the gap that created libdrone and why it is now the
EU civilian reference implementation for open-source aerial infrastructure.

---

## Concept

### Why DJI stopped being a default

Until roughly 2022, DJI was the unquestioned default for anyone needing an
affordable, capable drone. The hardware remained — and remains — genuinely
impressive. What changed was the political and regulatory environment around it.

Several converging pressures made DJI problematic for institutional EU use:

**Data routing.** DJI's app transmits telemetry, imagery metadata, and in
some configurations video frames to DJI servers. The destination of that
data is outside EU jurisdiction, outside GDPR enforcement reach, and outside
any EU institution's ability to audit. For a commercial photographer, this
is a privacy inconvenience. For a civil protection officer mapping a flood
in a European city, it is a data sovereignty breach.

**US restrictions as a signal.** The US Department of Defense added DJI to
its list of Chinese military companies in 2022. The US government banned DJI
purchases across federal agencies. Whatever the specific legal rationale,
the signal was unambiguous: US government and NATO-adjacent institutions do
not consider DJI a trusted platform. EU institutions operating in
NATO-compatible procurement frameworks read this signal correctly.

**Supply chain opacity.** DJI's component sourcing is not publicly documented.
An institution cannot audit what is inside a DJI drone. It cannot verify
the firmware running on the flight controller. It cannot know whether a
software update changed the data routing behaviour. This is not a theoretical
concern — it is a structural property of closed-source hardware that makes
independent verification impossible.

**Closed payload interface.** DJI's payload SDK is gated behind a developer
programme with significant cost and NDA requirements. A sensor manufacturer
cannot build a DJI-compatible payload without DJI's permission and without
committing to terms that include data sharing with DJI. For any institution
that wants to deploy its own sensor — an air quality monitor, a radiation
survey instrument, a thermal camera — this is a fundamental constraint.

### The alternatives that did not fill the gap

When EU institutions began moving away from DJI, they found that the
alternatives were worse in different ways.

**Commercial enterprise drones** (Parrot Anafi, Autel, Skydio) addressed the
Chinese supply chain concern but kept the closed-software and closed-payload
problems. Paying €2,000–8,000 for a drone that still has a proprietary payload
interface is not a meaningful improvement for an institution that wants to
deploy its own sensors.

**Academic research platforms** (PX4-based custom builds, institutional UAV
programmes) were genuinely open but started at €10,000–50,000 and required
institutional procurement processes, specialised technical staff, and multi-
year deployment timelines. A Czech municipal civil protection office with a
€2,000 budget and no dedicated drone engineer cannot use these.

**Racing FPV drones** were cheap, community-supported, and technically
excellent — but built specifically to fly fast and crash safely. No payload
concept. No structured data output. No GPS-assisted navigation. No
documentation for anything beyond flying fast.

None of these options served the municipality, the community preparedness
group, the university research team, or the volunteer SAR coordinator. The
gap between "I can afford it but it is proprietary" and "it is open but I
cannot afford it" was real and unfilled.

### What libdrone actually is

libdrone is the EU civilian reference implementation for open-source aerial
infrastructure. It is not a product you buy. It is a platform you build,
understand, and own completely.

Designed in the Czech Republic. Licensed under CERN OHL-S v2 — the strongest
open hardware copyleft licence available, developed at CERN for exactly this
class of infrastructure. Legal entity in the Czech Republic. All design files,
every component choice, every engineering decision publicly documented and
permanently preserved.

The hardware summary: a 330 mm quadrotor, 6-inch propellers, approximately
720 g all-up weight with battery — a weight class with regulatory implications
covered in [[legal-and-regulatory]]. 12–15 minutes
endurance. The structural frame costs €16 in filament on any consumer FDM
printer. Total build cost approximately €1,400 with goggles and a complete
sensor payload.

The complete software and firmware stack is open source: Betaflight (GPL v3)
on the flight controller, ExpressLRS (GPL v3) for the radio link, AM32 (MIT)
for ESC firmware, EdgeTX (GPL v2) on the transmitter, FreeCAD (LGPL v2) for
CAD. Every line of code is publicly readable and independently verifiable.
No proprietary firmware in the critical path.

The satellite navigation uses Galileo and EGNOS — EU-origin infrastructure
— in addition to GPS. This removes dependency on US military policy decisions.
GPS Selective Availability demonstrated that this dependency is real; Galileo
removes it.

### The payload interface: why this is infrastructure, not a product

The feature that separates libdrone from any drone-with-sensors is the GX12-7
payload interface. Two aviation-grade connectors on the sealed top surface
of every platform provide: regulated power, GPS coordinates at 10 Hz,
bidirectional communications (UART and I2C), radio-controlled switching, and
live overlay in the pilot's goggles.

Any sensor, camera, or instrument built to this interface works on any libdrone
platform, regardless of version or manufacturer. An institution that invests
in building an air quality payload can fly it on a Pro, a Bandit, or a future
platform variant — without electrical rework, without a developer programme,
without NDA. The interface specification is public.

→ [[gx12-connector-standard]] contains the full ICD.

This is the architectural distinction between a drone and a platform. A drone
with a sensor is a single-purpose tool. A platform with a documented interface
is infrastructure that compounds in value as more payloads are built for it.

---

## Reference

### Who is using libdrone and for what

**Community preparedness groups** deploying thermal and air quality payloads
for flood route assessment, chemical incident monitoring, and night perimeter
awareness. The drone that has been flown 50 times before the flood exists —
the drone in a box does not. → [[civilian-preparedness]], → [[resilience-use-cases]]

**Municipal civil protection offices** in Central Europe specifying a
community-level aerial awareness capability at €1,400 rather than €5,000–50,000.
The cost differential is not marginal — it is the difference between deployment
and continued non-deployment. → [[sk-municipal-emergency-guide]]

**University research groups** using the payload interface to deploy novel
sensors without custom drone development. The SEN66 air quality payload, the
radiation survey payload, and the thermal imaging payload are documented and
reproducible. → [[sk-university-programme-proposal]], → [[payload-sdk]]

**Civil defence and volunteer SAR groups** in NATO-adjacent countries
building autonomous situational awareness capability on the Bandit platform
with ArduPilot, ATAK integration, and MAVLink telemetry. → [[bandit-variant]],
→ [[iff-architecture]]

### Cost comparison

| Platform | Cost | Open source | Payload interface | Data sovereignty |
|---|---|---|---|---|
| DJI Mavic 3 Enterprise | €4,800 | No | Proprietary SDK, NDA | No |
| Parrot Anafi USA | €7,000 | Partial | Limited | Partial |
| Academic PX4 build | €10,000–50,000 | Yes | Custom | Yes |
| libdrone Pro (full build) | ~€1,400 | Yes | Open standard | Yes |
| libdrone Core (training) | ~€320 | Yes | Open standard | Yes |

### The EU regulatory position

libdrone is a privately-built, EU-origin platform. The regulatory specifics —
which subcategory a given variant falls in, what that permits, and the route to
institutional operations — are consolidated in one place; read it and decide for
yourself. The headline relevant here: a self-built libdrone is a privately-built
UAS under EASA, a permanent named category independent of the commercial
class-marking regime.

The CERN OHL-S v2 licence satisfies open science requirements for EU Horizon
Europe and national research funding frameworks. The full FOSS stack satisfies
EU Cyber Resilience Act auditability requirements. Galileo + EGNOS navigation
satisfies EU strategic autonomy requirements where applicable.

→ [[legal-and-regulatory]], → [[foss-stack-libdrone]]

### The supply chain argument in one paragraph

Every libdrone component has a documented alternative. The BOM is public.
The suppliers are documented. An institution can audit the supply chain
independently without trusting the platform designer's claims. If AliExpress
stops shipping, the alternative components are documented. If a specific ESC
manufacturer discontinues a model, the compatible replacement is documented.
No single company can strand a libdrone deployment.

→ [[bom-summary]], → [[vendor-lock-in]]

---

## Procedure

### If you are evaluating libdrone for institutional procurement

Start here: → [[sk-platform-brief]] — 30 minutes, takes you from zero to
a procurement recommendation.

Then: → [[resilience-use-cases]] for the 15 documented operational use cases.

Then: → [[bom-summary]] for the cost structure and supplier map.

Then: → [[sk-libdrone-eu-nato-bridge]] if your context involves NATO-adjacent
governance or EU institutional documentation requirements.

### If you found this article from a search and want to understand more

→ [[platform-overview]] is the correct next article. It covers the complete
variant family, the payload interface in more depth, and the three gaps
in the market that libdrone fills.

→ [[why-build-a-drone]] explains the engineering and preparedness case
from first principles.

→ [[civilian-preparedness]] explains the specific use case for community
and household preparedness deployment.

---

## Rationale

### Why this article exists

The people who need libdrone most are not searching for "libdrone." They are
searching for "DJI alternative Europe," "open source drone EU," "drone data
sovereignty," "affordable community preparedness drone," or "municipal drone
program open source." This article is written for those searches. It names
the problem they are experiencing before it names the platform that addresses it.

The goal is not to sell libdrone. It is to give an honest account of why DJI
stopped being a default for EU institutional use, what the alternatives actually
offer, and what libdrone is — so that anyone who lands here from a search can
decide quickly and accurately whether this platform fits their context.

---

## Connections

requires: []
related:
  - [[platform-overview]]
  - [[foss-stack-libdrone]]
  - [[vendor-lock-in]]
  - [[civilian-preparedness]]
  - [[bom-summary]]
  - [[sk-platform-brief]]
leads_to:
  - [[platform-overview]]
  - [[civilian-preparedness]]
  - [[sk-platform-brief]]


[gx12-connector-standard]: gx12-connector-standard.md "GX12 connector standard"
[civilian-preparedness]: civilian-preparedness.md "Civilian preparedness"
[resilience-use-cases]: resilience-use-cases.md "Resilience use cases"
[sk-municipal-emergency-guide]: ../skeletons/sk-municipal-emergency-guide.md "Municipal Emergency Deployment Guide"
[sk-university-programme-proposal]: ../skeletons/sk-university-programme-proposal.md "University Programme Proposal"
[payload-sdk]: payload-sdk.md "Payload SDK"
[bandit-variant]: bandit-variant.md "Bandit variant"
[iff-architecture]: iff-architecture.md "IFF architecture"
[easa-open-category]: easa-open-category.md "EASA Open Category"
[foss-stack-libdrone]: foss-stack-libdrone.md "FOSS stack in libdrone"
[regulatory-overview]: regulatory-overview.md "Regulatory overview"
[bom-summary]: bom-summary.md "Bill of materials summary"
[vendor-lock-in]: vendor-lock-in.md "Vendor lock-in"
[sk-platform-brief]: ../skeletons/sk-platform-brief.md "Platform Brief"
[sk-libdrone-eu-nato-bridge]: ../skeletons/sk-libdrone-eu-nato-bridge.md "libdrone documentation as EU/NATO-compatible infrastructure"
[platform-overview]: platform-overview.md "Platform overview"
[why-build-a-drone]: why-build-a-drone.md "Why build a drone"
