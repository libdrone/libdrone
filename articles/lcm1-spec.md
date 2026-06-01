---
id: lcm1-spec
title: "LCM-1 compute module"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - payload-architecture
personas:
  - 3.payload-dev
  - 8.architect
  - 5.student
platform:
  - pro
  - bandit
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

The LCM-1 (libdrone Compute Module, revision 1) is a Raspberry Pi Zero 2W
fitted into the Pi bay on the Backplane. It is the intelligence layer of
the platform: it reads flight state from the FC via companion UART, reads
sensor data from the payload via WiFi, applies threshold logic to decide
what matters, and transmits only meaningful events to the ground operator
through the existing ELRS radio link. The LCM-1 is not a sensor and not
a camera — it is the decision layer that turns raw data streams into
actionable operator alerts. It requires no additional radio hardware and
adds no dependency on cellular networks or cloud services.

---

## Concept

### The problem it solves: data vs information

A sensor payload logging at 1 Hz produces 3,600 data points per flight hour.
Transmitted raw, this saturates the ELRS telemetry link and gives the operator
a firehose they cannot process while also flying. Most of those 3,600 points
are "nothing significant happened." The ones that matter — a PM2.5 spike at
67 µg/m³ while flying over a specific GPS coordinate — are buried.

The LCM-1 inverts this. It watches everything, decides what changed
significantly, and transmits a single alert with context:

    PM2.5: 67 µg/m³ (+55 from baseline) at 48.503°N 15.452°E, altitude 45m, heading NE

The ground operator receives actionable information, not a stream of numbers.

### What the LCM-1 sees

Via companion UART (UART6, 921,600 baud):
- GPS position, altitude, attitude, battery, flight mode, RC switch states
- On Betaflight (Pro/Core): polled via MSP at 2–5 Hz
- On ArduPilot (Bandit): streamed via MAVLink2 automatically

Via WiFi (payload ESP32-S3 connects to Pi hotspot):
- Sensor readings from fitted payload at 1–2 Hz
- Payload status

### Threshold logic — the intelligence layer

The Pi applies configurable thresholds to decide when a reading is
significant enough to transmit. Default thresholds:

    THRESHOLDS = {
        'PM25': 5.0,      # µg/m³ — change triggers transmission
        'CO2':  25.0,     # ppm
        'VOC':  10.0,     # index
        'RAD':  0.05,     # µSv/h — tight: radiation matters early
    }
    HEARTBEAT_INTERVAL = 30   # seconds — always transmit something
    ALTITUDE_MIN_M     = 20   # metres — ignore below this (ground contamination)

Below the minimum altitude, all readings are suppressed — the drone is in
the downwash contamination zone. Above it, a reading is transmitted when it
changes by more than the threshold since the last transmission for that
channel. Every 30 seconds, a heartbeat transmits the current state regardless
of changes — confirming the link is live and logging is active.

The threshold table is configurable via a JSON file on the Pi's SD card,
editable without reflashing. Mission-specific thresholds (lower PM2.5
threshold for air quality research, lower radiation threshold for CBRN
deployments) are applied by editing the config file before the flight.

---

## Reference

### Physical interface

| Parameter | Value |
|---|---|
| Pi bay location | Above Backplane, below payload mast boss pads |
| Pi bay internal dimensions | 72 × 38 × 6 mm |
| Standoff spacing | 58 mm × 23 mm, M2.5 × 5 mm |
| Pi bay fitted on | All standard libdrone builds — every drone is LCM-1 ready |
| Cover plate when LCM-1 not fitted | Printed PETG, zero functional penalty |

### Companion harness

| Pin | Signal | Direction |
|---|---|---|
| 1 | 5V_COMP | Dedicated XL4016 buck → Pi (NOT FC BEC) |
| 2 | GND | Common star ground |
| 3 | FC_TX (UART6) | FC → Pi, MAVLink2 or MSP at 921,600 baud |
| 4 | FC_RX (UART6) | Pi → FC, return path |

UART6 is permanently reserved as COMPANION on all libdrone builds. Never
reassign it. The companion harness is pre-wired during Phase 5 electronics
installation.

### Power

Pi Zero 2W is powered from a dedicated XL4016 buck converter (5.1V, 1A
minimum), independent of the FC BEC. The BEC is already loaded with receiver,
GPS, fan, and payload — the Pi's 200 mA typical draw (400 mA peak at boot)
does not affect the BEC budget.

### Gate: Phase 9 (optional)

The LCM-1 is Phase 9 in the WBS — optional, and gated on Phases 1–8 complete
and the Pro flying reliably with minimum 10 logged flights. Do not build the
LCM-1 until the platform is proven stable.

---

## Procedure

### LCM-1 first integration

1. Print Pi bay cover removal and set aside — bay is already present.
2. Fit Pi Zero 2W on M2.5 × 5 mm standoffs in Pi bay.
3. Connect companion harness JST-SH loom to Pi GPIO pins per pin map.
4. Install companion XL4016 buck converter, output 5.1V, input from battery tap.
5. Configure UART6 in Betaflight as MSP (Pro) or enable MAVLink2 streaming
   (ArduPilot for Bandit).
6. Flash Pi with Raspberry Pi OS Lite. Install LCM-1 firmware package.
7. Edit `/boot/lcm1_config.json` with mission-specific thresholds.
8. Power on. Verify Pi boots (LED pattern). Verify FC data arriving via serial
   log. Verify payload ESP32-S3 connecting to Pi WiFi hotspot.
9. Verify ground station (TX16S → ELRS backpack → tablet QGroundControl)
   shows position and sensor events.

---

## Rationale

### Why WiFi for sensor data and not a direct GX12 wired link

The GX12 connectors are the payload-to-drone interface, not the payload-to-Pi
interface. The Pi reads from the payload via WiFi so that the GX12 wiring
remains clean and fixed — adding a third connection to the GX12 would require
rerouting wires and potentially creating conflicts. WiFi between the payload
ESP32-S3 and the Pi hotspot is short-range (50 cm), effectively lossless, and
requires no additional wiring. The GX12 carries power and FC communications;
WiFi carries sensor data. The separation is intentional.

### Why the LCM-1 is optional and gated on 10 flights

Adding the LCM-1 to a drone that is not yet reliable adds an untested
component to an already complex system. Any instability — Pi crashing, UART
conflict, power draw spike — is much harder to diagnose if the base platform
is also unproven. The 10-flight gate ensures the platform behaviour is well
understood before the intelligence layer is added.

---

## Connections

requires:
  - [[flight-controller-hardware]]
  - [[payload-software-protocol]]
  - [[gx12-connector-standard]]
related:
  - [[payload-electrical-interface]]
  - [[betaflight-setup]]
  - [[gnss-gps]]
  - [[pro-variant]]
leads_to:
  - [[payload-integration]]


[flight-controller-hardware]: flight-controller-hardware.md "Flight controller hardware"
[payload-software-protocol]: payload-software-protocol.md "Payload software protocol"
[gx12-connector-standard]: gx12-connector-standard.md "GX12 connector standard"
[payload-electrical-interface]: payload-electrical-interface.md "Payload electrical interface"
[betaflight-setup]: betaflight-setup.md "Betaflight setup"
[gnss-gps]: gnss-gps.md "GNSS and GPS"
[pro-variant]: pro-variant.md "Pro variant"
[payload-integration]: payload-integration.md "Payload integration"
