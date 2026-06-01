---
id: elrs-mavlink-mode
title: "ELRS MAVLink mode"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: generic
topic:
  - communication-rf
personas:
  - 1.builder
  - 8.architect
  - 2.operator
platform:
  - bandit
  - ghost
  - wing
lang: en
licence: CC BY-SA 4.0
---

## Summary

ELRS MAVLink mode, introduced in ExpressLRS ≥3.5, carries both RC control
channels and bidirectional MAVLink telemetry over a single radio link and a
single flight controller UART. No separate telemetry radio (such as a SiK
433 MHz module) is required. The ELRS transmitter detects MAVLink packets
automatically and switches link mode; on the FC side, the UART protocol is
set to MAVLink2 rather than RCIN — RC channel data is embedded within the
MAVLink stream. This is the link architecture used on all ArduPilot-based
libdrone platforms.

---

## Concept

### What changes in ELRS MAVLink mode

In standard ELRS operation, the link carries RC channel data only: 16 channels
of control input, one direction (TX to RX to FC). Telemetry — battery voltage,
RSSI, GPS data — flows in a separate, low-rate path back to the transmitter and
is displayed on the TX16S screen.

In MAVLink mode, the link becomes bidirectional and higher-bandwidth for data.
The FC outputs a continuous MAVLink2 stream (HEARTBEAT, GLOBAL_POSITION_INT,
BATTERY_STATUS, ATTITUDE, and others) at 460800 baud. The ELRS receiver
passes this stream to the TX module. The TX module makes it available via:
- WiFi bridge (ELRS Backpack) → QGroundControl on laptop or tablet via UDP
  port 14550
- USB-C cable from TX16S to laptop → QGroundControl selects COM port at 460800

RC channel data from the transmitter travels in the opposite direction, embedded
in the same link, and is decoded by ArduPilot when the UART protocol is set
to MAVLink2.

### The stubborn sender improvement

ELRS ≥3.5's stubborn sender system retries undelivered MAVLink packets. Over
a long survey range, packet loss of 10–20% is normal. Without retry, this
produces gaps in the QGC telemetry display and potential mission log corruption.
With stubborn sender, the GCS link quality is maintained even at significant
packet loss — important for Bandit survey missions at 500–1000 m range.

### The critical UART protocol error

The H7A3-SLIM ships with SERIAL2_PROTOCOL=23 (RCIN). In this default state,
ArduPilot treats UART2 as a raw RC input — it reads RC channel pulses but
does not parse MAVLink. Setting SERIAL2_PROTOCOL=2 (MAVLink2) switches the
parser: ArduPilot now reads the MAVLink stream and extracts RC channel data
from within it. Leaving the protocol on 23 while using ELRS MAVLink mode is
the single most common commissioning error — the aircraft will have no RC
control.

---

## Reference

**FC parameters (Bandit/Ghost, UART2):**
    SERIAL2_PROTOCOL,2     ; MAVLink2 — NOT 23 (RCIN)
    SERIAL2_BAUD,460       ; 460800 baud
    RSSI_TYPE,5            ; Telemetry radio mode
    RC_PROTOCOLS,512       ; CRSF/ELRS enabled
    RC_OPTIONS,8448        ; Bit 9: suppress CRSF mismatch
                          ; Bit 13: 420K baud for ELRS

**ELRS TX module (Lua script on TX16S):**
- Link Mode: MAVLink (not Normal)
- Telemetry Ratio: 1:2 (auto-set; cannot be changed in MAVLink mode)
- Packet rate: 100 Hz preferred; 50 Hz minimum for reliable GCS link
- Power: 100 mW default; 250 mW for survey range

**QGroundControl connection options:**
- UDP: TX16S WiFi hotspot (ELRS Backpack) → QGC → UDP 14550
- USB: TX16S USB-C to laptop → QGC selects COM port at 460800 baud

---

## Procedure

### Verify ELRS MAVLink mode on bench

1. Set SERIAL2_PROTOCOL=2 and SERIAL2_BAUD=460 in ArduPilot parameters.
2. Configure ELRS Lua script: set Link Mode to MAVLink.
3. Connect QGroundControl via UDP or USB.
4. Power on aircraft. Within 5 seconds, QGC should display HEARTBEAT and
   show vehicle armed/disarmed status.
5. Move all TX16S sticks and switches. Confirm QGC Radio Calibration page
   shows live channel inputs responding.
6. Verify RSSI value is displayed in QGC HUD (non-zero when TX is on).

If QGC connects but shows no RC channels: SERIAL2_PROTOCOL is still 23.
If QGC does not connect at all: ELRS Link Mode is still Normal, not MAVLink.

---

## Rationale

The decision to use ELRS MAVLink mode over a separate SiK telemetry radio
is driven by weight and hardware simplicity. A SiK 433 MHz module adds 15–30 g,
requires a separate UART, and adds an additional RF source with its own antenna
positioning constraints. On a 450–550 g platform like Bandit, the weight budget
is tight. ELRS MAVLink delivers equivalent GCS functionality with no added
hardware — the RC link hardware that was already required now carries telemetry
as well. The ELRS ≥3.5 stubborn sender improvement removed the previous
reliability concern at survey ranges.

---

## Connections

```yaml
requires:
  - [[elrs-protocol]]
  - [[ardupilot-copter]]
  - [[serial-protocols]]
related:
  - [[ardupilot-commissioning]]
  - [[qgroundcontrol]]
  - [[crsf-protocol]]
  - [[bandit-variant]]
leads_to:
  - [[ardupilot-commissioning]]
  - [[qgroundcontrol]]
```
