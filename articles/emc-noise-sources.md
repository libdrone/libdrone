---
id: emc-noise-sources
title: "EMC noise sources in a drone"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - emc-signal-integrity
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

Every wire carrying a changing current radiates an electromagnetic field. A
drone concentrates several powerful noise sources — ESC switching, motor
winding transients, battery lead current spikes, and buck converter switching
— in a small volume alongside sensitive sensors that must be protected from
that noise. Understanding the source, frequency, and coupling mechanism of
each noise type is the prerequisite to choosing the right mitigation. There
is no single fix: each source requires a targeted approach, and the approaches
must be layered.

---

## Concept

### Maxwell's equations as the root cause

A changing current creates a changing magnetic field (Ampère's law). A changing
magnetic field induces a voltage in any nearby conductor (Faraday's law). In a
drone, this means every time motor current changes — on every throttle input, on
every ESC MOSFET switching event, on every RPM change — a changing field
propagates outward from the power wires and couples onto nearby signal wires,
sensor supply traces, and PCB ground planes.

This is not a peripheral concern. The gyroscope is measuring changes in the order
of 0.01°/s. The GPS is receiving signals at −130 dBm. The I2C bus operates at
logic levels that a few millivolts of noise can corrupt. The noise sources in a
drone operate at voltages and currents that dwarf these signal levels by many
orders of magnitude.

### ESC switching noise (48 kHz and harmonics)

The ESC switches its six MOSFETs at 48,000 times per second. Each switching event:
- Creates a fast current edge in the motor phase wires (~50 A/µs)
- Creates a voltage edge on the power bus (~50 V/µs with inadequate decoupling)
- Radiates electromagnetic energy at 48 kHz and its harmonics (96, 144, 192 kHz...)
  extending into the MHz range

The 48 kHz fundamental is well above the gyro's useful signal band (0–100 Hz)
but couples directly into the gyro supply voltage, appearing as shifted zero-rate
output and elevated noise floor.

### Motor winding transients

Motor windings are inductors. When the ESC switches the active phase, the
collapsing current in the previous phase induces a back-EMF spike — the inductor
resists the sudden current change. These spikes can reach several hundred volts
per microsecond in the absence of clamping. The 1000 µF capacitor and TVS diode
on the ESC power pads clamp these spikes on the power bus; what escapes as
radiated field is attenuated by routing and separation.

### Battery lead current spikes

Every throttle change requires a rapid change in motor current, which requires
a rapid change in battery lead current. A 40 A step in 1 µs through a 20 cm
battery lead radiates a significant electromagnetic field. The battery lead is
an effective antenna at the frequencies corresponding to the current rise time.
Twisting the battery leads together cancels most of the radiated field —
two equal and opposite currents flowing in opposite directions cancel each
other's fields at any external point.

### Buck converter switching (180 kHz)

The XL4015 buck converter powering the VTX switches at 180 kHz. This frequency
and its harmonics appear on the VTX power wire and can radiate from it,
coupling into the GPS antenna (tuned to 1.575 GHz but susceptible to conducted
noise on its supply) and the receiver.

Ferrite beads on the VTX power wire provide frequency-selective attenuation
of the 180 kHz switching frequency. → See [[ferrite-beads]].

### USB/UART switching (minor)

Serial data transitions on UART lines are minor noise sources compared to the
above, but at high baud rates (CRSF at 420,000 baud) the transition rate is
sufficient to produce low-level radiated noise. Twisted-pair routing of
differential signals and adequate separation from sensitive sensors mitigates this.

---

## Reference

### Noise source summary

| Source | Frequency | Amplitude | Primary coupling mechanism |
|---|---|---|---|
| ESC MOSFET switching | 48 kHz and harmonics | High (A-class) | Magnetic near-field, conducted via power bus |
| Motor winding transients | Broadband (DC–MHz) | Very high, brief | Magnetic near-field |
| Battery lead current steps | Broadband | High | Magnetic near-field |
| Buck converter (XL4015) | 180 kHz and harmonics | Medium | Conducted via VTX power wire |
| UART transitions (CRSF etc.) | Up to few MHz | Low | Electric near-field |

### Sensitive victims and their susceptibility

| Victim | Susceptibility | Key frequency range |
|---|---|---|
| Gyroscope (ICM-42688-P) | Very high — supply noise shifts zero-rate output | 1 kHz–1 MHz |
| Magnetometer (QMC5883) | Very high — DC fields cause heading error | DC–1 kHz |
| GPS antenna (1.575 GHz) | High — wideband noise raises noise floor | 100 MHz–2 GHz |
| ELRS receiver (2.4 GHz) | Medium — spread spectrum provides processing gain | 2.4 GHz |
| I2C bus (400 kHz) | Medium — noise on SDA/SCL causes data errors | 400 kHz–1 MHz |

---

## Procedure

<!-- not applicable — mitigations are in the linked articles -->

---

## Rationale

### Why this article exists before the mitigation articles

A builder who only knows the mitigations — "twist the motor wires," "add ferrite
beads" — follows instructions without understanding why. When something unexpected
happens (elevated noise floor, compass drift, GPS multipath), they have no framework
to diagnose it. Understanding the source, mechanism, and frequency of each noise
type enables targeted diagnosis: "the compass is drifting intermittently — is it a
DC field from a battery lead, or a high-frequency field from the ESC? Check the
routing." This article provides that framework before the mitigation articles that
follow.

---

## Connections

requires: []
related:
  - [[vibration-isolation-theory]]
  - [[rpm-filter]]
leads_to:
  - [[twisted-pairs]]
  - [[star-grounding]]
  - [[capacitor-placement-emc]]
  - [[power-signal-separation]]
  - [[ferrite-beads]]
