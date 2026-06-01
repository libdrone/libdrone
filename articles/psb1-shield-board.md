---
id: psb1-shield-board
title: "PSB-1 payload shield board"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - payload-architecture
personas:
  - 3.payload-dev
  - 1.builder
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The PSB-1 (Payload Shield Board 1) is the reference hardware implementation
of the libdrone GX12 payload interface. It provides all required discrete
protection and power management components — master enable MOSFET, diode-OR
gate, 3.3V LDO regulator, I2C pull-ups, GPIO protection resistors — pre-built
and tested, so payload developers start from a known-good hardware baseline
rather than designing these components from scratch for each payload. The
PSB-1 can be built on perfboard in one evening with 12 components, or ordered
as a fabricated PCB.

---

## Concept

### What the PSB-1 provides

The interface specification (→ [[payload-electrical-interface]]) defines what
signals are available at the GX12 connectors. It does not tell a payload
developer what components are needed to use those signals safely. The PSB-1
answers that question with a complete, tested circuit:

**Master enable MOSFET**: the 5V supply from PIN A1 is not always live. The
payload must be switchable by the pilot via GPIO1. An N-channel MOSFET
(IRLML6344) in the 5V supply path provides this switching with negligible
voltage drop (< 50 mV at 1A).

**Diode-OR logic**: the master enable switch has two sources — the physical
latching switch on the mast body, and AUX GPIO1 from the FC. Either source
alone should enable the payload. A diode-OR circuit (two 1N4148 diodes with
a common anode) combines both sources onto the MOSFET gate. If the physical
switch is ON, the payload is enabled regardless of the radio switch. If the
physical switch is OFF, the radio switch controls it.

**3.3V LDO**: the switched 5V rail from the MOSFET output feeds a
MCP1700-3302E LDO producing regulated 3.3V for the ESP32-S3 and I2C sensors.
The LDO powers down when the MOSFET switches off — the MCU and all sensors
lose power cleanly with no residual current draw.

**I2C pull-ups**: 4.7 kΩ resistors on SCL/SDA, fitted via solder bridge.
Install when the payload cable is longer than 200 mm. Leave open (solder
bridge not made) when the FC's own pull-ups are sufficient.

**GPIO protection**: 10 kΩ series resistors on AUX GPIO1 and GPIO2 before
they reach the MCU pins. Limits current in case of inadvertent voltage
mismatch and provides ESD protection.

---

## Reference

### PSB-1 bill of materials

| Qty | Part | Value | Package | Notes |
|---|---|---|---|---|
| 1 | IRLML6344 | N-ch MOSFET | SOT-23 | Master enable switch |
| 1 | IRLML6344 | N-ch MOSFET | SOT-23 | Optional camera switch (omit if not needed) |
| 2 | 1N4148 | Signal diode | DO-35 | Diode-OR for gate drive |
| 1 | MCP1700-3302E | 3.3V LDO | SOT-23 | 3.3V rail for MCU and sensors |
| 2 | 4.7 kΩ | Resistor | 0805 or TH | I2C pull-ups — solder bridge to install |
| 2 | 10 kΩ | Resistor | through-hole | GPIO protection |
| 1 | 10 kΩ | Resistor | through-hole | MOSFET gate pull-down |
| 1 | 100 nF | Ceramic cap | through-hole | LDO input decoupling |
| 1 | 10 µF | Ceramic or electrolytic | through-hole | LDO output decoupling |
| 1 | LED + 1 kΩ | Any colour | — | Payload active indicator |
| 1 | Latching SPDT | Miniature | — | Physical master switch |
| 2 | GX12-7 female | Cable mount | — | Payload-side connectors |

Total component cost: approximately €5–8.

### PSB-1 signal headers

**Connector A header (J1) — 2.54 mm pitch:**

| Pin | Signal | From GX12 |
|---|---|---|
| 1 | 5V_SW | A1 — switched by MOSFET |
| 2 | GND | A2 |
| 3 | UART4_TX | A3 — FC commands |
| 4 | UART4_RX | A4 — MSP to FC |
| 5 | I2C_SCL | A5 |
| 6 | I2C_SDA | A6 |

**Connector B header (J2) — 2.54 mm pitch:**

| Pin | Signal | From GX12 |
|---|---|---|
| 1 | GND_SHLD | B1 |
| 2 | GPS_RX | B2 — MCU UART RX |
| 3 | UART5_TX | B3 |
| 4 | UART5_RX | B4 |
| 5 | GPIO1 | B5 — through 10 kΩ |
| 6 | GPIO2 | B6 — through 10 kΩ |

**MCU header (J3/J4)**: matches ESP32-S3 mini dev board pinout. All GX12
signals pre-routed to correct ESP32-S3 GPIO pins per `libdrone.py` default
pin map — no additional wiring required between PSB-1 and ESP32-S3.

---

## Procedure

### Bench test sequence before first flight

With no MCU installed:

1. Connect GX12 female connectors to drone. Battery connected, drone powered.
2. Payload master switch ON. Measure 5V at J1 PIN 1. Should be 4.85–5.15V.
3. Measure 3.3V at LDO output. Should be 3.28–3.32V.
4. Payload master switch OFF. Measure J1 PIN 1. Should drop to 0V within
   100 ms.
5. Toggle AUX GPIO1 from TX16S. Measure J1 PIN 1. Should switch on and off
   with the radio switch.

With ESP32-S3 installed:

6. Flash `libdrone.py` test sketch. Power on via payload switch.
7. Verify OSD test string appears in HDZero goggles within 5 seconds.
8. In serial monitor (57,600 baud on GPS port): verify NMEA sentences arriving
   when drone has GPS fix.
9. From TX16S send ENABLE command: payload should respond OK in serial log.
10. Payload is ready for integration with sensor hardware.

---

## Rationale

### Why diode-OR and not a microcontroller-controlled switch

A microcontroller-controlled switch would offer more flexibility but introduces
a software failure mode: if the MCU crashes or hangs, the pilot loses the
ability to disable the payload via radio switch. The diode-OR circuit is
purely hardware — it cannot crash. Physical switch ON always enables the
payload regardless of MCU state. This is a safety-critical design choice:
hardware OR is more reliable than software AND for a safety function.

### Why the PSB-1 is a reference design and not a mandatory component

The ICD defines the interface. The PSB-1 shows one correct way to implement
it. A payload developer may design their own equivalent circuit, use a
different MCU, or integrate the protection components differently — provided
the electrical limits and protocol contracts in the ICD are met. The PSB-1
is a productivity tool that eliminates the "what components do I need" question
for first-time payload builders.

---

## Connections

requires:
  - [[payload-electrical-interface]]
  - [[payload-software-protocol]]
related:
  - [[gx12-connector-standard]]
leads_to:
  - [[payload-integration]]
