---
id: pendulum-stability
title: "Pendulum stability"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - physics-flight-mechanics
personas:
  - 5.student
  - 7.contributor
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

A drone with its centre of mass below the propeller plane behaves like a
pendulum: any tilt displaces the heavy centre of mass, gravity creates a
restoring torque, and the drone tends to return to level. The lower the centre
of mass relative to the propeller plane, the stronger this passive stabilising
effect and the longer the effective pendulum arm. In libdrone V2.4.6, the
battery is mounted flat on the body rather than on a raised stack, lowering
the CG by 8–12 mm compared to the previous version — a deliberate design
decision with calculable consequences for handling and PID tuning.

---

## Concept

### The pendulum analogy

Suspend a weight from a string and push it sideways. Gravity creates a
restoring torque proportional to the sine of the displacement angle — the
weight swings back. The longer the string (pendulum arm), the stronger the
restoring effect per unit mass, and the lower the natural oscillation frequency.
Shorten the string and the pendulum oscillates faster.

A drone with its CG below the propeller plane behaves identically. When the
drone tilts, the CG hangs lower on the tilted side. The gravitational force
acting on the CG, now displaced from the prop plane's centre, creates a torque
that tends to restore level attitude. The propeller-plane-to-CG distance is
the effective pendulum arm.

### Effect on PID tuning

The natural frequency of the pendulum system is:

    f₀ = (1 / 2π) × sqrt(g / L)

Where g = 9.81 m/s² and L = pendulum arm length (CG below prop plane).

A shorter pendulum arm means higher f₀ — the drone responds faster to
disturbances. This sounds like a benefit, but it means the PID derivative
(D) term must be tuned more aggressively to damp the faster oscillations.
Insufficient D at higher f₀ results in visible oscillation at the natural
pendulum frequency — which is exactly what a badly tuned D-term looks like
in a Blackbox trace.

This is why the libdrone V2.4.6 release note says: **reduce D-term 10–15%
from V2.14 baseline at maiden**. The lower CG raised f₀, making the drone
more responsive to D and requiring a lower gain to prevent oscillation.

### CG above the prop plane — unstable

If the CG were above the propeller plane, the geometry inverts: a tilt moves
the heavy mass higher on the tilted side. Gravity now creates a torque that
amplifies the tilt rather than restoring it. The equilibrium is unstable —
any small disturbance grows rather than damps. This is the inverted pendulum
problem. Active control can stabilise an inverted pendulum, but the flight
controller must work against the natural geometry, requiring higher gains and
faster loop rates. Most multirotor platforms are designed with CG well below
the prop plane to exploit passive stability.

---

## Reference

### CG effect on PID in libdrone V2.4.6

| Version | Battery mount | CG offset from prop plane | PID consequence |
|---|---|---|---|
| V2.14 | Elevated stack | Higher | Longer arm, lower f₀, softer D |
| V2.4.6 | Flat side-slide | Lower by ~8–12 mm | Shorter arm, higher f₀, needs D reduced 10–15% |

### CG location principles

- Heavy components (battery) placed as low as possible to maximise pendulum arm
- Electronics on Platform middle layer — centred vertically in the body
- Payload mast raises payload above body — increases CG for heavy payloads;
  verify CG position with payload fitted before maiden

### CG shift with payload

A tall sensor mast (80–120 mm) raises the CG by an amount proportional to
the payload mass. For a 40 g payload at 100 mm height on a 860 g drone with
CG at −10 mm below prop plane:

    CG shift = (payload_mass × payload_height) / total_mass
            = (0.040 × 100) / 0.860 ≈ +4.7 mm

The CG moves 4.7 mm upward — shortening the effective pendulum arm. Retune
D slightly downward with tall, heavy payloads fitted. Not required for payloads
under 20 g or mast heights under 60 mm.

---

## Procedure

<!-- not applicable — tuning procedure is in pid-tuning-rate-profile -->

---

## Rationale

### Why lowering the CG was an explicit V2.4.6 design goal

The previous battery mount placed the battery on top of a raised PETG tray,
elevating it approximately 20 mm above the sandwich top surface. The V2.4.6
side-slide battery rail mounts the battery flush with the Platform surface —
reducing CG height by 8–12 mm. This was not a side effect of the new battery
rail geometry; it was a stated design goal. Lower CG means faster roll and
pitch response from the same propulsion system, without any change to motor or
prop selection.

---

## Connections

requires:
  - [[lift-and-thrust]]
related:
  - [[six-degrees-of-freedom]]
  - [[hover-and-forward-flight]]
  - [[moment-of-inertia]]
leads_to:
  - [[hover-and-forward-flight]]
  - [[pid-tuning-rate-profile]]
  - [[moment-of-inertia]]


[lift-and-thrust]: lift-and-thrust.md "Lift and thrust"
[six-degrees-of-freedom]: six-degrees-of-freedom.md "Six degrees of freedom"
[hover-and-forward-flight]: hover-and-forward-flight.md "Hover and forward flight"
[moment-of-inertia]: moment-of-inertia.md "Moment of inertia"
[pid-tuning-rate-profile]: pid-tuning-rate-profile.md "PID tuning and rate profile"
