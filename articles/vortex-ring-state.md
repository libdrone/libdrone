---
id: vortex-ring-state
title: "Vortex ring state"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - physics-flight-mechanics
personas:
  - 5.student
  - 2.operator
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Vortex ring state (VRS) is a dangerous flight condition in which a drone
descends vertically fast enough to descend into its own downwash. The propellers
recirculate disturbed air rather than pulling in fresh air, effective thrust
drops by 30–50%, and the drone enters an accelerating descent. Adding throttle
makes it worse. The only recovery is translating horizontally — even 3–5 m/s
sideways is enough to break the vortex. Vortex ring state is the documented
cause of real manned helicopter accidents. The prevention rule is simple: never
descend vertically faster than 2 m/s.

---

## Concept

### How VRS develops

In normal hover, the drone is stationary and the propellers pull in undisturbed
air from above. The downwash exits below and around the sides. This is the
normal flow regime — clean, predictable, efficient.

When the drone descends, it moves downward into the air column it has already
pushed down. At low descent rates (below about 1 m/s), the flow regime stays
close to normal — fresh air still enters the prop disk from the sides and from
above the descent path.

At higher descent rates, the drone is descending at a speed that approaches the
induced velocity of the downwash. For libdrone at ~860 g AUW:

      v_induced ≈ 3.4 m/s
      VRS onset: descent rate > ~0.5 × v_induced ≈ 1.5–2 m/s

At this point, the downwash can no longer escape downward fast enough — the
drone is catching up with it. Air that the propellers just pushed down is now
being drawn back up into the prop disk from below. The propellers are now
recirculating a vortex ring of disturbed, low-momentum air.

### Why more throttle makes it worse

The instinctive response to the drone sinking is to apply more throttle.
In VRS, this is exactly wrong. More throttle increases the induced velocity
of the downwash, which strengthens the recirculation, which increases the
volume of disturbed air being ingested, which further reduces effective thrust.
The drone sinks faster despite more throttle. Pilots who do not recognise VRS
keep adding throttle and the descent accelerates.

### Recovery

The only effective recovery is to translate horizontally. Moving the drone
sideways, forward, or backward at 3–5 m/s causes the rotor disk to sweep
through undisturbed air rather than its own recirculation. The vortex ring
collapses within one to two seconds. Effective thrust returns to normal.
The descent stops.

The key insight: the vortex exists because the drone is descending into its
own downwash. Any horizontal motion moves the disk away from the disturbed
air column. Even a small horizontal translation is enough.

Applying throttle simultaneously with horizontal translation is correct —
throttle helps once the flow regime has been broken. Throttle without
horizontal translation does not break the vortex.

---

## Reference

### VRS onset conditions

| Parameter | Value for libdrone |
|---|---|
| Induced velocity v_induced | ~3.4 m/s |
| VRS onset (typical) | descent rate > 1.5–2 m/s |
| Maximum safe vertical descent | < 2 m/s in calm air |
| Recovery horizontal velocity needed | 3–5 m/s |
| Time to recover after translation | 1–2 seconds |

These values are approximate and depend on atmospheric conditions, throttle
level, and drone configuration. In turbulent air or at lower battery voltage
(reduced maximum thrust), VRS onset may occur at lower descent rates.

### Risk factors

| Condition | Effect on VRS risk |
|---|---|
| Low battery (reduced max thrust) | Onset at lower descent rate |
| High payload mass | Higher AUW → higher v_induced → higher onset speed |
| Still air | VRS more pronounced; wind provides some horizontal flow naturally |
| Turbulent air | Unpredictable onset, can enter VRS at lower descent rates |
| Descending over forest / roof / thermal | Rising air below can reduce VRS risk |

### Historical accidents

VRS has contributed to accidents in manned rotorcraft including:
- 1994 US Army UH-60 Black Hawk, Germany (training)
- 2005 Royal Navy Sea King, Irish Sea (training)

These are documented in accident investigation reports as contributing factors.
The physics is identical at all scales: the drone's v_induced is in the same
range as the helicopter's — the hazard is not diminished by smaller scale.

---

## Procedure

### Avoiding VRS in normal operations

1. Descend at angles rather than vertically wherever possible. An angled
   descent continuously moves the drone through undisturbed air — the vortex
   never establishes itself.
2. When vertical descent is required, limit descent rate to 2 m/s. In
   Betaflight/ArduPilot position modes, this is configurable as the maximum
   descent speed.
3. Monitor altitude in OSD. A descent that is accelerating without increasing
   stick input is a VRS warning sign.

### Recovery if VRS is suspected

1. Apply immediate lateral translation: push the roll or pitch stick to full
   deflection in any horizontal direction.
2. Simultaneously apply throttle to compensate for altitude loss.
3. Maintain horizontal motion for at least 2–3 seconds until the flow regime
   normalises and the drone responds normally to throttle.
4. Do not reduce horizontal motion until the drone has fully recovered vertical
   authority (normal throttle response).

---

## Rationale

### Why this article targets operators as well as students

VRS is not an abstract physics concept — it is a real, documented hazard
that any operator descending a loaded drone in calm air can encounter.
The operator needs to know: what it feels like (sinking despite throttle),
what to do (translate immediately), and what not to do (more throttle alone).
The student needs to understand why it works that way. Both personas are
served by the same article because the concept and the practical response
are inseparable.

---

## Connections

requires:
  - [[induced-velocity]]
  - [[hover-and-forward-flight]]
related:
  - [[lift-and-thrust]]
leads_to:
  - [[piloting-operations]]


[induced-velocity]: induced-velocity.md "Induced velocity and sensor placement"
[hover-and-forward-flight]: hover-and-forward-flight.md "Hover and forward flight"
[lift-and-thrust]: lift-and-thrust.md "Lift and thrust"
[piloting-operations]: piloting-operations.md "Piloting and operations"
