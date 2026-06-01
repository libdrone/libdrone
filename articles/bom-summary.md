---
id: bom-summary
title: "Bill of materials summary"
version: 1.1.0
date: 2026-06-01
author: jsa
status: released
scope: libdrone
topic:
  - resilience-community
personas:
  - 6.evaluator
  - 1.builder
platform:
  - pro
lang: en
licence: CC BY-SA 4.0
---

## Summary

The libdrone Pro bill of materials is entirely composed of commercially
available components with no proprietary dependencies. Every item has a
documented alternative or substitute. The full BOM is maintained in the
shopping list document; this article provides the cost and category summary
for procurement planning. A single-frame flyable build (no goggles) costs
approximately 18,000 CZK. A complete two-frame build with HDZero Goggle 2
costs approximately 34,000 CZK. The sensor payload (air quality mast) adds
approximately 2,650 CZK.

---

## Concept

### Cost structure

The cost breaks into six categories:

**Video system** (~19,300 CZK for two-frame with goggles) — the HDZero Goggle 2
(15,500 CZK) is the single largest line item and is shared across both frames.
The VTX + camera (3,800 CZK) is per-frame. For multi-frame deployments, the
goggle cost is amortised across all frames.

**Electronics core** (~8,050 CZK per frame) — FC, ESC, motors, GPS, receiver.
These are the components most likely to be sourced locally from Czech hobby
suppliers for reduced lead time.

**Batteries and charging** (~4,300 CZK) — three 6S packs plus charger.
Budget scales linearly with the number of packs required for the operational
profile.

**Mechanical and consumables** (~2,200 CZK) — screws, standoffs, connectors,
O-rings, conformal coating, Loctite.

**Filament** (~1,000 CZK in stock) — PC-CF, PETG, ASA, TPU. Assuming a
Prusa CoreOne printer with hardened nozzle is already available.

**Sensor payload** (~2,650 CZK, deferred) — SEN66, ESP32-S3, SD module,
I2C cables. Not required for flight.

### Make vs buy

The structural frame components (arm shafts, sandwich layers, Platform,
Backplane, bumpers) are printed — approximately €16 in filament per frame.
The same geometry in machined carbon fibre or injection-moulded nylon would
cost ten to thirty times more. The printability is a cost advantage, a
repairability advantage, and a customisability advantage.

There is no buy option for the frame. This is by design.

---

## Reference

### Cost summary by category (single-frame build with goggles)

| Category | Approx cost (CZK) | Notes |
|---|---|---|
| Video system (VTX + Goggle 2) | 19,300 | Goggle shared across frames |
| FC + ESC | 3,200 | Matek H7A3-SLIM + Pilotix 75A AM32 |
| Motors (×4) | 2,400 | BrotherHobby Avenger V2 2507 |
| GPS + receiver | 1,050 | Matek M10Q + RadioMaster RP2 |
| Propellers (2 sets) | 850 | HQProp 6×3×3 + 6×2.5×3 |
| Batteries + charger | 4,300 | ×3 packs + HOTA D6 Pro |
| Power components | 357 | Buck, TVS, caps, ferrites |
| Mechanical + consumables | 2,200 | Screws, O-rings, coating, Loctite |
| Filament (in stock) | ~1,000 | PC-CF, PETG, ASA, TPU |
| **Single-frame with goggles** | **~34,657 CZK** | |
| Less goggles (second frame) | −15,500 | Goggle not repeated |
| **Second frame incremental cost** | **~7,000 CZK** | |
| Sensor payload (deferred) | 2,650 | SEN66 air quality mast |

### Key suppliers (Czech Republic)

| Supplier | Items | Lead time |
|---|---|---|
| HobbyDrone.cz / RCStudio.cz | FC, ESC, VTX, goggles, GPS, receiver, props | 7–10 days |
| Laskakit.cz | Buck converter, standoffs, passives | 2–3 days |
| AliExpress | Motors, batteries, hardware, O-rings, connectors | 10–15 days |
| Prusa.shop | Filament, nozzles, bed consumables | Next day |
| Farnell CZ / RS Components CZ | Conformal coating (HPA200H) | 2–3 days |
| Carbonrods.cz / RCProfi.cz | 2.0mm CF rods | 3–5 days |

### Component substitutions (documented)

All critical components have documented substitutes in the hardware reference:
- FC: any Betaflight-supported H7 board with 6× UART
- ESC: any 4-in-1 6S AM32 or BLHeli_32 unit with BiDShot telemetry
- GPS: any u-blox M8/M9/M10 module with magnetometer
- ELRS receiver: any ELRS 2.4GHz receiver (bind phrase matching required)
- Props: HQProp 6-inch variants — pitch choice affects calibration

---

## Procedure

<!-- not applicable — see procurement article for ordering sequence -->

---

## Rationale

### Why the BOM is public and maintained

A BOM that is not public requires the buyer to trust the seller's claims about
component sourcing and supply chain security. For institutional procurement in
security-sensitive contexts, this trust is not a substitute for verification.
The libdrone BOM is public, sourced from documented suppliers, and uses
components whose specifications are publicly verifiable. An institution can
audit the supply chain independently.

---

## Connections

requires:
  - [[platform-overview]]
related:
  - [[procurement]]
  - [[lipo-batteries]]
  - [[floating-motor-mounts]]
  - [[legal-and-regulatory]]
leads_to:
  - [[platform-overview]]
