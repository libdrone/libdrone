---
id: civilian-preparedness
title: "Civilian preparedness"
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
  - 5.student
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

libdrone changes the information landscape of crisis response for civilian
households and neighbourhood groups. Before any of the scenarios covered by
the Czech "72 Hours" preparedness programme — flood, chemical incident,
structural fire, elevated security risk — the person with a drone has access
to verified ground truth. Everyone else is guessing. This shift from reactive
exposure to proactive assessment is the central resilience contribution of an
aerial platform. libdrone is designed specifically for this context: repairable
from printed parts, zero cloud dependency, EU-origin and auditable, and
affordable at community level without institutional funding.

---

## Concept

### The information gap as the core danger

Every major civilian preparedness manual agrees: verified information reduces
anxiety and enables better decisions. The absence of verified information is
not silence — it is rumour, catastrophic imagination, and paralysis.

In a flood, you cannot see whether the road three streets away is passable. In
a chemical incident, you cannot see which direction the plume is moving. At
night in an elevated security situation, you cannot see who or what is
approaching along your street. After an earthquake, you cannot see whether
the building your neighbour is in is safe to enter.

A drone closes this gap. The person who can fly an assessment before committing
to an action — evacuation, shelter-in-place, physical rescue attempt — makes
fundamentally better decisions than the person who cannot.

### Three levels of impact

**Individual level**: a drone pilot can determine which evacuation routes are
passable, whether the air in a given direction is safe, whether a building under
consideration for shelter has thermal or structural hazards — without physically
entering any of those environments. The central shift: from reactive exposure
to proactive assessment.

**Neighbourhood level**: one competent pilot can check on every isolated
neighbour within 500 metres in under 10 minutes, confirm safe routes for the
group before anyone moves, provide live aerial video to the group for shared
situational awareness, and deliver critical small supplies to someone who
cannot be physically reached safely.

**Security level**: a thermal payload detects human body heat in darkness at
30–100 metres. For a group sheltering in place, periodic perimeter sweeps at
night — without exposing any person — provide advance notice of approaching
activity. This is not offensive capability. It is the civilian equivalent of
keeping watch, extended by technology.

### Psychological dimensions

Czech psychosocial preparedness research identifies several factors that
predict better outcomes in crisis:
- Having a concrete, valued task
- Feeling competent and exercising agency
- Providing irreplaceable value to the group
- Making decisions from verified information rather than rumour

Drone operation addresses all four simultaneously. For young people
specifically, learning to fly, maintain, and operate libdrone is preparation
with direct crisis utility — incomparably more engaging than theoretical
exercises.

### Why libdrone specifically for resilience

Five properties that separate libdrone from commercial alternatives in a
resilience context:

| Property | Resilience consequence |
|---|---|
| EU origin, open design | Auditable; trustworthy in sensitive contexts |
| Locally repairable from printed parts | Functions when supply chains are disrupted |
| Zero cloud dependency | Works when internet and mobile networks fail |
| Community-level affordability (~€720) | No institutional funding required |
| Extensible payload platform | One airframe, unlimited missions |

A commercial professional drone with equivalent thermal imaging capability
costs €5,000–50,000. libdrone's structural components are 3D-printed from
materials available at any hardware store. Arm shafts — the most frequently
replaced parts — are 15 g of PETG filament and 20 minutes of print time.

---

## Reference

### libdrone operational parameters for resilience planning

| Parameter | Value |
|---|---|
| All-up weight (bare) | ~410 g |
| All-up weight (with sensor payload) | ~490 g |
| Practical payload capacity | 80–150 g |
| Flight time (cruise, no payload) | 12–15 min |
| Flight time (with sensor payload) | ~10–12 min |
| Build cost (complete with goggles) | ~€720 |
| Frame filament cost | ~€16 per frame |
| Arm replacement time | < 5 min, no tools |
| Payload swap time | < 60 s |
| Radio link | ExpressLRS 2.4 GHz — no internet |
| Data logging | Local SD card — no cloud |

### Regulatory note for crisis operations

Under normal conditions, the rules in [[legal-and-regulatory]] apply. Under a declared
state of emergency (*nouzový stav*), IZS authorities may restrict or
re-authorise civilian airspace. In an active rescue zone, coordinate with
on-scene IZS commanders before any flight. Outside active rescue operations,
a neighbourhood welfare check over your own street is qualitatively different
from commercial operation. Use judgement and follow all official instructions.

**Always follow IZS guidance. libdrone extends your capability; it does not
supersede the authority of emergency services.**

---

## Procedure

<!-- not applicable — operational procedures are in resilience-use-cases -->

---

## Rationale

### Why this article is in the corpus

libdrone's primary commercial and institutional market is civilian preparedness
groups, municipal emergency management, and civil resilience organisations.
The evaluator persona (procurement) needs to understand the resilience case for
libdrone in plain, non-technical terms before they read the technical
specifications. This article provides that case directly from the 3.0.0 corpus.

---

## Connections

requires: []
related:
  - [[resilience-use-cases]]
  - [[community-deployment]]
  - [[legal-and-regulatory]]
leads_to:
  - [[resilience-use-cases]]
  - [[community-deployment]]
