---
id: first-flight
title: "First flight"
version: 1.0.1
date: 2026-05-31
author: jsa
status: released
scope: libdrone
topic:
  - piloting-operations
personas:
  - 4.workshop
  - 2.operator
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The first flight of a workshop-built drone is a structured event, not a free
session. It runs in a clear open area with a qualified instructor present,
follows the acceptance validation gate, and proceeds through a defined
sequence: hover at 1 m, land and inspect, expand to slow circuits, GPS Rescue
test. The first flight is not the end of the workshop — it is the beginning
of the operational phase. Every participant leaves having flown the drone they
built, having reviewed the Blackbox trace from that flight, and with the
knowledge of what to do when something unexpected happens.

---

## Concept

### What makes the first flight different from the maiden flight

The [[maiden-flight]] article covers the builder's own maiden flight — a data
collection event focused on verifying the build. The first flight in a
workshop context is also a learning event: the participant is flying for the
first time, likely in a supervised environment, possibly in borrowed goggles.

The differences:
- **Instructor present**: the instructor holds the emergency disarm authority
  and can take over transmitter control if needed
- **Simplified sequence**: the participant does not yet run a Blackbox analysis
  independently — the instructor guides the review
- **Emotional context**: first flights carry anxiety. The structure is not
  bureaucratic — it is there to reduce cognitive load so the participant can
  focus on the experience of flying

### The milestone this represents

A participant who completes the first flight has, in one workshop series:
- Learned parametric CAD and printed structural components
- Assembled a five-layer composite sandwich frame
- Soldered a complete electronics stack with EMC discipline
- Configured two open-source firmware systems from CLI
- Flown the machine they built

This is not a hobby outcome. It is an engineering competency outcome. The
certificate of completion from a libdrone workshop is a demonstration that
the holder has built and operated an autonomous aerial system.

---

## Reference

### First flight sequence (workshop)

**Site preparation**
- Open outdoor area, minimum 30 m from any person not in the group
- Instructor confirms acceptance validation is complete
- Instructor confirms GPS fix ≥ 8 satellites
- Participant confirmed in goggles with good link quality

**Flight 1 — hover stability (instructor supervises)**
1. Participant arms the drone (throttle low, SA switch down).
2. Instructor talks the participant through smooth throttle up to ~1.5 m hover.
3. Hold hover for 30 seconds. Instructor observes stability and participant
   body language.
4. Guided descent and disarm.
5. Inspection: motors, arm T-locks, battery.

**Flight 2 — slow translation (if Flight 1 was stable)**
6. Arm. Hover to 2 m.
7. Slow forward translation 10 m, stop, return.
8. Slow lateral translations.
9. Land. Disarm. Discuss: what did the drone feel like? What surprised you?

**Flight 3 — GPS Rescue demonstration**
10. Arm. Fly to 15 m altitude, 30 m distance.
11. Instructor activates GPS Rescue manually via SE switch.
12. Participant observes: drone climbs to rescue altitude, orients toward home,
    returns, descends.
13. Instructor hands control back via SE switch.
14. Participant lands.

**Post-flight review**
15. Download Blackbox with instructor.
16. Open Blackbox Explorer. Instructor shows: gyro spectrum, noise floor,
    RPM filter peaks (absent = working).
17. Participant logs the flight in their build logbook.

---

## Procedure

### If the participant is not ready to fly alone

After Flight 1, the instructor assesses readiness. Criteria for continuing
to Flight 2 unassisted:
- Participant maintained hover altitude within ±0.5 m
- No panic inputs observed
- Participant could describe what the drone was doing throughout hover

If criteria are not met: Flight 2 runs with instructor shadow control active.
This is not a failure — it is the correct use of the workshop structure.
There is no minimum time to solo. The progression exists to match the
participant's skill, not to meet a schedule.

---

## Rationale

### Why GPS Rescue is demonstrated in Flight 3, not left to theory

A participant who has only read about GPS Rescue will not know what it looks
like — and will not know whether their drone is experiencing GPS Rescue or
malfunctioning when they first encounter it in the field. Seeing GPS Rescue
activate deliberately, observing the drone's behaviour, and experiencing the
moment of control return turns an abstract failsafe mechanism into a known and
trusted behaviour. The demonstration takes 3 minutes and is worth more than
an hour of classroom explanation.

---

## Connections

requires:
  - [[acceptance-validation]]
  - [[flight-modes]]
  - [[betaflight-gps-rescue]]
related:
  - [[piloting-progression]]
  - [[blackbox-analysis]]
  - [[maiden-flight]]
leads_to:
  - [[piloting-progression]]
  - [[blackbox-analysis]]
