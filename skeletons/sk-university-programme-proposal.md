---
id: sk-university-programme-proposal
title: "University Programme Proposal"
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

After reading this proposal, a university programme director can evaluate
whether libdrone is an appropriate teaching platform for their engineering
curriculum and what a formal adoption pathway looks like. Learning objective:
propose libdrone for inclusion in a drone engineering module or practical course,
or conclude it does not match the programme's technical scope.

---

## Concept

### The curriculum argument

A student who builds a libdrone from components engages with: Newton's second
and third laws (thrust, reaction, inertia), kinematics (position, velocity,
acceleration), feedback control theory (PID, feed-forward, filter design),
electronics (power systems, motor control, signal integrity, sensor interfacing),
digital communications (UART, SPI, I2C, DShot, ELRS), software systems
(firmware configuration, open-source contribution workflow), mechanical
engineering (material selection, failure hierarchy, vibration isolation),
and regulatory frameworks (EASA A2, risk assessment, operational compliance).

No other single student project delivers this breadth at this cost. The drone
either flies correctly or it does not — feedback is immediate and unambiguous.
→ [[why-build-a-drone]] makes the full argument.

### The open-source educational advantage

libdrone uses exclusively open-source tools throughout the entire stack.
→ [[foss-stack-libdrone]] maps it completely: Betaflight (GPL v3), ExpressLRS
(GPL v3), AM32 (MIT), EdgeTX (GPL v2), FreeCAD (LGPL v2), MicroPython (MIT).
No student needs to purchase a software licence. No institution needs to
maintain a software agreement. Skills acquired with open tools transfer
everywhere — including to employers who use the same open tools.

The EU dimension is increasingly significant: EU research funding bodies
(Horizon Europe, national research councils) expect open science, open data,
and auditable platforms. A libdrone-based student project meets these
expectations by design. → [[foss-principles]] explains the CERN OHL-S v2
hardware copyleft and what it means for a university that builds on and
modifies the design.

### The teaching platform family

→ [[platform-overview]] covers the variant family. For a university context:

**Core** (4S, < 250g) is the correct starting platform for a drone engineering
module. Below 250g means students can operate under EASA A1 with minimal
regulatory friction. Shares key components with Pro — skills transfer directly.

**Pro** (6S, ~720g) is the research and advanced module platform. Full payload
interface, 6S performance, GPS-assisted navigation, full sensor integration.
The platform for a final-year project or research group deployment.

**Bandit** (ArduPilot) is the correct choice for an autonomous systems module.
Waypoint missions, GCS integration, MAVLink ecosystem. A student who learns
ArduPilot on Bandit can contribute to any ArduPilot-based project in the world.

### The corpus as course material

→ [[sk-engineering-101]] is a structured reading path through the physics,
control theory, propulsion, sensors, and structural engineering atoms. A
course that assigns atoms sequentially has a free, version-controlled,
community-maintained textbook. → [[sk-electronics-deep-dive]] covers the
electronics curriculum from battery chemistry to EMC.

The knowledge corpus is licensed under CC BY-SA 4.0 — any university can
fork it, extend it with course-specific content, and publish their version.
The copyleft requires publishing modifications under the same licence, which
contributes back to the community.

### The research application

libdrone's GX12 payload standard was designed specifically for the researcher
who has a sensor and a question. → [[payload-sdk]] maps the developer path.
→ [[payload-software-protocol]] defines the three-bus protocol that every
payload uses. A research group can deploy a novel sensor on libdrone in one
afternoon with the PSB-1 breakout board (→ [[psb1-shield-board]]).

Air quality mapping, radiation survey, multispectral imaging, acoustic
monitoring — any instrument that fits within 93g and can communicate via
I2C or UART is a libdrone payload candidate. The data stays in-house —
no cloud, no data sharing agreement, no vendor access.

---

## Reference

### Curriculum module mapping

| Module | Platform | Key skeleton/atoms |
|---|---|---|
| Introduction to drone engineering | Core | [[sk-engineering-101]], [[why-build-a-drone]] |
| Applied electronics | Core/Pro | [[sk-electronics-deep-dive]], electronics domain |
| Control systems practical | Pro | control-systems domain, [[pid-tuning-rate-profile]] |
| Autonomous systems | Bandit | [[ardupilot-copter]], [[ardupilot-flight-modes]], [[sk-ardupilot-operator-guide]] |
| Sensor payload development | Pro | [[sk-payload-developer-guide]], payload-architecture domain |
| Regulation and airspace | All | [[legal-and-regulatory]], [[risk-assessment]] |

### Cost per student build (indicative)

| Configuration | Cost |
|---|---|
| Core (training, < 250g) | ~8,000 CZK (~€320) |
| Pro (research, complete) | ~18,000–34,000 CZK (~€720–1,400) |
| Shared goggles (pool of 3) | 15,500 CZK (~€620) for 3 students |

---

## Procedure

### Pilot programme pathway

1. One staff member or PhD student completes the full libdrone build (use
   → [[sk-complete-build-guide]]) and reports back on the build experience
2. Identify which module(s) the platform fits (see curriculum table above)
3. Procure Core platforms for the target module (lower cost, lower regulatory friction)
4. Run first cohort with staff facilitator + libdrone workshop support
5. Evaluate student outcomes against the module learning objectives

---

## Rationale

Universities evaluate platforms on three axes: curriculum coverage, total cost
of ownership, and licensing/data sovereignty. This skeleton addresses all
three directly and links to the atoms that contain the supporting detail. The
call to action (pilot programme) is small and specific — reducing the friction
to a first commitment.

---

## Connections

requires: []
related:
  - [[sk-platform-brief]]
  - [[sk-engineering-101]]
  - [[sk-ardupilot-operator-guide]]
  - [[bandit-variant]]
  - [[sen66-sensor]]
leads_to:
  - [[sk-engineering-101]]
