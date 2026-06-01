---
id: hover-and-forward-flight
title: "Hover and forward flight"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - physics-flight-mechanics
personas:
  - 5.student
  - 4.workshop
  - 2.operator
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Hovering requires total thrust to equal weight. Forward flight requires the
drone to pitch forward, redirecting part of the thrust vector horizontally —
which simultaneously reduces the vertical component and requires more throttle
to maintain altitude. There is a counterintuitive consequence: a heavier drone
requires less pitch angle than a lighter drone to achieve the same horizontal
speed, because its larger thrust magnitude provides more horizontal force per
degree of tilt. Maximum speed is limited by the geometry of how much vertical
thrust remains after tilting far enough to produce the required horizontal
force.

---

## Concept

### Hover: equilibrium of forces

For level hover, the sum of all forces acting on the drone must be zero.
Vertically: total motor thrust upward = weight downward. Horizontally: in
still air, no net horizontal force, so motors need no horizontal component.
Each motor runs at equal speed, producing equal thrust, and the frame is
perfectly level.

Hover throttle — the percentage of total throttle required to maintain
altitude — directly reveals the thrust-to-weight ratio:

    hover_throttle ≈ 1 / TWR

For libdrone at TWR ≈ 12.4:1 bare:
    `hover_throttle ≈ 1 / 12.4 ≈ 8%` of maximum thrust
→ This equals approximately 28% of throttle input (since throttle is not
linearly mapped to thrust at low values in Betaflight's thrust linearisation).

High TWR means more throttle headroom above hover — more authority for rapid
altitude changes and wind gusts.

### Forward flight: the tilted thrust vector

To accelerate forward, the flight controller pitches the drone nose-down.
The total thrust vector, previously pointing straight up, now tilts forward.
The thrust has two components:
- Vertical component: `T × cos(θ)` — supports weight
- Horizontal component: `T × sin(θ)` — accelerates the drone forward

As pitch angle θ increases, the vertical component decreases. To maintain
altitude, total thrust T must increase to compensate — the motors must work
harder just to stay at the same height while also producing forward force.

At constant forward speed, horizontal thrust equals aerodynamic drag:

    T × sin(θ) = Drag

### Maximum forward speed

There is a maximum pitch angle beyond which the vertical component of thrust
can no longer support the drone's weight even at full throttle:

    T_max × cos(θ_max) = Weight
    θ_max = arccos(Weight / T_max)

For libdrone bare (807 g, T_max ≈ 10,000 g):
    `θ_max = arccos(807/10000) ≈ 85°` — nearly horizontal, not the limiting factor.

The practical speed limit is reached earlier: the aerodynamic drag grows
with the square of speed, requiring greater pitch angle to overcome it. At
some speed, the pitch angle needed to overcome drag also requires throttle
above 100%. That is the actual maximum speed.

### The pitch paradox

Counterintuitive conclusion: **a heavier drone requires less pitch angle than
a lighter drone to achieve the same forward speed.**

The reason: a heavier drone must generate more total thrust T to support its
weight in hover. In forward flight at angle θ, its horizontal force component
is `T × sin(θ)` — larger for the same angle θ because T is larger. To generate
enough horizontal force to overcome drag at a given speed, the heavier drone
needs a shallower angle.

The lighter drone, with its smaller T, must pitch more steeply to generate
the same horizontal force component. At extreme pitch angles, the lighter
drone is actually less efficient in forward flight despite its lower AUW.

Note: this does not mean heavier drones are faster overall. Their higher drag
at the same speed ultimately limits them. But the relationship between weight
and pitch angle is not the simple inverse that intuition suggests.

---

## Reference

### Force balance equations

**Hover:**
    T = mg

**Forward flight at constant speed and altitude:**
    T_vertical = T × cos(θ) = mg      (altitude maintained)
    T_horizontal = T × sin(θ) = Drag  (constant speed)

**Required total thrust in forward flight:**
    T = mg / cos(θ)

For θ = 30°: `T = mg / cos(30°) = mg / 0.866 = 1.155 × mg`
→ 15.5% more thrust required than hover to maintain altitude at 30° pitch.

### libdrone V2.4.6 hover figures

| Config | AUW | Hover throttle (approx) |
|---|---|---|
| No payload | ~807 g | ~28% |
| +80g payload | ~887 g | ~30% |

Hover throttle changes with battery voltage — higher at the end of a flight
as voltage drops. Monitor voltage in OSD.

---

## Procedure

<!-- not applicable -->

---

## Rationale

### Why hover throttle is a useful build quality indicator

After maiden flight, hover throttle should match the calculated value from
the TWR estimate. If hover throttle is significantly higher than expected,
either the AUW is higher than estimated (check with scale) or the motors
are not producing their rated thrust (check for mechanical damage, incorrect
motor direction, wrong prop). If lower, the AUW estimate was pessimistic.
Hover throttle is the first post-maiden sanity check.

---

## Connections

requires:
  - [[lift-and-thrust]]
  - [[six-degrees-of-freedom]]
related:
  - [[pendulum-stability]]
  - [[angular-momentum-multirotors]]
  - [[induced-velocity]]
leads_to:
  - [[induced-velocity]]
  - [[vortex-ring-state]]
  - [[inertia-and-stopping]]


[lift-and-thrust]: lift-and-thrust.md "Lift and thrust"
[six-degrees-of-freedom]: six-degrees-of-freedom.md "Six degrees of freedom"
[pendulum-stability]: pendulum-stability.md "Pendulum stability"
[angular-momentum-multirotors]: angular-momentum-multirotors.md "Angular momentum in multirotors"
[induced-velocity]: induced-velocity.md "Induced velocity and sensor placement"
[vortex-ring-state]: vortex-ring-state.md "Vortex ring state"
[inertia-and-stopping]: inertia-and-stopping.md "Inertia and stopping distance"
