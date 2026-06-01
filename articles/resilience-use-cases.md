---
id: resilience-use-cases
title: "Resilience use cases"
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
platform:
  - pro
  - bandit
lang: en
licence: CC BY-SA 4.0
---

## Summary

libdrone enables fifteen distinct use cases for civilian and community crisis
response, organised from everyday training through to active emergency scenarios.
The four payload systems — air quality (SEN66), thermal imaging, radiation survey
(Geiger-Müller), and supply drop (servo release) — cover the most common civilian
assessment needs. No single flight requires all payloads; each mission selects the
appropriate instrument. The most important preparedness rule: the drone must be
built, flown, and tested before any crisis. A drone in a box is not preparedness.

---

## Concept

### Payload-mission matrix

Each payload enables a distinct class of mission:

| Payload | Primary missions |
|---|---|
| Air quality (SEN66) | Chemical/smoke assessment, air quality baseline, pollution mapping |
| Thermal imaging | Person search, building survey, night perimeter watch, structural assessment |
| Radiation survey | Post-incident zone assessment before human entry |
| Supply drop (servo release) | Medication delivery, water purification tablets, written communications |
| FPV only (no payload) | Route reconnaissance, welfare checks, situational awareness |

---

## Reference

### Use case register

**Everyday and training use cases**

| ID | Use case | Payload | Key action |
|---|---|---|---|
| UC-01 | Pilot training and skills maintenance | None | Fly monthly minimum |
| UC-02 | Local air quality baseline mapping | SEN66 | Monthly route, log to local NAS |
| UC-03 | Neighbourhood aerial survey | FPV | Seasonal survey, archive offline |

**Crisis assessment**

| ID | Use case | Payload | Key action |
|---|---|---|---|
| UC-04 | Flood route assessment | FPV | Fly intended route before committing to it |
| UC-05 | Chemical or smoke plume assessment | SEN66 | Fly upwind first; read live PM2.5 in OSD |
| UC-06 | Structural assessment after fire/collapse | Thermal | Fly all building faces; look for hot spots |
| UC-07 | Radiation zone assessment | Geiger-Müller | Grid pattern at 1–3 m altitude; threshold 1 µSv/h |

**Person search and welfare**

| ID | Use case | Payload | Key action |
|---|---|---|---|
| UC-08 | Welfare check on isolated neighbours | Thermal or FPV | Check for movement/heat through windows |
| UC-09 | Search in flooded or collapsed areas | Thermal | Systematic grid; GPS-coordinate any heat signature |
| UC-10 | Night perimeter sweep | Thermal | Consistent low-speed route; two-person operation |

**Supply delivery**

| ID | Use case | Payload | Key action |
|---|---|---|---|
| UC-11 | Water purification tablets | Supply drop | Slow hover-and-release; pre-test accuracy |
| UC-12 | Essential medications | Supply drop | Coordinate with recipient; weatherproof container |
| UC-13 | Written communications | Supply drop | Laminated note in waterproof pouch; < 20 g |

**Coordination and information**

| ID | Use case | Payload | Key action |
|---|---|---|---|
| UC-14 | Shared situational awareness | FPV | Two goggle sets; pilot + observer roles |
| UC-15 | Pre-movement route reconnaissance | FPV | Fly the route; review video; then move |

### Critical thresholds for sensor-based decisions

| Sensor | Reading | Decision |
|---|---|---|
| PM2.5 | < 12 µg/m³ | Clean air — safe to proceed |
| PM2.5 | 12–35 µg/m³ | Moderate — monitor, limit exposure |
| PM2.5 | > 35 µg/m³ | Elevated — shelter or use respiratory protection |
| CO₂ | < 1000 ppm | Normal background |
| CO₂ | > 5000 ppm | Hazardous — do not enter unprotected |
| Radiation (dose rate) | < 0.3 µSv/h | Czech normal background |
| Radiation | > 1 µSv/h | Do not enter without official clearance |

These are field decision thresholds only. Always defer to official IZS guidance
when authorities are present and accessible.

---

## Procedure

### Pre-crisis readiness checklist

The drone must be tested on each payload before any crisis:

- [ ] Air quality payload: complete a 10-minute outdoor flight, verify GPS-tagged
  data logs to SD card and syncs to local NAS
- [ ] Thermal payload: fly outdoors at dusk, verify thermal contrast between
  persons and background in goggles
- [ ] Supply drop mechanism: complete 5 drop-accuracy tests in a controlled
  environment; confirm servo actuation from TX16S AUX switch
- [ ] Route reconnaissance: fly a planned local evacuation route end-to-end;
  review SD card video immediately after

---

## Rationale

### Why the use cases span from everyday to extreme scenarios

Preparedness is a skill that degrades without practice. A pilot who only flies
in emergencies will make worse decisions under stress than one who flies regularly
for non-emergency purposes. The everyday use cases (air quality baseline, neighbourhood
survey) maintain the skill and calibrate the sensor baseline simultaneously.
The crisis use cases build directly on that foundation — the pilot already knows
the area, already has baseline data, and already knows their equipment. Treating
the two as separate categories ("training" vs "real") is a false distinction
that produces pilots who are undertrained for the moment that matters.

---

## Connections

requires:
  - [[civilian-preparedness]]
related:
  - [[payload-integration]]
  - [[induced-velocity]]
  - [[pre-flight-check]]
leads_to:
  - [[community-deployment]]
