---
id: payload-electrical-interface
title: "Payload electrical interface"
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
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The libdrone payload electrical interface provides power, ground, two UART
channels, I2C, a GPS tap, and two GPIO lines across the dual GX12-7 connectors.
The 5V supply (Connector A PIN 1) is limited to 2A continuous — payloads
requiring more must supply their own regulation from the ESC bus. All logic
is 3.3V and not 5V-tolerant. The GPS tap (Connector B PIN 2) is strictly
read-only via a 1 MΩ series resistor on the drone side — driving this pin
from the payload will corrupt the flight controller's GPS data.

---

## Concept

### Why 5V and not 12V or raw battery

The FC's internal BEC provides a regulated 5V at up to 2A — clean, regulated,
already present. Payloads designed for 5V operate on this directly without
any additional regulation hardware. Providing raw battery voltage (21–25V)
would require every payload to carry its own step-down circuitry, adding
mass, cost, and a design task to every payload build.

Payloads requiring more than 2A (or requiring a different voltage) tap the ESC
bus via their own regulator on the PSB-1 shield board. The 2A limit is stated
clearly — it is not a soft guideline.

### Why 3.3V logic and not 5V

The FC's GPIO and UART pins are native 3.3V STM32 outputs. Providing 5V-tolerant
logic would require level-shifting on every signal pin — added complexity with
no benefit for the intended sensor payloads (ESP32-S3 is 3.3V native, SEN66
is 3.3V native, most modern sensor ICs are 3.3V). Any 5V-only sensor requires
a level shifter on the payload side.

### The 1 MΩ GPS tap

Connector B PIN 2 is the TX output of the M10Q GPS receiver on the flight
controller, accessible to the payload as a read-only feed. A 1 MΩ series
resistor is installed on the drone side between the GPS TX pin and the
connector. This resistor is the critical protection element.

Without it: the payload's UART input pin (typically 50 kΩ input impedance
with internal pull-up) would load the GPS TX line and shift its logic levels.
At 57,600 baud, a shifted logic level means the FC receives corrupted GPS
data. With 1 MΩ in series, the loading on the GPS TX line is negligible.

The consequence for payload design: at 57,600 baud with 1 MΩ source impedance,
the signal rise time is limited by the payload input capacitance. Keep the
cable from the connector to the MCU UART RX pin short (< 100 mm) and ensure
no additional capacitance is added. Never drive this pin.

---

## Reference

### Connector A — Signal + Power (left, X = −25 mm)

| Pin | Signal | Direction | AWG | Notes |
|---|---|---|---|---|
| 1 | 5V regulated | Drone → Payload | 24 | FC BEC, **2A continuous maximum** |
| 2 | GND primary | — | 24 | Star ground via FC to ESC GND |
| 3 | UART4 TX | Drone → Payload | 28 | Commands from FC at 115,200 baud |
| 4 | UART4 RX | Payload → Drone | 28 | MSP telemetry payload → FC → OSD |
| 5 | I2C SCL | Drone → Payload | 28 | 400 kHz Fast Mode, FC is master |
| 6 | I2C SDA | Bidirectional | 28 | 400 kHz Fast Mode, open-drain |
| 7 | SPARE | — | — | Reserved — do not connect |

### Connector B — Data + Aux (right, X = +25 mm)

| Pin | Signal | Direction | AWG | Notes |
|---|---|---|---|---|
| 1 | GND shield | — | 28 | Secondary signal ground reference |
| 2 | GPS TX tap | Drone → Payload | 28 | NMEA 57,600 baud, **1 MΩ series on drone side — read-only** |
| 3 | UART5 TX | Drone → Payload | 28 | Secondary communications |
| 4 | UART5 RX | Payload → Drone | 28 | Secondary communications return |
| 5 | AUX GPIO 1 | Drone → Payload | 28 | Master enable, 3.3V logic, ≤10 mA |
| 6 | AUX GPIO 2 | Drone → Payload | 28 | Camera control, 3.3V logic, ≤10 mA |
| 7 | SPARE | — | — | Reserved — do not connect |

### Electrical limits

| Parameter | Limit |
|---|---|
| 5V supply (A1) | 2A continuous — never exceed |
| GPIO logic (B5, B6) | 3.3V logic, NOT 5V tolerant |
| GPIO source current | ≤ 10 mA — use MOSFET for higher loads |
| I2C bus speed | 400 kHz Fast Mode maximum |
| GPS tap (B2) | Read-only — never drive this pin |
| Reserved pins (A7, B7) | Do not connect |

### Wiring recommendations for payload cables

- Twist I2C SCL/SDA pair (A5/A6)
- Twist UART4 TX/RX pair (A3/A4)
- Twist UART5 TX/RX pair (B3/B4)
- Run 5V and GND (A1/A2) separately — no twisting required
- Run GPS tap (B2) and GND shield (B1) separately
- Maximum payload cable length: 300 mm from connector to first PCB
- At cable length > 200 mm: add 2.2 kΩ I2C pull-ups on payload side

### I2C reserved addresses

These addresses are in use by the drone's own sensors. Payload devices must
not use them:

| Address | Device |
|---|---|
| 0x68 or 0x69 | ICM-42688-P IMU (flight controller) |
| 0x0D | QMC5883 magnetometer (M10Q GPS module) |

Address conflict causes corrupted flight controller sensor data. Use an
I2C multiplexer (TCA9548A) if your sensor shares an address with these.

---

## Procedure

### Payload power budget check

Before designing a payload:

1. Sum the 5V current draw of all payload components at peak operation.
2. If total < 1.5A: power from PIN A1 directly via PSB-1 MOSFET switch.
3. If total 1.5–2.0A: power from PIN A1 with careful thermal monitoring
   of the FC BEC during flight. Leave 500 mA headroom for other BEC loads.
4. If total > 2.0A: tap the ESC bus (21–25V) via a separate buck converter
   on the payload mast board. Do not draw >2A from PIN A1 under any condition.

---

## Rationale

### Why GPS tap is 1 MΩ and not a buffer IC

A buffer IC (3.3V logic gate used as a repeater) would provide a clean,
low-impedance GPS signal to the payload at no current cost to the GPS receiver.
However, it adds a component to the drone side of the interface — increasing
build complexity, adding a failure point, and requiring drone-side rework if
the IC fails. The 1 MΩ resistor provides adequate signal quality for payloads
with short cable runs at 57,600 baud (the signal's bandwidth requirement is
modest). For longer runs or faster baud rates, a buffer on the payload side
is the correct solution — it keeps the drone interface simple and moves
complexity to the payload where it belongs.

---

## Connections

requires:
  - [[gx12-connector-standard]]
related:
  - [[payload-software-protocol]]
  - [[power-rail-architecture]]
  - [[emc-noise-sources]]
leads_to:
  - [[payload-software-protocol]]
  - [[psb1-shield-board]]
