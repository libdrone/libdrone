---
id: angular-momentum-multirotors
title: "Angular momentum in multirotors"
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
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

A spinning propeller has angular momentum. On a multirotor with all motors
spinning in the same direction, the net angular momentum would cause the
airframe to spin in the opposite direction — making it uncontrollable. Counter-
rotating motor pairs cancel the net angular momentum at hover. More importantly,
this means yaw control on a quadcopter requires no moving parts: it works
entirely by adjusting the speed balance between the two pairs of counter-rotating
motors, shifting the net angular momentum and forcing the airframe to react.

---

## Concept

### Angular momentum and why it matters

Angular momentum is the rotational equivalent of linear momentum. A spinning
object resists changes to its spin axis in proportion to how massive it is and
how fast it spins. The angular momentum vector points along the spin axis
(by the right-hand rule: curl the fingers of the right hand in the direction
of rotation, the thumb points in the direction of the angular momentum vector).

When a propeller spins clockwise viewed from above, its angular momentum vector
points downward. To change this angular momentum — to speed the propeller up,
slow it down, or tilt the airframe — requires applying a torque. The reaction
to that torque acts on the airframe.

### Why counter-rotation is a physical necessity, not a convention

Consider a drone with all four motors spinning clockwise viewed from above.
The total angular momentum of the propeller system points downward. The airframe,
reacting to this angular momentum, tends to spin counterclockwise. No amount of
PID tuning can correct this — it is a direct physical consequence of all the
angular momentum being aligned in one direction. The drone is uncontrollable
in yaw.

Counter-rotating motor pairs cancel this. Two motors spin clockwise (angular
momentum pointing down), two spin counterclockwise (angular momentum pointing
up). At equal speed, the total angular momentum of the system is zero — the
airframe experiences no net rotational reaction and does not yaw.

### Yaw control by angular momentum differential

To yaw the drone clockwise: increase the speed of the two counterclockwise
motors (increasing their upward angular momentum) while decreasing the speed
of the two clockwise motors (decreasing their downward angular momentum).
The net angular momentum of the propeller system shifts toward pointing upward.
The reaction in the airframe is to rotate clockwise.

This is elegant: yaw is controlled entirely by adjusting four numbers (motor
speeds), with no mechanical linkages and no moving parts beyond the motors
themselves. The entire yaw response comes from physics, not from mechanical
complexity.

### Motor layout and prop direction assignment

In a standard quadcopter (Betaflight "Props In" configuration):
- Front-left (FL): counterclockwise
- Front-right (FR): clockwise
- Rear-left (RL): clockwise
- Rear-right (RR): counterclockwise

Diagonal pairs share the same direction. This arrangement ensures that all
roll, pitch, and yaw commands produce balanced thrust changes across the frame.
Installing a propeller in the wrong rotation direction produces incorrect mixing
— the drone will attempt to spin uncontrollably on arm.

---

## Reference

### Right-hand rule for angular momentum direction

| Motor rotation (viewed from above) | Angular momentum vector |
|---|---|
| Clockwise | Points downward (into ground) |
| Counterclockwise | Points upward (toward sky) |

### Yaw mixing (standard X quad, Props In)

| Command | FL (CCW) | FR (CW) | RL (CW) | RR (CCW) |
|---|---|---|---|---|
| Yaw clockwise | ↑ increase | ↓ decrease | ↓ decrease | ↑ increase |
| Yaw counterclockwise | ↓ decrease | ↑ increase | ↑ increase | ↓ decrease |

Increasing CCW motor speed shifts net angular momentum upward → airframe
reacts clockwise (Newton's third law).

### Why yaw is the weakest axis

Yaw torque is proportional to the angular momentum differential between
clockwise and counterclockwise pairs. At any given throttle, the maximum
yaw torque available is limited by how much speed differential can be
created before one motor pair runs out of headroom. Roll and pitch use
thrust differential directly — a much larger force. Yaw uses angular momentum
differential — a smaller, indirect effect. Result: yaw has inherently
lower maximum rate than roll or pitch on a quadcopter.

---

## Procedure

<!-- not applicable -->

---

## Rationale

### Why this article exists separately from six-degrees-of-freedom

[[six-degrees-of-freedom]] explains the geometry of control — which actuators
produce which motions. This article explains the underlying physics of the yaw
axis specifically — why counter-rotation is necessary, why yaw authority is
limited, and why the mixing table has the signs it does. A student reading
only the geometry article will know that yaw is produced by motor pairs; a
student reading this article will understand why that works and why it is
weaker than the other axes.

---

## Connections

requires:
  - [[six-degrees-of-freedom]]
related:
  - [[lift-and-thrust]]
  - [[hover-and-forward-flight]]
  - [[moment-of-inertia]]
leads_to:
  - [[hover-and-forward-flight]]
  - [[moment-of-inertia]]
