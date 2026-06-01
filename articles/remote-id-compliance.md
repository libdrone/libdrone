---
id: remote-id-compliance
title: "Remote ID compliance"
version: 1.1.0
date: 2026-06-01
author: jsa
status: released
scope: libdrone
topic:
  - iff-deconfliction
personas:
  - 2.operator
  - 6.evaluator
  - 1.builder
platform:
  - pro
  - ghost
  - bandit
lang: en
licence: CC BY-SA 4.0
---

## Summary

Remote ID is a broadcast function that transmits a drone's identity, GPS
position, altitude, and operator location locally over WiFi Neighbor Awareness
Networking (NAN) and/or Bluetooth 5.0 Long Range. Whether it is legally required
for a given libdrone platform and operation is covered in the single source of
truth, [[legal-and-regulatory]]; this atom covers the technical implementation.
Where it is required, a compliant module (Dronetag Mini, BlueMark DB120, or
equivalent) connects to the FC UART to receive GPS position and transmits the
required data autonomously, total mass under 10 g. Remote ID is a separate thing
from operator registration — see [[legal-and-regulatory]] for what applies.

---

## Concept

### What Remote ID broadcasts

Every Remote ID transmission contains:
- UAS ID (operator registration number + serial number)
- Current GPS latitude, longitude, altitude
- Speed and heading
- Operator position (GPS position of the ground controller)
- Timestamp

This data is broadcast locally at approximately 1 Hz via WiFi NAN (range
~300 m) and BLE 5.0 Long Range (range ~100 m). Any smartphone with a
Remote ID receiver app in range can read the identity and position of every
compliant drone overhead.

### What Remote ID does not provide

Remote ID is civilian airspace transparency, not tactical IFF:
- It does not authenticate the identity — spoofing is possible
- It does not reach military tactical networks
- It does not provide friend/foe status to combat forces
- Its broadcast range is limited to ~300 m

In a contested environment where broadcasting position is a liability,
evaluate whether broadcasting is tactically appropriate.
This is a mission planning decision, not a technical one.

### Operational security consideration

Remote ID broadcasts GPS position to any receiver in range. In environments
where the operator's position or the drone's route should not be disclosed
to potentially hostile observers, the mandatory broadcast nature of Remote ID
is a security concern. Whether an opt-out or modified operation is available
is a regulatory question — see [[legal-and-regulatory]] and consult the national
authority if this concern applies to your deployment.

---

## Reference

### Compliant module options

| Module | Mass | Interface | Standards |
|---|---|---|---|
| Dronetag Mini | 9 g | UART (GPS feed) | EASA, FAA |
| BlueMark DB120 | 8 g | UART (GPS feed) | EASA |
| u-blox RCB-F9T (integrated) | — | Internal | EASA |

### FC integration

The Remote ID module connects to a spare UART on the H7A3-SLIM, receiving
GPS NMEA data (or MAVLink position) to populate the broadcast. On libdrone
Pro/Ghost, UART6 (companion/spare) is available. Configure in Betaflight
Configurator → Ports → UART6: GPS Passthrough or MSP, depending on the
module's requirements.

### Operator registration

Remote ID and operator registration are separate obligations — having one does
not satisfy the other. What registration requires and where to do it is in
[[legal-and-regulatory]]. The Remote ID module must be programmed with the
operator ID once obtained:
- Program the operator ID into the Remote ID module
- Display the ID on the drone (label or engraving)

---

## Procedure

### Installing and configuring Remote ID module

1. Mount the module on or near the Platform using a small M2 screw or
   foam-tape pad. Keep clear of the GPS antenna skyview.
2. Connect UART TX/RX to FC UART6 TX/RX (cross-connect: module RX to FC TX).
3. In Betaflight: configure UART6 as GPS passthrough at 57,600 baud.
   The module receives NMEA sentences and uses them for its broadcast.
4. Power module from the 5V GX12 rail or directly from the FC BEC
   (check module current draw — most are <50 mA).
5. Program the operator e-ID into the module via its configuration app.
6. Verify broadcast: download a Remote ID receiver app (e.g. OpenDroneID)
   on a smartphone. Power on the drone outdoors with GPS fix.
   The drone should appear on the app within 30 seconds.

---

## Rationale

### Why a dedicated module and not software Remote ID on the FC

Betaflight does not implement Remote ID natively — it is not designed for
regulatory broadcast functions. Adding Remote ID to Betaflight firmware would
require significant changes that are outside the project's scope and would
create a dependency on regulatory compliance in flight-critical firmware.
A dedicated module keeps compliance isolated from flight-critical code: if
the Remote ID module fails, the drone still flies safely. If Remote ID were
in Betaflight, a compliance bug could introduce flight bugs.

---

## Connections

requires:
  - [[iff-layers]]
  - [[legal-and-regulatory]]
related:
  - [[emissions-control]]
  - [[gnss-gps]]
leads_to:
  - [[emissions-control]]
