---
id: sk-community-resilience-guide
title: "Community Resilience Guide"
version: 1.1.0
date: 2026-06-01
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 6.evaluator
  - 2.operator
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

After reading this guide, the community group or household can decide whether
libdrone fits their preparedness context, understand what capabilities it
provides in a crisis, and know exactly what they need to build before any
crisis occurs. Learning objective: commit to building and training before any
emergency, or conclude the platform is not right for their situation.

---

## Concept

### The information gap is the danger

Every preparedness manual agrees: verified information enables better decisions.
Three streets away in a flood, you cannot see whether the road is passable.
In a chemical incident, you cannot see which direction the plume is moving.
Without a drone, you make those decisions based on rumour and assumption.

→ [[civilian-preparedness]] explains this information gap and how libdrone
closes it. The central shift is from reactive exposure to proactive assessment:
the drone goes into the hazard first, and the person goes only where the drone
confirms it is safe.

### What you can do with it — the use case register

→ [[resilience-use-cases]] maps 15 specific use cases from everyday training
(maintain the skill before you need it) through crisis assessment (flood route,
chemical plume, structural assessment) to supply delivery (water purification
tablets, medications, written communications to isolated neighbours).

The sensor payloads determine which missions are possible:

The **air quality payload** (SEN66) reads PM2.5, CO2, VOC, and radiation
precursors in real time in the pilot's goggles. PM2.5 > 35 µg/m³ means
elevated particulate — stay upwind. CO2 > 5000 ppm means hazardous atmosphere
— do not enter.

The **thermal payload** (FLIR Lepton, designed) reads body heat at 30–100m
at night. For welfare checks on isolated neighbours, night perimeter watches,
person search in flooded or collapsed areas.

Neither payload requires any external infrastructure — all data stays on the
drone's SD card and syncs to a local NAS on landing. No cloud. No subscription.
No dependency on the internet continuing to function.

### What you need before the crisis

→ [[community-deployment]] is the checklist. The most important rule, quoted
directly from the article: **a drone in a box is not preparedness. A drone that
has been flown 50 times and has spare arms on the shelf is preparedness.**

Three roles to distribute across the group: a qualified pilot who flies at
minimum monthly, a builder and maintainer who can print replacement arms and
update firmware, and a data operator who knows what PM2.5 readings mean.
One person can hold all three, but distributing them across the group makes
the capability resilient when one person is unavailable.

Spare parts that must be on the shelf before any crisis: 10 printed arm shafts
(20g PETG each, 20 minutes each), 2 spare motors, 1 spare ESC, 2 spare ELRS
receivers. All fit in a small box. → [[community-deployment]] contains the
complete equipment list.

### The regulatory picture for community operations

→ [[legal-and-regulatory]] is the single source of truth for operator
obligations — read it and decide what applies to you. Under a declared
state of emergency, IZS authorities may modify airspace access — always
follow official instructions. A neighbourhood welfare check over your own
street is categorically different from commercial drone operation.

### Why libdrone and not a commercial drone

Five properties that commercial alternatives cannot match:

→ [[foss-principles]] explains the open-source design. → [[civilian-preparedness]]
addresses the zero cloud dependency requirement. → [[bom-summary]] shows the
community-level cost. → [[foss-stack-libdrone]] shows the EU-origin, auditable
software stack.

The one-sentence answer: a commercial drone in a crisis depends on a company
continuing to operate, a cloud service continuing to function, and a supply
chain continuing to deliver spares. libdrone depends on a printer and filament.

---

## Reference

### Crisis response quick reference

| Crisis type | Payload | Key use cases |
|---|---|---|
| Flood | FPV only or thermal | UC-04 route assessment, UC-09 person search |
| Chemical / smoke | SEN66 air quality | UC-05 plume assessment — fly upwind, read PM2.5 |
| Fire / structural | Thermal | UC-06 building assessment before entry |
| Night security | Thermal + IR strobe | UC-10 perimeter sweep |
| Isolated neighbour | FPV or thermal | UC-08 welfare check |
| Supply delivery | Drop mechanism | UC-11 water purification, UC-12 medications |

---

## Procedure

### Community group activation checklist

Before any crisis:
1. One qualified pilot, current (flew within 30 days)
2. Drone built, tested, airworthy
3. At least 3 charged LiPo batteries
4. 10 spare arm shafts printed and on shelf
5. Offline documentation downloaded
6. Air quality payload bench-tested with logging confirmed
7. At least one seasonal air quality baseline flight completed

---

## Rationale

The Resilience Guide (V2.4.6) contained the full use case descriptions and
the preparedness argument as a single document. The 3.0.0 skeleton delegates
the use case specifics to atoms and provides the decision narrative: should
your community group adopt this platform, and if so, what do you need to
do before any crisis? The atoms provide the operational depth; this skeleton
provides the commitment rationale.

---

## Connections

requires: []
related:
  - [[sk-platform-brief]]
  - [[sk-municipal-emergency-guide]]
leads_to:
  - [[sk-platform-brief]]
