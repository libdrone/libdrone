---
id: pro-variant
title: "Pro variant"
version: 1.0.0
date: 2026-04-15
author: jsa
status: released
scope: libdrone
topic:
  - resilience-community
personas:
  - 6.evaluator
  - 1.builder
  - 3.payload-dev
  - 8.architect
platform:
  - pro
lang: en
licence: CC BY-SA 4.0
---

## Summary

libdrone Pro is the reference platform of the libdrone family — the 6-inch,
6S, research and commercial variant around which the GX12-7 payload interface
standard, the five-layer airframe architecture, and the full documentation
stack were designed. Where Core teaches the fundamentals and Bandit enables
autonomous missions, Pro is the platform that carries real payloads to real
operational tasks: environmental monitoring, aerial survey, research
instrumentation, and civilian situational awareness. It is the most capable
and most expensive family member, and the one that defines what every other
variant is compared against.

---

## Concept

### What Pro is for

Pro is a payload platform first and a flying platform second. The 330mm
True-X wheelbase, 6S 1800mAh power system, and PC-CF arm construction exist
to support 150–250g of sensor payload reliably in the conditions where that
payload is useful — not to achieve maximum flight time or minimum weight.
Every structural and electronics decision traces to the payload requirement:
the five-layer airframe creates the Platform and Backplane geometry that the
GX12-7 payload interface requires; the 6S power system provides the current
capacity for high-draw payloads; the HDZero digital FPV system provides the
clean live feed the payload operator needs.

### The GX12-7 payload interface

Pro's defining commercial feature is the dual GX12-7 payload interface — two
7-pin aviation connectors, one carrying power and primary communications
(Connector A, left), one carrying secondary communications and auxiliary GPIO
(Connector B, right). Any payload built to the ICD LD-PAY-002 specification
works on Pro without modification, and the same payload works on Bandit, Ghost,
and Wing — the standard is family-wide.

This interface is what makes Pro a platform rather than a drone. A payload
developer writes to the GX12-7 standard once and gets access to all four
capable family members as deployment targets. See → [[gx12-connector-standard]]
and → [[gx12-icd]] for the full specification.

### The intelligence layer

Every Pro is built Pi-ready from the first print: a 6mm PETG tray above the
Backplane, a pre-wired 4-wire companion harness to FC UART6, and a dedicated
buck converter on the battery rail — installed whether or not a Pi Zero 2W
is ordered. When the LCM-1 companion module is fitted, Pro gains onboard
compute: MAVLink bridge, sensor data aggregation, contextual alerting, and
WiFi hotspot for live payload data streaming. See → [[lcm1-spec]].

### PC-CF arms

Pro uses PC-CF (polycarbonate carbon fibre) printed arms rather than PETG.
The higher modulus of PC-CF reduces arm flex at the 330mm wheelbase, keeping
the IMU vibration profile clean. The trade-off is printer requirements: PC-CF
needs a hardened steel nozzle and a heated enclosure. This is why Core uses
PETG — the educational context cannot assume enclosed printers, and 220mm
arms do not need the stiffness that 330mm arms do.

---

## Reference

| Parameter | Value |
|---|---|
| Wheelbase | 330mm (6-inch class, True-X) |
| Flight system | Betaflight |
| FC | Matek H7A3-SLIM |
| ESC | Pilotix 75A AM32 4-in-1 |
| Motors | BrotherHobby Avenger V2 2507 1750KV |
| Battery | 6S 1800mAh XT60 |
| Video | HDZero Freestyle V2 (digital) |
| AUW target | ~807g bare; ~860g with sensor payload |
| Payload interface | Dual GX12-7 A/B (mandatory, fully wired) |
| Arm material | PC-CF |
| Companion bay | LCM-1 ready (Pi Zero 2W) |
| BOM cost | ~€380 |
| EASA category | Open A2 |

**Shared SKUs with Core and Bandit:** Matek H7A3-SLIM, Happymodel EP2 Nano,
3mm CF rod stock, M2/M3 hardware.

---

## Procedure

<!-- not applicable — build and commissioning are covered in
[[sk-complete-build-guide]], [[betaflight-setup]], and [[maiden-flight]].
For payload integration: [[sk-payload-developer-guide]] -->

---

## Rationale

Pro is the platform from which all others diverge. Core removes capability
to reduce cost and regulatory weight. Bandit replaces Betaflight with
ArduPilot to enable autonomous missions. Ghost scales up for endurance.
Wing changes airframe class entirely. Each departure is defined relative to
Pro's baseline. The Pro specification is therefore the single most important
platform document in the family — it defines what "standard" means for every
comparison that follows.

---

## Connections

requires:
  - [[platform-overview]]
related:
  - [[platform-selection]]
  - [[gx12-connector-standard]]
  - [[gx12-icd]]
  - [[lcm1-spec]]
  - [[sandwich-structure]]
  - [[pccf]]
  - [[digital-fpv]]
  - [[betaflight-setup]]
  - [[sk-complete-build-guide]]
leads_to:
  - [[gx12-connector-standard]]
  - [[payload-architecture]]
  - [[sk-complete-build-guide]]
