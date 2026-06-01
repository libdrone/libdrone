---
id: fixed-wing-fundamentals
title: "Fixed-wing fundamentals"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: generic
topic:
  - physics-flight-mechanics
personas:
  - 5.student
  - 2.operator
  - 8.architect
platform:
  - wing
lang: en
licence: CC BY-SA 4.0
---

## Summary

Fixed-wing aircraft generate lift from the aerodynamic shape of a wing moving
through air, rather than from continuous powered thrust vectored downward as
in a multirotor. This fundamental difference makes fixed-wing aircraft far more
efficient at covering area — a fixed-wing travelling at cruise speed generates
lift nearly for free, while a multirotor must continuously expend energy to
oppose gravity even when stationary. For survey applications where area coverage
per battery matters more than hover capability or vertical take-off, fixed-wing
is the architecturally correct choice.

---

## Concept

### Lift from motion vs lift from thrust

A multirotor generates lift by accelerating air downward through its rotors.
Every joule of hover energy is spent entirely on overcoming gravity. Travelling
forward is an additional energy cost on top of hover.

A fixed-wing generates lift from pressure difference: the wing's camber causes
air to travel faster over the upper surface than the lower, reducing pressure
above the wing relative to below. The forward motion that generates this
pressure difference is maintained by a single propeller or motor at a fraction
of the power required to hover at the same weight. The glide ratio —
the distance travelled horizontally per unit of altitude lost with motor off
— is typically 8:1 to 15:1 for foam flying wings. A multirotor's glide ratio
without power is approximately 1:1 (it drops).

### Efficiency in survey terms

For a survey platform at 50 m AGL covering a 30-hectare field:

A multirotor covers ground by flying horizontal transects — every metre of
forward travel is powered by hover thrust plus forward thrust. Power consumption
is approximately proportional to flight time regardless of speed.

A fixed-wing covers the same ground at cruise speed (12–15 m/s vs a
multirotor's 5–8 m/s), using only cruise thrust to maintain altitude. Typical
flying wing power consumption at cruise is 40–80 W. A comparable multirotor
in forward flight consumes 150–300 W. The area coverage rate per watt is
3–5× better for fixed-wing at survey speeds.

This efficiency directly translates to endurance: the same 4S LiPo that
provides 12 minutes of multirotor hover provides 45–60 minutes of fixed-wing
cruise.

### Flight characteristics vs multirotor

Fixed-wing aircraft cannot hover. They must maintain a minimum airspeed above
the stall speed — typically 8–12 m/s for flying wings — or lose lift and
descend. Launching and landing require either a runway, hand launch, bungee,
or VTOL capability. ArduPilot handles auto-takeoff (climb to altitude after
hand launch) and auto-land (RTH → landing pattern → touchdown) in ArduPlane.

Control axes are different: roll is controlled by ailerons or elevons (not
motor differential), pitch by elevator, yaw by rudder or differential thrust.
A flying wing like the Skywalker X8 uses elevons — combined elevator/aileron
surfaces — and has no separate rudder. ArduPilot configures mixing for the
correct geometry.

Wind affects fixed-wing flight differently from multirotor. A multirotor
maintains position against wind by tilting into it. A fixed-wing must
maintain airspeed — a headwind reduces groundspeed but does not stall the
aircraft; a tailwind increases groundspeed and decreases control authority
at low throttle. ArduPilot's TECS (Total Energy Control System) manages the
throttle/pitch relationship to maintain the target airspeed regardless of
wind. See → [[ardupilot-plane]] for TECS configuration.

---

## Reference

| Parameter | Fixed-wing (flying wing) | Multirotor |
|---|---|---|
| Lift source | Wing aerodynamics | Rotor thrust |
| Minimum speed | Stall speed: ~8–12 m/s | 0 m/s (hover) |
| Cruise efficiency | ~40–80 W at 12 m/s | ~150–300 W at 8 m/s |
| Survey endurance | 45–75 min | 10–15 min |
| Area coverage rate | High | Low |
| Hover capability | None | Yes |
| Launch | Hand/bungee/runway | Vertical |
| Landing | Runway/belly land/hand-catch | Vertical |
| Wind sensitivity | Groundspeed varies | Position drift |

---

## Procedure

<!-- not applicable — flight procedures are platform and firmware specific;
see [[ardupilot-plane]] for ArduPilot Plane setup and [[wing-variant]] for
Wing-specific operational procedure -->

---

## Rationale

Understanding the fixed-wing efficiency advantage is a prerequisite for
evaluating Wing as a platform choice. Institutions or operators accustomed
to multirotor operations often underestimate the endurance and coverage
rate difference — it is not incremental (20% better) but categorical
(3–5× better for area coverage). Equally, the absence of hover capability
is not a limitation to minimise but a trade to understand: if the mission
requires hover (inspection, precise delivery), fixed-wing is wrong; if the
mission requires area coverage (survey, search, monitoring), fixed-wing is
correct. The libdrone platform family is designed so the correct variant is
available for both mission types.

---

## Connections

requires:
  - [[lift-and-thrust]]
  - [[hover-and-forward-flight]]
related:
  - [[wing-variant]]
  - [[ardupilot-plane]]
  - [[six-degrees-of-freedom]]
  - [[propellers]]
leads_to:
  - [[wing-variant]]
  - [[ardupilot-plane]]
