---
id: li-ion-batteries
title: "Li-Ion batteries"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: generic
topic:
  - propulsion
personas:
  - 1.builder
  - 5.student
  - 8.architect
platform:
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

Lithium-Ion (Li-Ion) cells offer higher energy density than LiPo pouch cells
at the cost of lower peak discharge current. In drone applications this
trade-off is mission-specific: Li-Ion is the correct chemistry for
long-endurance platforms with low average current demand (Ghost, Wing), while
LiPo is correct for high-performance platforms with high peak current demand
(Pro, Bandit). On Ghost, a 4S2P pack of Sony VTC6 18650 cells provides
approximately 6 000 mAh at ~436 g — delivering 30–45 minutes hover endurance
that LiPo cannot match at the same weight.

---

## Concept

### Energy density vs power density

LiPo cells are optimised for power density: the ability to deliver high current
in short bursts. A 4S 850 mAh LiPo (Bandit) can deliver 25–50C discharge rates
— 21–42 A from an 850 mAh cell. This enables rapid throttle response, high
climb rates, and the sustained power demand of sport flight.

Li-Ion 18650 cells are optimised for energy density: the amount of energy
stored per unit of weight. A Sony VTC6 stores approximately 250 Wh/kg —
compared to a typical LiPo's 150–180 Wh/kg. The price is a lower maximum
discharge rate: VTC6 is rated at 30 A continuous, but a 2P configuration
(two cells in parallel per series string) doubles this to 60 A — sufficient
for Ghost's low-KV motors at survey-mission current demands.

For Ghost's operating profile — large props at low RPM, moderate forward speed,
no aerobatic manoeuvres — the average current draw is 8–15 A total. A 6 000 mAh
pack at this current draws down over 24–45 minutes. The same mission on a
6 000 mAh LiPo pack would be significantly heavier with minimal range benefit.

### 4S2P construction

Ghost's battery is a 4S2P pack: four series groups, each containing two 18650
cells in parallel. The series groups establish the nominal voltage (4 × 3.6 V =
14.4 V nominal, 16.8 V fully charged). The parallel pairs double the capacity
(2 × 3 000 mAh = 6 000 mAh) and double the maximum discharge current
(2 × 30 A = 60 A). Cell matching — selecting cells with identical capacity
and internal resistance — is important in parallel groups; mismatched cells
in parallel will not share current equally and the weaker cell will overheat.

### Charging and storage

Li-Ion charges to 4.2 V/cell maximum (same as LiPo). Standard CC/CV charging
at 1C (6 A for a 6 000 mAh pack) is appropriate. Unlike LiPo, Li-Ion does not
need storage voltage management with the same urgency — cells stored at 50%
charge degrade slowly over months. Fire risk from Li-Ion is lower than LiPo:
the liquid electrolyte in 18650 cells is less prone to thermal runaway from
mechanical damage than the thin LiPo pouch design, but the risk is not zero.
Charge supervision and metal storage containers remain best practice.

---

## Reference

| Parameter | Sony VTC6 18650 | Typical 4S LiPo |
|---|---|---|
| Nominal voltage | 3.6 V/cell | 3.7 V/cell |
| Capacity (single cell) | 3 000 mAh | varies |
| Max continuous discharge | 30 A/cell | 25–50C × capacity |
| Energy density | ~250 Wh/kg | ~150–180 Wh/kg |
| Charging voltage | 4.2 V/cell | 4.2 V/cell |
| Storage voltage | 3.6–3.7 V/cell | 3.8 V/cell |
| Thermal runaway risk | Lower | Higher |

**Ghost 4S2P pack specification:**
- Cells: 8× Sony VTC6 (or equivalent matched cells)
- Configuration: 4S2P
- Nominal capacity: 6 000 mAh
- Nominal voltage: 14.4 V
- Connector: XT60
- Estimated pack mass: ~436 g (cells + housing + wiring)

**ArduPilot failsafe voltage (Ghost — adjust from LiPo defaults):**
    BATT_LOW_VOLT,14.4     ; 3.6V/cell — Li-Ion flatter discharge curve
    BATT_CRT_VOLT,14.0     ; 3.5V/cell — do not discharge below this

---

## Procedure

### Build a 4S2P 18650 pack

1. Match cells: measure OCV and internal resistance of all 8 cells. Group
   pairs with < 10 mΩ difference and < 5% capacity difference.
2. Spot-weld or solder parallel pairs (2P groups): connect positive to
   positive, negative to negative. Do not use heat shrink yet.
3. Series-connect the 4 groups: positive of group 1 to negative of group 2,
   etc. Verify 4S voltage: ~14.4 V nominal when all cells at 3.6 V.
4. Add balance leads: one lead per series cell group boundary (5-pin JST-XH
   for 4S).
5. Wrap in kapton tape, then heat shrink. Add XT60 connector.
6. Initial charge at 0.5C (3 A) to verify all cells charge and balance correctly.

---

## Rationale

Sony VTC6 cells were specified for Ghost rather than cheaper 18650 alternatives
because VTC6's 30 A continuous discharge rating provides sufficient headroom
for the 4S2P pack at Ghost's operating current without cell stress. Cheaper
cells rated at 10–15 A continuous would require a larger parallel count (3P or
4P) to achieve the same discharge headroom, adding mass and build complexity.
VTC6 is widely available, well-characterised, and a known quantity in the
battery pack building community.

---

## Connections

requires:
  - [[lipo-batteries]]
related:
  - [[ghost-variant]]
  - [[ardupilot-failsafe]]
  - [[power-rail-architecture]]
  - [[voltage-regulation]]
leads_to:
  - [[ghost-variant]]
  - [[ardupilot-failsafe]]


[lipo-batteries]: lipo-batteries.md "LiPo batteries"
[ghost-variant]: ghost-variant.md "Ghost variant"
[ardupilot-failsafe]: ardupilot-failsafe.md "ArduPilot failsafe"
[power-rail-architecture]: power-rail-architecture.md "Power rail architecture"
[voltage-regulation]: voltage-regulation.md "Voltage regulation"
