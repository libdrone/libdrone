---
id: scheduled-maintenance
title: "Scheduled maintenance"
version: 1.0.0
date: 2026-04-12
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

libdrone maintenance is interval-based: specific tasks are triggered by flight
count, flight hours, elapsed time, or crash events. The most safety-critical
intervals are floating motor mount O-ring replacement (every 20–30 flight hours)
and post-crash arm inspection (every crash, regardless of apparent damage).
Battery condition is assessed after every flight using resting voltage per cell.
A simple logbook — even a notes file — tracking flight count, battery cycles,
and any maintenance performed is the minimum required to maintain situational
awareness of the platform's condition.

---

## Concept

### Why intervals matter

A drone that has flown 50 hours has worn O-rings, fatigued solder joints, and
accumulated vibration stress in the frame that a drone with 5 hours does not.
Visual inspection at each pre-flight catches visible damage; interval-based
maintenance catches the invisible degradation that pre-flight inspection misses.
The silicone O-rings in the floating motor mounts are the highest-replacement-
frequency item: they harden and crack with UV and heat exposure, and degraded
O-rings transmit more vibration to the gyroscope, degrading flight quality
before they fail visibly.

### Crash-triggered vs flight-interval maintenance

Some maintenance tasks are triggered by an event (crash) rather than an
interval. After any hard landing or crash, even one that appears minor,
the post-crash inspection is mandatory. Hairline cracks in PCCF layers are
not visible from outside the frame and only become apparent under load —
in the air. The cost of a ground inspection is 10 minutes; the cost of an
in-flight structural failure is the drone.

---

## Reference

### Maintenance schedule

| Component | Task | Interval |
|---|---|---|
| Props | Visual inspection for cracks, chips, looseness | Every flight |
| Props | Balance check on magnetic balancer | Every 10 flights or after any tip strike |
| Motor mount O-rings | Visual inspect for cracking or deformation | Every 5 flights |
| Motor mount O-rings | Replace complete set (O-rings + sleeves) | Every 20–30 flight hours |
| Motor mount screws | Re-torque to 0.4–0.5 N·m | Every 10 flights |
| Arm T-locks | Press each arm, check for lateral play | Every flight (pre-flight) |
| Sandwich bolts | Re-torque to 0.3 N·m | Every 20 flights |
| CF rods | Acoustic ping — confirm ring tone | Every 20 flights |
| FC connectors | Visual inspect for corrosion or looseness | Every 20 flights |
| Conformal coating | Visual inspect for chips or peeling | Every 20 flights; after rain |
| Battery | Resting voltage per cell, check for swelling | After every flight |
| Battery | Storage charge/discharge if not flying within 3 days | As needed |
| Battery | Full cycle (charge + fly + measure capacity) | Every 20 charge cycles |
| GX12 connectors | Inspect pins, verify lock rings | Every 10 flights |

### Post-crash inspection sequence

Inspect in order from the most to least likely damaged:

1. **Props**: inspect all 4. Replace any with visible damage.
2. **Arm shafts**: flex each by hand. Any play = fractured shaft. Replace.
3. **Arm tabs and T-slots**: remove shaft (4× M2 screws). Inspect T-lock
   root on each tab for cracking. Inspect T-slot walls in PCCF for cracking.
4. **Motor mount O-rings**: inspect for tearing. Replace if torn.
5. **CF rods**: acoustic ping all 4. Dull sound = rod loose. Re-seat.
6. **Sandwich bolts**: re-torque all to 0.3 N·m.
7. **Electronics**: check all connector seating. Visual inspect for impact
   damage. Review Blackbox on next flight for anomalies.
8. **Battery**: inspect for swelling, deformation, puncture. Retire if any.

### Motor mount O-ring replacement procedure

1. Remove motor (4× M3 motor mount screws). Disconnect MR30.
2. Remove passive cover.
3. Remove old O-rings and sleeves. Discard — never reuse degraded isolators.
4. Clean arm head surface with IPA. Allow to dry fully.
5. Apply thin film of Super Lube 52004 to new sleeves and O-rings.
6. Insert sleeves into motor bolt holes. Place O-rings in arm head counterbores.
7. Reinstall motor and passive cover. Torque to 0.4–0.5 N·m cross-pattern.
8. Verify: passive cover does not contact arm head except at O-ring bosses.

---

## Procedure

### Maintaining a flight logbook

Minimum entries per session:
- Date
- Flight count (increment each flight)
- Total flight time (running total)
- Battery cycles used (by pack identifier)
- Any maintenance performed
- Any anomalies noted

A simple notes app or spreadsheet is sufficient. The logbook answers:
"When did I last replace the O-rings? How many flights on this battery? Was
there a hard landing recently that I should inspect for?" — questions that
are impossible to answer reliably from memory after 50 flights.

---

## Rationale

### Why O-ring replacement is on a flight-hour interval rather than calendar time

O-ring degradation is driven by heat cycles (from motor temperature), UV
exposure, and mechanical compression/release cycles — all proportional to
flight hours, not calendar time. A drone flown intensively for 20 hours in
a month degrades O-rings more than the same drone flown for 20 hours over
a year. The interval is hours-based because hours are the relevant stress measure.

Calendar time is a secondary trigger: if the drone has been stored for more
than 6 months without flying, inspect the O-rings regardless of flight hours
— silicone ages, especially in warm storage conditions.

---

## Connections

requires:
  - [[floating-motor-mounts]]
  - [[failure-hierarchy]]
related:
  - [[pre-flight-check]]
  - [[arm-shaft]]
  - [[lipo-batteries]]
  - [[winter-protocol]]
leads_to:
  - [[piloting-operations]]
