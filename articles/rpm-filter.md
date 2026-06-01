---
id: rpm-filter
title: "RPM filter"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - control-systems
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

The RPM filter is Betaflight's primary gyroscope noise rejection system. It
uses the actual motor RPM — measured every PID loop cycle via bidirectional
DShot telemetry — to place narrow notch filters precisely at the motor
fundamental frequency and its harmonics, removing motor vibration noise
from the gyro signal while leaving attitude signal untouched. On libdrone's
H7A3-SLIM running at 8 kHz, the filter simultaneously tracks 36 notch filter
positions (4 motors × 3 harmonics × 3 axes), updated every 125 µs. The result
is a cleaner gyro signal at lower latency cost than any fixed-frequency
filtering approach.

---

## Concept

### The problem with fixed-frequency filters

Before the RPM filter, gyroscope noise was addressed using fixed low-pass
filters: remove all signal above a chosen cutoff frequency. This eliminates
motor noise (typically 300–800 Hz) but also removes real attitude signal
above the cutoff. Every 10 Hz of cutoff reduction adds measurable phase lag
to the control loop — the flight controller sees attitude changes later than
they happen. Aggressive filtering for noisy builds produced sluggish,
unresponsive drones.

The fundamental problem: motor noise frequency changes with throttle.
At 20,000 RPM the fundamental is 333 Hz. At 35,000 RPM it is 583 Hz.
A fixed notch filter at 400 Hz catches the noise at one throttle level
and misses it at another. A broad low-pass filter catches it everywhere
but at the cost of latency across the whole spectrum.

### How the RPM filter solves this

Bidirectional DShot makes each ESC report the motor's exact eRPM to the
flight controller every PID cycle. The RPM filter uses this real-time RPM
data to calculate the current fundamental frequency of each motor:

    fundamental_Hz = (eRPM / pole_pairs) / 60
                  = mechanical_RPM / 60

It then places notch filters at the fundamental and its harmonics (2× and
3× the fundamental), tracking them continuously as throttle changes. When
a motor changes speed, the notch filters follow within one PID cycle (125 µs).

The notch filters are narrow — they remove only a few Hz of bandwidth around
each motor frequency. Everything else, including real attitude dynamics below
100 Hz, passes through untouched. The phase lag introduced by narrow notch
filters is negligible compared to a broad low-pass filter achieving the same
noise rejection.

### The computational requirement

36 notch filter positions, updated every 125 µs:
- 4 motors
- 3 harmonics per motor (fundamental, 2nd, 3rd)
- 3 gyroscope axes (roll, pitch, yaw)
- Updated at 8,000 Hz

This is why the H7A3 (Cortex-M7, 280 MHz) was selected for libdrone. Earlier
F4-class flight controllers could run the PID loop at 8 kHz but ran out of
processing headroom before the RPM filter computation could be added. The
H7 runs both simultaneously with substantial CPU headroom remaining.

### The dynamic notch filter

On top of the RPM filter, Betaflight runs a dynamic notch filter that analyses
the gyro frequency spectrum in real time, identifies high-amplitude noise peaks
not accounted for by motor frequencies, and places additional notch filters
there. This catches frame structural resonances, aerodynamic turbulence peaks,
and any other persistent noise sources.

The RPM filter and dynamic notch filter work together: RPM filter handles
predictable, calculated motor noise; dynamic notch handles anything
unpredictable that appears in the actual spectrum.

---

## Reference

### RPM filter dependencies

| Requirement | Detail |
|---|---|
| Bidirectional DShot | Must be enabled in Betaflight AND ESC firmware |
| ESC firmware | AM32 with BiDi DShot support (confirmed for Pilotix 75A AM32) |
| FC processor | H7 class or equivalent (F4 cannot sustain 8 kHz + RPM filter) |
| Motor pole count | Must be set correctly in Betaflight for eRPM→RPM conversion |

### libdrone V2.4.6 RPM filter configuration

| Parameter | Value |
|---|---|
| Loop rate | 8 kHz |
| Gyro rate | 8 kHz |
| RPM filter harmonics | 3 per motor |
| Total notch filter positions | 36 (4 motors × 3 harmonics × 3 axes) |
| Motor pole count (2507) | 14 poles = 7 pole pairs |

### Verifying RPM filter is working

1. In Betaflight Motors tab: spin up all four motors to ~30% throttle with
   props removed. All four should report eRPM values that are non-zero and
   proportional to commanded speed.
2. In Betaflight Blackbox Explorer: after a flight, view the gyro spectrum.
   The characteristic motor frequency peaks (fundamental + harmonics) should
   be largely absent. Residual peaks indicate the filter is not fully effective —
   check BiDi DShot is enabled in both FC and ESC configuration.

---

## Procedure

### Enabling RPM filter on libdrone H7A3-SLIM

1. In ESC configurator (AM32 Configurator or BLHeli Suite): enable bidirectional
   DShot on all four ESC outputs.
2. In Betaflight Configurator → Configuration tab: set Motor Protocol to
   DShot600, enable Bidirectional DShot.
3. In Betaflight CLI: `set motor_poles = 14` (for the BrotherHobby 2507).
4. Save and reboot.
5. Verify in Motors tab: all four motors show eRPM when spun up (props removed).
6. In Betaflight Filtering tab: RPM filter should show as enabled with 3 harmonics.

---

## Rationale

### Why this article lives in control-systems and not software-stack

The RPM filter is a control system concept — it is a real-time adaptive
notch filter that makes PID tuning possible on noisy airframes. Understanding
what it does (track motor noise and remove it surgically) is essential for
understanding why the D term can be set higher than on pre-RPM-filter drones,
why BiDi DShot is required, and why the H7 processor matters. The Betaflight
configuration steps belong in the software-stack domain. The concept belongs here.

---

## Connections

requires:
  - [[closed-loop-control]]
  - [[pid-derivative-term]]
  - [[resonance-filtering]]
related:
  - [[vibration-isolation-theory]]
  - [[floating-motor-mounts]]
leads_to:
  - [[imu-filter-tuning]]


[closed-loop-control]: closed-loop-control.md "Closed-loop control"
[pid-derivative-term]: pid-derivative-term.md "PID — derivative term"
[resonance-filtering]: resonance-filtering.md "Resonance and filtering"
[vibration-isolation-theory]: vibration-isolation-theory.md "Vibration isolation theory"
[floating-motor-mounts]: floating-motor-mounts.md "Floating motor mounts"
[imu-filter-tuning]: imu-filter-tuning.md "IMU filter tuning"
