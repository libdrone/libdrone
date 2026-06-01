---
id: power-rail-architecture
title: "Power rail architecture"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - power-systems
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

libdrone has three distinct power domains fed from the 6S battery: the ESC
main bus supplying the motors directly at battery voltage, the 5V BEC from
the flight controller powering all logic and signal electronics, and a
regulated 9–12V rail from a buck converter powering the video transmitter.
Keeping these three domains separate — with the motors never sharing a ground
path with the signal electronics — is essential for EMC. The motor current
switching generates voltage spikes and electromagnetic noise; if the signal
electronics share that path, noise couples directly into the gyroscope and
GPS.

---

## Concept

### Three domains, three purposes

**Main bus (battery voltage, 21–25V):** The ESC takes power directly from the
battery through the XT60H connector. Motors draw from this rail. No regulation
— voltage varies from 25.2V (full charge) to 21.0V (minimum). This rail carries
the highest current on the drone (up to 200A peak across all four motors) and
generates the most noise. Nothing sensitive connects here.

**5V BEC (flight controller output):** The H7A3-SLIM's internal BEC converts
battery voltage to a regulated 5.0V, 1A continuous (2A peak). This powers the
FC itself, the ELRS receiver, GPS module, buzzer, cooling fan, and the 5V line
on the GX12 payload connectors. BEC output is low-noise regulated DC — the
correct supply for all digital logic and sensitive signal electronics.

**9–12V regulated rail (XL4015 buck converter):** The HDZero VTX accepts 7–25V
but benefits from a stable supply to maintain consistent transmit power. A
dedicated XL4015 step-down converter takes battery voltage and outputs 9–12V
specifically for the VTX. This keeps VTX supply voltage stable as the battery
discharges from 25.2V to 21.0V.

### Why a switching converter for the VTX and not an LDO

A linear regulator (LDO) drops the voltage difference as heat. From 22V to
12V at 400 mA of VTX current draw: 10V × 0.4A = 4W as heat — requires a
heatsink and reduces total system efficiency noticeably.

The XL4015 buck converter achieves ~90% efficiency at this operating point:
approximately 0.5W dissipated versus 4W for an LDO. The tradeoff is EMC: the
XL4015 switches at 180 kHz, generating harmonics that must not reach the GPS,
gyroscope, or ELRS receiver. Three to four clip-on ferrite beads on the VTX
power wire immediately at the converter output attenuate the 180 kHz noise
before it propagates.

### Star grounding

Multiple ground connections between components form closed loops. A closed
conductive loop is an antenna — changing magnetic fields (from motor current
switching) induce currents in the loop, creating noise voltages at every point
referenced to that ground.

libdrone's power architecture uses star grounding: all ground connections meet
at the ESC ground plane (the ESC PCB acts as the star point). The signal
electronics (FC, GPS, receiver) connect to this ground plane at one point only
— through the FC-to-ESC stack connection. No separate ground wires run from
individual components back to the battery negative.

### Wire routing zones

Three physical routing zones on the Platform enforce power separation:
- **Left channel (X = −20 mm):** signal wires — UART, I2C, GPIO, ELRS antenna
- **Centre (MIPI channel):** camera to VTX only
- **Right channel (X = +20 mm):** power wires — ESC 5V, buck converter output, motor current

These channels are moulded into the Platform PETG. Violating the zone separation
by running a signal wire alongside a power wire creates a transmission line that
couples motor switching noise into the signal.

---

## Reference

### Power architecture diagram

    6S Battery (21–25V)
        │
        ├── XT60H ──► ESC main bus (21–25V)
        │                 └── 4× motors (0–200A peak total)
        │
        ├── ESC main bus ──► H7A3-SLIM (FC)
        │                         └── 5V BEC (regulated, 1A/2A)
        │                               ├── FC logic
        │                               ├── ELRS RP2 receiver
        │                               ├── Matek M10Q-5883 GPS
        │                               ├── Vifly buzzer
        │                               ├── Gdstime fan (28 AWG, always-on)
        │                               └── GX12-A PIN 1 (5V payload rail)
        │
        └── ESC main bus ──► XL4015 buck converter ──► 9–12V
                                                          └── HDZero VTX

### Current budgets

| Consumer | Typical current | Peak current |
|---|---|---|
| 4× motors (total) | 20–80A (throttle dependent) | ~200A |
| FC + receiver | ~0.5A | ~0.8A |
| GPS | ~0.1A | ~0.15A |
| Fan | ~0.07A | ~0.07A |
| VTX (at 200 mW) | ~0.4A from 12V rail | ~0.6A |
| GX12 payload (typical SEN66 mast) | ~0.2A from 5V rail | ~0.4A |

### Wire gauge requirements

| Wire | AWG | Ampacity |
|---|---|---|
| Battery to ESC (main) | 12 AWG | ~30A continuous (XT60 limited) |
| Motor phase wires | 24 AWG | ~30A (MR30 connector limited) |
| BEC to consumers | 26–28 AWG | 1–2A |
| Signal wires (UART, I2C) | 28 AWG | <0.5A |

---

## Procedure

### Pre-wiring power domain check

1. Before soldering any signal electronics connections, complete and verify
   the main power path: battery → XT60 → ESC.
2. Verify no dead shorts with a multimeter (resistance mode, battery not connected).
   Main bus to ground should read open circuit before the ESC capacitors charge.
3. Connect battery through a current-limited bench supply or XT60 anti-spark
   connector for first power-on. Verify all three power domains reach their
   correct voltages before connecting any signal electronics.

### Verifying domain isolation

1. Motor phase wire should have no measurable DC continuity to any signal
   wire — check each motor phase wire to FC UART TX/RX pins with multimeter.
2. Battery negative and FC signal ground should connect at one point only:
   the ESC ground pad. Trace any unexpected additional ground paths and remove them.

---

## Rationale

### Why the fan connects to FC 5V and not a dedicated switching rail

The fan is 70 mA at 5V — within the BEC's continuous rating with margin.
Adding a separate switching converter for the fan would add mass, cost, and
complexity for no benefit. The BEC's regulated output is low-noise — better
for the fan motor (which is also a potential noise source) than a
separate switcher would be.

### Why GX12 PIN 1 (5V payload rail) comes from the BEC

Payload sensors (SEN66, ESP32-S3) are sensitive digital logic operating at
3.3V or 5V. They must have a stable, low-noise supply. Providing payload 5V
directly from the battery bus would expose them to motor switching transients.
The BEC's regulated output is the correct supply — at the cost of deducting
payload current from the BEC's 1A budget, which is why the maximum payload
current draw is specified as part of the GX12 interface standard.

---

## Connections

requires:
  - [[lipo-batteries]]
related:
  - [[electronic-speed-controllers]]
  - [[power-sequencing]]
  - [[emc-signal-integrity]]
leads_to:
  - [[power-sequencing]]


[lipo-batteries]: lipo-batteries.md "LiPo batteries"
[electronic-speed-controllers]: electronic-speed-controllers.md "Electronic speed controllers"
[power-sequencing]: power-sequencing.md "Power sequencing"
[emc-signal-integrity]: emc-signal-integrity.md "EMC and signal integrity"
