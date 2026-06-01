---
id: pid-proportional-term
title: "PID — proportional term"
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
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The proportional term (P) of a PID controller applies a correction proportional
to the current error: large error produces large correction, small error produces
small correction. P is the primary stiffness of the flight controller — too low
and the drone drifts and responds sluggishly, too high and it oscillates rapidly.
P alone cannot eliminate steady-state error (a drone that needs constant slight
correction to fly level will always be slightly off) — that is the job of the
integral term. For libdrone's mapping role, P is tuned conservatively: responsive
enough to reject wind, not so aggressive that it fights itself during slow survey
transects.

---

## Concept

### What proportional means

The proportional term multiplies the current error by a constant gain K_P:

    P_output = K_P × error

Where `error = setpoint − measured_value` (desired rotation rate minus actual
rotation rate in degrees/second).

If the drone is 10°/s away from the commanded rate, and K_P = 50, the correction
output is 500. If the drone is 2°/s away, the correction is 100. The controller
applies exactly as much correction as the error requires — proportionally.

### The residual offset problem

A purely proportional controller always leaves a small residual error. Here is why:
as the drone approaches the setpoint, the error shrinks, so the correction shrinks.
At some point, the correction is just barely large enough to overcome the forces
holding the drone off setpoint (friction, steady wind, slight mass imbalance).
At that point, the system reaches equilibrium — but slightly off the setpoint.
The correction exactly balances the disturbance, but the drone is not quite at
the commanded attitude.

This residual offset is called **steady-state error**. In practice it means the
drone consistently flies at a slightly wrong attitude unless the pilot applies
a permanent stick input. The I term (integral) is designed to eliminate this.
→ See [[pid-integral-term]].

### P too low: sluggish and drifting

When K_P is too low, even a large error produces only a small correction. The
drone responds slowly to disturbances — wind pushes it off course and it
takes a long time to return. Manual stick inputs feel mushy. The drone oscillates
slowly, never snapping to the commanded attitude.

In a Blackbox trace, low P shows as large, slow gyro excursions that gradually
damp out over many cycles.

### P too high: rapid oscillation

When K_P is too high, even a small error produces a large, aggressive correction.
The drone overshoots the setpoint, overcorrects, overshoots again — oscillating
at high frequency. The oscillation frequency is approximately the natural frequency
of the airframe-motor system. At extreme P values, the oscillation becomes
self-sustaining and the drone is unflyable.

In a Blackbox trace, high P shows as a rapid, sustained oscillation on all axes,
visible in both the gyro trace and the motor output trace.

### Correct P: crisp, settled, no oscillation

Correctly tuned P produces a response that reaches the setpoint quickly and
settles without visible oscillation. Stick inputs feel direct and proportional.
Wind gusts are rejected promptly. There is no sustained ringing after a disturbance.

---

## Reference

### P effects on flight behaviour

| P value | Symptom | Observable |
|---|---|---|
| Too low | Slow oscillation, mushy response | Gyro: slow, large excursions |
| Slightly low | Under-responsive to wind, drifts | OSD: poor position hold |
| Correct | Crisp, stable, prompt wind rejection | Blackbox: clean settle |
| Slightly high | Some oscillation after manoeuvres | Gyro: small ringing post-disturbance |
| Too high | Rapid sustained oscillation, hot motors | Audio: high-pitched buzz from motors |

### P and the pendulum natural frequency

The correct P gain is related to the airframe's natural frequency (determined
by its moment of inertia and the pendulum effect). Lowering the CG (as in
V2.4.6 vs V2.14) increases the natural frequency → requires slightly different
P tuning. Start from documented baseline values and adjust from Blackbox
evidence, not by feel alone. → See [[pendulum-stability]].

---

## Procedure

### P tuning sequence (Betaflight)

1. Set I and D to zero (or very low). Work on P in isolation.
2. Hover and observe stability. Introduce a sharp disturbance (brisk pitch input,
   hand-wave near the drone).
3. If drone oscillates continuously: lower P by 10–15%.
4. If drone drifts slowly: raise P by 10–15%.
5. Target: drone snaps back from a disturbance and settles in 1–2 oscillation
   cycles without sustained ringing.
6. Once P is set, restore I and D before further tuning.
7. Verify result in Blackbox: gyro trace should show clean, damped response
   to step inputs.

---

## Rationale

### Why P is the first term to tune

P sets the fundamental gain of the control loop — the relationship between
error magnitude and correction magnitude. I and D modify P's behaviour (I
removes steady-state error, D prevents overshoot), but they cannot compensate
for a badly set P. Starting with P correct before adding I and D is the standard
practice because the interactions are easier to understand one term at a time.

### Why libdrone tunes P conservatively

libdrone spends most of its flight time in GPS position hold at low speed.
In this regime, the disturbances are slow-moving (wind, thermal drift) and
the control demands are modest. Aggressive P tuned for freestyle flying would
produce unnecessary motor activity, heat, and vibration during steady-state
hover. Conservative P keeps the flight smooth and the motors cool during
long mapping missions, accepting slightly slower transient response that
is invisible in practice.

---

## Connections

requires:
  - [[closed-loop-control]]
related:
  - [[pid-integral-term]]
  - [[pid-derivative-term]]
  - [[pendulum-stability]]
leads_to:
  - [[pid-integral-term]]
  - [[pid-derivative-term]]


[pid-integral-term]: pid-integral-term.md "PID — integral term"
[pendulum-stability]: pendulum-stability.md "Pendulum stability"
[closed-loop-control]: closed-loop-control.md "Closed-loop control"
[pid-derivative-term]: pid-derivative-term.md "PID — derivative term"
