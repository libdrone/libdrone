---
id: sk-field-pod-guide
title: "Off-Grid Field Production Pod Guide"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 2.operator
  - 6.evaluator
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

After reading this guide, the operator can design and deploy a self-contained
field pod capable of charging batteries, repairing hardware, and printing
replacement parts independently of grid power. This is the 3.0.0 replacement
for the V2.4.6 Field Pod document, inspired by frontline Ukrainian drone
workshop practice (MZAK1, Nebokray) and adapted for 1–5 person civilian
resilience and survey teams.

---

## Concept

### Why the field pod exists

The libdrone workshop in Telč has a grid connection. Most of the time this
is invisible. When the grid fails — which is exactly when drone capability
is most needed — a drone platform without field power independence is a
demonstration piece, not a preparedness asset.

Ukraine provided the specific lesson: small drone teams that can operate
without infrastructure are disproportionately effective. The ability to
charge batteries, repair a broken arm, and print a replacement part in a
field environment — without grid power, without a fixed location, without a
logistics chain — is the difference between a deployable capability and an
equipment inventory.

### Power budget — what libdrone actually draws

Before sizing any generator or battery, the actual loads must be established.
Three realistic simultaneous scenarios define the requirements:

**Charging only** (~240W): two 6S packs at 2C on HOTA D6 Pro plus laptop.
This is the recovery scenario after a flight session.

**Charging plus repair** (~335W): two packs charging, soldering station
active, laptop, and field lighting. The most common field scenario.

**Full production** (~540W): Prusa CoreOne+ printing a replacement arm plus
two packs charging plus laptop and lighting. The demanding scenario required
when structural parts are damaged mid-deployment.

**Peak spike** (~1000W): printer bed warming up simultaneously with charger
at maximum. This is brief but must not trip a generator's thermal protection.

The minimum generator specification for full production capability: **1200W
continuous, 2000W peak**. An inverter generator (sine wave output) is
required for the Prusa CoreOne+ — PWM-modulated generator output causes
printer electronics errors.

### Power system options

**Generator path** (higher initial cost, maximum capability): Honda EU22i
or equivalent inverter generator. 2200W peak, clean sine wave, quiet
operation (~53 dBA at 7m). 3.6L tank at eco mode ≈ 4–5 hours. The standard
Czech recommendation for field production capability.

**LiFePO4 battery path** (lower noise, weather-independent): a 48V 50Ah
LiFePO4 pack (2.4 kWh) can sustain the charging-only scenario (~240W)
for approximately 8 hours or a single full production cycle (1.5–2 hours
at 540W average). Recharges from generator in ~3 hours. The combination —
LiFePO4 for routine operations, generator for extended or high-demand
sessions — is optimal.

**Solar supplement**: a 400W foldable solar panel array in summer conditions
contributes approximately 200–240W average in Central European daylight,
covering the charging-only load. Not a primary power source for full
production.

### Battery charging in the field

→ [[lipo-batteries]] covers the charging rules that apply regardless of field
or home context. The field-specific constraints:

Field charging requires LiPo charging bags (ammo boxes preferred for
puncture resistance). Never charge inside an enclosed vehicle. In temperatures
below 10°C, allow 30 minutes warm-up time before starting any charge cycle.
→ [[winter-protocol]] covers the cold-weather voltage threshold adjustments.

The HOTA D6 Pro at 2C on two 1800mAh 6S packs draws approximately 200W
and completes a charge in 30 minutes. In a field rotation: fly (12–15 min),
charge (30 min), fly. Two packs give a 30-minute continuous rotation.

### Printing in the field

The Prusa CoreOne+ is the specified printer. → [[print-profiles]] covers the
profiles that govern field print quality. Field-specific constraints:

The printer requires a level, vibration-free surface. In a vehicle or
temporary shelter, a dedicated table with non-slip pads is required.
PCCF printing requires enclosure temperature ≥25°C — in cold field conditions,
an insulated tent or vehicle cabin is the enclosure.

Field priority print sequence: arm shafts first (20 minutes each, most
likely needed), then bumpers (high crash frequency), then structural PCCF
layers only if a major structural failure requires them.

Filament storage in the field: PETG and PCCF are moderately hygroscopic.
Keep in sealed bags with silica gel. Filament that has absorbed moisture
produces stringing and poor layer adhesion.

### Pod configuration

**Minimum mobile kit** (backpack deployable, all-charging no printing):
HOTA D6 Pro charger, 3× LiPo ammo boxes, 3× 6S packs, laptop, 2.4 kWh
LiFePO4, inverter (600W), cables, field bag.

**Full production pod** (vehicle deployable, charging + repair + printing):
All of the above plus Prusa CoreOne+, Honda EU22i generator, SEQURE soldering
station, filament stock (PETG, PCCF, ASA), tools.

### Winter field operations

→ [[winter-protocol]] applies in full. Additional field-specific requirements:
Generator fuel viscosity changes below −10°C — use winter-grade fuel.
LiFePO4 capacity drops approximately 20% at −10°C. LiPo charging at
temperatures below 0°C must not be attempted — allow warm-up in the vehicle
cabin first.

The drone itself should not fly below 0°C in standard configuration —
→ [[winter-protocol]] explains why PETG arm shaft brittleness and LiPo sag
both become significant below this threshold.

---

## Reference

### Field pod power system sizing

| Scenario | Peak draw | Recommended power source |
|---|---|---|
| Charging only | ~240W | LiFePO4 2.4 kWh alone (8h endurance) |
| Charging + repair | ~335W | LiFePO4 + small generator backup |
| Full production | ~540W | Honda EU22i or equivalent |
| Peak spike (brief) | ~1000W | Generator with ≥2000W peak rating |

### Minimum field spares list

| Item | Quantity | Why |
|---|---|---|
| PETG arm shafts (printed) | 10 | Most common repair |
| Bumpers ASA | 8 + 4 spare | High crash frequency |
| Props HQProp 6" (both pitches) | 2 full sets | Any prop damage grounds flight |
| Motors 2507 1750KV | 2 | Bearing or winding failure |
| MR30 connector pairs | 5 | Motor connector damage in crashes |
| RP2 ELRS receiver | 2 | Antenna damage common |
| Silicone O-rings ID4/OD7 | 20 | Motor mount maintenance |
| Loctite 243 | 1× tube | Rod pinch bolts |
| Conformal coating (HPA200H) | 1× aerosol | Post-repair coating |

---

## Procedure

### Field pod deployment sequence

1. Level and secure printing surface before printer arrives
2. Generator: check oil, check fuel, run for 5 minutes before connecting
   any electronics load
3. LiFePO4: check state of charge before departure — arrive with full pack
4. Print 2 spare arm shafts on arrival at any new deployment site
5. Establish charging rotation: charge between flights, not during

---

## Rationale

The V2.4.6 Field Pod document was a standalone community document with full
power budget calculations, worked examples, and BOM. The 3.0.0 skeleton
delegates the LiPo handling rules to → [[lipo-batteries]], the winter protocol
to → [[winter-protocol]], and the print profiles to → [[print-profiles]] — this
skeleton provides the field-deployment architecture that connects them.

---

## Connections

requires: []
related:
  - [[sk-complete-build-guide]]
  - [[sk-operations-manual]]
  - [[sk-community-resilience-guide]]
leads_to:
  - [[sk-community-resilience-guide]]
