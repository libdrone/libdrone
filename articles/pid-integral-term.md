---
id: pid-integral-term
title: "PID — integral term"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - control-systems
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

The integral term (I) accumulates error over time. If a small error persists
— the drone consistently drifts right because one motor is slightly weaker,
or the centre of mass is off-centre — I builds up a stored correction that
grows until it exactly eliminates the residual. I is the term that allows the
drone to hold a precise position against steady wind or compensate for hardware
imbalance without constant stick input. Its risk is windup: if the error never
reduces (commanded attitude is physically impossible), I accumulates without
bound and delivers an unexpected large correction when conditions change.

---

## Concept

### Why P alone is insufficient

The proportional term can only correct what it can currently see. If the drone
needs a constant small correction — say, a 1% motor speed difference to fly
level — P provides that correction, but as an equilibrium condition where the
error is exactly the size needed to produce the balancing correction. The drone
is slightly off the setpoint forever, because reducing the error would reduce
the correction, which would let the disturbance push the drone further off.

This is steady-state error. P cannot eliminate it; I can.

### How I works

The integral term accumulates error over time:

    I_output = K_I × sum(error × dt)

Every PID cycle, the current error is multiplied by the cycle time and added
to a running total. As long as any error exists, this total grows. The I output
grows with it. Eventually the I term alone provides enough correction to
balance the steady disturbance — at which point the error drops to zero,
the integrator stops accumulating, and the total stabilises. The drone
holds the setpoint exactly.

This is the mechanism that allows a drone to maintain a perfectly level hover
when one arm is slightly heavier, or to hold a fixed altitude despite slow
battery voltage sag changing the effective motor power.

### I windup — the failure mode

If the commanded setpoint is physically impossible to achieve — the drone is
commanded to hover but is being held down by a hand — the error never reduces
to zero. The integrator accumulates without limit. When the constraint is removed
(the hand lets go), the accumulated integral delivers a large, sudden correction.
The drone shoots upward.

Betaflight limits I accumulation to prevent runaway windup. The I term is also
anti-wound during throttle saturation (when motors are at maximum) and during
arming/disarming.

### I and long-duration hover

For libdrone's air quality mapping missions, which may involve hovering at a
fixed position for 30–120 seconds, the I term is critical. Battery voltage
sags continuously during the flight, reducing motor output per unit throttle
command. Without I, the drone would gradually descend as the battery empties,
requiring the operator to continuously apply upward throttle. With I, the
integrator detects the altitude error and automatically increases throttle to
compensate. The operator sees a stable hover; the integrator silently
compensates for 5–8V of battery sag over the flight.

---

## Reference

### I effects on flight behaviour

| I value | Symptom |
|---|---|
| Too low | Steady drift in constant conditions, needs stick correction to stay level |
| Slightly low | Slow oscillation at low frequency, drone wanders |
| Correct | Holds position and attitude precisely in steady conditions |
| Too high | Slow oscillation after large corrections — "toilet bowl" oscillation in position hold |
| Windup | Sudden large correction after escape from constrained condition |

### I and GPS position hold

In GPS position hold, the outer GPS loop generates position error and feeds
it as a setpoint to the attitude loop. The I term in the position loop
compensates for sustained wind — if a 10 km/h wind consistently pushes
the drone north, the position I accumulates a southward pitch bias that
counters the wind without requiring continuous GPS correction. This is
the mechanism behind position hold that "leans into" sustained wind rather
than constantly chasing the setpoint.

---

## Procedure

### I tuning sequence (Betaflight)

1. Tune P first. Then tune D. Only adjust I after both P and D are set.
2. In calm air, hover and observe whether the drone maintains attitude
   without stick input. If it drifts consistently in one direction, I is
   too low.
3. After a large pitch or roll manoeuvre, observe whether the drone returns
   cleanly to level. If it overshoots and oscillates slowly: I is too high.
4. Adjust I in 10% steps. I changes are slow-acting — evaluate over a
   10–30 second hover, not a brief hover.
5. The ideal: drone holds a fixed hover position in calm air without stick
   input, returns cleanly to level after manoeuvres, no slow oscillation.

---

## Rationale

### Why I is tuned last

I operates on accumulated error over time. If P or D are wrong, the error
accumulation seen by I is also wrong — I would compensate for oscillations
caused by incorrect P or D rather than for real steady-state error. Tuning I
after P and D ensures it only compensates for genuine steady disturbances,
not for tuning artefacts.

---

## Connections

requires:
  - [[closed-loop-control]]
  - [[pid-proportional-term]]
related:
  - [[pid-derivative-term]]
  - [[feed-forward-control]]
leads_to:
  - [[pid-derivative-term]]
  - [[feed-forward-control]]


[closed-loop-control]: closed-loop-control.md "Closed-loop control"
[pid-proportional-term]: pid-proportional-term.md "PID — proportional term"
[pid-derivative-term]: pid-derivative-term.md "PID — derivative term"
[feed-forward-control]: feed-forward-control.md "Feed-forward control"
