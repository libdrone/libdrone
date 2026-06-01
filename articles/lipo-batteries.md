---
id: lipo-batteries
title: "LiPo batteries"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - power-systems
personas:
  - 5.student
  - 1.builder
  - 2.operator
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Lithium polymer (LiPo) batteries power drone propulsion because they combine
high energy density, low internal resistance, and a favourable voltage range.
Each cell has a nominal voltage of 3.7V, a fully charged voltage of 4.2V, and
a minimum safe discharge voltage of 3.5V. Cells connect in series for higher
bus voltages. The same electrochemistry that makes LiPo batteries powerful
makes them dangerous if mishandled: overcharging, over-discharging, or physical
damage can trigger thermal runaway — a self-accelerating reaction producing fire
that cannot be extinguished by conventional means.

---

## Concept

### Cell chemistry and voltage

Inside each LiPo cell, lithium ions move between a graphite anode and a
lithium cobalt oxide cathode through a polymer gel electrolyte. During
discharge, ions migrate from graphite to cathode; electrons travel through
the external circuit doing work. Charging reverses this migration.

The cell voltage reflects the electrochemical potential between anode and
cathode materials. Fully lithiated cathode = 4.2V; fully delithiated = 3.5V.
Below 3.0V, the cathode changes phase irreversibly — permanent structural
damage. This is why the minimum voltage cutoff is enforced in firmware.

### Series cells and the "S" designation

Cells in series add their voltages. "6S" means six cells in series:

    Fully charged:   6 × 4.20V = 25.2V
    Nominal:         6 × 3.70V = 22.2V
    Storage voltage: 6 × 3.80V = 22.8V
    Minimum safe:    6 × 3.50V = 21.0V
    Hard cutoff:     6 × 3.30V = 19.8V

6S was chosen for libdrone because the 2507 1750kV motor at 22.2V nominal
spins at approximately 38,850 RPM unloaded — settling under prop load at
28,000–34,000 RPM. This is the optimal range for 6-inch propellers. At 4S
(14.8V), the motor spins too slowly for efficient thrust. At 8S (29.6V), RPM
exceeds safe bearing limits for this stator size.

### C rating

The C rating is maximum continuous discharge as a multiple of capacity. For
the Tattu R-Line 1800 mAh 150C:

    Theoretical max continuous: 150 × 1.8A = 270A

This is a marketing ceiling. In flight, libdrone draws 20–60A total depending
on throttle. The XT60 connector is rated 60A continuous — the practical limit
is the connector, not the C rating.

### Thermal runaway

At approximately 130°C the polymer separator melts, directly shorting anode
and cathode. The short generates more heat. Above ~200°C the cathode
decomposes, releasing oxygen. Flammable electrolyte plus oxygen produces fire.
This is self-reinforcing: heat → decomposition → more heat. Once started it
proceeds to completion regardless of external action.

In a multi-cell pack, runaway in one cell triggers adjacent cells within
seconds. Water reacts with lithium. Smothering removes external oxygen but
not the internal source from cathode decomposition. **The only effective
response is prevention.**

Triggers: overcharge (above 4.2V/cell), over-discharge (below 3.0V/cell),
physical puncture, internal short from crash damage.

---

## Reference

### libdrone battery specification

| Parameter | Value |
|---|---|
| Pack | Tattu R-Line V3 1800mAh 150C 6S |
| Nominal voltage | 22.2V |
| Fully charged | 25.2V |
| Storage voltage | 22.8V (~3.8V/cell) |
| Minimum flight voltage | 21.0V (3.5V/cell) — land now |
| Hard cutoff | 19.8V (3.3V/cell) — land immediately |
| Dimensions | 78 × 40 × 53 mm |
| Mass | ~210 g |
| Connector | XT60H-M |

### OSD voltage thresholds

| OSD reading at hover | Action |
|---|---|
| >22.0V | Normal |
| 22.0–21.5V | Return to landing zone |
| 21.5–21.0V | Land within 2 minutes |
| <21.0V | Land immediately |

---

## Procedure

### Safe storage

1. After each flight, check pack voltage. If above 23.5V (>3.9V/cell),
   run a storage charge to 22.8V.
2. If not flying within 3 days, storage-charge or discharge to 3.8V/cell.
3. Store at room temperature in a fireproof LiPo bag or steel ammunition box.
4. Never store in a vehicle or in direct sunlight.

### Post-crash inspection

1. Inspect for swelling, deformation, or puncture.
2. Check individual cell voltages — any cell above 4.25V or below 3.0V:
   retire the pack.
3. If pack is warm after a crash without heavy flight: wait 30 minutes in an
   open area away from flammables before handling.
4. Any swollen pack must be fully discharged in a fireproof container and
   disposed of properly. Do not continue using a swollen pack.

### Winter operations

Do not fly below 0°C in standard configuration. Transport batteries inside
a pocket or insulated bag; bring to site in the last 5 minutes. A battery at
+5°C may behave as if 30–40% of rated capacity is unavailable. Land at higher
remaining voltage and monitor OSD more frequently.

---

## Rationale

### Why 6S and not 4S

4S nominal (14.8V) would put the 2507 1750kV at ~25,900 RPM under load —
below the efficient range for 6-inch props. Additionally, higher voltage
for the same power means lower current: halving the current reduces I²R
losses in wires and connectors by 75%, meaningfully improving efficiency and
reducing heat across the entire power distribution chain.

### Why storage voltage matters

A LiPo stored fully charged slowly degrades through electrolyte oxidation.
Stored fully discharged, it risks falling below 3.0V/cell through self-discharge,
causing irreversible cathode damage. Storage voltage (3.8V/cell) minimises
both degradation mechanisms simultaneously.

---

## Connections

requires: []
related:
  - [[power-rail-architecture]]
  - [[power-sequencing]]
  - [[li-ion-batteries]]
leads_to:
  - [[power-rail-architecture]]
  - [[power-sequencing]]
  - [[li-ion-batteries]]


[power-rail-architecture]: power-rail-architecture.md "Power rail architecture"
[power-sequencing]: power-sequencing.md "Power sequencing"
[li-ion-batteries]: li-ion-batteries.md "Li-Ion batteries"
