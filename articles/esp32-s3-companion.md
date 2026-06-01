---
id: esp32-s3-companion
title: "ESP32-S3 companion board"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: libdrone
topic:
  - iff-deconfliction
personas:
  - 1.builder
  - 3.payload-dev
  - 8.architect
  - 9.defense
platform:
  - ghost
  - wing
lang: en
licence: CC BY-SA 4.0
---

## Summary

The ESP32-S3 companion board is a mandatory component on Ghost and Wing,
running three concurrent firmware tasks over a UART MAVLink2 connection to
the flight controller: a MAVLink-to-CoT bridge that feeds position and attitude
data to ATAK, an EASA-compliant Remote ID broadcast over WiFi NAN and BLE 5.0,
and a GPIO interface reserved for future allied IFF hardware modules. It is
distinct from the LCM-1 (Pi Zero 2W) companion in both capability and role:
the ESP32-S3 handles IFF and deconfliction; the LCM-1 handles onboard compute
and mission processing. An EMCON kill switch on the airframe body cuts all
ESP32-S3 radio frequency emissions simultaneously without affecting flight.

---

## Concept

### The three firmware tasks

**Task 1 — MAVLink→CoT bridge:** The ESP32-S3 connects to the FC UART
(UART6, labelled COMPANION, at 921600 baud) and receives the continuous
ArduPilot MAVLink2 telemetry stream. It parses GLOBAL_POSITION_INT and
HEARTBEAT messages, converts the position and attitude data to Cursor on
Target (CoT) XML format, and multicasts UDP CoT packets to the local
network. ATAK clients on the same network receive these packets and display
the aircraft as a blue icon on the tactical map — a blue rotary-wing icon
(CoT type `a-f-A-M-H-Q`) for Ghost, a blue fixed-wing icon
(`a-f-A-F-W`) for Wing.

This is the lowest-latency IFF layer. Position updates flow at the ArduPilot
telemetry rate (5–10 Hz) with approximately 50–100 ms latency from GPS fix
to ATAK display. No internet connection is required — the CoT bridge operates
entirely on the local WiFi network created by the ELRS Backpack or a field
router.

**Task 2 — Remote ID broadcast:** EASA regulation (EU 2019/947 and implementing
acts) requires all drones above 250 g operating in Open or Specific category
to broadcast Remote ID containing: operator ID, drone position (GPS), drone
altitude, drone speed, and session ID. The ESP32-S3 broadcasts this data
simultaneously over WiFi NAN (network announcement) and Bluetooth 5.0 BLE
using the ASTM F3411-22a Remote ID standard. Both broadcast channels are
active simultaneously to maximise receiver compatibility.

**Task 3 — IFF GPIO interface:** GPIO pins 3 and 4 on GX12-7 Connector B
are reserved for a future allied IFF hardware module. The ESP32-S3 firmware
includes a GPIO interrupt handler on these pins that can activate a challenge-
response IFF sequence when triggered by an external hardware module. No IFF
hardware module exists yet — the interface is forward-compatible. Adding a
national IFF module requires only a firmware update, not airframe modification.

### EMCON kill switch

The EMCON kill switch is a latching toggle mounted on the Ghost or Wing
airframe body, accessible without tools. It cuts power to the ESP32-S3's
radio frequency section (WiFi and BLE transceivers) simultaneously. Flight
operations are unaffected — the ESP32-S3 continues to parse MAVLink and
log to MicroSD (on Wing), but no RF is emitted. The IR strobe circuit is
independent of the kill switch and cannot be cut by it.

EMCON levels and their meaning: → [[operational-security]].

### Distinction from LCM-1

LCM-1 (Raspberry Pi Zero 2W): Linux-based companion computer for onboard
processing — MAVLink bridging over WiFi hotspot, KML generation, QGroundControl
relay, heavy compute. Optional on all ArduPilot platforms.

ESP32-S3: microcontroller, no Linux, runs firmware. IFF bridge, Remote ID,
GPIO interface. Mandatory on Ghost and Wing. The two can coexist: LCM-1 on
the Pi bay, ESP32-S3 on its dedicated mount, sharing the 5V BEC rail but
on separate UARTs.

---

## Reference

| Parameter | Value |
|---|---|
| Module | ESP32-S3 Mini + MicroSD breakout |
| FC connection | UART6 (labelled COMPANION), 921600 baud, MAVLink2 |
| Protocol | SERIAL6_PROTOCOL=2 (MAVLink2) |
| CoT multicast | UDP 239.2.3.1:6969 (ATAK default) |
| Remote ID standard | ASTM F3411-22a |
| Remote ID channels | WiFi NAN + BLE 5.0 (simultaneous) |
| IFF GPIO | Connector B GPIO 3 + 4 (reserved) |
| Power | 5V from FC BEC, ~200 mA |
| Mass | ~12 g (module + wiring) |
| EMCON kill switch | Cuts RF; MicroSD logging continues |

---

## Procedure

### Install ESP32-S3 on Ghost or Wing

1. Mount ESP32-S3 module on dedicated mount above the GPS mast base
   (Ghost) or fuselage spine (Wing).
2. Wire UART6 TX/RX to ESP32-S3 RX/TX. Wire 5V and GND from BEC.
3. Set `SERIAL6_PROTOCOL=2`, `SERIAL6_BAUD=921` in ArduPilot parameters.
4. Flash ESP32-S3 firmware (LD-IFF-FW, planned — see Ghost §16 status).
5. Verify CoT bridge: power on, check ATAK for aircraft icon within 10 s
   of GPS lock.
6. Verify Remote ID: use a BLE scanner app to confirm broadcast packets.
7. Test EMCON kill switch: confirm ATAK icon freezes and BLE packets stop
   when switch is activated. Confirm MAVLink log continues on MicroSD.

---

## Rationale

The ESP32-S3 was selected over a dedicated Remote ID module (Dronetag Mini,
~€90) for Ghost and Wing because it combines Remote ID with the CoT bridge
and GPIO interface in one component at lower cost (~€12). The Dronetag Mini
is listed in the Ghost BOM as an alternative for builds where the ESP32-S3
firmware is not yet available — the firmware development is a planned milestone,
not a current deliverable. For builds that need Remote ID immediately without
waiting for the firmware, the Dronetag Mini is the fallback.

---

## Connections

```yaml
requires:
  - [[iff-architecture]]
  - [[iff-layers]]
  - [[serial-protocols]]
  - [[ardupilot-copter]]
related:
  - [[ghost-variant]]
  - [[wing-variant]]
  - [[operational-security]]
  - [[remote-id-compliance]]
  - [[payload-sdk]]
leads_to:
  - [[iff-architecture]]
  - [[operational-security]]
```
