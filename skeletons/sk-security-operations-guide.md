---
id: sk-security-operations-guide
title: "Security Operations Guide"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 9.defense
  - 6.evaluator
platform:
  - pro
  - bandit
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

After reading this guide, the defence analyst or municipal security procurement
officer can assess libdrone's IFF and operational security architecture, select
the appropriate platform variant for their deployment context, and understand
what training and discipline is required to operate the platform in security-
sensitive environments. Learning objective: produce a platform selection
recommendation with a supporting rationale.

---

## Concept

### The civilian operator's IFF position

Civilian operators in security-relevant environments are not equipped with
classified military IFF. They do not have access to NATO Mode 4/5 transponders.
They are, nonetheless, operating in environments where being identified as
friendly — by allied observers, by security forces, by community groups
managing a shared operating picture — is a meaningful safety requirement.

→ [[threat-assessment]] frames the problem precisely: the goal is not to
identify hostile drones. The goal is to remove libdrone platforms from the
ambiguous population — to make them positively identifiable to allied observers
so that the cognitive load of "is that ours?" is reduced to zero for any
observer with the right equipment.

→ [[iff-architecture]] maps the five-layer implementation from IR strobe (L1)
through ATAK CoT integration (L3/L4) to the reserved future allied IFF
interface (L6). Every layer adds coverage in the scenario where the layer
above it fails.

### Platform selection for security context

→ [[platform-selection]] is the decision matrix. The short version:

For **ATAK-integrated operations with mission state visibility**: Bandit
(ArduPilot, MAVLink native, full ATAK integration). The Bandit's ArduPilot
firmware streams HEARTBEAT, GPS, and ATTITUDE via MAVLink to the ESP32-S3
bridge, which relays CoT to the tactical network.

For **manually-piloted payload operations with position-only ATAK presence**:
Pro (Betaflight, MSP→CoT bridge, position and battery state visible in ATAK).
Not mission state, but adequate for situational awareness.

For **reduced-emissions operations where visual and RF signature is a priority**:
Ghost (standard EMCON reduced configuration, VTX at 25 mW or off, ELRS at
minimum power).

### Operating the IFF stack

→ [[iff-layers]] is the operational quick reference: what each layer provides,
what equipment observers need to benefit from it, and what the operator must
do to maintain it. The IR strobe summary: fits in a vest pocket, costs €10,
works when everything else fails, requires no configuration.

The ATAK CoT configuration is in → [[iff-architecture]]. The ESP32-S3 companion board architecture — three concurrent firmware tasks (MAVLink→CoT bridge, Remote ID broadcast, IFF GPIO interface) and EMCON kill switch — is in → [[esp32-s3-companion]]. The firmware
update, TAK server configuration, and verification procedure are all covered.
Once configured, the blue rotary-wing icon appears on ATAK automatically
when the drone has a GPS fix.

### Emissions control decisions

→ [[operational-security]] is the EMCON reference. Before each deployment in
a security-sensitive context, the operator should answer four questions:

1. What am I broadcasting and to whom?
2. Does Remote ID broadcasting create an operator position disclosure risk in
   this context?
3. Which EMCON level (standard / reduced / minimum) matches this environment?
4. If EMCON minimum, what IFF capability remains? (Answer: IR strobe only.)

→ [[emissions-control]] covers the platform-level controls: VTX power reduction
or disable, ELRS dynamic power minimum, ESP32-S3 WiFi hotspot disable, CoT
output to authenticated TAK only.

### Training requirements

This guide is not a training programme — it is an operational reference. The
training programme is → [[sk-bandit-awareness-curriculum]]: Part A covers the
threat landscape and IFF theory, Part B covers the practical exercises
(visual identification, night ops with IR strobe, ATAK integration, emissions
awareness demonstration).

A security operator who has not completed the awareness curriculum should
not be operating with IFF-configured hardware in a security-sensitive context.
The hardware capability is meaningless without the operational discipline to
use it correctly — particularly the EMCON discipline of knowing when to go
silent and what that costs.

---

## Reference

### Decision summary by scenario

| Scenario | Platform | IFF layers active | EMCON |
|---|---|---|---|
| Community preparedness, civilian | Pro | L1 + L2 + L4 (if ATAK available) | Standard |
| Municipal emergency response | Pro or Bandit | L1 + L2 + L3/L4 | Standard |
| Night security watch | Ghost | L1 (IR strobe) + optional L3/L4 | Reduced |
| ATAK-integrated coordination | Bandit | L1 + L2 + L3 | Standard or Reduced |
| High-risk contested environment | Ghost | L1 only (IR strobe) | Minimum |

---

## Procedure

### Pre-deployment IFF checklist

1. IR strobe fitted, battery charged, operating pattern confirmed
2. Remote ID module active and broadcasting correct e-ID (or operational
   decision to suspend — documented)
3. If CoT active: TAK server accessible, callsign configured, blue icon
   visible on test tablet before departure
4. EMCON level determined and documented in mission plan
5. All team members briefed on the drone's IR strobe pattern and the EMCON
   level for this operation

---

## Rationale

The defence analyst persona traversal (threat-assessment → iff-architecture →
operational-security → platform-selection) exists because the technical atoms
in these domains require a connecting narrative for a reader who is evaluating
the platform from a security procurement perspective rather than a technical
building perspective. This skeleton provides that narrative and the decision
sequence — the atoms provide the technical depth.

---

## Connections

requires: []
related:
  - [[sk-platform-brief]]
  - [[sk-bandit-awareness-curriculum]]
  - [[esp32-s3-companion]]
  - [[acoustic-signature-design]]
  - [[sk-ghost-operations-guide]]
leads_to:
  - [[sk-platform-brief]]
  - [[sk-bandit-awareness-curriculum]]
