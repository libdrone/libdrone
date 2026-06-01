---
id: flight-controller-hardware
title: "Flight controller hardware"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - sensors-fc
personas:
  - 1.builder
  - 5.student
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The flight controller (FC) is the central computer of the drone. It runs the
PID loops, interfaces with all sensors, interprets pilot commands, generates
motor speed commands, logs flight data, and manages failsafe behaviour.
libdrone uses the Matek H7A3-SLIM running Betaflight. Its STM32H7A3 processor
runs at 280 MHz with a hardware floating-point unit — fast enough to execute
the 8 kHz PID loop, RPM filter, GPS parsing, OSD generation, and Blackbox
logging simultaneously. Six hardware UARTs connect all external devices with
dedicated, non-competing serial channels.

---

## Concept

### Why processor class matters

The 8 kHz PID loop runs every 125 µs. Within that window, the FC must: read
filtered gyro data, run three PID calculations, update 36 RPM filter notch
positions, mix motor commands, transmit DShot packets, and receive BiDi eRPM
responses. On older F4-class processors (168 MHz, no hardware FPU for
floating-point), this was not achievable simultaneously — pilots had to choose
between 8 kHz loop rate and the RPM filter. The H7A3's hardware FPU executes
floating-point multiply-accumulate in a single clock cycle, making the PID
calculation essentially free in processor terms.

### DMA (Direct Memory Access)

The gyroscope communicates over SPI at 10 MHz. Without DMA, the CPU would sit
in a busy-wait loop during every sensor read — watching 16 bytes arrive at
10 MHz, doing nothing else for ~13 µs. With DMA, the SPI controller transfers
data autonomously into RAM and raises an interrupt when done. The CPU continues
executing other code during the transfer.

At 8 kHz loop rate, the gyro read happens 8,000 times per second. Without DMA,
~10% of CPU time would be spent waiting for sensor data. With DMA, that time
is spent productively — running the PID loop, parsing GPS, building OSD frames.

### UART assignments on libdrone

Six hardware UARTs, each dedicated to one external device:

| UART | Device | Baud | Protocol |
|---|---|---|---|
| 1 | HDZero VTX | 115,200 | MSP DisplayPort (OSD) |
| 2 | Matek M10Q GPS | 57,600 | UBX |
| 3 | RadioMaster RP2 ELRS | 420,000 | CRSF |
| 4 | GX12 Connector A (payload) | configurable | MSP |
| 5 | GX12 Connector B (payload) | configurable | custom |
| 6 | Companion / spare | 921,600 | MAVLink2 (ArduPilot) / MSP (BF) |

Each UART has hardware inversion on the H7A3-SLIM — no external inverter needed
for CRSF or other protocols that require inverted logic.

### Gyro PCB isolation (moat)

On the H7A3-SLIM, the IMU chip sits inside a slot cut into the PCB substrate —
a "moat" that isolates the gyro mounting island from the rest of the board.
Frame vibration transmitted through the FC mounting screws reaches the PCB
edge but cannot cross the moat to the gyro island. This is mechanical decoupling
at the PCB level — a second isolation stage complementing the floating motor mounts.

---

## Reference

### Matek H7A3-SLIM specification

| Parameter | Value |
|---|---|
| Processor | STM32H7A3, ARM Cortex-M7, 280 MHz |
| FPU | Hardware, single-precision |
| IMU | ICM-42688-P (gyro + accelerometer), SPI |
| Barometer | SPL06-001 |
| OSD | AT7456E |
| UARTs | 6 hardware |
| Motor outputs | 4 × DShot (bidirectional capable) |
| BEC output | 5V / 1A continuous, 2A peak |
| ADC | 16-bit, battery voltage + current inputs |
| Stack pattern | 20 × 20 mm or 30.5 × 30.5 mm |
| Mass | 12 g |
| Firmware | Betaflight (target: MATEKH743SLIM) |

### Critical first-time configuration

1. Flash correct Betaflight target: `MATEKH743SLIM`
2. Set motor count: 4
3. Set motor protocol: DShot600, bidirectional DShot enabled
4. Set motor poles: 14 (BrotherHobby 2507)
5. Assign UARTs per table above
6. Enable RPM filter, 3 harmonics
7. Enable GPS, configure M10Q: UBX, 57,600 baud, Galileo + GPS + BeiDou

---

## Procedure

### FC mounting

1. Mount FC on 30.5 mm stack pattern with M3 nylon standoffs (7 mm height).
   Nylon standoffs isolate the FC from the ESC PCB — breaking the direct
   vibration conduction path through metal.
2. Verify FC orientation matches Betaflight configuration. The arrow on the
   H7A3-SLIM must point forward, or FC orientation must be set in Betaflight
   to match the actual mounting direction.
3. Do not overtighten mounting screws — finger tight plus 1/4 turn. Overtorquing
   deforms the FC PCB and defeats the PCB moat isolation.

---

## Rationale

### Why Betaflight and not ArduPilot for libdrone standard configuration

Betaflight's RPM filter, DShot600 with BiDi telemetry, and the tuning community
around it are the most mature ecosystem for 6-inch-class multirotors. ArduPilot
provides richer autonomous navigation features (waypoints, missions, terrain
following) but its PID loop implementation is less optimised for aggressive
filtering at 8 kHz. The Bandit platform uses ArduPilot specifically for its
navigation capability. Core and Pro use Betaflight for its vibration rejection
and responsiveness on manual flights. The H7A3-SLIM runs both — switching firmware
is a reflash operation.

---

## Connections

requires: []
related:
  - [[imu-gyroscope]]
  - [[rpm-filter]]
  - [[dshot-protocol]]
  - [[closed-loop-control]]
  - [[pid-loop-rate]]
leads_to:
  - [[imu-gyroscope]]
  - [[gnss-gps]]
  - [[pid-loop-rate]]
