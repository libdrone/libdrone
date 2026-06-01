---
id: community-deployment
title: "Community deployment"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - resilience-community
personas:
  - 6.evaluator
  - 2.operator
  - 1.builder
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

A community resilience deployment of libdrone requires three distinct roles
(pilot, builder/maintainer, data operator), a defined equipment list including
spare parts and filament stock, and offline documentation ready for use
without internet. Skills must be maintained through regular practice — a drone
flown only once and stored for six months is not a preparedness asset. The
minimum viable deployment is one built and tested Pro platform, one trained
pilot, spare arms on the shelf, and all documentation downloaded to local
storage.

---

## Concept

### Role distribution

Three roles cover the full capability:

**Pilot**: flies at minimum monthly; current on cinematic mode, low-speed mode,
and night operations. Can respond to an emergency call and fly a meaningful
assessment mission within 15 minutes of notification.

**Builder and maintainer**: can 3D-print replacement arms, resolder a motor pad,
update firmware, and calibrate sensors. Does not need to be the pilot — in
fact, distributing these roles increases group resilience. If the pilot is
unavailable, capability does not disappear if a second person can maintain
the equipment.

**Data operator**: understands what sensor readings mean. Knows that PM2.5 > 35
µg/m³ means elevated particulate. Can interpret thermal imagery (hot spots in
a building, body heat in darkness). Translates drone data into decisions for
the group.

One person can hold all three roles. For a neighbourhood group, distributing
them across three people is significantly more resilient.

### The pre-crisis requirement

**The most important rule:** libdrone must be built, flown, and tested before
any crisis. A drone in a box is not preparedness.

A drone that has been flown 50 times and has spare arms on the shelf is
preparedness. A drone that has been used to fly the neighbourhood routes and
establish air quality baselines is preparedness. A drone that has had each
payload field-tested is preparedness.

The difference between a drone-as-tool and a drone-as-prop is 50 flights.

### Offline documentation

In a crisis with internet disruption, access to build and operational
documentation must be local. Apply the same discipline as offline maps.

Required offline: full libdrone documentation stack, wiring diagrams,
Betaflight CLI configuration, payload SDK, connector pinout diagrams.
Critical one-page references (wiring, motor replacement, Betaflight CLI
commands) should be printed and laminated, stored with the drone.

---

## Reference

### Minimum viable community deployment

| Item | Quantity | Notes |
|---|---|---|
| libdrone Pro — built and tested | 1 | Primary platform |
| libdrone Core — built and tested | 1 | Training and backup |
| Air quality payload (SEN66) | 1 | Built, field-tested |
| LiPo batteries (6S 1800mAh) | 3 minimum | Charged and regularly rotated |
| Spare arm shafts (PETG, printed) | 10 | 15 g each, 20 min print |
| Spare motors | 2 | Same spec as build |
| Spare ESC | 1 | Same model as build |
| Spare ELRS receiver (RP2) | 2 | Same firmware version |
| PETG filament | 1 kg | Standard PETG, any brand |
| PCCF filament | 1 kg | For sandwich structural layers |
| 3D printer | 1 | Operational, spare nozzle, calibrated |
| Offline documentation | Complete | Downloaded, one-page references laminated |
| LiPo charging bag | 1 | Mandatory for safe storage |

**Recommended additions** (not minimum, but strongly recommended):
- Thermal payload — extends night and search capability significantly
- Supply drop mechanism — enables contactless delivery
- IR strobe unit — enables IFF Layer 1 for security-sensitive deployments
- Remote ID module — regulatory compliance for Pro platform

### Skills maintenance schedule

| Activity | Frequency | Purpose |
|---|---|---|
| Standard FPV flight | Monthly minimum | Maintain reflexes |
| Air quality route flight | Monthly | Baseline data + skills |
| Night flight training | Quarterly | Maintain night capability |
| Emergency scenario drill | Biannually | Practice stress-response |
| Maintenance inspection | After every 10 flights | Platform reliability |
| Firmware check and update | Biannually | Security and features |

### Group briefing before first deployment

All group members who will observe or use drone data should understand:
1. The pilot is the final authority on flight safety — no one overrides the pilot
2. What the OSD shows and what it means (battery voltage, GPS sats, payload readings)
3. The decision thresholds for sensor readings (PM2.5, radiation)
4. That drone data supplements but does not replace official IZS guidance

---

## Procedure

### Standing up a community deployment from scratch

1. **Build**: complete Pro platform following the FreeCAD skeleton and
   electronics installation guides. Verify maiden flight.
2. **Train**: 10 flights minimum before any operational use. Include one
   night flight.
3. **Payload**: build and field-test the air quality payload. Log 3 outdoor
   flights of GPS-tagged data.
4. **Spares**: print 10 arm shafts. Verify printer is calibrated and
   filament stocks are sufficient.
5. **Documentation**: download complete documentation stack. Print and laminate
   critical references.
6. **Practice**: fly the local neighbourhood routes. Build a visual map of
   the area from aerial footage. Note flood-prone low spots, access bottlenecks,
   and buildings of interest.
7. **Baseline**: establish air quality baseline over 3 seasonal measurements.
8. **Drill**: simulate a crisis scenario with the group. Practice the observer
   role alongside the pilot. Debrief.

---

## Rationale

### Why the Core platform is listed as a mandatory item

The Core platform serves two functions: it is the training aircraft that
absorbs the inevitable crashes of skill development without risking the Pro
airframe, and it is the backup platform if the Pro is out of service for
repair. A community with only one drone has a single point of failure that
is guaranteed to appear at the worst possible time. The Core is smaller,
cheaper to crash, and shares the key components (FC, radio, goggles) with
the Pro — the pilot's skills transfer directly.

---

## Connections

requires:
  - [[civilian-preparedness]]
  - [[resilience-use-cases]]
related:
  - [[pre-flight-check]]
  - [[scheduled-maintenance]]
  - [[lipo-batteries]]
  - [[iff-layers]]
leads_to:
  - [[resilience-use-cases]]
