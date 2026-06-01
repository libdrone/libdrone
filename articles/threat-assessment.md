---
id: threat-assessment
title: "Threat assessment"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: generic
topic:
  - iff-deconfliction
personas:
  - 9.defense
  - 6.evaluator
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The drone threat landscape has changed irreversibly. Small commercial and
DIY drones are now standard equipment for criminal organisations, hybrid
warfare actors, and state-affiliated groups operating below the threshold of
conventional armed conflict. The challenge is not detecting large military
UAVs — it is distinguishing hostile small drones from the expanding population
of legitimate civilian drones operating in the same airspace. This ambiguity
is the operational problem. libdrone's IFF architecture responds to this
specific problem: not by identifying hostile drones, but by making friendly
civilian drones positively identifiable, removing them from the ambiguous
population.

---

## Concept

### The identification problem at scale

Traditional air defence was designed around a small number of large aircraft
operating in segregated airspace. The sensor, decision, and response timelines
were measured in minutes. A radar operator could distinguish a commercial
airliner from a military fast jet.

The modern small drone environment has inverted every parameter:
- Hundreds to thousands of platforms in overlapping airspace
- Visual and radar cross-sections below conventional detection thresholds
- Decision timelines measured in seconds, not minutes
- No reliable single indicator distinguishing friendly from hostile

A drone overhead is now a Bayesian problem. The observer has incomplete
information and must assign a probability to hostile intent based on indirect
signals: flight pattern, altitude, speed, emissions signature, time of day,
and operational context. An observer who sees a drone with an IR strobe
pulsing at a known friendly pattern can immediately remove it from the
ambiguous population. An observer who sees a dark drone with no emissions
cannot.

### What libdrone can and cannot do

**Can do:**
- Make every libdrone positively identifiable to allied observers via the
  layered IFF architecture
- Remove libdrone platforms from the ambiguous population in the observer's
  threat assessment
- Provide GPS position to allied tactical networks in near-real time
- Enable selective emissions control when broadcasting is tactically inadvisable

**Cannot do:**
- Identify hostile drones (libdrone is a civilian platform, not a C-UAS system)
- Replace classified military IFF (Mode 4/5 transponders are not accessible to
  civilian operators)
- Guarantee deconfliction in environments where allied tactical networks are
  unavailable or compromised
- Operate safely in active kinetic environments — libdrone is civilian
  preparedness infrastructure, not a military platform

### The three threat categories relevant to civilian operations

**Category 1 — Criminal surveillance and interference.** Unauthorised drones
used to surveil facilities, map security perimeters, or interfere with
operations. Primary defence: awareness of the airspace. A community group
that knows what it is seeing overhead (IR strobe = friendly libdrone; no
strobe = investigate) is better positioned to respond.

**Category 2 — Hybrid warfare actors.** State-affiliated groups using small
drones for reconnaissance and psychological effect below the threshold of
declared conflict. The Czech Republic's position near the eastern EU border
makes this a planning assumption, not a theoretical concern. Primary defence:
the same layered IFF that makes libdrone visible to allied observers also
makes hostile drones visibly absent from the friendly registry.

**Category 3 — Fratricide and deconfliction failure.** Friendly assets being
mistaken for hostile. This is the primary addressable risk for libdrone. An
IR strobe, Remote ID, and CoT position on an allied tactical map directly
reduce this risk. The Ukraine experience from 2022 onward demonstrates
consistently that fratricide of small drones by allied forces was reduced
when IR strobe discipline was enforced.

---

## Reference

### Threat indicator matrix

| Indicator | Suggests hostile | Suggests friendly | Inconclusive |
|---|---|---|---|
| IR strobe (850/940nm) | Absent | Present at known pattern | Absent (day) |
| Remote ID | Absent or spoofed | Present, registered operator | Present, unknown operator |
| CoT on allied TAK network | Absent | Present as blue track | — |
| Flight pattern | Loitering near sensitive area | Transit, survey pattern | Any |
| RF emissions | Unknown / non-standard | ELRS 2.4 GHz, HDZero 5.8 GHz | Any single signal |
| Altitude | < 20m loitering | Mission-appropriate | Any |
| Time | Night, poor visibility | Daylight, filed with authority | Any |

No single indicator is definitive. Threat assessment is a composite judgment.
The value of IFF is reducing the number of unknowns, not eliminating ambiguity.

---

## Procedure

### Site threat assessment before deployment

For any deployment in a security-sensitive environment:

1. Identify the threat category most relevant to the site and mission
2. Determine which IFF layers are available and appropriate
   (Remote ID broadcasting appropriate? Or is emissions control required?)
3. Confirm IR strobe is fitted and operational before departure
4. If CoT integration is planned: confirm TAK server is accessible and
   credentials are provisioned
5. Brief all observers and support personnel on the libdrone IR strobe pattern
   so they can positively identify friendly platforms
6. Establish a challenge procedure for any unidentified drone observed during
   the operation

---

## Rationale

### Why civilian operators need threat assessment competency

A civilian operator who does not understand the threat landscape cannot make
good decisions about which IFF layers to deploy, whether to use emissions
control, or how to respond to an unidentified drone observation. Threat
assessment is not a military skill being inappropriately applied to civilian
operations — it is the prerequisite for using the IFF architecture intelligently.
An operator who blindly follows a checklist without understanding why is one
edge case away from a dangerous decision.

---

## Connections

requires:
  - [[iff-layers]]
related:
  - [[iff-architecture]]
  - [[emissions-control]]
  - [[remote-id-compliance]]
  - [[civilian-preparedness]]
leads_to:
  - [[iff-architecture]]
  - [[operational-security]]
