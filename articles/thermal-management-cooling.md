---
id: thermal-management-cooling
title: "Thermal management and cooling"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - thermal-management
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

libdrone's electronics zone generates 6 W of waste heat in hover (ESC, VTX,
FC, and buck converter) and up to 14 W at peak. An always-on Gdstime 3010
fan at the rear of the Platform draws air front-to-rear across the ESC and
FC stack. In standard open-frame configuration, the fan provides adequate
cooling under normal conditions but delivers only ~1.5°C of temperature rise
above ambient — insufficient to prevent condensation in the Czech autumn/winter
operating envelope. The Thermal Retention Shroud (TRS) addresses this by
partially enclosing the electronics zone, raising the microclimate temperature
above the dew point using the waste heat already being generated.

---

## Concept

### The cooling fan

The Gdstime 3010 (30 × 30 × 10 mm, 5V ball bearing) is hardwired to the FC
5V pad and runs continuously whenever the FC is powered — no thermostat, no
control. The "massively overcool" design philosophy: for a mapping drone that
flies methodically rather than aggressively, the thermal margin is more
important than marginal current savings from variable-speed control.

The fan is rear-facing and exhausts rearward. In hover, it creates a pressure
differential that draws air through the electronics zone front-to-rear. In
forward flight, ram air enters through front arm root gaps and is exhausted
by the fan.

Power draw: ~70 mA at 5V = 0.35 W. Always on, drawing from the FC BEC.

### Heat sources and budget

| Component | Waste heat (hover) | Waste heat (peak) |
|---|---|---|
| ESC (4 FETs, ~30A total) | ~3 W | ~8 W |
| VTX (800 mW RF, 40% PA efficiency) | ~2 W | ~5 W |
| FC + Buck converter | ~1 W | ~1 W |
| **Total** | **~6 W** | **~14 W** |

### Open-frame thermal performance

At 6 W waste heat and the fan moving 0.2 m³/min (3.3 L/s) through the open
backplane (65% open area), the temperature rise above ambient in the electronics
zone is approximately:

    ΔT = Q / (ṁ × cp)
      = 6 / (4.0×10⁻³ × 1005)
      ≈ 1.5°C

1.5°C above ambient is below the dew point margin in most Czech autumn conditions
(worst case: 5°C ambient, 90% RH → dew point ≈ 3.5°C, requires ΔT ≥ 5°C for
real protection). The open-frame build is thermally unprotected against condensation.

### Thermal Retention Shroud (TRS)

The TRS is a single printed PETG part that partially encloses the electronics
zone. By restricting airflow to approximately 20% of fan capacity through the
cavity (with 80% recirculating), the temperature rise above ambient increases
proportionally:

    T_cavity = T_amb + Q / ((1 − R) × ṁ × cp)
            = T_amb + 6 / (0.20 × 4.0×10⁻³ × 1005)
            ≈ T_amb + 7.5°C

7.5°C above ambient provides real-world protection across the Czech autumn/winter
envelope (target: ΔT ≥ 8°C). The TRS uses the waste heat already being generated
— no additional electronics, no additional power.

At forward speeds above approximately 40 km/h, ram air pressure dominates and
recirculation stops. This is acceptable — condensation risk is greatest in slow
hover and on the ground, not at cruise speed.

---

## Reference

### Fan specification

| Parameter | Value |
|---|---|
| Model | Gdstime 3010 (30 × 30 × 10 mm) |
| Voltage | 5V (hardwired to FC 5V pad) |
| Bearing | Ball bearing (adequate for always-on continuous duty) |
| Current | ~70 mA |
| Flow rate | ~0.2 m³/min |
| Mount | Platform rear face slot |
| Control | Always on — no thermostat |

### ESC temperature monitoring

The Pilotix 75A AM32 ESC reports temperature via DShot telemetry. In
Betaflight: set `set osd_esc_temp_pos` to display in OSD. Normal operating
temperature: 40–60°C at sustained hover. Above 80°C: ESC current limiting
may activate — land and investigate airflow restriction.

---

## Procedure

### Verifying adequate cooling after build

1. Fly a 5-minute hover at 80% of maximum payload (approximately hover-relevant
   throttle, not full throttle).
2. After landing, immediately feel the ESC through the backplane (carefully —
   it will be warm). Should be warm but not painful to touch (<60°C).
3. Check OSD ESC temperature during flight if configured. If consistently
   above 70°C, verify fan operation (audible, feels airflow from rear) and
   check that the airflow path is not obstructed.
4. If fan is not audible after FC boot: check 5V connection to fan leads.
   Fan failure is a maintenance-priority item — fly without fan only in cool
   conditions and at reduced throttle.

---

## Rationale

### Why ball bearing and not sleeve bearing

Ball bearing fans are rated for longer service life under continuous-duty
conditions. Sleeve bearing fans are adequate for intermittent use but
degrade faster when run continuously, particularly in horizontal orientations
where gravity acts perpendicular to the bearing's designed load axis. The
3010 in libdrone runs continuously in a horizontal airframe — ball bearing
is the correct choice.

---

## Connections

requires:
  - [[power-rail-architecture]]
related:
  - [[thermal-retention-shroud]]
  - [[conformal-coating]]
  - [[lipo-batteries]]
leads_to:
  - [[thermal-retention-shroud]]


[power-rail-architecture]: power-rail-architecture.md "Power rail architecture"
[thermal-retention-shroud]: thermal-retention-shroud.md "Thermal Retention Shroud"
[conformal-coating]: conformal-coating.md "Conformal coating"
[lipo-batteries]: lipo-batteries.md "LiPo batteries"
