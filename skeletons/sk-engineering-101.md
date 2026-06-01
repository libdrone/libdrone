---
id: sk-engineering-101
title: "Engineering Principles 101"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: generic
topic:
  - skeletons
personas:
  - 5.student
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

After reading this document, the student can explain the physics behind drone
flight, describe how each subsystem contributes to controlled motion, and
identify the engineering tradeoffs that govern the design of a real platform.
This is the student entry point to the libdrone corpus — the equivalent of
EP101 in the 2.x documentation stack, rewritten as navigation through atoms.

---

## Concept

### Why drones fly: the physics foundation

Everything a multirotor does follows from one relationship: thrust must
exceed weight for sustained flight, and differential thrust between motors
creates rotation. Before touching any libdrone hardware, a student should
own this foundation.

Start with the forces: → [[lift-and-thrust]] explains how a propeller produces
thrust, why thrust scales with RPM squared, and why doubling the payload
requires 2.8× the power. → [[six-degrees-of-freedom]] maps the six axes of
motion (three translational, three rotational) to the control inputs that
produce them. → [[hover-and-forward-flight]] shows how those forces combine in
steady-state flight and what changes when you add forward speed.

The dynamics of what a drone does between inputs — inertia, stopping distance,
pendulum stability — are not obvious and cause real pilot errors until they
are understood. → [[inertia-and-stopping]] covers why a moving drone does not
stop instantly and how to anticipate it. → [[pendulum-stability]] explains why
centre-of-gravity matters for both flight quality and payload placement.
→ [[vortex-ring-state]] is the failure mode that catches pilots who descend
too quickly — understanding it is a safety prerequisite.

### How the control system works

Physics gives us a drone that could fly. A control system makes it fly
stably. → [[closed-loop-control]] introduces the feedback loop concept: the
system measures its state, compares it to the desired state, and applies
corrections. This is the foundation of all stable flight.

The PID controller is the specific implementation. Three terms, each
addressing a different aspect of error: → [[pid-proportional-term]] responds
to the size of the current error. → [[pid-derivative-term]] responds to how
fast the error is changing — this is what prevents overshoot and why the
D-term is sensitive to noise. → [[pid-integral-term]] accumulates error over
time and eliminates steady-state drift. → [[feed-forward-control]] anticipates
the input rather than reacting to it — reducing the lag inherent in reactive
control.

Noise is the central challenge for the D-term. The gyroscope captures both
real attitude changes and mechanical vibration from motors at hundreds of
hertz. → [[propeller-balance]] is the mechanical prerequisite — a balanced prop reduces the noise that the RPM filter must remove. → [[resonance-filtering]] explains the frame resonance physics that determines where notch filters must be placed, and why the RPM filter is more effective than static notches. → [[rpm-filter]] explains the breakthrough that made modern FPV drones
tunable: by knowing the exact motor RPM from bidirectional DShot telemetry,
the flight controller places notch filters precisely at the motor harmonics
in real time, removing the noise without sacrificing responsiveness.

### Propulsion: where power becomes motion

The motor converts electrical energy into mechanical rotation.
→ [[thrust-to-weight-ratio]] translates motor thrust and frame weight into the ratio that determines hover throttle, wind resistance ceiling, and minimum safe T:W for Autotune. → [[brushless-motors]] covers the KV rating, pole count, and why the
relationship between motor speed and voltage is linear. → [[propellers]]
explains pitch, diameter, and the efficiency-versus-thrust tradeoff —
why a larger, slower-turning propeller is more efficient than a small,
fast one at the same thrust. → [[electronic-speed-controllers]] bridges the
digital DShot protocol from the flight controller to the three-phase AC
that drives the motor. → [[dshot-protocol]] covers the specific digital motor
protocol and why bidirectional telemetry (eRPM reporting back to the FC)
enables the RPM filter.

The angular momentum of counter-rotating propellers is what makes yaw control
possible without a tail rotor: → [[angular-momentum-multirotors]] explains
why differential drag torque between pairs of co-rotating and counter-rotating
motors produces yaw.

### Power: the energy budget

Every flight is a race against the battery's capacity. → [[lipo-batteries]]
covers the 6S lithium polymer chemistry, C-rating, why cell count determines
voltage and therefore motor power ceiling, and the handling discipline that
prevents thermal runaway. → [[power-rail-architecture]] maps how voltage
flows from the XT60 connector through the ESC to the motors, the BEC to the
flight controller, and the buck converter to the video system.
→ [[voltage-regulation]] explains why the flight controller needs regulated
5V while the motors want raw battery voltage, and how the two rails are kept
independent.

### Sensors: how the drone knows where it is

The flight controller's sensor suite is what enables stabilised flight and
GPS navigation. → [[imu-gyroscope]] covers the MEMS gyroscope at the heart
of the IMU — how it measures rotation rate using the Coriolis effect, why
it samples at 6400 Hz, and why the IMU chip on the H7A3-SLIM sits in a
physical "moat" cut into the PCB. → [[imu-filter-tuning]] connects the sensor
data to the filter pipeline. → [[gnss-gps]] explains the constellation approach
(GPS + Galileo + BeiDou, GLONASS disabled), EGNOS augmentation, and why
satellite count gates GPS Rescue arming. → [[barometer-magnetometer]] covers
altitude hold and heading — and why the compass is mounted at the nose.

### Structure and materials

The frame must be stiff enough to give the gyroscope a clean signal, light
enough to fly efficiently, and able to survive crashes without destroying
the electronics. → [[sandwich-structure]] explains the five-layer PETG-PCCF
composite and why this combination outperforms pure carbon or pure polymer
frames for the community builder use case. → [[failure-hierarchy]] is the
design principle: crash energy is deliberately routed to the arm shaft first,
protecting the electronics stack. → [[vibration-isolation-theory]] explains
why floating motor mounts with silicone O-ring isolators are the primary
defence against gyroscope noise. → [[arm-shaft]] covers the T-lock system
that makes field arm replacement possible in under five minutes.

### Signal integrity and electromagnetic compatibility

A drone packs high-current switching sources (ESC at 48 kHz, buck converter
at 180 kHz) and sensitive measurement devices (gyroscope, GPS, receiver)
into a volume of centimetres. → [[emc-noise-sources]] maps the electromagnetic
threat landscape. The mitigations are layered: → [[twisted-pairs]] for motor
phase wires, → [[star-grounding]] to eliminate ground loops, → [[capacitor-placement-emc]]
for the decoupling capacitors that must be directly on the ESC pads,
→ [[power-signal-separation]] for the three-zone routing enforced by the
Platform geometry, → [[ferrite-beads]] on the VTX power wire.

---

## Reference

### Atom index by topic

| Domain | Key articles |
|---|---|
| Physics | [[lift-and-thrust]], [[six-degrees-of-freedom]], [[hover-and-forward-flight]], [[inertia-and-stopping]], [[pendulum-stability]], [[vortex-ring-state]], [[angular-momentum-multirotors]] |
| Control | [[closed-loop-control]], [[pid-proportional-term]], [[pid-derivative-term]], [[pid-integral-term]], [[feed-forward-control]], [[rpm-filter]] |
| Propulsion | [[brushless-motors]], [[propellers]], [[electronic-speed-controllers]], [[dshot-protocol]] |
| Power | [[lipo-batteries]], [[power-rail-architecture]], [[voltage-regulation]] |
| Sensors | [[imu-gyroscope]], [[imu-filter-tuning]], [[gnss-gps]], [[barometer-magnetometer]] |
| Structure | [[sandwich-structure]], [[failure-hierarchy]], [[arm-shaft]], [[cf-rod-architecture]], [[vibration-isolation-theory]], [[floating-motor-mounts]] |
| EMC | [[emc-noise-sources]], [[twisted-pairs]], [[star-grounding]], [[capacitor-placement-emc]], [[power-signal-separation]], [[ferrite-beads]] |
| Software | [[betaflight-setup]], [[betaflight-gps-rescue]], [[pid-tuning-rate-profile]] |

---

## Procedure

### Recommended reading sequence

For a student approaching drone engineering for the first time:

1. [[lift-and-thrust]] → [[six-degrees-of-freedom]] → [[hover-and-forward-flight]]
2. [[closed-loop-control]] → [[pid-proportional-term]] → [[pid-derivative-term]] → [[pid-integral-term]]
3. [[rpm-filter]] → [[imu-gyroscope]] → [[imu-filter-tuning]]
4. [[brushless-motors]] → [[propellers]] → [[electronic-speed-controllers]] → [[dshot-protocol]]
5. [[lipo-batteries]] → [[power-rail-architecture]]
6. [[sandwich-structure]] → [[failure-hierarchy]] → [[floating-motor-mounts]]
7. [[emc-noise-sources]] → [[twisted-pairs]] → [[star-grounding]]

For a workshop participant needing a 2-hour pre-read before the build session:
Read sections 1–3 of Concept above, then [[lipo-batteries]] and [[failure-hierarchy]].

---

### Structural engineering: why the frame is designed the way it is

The PID and propulsion sections explain how the drone flies. This section
explains why it holds together — and why it fails predictably rather than
catastrophically when it does not.

The foundational principle is → [[failure-hierarchy]]: the arm is the
cheapest component in the crash energy path, so it is the one that breaks
first. This is not an accident — it is the crumple zone philosophy applied
to drone frames. A frame that always breaks the arm protects the electronics
stack behind it. A frame with uniform strength breaks unpredictably.

→ [[zonal-stiffness]] explains how deliberately different stiffness values
in different zones route crash energy to the sacrificial arm. The body
sandwich (PCCF layers) is stiff; the arms (PETG) are compliant; the
transition point between them is the designed failure location.

The body itself is a → [[sandwich-structure]] — two stiff face sheets
(PCCF) separated by a core (PETG), behaving as a → [[monocoque-structure]]
that carries loads through its skin rather than an internal skeleton. The
second moment of area is what gives the sandwich panel its bending
resistance, not its mass.

Two structural principles govern how the components connect:

→ [[pre-tensioning]]: the CF rod channels are designed 0.1–0.15mm smaller
than the rod diameter. Pressing the rod in deforms the printed channel
elastically, creating a clamping force before any flight load is applied.
This passive pre-load eliminates micro-slip at the joint under vibration —
the same principle as a properly torqued bolt versus a finger-tight one.

→ [[exact-constraint-design]]: each degree of freedom in every joint is
constrained exactly once. Over-constraint introduces internal stress from
manufacturing tolerance mismatches and cracks printed parts. The T-slot
tab system locates the arm laterally but lets it float axially — deliberately
under-constrained in the assembly direction to accommodate real-world
print tolerances.

Understanding these principles is what allows a builder to diagnose a
structural problem. A crack at the arm-body joint that was not caused by
a crash is over-constraint. A joint that loosens under vibration has
insufficient pre-tension. The failure tells you which principle was violated.


## Rationale

Engineering Principles 101 exists because the individual atoms are too granular
for a student encountering drone engineering for the first time. The student
needs a narrative arc that places each concept in context before they encounter
the technical depth. This skeleton provides that arc while keeping all
specification content in the atoms — where it can be maintained and corrected
in one place.

---

## Connections

requires: []
related:
  - [[sk-electronics-deep-dive]]
  - [[sk-complete-build-guide]]
leads_to:
  - [[sk-complete-build-guide]]
  - [[sk-electronics-deep-dive]]
