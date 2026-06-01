---
id: post-flight-check
title: "Post-flight check"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - piloting-operations
personas:
  - 2.operator
  - 1.builder
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The post-flight check runs immediately after landing and before battery
removal. It catches damage while the context of the flight is fresh, ensures
the battery is handled correctly before it is warm, and documents flight data
before it is overwritten. The check takes 3–5 minutes and is not optional —
damage found immediately after landing costs minutes to document; damage found
two flights later is ambiguous in origin and harder to attribute.

---

## Concept

### Why immediately after landing

Two things degrade quickly after landing: LiPo temperature and pilot memory.
A battery pulled from a drone immediately after landing may be too warm to
handle safely or to put in storage. The post-flight check is the correct
use of the 15-minute cooling window — inspect the drone, download Blackbox
if warranted, log flight data, and by the time all of this is done the battery
has cooled enough to handle.

Pilot memory of an in-flight anomaly — a brief vibration, an unusual sound, a
moment of unexpected drift — is accurate for approximately 5–10 minutes after
landing. Logging it immediately produces a useful defect report. Logging it
the next day produces a vague recollection.

---

## Reference

### Post-flight check sequence

**Immediate (battery still warm, drone still armed position)**

1. Disarm. Transmitter still on.
2. Feel all 4 motor housings: warm = normal, hot = log and investigate.
3. Visual check: any visible damage to props, arms, or bumpers?
4. Check battery for swelling or deformation. If swollen: isolate immediately,
   do not charge or reuse.

**After battery removal**

5. Remove battery. Set aside to cool for 15–20 minutes.
6. Press each arm laterally: T-lock engagement should show no play.
7. Inspect propellers under good light: any crack, chip, or deformation —
   discard and replace.
8. Check motor mount passive covers: no cracking or loosening.

**Documentation**

9. Log in flight logbook:
   - Date, site, flight number (running total)
   - Battery pack used and cycle count increment
   - Flight duration (approximate)
   - Any anomalies observed in flight
   - Any damage found in post-flight check

10. If an anomaly was observed in flight: download Blackbox while memory is
    fresh. Add Blackbox file reference to log entry.

**Battery handling**

11. If flying again within 2 hours: battery can rest at flight voltage.
12. If not flying within 3 days: run storage discharge to 3.85V/cell (22.1V).
13. Never charge a warm battery. Wait minimum 15 minutes after landing.
14. Store in LiPo ammo box, not in the drone or vehicle boot.

---

## Procedure

### When to escalate to corrective maintenance

Stop further flights and perform corrective maintenance if any of the
following are found:

- Motor temperature > 65°C after normal flight profile
- Any T-lock showing play (arm moves under lateral hand pressure)
- Any prop cracked, chipped, or deformed
- Battery swollen or deformed
- Passive motor cover cracked or displaced
- Any in-flight anomaly that could not be explained (unexpected vibration,
  motor sound change, control response change)

---

## Rationale

### Why battery cooling time is part of the post-flight check

A LiPo battery that is still warm from flight has elevated internal resistance
and is chemically more reactive than at room temperature. Charging a warm LiPo
accelerates electrolyte decomposition and reduces cycle life. The 15-minute
post-flight check window is deliberately sized to coincide with the battery
cooling window — the check is not a delay, it is the correct use of waiting time.

---

## Connections

requires: []
related:
  - [[pre-flight-check]]
  - [[scheduled-maintenance]]
  - [[lipo-batteries]]
  - [[blackbox-analysis]]
leads_to:
  - [[scheduled-maintenance]]
