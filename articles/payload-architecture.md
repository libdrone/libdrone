---
id: payload-architecture
title: "Payload architecture"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - payload-architecture
personas:
  - 3.payload-dev
  - 6.evaluator
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The payload-architecture domain defines the modular payload system that makes
libdrone a platform rather than a fixed instrument. The dual GX12-7 connector
standard provides a mechanical and electrical interface that is identical across
all libdrone variants. Any payload built to the interface control document works
on any compliant platform. The PSB-1 reference board provides a tested starting
point for payload hardware. The domain covers the connector standard, electrical
pinout, software protocol, and reference hardware implementation.

---

## Concept

<!-- not applicable — this is a domain index article -->

---

## Reference

### Articles in this domain

| Article | Content |
|---|---|
| [[gx12-connector-standard]] | Mechanical interface, D-D bore, positions, retention |
| [[payload-electrical-interface]] | Full pinout, electrical limits, wiring recommendations |
| [[payload-software-protocol]] | MSP OSD bus, command bus, GPS tap, I2C, GPIO |
| [[psb1-shield-board]] | Reference hardware: MOSFET, LDO, protection components |
| [[payload-integration]] | Field swap procedure, mast heights, EASA mass budget |

---

## Procedure

<!-- not applicable -->

---

## Rationale

### Why payload architecture is a separate domain

Payload development is a distinct activity from drone building. A payload
developer needs the ICD, the electrical limits, and the software protocol
— they do not need the FreeCAD Cookbook. Isolating payload architecture as a
domain creates a clean entry point for third-party developers who want to
build payloads without learning the full platform stack.

---

## Connections

requires: []
related:
  - [[gx12-connector-standard]]
  - [[payload-electrical-interface]]
  - [[payload-software-protocol]]
leads_to:
  - [[gx12-connector-standard]]
