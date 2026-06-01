---
id: six-degrees-of-freedom
title: "Six degrees of freedom"
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
  - 1.builder
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Any rigid body moving in three-dimensional space has exactly six degrees of
freedom: three translational (forward/back, left/right, up/down) and three
rotational (roll, pitch, yaw). A quadcopter has four independent actuators —
four motor speeds — which means it cannot independently control all six
simultaneously. Understanding which freedoms are coupled, and how the flight
controller manages that coupling, explains why drones behave the way they do.

---

## Concept

### Six degrees, four actuators

Three translational and three rotational degrees of freedom give six
dimensions to control. A quadcopter has exactly four independent inputs:
motor 1 speed, motor 2 speed, motor 3 speed, motor 4 speed. With four numbers
controlling six dimensions, the system is underdetermined — it cannot achieve
arbitrary combinations of position and attitude simultaneously.

In practice, the four actuators control: total thrust (vertical translation),
roll (differential thrust left vs right), pitch (differential thrust front vs
rear), and yaw (differential angular momentum). That is four controlled
outputs from four inputs — exactly determined, no redundancy.

What a quadcopter cannot do: move horizontally while keeping its heading and
altitude fully independent. To move left it must roll left — tilting the thrust
vector sideways. The reduced vertical component then requires increased throttle
to maintain altitude. Every degree of pitch or roll requires simultaneous
altitude compensation. Everything couples to everything else.

### Why coupling matters for the flight controller

Because roll affects altitude, pitch affects altitude, and yaw affects neither
translation directly but changes the drag asymmetry, the flight controller
runs separate PID loops for roll, pitch, yaw, altitude, and position
simultaneously — each feeding corrections into the others. The coupling is the
reason the flight controller needs to run at 8,000 loops per second: any slower
and the corrections from each loop arrive too late to prevent the cross-axis
effects from accumulating into visible oscillation.

### Motor redundancy and failure modes

A standard quadcopter losing one motor drops to three actuators for six
degrees of freedom — catastrophically underdetermined, uncontrollable.
This is not a design flaw; it is the explicit cost of using the minimum number
of motors. The tradeoff is direct: fewer motors means less weight, complexity,
and cost, but also zero redundancy.

A hexacopter has six actuators for six degrees — exactly determined. Lose one
motor and it drops to five actuators — still underdetermined, but with enough
redundancy to maintain controlled flight with reduced authority. This is why
professional survey drones for safety-critical applications use six or eight
motors despite the mass penalty: each additional motor buys one level of
redundancy.

### Yaw authority

Yaw is the weakest axis on a quadcopter. Roll and pitch are produced by
differential thrust — the primary force the motors generate. Yaw is produced
by differential angular momentum between clockwise and counterclockwise motor
pairs, which is a much smaller effect. At high throttle, the yaw authority
decreases relative to the available roll and pitch authority. This is why
aggressive yaw manoeuvres are the hardest to tune in Betaflight and why
yaw spins in freestyle flying require much more throttle than roll or pitch
rolls of equal angular velocity.

---

## Reference

### Degrees of freedom summary

| Axis | Motion type | Controlled by | Notes |
|---|---|---|---|
| Z (vertical) | Translation | All four motors simultaneously | Throttle |
| X (lateral) | Translation | Roll → tilt → horizontal thrust | Coupled to altitude |
| Y (fore/aft) | Translation | Pitch → tilt → horizontal thrust | Coupled to altitude |
| Roll | Rotation | Differential thrust left vs right | Decoupled at hover |
| Pitch | Rotation | Differential thrust front vs rear | Decoupled at hover |
| Yaw | Rotation | Differential angular momentum CW vs CCW | Weakest axis |

### Motor redundancy by configuration

| Motors | Actuators vs DOF | Motor failure result |
|---|---|---|
| Quad (4) | 4 vs 6 — underdetermined | 3 vs 6 — uncontrollable |
| Hex (6) | 6 vs 6 — exactly determined | 5 vs 6 — reduced authority, flyable |
| Octo (8) | 8 vs 6 — overdetermined | 7 vs 6 — full authority retained |

---

## Procedure

<!-- not applicable -->

---

## Rationale

### Why libdrone uses a quad configuration

Four motors is the minimum for controlled flight in three dimensions. Each
additional motor adds weight, cost, and complexity. For a research payload
platform that flies in controlled conditions with a competent operator, the
no-redundancy tradeoff is acceptable. The weight saving of a quad versus a
hex directly translates to payload mass budget or flight time — both of which
are mission-critical parameters. A hex or octo would extend the redundancy but
consume the payload weight budget.

---

## Connections

requires:
  - [[lift-and-thrust]]
related:
  - [[angular-momentum-multirotors]]
  - [[hover-and-forward-flight]]
leads_to:
  - [[angular-momentum-multirotors]]
  - [[hover-and-forward-flight]]
