---
id: payload-sdk
title: "Payload SDK"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - payload-architecture
personas:
  - 3.payload-dev
  - 5.student
  - 7.contributor
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The libdrone Payload SDK is the complete developer guide for building payloads
on the libdrone platform. It is intended for a builder who has never read the
drone documentation and does not need to build a drone — only access one. The
SDK covers the dual GX12-7 electrical interface, three-bus protocol
architecture, reference payload design (SEN66 air quality module), mechanical
mast standard, field procedures, and compliance requirements. The underlying
technical specifications live in [[gx12-connector-standard]],
[[payload-electrical-interface]], and [[payload-software-protocol]]. This article
is the navigational entry point and design philosophy overview.

---

## Concept

### The SDK philosophy: drone as sealed infrastructure

The drone is sealed infrastructure. Payloads clip on top via two GX12-7
connectors and two M3 boss pads. The drone does not need to know what payload
it carries. A payload developer does not need to understand how the drone
flies. The interface is the contract between drone and payload — and the
contract is fully documented.

This separation has a practical consequence: payload developers can design,
build, and test payloads on the bench using a breakout board (the PSB-1)
without access to a flying drone. The electrical interface is completely
reproducible from the ICD. A payload that passes bench compliance testing
will work on any compliant libdrone platform without modification.

### The three-bus architecture

Every compliant payload implements three communication paths:

**Storage bus** — what happened. Full-resolution sensor data, GPS-tagged,
timestamped, written to MicroSD card on the payload. Remains valid with
no RC link, no WiFi, no ground station. The data is always collected.

**Realtime bus** — what is happening now. Live readings sent via MSP
DisplayPort from the payload ESP32-S3 to the flight controller, overlaid
on the pilot's HDZero goggles OSD. The pilot sees PM2.5, CO2, radiation
level, or camera status without landing. Update rate: 2–10 Hz.

**Control bus** — what to do next. Pilot transmitter switches map to FC
GPIO outputs, which arrive at the payload as 3.3V logic signals. The
payload responds: start logging, stop logging, deploy actuator, change
sample rate. Full pilot authority over payload behaviour in flight.

A payload that only logs to SD card is non-compliant — the pilot has no
visibility. A payload that only shows OSD but ignores pilot commands is
non-compliant — the pilot has no authority. All three buses are mandatory.

### Payload IP protection

CERN OHL-S v2 copyleft applies to modifications of the libdrone platform
hardware. It does not apply to payload designs that use the GX12 interface
standard. A company building a proprietary sensor payload to this SDK retains
full ownership of that payload design. The platform is open. Your payload is
yours.

---

## Reference

### SDK document map

| Article | What it covers |
|---|---|
| [[gx12-connector-standard]] | Mechanical interface, D-D bore, positions, dust caps, retention |
| [[payload-electrical-interface]] | Full pinout, electrical limits, wiring recommendations |
| [[payload-software-protocol]] | MSP OSD framing, command vocabulary, GPS parsing, I2C, GPIO |
| [[psb1-shield-board]] | Reference hardware: MOSFET, LDO, protection components, BOM |
| [[payload-integration]] | Field swap procedure, mast heights, EASA mass budget |

### Reference payload: SEN66 air quality module

| Parameter | Value |
|---|---|
| Sensor | Sensirion SEN66 — PM1/2.5/4/10, temperature, humidity, VOC, NOx, CO2 |
| Compute | ESP32-S3 mini dev board with MicroPython |
| Storage | MicroSD card, JSONL format, 1 Hz GPS-tagged records |
| Realtime | MSP DisplayPort OSD: PM2.5, CO2, VOC, log status |
| Power | 5V from GX12 Connector A PIN 1 via PSB-1 MOSFET switch |
| Mass | ~50–65 g total mast assembly |
| Mast height | 80 mm (medium) or 120 mm (tall — recommended for clean air sampling) |

### Payload compliance levels

| Level | Requirements |
|---|---|
| Mechanical | GX12-7 female connectors, M3 boss pad mounting, dust cap discipline |
| Full | Mechanical + MSP OSD at ≥2 Hz + respond to ENABLE/DISABLE + GPS-tagged storage |

Partial compliance (mechanical only) is acceptable for prototypes. Declare
compliance level explicitly in payload documentation.

---

## Procedure

### Minimum viable payload development sequence

1. Read [[gx12-connector-standard]] — understand the mechanical interface
2. Read [[payload-electrical-interface]] — understand the pinout and limits
3. Read [[payload-software-protocol]] — understand MSP framing and command vocab
4. Build PSB-1 on perfboard — provides all protection and power management
5. Flash ESP32-S3 with MicroPython and libdrone.py template
6. Bench test: verify OSD data appears in goggles, GPS data arrives at 57,600
   baud, GPIO responds to switch
7. Build payload mast from PETG — use standard mast STL or design custom
8. Bench compliance test: all three buses active, all compliance requirements met
9. First flight test: low altitude, short duration, verify all buses in flight

---

## Rationale

### Why a developer-facing SDK is a separate document from the ICD

The ICD ([[gx12-connector-standard]], [[payload-electrical-interface]],
[[payload-software-protocol]]) defines what the interface is and what it
requires. The SDK tells a developer how to build to that interface efficiently.
These are different documents serving different purposes. The ICD is normative
— it defines compliance. The SDK is procedural — it guides implementation.
A developer who reads only the ICD knows what to build but not where to start.
A developer who reads only the SDK knows how to start but may miss compliance
details. Both are needed.

---

## Connections

requires: []
related:
  - [[gx12-connector-standard]]
  - [[payload-electrical-interface]]
  - [[payload-software-protocol]]
  - [[psb1-shield-board]]
  - [[payload-integration]]
leads_to:
  - [[gx12-connector-standard]]
  - [[psb1-shield-board]]
