---
id: sk-bandit-awareness-curriculum
title: "Bandit Awareness Curriculum"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 9.defense
  - 2.operator
  - 4.workshop
platform:
  - bandit
lang: en
licence: CC BY-SA 4.0
---

## Summary

After completing this curriculum, the participant understands the civilian
drone threat landscape at a level that informs operational decisions, can
operate libdrone Bandit with correct IFF discipline, and can contribute to
community situational awareness in security-relevant environments. This
curriculum is not about preparing for war. It is about informed awareness —
the same logic that makes a good driver understand vehicle dynamics, or a
good sailor understand weather patterns.

---

## Concept

### Part A — Theory: Understanding the threat landscape

The starting point is not technical — it is attitudinal. The correct mental
model: awareness is protective. Understanding how civilian drones work, what
they can and cannot do, and how to identify friendly platforms does not
create a threat — it reduces the confusion that allows threats to operate
in the dark.

Begin with the threat context: → [[threat-assessment]] explains the three
categories relevant to civilian operations (criminal surveillance, hybrid
warfare, fratricide) and what libdrone can and cannot address. The critical
takeaway: libdrone addresses the fratricide and friendly identification
problem; it is not a counter-drone system.

The IFF architecture answers the question "how do observers know this drone
is ours?" rather than "how do we identify hostile drones." → [[iff-layers]]
maps the five layers from IR strobe (simplest, most resilient) to future
allied standards (reserved but not yet available). → [[iff-architecture]]
explains the specific libdrone implementation and the role of the ESP32-S3
as the IFF intelligence bridge.

The lesson from Ukraine (2022–present): the IR strobe was the single most
effective anti-fratricide measure precisely because it requires no
infrastructure and continues working when everything else fails. Every
Bandit deployment should include a fitted IR strobe. This is not a
recommendation — it is a baseline requirement.

### Part B — Practical exercises

The exercises use libdrone Bandit as a training tool. The Bandit's ArduPilot
firmware and MAVLink telemetry make it the correct platform for ATAK
integration exercises — it participates in the same digital network as the
platforms it is meant to deconflict with.

**Exercise 1 — Visual identification**

Fly the Bandit at varying distances (10m, 30m, 50m, 100m) and altitudes
(5m, 15m, 30m). From the ground, practise identifying: Is the drone moving
toward me or away? Where is the nose pointing? What is the approximate altitude?

This is a prerequisite for VLOS operations in complex environments. A pilot
who cannot reliably orient a drone at 50m distance is not VLOS-capable.

**Exercise 2 — Night operations with IR strobe**

Fit the IR strobe to the Bandit. Fly at night (civil twilight or darker).
With NVG or a Night Vision-capable camera: observe the IR strobe. Confirm
it is clearly visible and clearly associated with the drone's position.

Then: fly a second pass without the strobe active. Note the difference in
visibility. This is the operational demonstration of why IR strobe discipline
matters — the difference between visible and invisible at night is a switch.

**Exercise 3 — ATAK CoT integration**

Configure the ESP32-S3 MAVLink→CoT bridge on the Bandit (→ [[iff-architecture]]
for the configuration procedure). Fly the Bandit at 30m altitude, 50m
distance. On a TAK-enabled tablet at the launch point: observe the blue
rotary-wing icon tracking the drone's GPS position in near-real time.

Discuss: Who else on this network can see this icon? What does it reveal about
operational intent? When should CoT output be active and when should it be
suspended? → [[operational-security]] provides the framework for this discussion.

**Exercise 4 — Emissions awareness**

Fly the Bandit with a 2.4 GHz spectrum analyser running on a laptop at the
launch point. Observe: the ELRS control link signature is visible at several
hundred metres. The HDZero 5.8 GHz transmission is also visible if your
analyser covers that range.

This is the visceral demonstration of the OPSEC principle: every RF emission
is a detectable signal. → [[emissions-control]] covers what can and cannot be
reduced. The ELRS link cannot be eliminated — the drone requires control.
The VTX power can be reduced or the VTX disabled entirely.

**Exercise 5 — Autonomous area survey**

Fly a programmed survey grid using QGroundControl mission planning. The
Bandit executes the mission without continuous pilot input. The pilot monitors
via → [[flight-modes]] — angle mode, GPS hold, and mission modes are all
relevant.

This exercise demonstrates the autonomous capability that distinguishes
Bandit from Pro and illustrates why → [[betaflight-gps-rescue]] (GPS Rescue
on Pro) is a safety feature, not a navigation capability.

### EMCON discipline

→ [[operational-security]] is the curriculum module on emissions control.
Every participant should leave with a clear answer to: In what operational
contexts would I reduce my RF emissions, and what capability do I trade?

The answer is context-dependent and requires judgment. The curriculum does
not provide a single answer — it provides the framework and the exercises
to develop that judgment.

---

## Reference

### Curriculum sessions

| Session | Mode | Key articles |
|---|---|---|
| A1 — Threat landscape | Theory | [[threat-assessment]], [[iff-layers]] |
| A2 — IFF architecture | Theory | [[iff-architecture]], [[remote-id-compliance]] |
| A3 — Emissions awareness | Theory | [[emissions-control]], [[operational-security]] |
| B1 — Visual identification | Practical | [[flight-modes]], [[piloting-progression]] |
| B2 — Night ops + IR strobe | Practical | [[iff-layers]] |
| B3 — ATAK CoT integration | Practical | [[iff-architecture]], [[lcm1-spec]] |
| B4 — Emissions demonstration | Practical | [[emissions-control]], [[elrs-protocol]] |
| B5 — Autonomous survey | Practical | [[ardupilot-flight-modes]], [[qgroundcontrol]] |

---

## Procedure

### Participant prerequisites

Part B exercises require: A2 CoC (or direct supervision by an A2-qualified
instructor), completion of Part A theory, and prior flight experience on
Pro or Core before flying Bandit exercises.

---

## Rationale

The Bandit Awareness Curriculum (V2.4.6) was a standalone document combining
theory and practical exercises. The 3.0.0 version delegates the technical
content to atoms and focuses the skeleton on the pedagogical sequence —
what order to present the material, why each exercise exists, and what
the participant should leave knowing.

---

## Connections

requires: []
related:
  - [[sk-security-operations-guide]]
  - [[sk-platform-brief]]
  - [[ardupilot-flight-modes]]
  - [[qgroundcontrol]]
leads_to:
  - [[sk-security-operations-guide]]
