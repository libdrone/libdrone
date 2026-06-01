---
id: vibration-isolation-theory
title: "Vibration isolation theory"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - frame-structure
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

Motor vibration propagates through a rigid frame into the IMU where it appears
as noise indistinguishable from genuine aircraft motion. The flight controller
cannot separate the two and attempts to correct for both — degrading control
quality and demanding aggressive software filtering that adds control loop
latency. A mechanical isolator inserted between the motor and the frame creates
a low-pass filter in the structural path: vibration above the isolator's
resonance frequency is attenuated before reaching the IMU. This article explains
the physics of structural vibration propagation and mechanical isolation. For
the libdrone implementation see [[floating-motor-mounts]].

---

## Concept

### Vibration sources in a multirotor

A brushless motor produces vibration at several frequencies simultaneously:

- **Motor fundamental frequency:** one vibration cycle per revolution.
  At 20,000 RPM = 333 Hz. At 40,000 RPM = 667 Hz.
- **Blade passage frequency:** for a 3-blade prop, three pulses per revolution.
  At 20,000 RPM = 1000 Hz.
- **Harmonics:** integer multiples of the above, extending to several kHz.
- **Bearing noise:** broadband, centred around bearing resonance (typically
  1–5 kHz for small brushless motors).

On a rigid connection between motor and frame, all of these propagate with
minimal attenuation. The IMU's gyroscope samples angular velocity typically
at 8 kHz or higher — it captures the full spectrum.

### How vibration degrades flight control

The gyroscope samples the sum of genuine aircraft motion and structural
vibration. At 1000 Hz blade passage the gyroscope sees a 1000 Hz signal
component that looks identical to very rapid angular oscillation. The flight
controller's PID loop treats it as real and generates a corrective motor command
— which itself creates additional vibration. The system enters a self-exciting
oscillation loop.

Software filters (dynamic notch filter, RPM filter, low-pass filters on
gyroscope output) are designed to remove these frequency components. However,
every filter introduces phase lag — a delay between when the real motion occurs
and when the flight controller sees it. High phase lag means slow loop response:
the drone reacts sluggishly to disturbances and pilot inputs.

The fundamental trade-off: more aggressive filtering → less vibration noise →
more phase lag → slower loop response. Mechanical isolation before the signal
reaches the gyroscope reduces the noise floor, allowing less aggressive filtering
and lower phase lag for equivalent noise rejection.

### Mechanical low-pass filter model

A spring-mass-damper system has a characteristic resonance frequency:

    f₀ = (1 / 2π) × √(k / m)

Where:
- `k` = spring stiffness (N/m) — set by isolator Shore hardness and geometry
- `m` = mounted mass (kg) — the motor mass
- `f₀` = resonance frequency (Hz)

Below `f₀`: vibration passes through with amplitude gain (near resonance) or
unity gain (well below resonance).

Above `f₀`: vibration is attenuated. A simple spring-mass system attenuates
at 40 dB/decade (−40 dB per 10× frequency increase). With damping added
(viscoelastic material), resonance amplitude is suppressed and attenuation
above resonance is approximately 20–40 dB/decade depending on damping ratio.

For effective isolation, `f₀` must be well below the lowest motor operating
frequency. If a motor operates from 5,000–40,000 RPM (83–667 Hz), the isolator
resonance should be below approximately 50 Hz. This requires a combination of
low stiffness (soft silicone) and sufficient mounted mass.

### Viscoelastic isolators

Rubber and silicone are viscoelastic: their deformation has both elastic
(spring-like, energy-storing) and viscous (damping, energy-dissipating)
components. The ratio of these components determines the damping ratio ζ.

High ζ (over-damped): resonance amplitude is suppressed but attenuation above
resonance is reduced. Good for eliminating resonance peaks.

Low ζ (under-damped): higher resonance amplitude but steeper roll-off above
resonance. Can amplify vibration at frequencies near `f₀`.

Silicone isolators for motor mounts are designed with moderate damping (ζ ≈ 0.3–0.6)
to suppress the resonance amplitude while maintaining useful attenuation slope
above `f₀`.

### Shore hardness and its effect

Shore A hardness is a surface indentation measure that correlates with stiffness
`k`. For a given isolator geometry:

- Higher Shore A → higher `k` → higher `f₀` → less effective isolation at
  lower frequencies.
- Lower Shore A → lower `k` → lower `f₀` → better isolation but more compliance
  (motor positional stability reduced).

Two isolator elements in the floating mount system serve different functions
and have different Shore specifications:

- **O-rings (40–50A):** carry compressive load from motor weight and thrust
  reaction. Firmer durometer prevents motor sag under sustained thrust.
- **Sleeves (30–40A):** provide radial isolation at the bolt shaft. Softer
  durometer gives more compliance in the radial direction where motor
  vibration is highest.

### Temperature dependence

Silicone Shore hardness is relatively stable across a wide temperature range,
but does increase at low temperatures. Standard silicone shows significant
stiffening below 0°C, raising `f₀` and reducing isolation effectiveness
in cold weather. VMQ (vinyl methyl silicone) maintains more consistent Shore
hardness from −50°C to +200°C and is specified for this reason in libdrone's
floating mount. → See [[floating-motor-mounts]] §Rationale.

### Isolation vs decoupling

A mechanical isolator does not eliminate the connection between motor and frame
— it changes the character of the connection from rigid to compliant. The motor
is still attached. Forces at frequencies below `f₀` still propagate. The
isolator is not perfect.

For the residual vibration that passes the mechanical filter, software filters
act as a second stage. The two stages address different frequency regions:
mechanical isolation handles the high-amplitude fundamental and low harmonics;
software filters handle the residual and higher-frequency components. Together
they achieve lower total gyroscope noise than either could alone.

---

## Reference

### Isolation effectiveness (approximate, single-axis model)

| Frequency relative to f₀ | Transmissibility |
|---|---|
| 0.1 × f₀ | ~1.0 (passes through) |
| 0.5 × f₀ | ~1.1–1.3 (slight amplification) |
| 1.0 × f₀ (resonance) | 2–10× (amplification — must not coincide with motor operating range) |
| 2 × f₀ | ~0.3–0.5 (30–50% attenuation) |
| 5 × f₀ | ~0.05–0.1 (90–95% attenuation) |
| 10 × f₀ | ~0.01–0.03 (97–99% attenuation) |

Values are approximate and depend on damping ratio. Real isolators deviate
from the ideal model, particularly at high frequencies where mass and stiffness
of the isolator itself introduce secondary resonances.

### Blackbox indicators of vibration issues

| Symptom | Probable cause |
|---|---|
| High-frequency noise band on all axes (250–700 Hz) | Motor fundamental / blade passage reaching IMU |
| Narrow spike at specific RPM | Resonance near motor operating frequency |
| Noise increases with throttle | Mechanical isolation bypassed (direct contact, worn isolators) |
| Noise present at idle, not correlated with RPM | Airframe resonance from external excitation |

---

## Procedure

<!-- not applicable — this is a theory article. For the implementation procedure
see floating-motor-mounts § Procedure. -->

---

## Rationale

### Why this article exists separately from floating-motor-mounts

The implementation article ([[floating-motor-mounts]]) tells a builder what to do:
which O-rings, which torque, which lubricant. This article tells a student or
contributor *why* it works: the physics of vibration propagation, the spring-mass
model, the frequency domain behaviour. Separating them follows the atom boundary
rule — the implementation article links here for depth without repeating
the physics. A builder does not need the spring-mass model to assemble the mount;
a student studying drone control systems does not need the part numbers to
understand isolation.

---

## Connections

requires: []
related:
  - [[floating-motor-mounts]]
  - [[imu-filter-tuning]]
  - [[pid-tuning-rate-profile]]
  - [[resonance-filtering]]
leads_to:
  - [[floating-motor-mounts]]
  - [[resonance-filtering]]


[floating-motor-mounts]: floating-motor-mounts.md "Floating motor mounts"
[imu-filter-tuning]: imu-filter-tuning.md "IMU filter tuning"
[pid-tuning-rate-profile]: pid-tuning-rate-profile.md "PID tuning and rate profile"
[resonance-filtering]: resonance-filtering.md "Resonance and filtering"
