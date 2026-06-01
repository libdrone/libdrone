---
id: acoustic-signature-design
title: "Acoustic signature design"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: generic
topic:
  - propulsion
personas:
  - 8.architect
  - 5.student
  - 9.defense
platform:
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

A multirotor's acoustic signature is dominated by propeller tip speed, not
motor noise or frame vibration. Tip speed is the product of rotational speed
and propeller radius; reducing either reduces tip speed and therefore noise.
Ghost's design exploits this directly: large-diameter props driven by low-KV
motors produce the same thrust at substantially lower RPM than the small
high-KV motors on other family members, reducing tip speed and acoustic
emission by approximately 10–15 dB(A) — a reduction the human ear perceives
as roughly half as loud. This is the primary design decision of the Ghost
variant.

---

## Concept

### The tip speed mechanism

Propeller noise is generated primarily at the blade tips, where the local
velocity relative to the surrounding air is highest. This tip velocity has
two components: the rotational velocity (propeller RPM × tip radius) and
the forward velocity of the aircraft. In hover, only the rotational component
is present.

Tip speed (m/s) = RPM × π × diameter / 60

For a standard 6-inch (152 mm diameter) drone at 14 000 RPM:
Tip speed = 14 000 × π × 0.152 / 60 = **111 m/s**

For Ghost's 12-inch (305 mm diameter) props at 3 200 RPM (sufficient for
hover at 1 360 g AUW with MN4108 480KV on 4S):
Tip speed = 3 200 × π × 0.305 / 60 = **51 m/s**

The 51 m/s vs 111 m/s difference in tip speed corresponds to approximately
10–15 dB(A) reduction in broadband noise emission. The A-weighting (dB(A))
reflects human auditory sensitivity — low-frequency content from large slow
props is less audible than high-frequency content from small fast props even
at equal acoustic power.

### The KV-diameter relationship

A motor's KV rating (RPM per volt) determines the no-load RPM at a given
voltage. T-Motor MN4108 at 480 KV on a 4S (16.8 V full charge) produces
approximately 8 064 RPM at no load. Under the load of a 12-inch prop, actual
operating RPM at hover throttle is much lower — typically 3 000–3 500 RPM.
This is the fundamental trade: low KV forces low RPM at any given voltage.
The same voltage that spins a 3 400 KV P1804 motor at 56 000 RPM no-load
spins the MN4108 at 8 000 RPM. Large props at low RPM carry as much or
more air per unit time as small props at high RPM — the difference is
acoustic efficiency.

### Detectability implications

Acoustic detection range is the distance at which a sound source can be
distinguished from background noise by a human listener. At 65–70 dB(A)
source level (typical 6-inch drone), the detection range in quiet outdoor
conditions is 80–150 m. At 50–55 dB(A) (Ghost), the same outdoor background
noise reduces detection range to 20–50 m. This is not invisibility — it is
a meaningful reduction in the warning time available to an observer.

For Ghost's operational context (perimeter watch, security-sensitive survey,
night operations), the difference between 150 m and 30 m acoustic detection
range is operationally significant. The awareness curriculum measures this
directly using Bandit Part B Exercise B2.1.

---

## Reference

| Platform | Prop diameter | Typical hover RPM | Tip speed | Approx. noise level |
|---|---|---|---|---|
| Pro (6S) | 6 in (152 mm) | 12 000–14 000 | 95–111 m/s | 65–70 dB(A) at 50 m |
| Bandit (4S) | 4 in (101 mm) | 14 000–16 000 | 74–84 m/s | 60–65 dB(A) at 50 m |
| Ghost (4S) | 12 in (305 mm) | 3 000–3 500 | 48–56 m/s | 50–55 dB(A) at 50 m |

**Note:** Absolute dB(A) values are estimates from published data for
comparable platforms; exact Ghost values require field measurement after
build and maiden flight.

---

## Procedure

### Measure Ghost acoustic detection range (Bandit Part B methodology)

1. Place Ghost in hover at 50 m AGL in Loiter mode. Operator monitors
   QGroundControl from the launch point.
2. A second operator (the listener) walks away from the hover point on flat
   terrain in calm wind conditions (< 2 m/s).
3. The listener walks until they can no longer reliably hear the aircraft,
   then walks back until they can reliably hear it. Mark this distance.
4. Repeat in three directions from the hover point. Average results.
5. Compare against the same measurement on Bandit — the ratio is the
   acoustic reduction Ghost achieves in this specific environment.

---

## Rationale

The 10–15 dB(A) reduction from Ghost's large-prop low-RPM design was
considered sufficient to justify the non-printable CF plate arm architecture
and the Li-Ion battery pack complexity. A smaller noise reduction — achievable
with slightly larger props on a printed arm — would not justify the departure
from the family's print-at-home philosophy. The 10 dB threshold was chosen
because it represents a perceptual doubling of quietness to the human ear —
a reduction that is operationally meaningful, not just measurable on a meter.

---

## Connections

requires:
  - [[propellers]]
  - [[brushless-motors]]
  - [[lift-and-thrust]]
related:
  - [[ghost-variant]]
  - [[cf-plate-arms]]
  - [[operational-security]]
  - [[hover-and-forward-flight]]
leads_to:
  - [[ghost-variant]]
