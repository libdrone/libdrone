---
id: jello-effect-mitigation
title: "Jello effect mitigation"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - aerial-imaging
personas:
  - 5.student
  - 2.operator
  - 1.builder
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Jello effect in drone video is caused by rolling shutter reading successive
pixel rows at slightly different moments while the camera vibrates. The fix
is to reduce vibration amplitude at the camera before it reaches the sensor.
The mitigation hierarchy follows the same principle as all vibration control:
eliminate at source first (prop balance), then isolate (floating motor mounts),
then filter in software (gyroflow stabilisation). Each layer addresses a
different frequency range. All three layers working together produce footage
clean enough for professional use from a non-gimbal platform.

---

## Concept

### Rolling shutter and why jello appears

A global-shutter sensor reads all pixels at exactly the same instant — a
perfect snapshot. A rolling-shutter sensor (used in nearly all small cameras
and drones) reads pixel rows sequentially: row 1, then row 2, then row 3...
all the way to the last row. The time to read a full frame might be 1/1000 s.
If the camera is vibrating during that readout, row 500 is captured with
the camera at a slightly different position than row 1.

The result: horizontal lines in the image are displaced relative to each
other, creating the characteristic wobbly distortion. A stationary scene
appears to wriggle; a straight propeller tip traces a wobbly arc.

At typical drone vibration frequencies (300–600 Hz), the readout time per row
(approximately 15–30 µs for a typical 1080p sensor) captures the camera at
meaningfully different positions on each row, producing visible jello.

### The mitigation hierarchy

**Layer 1 — Prop balance (eliminate at source)**

An unbalanced propeller vibrates at its rotation frequency (300–600 Hz at
operational RPM). This is the highest-amplitude single-frequency vibration
source. Three minutes of magnetic prop balancing before the first flight
of the day reduces this dramatically. Measure before and after with
Blackbox — the noise floor change at motor fundamental frequency is visible.

**Layer 2 — Floating motor mounts (mechanical isolation)**

O-ring isolators between motor and arm provide approximately 10–20 dB of
attenuation at motor vibration frequencies. This is the primary structural
defence against jello. Worn or missing O-rings eliminate this protection.
Inspect at every pre-flight. Replace on schedule (every 20–30 flight hours)
or whenever cracked/flattened.

**Layer 3 — Camera mounting (soft mount the camera)**

If the camera is rigidly mounted to the airframe, all residual vibration
that passes through the motor mounts reaches the camera directly. Mounting
the camera on a soft pad (foam, silicone, or TPU printed dampers) adds a
second mechanical isolation stage specifically at the camera. For fixed
cameras without a gimbal, this is the highest-impact single change.

On libdrone's GPS/camera bracket, the HDZero camera mounts in a PETG slot.
Adding a thin layer of anti-vibration foam between camera body and slot wall
provides additional damping at minimal mass cost.

**Layer 4 — Software stabilisation (remove residual)**

Post-processing software (Gyroflow, DaVinci Resolve stabiliser) analyses
the video and gyroscope data together to warp each frame, correcting for
camera movement during the exposure. Gyroflow is particularly effective
because it uses the actual IMU gyroscope data from Blackbox to compute the
correction precisely rather than estimating it from the video content alone.

Software stabilisation crops the image (to allow warping room) and cannot
fix jello caused by very high-frequency vibration (above the gyroscope's
useful bandwidth). It is the final layer, not a substitute for the mechanical
layers.

---

## Reference

### Jello mitigation effectiveness (approximate, cumulative)

| Layer | Technique | Jello reduction |
|---|---|---|
| 0 (baseline) | No mitigation | — |
| 1 | Balanced props | 40–60% reduction |
| 1+2 | Balanced props + good O-rings | 70–85% reduction |
| 1+2+3 | + soft camera mount | 85–95% reduction |
| 1+2+3+4 | + Gyroflow post-processing | 95–99% reduction |

These are representative values — actual results depend on specific platform,
vibration frequency profile, and camera model.

### Gyroflow integration with libdrone

Gyroflow works best with synchronised IMU data. To use Gyroflow with libdrone:

1. Enable Blackbox at maximum rate (`blackbox_rate_denom = 1`).
2. In Gyroflow: import the video file and the Blackbox log from the same flight.
3. Sync: align the gyro data with the video using motion matching or manual
   sync markers (a sharp movement visible in both the video and the gyro trace).
4. Apply correction. Gyroflow warps each frame based on the actual measured
   camera movement.

The Matek H7A3-SLIM's IMU (ICM-42688-P) is well-characterised in Gyroflow's
lens/IMU database.

---

## Procedure

### Checking jello level after build changes

Any change to the motor mounts, motors, or propellers should be followed by
a jello check:

1. Fly a slow (< 3 m/s) lateral pass over a flat, textured surface (grass,
   pavement, roof tiles).
2. Review the footage frame-by-frame. Look for horizontal waviness in what
   should be straight lines (pavement cracks, fence posts).
3. Check the Blackbox gyro spectrum simultaneously — peaks at motor RPM
   harmonics correlate with jello.
4. If jello has increased: check prop balance, check O-ring condition, check
   that the passive cover is not touching the arm head surface directly.

---

## Rationale

### Why all four layers are needed rather than relying on software alone

Software stabilisation is tempting as a complete solution — add Gyroflow and
forget mechanical mitigation. This fails in practice for two reasons:

First, software stabilisation crops the image. On a narrow-FOV FPV camera,
a 10–15% crop can eliminate context that is part of the shot. The more
residual jello, the more aggressive the crop needed to remove it.

Second, very high-frequency jello (frame-to-frame row displacement at 600 Hz)
introduces artefacts that software cannot remove because the gyroscope samples
at 8 kHz but the correction is applied per-frame (at 30–60 Hz). Software
stabilisation corrects frame-level motion, not within-frame row displacement.
Mechanical mitigation is the only path to eliminating within-frame distortion.

---

## Connections

requires:
  - [[aerial-imaging-basics]]
  - [[floating-motor-mounts]]
  - [[vibration-isolation-theory]]
related:
  - [[pid-tuning-rate-profile]]
  - [[blackbox-analysis]]
leads_to:
  - [[survey-imaging]]
