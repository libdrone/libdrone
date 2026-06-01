---
id: platform-selection
title: "Platform selection"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
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

Platform selection for security-sensitive deployments involves matching the
operational mission against the IFF capability, autonomy level, emissions
profile, and flight system of each libdrone variant. Bandit (ArduPilot) is
the correct choice for autonomous missions requiring full ATAK integration
and mission state visibility. Pro (Betaflight) is correct for manually-piloted
payload operations where GPS-assisted navigation suffices and the MSP→CoT
bridge covers the IFF requirement. Ghost is the correct choice where reduced
emissions and lower visual signature are priority. Core is the training and
redundancy platform — not an operational choice for security-sensitive missions.

---

## Concept

### The selection axes

Four axes determine the appropriate variant for a given security deployment:

**Autonomy requirement**: Does the mission require autonomous waypoint
navigation, return-to-home without pilot intervention, or integration with
GCS mission planning? ArduPilot variants (Bandit, Ghost) provide this.
Betaflight variants (Pro, Core) provide GPS-assisted navigation and GPS
Rescue, but not full autonomous mission execution.

**IFF requirement**: Is full ATAK integration with mission state visibility
required? Bandit provides this natively via MAVLink. Does MSP→CoT bridge
with position-only tracking suffice? Pro covers this. Is emissions control
the priority over network IFF? Ghost with EMCON reduced or minimum.

**Emissions profile**: Is the operation in a context where RF emissions from
FPV video are a liability? Ghost is configured for reduced emissions. Does
the mission require the lowest possible RF signature? Ghost with FPV disabled
and relay-based operation.

**Payload requirement**: Does the mission require a sensor payload on the
GX12 interface? All variants except Core support the dual GX12 standard.
Does the mission require LCM-1 intelligence layer (threshold alerting, CoT
output)? Pro, Bandit, Ghost — all carry ESP32-S3 as mandatory.

### When ArduPilot (Bandit) is the correct choice

- Autonomous area survey without continuous pilot input
- Integration with a GCS (QGroundControl, Mission Planner) for mission planning
- Full ATAK Blue Force tracking with mission state (waypoints, auto modes visible)
- Geofencing enforcement via MAVLink parameters
- Operations where the pilot cannot maintain VLOS and relies on autonomous
  return-to-home as primary safety measure

### When Betaflight Pro is the correct choice

- Manually-piloted payload missions (air quality mapping, surveillance support)
- ATAK presence via MSP→CoT bridge is sufficient (position and status, no mission state)
- Operations in EASA A2 urban environment where low-speed mode and GPS Rescue suffice
- Operator wants higher-fidelity manual control feel than ArduPilot provides
- Primary use case is community preparedness rather than structured autonomous mission

### When Ghost is the correct choice

- Operations where visual and RF signature is a primary concern
- Night operations with IR strobe as primary IFF (video off or minimal)
- Security-sensitive environments where Remote ID broadcast is evaluated
  against operational risk
- Missions where the operator needs EMCON reduced or minimum configuration
  as the default, not an exception

---

## Reference

### Platform selection matrix

| Requirement | Pro | Bandit | Ghost | Core |
|---|---|---|---|---|
| GPS-assisted manual flight | ✓ | ✓ | ✓ | ✓ |
| Autonomous waypoint mission | ✗ | ✓ | ✓ | ✗ |
| GCS mission planning | ✗ | ✓ | ✓ | ✗ |
| ATAK CoT (position) | ✓ (MSP bridge) | ✓ (MAVLink native) | ✓ (MAVLink) | ✗ |
| ATAK CoT (mission state) | ✗ | ✓ | ✓ | ✗ |
| Dual GX12 payload interface | ✓ | ✓ | ✓ | ✗ |
| LCM-1 intelligence layer | ✓ | ✓ | ✓ | ✗ |
| Reduced emissions profile | Possible | Possible | **Default** | N/A |
| EASA A2 compliant AUW | ✓ | ✓ | ✓ | ✓ (< 250g) |
| Field arm replacement | ✓ | ✓ | ✓ | ✓ |
| Training platform | Capable | Capable | **No** | ✓ |

### Deployment recommendation by scenario

| Scenario | Recommended | Rationale |
|---|---|---|
| Urban air quality mapping (civilian) | Pro | Manual pilot, GPS Rescue, MSP CoT adequate |
| Municipal emergency preparedness | Pro + Bandit | Pro for flexibility, Bandit for autonomous survey |
| Night perimeter security watch | Ghost | IR strobe + reduced VTX + EMCON minimum |
| Community resilience (flood, disaster) | Pro | Fast deployment, field-repairable, A2 compliant |
| ATAK-integrated allied coordination | Bandit | MAVLink native, mission state visible to GCS |
| Pilot and builder training | Core | Purpose-built, crash-tolerant, low consequence |
| Research and payload development | Pro | Best sensor payload integration, active community |

---

## Procedure

### Pre-procurement platform decision sequence

1. Identify the primary operational scenario from the scenario table above.
2. Identify the IFF requirement: position-only, full mission state, or EMCON priority.
3. Identify the autonomy requirement: manual + GPS rescue, or autonomous waypoints.
4. Identify the payload requirement: no payload, GX12 sensor, or LCM-1 intelligence.
5. Select the variant from the matrix.
6. If the scenario requires capabilities spanning two variants (e.g. autonomous
   survey *and* manual payload operations): procure both. The Bandit and Pro
   share key components (FC family, ELRS radio, goggles) — combined procurement
   is efficient.

---

## Rationale

### Why Ghost is not recommended for training

Ghost's reduced-emissions configuration, EMCON discipline requirements, and
role-specific operational procedures require a foundation of confident platform
operation. An operator who is still developing situational awareness and flight
skills should not simultaneously be managing emissions control. Ghost deployments
require pilots who are proficient on Pro or Bandit first. The training path is
always: Core → Pro or Bandit → Ghost.

### Why Core is not listed for security missions

Core is designed for pilot training and budget builds under 250g. Its omission
of the dual GX12 payload interface, the LCM-1 bay, and ESP32-S3 companion board
means it cannot participate in IFF layers above L1. It is not a capability gap
in Core — it is a deliberate design scoping decision. Core's use in security
contexts is limited to providing a spare flyable platform for pilot currency
maintenance. It is not deployed on operational missions.

---

## Connections

requires:
  - [[threat-assessment]]
  - [[iff-architecture]]
  - [[operational-security]]
related:
  - [[platform-overview]]
  - [[emissions-control]]
  - [[civilian-preparedness]]
  - [[lcm1-spec]]
leads_to:
  - [[platform-overview]]
