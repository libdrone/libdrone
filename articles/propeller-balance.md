---
id: propeller-balance
title: "Propeller balance"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: generic
topic:
  - manufacturing
personas:
  - 1.builder
  - 4.workshop
  - 5.student
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Propeller balance is the correction of mass asymmetry between the blades of
a propeller. An unbalanced prop generates a once-per-revolution vibration at
the motor shaft frequency — typically 100–300 Hz — that couples directly into
the IMU, degrading flight controller performance and accelerating bearing wear.
Static balancing removes the primary imbalance with a magnetic balancer; dynamic
balancing (on a spinning prop) removes secondary imbalances but is rarely
required for FDM-scale props. Balancing takes five minutes and is the highest
return-on-time vibration reduction step available before first flight.

---

## Concept

### Why unbalanced props matter

A propeller blade's centre of mass should lie exactly on the rotation axis.
If one blade is heavier than the other by even 0.05 g, the centre of mass
is offset from the rotation axis by a small distance. At 10 000 RPM, this
offset produces a centrifugal force that rotates once per revolution —
a sinusoidal force at 167 Hz applied to the motor shaft and transmitted
through the motor mount into the arm and body.

The RPM filter in Betaflight and ArduPilot is designed to remove this
frequency from the gyroscope signal, but it cannot remove it completely
without also removing control signal content near that frequency. A better-
balanced prop requires less aggressive filtering, resulting in cleaner
gyroscope data and better PID response. See → [[rpm-filter]] for the
filter mechanism.

### Static vs dynamic imbalance

**Static imbalance** is a mass offset in the plane of rotation: one blade
is heavier. The prop tilts on a freely-rotating axle toward the heavy blade.
This is what a prop balancer measures and what manual correction addresses.

**Dynamic imbalance** is a mass offset perpendicular to the rotation plane:
one blade is heavier at its tip while the other is heavier at its root. The
prop rotates symmetrically on a static balancer but wobbles axially at speed.
Dynamic imbalance is uncommon in consumer props and requires a spinning
balancer to detect. For libdrone scale operations, static balance is sufficient.

### What a magnetic prop balancer measures

A magnetic prop balancer is a cradle with two magnetic pivot points. The prop
hub rests on the pivot; the blades hang freely. In an unbalanced prop, the
heavy blade rotates to the bottom. The heavier blade can be identified
visually. Correction is by removing material from the heavy blade (sanding
the trailing edge tip lightly) or adding material to the light blade (a small
adhesive weight on the blade surface near the hub).

---

## Reference

**Tools required:**
- Magnetic prop balancer (Du-Bro or equivalent, ~€10)
- 400-grit sandpaper
- Fine permanent marker

**Acceptance criterion:** The prop should remain stationary in any rotational
position on the balancer — no blade should fall to the bottom consistently.

**Time per prop:** 3–8 minutes.

**When to balance:**
- New props before first flight
- After any prop strike or impact
- After noticing increased vibration on blackbox logs
- Not required for TPU flex props (deform under imbalance forces)

---

## Procedure

### Static balance a propeller

1. Place the prop on the magnetic balancer. Note which blade descends.
   That blade is the heavy blade.
2. Mark the heavy blade's tip with a fine marker.
3. Sand the heavy blade's trailing edge at the tip: 5 strokes of 400-grit,
   light pressure, even strokes along the edge.
4. Return prop to balancer. If the blade no longer falls, the prop is
   within tolerance — test by releasing from 30°, 60°, 120°, and 180°
   positions. All should hold without rotating.
5. If the prop now overcorrects (light blade falls), sand 2–3 strokes from
   the other blade.
6. Repeat until the prop holds any position on the balancer.

**Do not** sand the leading edge, the root, or the top surface — these
affect aerodynamic performance. Trailing edge tip removal has the largest
mass effect with the least aerodynamic change.

---

## Rationale

Propeller balancing is listed as an operational principle in Engineering
Principles 101 despite being a simple mechanical task because it is
systematically skipped by first-time builders. The vibration consequence
of skipping it is not immediately obvious — the drone flies — but shows up
in blackbox logs as elevated gyroscope noise, requires more aggressive RPM
filter notch settings, and produces early bearing failure. Making balancing
an explicit step in the build workflow, with clear time and tool requirements,
removes the main reason it is skipped: builders do not know how long it takes
or what tool they need.

---

## Connections

requires:
  - [[propellers]]
  - [[vibration-isolation-theory]]
related:
  - [[rpm-filter]]
  - [[jello-effect-mitigation]]
  - [[imu-filter-tuning]]
  - [[blackbox-analysis]]
  - [[floating-motor-mounts]]
leads_to:
  - [[rpm-filter]]
  - [[first-flight]]
