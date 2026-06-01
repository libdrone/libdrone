---
id: closed-loop-control
title: "Closed-loop control"
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
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

A closed-loop control system measures its own output, compares it to a desired
value, and uses the difference to correct its input — continuously. An open-loop
system applies a fixed input and accepts whatever output results. Drone flight
control is impossible without closed-loop feedback: a human pilot cannot
execute the thousands of corrections per second needed to keep a multirotor
stable. The flight controller closes the loop using gyroscope measurements,
running the sense-compare-correct cycle at 8,000 times per second. Without
sensors to close the loop, the controller is blind and the drone falls.

---

## Concept

### The sense-compare-correct cycle

Every closed-loop controller follows the same cycle:

1. **Sense** — measure the current state of the system
2. **Compare** — find the difference between current state and desired state (the error)
3. **Correct** — apply a corrective output proportional to the error
4. **Repeat**

The faster this cycle runs, the more responsive and stable the system. A
thermostat runs the cycle every few minutes — acceptable for temperature
control, which changes slowly. A drone runs the cycle 8,000 times per second —
necessary for attitude control, where disturbances (wind gusts, motor transients)
happen in milliseconds.

### Why open-loop control fails for multirotors

An open-loop multirotor would require the pilot to manually calculate and command
each motor's speed every instant. Four motors, each at variable speed, with coupled
effects on all three axes simultaneously. Even at 10 corrections per second — the
maximum achievable by a human — the drone would be uncontrollable: disturbances
would accumulate between corrections until the drone flipped.

Closed-loop control removes this problem. The flight controller measures the
actual attitude 8,000 times per second and applies corrections at the same rate.
No human involvement required between pilot stick inputs.

### What closes the loop

The gyroscope is the sensor that closes the loop for attitude control. It measures
the actual rotation rate on all three axes — roll rate, pitch rate, yaw rate — and
delivers this to the flight controller every 125 µs. The flight controller compares
this to the commanded rotation rate (from pilot sticks) and computes the necessary
motor corrections.

The accelerometer closes the loop for the level/attitude estimate. The GPS closes
the loop for position. Each additional sensor adds another closed loop at a higher
level of the control hierarchy.

### Sensor dependencies and failure modes

The dependency chain is the safety-critical knowledge every operator needs:

- Lose gyroscope: attitude control fails, drone is uncontrollable
- Lose accelerometer: attitude hold fails, GPS modes fail, pilot falls back to rate mode
- Lose GPS: position hold fails, RTH unavailable, pilot falls back to attitude mode
- Lose RC link: failsafe activates (usually RTH if GPS available, or disarm)

A pilot who understands the dependency chain responds correctly to failures.
A pilot who does not may fight the wrong problem.

---

## Reference

### Control hierarchy in Betaflight / ArduPilot

| Loop level | Input | Sensor | Output |
|---|---|---|---|
| Inner (attitude rate) | Stick deflection → rate setpoint | Gyroscope | Motor speed corrections |
| Middle (attitude angle) | Stick release → level | Accelerometer + gyro fusion | Rate setpoint to inner loop |
| Outer (position) | GPS waypoint or position hold | GPS + barometer | Attitude setpoint to middle loop |

Each outer loop feeds setpoints to the inner loop. Failure of an outer-loop
sensor drops the control to the next inner level.

### Loop rates

| Controller | Loop rate | Update period |
|---|---|---|
| Attitude rate (inner) | 8,000 Hz | 125 µs |
| Attitude angle (middle) | 1,000 Hz | 1 ms |
| GPS position (outer) | 10 Hz | 100 ms |

The inner loop runs the fastest because attitude dynamics are the fastest
to diverge. GPS position changes slowly — 10 Hz is adequate.

---

## Procedure

<!-- not applicable -->

---

## Rationale

### Why this article precedes the PID articles

The PID articles describe specific implementations of closed-loop control.
This article establishes the concept — what a closed loop is, why it is
necessary, and how sensors make it work. A student who reads this article
first will understand why the P, I, and D terms exist before encountering
the mathematical details of each.

---

## Connections

requires:
  - [[six-degrees-of-freedom]]
related:
  - [[pid-proportional-term]]
  - [[pid-integral-term]]
  - [[pid-derivative-term]]
  - [[imu-gyroscope]]
leads_to:
  - [[pid-proportional-term]]
