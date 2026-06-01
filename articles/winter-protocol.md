---
id: winter-protocol
title: "Winter protocol"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - safety-regulations
personas:
  - 2.operator
  - 1.builder
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

libdrone is not rated for flight below 0°C in its standard configuration.
Two independent failure mechanisms apply: PETG arm shafts become more brittle
below 0°C, making crash fractures more energetic and less predictable; and
LiPo batteries lose capacity non-linearly in cold, with a pack at +5°C
potentially behaving as if 30–40% of its rated capacity is unavailable.
Winter operations are possible with procedural mitigations — battery warming,
reduced flight time planning, higher landing voltage thresholds, and increased
crash inspection discipline — but the standard build is not optimised for
sustained sub-zero use.

---

## Concept

### PETG behaviour below 0°C

PETG undergoes a transition toward brittler behaviour as temperature drops.
Above the glass transition temperature (~80°C for PETG), it softens. Below
approximately 0°C, impact toughness decreases measurably — a crash that would
produce a clean arm shaft fracture at +20°C may produce a more complex failure
at −10°C: multiple fracture points, fragmentation, or energy transfer beyond
the designed failure hierarchy.

The PCCF structural layers are less affected by temperature in this range —
their brittleness is already a design consideration at room temperature. The
risk is primarily in the PETG arm shafts losing their designed ductile failure mode.

**Practical threshold**: do not fly below 0°C in standard configuration.
The 0°C limit is a conservative boundary that maintains the designed failure
hierarchy with reasonable confidence.

### LiPo capacity loss in cold

LiPo internal resistance increases as temperature decreases. The increased
resistance causes two effects under load: greater voltage sag (the terminal
voltage drops further under the same current draw), and reduced effective
capacity (energy that is theoretically in the cells cannot be extracted before
the voltage drops below the cutoff threshold).

At +5°C, a 1800 mAh pack may behave as if only 1100–1300 mAh is available.
At −5°C, effective capacity may be 800–1000 mAh. Flight time planning based
on room-temperature capacity figures will overestimate available flight time
significantly.

Additionally, the voltage sag under load is larger in cold conditions. The OSD
voltage reading during a hover will be lower than at room temperature for the
same state of charge, and will recover to a higher value when throttle reduces.
This makes voltage-based remaining capacity estimation less reliable.

### Winter voltage thresholds

At low temperatures, landing at the standard minimum voltage (3.5 V/cell,
21.0V) may leave the pack over-discharged from a cold-recovery standpoint.
A cell that reads 21.5V at rest (3.58V/cell) after landing in cold conditions
may actually be at a lower effective state of charge than the same reading
at room temperature.

Apply the winter voltage diff to Betaflight:
    set vbat_min_cell_voltage = 36    # 3.6V (instead of 3.5V)
    set vbat_warning_cell_voltage = 37 # 3.7V (instead of 3.6V)

This raises the warning threshold conservatively. Land sooner in cold conditions.

---

## Reference

### Winter operating limits

| Parameter | Standard | Winter (< +5°C) |
|---|---|---|
| Minimum temperature | 0°C | Not recommended below 0°C |
| Battery pre-warm | Not required | Transport in inside pocket to site |
| Time from warm storage to flight | Not specified | Fly within 10 minutes of removing from pocket |
| Minimum landing voltage | 21.0V (3.5V/cell) | 21.6V (3.6V/cell) |
| OSD warning voltage | 21.6V (3.6V/cell) | 22.2V (3.7V/cell) |
| Flight time estimate | Per capacity | Reduce estimate 30–40% |
| Post-crash inspection | Standard | Extended — check all arms individually |
| Battery storage after flight | Standard | Allow 30 min warm-up before storage charge |

### Winter Betaflight CLI diff

    set vbat_min_cell_voltage = 36
    set vbat_warning_cell_voltage = 37
    save

Revert to standard values when flying above +5°C.

---

## Procedure

### Winter flight procedure

1. Store batteries at room temperature. Do not store in vehicle or cold space.
2. Transport batteries in an inside jacket pocket or insulated bag to the site.
3. At the site, keep batteries warm until 5 minutes before flight.
4. Apply winter voltage diff to Betaflight before the first winter flight of
   the season (revert when temperatures return above 5°C).
5. Reduce planned flight time by 30–40% from room-temperature estimates.
6. Monitor OSD voltage more frequently than usual — voltage sag spikes are
   larger in cold.
7. Land at the raised warning threshold (22.2V at hover).
8. After landing, allow battery to warm to room temperature (~30 minutes)
   before running a storage charge. Cold charging raises internal resistance
   and can cause lithium plating on the anode.

### Post-flight battery handling in cold

Never charge a cold battery. Allow 30 minutes warm-up at room temperature
before connecting to the charger. A battery charged while cold may show
a full charge voltage but have reduced capacity on the next flight — lithium
plating on the graphite anode reduces effective capacity and eventually causes
internal shorts.

---

## Rationale

### Why 0°C is the limit and not −10°C or −5°C

The 0°C limit is a safety margin, not a measured material limit. PETG's
impact toughness reduction below 0°C is gradual, not a cliff. The limit
is set at 0°C because it is easy to identify in the field, it provides a
conservative margin above the temperature where failure behaviour begins to
deviate from the designed hierarchy, and it aligns with the battery
performance degradation threshold at which planning becomes difficult.
Operators with specific cold-weather requirements should test arm shaft
fracture behaviour at their operating temperature before deploying.

---

## Connections

requires:
  - [[lipo-batteries]]
  - [[failure-hierarchy]]
related:
  - [[pre-flight-check]]
  - [[risk-assessment]]
  - [[arm-shaft]]
leads_to:
  - [[piloting-operations]]


[lipo-batteries]: lipo-batteries.md "LiPo batteries"
[failure-hierarchy]: failure-hierarchy.md "Failure hierarchy"
[pre-flight-check]: pre-flight-check.md "Pre-flight check"
[risk-assessment]: risk-assessment.md "Risk assessment"
[arm-shaft]: arm-shaft.md "Arm shaft"
[piloting-operations]: piloting-operations.md "Piloting and operations"
