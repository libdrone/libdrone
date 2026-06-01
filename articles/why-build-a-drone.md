---
id: why-build-a-drone
title: "Why build a drone"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - resilience-community
personas:
  - 4.workshop
  - 5.student
  - 6.evaluator
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Building a drone is one of the few projects where a single weekend of work
produces a functional flying machine that touches physics, electronics,
software, mechanical engineering, and regulation simultaneously. But "why
build a drone" has a better answer than curiosity. A drone you built
yourself is one you can repair, extend, and trust — because you understand
every layer of it. A drone you bought is a black box that can be updated,
restricted, or discontinued by someone else. This article is the entry
point for workshop participants and new students: what the build teaches,
what the platform enables, and why the open-source choice matters.

---

## Concept

### What the build teaches

Building a libdrone is not a drone project. It is a systems engineering
project that uses a drone as the integrating artefact.

The skills touched in one complete build:

| Domain | What you encounter |
|---|---|
| Mechanical engineering | Parametric CAD, failure hierarchies, vibration isolation, material selection |
| Electronics | Power systems, motor control, signal integrity, sensor interfacing |
| Control theory | PID loops, filter design, RPM filter, feed-forward |
| Software | Firmware configuration, CLI tooling, open-source contribution workflow |
| RF and communications | ELRS link budget, CRSF protocol, digital FPV |
| Regulation | EASA framework, risk assessment, pre-flight discipline (see [[legal-and-regulatory]]) |
| Data | GPS-tagged logging, sensor data formats, post-processing |

No other single student project delivers this breadth at this cost. The drone
either flies correctly or it does not — feedback is immediate and unambiguous.
There is no partial credit. A blinking LED is not the same as a stable hover.

### What the platform enables after the build

A completed libdrone is not the endpoint of the workshop — it is the starting
point. The GX12 payload interface means the drone can carry any instrument
you design and build to the standard. The open firmware means you can modify
the flight behaviour. The open hardware means you can change the frame geometry.

The most important skill the build develops is not any of the specific
techniques — it is the habit of working with systems where every component is
understood and auditable. This habit transfers to every future engineering
project.

### Why open source specifically

Every component in libdrone's software stack is open source. This means:

- The firmware that controls the motors can be read, verified, and modified
- The radio protocol specification is public — no vendor can break your RC link
  by releasing an incompatible update
- The CAD files are parametric and open — you can change any dimension
- The documentation is free — no licence, no subscription, no DRM

A student who learns on open tools owns their skills. The tools will always be
available to them. A student who learns on proprietary tools can only work
where those tools are licensed. The career argument is direct: open-source
contribution is a public portfolio that any employer can see and verify.

### Why building beats buying

A bought drone is opaque. You cannot know what the firmware does to your data.
You cannot fix it when it breaks beyond the vendor's supported repair window.
You cannot extend it beyond what the vendor permits. You cannot audit it for
a security-sensitive deployment.

A built drone is transparent. You know what every component does because you
installed it. You can repair it in the field because you understand the failure
hierarchy. You can adapt it because the design is open. You can audit it because
every line of code and every CAD file is public.

The build is not the price of admission. The build is the point.

---

## Reference

### Workshop participant prerequisites

No prior experience is required to attend a libdrone workshop. Participants
who will benefit most:

- Can use a computer at a basic level (file management, browser)
- Are comfortable with hand tools (screwdrivers, hex keys)
- Have some soldering experience (helpful but not required — taught in workshop)
- Are curious about how things work

The workshop covers the full build sequence over multiple sessions. Participants
who complete the workshop will have flown a drone they built themselves.

### What to expect from the workshop

| Session | Content |
|---|---|
| 1 | Why drones, platform overview, EASA basics, print coupon validation |
| 2 | Frame assembly, motor mount installation, arm attachment |
| 3 | Electronics installation, wiring, capacitors, conformal coating |
| 4 | Software commissioning, Betaflight, EdgeTX, first power-on |
| 5 | Acceptance validation, maiden flight, Blackbox review |
| 6 | Payload introduction, air quality mast, first data collection flight |

---

## Procedure

<!-- not applicable — this is an orientation article -->

---

## Rationale

### Why the workshop uses libdrone and not a commercial kit

Commercial drone kits abstract the engineering. You follow instructions to
assemble pre-designed parts and configure pre-written firmware. The result
is a drone you can fly but not understand. When it breaks, you are dependent
on the manufacturer. When it is updated, you lose any customisations.

libdrone workshops expose every layer: why each component exists, what failure
mode it protects against, what the physics behind each design decision is.
The extra complexity is the curriculum. Understanding the system — not just
operating it — is the learning outcome.

---

## Connections

requires: []
related:
  - [[platform-overview]]
  - [[foss-principles]]
  - [[legal-and-regulatory]]
  - [[civilian-preparedness]]
leads_to:
  - [[procurement]]
  - [[prep-and-parametrics]]
  - [[coupon-validation]]
