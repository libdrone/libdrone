---
id: power-signal-separation
title: "Power and signal separation"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
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

Parallel power and signal wires form a transmission line. Energy couples
from power wires into signal wires both capacitively (electric field) and
inductively (magnetic field). The coupling falls off with separation distance.
On libdrone, the Platform layer enforces three physically separated routing
zones — signal channel at X = −20 mm, MIPI centreline at X = 0, power channel
at X = +20 mm — maintained by printed walls throughout the Platform length.
Three geometry gates must pass in CAD before any Platform part proceeds to print.

---

## Concept

### Capacitive coupling

Two parallel conductors at different voltages form a capacitor with capacitance
proportional to their length and inversely proportional to their separation:

    C_mutual ∝ length / separation

A rapidly changing voltage on the power wire (motor current spike on the ESC bus)
induces a proportional current spike in the adjacent signal wire through this
mutual capacitance. The shorter the separation and the longer the parallel run,
the more energy couples across.

Capacitive coupling is reduced by: increasing separation, shortening the parallel
run length, inserting a grounded conductor between power and signal (shielding).

### Inductive coupling

A current-carrying wire creates a magnetic field. An adjacent signal wire that
encloses some of this field will have a voltage induced in it proportional to
the rate of field change:

    V_induced ∝ M × dI/dt

Where M is the mutual inductance between the two wires. M decreases with
increasing separation. At 15 mm separation, M is approximately 4× lower than
at 5 mm separation for typical wire geometries.

Both capacitive and inductive coupling increase with the length of parallel
run. Every centimetre of unnecessary parallel routing between a power wire and
a signal wire adds coupling.

### libdrone three-zone routing

The Platform layer implements mandatory physical separation via printed walls:

| Zone | X position | Contents |
|---|---|---|
| Signal channel | −20 mm | UART, I2C, GPS, RC receiver signal wires |
| MIPI centreline | 0 mm (enclosed channel) | MIPI CSI-2 camera-to-VTX cable only |
| Power channel | +20 mm | ESC power, motor wires, battery lead |

The walls between zones are minimum 3 mm PETG — not electrically conductive,
but physically prevent wires from migrating across channels and provide ~20 mm
of separation as a minimum. The MIPI channel is fully enclosed, preventing the
MIPI CSI-2 clock (running at hundreds of MHz) from radiating into adjacent zones.

The GX12 connector wire routing follows the zone assignment:
- Connector A (signal + I2C) exits LEFT into the signal channel
- Connector B (GPIO + GPS tap) exits RIGHT into the power channel

This assignment is deliberate — I2C SDA/SCL are more noise-sensitive than the
GPIO lines, so they are routed in the quieter signal channel. → See [[gnss-gps]]
for the GPS antenna and carbon fibre interaction.

### The compass and power wire distance rule

The magnetometer (QMC5883 on the M10Q) is mounted at the nose of the drone —
the maximum physical distance achievable from the ESC, battery leads, and motor
wires. A single motor wire carrying 20 A at 30 mm distance creates a magnetic
field of approximately 130 µT at the sensor — comparable to Earth's magnetic
field (~50 µT). Placing the compass at this distance would prevent it from
accurately reading Earth's field direction.

At the nose (approximately 150 mm from the ESC), the same motor wire's field
falls to approximately 2.6 µT — well below the Earth's field and within
calibration compensation range. This is why compass placement at maximum
distance from power wiring is a layout constraint, not an aesthetic choice.

---

## Reference

### EMC geometry gates (Platform pre-print checks)

All three must pass in CAD before printing the Platform:

| Gate | Check | Why |
|---|---|---|
| 1 | Signal channel wall height ≥ 3 mm | Ensures physical barrier between signal and power zones |
| 2 | MIPI cable channel fully enclosed | Prevents MIPI high-frequency clock from radiating into adjacent zones |
| 3 | GX12 chimney wall thickness ≥ 3 mm | Prevents chimney bore from acting as a waveguide coupling electronics-zone noise to payload connectors |

### Minimum separation rules

| Pair | Minimum separation |
|---|---|
| Motor phase wire to GPS antenna wire | 30 mm |
| Battery lead to UART signal wire | 20 mm |
| ESC power pad to FC IMU chip | Design constraint — fulfilled by 30.5 mm stack spacing |
| Buck converter output wire to ELRS antenna | 20 mm |

---

## Procedure

### Wiring within the Platform zones during build

1. Before routing any wire, identify its zone: signal or power.
2. Power wires (ESC leads, motor phase bundles, battery) route through the
   RIGHT channel (X = +20 mm). Signal wires (UART, I2C, GPS cable, RX wire)
   route through the LEFT channel (X = −20 mm).
3. MIPI cable routes through the centreline channel — never disturb this channel
   with other wires. MIPI cable minimum bend radius: 30 mm.
4. Where a wire must cross from one zone to another, cross at 90° and minimise
   the crossing length. A wire crossing at right angles has near-zero inductive
   coupling regardless of separation.
5. Use cable ties or sticky-mount tie bases to secure wires within their zones.
   Wires that migrate during flight can enter the wrong zone and cause previously
   absent noise.

---

## Rationale

### Why the zones are at ±20 mm and not ±10 mm or ±30 mm

±20 mm from centreline places the zone boundaries at the edge of the
Platform's narrow section (40 mm wide in the battery zone). Moving to ±30 mm
would place power wires outside the Platform envelope — they would have no wall
to route against. Moving to ±10 mm would halve the separation and increase
coupling by approximately 4×. ±20 mm is the maximum separation achievable
within the Platform's geometric constraints.

---

## Connections

requires:
  - [[emc-noise-sources]]
related:
  - [[twisted-pairs]]
  - [[star-grounding]]
  - [[capacitor-placement-emc]]
  - [[ferrite-beads]]
leads_to:
  - [[ferrite-beads]]
  - [[gps-antenna-placement]]


[gnss-gps]: gnss-gps.md "GNSS and GPS"
[emc-noise-sources]: emc-noise-sources.md "EMC noise sources in a drone"
[twisted-pairs]: twisted-pairs.md "Twisted pairs"
[star-grounding]: star-grounding.md "Star grounding"
[capacitor-placement-emc]: capacitor-placement-emc.md "Capacitor placement for EMC"
[ferrite-beads]: ferrite-beads.md "Ferrite beads"
[gps-antenna-placement]: gps-antenna-placement.md "GPS antenna placement"
