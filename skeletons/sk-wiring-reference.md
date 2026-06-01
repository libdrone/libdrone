---
id: sk-wiring-reference
title: "Wiring and Electrical Integration Reference"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 1.builder
  - 4.workshop
platform:
  - pro
lang: en
licence: CC BY-SA 4.0
---

## Summary

After reading this reference, the builder can select the correct wire gauge
for every connection in the build, route all wires in accordance with EMC
discipline, verify the complete installation against a structured checklist,
and understand why each specification exists. This is the 3.0.0 replacement
for the V2.4.6 Wiring and Electrical Integration Reference.

---

## Concept

### Wiring is EMC engineering

The wiring is not just connectivity — it is the physical implementation of
the electromagnetic compatibility architecture. A correctly wired libdrone
has star grounding, twisted pairs on all high-current runs, power wires in
the right channel and signal wires in the left channel, capacitors directly
on ESC pads, and ferrite beads on the VTX power wire. An incorrectly wired
libdrone has exactly the same components and will appear to work — until it
doesn't. The failures are typically intermittent, hard to diagnose, and
directly traceable to wiring discipline.

→ [[emc-noise-sources]] establishes why this matters. → [[star-grounding]],
→ [[twisted-pairs]], → [[capacitor-placement-emc]], → [[power-signal-separation]],
and → [[ferrite-beads]] each address a specific failure mode.

### Wire selection physics

The guide to wire gauge (AWG) is in the 2.x Wiring document and will be
extracted into atoms in a future revision. The summary that belongs here:
lower AWG number = thicker wire = lower resistance = more current capacity.
The critical gauges for libdrone Pro:

- **12 AWG**: battery leads XT60 to ESC pads. High-current backbone.
- **20 AWG**: VTX power from buck converter. Up to 10A continuous.
- **24 AWG**: 5V BEC rails, short UART signal runs.
- **28 AWG**: all signal wires — GPS, I2C, payload UART, GX12 pins.

Never substitute a thinner gauge "just for now." The physics of I²R heating
is not negotiable.

### Colour code

Consistent colour coding means any wire's purpose is visible without a
multimeter six months after the build. Five colours, absolute assignments:

- **Red** — positive power at any voltage
- **Black** — ground and negative return
- **Yellow** — analogue measurement (voltage sense, current sense)
- **Blue** — high-speed digital signal (DShot, CRSF, MSP UART)
- **Green** — low-speed bus signals (GPS UART, I2C, payload UART)

---

## Reference

### Section-by-section wiring map

| Section | Connection | Gauge | Notes |
|---|---|---|---|
| 1 | Battery (XT60) → ESC VBAT/GND pads | 12 AWG | Twisted pair, ≤50mm, drop through battery lead notch |
| 1 | 1000µF cap | — | Directly on ESC pads, leads ≤5mm — → [[capacitor-placement-emc]] |
| 1 | TVS diode SMBJ28A | — | On ESC pads alongside cap |
| 2 | ESC → Motors (MR30) | 18 AWG (motor leads) | Twist all 3 phase wires per motor, 1 twist/15mm — → [[twisted-pairs]] |
| 3 | ESC BEC 5V → FC | 24 AWG | Via 100µF MLCC on FC 5V pads |
| 3 | FC GND → ESC GND pad | 24 AWG | Short direct wire, star ground point — → [[star-grounding]] |
| 4 | FC UART3 → RP2 ELRS receiver | 28 AWG blue | LEFT (signal) channel |
| 5 | FC UART2 → M10Q GPS | 28 AWG green | LEFT channel, GPS GND via FC not ESC |
| 6 | XL4015 buck output → VTX power | 20 AWG | Ferrite beads at converter output — → [[ferrite-beads]] |
| 6 | VTX GND → buck GND → ESC GND | 22 AWG | Star ground path |
| 6 | FC UART1 → VTX MSP | 28 AWG blue | LEFT channel |
| 6 | Camera MIPI cable | — | Through Platform centreline channel, 30mm min bend radius |
| 7 | GX12 Connector A wires | 24/28 AWG | Solder to FC BEFORE placing top layer — → [[gx12-connector-standard]] |
| 7 | GX12 Connector B wires | 24/28 AWG | Route A LEFT, B RIGHT |
| 8 | Fan power | 22 AWG | FC 5V pad, always-on |
| 9 | Companion harness (LCM-1) | JST-SH 4-pin | Pre-wire during Phase 4 — → [[lcm1-spec]] |

### Routing zone discipline

| Zone | X position | Contents |
|---|---|---|
| Signal (LEFT) | −20mm | UART, I2C, GPS, ELRS, MIPI (centreline enclosed) |
| Power (RIGHT) | +20mm | ESC VBAT, motor phase bundles, battery lead |

Never route power wires toward the GPS bracket. Never route a power wire
adjacent to the GPS module or compass.

### Star ground map

    ESC GND pad ← master ground point
      ├── Battery GND (direct, twisted pair with +)
      ├── 1000µF cap GND (directly on pad)
      ├── TVS diode GND (on pad)
      ├── FC GND (short direct wire)
      └── Buck converter GND → VTX GND

    GPS GND → via FC
    ELRS receiver GND → via FC

Nothing else connects to battery negative. No separate GND wire from any
subsystem back to battery. → [[star-grounding]] explains why.

### Build verification sequence

After all soldering is complete, before conformal coating:

1. Visual: every joint shiny, concave fillet, no cracks or blobs
2. Continuity: check each GX12 pin to its FC destination
3. Short check: multimeter between VBAT and GND — should read battery voltage,
   not zero ohms
4. Motor spin: props off, battery via ShortSaver, verify all 4 motors spin
   correct direction
5. Voltage check: OSD battery reading matches multimeter ±0.2V
6. GPS check: outdoors, ≥8 satellites within 90 seconds cold start
7. OSD check: all required fields visible in goggles

---

## Procedure

### First-time wiring session sequence

1. Route ALL wires to final position before bolting down the FC/ESC stack
2. Solder all GX12 connector wires to FC before placing the Platform top layer
3. Install capacitors before any other soldering — they must be present for
   first power-on
4. Apply conformal coating after all soldering and inspection — before any
   full power test
5. → [[electronics-installation]] contains the full phase-by-phase procedure

---

## Rationale

The V2.4.6 Wiring Reference (917 lines) contained the full physics derivations,
worked examples, colour code rationale, and every connection specification in
a single document. This skeleton delegates the specifications to atoms and
provides the builder with the navigational structure: which connection, which
atom, what to verify. The physics derivations for wire gauge will be extracted
into a dedicated atom in a future revision.

---

## Connections

requires: []
related:
  - [[sk-complete-build-guide]]
  - [[sk-electronics-deep-dive]]
  - [[wire-gauge-selection]]
leads_to:
  - [[sk-complete-build-guide]]


[emc-noise-sources]: ../articles/emc-noise-sources.md "EMC noise sources in a drone"
[star-grounding]: ../articles/star-grounding.md "Star grounding"
[twisted-pairs]: ../articles/twisted-pairs.md "Twisted pairs"
[capacitor-placement-emc]: ../articles/capacitor-placement-emc.md "Capacitor placement for EMC"
[power-signal-separation]: ../articles/power-signal-separation.md "Power and signal separation"
[ferrite-beads]: ../articles/ferrite-beads.md "Ferrite beads"
[gx12-connector-standard]: ../articles/gx12-connector-standard.md "GX12 connector standard"
[lcm1-spec]: ../articles/lcm1-spec.md "LCM-1 compute module"

[electronics-installation]: ../articles/electronics-installation.md "Electronics installation"
[sk-complete-build-guide]: sk-complete-build-guide.md "Complete Build Guide"
[sk-electronics-deep-dive]: sk-electronics-deep-dive.md "Electronics Deep Dive"
[wire-gauge-selection]: ../articles/wire-gauge-selection.md "Wire gauge selection"
