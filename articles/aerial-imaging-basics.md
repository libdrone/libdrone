---
id: aerial-imaging-basics
title: "Aerial imaging basics"
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
  - 3.payload-dev
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Aerial imaging from a multirotor requires managing three compounding sources
of image degradation: platform vibration (causing jello effect), exposure
settings (rolling shutter artefacts at high shutter speeds), and pilot
technique (jerky inputs producing unusable footage). The solution to each
is distinct: vibration is controlled mechanically and by floating motor mounts;
exposure is managed with neutral density (ND) filters and the 180° shutter
rule; technique is developed through deliberate practice of smooth, planned
movements. libdrone's HDZero Freestyle V2 system is optimised for low latency
rather than imaging quality — for serious mapping and survey applications, a
dedicated camera payload on the GX12 interface provides higher-quality results.

---

## Concept

### Jello effect and its mechanical cause

The jello effect is the wobbly, gelatin-like distortion visible in video from
a vibrating drone. It is caused by the rolling shutter: the camera sensor
reads pixel rows sequentially from top to bottom, not all at once. Each row
is captured at a slightly different moment in time. If the camera is vibrating
during the readout, successive rows are captured with the camera at slightly
different positions, producing the characteristic lateral distortion.

The amplitude of jello is proportional to the vibration amplitude at the camera
mount. Mechanical vibration isolation — floating motor mounts, correct O-ring
durometer, balanced propellers — reduces vibration at its source. A well-built
libdrone with balanced props and functional O-rings produces significantly less
jello than one with worn mounts or unbalanced propellers.

A gimbal eliminates jello entirely by mechanically stabilising the camera in
all three axes, regardless of airframe attitude. Without a gimbal, any pitch,
roll, or yaw movement of the drone appears directly in the image.

### Exposure: the 180° shutter rule

In still photography, fast shutter speed freezes motion — desirable. In video,
frozen motion looks unnatural. Natural-looking motion blur requires a shutter
speed approximately twice the frame rate: for 30 fps video, 1/60 s; for 60 fps,
1/120 s. This is the "180° shutter rule" (from the analogy to film camera shutter
arc angle).

In bright daylight, achieving 1/60 s shutter speed requires reducing incoming
light. A neutral density (ND) filter attaches to the camera lens and reduces
light by a fixed factor (ND4 = 2 stops, ND8 = 3 stops, ND16 = 4 stops). The
correct ND strength depends on ambient light conditions.

Additionally, slower shutter speeds reduce rolling shutter artefacts from
residual vibration — the longer exposure time averages out the vibration rather
than sampling it in the middle of a movement.

For the HDZero system: fixed-lens cameras have no filter thread. External filter
holders or UV-cut filter kits are available for common HDZero camera models.

### Composition and pilot technique

Aerial footage benefits from:

- **Deliberate, planned movements**: ascending reveal, orbit around a subject,
  linear tracking shot, fly-through. Each movement should be planned before
  execution — not improvised mid-flight.
- **Slow, smooth inputs**: stick movements should be gradual and continuous.
  Any sudden change in direction produces a visible jerk in the footage.
- **Consistent altitude**: altitude variation during a planned shot produces
  distracting vertical drift. Engage GPS position hold for altitude stability
  on survey and mapping passes.
- **Golden hour shooting**: the first and last hour of daylight produces warm,
  directional light with long shadows that add depth to aerial imagery. Flat
  midday light produces less visually interesting results.

---

## Reference

### ND filter selection guide

| Lighting condition | Target shutter (30fps) | Recommended ND |
|---|---|---|
| Overcast | 1/60 s | ND2–ND4 |
| Partly cloudy | 1/60 s | ND4–ND8 |
| Bright sunny | 1/60 s | ND8–ND16 |
| Very bright / reflective | 1/60 s | ND16–ND32 |

Values are approximate — measure exposure in the actual conditions.

### Jello severity indicators and fixes

| Jello level | Probable cause | Fix |
|---|---|---|
| Mild horizontal shimmer | Propeller imbalance | Balance props on magnetic balancer |
| Moderate wavy distortion | Worn O-rings | Replace floating mount O-rings |
| Severe jello | Direct rigid connection to airframe | Verify passive cover not touching arm head |
| Jello only at specific throttle | Frame resonance at that RPM | Check Blackbox — frame resonance peak |

---

## Procedure

### Pre-flight imaging check

1. Balance all props on a magnetic balancer before imaging flights.
2. Verify floating mount O-ring condition (not cracked or flattened).
3. Fit ND filter appropriate to planned lighting conditions.
4. In Betaflight: enable GPS position hold for altitude stability during passes.
5. Review one flight's footage immediately after the first pass. Assess jello
   level and exposure before committing to a full session.

---

## Rationale

### Why imaging quality is secondary in libdrone's standard FPV system

The HDZero Freestyle V2 is selected for minimum latency for pilot safety and
flight quality assessment — not for cinematographic quality. Its fixed lens,
narrow FOV, and compression artefacts are acceptable for FPV navigation but
not for mapping or documentation purposes. Applications requiring imaging quality
should use a dedicated camera payload on the GX12 interface (e.g. Insta360 on
Connector B GPIO2 camera trigger, or a survey camera with USB/UART control).

---

## Connections

requires:
  - [[floating-motor-mounts]]
  - [[vibration-isolation-theory]]
related:
  - [[jello-effect-mitigation]]
  - [[survey-imaging]]
  - [[thermal-imaging-payload]]
leads_to:
  - [[jello-effect-mitigation]]
  - [[survey-imaging]]
