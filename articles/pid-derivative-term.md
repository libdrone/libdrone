---
id: pid-derivative-term
title: "PID — derivative term"
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

The derivative term (D) acts on the rate of change of error — it applies
braking when the drone is approaching the setpoint rapidly, preventing
overshoot. D is the most noise-sensitive PID term: because differentiation
amplifies high-frequency content, any motor vibration reaching the gyroscope
is amplified by D and converted into motor commands. This is why vibration
isolation and RPM filtering must be in place before D is tuned — without
them, D amplifies noise rather than damping the response. D also damps prop
wash oscillation, the characteristic bouncing that occurs when a drone flies
through disturbed air from its own previous path.

---

## Concept

### Predictive braking

The derivative term calculates:

    D_output = K_D × d(error)/dt

The rate of change of error: how fast the error is decreasing (or increasing).
If the error is decreasing rapidly — the drone is snapping back toward the
setpoint quickly — D applies a large braking force proportionally. If error
is changing slowly, D is small.

The effect: the drone decelerates before it reaches the setpoint, arriving
smoothly rather than overshooting. D makes corrections that P would
otherwise overshoot. Without D, a well-tuned P still oscillates; with D,
the P correction is damped at the right moment.

Physical analogy: car suspension dampers. The spring (P) pushes the wheel
back up after a bump. The damper (D) slows the spring's return, preventing
the car from bouncing. Without the damper, even a well-sprung car would
oscillate after every bump.

### Why D amplifies noise

Differentiation is the mathematical operation that amplifies high-frequency
signal content. A slowly varying signal (attitude changing at 10 Hz) has
a large derivative term only when it changes quickly. A high-frequency noise
signal (motor vibration at 500 Hz) appears to be changing rapidly at all
times — its derivative is always large.

When motor vibration reaches the gyroscope, the gyro faithfully reports it.
The D term sees a rapidly changing error signal and generates large, rapid
corrective motor commands. These commands create additional motor current
changes, which generate additional vibration. The loop closes in a way that
amplifies the noise rather than the correction.

This is the fundamental reason why mechanical vibration isolation and the
RPM filter must precede D tuning. They remove the high-frequency noise
before D sees it, allowing D to act only on genuine attitude dynamics.
→ See [[floating-motor-mounts]], [[rpm-filter]].

### Prop wash

Prop wash is the disturbed air that forms behind a drone after a fast
forward pass or after a quick deceleration. When the drone's propellers
fly through this disturbed air (on the return path, or if the drone
decelerates into its own wake), the airflow into each propeller disc
is asymmetric and turbulent. The motors experience rapidly changing
load, causing rapid attitude disturbances that appear as oscillation.

D is the primary tuning term for prop wash handling. Higher D provides
more damping of the rapid oscillations. However, the same higher D
amplifies motor noise — the tuning is a direct tradeoff between noise
sensitivity and prop wash handling.

The RPM filter resolves this tradeoff by removing motor noise before D
acts on it, allowing D to be tuned higher for better prop wash without
the noise amplification penalty.

### D and the V2.4.6 lower CG

The lower CG in V2.4.6 raises the pendulum natural frequency — the drone
oscillates more quickly after a disturbance. This means the rate of change
of error is higher for the same displacement, making D more sensitive.
The documented recommendation to reduce D by 10–15% from V2.14 baseline
is a direct consequence: the same physical D gain produces more aggressive
braking on the higher-frequency dynamics.

---

## Reference

### D effects on flight behaviour

| D value | Symptom |
|---|---|
| Too low | Overshoot after stick inputs, bouncy in prop wash, slow settling |
| Slightly low | Oscillation after fast manoeuvres, visible in Blackbox as ringing |
| Correct | Clean settle after disturbances, good prop wash handling |
| Slightly high | Motor buzz, elevated motor temperature, noise floor higher in Blackbox |
| Too high | Rapid motor noise transmission, motors overheating, chassis vibration |

### D tuning with libdrone V2.4.6

Starting point: 10–15% below the V2.14 baseline value (as documented in
the Betaflight configuration). Adjust from Blackbox evidence:
- If gyro trace shows ringing after sharp inputs: raise D slightly
- If motor temperature is elevated at rest after hover: lower D slightly
- If prop wash is visible (Blackbox: gyro oscillation on roll/pitch axis
  during descents): raise D slightly

---

## Procedure

### D tuning sequence (Betaflight)

1. Ensure RPM filter is active and functional (BiDi DShot confirmed working
   — all four motors report eRPM in Betaflight motors tab).
2. Tune P first, then add D.
3. Set D to half the expected value. Fly and observe prop wash: make a fast
   forward pass, then a quick stop. Oscillation in the hover after stopping
   indicates insufficient D.
4. Raise D in 5–10% steps. After each increase, check motor temperature
   with a hand (warm is acceptable, hot is not) and review Blackbox noise floor.
5. Stop raising D when motor temperature increases noticeably or the Blackbox
   noise floor rises significantly.
6. Target: clean gyro trace with no sustained oscillation, motors warm but
   not hot after 3–5 minutes hover.

---

## Rationale

### Why D is tuned after vibration isolation is confirmed

D's entire effect depends on the quality of the gyro signal it receives.
If significant motor vibration noise reaches the gyro, any D value will
partially amplify noise rather than damp genuine dynamics. The result is
a D value that appears to work at low settings but generates motor heat
and noise at higher settings. Confirming that mechanical isolation and RPM
filtering are working before tuning D ensures D responds to attitude dynamics,
not noise.

---

## Connections

requires:
  - [[closed-loop-control]]
  - [[pid-proportional-term]]
related:
  - [[pid-integral-term]]
  - [[rpm-filter]]
  - [[floating-motor-mounts]]
  - [[vibration-isolation-theory]]
  - [[pendulum-stability]]
leads_to:
  - [[feed-forward-control]]
  - [[rpm-filter]]


[floating-motor-mounts]: floating-motor-mounts.md "Floating motor mounts"
[rpm-filter]: rpm-filter.md "RPM filter"
[closed-loop-control]: closed-loop-control.md "Closed-loop control"
[pid-proportional-term]: pid-proportional-term.md "PID — proportional term"
[pid-integral-term]: pid-integral-term.md "PID — integral term"
[vibration-isolation-theory]: vibration-isolation-theory.md "Vibration isolation theory"
[pendulum-stability]: pendulum-stability.md "Pendulum stability"
[feed-forward-control]: feed-forward-control.md "Feed-forward control"
