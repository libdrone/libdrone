---
id: imu-gyroscope
title: "IMU and gyroscope"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - sensors-fc
personas:
  - 5.student
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The gyroscope is the sensor that closes the innermost flight control loop. It
measures the rotation rate of the airframe on three axes — roll, pitch, yaw —
delivering new readings at up to 32,000 times per second. The MEMS gyroscope
works using the Coriolis effect: a microscopic proof mass driven to oscillate
at a known frequency deflects perpendicular to its oscillation when the chip
rotates, and that deflection is proportional to rotation rate. The gyro cannot
distinguish genuine rotation from vibration — both look identical in the sensor
output — which is why motor vibration filtering is not optional. The
accelerometer in the same IMU package measures the specific force (gravity
plus linear acceleration) needed for level sensing and GPS-assisted modes.

---

## Concept

### MEMS gyroscope — how it works

Inside the ICM-42688-P, a microscopic proof mass (a few micrograms of etched
polysilicon) is driven to oscillate at a precisely controlled resonant frequency
— typically 20–40 kHz — by electrostatic actuation. When the chip rotates,
the Coriolis force deflects the oscillating mass perpendicular to both its
oscillation axis and the rotation axis. A capacitive sense element measures
this deflection. The deflection magnitude is proportional to rotation rate.

The Coriolis effect is the physical basis of all MEMS gyroscopes. It is the
same effect that causes hurricanes to spiral as air moves toward the equator
in the Earth's rotating reference frame. In the gyroscope, the rotating
reference frame is the chip itself.

The genius of using the Coriolis effect is that measurement is self-referencing.
The drive frequency is precisely controlled; the sense measurement is
synchronously demodulated at that same frequency. Environmental vibration at
different frequencies is rejected by this demodulation. This is why MEMS
gyroscopes can measure rotation in the presence of motor vibration — the motor
vibration is at different frequencies than the drive frequency and is naturally
rejected.

However, vibration at or near the drive frequency does contaminate the output.
And more practically: vibration at flight-relevant frequencies (100–2000 Hz)
generates gyro output that is indistinguishable from real rotation at those
frequencies. The gyro samples rotation rate — it cannot know whether the rate
change came from the aircraft moving or from the frame vibrating.

### Gyro output data rate

The ICM-42688-P outputs data at up to 32,000 Hz (ODR 32 kHz). Betaflight
samples this at 8 kHz — one reading every 125 µs. The gyro data arrives via
SPI at ~10 MHz; a DMA transfer reads 16 bytes in ~13 µs without CPU involvement.

### The accelerometer

The accelerometer in the same IMU chip measures specific force — the sum of
all non-gravitational forces per unit mass. In steady hover, specific force
is approximately 1g pointing downward (opposing gravity). The accelerometer
tells the FC which direction is "down" — essential for self-leveling (angle
mode) and for the GPS-assisted modes that need an absolute attitude reference.

In rate (manual) mode, the accelerometer is largely irrelevant — the FC tracks
attitude by integrating gyro rate. Over time, gyro drift accumulates, but in
the seconds-to-minutes typical flight duration this error is small enough to
be managed by I-term correction.

In angle mode or GPS hold, the accelerometer provides the gravity reference
that prevents accumulated gyro drift from giving a wrong "down" direction.

### Noise sources that contaminate gyro output

Real attitude signal occupies 0–100 Hz for any realistic flight manoeuvre.
Everything above ~100 Hz is noise. Sources:

| Source | Frequency range | Mechanism |
|---|---|---|
| Propeller imbalance | Motor RPM in Hz (e.g. 500 Hz at 30,000 RPM) | Mass asymmetry → rotating centrifugal force |
| Motor commutation | RPM × pole_pairs ÷ 60 (e.g. 3,500 Hz) | Electromagnetic torque ripple |
| Frame resonance | 100–300 Hz (PCCF/PETG frame) | Structural modes excited by motor vibration |
| ESC switching | 48,000 Hz + harmonics | EMC coupling onto gyro supply |

The D term amplifies high-frequency noise. Every noise source above therefore
contributes to motor command noise via the D term unless filtered.

---

## Reference

### ICM-42688-P key parameters

| Parameter | Value |
|---|---|
| Gyro full-scale range | ±250 to ±2000 °/s (configurable) |
| Gyro noise density | 2.8 mdps/√Hz (typical) |
| Output data rate | Up to 32,000 Hz |
| Interface | SPI at up to 24 MHz |
| Accelerometer range | ±2 to ±16g (configurable) |
| Package | 3 × 3 mm |
| Betaflight default ODR | 8 kHz |

### Filter chain (Betaflight)

    Raw gyro (8 kHz) → RPM filter (36 notch positions) →
    Dynamic notch filter (3 notches per axis) →
    Gyro lowpass filter 1 (static PT1/Biquad) →
    Gyro lowpass filter 2 (static PT1/Biquad) →
    D-term lowpass filter →
    PID calculations

Each filter stage removes a class of noise at the cost of some phase lag.
The RPM filter contributes least phase lag per noise rejection because its
notches are narrow. Static lowpass filters contribute the most. Minimising
the number and aggression of static filters while relying on RPM + dynamic
notch filtering is current best practice. → See [[imu-filter-tuning]].

---

## Procedure

<!-- not applicable — filter configuration procedure is in imu-filter-tuning -->

---

## Rationale

### Why the gyro is on a PCB moat

Frame vibration enters the FC through the mounting screws. A rigid PCB transmits
this vibration directly to the IMU. The moat (a slot cut around the IMU island)
mechanically decouples the IMU mounting point from the screw mounting points.
Vibration must travel around the moat, attenuating significantly. Combined with
the nylon standoffs (which further attenuate transmission from the ESC to the FC),
two stages of mechanical isolation precede the software filtering chain.

---

## Connections

requires:
  - [[closed-loop-control]]
related:
  - [[flight-controller-hardware]]
  - [[vibration-isolation-theory]]
  - [[rpm-filter]]
leads_to:
  - [[imu-filter-tuning]]
  - [[rpm-filter]]


[imu-filter-tuning]: imu-filter-tuning.md "IMU filter tuning"
[closed-loop-control]: closed-loop-control.md "Closed-loop control"
[flight-controller-hardware]: flight-controller-hardware.md "Flight controller hardware"
[vibration-isolation-theory]: vibration-isolation-theory.md "Vibration isolation theory"
[rpm-filter]: rpm-filter.md "RPM filter"
