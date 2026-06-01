---
id: thermal-retention-shroud
title: "Thermal Retention Shroud"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - thermal-management
personas:
  - 1.builder
  - 8.architect
platform:
  - pro
  - ghost
  - bandit
lang: en
licence: CC BY-SA 4.0
---

## Summary

The Thermal Retention Shroud (TRS) is a single printed PETG part that partially
encloses the electronics zone on the Platform. It uses waste heat from the ESC,
VTX, FC, and buck converter to maintain a microclimate approximately 7.5°C
above ambient, preventing condensation on the electronics in the Czech
autumn/winter operating environment. The TRS uses a labyrinth inlet to restrict
fresh air flow to ~20% of fan capacity while allowing the remaining ~80% to
recirculate, maximising the temperature rise with the heat already being generated.
At forward speeds above ~40 km/h, ram air pressure breaks the recirculation and
full cooling is restored. With TRS fitted, the conformal coating specification
changes from permanent silicone to reworkable acrylic, resolving the long-standing
tension between moisture protection and component replaceability.

---

## Concept

### The labyrinth inlet

A simple open inlet would allow rain and condensation to enter directly. A
labyrinth — a series of offset baffles — forces air to change direction multiple
times before entering the cavity. Water droplets, with higher inertia than air,
cannot follow the direction changes and impinge on the baffles. The air enters
dry; the moisture stays outside.

The labyrinth inlet is sized to restrict flow to approximately 20% of fan design
capacity. This is the key constraint: too large = insufficient temperature rise;
too small = ESC thermal risk from insufficient cooling.

### The recirculation path

With the labyrinth restricting fresh air inflow, most of the air the fan pushes
rearward re-enters the cavity from the sides rather than exiting to atmosphere.
This recirculation means the same warm air passes through the electronics zone
repeatedly, accumulating temperature. At 80% recirculation:

    T_cavity = T_amb + 6 W / ((1 − 0.80) × 4.0×10⁻³ kg/s × 1005 J/kg·K)
            ≈ T_amb + 7.5°C

The recirculation path must not obstruct the fan exhaust — the fan must be able
to expel air rearward to drive the circulation. The TRS geometry creates a
sealed top and sides for the cavity with openings at the labyrinth inlet
(front/top) and the fan exhaust (rear).

### Conformal coating change with TRS

With TRS fitted, the electronics zone is no longer directly exposed to rain or
condensation. The moisture protection role shifts from conformal coating (first
defence) to thermal exclusion (primary defence) + conformal coating (secondary,
for edge cases). This allows switching from permanent silicone conformal coating
to reworkable thin acrylic coating. Acrylic can be removed with acetone for
component rework — something silicone cannot do cleanly.

**Without TRS**: silicone conformal coating (permanent, highest protection).
**With TRS**: acrylic conformal coating (reworkable, adequate protection given
thermal exclusion).

---

## Reference

### TRS print specification

| Parameter | Value |
|---|---|
| Material | PETG Natural |
| Layer height | 0.20 mm |
| Perimeters | 4 minimum |
| Print orientation | Flat (largest face on bed) |
| Supports | None required |
| Approx mass | ~15–18 g |
| Attachment | M3 screws to Backplane posts |

### Labyrinth inlet dimensions

The labyrinth inlet area is sized for ~20% fan flow at a healthy inlet velocity
of 3–3.5 m/s:

    Required area ≈ 0.20 × 0.2 m³/min / 3.2 m/s × (1/60)
                ≈ 200 mm²

The labyrinth baffles are two offset rows of 8 mm tall × 3 mm thick baffles
spaced 6 mm apart. Each baffle row forces a 180° direction change. Water droplet
separation efficiency at inlet velocities 2–5 m/s: >95%.

### Operating envelope

| Condition | TRS effect |
|---|---|
| Hover, calm air | 7.5°C above ambient, recirculation active |
| Slow forward flight (<40 km/h) | Partial recirculation, reduced ΔT |
| Fast forward flight (>40 km/h) | Ram air breaks recirculation, full cooling |
| Rain / drizzle | Labyrinth blocks direct water ingress |
| Heavy rain | Not rated — land before heavy rain |

---

## Procedure

### TRS installation

1. Verify the fan is operational before fitting the TRS — the TRS reduces
   cooling airflow deliberately; a non-functional fan under TRS is a
   thermal risk.
2. Align TRS over the electronics zone on top of the Backplane.
3. Secure with 4× M3 × 8 mm screws into the Backplane posts.
4. Verify the labyrinth inlet faces forward (toward the nose).
5. Verify the fan exhaust slot in the TRS aligns with the Platform fan slot.
6. After installation: power on and verify fan is audible. Feel for slight
   warm air from the exhaust.

### First flight check with TRS

1. After a 3-minute hover, check ESC temperature via OSD.
2. Should read 40–65°C. If above 70°C, verify TRS installation is correct
   and fan is functional.
3. After landing, feel the underside of the TRS — should be warm, not hot.

---

## Rationale

### Why a physical shroud and not forced active cooling

Active cooling (variable-speed fan with temperature sensor) would provide more
precise thermal management but adds complexity, a controllable component, and
a potential single point of failure. The TRS achieves the required microclimate
using only fluid dynamics and the heat that is already being generated — no
additional electronics, no power draw, no failure modes. Elegant thermal
engineering uses what is already there.

---

## Connections

requires:
  - [[thermal-management-cooling]]
related:
  - [[conformal-coating]]
  - [[lipo-batteries]]
leads_to:
  - [[airframe-integration]]


[thermal-management-cooling]: thermal-management-cooling.md "Thermal management and cooling"
[conformal-coating]: conformal-coating.md "Conformal coating"
[lipo-batteries]: lipo-batteries.md "LiPo batteries"
[airframe-integration]: airframe-integration.md "Airframe integration"
