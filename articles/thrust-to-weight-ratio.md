---
id: thrust-to-weight-ratio
title: "Thrust-to-weight ratio"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: generic
topic:
  - propulsion
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

Thrust-to-weight ratio (T:W) is the ratio of the maximum thrust the propulsion
system can produce to the all-up weight of the aircraft. A T:W of 1.0 means
the motors can exactly balance gravity at full throttle; the aircraft can
barely hover and has no reserve for manoeuvre or wind. A T:W of 2.0 means
the motors produce twice the aircraft weight at full throttle; hover requires
roughly 50% throttle, leaving the other 50% for authority. For libdrone
variants, T:W at full throttle ranges from approximately 2.3:1 (Ghost, survey-
optimised) to 4:1+ (Pro and Bandit in sport trim). T:W determines hover
throttle position, climb rate, wind resistance ceiling, and the margin
available for attitude recovery from disturbances.

---

## Concept

### The hover throttle relationship

In steady hover, thrust equals weight. If maximum thrust is T_max and aircraft
weight is W, hover throttle position is approximately W / T_max. At T:W = 2,
hover requires 50% throttle. At T:W = 4, hover requires 25% throttle.

The hover throttle position matters for two reasons:

First, **control authority**: the flight controller modulates throttle ±N%
around the hover point to maintain altitude and respond to attitude changes.
If hover is at 90% throttle (T:W ≈ 1.1), only 10% throttle is available for
upward authority — the aircraft cannot accelerate upward quickly and will lose
altitude in any manoeuvre that demands more than the available 10%. If hover
is at 50% (T:W = 2), 50% remains for authority — full attitude recovery is
possible.

Second, **motor temperature**: motors near maximum throttle for sustained hover
run hot. Motors at 50% throttle for sustained hover run cool. Motor temperature
under hover load is a direct function of hover throttle position.

### T:W and wind resistance

In forward flight tilted into wind, the motor thrust vector has both a vertical
component (opposing gravity) and a horizontal component (opposing drag and wind
force). The maximum wind speed the aircraft can resist is the speed at which
the horizontal thrust component equals the aerodynamic drag — which depends on
the reserve thrust available above hover. Higher T:W means more reserve thrust,
which means higher maximum sustainable wind speed.

For a survey platform like Ghost with T:W ≈ 2.3, maximum sustainable wind is
approximately 8 m/s. For a sport platform like Pro with T:W ≈ 4, wind
resistance exceeds 15 m/s. This is why Ghost's mission weather limit is 8 m/s
and Pro's is much higher.

### T:W in motor and battery selection

T:W cascades through the entire design. Selecting heavier motors lowers T:W
(more weight, similar thrust) unless matched with larger props. Adding battery
mass lowers T:W. Adding payload mass lowers T:W. The design cycle for any
new variant starts with the target T:W, derives maximum AUW from the motor
thrust curves, then allocates that mass budget across components.

For Ghost: 4× MN4108 at 4S produce ~880 g thrust each = 3520 g total thrust.
AUW 1360 g. T:W = 3520/1360 = 2.6. Hover at ~38% throttle. This is appropriate
for a survey platform with calm-weather mission constraints.

---

## Reference

| Platform | Max thrust (4 motors) | AUW | T:W | Hover throttle |
|---|---|---|---|---|
| Pro (6S) | ~3 200 g | ~600 g | ~5.3 | ~19% |
| Bandit (4S) | ~2 436 g | ~500 g | ~4.9 | ~21% |
| Core (4S) | ~2 436 g | ~250 g | ~9.7 | ~10% |
| Ghost (4S) | ~3 520 g | ~1 360 g | ~2.6 | ~39% |

**Minimum T:W for stable flight:** 1.5 (provides control authority and 6 m/s
wind resistance). Below 1.5, altitude hold becomes unreliable in any wind.

**T:W for ArduPilot Autotune:** Autotune requires T:W ≥ 2.0. Below this,
the aircraft cannot perform the rapid attitude changes the procedure demands.

---

## Procedure

### Calculate T:W for a new build

1. Find the motor thrust curve from the manufacturer's datasheet (thrust
   at 100% throttle on the intended battery cell count and prop size).
2. Multiply single-motor max thrust by motor count.
3. Estimate AUW: sum BOM component masses + printed parts + battery.
4. T:W = total max thrust / AUW (both in the same unit, grams or Newtons).
5. If T:W < 2.0, increase motor size, reduce AUW, or accept limited wind
   resistance and reduced Autotune compatibility.

---

## Rationale

T:W is the first design parameter checked when evaluating any build or
modification — before motor temperature, before flight time, before regulatory
weight. A build with T:W < 1.5 is unsafe regardless of how good its other
parameters are. Establishing T:W analysis as a first-step check prevents
the common error of selecting motors that are correct for the frame size but
insufficient for the actual loaded AUW after all components are added.

---

## Connections

requires:
  - [[lift-and-thrust]]
  - [[brushless-motors]]
  - [[propellers]]
related:
  - [[hover-and-forward-flight]]
  - [[lipo-batteries]]
  - [[li-ion-batteries]]
  - [[ardupilot-autotune]]
  - [[motor-mixing]]
leads_to:
  - [[hover-and-forward-flight]]
  - [[ardupilot-autotune]]
