---
id: conformal-coating
title: "Conformal coating"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - emc-signal-integrity
personas:
  - 1.builder
  - 2.operator
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Conformal coating is a thin layer of silicone or acrylic applied over
completed PCB assemblies, covering every solder joint, component, and exposed
trace. It is electrically transparent at the frequencies electronics operate
at, mechanically protective against moisture and condensation, and prevents
conductive contamination (dust, water, salt) from bridging between exposed
conductors. Once applied it is essentially permanent — it cannot be removed
cleanly without damaging the board. Therefore: complete all soldering first,
mask all connectors and pads that will be soldered later, then coat. Apply
before the first flight, not after a moisture incident.

---

## Concept

### Why electronics are vulnerable to moisture

Electronic components and PCB traces are designed to function in dry air.
Moisture creates two failure modes:

**Conductive bridging**: Water — particularly with dissolved ionic
contamination from sweat, dew, salt, or condensation on concrete — is a
conductor. A water film across two adjacent PCB pads or traces creates a
resistive short. On a 3.3V logic circuit, this may cause misbehaviour. On
a power circuit, it can cause sustained current flow that heats the water
film, deposits ionic residue, and eventually creates a permanent conductive
path — a salt bridge that remains even after the water evaporates.

**Corrosion**: Exposed copper oxidises in the presence of moisture and oxygen.
Solder joints and exposed pads corrode gradually, increasing resistance and
eventually causing open circuits. Conformal coating prevents oxygen and moisture
from reaching the copper.

### Why a drone is particularly vulnerable

A drone operating in the environment encounters: morning dew when flying at
dawn; rain in conditions that start clear and deteriorate; condensation when
moving from a warm vehicle or case into cold outdoor air (the electronics are
warm from storage; cold humid air condenses on them); concrete spray from
landing near water; humidity inside a storage case that is not properly dried
after a wet flight.

Skateparks — one of libdrone's operational environments — are particularly
challenging: damp concrete, water features, and the practice of wetting
surfaces for certain activities. Even without direct water contact, the
humidity is elevated.

### What conformal coating does and does not do

**Does**: creates a hydrophobic (water-repelling) barrier over all exposed
conductors; prevents conductive bridging from surface moisture; slows
corrosion of exposed copper; provides minor mechanical protection against
abrasion.

**Does not**: make the board waterproof — connectors, through-holes, and
component openings are not sealed; prevent submersion damage; protect against
direct high-pressure water contact; survive repeated abrasion.

### Application sequence

Conformal coating cannot be removed cleanly from a PCB. Attempting removal
with solvent risks lifting traces, dissolving component markings, and
removing solder resist. Therefore:

1. **Complete all soldering first.** No further soldering after coating.
2. **Mask all connectors, pads, and test points** that must remain
   conductive or solderable. Use kapton tape or connector-specific masks.
3. **Apply coating** in thin, even layers. Brush application or spray are both
   acceptable; spray provides more even coverage on complex board topography.
4. **Allow to cure fully** before the first flight — typically 24 hours for
   silicone, 1–2 hours for acrylic (check manufacturer's datasheet).

---

## Reference

### Components requiring coating on libdrone

| Component | Coat? | Notes |
|---|---|---|
| Flight controller (H7A3-SLIM) | Yes | Mask USB port, all connectors |
| ESC (Pilotix 75A) | Yes, non-pad areas | Mask VBAT/GND pads, motor pads, signal pads |
| GPS module (M10Q-5883) | Yes | Mask GPS connector |
| ELRS receiver (RP2) | Yes | Mask antenna connector, UART pads |
| VTX (HDZero Freestyle V2) | No — manufacturer coating present | Do not double-coat; may affect thermal management |
| Capacitor solder joints | Yes | Coat the joint, not the capacitor body |

### Coating material options

| Type | Cure time | Removable? | Notes |
|---|---|---|---|
| Silicone (e.g. MG Chemicals 422B) | 24h | No (practical) | Most flexible, best vibration resistance |
| Acrylic (e.g. MG Chemicals 419D) | 1–2h | Partially (with acetone, damages board) | Faster cure, adequate for drone use |
| UV-cure acrylic | Minutes (with UV lamp) | No | Fast, requires UV lamp |

Silicone is preferred for drone use because it maintains flexibility at low
temperatures (important for winter operations) and provides the best vibration
resistance.

### Inspection after coating

Hold the board at an angle under a UV lamp. Silicone and acrylic conformal
coatings fluoresce under UV — coated areas glow, uncoated areas are dark.
Check for: uncoated areas on exposed traces (missed coverage), coated
connector pins (masking failure), bubbles or thick pools (may crack under
vibration).

---

## Procedure

### Coating the H7A3-SLIM

1. Apply kapton tape over: USB port, all JST/DF connectors, motor output pads,
   UART header pins, voltage/current monitor pads.
2. Secure the FC to a clean non-conductive surface so both faces are accessible.
3. Apply coating with a fine brush to all exposed copper: component pads,
   solder joints, exposed trace runs between components. Work in sections.
4. Avoid leaving pools in component cavities — thin and even is correct.
5. Allow to cure at room temperature for the specified time.
6. Remove masking tape before cure completes (if tape was not removed before
   application) to avoid pulling up adjacent coating.
7. Inspect under UV. Re-apply to any missed areas. Allow second application
   to cure fully before removing remaining masking.

---

## Rationale

### Why coat before the first flight rather than after a moisture incident

By the time moisture has caused a failure, conductive residues may already be
deposited on the board. Coating after a moisture incident seals those residues
in place — the problem may appear to be fixed but the residue continues to
cause intermittent failures under heat or humidity. Coating a clean,
never-moisture-exposed board ensures the barrier protects against contamination
from the beginning, not after the damage is done.

### Why the VTX is not coated

The HDZero Freestyle V2 VTX has a manufacturer-applied conformal coating.
Applying a second layer can trap heat between the coatings, interfering
with thermal management at the power amplifier — which runs at significant
dissipation (1–2W) during transmission. The manufacturer coating is adequate.

---

## Connections

requires: []
related:
  - [[emc-noise-sources]]
  - [[power-signal-separation]]
leads_to:
  - [[airframe-integration]]
