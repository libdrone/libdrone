---
id: sk-payload-developer-guide
title: "Payload Developer Guide"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 3.payload-dev
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

After reading this guide, the payload developer can design, build, test, and
deploy a compliant payload on any libdrone platform without reading the drone
documentation — only the payload interface documentation. This guide is
written for someone who has access to a libdrone but may have no interest
in how it flies.

---

## Concept

### The key insight: the drone is sealed infrastructure

The drone body does not open for payload access. The top surface is a platform
with a defined electrical and mechanical interface. You connect your payload
via two GX12-7 aviation connectors and two M3 boss pad screws. The drone does
not know or care what payload you attached. Your payload does not need to know
how the drone flies. The interface is the contract.

This separation means you can develop and bench-test your payload completely
independently of the flying drone. The PSB-1 breakout board provides the
electrical interface on your bench. The GPS simulator or a real drone with
a bench power supply provides test data. Your payload can reach full
functional compliance before its first flight.

### The mechanical interface

→ [[gx12-connector-standard]] covers everything you need to know about the
physical connectors: the D-D bore anti-rotation profile (not optional — a
round bore means the connector will rotate and back off the retention nut in
flight), the double-nut Loctite retention, and the dust cap discipline that
protects the pins when no payload is fitted. The connector positions are at
X = ±25 mm from centreline, Y = −66 mm from nose.

Your payload mast attaches via 2× M3 × 8mm screws into the boss pads on the
Backplane at 20mm spacing. The mast height determines how far above the
downwash zone your payload sits — for atmospheric sensors, use the 120mm tall
mast. → [[payload-integration]] has the mast height selection rationale and the
EASA mass budget (maximum 93g for A2 compliance).

### The electrical interface

→ [[payload-electrical-interface]] is your primary electrical reference.
Two connectors, 12 signals:

Connector A (LEFT) carries power (5V, 2A maximum — this limit is hard, not
advisory) and primary communications: UART4 for FC-to-payload commands, I2C
for the shared sensor bus.

Connector B (RIGHT) carries the GPS tap (1MΩ series resistor on the drone
side — read-only, never drive this pin), secondary UART5, and two AUX GPIO
lines that map to pilot radio switches.

All logic is 3.3V. Not 5V tolerant. If your sensor or MCU requires 5V logic,
add a level shifter on the payload side.

### The reference hardware: PSB-1

Before designing your own power management circuit, build the PSB-1.
→ [[psb1-shield-board]] contains the complete BOM (12 components, approximately
€5–8) and the bench test sequence. The PSB-1 provides the MOSFET master
enable, diode-OR gate for physical switch and GPIO, 3.3V LDO, I2C pull-ups,
and GPIO protection resistors — everything you need to start writing firmware
the same afternoon.

### The three-bus protocol

→ [[payload-software-protocol]] is the firmware contract. Three buses are
required for compliance:

The **realtime bus** sends live readings to the pilot's goggles via MSP
DisplayPort on UART4 RX. The protocol framing and update rate requirements
are in the article, along with a complete MicroPython implementation.

The **control bus** receives plain-text commands on UART4 TX from the FC.
Your payload must at minimum respond to `ENABLE\n` and `DISABLE\n`. The
pilot can send these from their radio switch via the FC GPIO mapping.

The **storage bus** writes GPS-tagged data to your SD card. The GPS position
arrives at 57,600 baud on Connector B PIN 2 as NMEA sentences — the 1MΩ
series resistor on the drone side limits the signal amplitude, so keep
your cable run short.

A payload that only logs to SD with no OSD and no command response is
non-compliant. The pilot needs visibility and authority.

### The intelligence layer: LCM-1

For payloads that generate high-volume continuous data streams, consider the
LCM-1 intelligence layer. → [[lcm1-spec]] covers the Raspberry Pi Zero 2W in
the Pi bay: it reads sensor data from the payload via WiFi and FC state via
companion UART, applies configurable threshold logic, and transmits only
meaningful events through the existing ELRS link to the ground operator.
This avoids saturating the telemetry link with data the pilot cannot process
while flying.

---

## Reference

### Compliance requirements summary

| Requirement | Article | Key constraint |
|---|---|---|
| Mechanical | [[gx12-connector-standard]] | D-D bore, double-nut, dust caps |
| Electrical | [[payload-electrical-interface]] | 5V 2A max, 3.3V logic, GPS pin read-only |
| Realtime OSD | [[payload-software-protocol]] | MSP DisplayPort, ≥ 2 Hz |
| Command response | [[payload-software-protocol]] | ENABLE/DISABLE minimum |
| GPS-tagged storage | [[payload-software-protocol]] | NMEA GGA parse, tag all records |
| Mass budget | [[payload-integration]] | ≤ 93g for EASA A2 |

### Development sequence

1. Build PSB-1 → [[psb1-build-guide]]
2. Flash ESP32-S3 with MicroPython and libdrone.py template
3. Bench test: OSD string in goggles, GPS NMEA in serial monitor, GPIO responds
4. Build payload mast from provided STL or custom PETG design
5. Bench compliance test: all three buses active
6. First flight: low altitude, short duration, verify all buses in flight

---

## Procedure

### Bench testing without a flying drone

Connect the PSB-1 to a bench power supply set to 5V (current limit 500mA).
Connect a USB-serial adapter to UART4 RX and monitor for MSP frames. Simulate
GPS input by replaying NMEA sentences from a file via another USB-serial
adapter to Connector B PIN 2.

This validates your firmware completely before the first drone connection.

---

## Rationale

The Payload SDK (V2.4.6) was written as a standalone document complete with
pinout tables, protocol framing, and code examples. This skeleton delegates
all specifications to atoms and provides the developer narrative. A payload
developer reading this guide gets the concepts and the development sequence;
they follow links to the atoms for the exact specifications they need.

---

## Connections

requires: []
related:
  - [[sk-complete-build-guide]]
  - [[sk-engineering-101]]
leads_to:
  - [[sk-complete-build-guide]]
