---
id: inertia-and-stopping
title: "Inertia and stopping distance"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - physics-flight-mechanics
personas:
  - 5.student
  - 2.operator
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

A moving drone does not stop when the stick is released. It continues moving
because of inertia — Newton's first law. To stop, the flight controller must
pitch the drone backward, redirecting thrust against the direction of motion.
This takes distance and time, and first-time pilots dramatically underestimate
both. At 5 m/s, stopping takes approximately 2–3 metres at comfortable
deceleration. GPS position hold manages inertia automatically but does not
eliminate it — the drone still overshoots and settles. Flying smoothly means
anticipating where the drone will be, not where it is.

---

## Concept

### Newton's first law in practice

An object in motion stays in motion unless acted upon by an external force.
For a drone moving forward at 5 m/s, the kinetic energy is:

    KE = ½ × m × v² = ½ × 0.86 × 5² = 10.75 J

That energy must be removed by doing work against something. Aerodynamic drag
does some work — but at 5 m/s, drag on a drone-sized object is small. The
primary braking force is the thrust vector reversed: pitch the nose up to
redirect thrust backward.

### Stopping distance calculation

To decelerate from 5 m/s at 0.5g (comfortable, ~5 m/s²):

    stopping_distance = v² / (2 × a) = 25 / (2 × 5) = 2.5 m
    stopping_time = v / a = 5 / 5 = 1 s

At 1g deceleration (aggressive, ~10 m/s²):

    stopping_distance = 25 / (2 × 10) = 1.25 m
    stopping_time = 0.5 s

At 10 m/s (fast forward flight):
    stopping_distance (0.5g) = 100 / 10 = 10 m

These distances apply in still air. In a headwind, deceleration is faster
(drag assists). In a tailwind, it is slower (drag and thrust both needed).

### The overshoot problem

When the flight controller pitches the drone back to decelerate, the drone
tilts. The pendulum effect then creates a restoring torque trying to return
the drone to level. The flight controller is commanding nose-up while the
pendulum is pulling toward level. If the PID D-term is insufficient, the drone
overshoots the commanded position, corrects, overshoots again — oscillation at
the pendulum frequency.

In GPS position hold, the flight controller manages this automatically: it
detects the drone moving past the commanded position and applies braking pitch
in advance. But the drone still overshoots slightly, decelerates, and settles.
The physics cannot be eliminated by software — it can only be managed.

### Smooth flying technique

A smooth pilot anticipates where the drone will be, not where it is. Key habits:

- **Apply corrections early.** A correction applied 1 second before the drone
  reaches a position requires less extreme pitch and produces less overshoot
  than a correction applied at the position.
- **Reduce speed before obstacles.** The stopping distance at 5 m/s is 2.5 m.
  At 10 m/s it is 10 m. Do not approach obstacles at speed unless there is
  10+ m of stopping room.
- **Use position-hold mode to stop.** In GPS-assisted modes, releasing the
  stick commands the drone to hold its current position. The flight controller
  handles the braking. In acro mode, there is no automatic braking.
- **Read the OSD speed readout.** Knowing the actual ground speed numerically
  calibrates the pilot's sense of stopping distance.

---

## Reference

### Stopping distances at common speeds

| Speed | Deceleration | Distance | Time |
|---|---|---|---|
| 3 m/s | 0.5g (5 m/s²) | 0.9 m | 0.6 s |
| 5 m/s | 0.5g | 2.5 m | 1.0 s |
| 5 m/s | 1.0g | 1.25 m | 0.5 s |
| 8 m/s | 0.5g | 6.4 m | 1.6 s |
| 10 m/s | 0.5g | 10 m | 2.0 s |

Libdrone V2.4.6 AUW: ~860–900 g. Aerodynamic drag at these speeds is 1–5 N
(small relative to thrust). The stopping forces are dominated by the thrust
vector reversal, not drag.

### Inertia in wind

In a 5 m/s headwind, the drone moving forward at 5 m/s ground speed has
0 m/s airspeed. Drag is zero. Stopping from ground motion relies entirely on
thrust reversal — wind provides no assistance. In a tailwind, the drone moving
at 5 m/s ground speed has 10 m/s airspeed. Drag now helps braking. In cross-
winds, stopping in one direction while drifting in another requires the pilot
to manage two axes simultaneously.

---

## Procedure

<!-- not applicable — flying technique is in piloting-operations -->

---

## Rationale

### Why this article focuses on physics, not technique

The operational flying technique (how to approach a landing zone, how to stop
for a survey waypoint) belongs in [[piloting-operations]]. This article exists
to give the numbers behind those techniques — so that a pilot following the
technique knows why it specifies the distances it does, and can adapt
intelligently when conditions change. A pilot who memorises "stop 3 metres
before the obstacle" is fragile; a pilot who knows stopping distance scales
with v² can adapt to any speed.

---

## Connections

requires:
  - [[lift-and-thrust]]
  - [[hover-and-forward-flight]]
related:
  - [[pendulum-stability]]
  - [[vortex-ring-state]]
  - [[moment-of-inertia]]
leads_to:
  - [[piloting-operations]]


[piloting-operations]: piloting-operations.md "Piloting and operations"
[lift-and-thrust]: lift-and-thrust.md "Lift and thrust"
[hover-and-forward-flight]: hover-and-forward-flight.md "Hover and forward flight"
[pendulum-stability]: pendulum-stability.md "Pendulum stability"
[vortex-ring-state]: vortex-ring-state.md "Vortex ring state"
[moment-of-inertia]: moment-of-inertia.md "Moment of inertia"
