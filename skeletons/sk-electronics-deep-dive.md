---
id: sk-electronics-deep-dive
title: "Electronics Deep Dive"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 5.student
  - 1.builder
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

After reading this document, the student can explain the electronics stack
of a modern FPV drone from battery to motor, understand the communication
protocols at each layer, apply EMC principles to their own builds, and
configure the firmware that makes it all work together. This is the 3.0.0
replacement for the Electronics Textbook.

---

## Concept

### Power: the energy source and distribution

A 6S LiPo delivers 22.2V nominal. That single voltage must serve motors
that want direct battery voltage, a flight controller that wants 5V, and a
video system that wants 9–12V. → [[lipo-batteries]] covers the electrochemistry,
the C-rating, and the handling rules that prevent thermal runaway. → [[power-rail-architecture]]
maps the full power distribution: XT60 → ESC → motors (direct), ESC BEC → FC
and peripherals (5V), XL4015 buck → VTX (regulated 9–12V). → [[voltage-regulation]]
explains the buck converter design and why the VTX cannot share the FC's BEC.
→ [[power-sequencing]] covers why transmitter must be on before battery connects.

### The motor control chain

The FC generates a digital command. The motor produces mechanical torque.
Between them is a precise chain of protocols and hardware:

1. FC computes motor output (0–2047 scale) from the PID loop
2. FC transmits via → [[dshot-protocol]] — a digital, checksummed protocol
   at 600 kHz carrying the command, and receiving eRPM back via bidirectional
3. → [[electronic-speed-controllers]] decode DShot and switch the six FETs
   that synthesise the three-phase AC current
4. The three-phase current drives the → [[brushless-motors]] via the
   electromagnetic interaction between stator windings and rotor magnets
5. The motor's → [[propellers]] convert rotation into thrust

The bidirectional DShot telemetry (eRPM reporting from ESC to FC) is the
enabling technology for the → [[rpm-filter]]: the FC knows the exact motor
frequency and places notch filters precisely at the harmonics. Without this
feedback, the filter would need to cover broad frequency bands and would
sacrifice control bandwidth.

### The sensor suite

Every sensor in the flight controller serves a specific function in the
state estimation and control pipeline:

→ [[imu-gyroscope]] — the ICM-42688-P samples at 6400 Hz over SPI at 10 MHz,
using the Coriolis effect in a MEMS proof mass to measure rotation rate. This
is the primary sensor for the PID loop. The DMA transfer from SPI to RAM is
what makes the 8 kHz loop rate possible without CPU blocking. The IMU "moat"
— a slot cut through the PCB substrate — provides vibration isolation at the
board level.

→ [[imu-filter-tuning]] — the filter pipeline between raw gyro and PID input.
The RPM filter removes motor harmonics. The dynamic notch filter removes
frame resonances. Lowpass filters smooth remaining broadband noise.

→ [[barometer-magnetometer]] — the barometer provides altitude reference for
GPS Rescue. The QMC5883 magnetometer at the drone nose provides heading —
placed there to maximise distance from the motor wires whose 20A currents
would otherwise swamp the Earth's 50µT field.

→ [[gnss-gps]] — the u-blox M10 GNSS receiver tracking GPS + Galileo + BeiDou
at 10 Hz, with EGNOS augmentation reducing horizontal error from 2–5m to
0.5–1.5m. The GLONASS constellation is disabled — near the Czech eastern
border, jamming has been observed.

→ [[supplemental-sensors]] — optical flow, lidar, sonar: what they provide,
how they connect to the GX12 interface, and when to use them.

### Communication protocols

The flight controller communicates with every peripheral via a different protocol,
each matched to its function: → [[serial-protocols]] provides the comparative
overview. At the highest level:

→ [[elrs-protocol]] — the RC link. Chirp spread spectrum at 2.4 GHz, 250 Hz
packet rate, LBT regulatory mode. The processing gain from CSS is what
enables reception below the noise floor — critical for range and interference
resistance in urban RF environments.

→ [[crsf-protocol]] — CRSF carries the RC channels from the RP2 receiver to
the FC at 420,000 baud. Bidirectional: RC data from transmitter to FC, link
statistics and telemetry from FC back to transmitter.

→ [[digital-fpv]] — HDZero encodes each video frame in hardware (H.265, 1–2 ms),
transmits on 5.8 GHz, and the goggle decodes with 4–8 ms total latency. The
MIPI CSI-2 cable between camera and VTX carries differential signals at
hundreds of MHz — its routing through the enclosed Platform centreline channel
is an EMC requirement, not an aesthetic choice.

### The EMC problem and its solutions

A drone is an EMC challenge because the noise sources (ESC switching at 48 kHz,
motor commutation at 3500 Hz, buck converter at 180 kHz) and the victims
(gyroscope, GPS, receiver) are centimetres apart. → [[emc-noise-sources]] maps
the problem. The mitigation is layered:

**Physical**: → [[power-signal-separation]] enforces three routing zones via
the Platform geometry. → [[gps-antenna-placement]] keeps the compass 150mm
from the nearest motor wire.

**Passive**: → [[twisted-pairs]] on motor phase wires and battery leads. → [[star-grounding]]
to eliminate ground loops. → [[capacitor-placement-emc]] with the 1000µF cap
directly on the ESC pads (wire inductance = latency = failed clamping).

**Frequency-selective**: → [[ferrite-beads]] on the VTX power wire damp the
180 kHz buck converter switching frequency before it propagates.

**Environmental**: → [[conformal-coating]] to prevent moisture-induced short
circuits and corrosion.

### Flight controller setup

→ [[betaflight-setup]] covers the initial firmware flash, CLI diff application,
UART assignments, and motor direction verification. → [[betaflight-profiles]]
covers the two-profile approach: standard operation and low-speed A2 compliance.
→ [[betaflight-gps-rescue]] configures the autonomous failsafe. → [[edgetx-model]]
configures the TX16S transmitter model with correct channel order, switch
assignments, and ELRS settings.

→ [[pid-tuning-rate-profile]] is where the builder's initial effort produces
dividends: the base PID values are starting points, not final values. The
Blackbox trace from the maiden flight is the diagnostic tool.

---

## Reference

### Protocol stack summary

| Layer | Protocol | Link | Speed |
|---|---|---|---|
| RC | ELRS (CSS) | TX16S → RP2 | 250 Hz, 2.4 GHz |
| RC serial | CRSF | RP2 → FC UART3 | 420,000 baud |
| Motor command | DShot600 | FC → ESC | 600 kHz |
| Motor telemetry | BiDi DShot | ESC → FC | Same wire |
| Gyro | SPI | IMU → FC | 10 MHz |
| GPS | UBX | M10Q → FC UART2 | 57,600 baud |
| OSD | MSP DisplayPort | FC UART1 → VTX | 115,200 baud |
| Camera-VTX | MIPI CSI-2 | Camera → VTX | ~100–500 MHz |
| Payload | MSP + I2C + UART | FC → GX12 | Various |

---

## Procedure

### For a student using this as a course text

Work through the Concept sections in order. For each topic, read the linked
atom fully before proceeding to the next. The atoms contain the depth; this
skeleton provides the thread that connects them.

---

## Rationale

The V2.4.6 Electronics Textbook was a single 1,000+ line document containing
all the technical depth. Every time a specification changed — a new firmware
version, a revised component, a corrected frequency — the entire textbook
needed review. This skeleton delegates specifications to atoms, keeping the
narrative stable while the details are maintained where they live.

---

## Connections

requires: []
related:
  - [[sk-engineering-101]]
  - [[sk-complete-build-guide]]
leads_to:
  - [[sk-complete-build-guide]]
