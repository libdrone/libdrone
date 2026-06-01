---
id: serial-protocols
title: "Serial communication protocols"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - communication-rf
personas:
  - 5.student
  - 3.payload-dev
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

A drone uses four serial communication protocols, each matched to its use
case: UART for point-to-point asynchronous data (GPS, RC receiver, VTX,
payload), SPI for high-speed synchronous sensor reads (IMU gyroscope),
I2C for multi-device low-bandwidth sensor buses (payload I2C chain), and
MAVLink for structured bidirectional mission and telemetry data (ArduPilot
on the Bandit platform). Understanding which protocol is appropriate for
a new connection — and why — prevents common integration errors like using
I2C for a high-bandwidth sensor or UART for a multi-device bus.

---

## Concept

### UART — Universal Asynchronous Receiver-Transmitter

UART is asynchronous: the transmitter and receiver agree on baud rate in
advance, then exchange data without a shared clock signal. A start bit
signals the beginning of each byte; a stop bit signals the end. The receiver
synchronises its clock to the start bit.

This clock-free design makes UART simple and universally supported. Every
microcontroller ever manufactured has at least one UART. Point-to-point —
one transmitter, one receiver per wire pair. Not suitable for multi-device
buses.

Uses on libdrone: GPS (UART2, 57,600 baud), ELRS receiver (UART3, 420,000
baud), VTX OSD (UART1, 115,200 baud), payload UART4 and UART5.

### SPI — Serial Peripheral Interface

SPI is synchronous: a shared clock (SCK) times each bit. The master drives
SCK, MOSI (Master Out Slave In), and chip-select (CS); the slave drives MISO
(Master In Slave Out). All four signals run simultaneously — full duplex.

The shared clock eliminates baud-rate negotiation and allows much higher
speeds than UART: 10–50 MHz is common. At 10 MHz, a 16-byte sensor read
takes ~13 µs — fast enough for 32 kHz gyro sampling.

Uses on libdrone: ICM-42688-P IMU gyroscope (SPI, 10 MHz). Not used for
payload connections — connector pin count is limited.

### I2C — Inter-Integrated Circuit

I2C uses just two wires (SDA + SCL) shared by multiple devices. Each device
has a 7-bit address. The master initiates all transactions by sending an
address; only the addressed device responds. Open-drain outputs allow
multiple devices without bus contention.

Speed: 100 kHz standard, 400 kHz fast mode (libdrone payload standard),
1 MHz fast-plus. Slower than SPI, but adequate for sensors that update at
1–100 Hz. Multi-device capability allows many sensors on one bus with simple
two-wire wiring.

Uses on libdrone: payload I2C bus (Connector A PIN 5/6), Sensirion SEN66
at address 0x6B.

### MAVLink

MAVLink (Micro Air Vehicle Link) is a message-based protocol designed for
flight controller to ground control station communication. Each message has
a system ID, component ID, message type, and payload. MAVLink runs over UART
(or UDP/TCP for ground station links) and supports hundreds of defined message
types covering: arm/disarm, navigation waypoints, mode changes, sensor
telemetry streaming, parameter read/write, and mission management.

Uses on libdrone: ArduPilot on the Bandit platform uses MAVLink on UART6
for the companion Pi Zero 2W (LCM-1). Betaflight on Core/Pro uses MSP (a
simpler FC-specific protocol) rather than MAVLink. Not used in standard
Core/Pro configuration.

---

## Reference

### Protocol selection guide

| Need | Protocol | Why |
|---|---|---|
| One sensor, high sample rate | SPI | Speed, no address contention |
| Multiple sensors, low sample rate | I2C | Multi-device on 2 wires |
| Periodic burst data, single device | UART | Simple, universal |
| Bidirectional mission data | MAVLink | Structured message library |
| Multi-node reliable bus | CAN | Automotive-grade, noise-tolerant |

### Protocol parameters used on libdrone

| Bus | Protocol | Baud/speed | Devices |
|---|---|---|---|
| Gyro (SPI1) | SPI | 10 MHz | ICM-42688-P (single device) |
| UART1 | UART | 115,200 | HDZero VTX (MSP DisplayPort) |
| UART2 | UART | 57,600 | Matek M10Q GPS |
| UART3 | UART | 420,000 | RadioMaster RP2 ELRS (CRSF) |
| UART4 | UART | 115,200 | GX12 Connector A (payload commands) |
| UART5 | UART | configurable | GX12 Connector B (payload secondary) |
| UART6 | UART | 921,600 | Companion Pi Zero 2W (LCM-1) |
| I2C (Conn A) | I2C | 400 kHz | Payload sensors (SEN66 at 0x6B) |

---

## Procedure

<!-- not applicable — protocol configuration is in betaflight-setup and payload-software-protocol -->

---

## Rationale

### Why the IMU uses SPI instead of I2C

The ICM-42688-P gyroscope samples at 6400 Hz in libdrone's configuration —
a new 16-byte reading every 156 µs. At I2C 400 kHz fast mode, transmitting
16 bytes plus protocol overhead takes approximately 400 µs — more than twice
the 156 µs sample interval. I2C cannot keep up with the gyro's sample rate.
At SPI 10 MHz, the same read takes ~13 µs — 12 times faster than the sample
interval. SPI is the only reasonable choice for high-rate gyro data.

---

## Connections

requires: []
related:
  - [[crsf-protocol]]
  - [[payload-software-protocol]]
  - [[flight-controller-hardware]]
leads_to:
  - [[crsf-protocol]]
  - [[payload-software-protocol]]
