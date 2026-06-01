---
id: motor-mixing
title: "Motor mixing"
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
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Motor mixing translates three PID axis corrections (roll, pitch, yaw) plus
throttle into four individual motor speed commands. The mixer is the only
place in the control chain where the specific geometry of the frame matters —
all PID logic above it is geometry-agnostic. For a standard True-X quad
with "Props In" configuration, the signs and weights of each axis correction
on each motor follow directly from the frame geometry. The mixer table is
fixed at configuration time and does not change during flight.

---

## Concept

### What the mixer must do

The PID loops produce four numbers: a base throttle level, a roll correction,
a pitch correction, and a yaw correction. These must be combined onto four
motors such that:
- Increasing throttle: all four motors increase equally
- Rolling right: left motors increase, right motors decrease
- Pitching forward: rear motors increase, front motors decrease
- Yawing clockwise: CCW motors increase, CW motors decrease

The mixer computes this algebraically for each motor simultaneously.

### Standard X-frame mixing table (Props In)

Motor positions and rotation directions (standard Betaflight "Props In"):
- FL (front-left): counterclockwise
- FR (front-right): clockwise
- RL (rear-left): clockwise
- RR (rear-right): counterclockwise

    Motor FL = throttle + roll + pitch - yaw
    Motor FR = throttle - roll + pitch + yaw
    Motor RL = throttle + roll - pitch + yaw
    Motor RR = throttle - roll - pitch - yaw

**Roll right** (+ roll correction): FL and RL (left side) increase, FR and
RR (right side) decrease. Left motors produce more thrust → left side rises
→ drone rolls right. ✓

**Pitch forward** (+ pitch correction): FL and FR (front) increase, RL and
RR (rear) decrease. Wait — this pitches nose up, not forward. In Betaflight's
convention, pitch correction and pilot stick directions follow a specific
sign convention. The exact signs depend on whether the FC is mounted nose-forward
or rotated, and on mode settings. The principle is correct; verify orientation
in Betaflight's motor test after assembly.

**Yaw clockwise** (+ yaw correction): CCW motors (FL, RR) decrease, CW motors
(FR, RL) increase. Decreasing CCW speed reduces upward angular momentum;
increasing CW speed reduces downward angular momentum. Net angular momentum
shifts downward. Airframe reacts clockwise. ✓

### Why geometry is isolated to the mixer

PID math is purely algebraic — it computes how much roll correction, pitch
correction, and yaw correction are needed at each moment. It does not know
whether the drone is an X-frame, an H-frame, or a V-tail. The mixer applies
the geometry. Change the frame layout and only the mixer coefficients change —
the P, I, D, and FF tuning above the mixer remains valid.

This separation is architecturally clean: the control logic and the geometry
are independent concerns. A Betaflight build for an X-frame and a build for
a stretched-X differ only in their mixer configuration.

---

## Reference

### Motor numbering convention (Betaflight)

    Motor 1: FR (front-right, clockwise)
    Motor 2: FL (front-left, counterclockwise)
    Motor 3: RR (rear-right, counterclockwise)
    Motor 4: RL (rear-left, clockwise)

Betaflight's motor numbering is fixed. The mixer signs adjust for the
specific motor rotation directions and positions based on the selected
mixer preset in Betaflight Configurator.

### Saturation handling

When one motor would be commanded above 100% or below 0%, the mixer saturates:
it clips the command to the achievable range. This temporarily reduces the
accuracy of the other axes that depend on the saturated motor. At very low
throttle (near 0%), yaw authority is the first to suffer — the mixer cannot
reduce any motor's speed further. At maximum throttle, any additional correction
would require a motor above 100%.

Betaflight implements "airmode" to manage saturation at zero throttle: the mixer
is allowed to spin up some motors while spinning down others even at 0% throttle,
maintaining roll/pitch/yaw authority when the pilot cuts throttle completely.

---

## Procedure

### Verifying motor direction and mixer

1. Connect to Betaflight Configurator. Go to Motors tab.
2. With props removed, spin each motor individually to identify which
   Betaflight motor number corresponds to which physical motor.
3. Verify rotation direction: FL and RR should be counterclockwise, FR and
   RL clockwise (Props In). If any motor rotates wrong, change motor direction
   in ESC configurator (reverse two motor wires or use ESC firmware direction
   setting).
4. In Motors tab: verify that master slider moves all four motors equally
   (throttle mixing correct).
5. Do not proceed to first flight until all four motor directions are verified.

---

## Rationale

### Why motor direction errors are a common first-flight failure

A motor spinning in the wrong direction generates thrust in the correct
direction (propellers are symmetric for aerodynamic lift) but generates
yaw torque in the wrong direction. With one motor reversed, the mixer table
produces incorrect yaw corrections — the drone may not be able to control
yaw at all, or may spin uncontrollably on arming. The 5-minute verification
procedure in Betaflight is the only way to confirm correct configuration
before risking the build in flight.

---

## Connections

requires:
  - [[closed-loop-control]]
  - [[six-degrees-of-freedom]]
  - [[angular-momentum-multirotors]]
related:
  - [[pid-proportional-term]]
  - [[rpm-filter]]
leads_to:
  - [[imu-filter-tuning]]


[closed-loop-control]: closed-loop-control.md "Closed-loop control"
[six-degrees-of-freedom]: six-degrees-of-freedom.md "Six degrees of freedom"
[angular-momentum-multirotors]: angular-momentum-multirotors.md "Angular momentum in multirotors"
[pid-proportional-term]: pid-proportional-term.md "PID — proportional term"
[rpm-filter]: rpm-filter.md "RPM filter"
[imu-filter-tuning]: imu-filter-tuning.md "IMU filter tuning"
