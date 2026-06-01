---
id: moment-of-inertia
title: "Moment of inertia"
version: 1.0.0
date: 2026-04-15
author: jsa
status: released
scope: generic
topic:
  - physics-flight-mechanics
personas:
  - 5.student
  - 8.architect
  - 1.builder
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Moment of inertia (MoI) is the rotational equivalent of mass — it describes
how strongly an object resists changes to its rotation. For a drone frame,
MoI determines how fast the aircraft responds to attitude commands: a lower
MoI means faster response, a higher MoI means slower and more predictable
response. Frame geometry and mass distribution are the primary MoI levers.
A compact frame with mass concentrated near the centre has lower MoI and
responds faster. A wide frame or one with heavy batteries or payloads far
from the centre has higher MoI and responds more slowly. This relationship
directly affects PID tuning — particularly the D-term — and must be
re-evaluated whenever the build geometry or payload changes.

---

## Concept

### What moment of inertia is

Linear inertia (mass) describes resistance to changes in linear velocity.
Push a heavy object and it accelerates slowly. Push a light object and it
accelerates quickly. Moment of inertia describes the same resistance for
rotation: how strongly a body resists changes in angular velocity when a
torque is applied.

The key difference from mass: MoI depends not just on how much mass is
present, but on where that mass is relative to the rotation axis. Mass far
from the rotation axis contributes more to MoI than the same mass near the
axis. Specifically, MoI = Σ(m × r²) — every mass element contributes its
mass multiplied by the square of its distance from the axis.

This r² dependence is what makes geometry so important. A drone where the
battery is at the centre of the frame has a lower MoI than an identical drone
where the battery is mounted on extended rails at the frame perimeter — even
if both weigh the same. Moving the battery 20mm outward does not increase
MoI by 20mm — it increases it by (20mm)² relative to the original distance.

### MoI in practice: response time and agility

The flight controller's PID loop applies torque to the drone through
differential motor speed. The same PID gains apply the same torque regardless
of MoI. With lower MoI, that torque produces faster angular acceleration and
therefore a faster attitude response. With higher MoI, the same torque produces
slower angular acceleration.

For a performance FPV platform, low MoI is desirable: snappy response to
stick inputs feels immediate and predictable. For a survey platform carrying
a sensor mast or payload, higher MoI is acceptable and may even be beneficial
— the drone resists wind gusts better when its inertia is larger, reducing
attitude excursions that degrade sensor data quality.

### The PID D-term dependency

The PID D-term responds to the rate of change of attitude error — it is a
braking term that prevents overshoot. The correct D-term value depends on
how fast the drone naturally responds to inputs: a faster (lower MoI) drone
requires less D-term to prevent overshoot; a slower (higher MoI) drone
requires more D.

This is why D-term must be re-tuned whenever MoI changes significantly:
- Adding a sensor payload (increased MoI → increase D)
- Mounting battery lower and flatter (decreased MoI → reduce D)
- Switching from 4-inch to 6-inch props with heavier motors (increased MoI)

The libdrone V2.4.6 geometry lowered the centre of gravity 8–12mm compared
to its predecessor by changing the battery mount from a tall stack to a flat
tray. This reduced the pendulum arm length (see → [[pendulum-stability]]) and
also reduced the vertical MoI — the D-term recommendation at maiden was
reduced 10–15% from the previous baseline specifically because of this.

### MoI and the pendulum effect

The pendulum arm (distance from the centre of mass to the propeller plane)
and MoI are related but distinct. The pendulum arm determines the natural
oscillation frequency of the frame under gravity. MoI determines how fast
the frame can be accelerated rotationally by the motors. A short pendulum
arm increases natural frequency; a low MoI increases motor-driven
responsiveness. Both change together when the battery is moved lower, which
is why both the D-term and the natural frequency shifted together in V2.4.6.

---

## Reference

### MoI sensitivity by component placement

| Change | MoI effect | D-term adjustment |
|---|---|---|
| Battery mounted lower (flat tray) | Decreases roll/pitch MoI | Reduce 10–15% |
| Battery on extended rear plate | Increases pitch MoI | Increase 10–15% |
| Sensor mast added (100g at 80mm height) | Increases pitch/roll MoI | Increase ~5–10% |
| Shorter/lighter arms | Decreases MoI | Reduce D slightly |
| Heavier motors (outer mass) | Increases MoI | Increase D |

**Rule of thumb**: a 10% MoI increase → approximately 5–8% D-term increase to
maintain the same overshoot behaviour. Always verify with blackbox after
significant payload changes.

---

## Procedure

### Identify MoI change after a build modification

1. After any modification that changes mass distribution — new battery, new
   payload, different motor mount height — expect the D-term to need adjustment.
2. Fly a hover, apply a sharp roll input, and observe the step response in
   the blackbox trace (filtered gyro vs motor output).
3. If the drone overshoots and rings → D-term too low (MoI increased, braking
   insufficient).
4. If the drone responds sluggishly and never quite reaches the commanded
   attitude → D-term too high (MoI decreased, braking excessive).
5. Adjust D-term in Betaflight rate profile in 5% increments until step
   response shows crisp arrival with minimal overshoot.

See → [[pid-derivative-term]] for D-term tuning methodology and
→ [[blackbox-analysis]] for how to read the step response.

---

## Rationale

Moment of inertia is treated as an implicit concept in most Betaflight tuning
guides — builders learn to adjust the D-term when the drone changes, but not
why. Making MoI explicit as an atom closes this gap: a student who understands
MoI can predict in advance how a design change will affect handling, rather
than discovering it empirically after the first flight. The V2.4.6 CG
lowering is the concrete libdrone example that makes the concept tangible.

---

## Connections

requires:
  - [[six-degrees-of-freedom]]
  - [[angular-momentum-multirotors]]
related:
  - [[pendulum-stability]]
  - [[pid-derivative-term]]
  - [[pid-tuning-rate-profile]]
  - [[vibration-isolation-theory]]
  - [[floating-motor-mounts]]
leads_to:
  - [[pendulum-stability]]
  - [[pid-derivative-term]]
  - [[blackbox-analysis]]
