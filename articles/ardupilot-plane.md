---
id: ardupilot-plane
title: "ArduPilot Plane"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: generic
topic:
  - firmware-autopilot
personas:
  - 1.builder
  - 2.operator
  - 8.architect
platform:
  - wing
lang: en
licence: CC BY-SA 4.0
---

## Summary

ArduPilot Plane is the fixed-wing variant of the ArduPilot autopilot firmware,
running on the same Matek H7A3-WING flight controller used by libdrone Wing.
Where ArduPilot Copter manages multirotor attitude and position, ArduPilot
Plane manages forward flight speed (airspeed), altitude, and navigation for
fixed-wing and flying-wing aircraft. Its core flight management system is TECS
— Total Energy Control System — which coordinates throttle and pitch to
maintain the target airspeed and altitude simultaneously. Configuration for a
flying wing (elevon mixing) differs from conventional aircraft (separate
elevator and ailerons) and must be set correctly before any flight.

---

## Concept

### TECS — Total Energy Control System

A multirotor controls altitude directly: increase throttle to climb, decrease
to descend. A fixed-wing cannot do this cleanly — increasing throttle
accelerates the aircraft as well as climbing, and pitching up to climb bleeds
speed. The two control inputs (throttle and pitch) couple.

TECS decouples them by managing total energy: the sum of potential energy
(altitude) and kinetic energy (speed). When the aircraft needs to climb
(increase potential energy), TECS increases throttle to add total energy and
uses pitch to allocate it between altitude and speed. When the aircraft needs
to descend, TECS reduces throttle and pitches to exchange altitude for speed
while maintaining the target airspeed.

The result is that the operator specifies a target airspeed and altitude; TECS
handles the throttle and pitch outputs to achieve both. This is what makes
autonomous survey grid flights stable: altitude hold in fixed-wing is
indistinguishable from altitude hold in a multirotor from the operator's
perspective, even though the control law is completely different.

### Flying wing configuration

A flying wing (Skywalker X8, Mini Talon V2) has no separate elevator or
ailerons — control surfaces called elevons combine both functions. ArduPilot
Plane must be configured for the correct airframe type:

    FRAME_CLASS,2    ; Flying wing

With this setting, ArduPilot outputs elevon mixing automatically: the
elevator channel drives both surfaces in the same direction (pitch), and
the aileron channel drives them in opposite directions (roll). No manual
mixing is required in the transmitter.

### Auto-takeoff and auto-land

ArduPilot Plane supports auto-takeoff from a hand launch. The aircraft is
armed with throttle at idle, hand-launched, and immediately switches to FBWA
(Fly-By-Wire-A) or TAKEOFF mode — climbing at the configured pitch angle
until the target altitude is reached, then transitioning to AUTO mode for
the mission.

Auto-land uses a landing waypoint in the mission: the aircraft flies a
descending approach to the landing point, then flares (pitch up, throttle
cut) at the configured flare altitude. For Wing's field deployments, a belly
landing on flat ground or hand-catch is the standard recovery method.

---

## Reference

| Parameter | Value | Notes |
|---|---|---|
| Firmware | ArduPilot Plane ≥4.4 | |
| FC target | `MatekH7A3-WING` | Different target from MatekH7A3 (Copter) |
| FRAME_CLASS | 2 | Flying wing |
| TECS_AIRSPEED_CRUISE | 12 m/s | Adjust per airframe stall speed |
| TECS_PITCH_MAX | 15° | Limit aggressive pitch for survey stability |
| TECS_PITCH_MIN | −15° | |
| ARSPD_FBW_MIN | 9 m/s | Minimum safe airspeed (above stall) |
| ARSPD_FBW_MAX | 22 m/s | Maximum safe airspeed |
| TKOFF_ALT | 30 m | Auto-takeoff target altitude |
| RTL_ALTITUDE | 50 m | RTH altitude above launch point |

**Key flight modes (Wing):**
- MANUAL: direct stick-to-surface passthrough, no stabilisation
- FBWA (Fly-By-Wire-A): attitude stabilised, pilot commands bank angle and pitch
- LOITER: GPS circle around a point at constant altitude
- AUTO: execute waypoint mission
- RTL: return to launch GPS coordinate and land

---

## Procedure

### Initial fixed-wing configuration (flying wing)

1. Flash ArduPilot Plane `MatekH7A3-WING` target via STM32CubeProgrammer.
2. Connect QGroundControl. Set FRAME_CLASS=2 (flying wing).
3. Calibrate accelerometer (6-position, same as Copter).
4. Calibrate compass (same as Copter).
5. Calibrate RC. Verify elevon surfaces move correctly: right stick right →
   right surface down, left surface up. If reversed, adjust RCMAP or reverse
   the relevant output channel.
6. Set TECS parameters for the chosen airframe (start with defaults;
   adjust after maiden flight based on cruise behaviour).
7. Configure auto-takeoff: set TKOFF_ALT=30, verify TAKEOFF mode in
   flight mode menu.
8. Verify RTL altitude is above terrain and obstacles in the survey area.

---

## Rationale

ArduPilot Plane was selected over iNAV for Wing for the same reasons ArduPilot
Copter was selected for Bandit and Ghost: the largest community-validated
parameter set for the H7A3 target, and the most complete QGroundControl
integration. iNAV is a capable fixed-wing firmware but its GCS integration
is less mature and its TECS implementation is less thoroughly documented for
survey applications. Maintaining a single autopilot ecosystem (ArduPilot)
across Bandit, Ghost, and Wing reduces the operator's cognitive load:
QGroundControl, mission planning workflow, and failsafe logic are the same
across all three platforms.

---

## Connections

```yaml
requires:
  - [[fixed-wing-fundamentals]]
  - [[ardupilot-copter]]
  - [[gnss-gps]]
related:
  - [[wing-variant]]
  - [[qgroundcontrol]]
  - [[elrs-mavlink-mode]]
  - [[closed-loop-control]]
leads_to:
  - [[qgroundcontrol]]
  - [[wildlife-survey-operations]]
```
