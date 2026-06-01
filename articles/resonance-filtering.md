---
id: resonance-filtering
title: "Resonance and filtering"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: generic
topic:
  - software-stack
personas:
  - 5.student
  - 1.builder
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Every drone frame has mechanical resonant frequencies — specific frequencies
at which it vibrates with amplified amplitude when excited. When propeller
and motor rotation frequencies sweep through a frame's resonant frequency,
vibration amplitude spikes. This spike couples into the IMU as apparent
rotation, causing the flight controller to command incorrect motor corrections
that amplify the vibration further — a positive feedback loop. The RPM filter
and notch filters in Betaflight and ArduPilot break this loop by removing
the resonant frequency from the gyroscope signal before it reaches the PID
controller. Understanding the resonance mechanism determines which filter
to apply and where to set it.

---

## Concept

### Mechanical resonance in frames

Every physical structure has one or more natural (resonant) frequencies
determined by its mass distribution and stiffness. When an external force
oscillates at this frequency, the structure absorbs energy efficiently and
vibration amplitude grows — the same principle as pushing a swing at its
natural pendulum frequency. At other frequencies, energy is not absorbed
efficiently and amplitude remains small.

For a drone frame, the resonant frequencies are typically in the range
80–400 Hz. A PETG frame with 3 mm CF rods has different resonant frequencies
from a PC-CF frame — stiffer material shifts resonant frequencies upward.
Adding mass (battery, payload) shifts them downward. The resonant frequencies
of a specific build can only be measured, not reliably predicted from
material properties alone.

### The motor RPM sweep problem

Motor RPM is not constant — it varies with throttle from near-zero at idle
to maximum at full throttle. The rotation frequency of the motor (Hz) equals
RPM / 60. The propeller blade-pass frequency equals rotation frequency ×
blade count. These two frequencies and their harmonics (2×, 3×, 4× rotation
frequency) sweep across the full frequency spectrum as the pilot changes throttle.

If any of these swept frequencies coincides with a frame resonant frequency,
vibration spikes at that throttle position. On a blackbox log, this appears
as a sudden increase in gyroscope noise at a specific throttle level — not
a constant noise floor, but a throttle-dependent spike. This is the diagnostic
signature of a resonance problem.

### RPM filter vs static notch filter

Two filter approaches address resonance:

**RPM filter (Betaflight, ArduPilot):** tracks the motor rotation frequency
in real time using bidirectional DShot RPM telemetry, and places a notch
filter at exactly the rotation frequency and its harmonics as they move with
throttle. The filter follows the resonance — wherever RPM goes, the notch goes.
This is the most precise approach but requires bidirectional DShot. See
→ [[rpm-filter]].

**Static notch filter:** a fixed-frequency notch placed at the measured frame
resonant frequency. Does not track with RPM — effective only when the RPM
sweep happens to coincide with the notch frequency. Useful for strong fixed-
frequency resonances (e.g. a frame mode that is always excited regardless of
motor speed) or as a backup when RPM telemetry is unavailable.

### The IMU coupling mechanism

The IMU's accelerometers and gyroscopes are mounted on the flight controller
PCB, which is mounted on the frame via vibration-dampening grommets. Despite
the dampening, high-amplitude frame vibration at the resonant frequency
partially couples into the IMU. The gyroscope reads it as angular rate — the
same signal it reads from actual rotation. The PID controller cannot
distinguish mechanical resonance vibration from commanded rotation and responds
by modulating motor outputs at the resonant frequency, reinforcing the vibration.
Without a notch filter, this loop can grow to the point where the motors
oscillate audibly and the aircraft is uncontrollable.

---

## Reference

**Resonance diagnostic checklist:**

| Symptom | Likely cause |
|---|---|
| Oscillation at specific throttle position | Frame resonance at that RPM harmonic |
| High gyroscope noise floor at all throttle | Unbalanced prop or motor |
| Oscillation at all throttle above threshold | PID gain too high (not resonance) |
| Sudden onset oscillation mid-flight | Loose prop or motor mounting |

**Filter configuration starting points (Betaflight):**

    # RPM filter (requires BiDi DShot)
    rpm_filter_harmonics = 3      ; Filter fundamental + 2 harmonics
    rpm_filter_q = 500            ; Q factor: higher = narrower notch

    # Static notch (if RPM filter unavailable)
    gyro_notch1_hz = 200          ; Measure frame resonance first
    gyro_notch1_cutoff = 170

---

## Procedure

### Identify frame resonant frequency from blackbox

1. Fly a hover, slowly sweeping throttle from 20% to 80% and back.
2. Download blackbox log. Open in Betaflight Blackbox Explorer.
3. Enable spectrum analyser view. Look for frequency peaks that shift
   with throttle (motor harmonics) vs fixed-frequency peaks (frame modes).
4. The fixed-frequency peak is the frame resonant frequency.
5. Set a static notch at ±10% of that frequency, or confirm the RPM filter
   is covering the motor harmonic that excites it.

---

## Rationale

Understanding resonance as the underlying cause — rather than treating filter
settings as magic numbers — allows builders to diagnose novel problems.
A new payload changes the frame mass distribution and shifts the resonant
frequency. A damaged arm changes the stiffness. Both require re-evaluation
of filter settings. Builders who understand the mechanism adjust correctly;
builders who copied filter settings from a build video struggle to understand
why the same settings do not work on their build.

---

## Connections

requires:
  - [[vibration-isolation-theory]]
  - [[imu-gyroscope]]
  - [[rpm-filter]]
related:
  - [[imu-filter-tuning]]
  - [[pid-tuning-rate-profile]]
  - [[propeller-balance]]
  - [[floating-motor-mounts]]
  - [[blackbox-analysis]]
  - [[dshot-protocol]]
leads_to:
  - [[rpm-filter]]
  - [[imu-filter-tuning]]
  - [[pid-tuning-rate-profile]]


[rpm-filter]: rpm-filter.md "RPM filter"
[vibration-isolation-theory]: vibration-isolation-theory.md "Vibration isolation theory"
[imu-gyroscope]: imu-gyroscope.md "IMU and gyroscope"
[imu-filter-tuning]: imu-filter-tuning.md "IMU filter tuning"
[pid-tuning-rate-profile]: pid-tuning-rate-profile.md "PID tuning and rate profile"
[propeller-balance]: propeller-balance.md "Propeller balance"
[floating-motor-mounts]: floating-motor-mounts.md "Floating motor mounts"
[blackbox-analysis]: blackbox-analysis.md "Blackbox analysis"
[dshot-protocol]: dshot-protocol.md "DShot protocol"
