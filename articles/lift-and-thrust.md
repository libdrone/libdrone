---
id: lift-and-thrust
title: "Lift and thrust"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - physics-flight-mechanics
personas:
  - 5.student
  - 4.workshop
  - 1.builder
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

A multirotor stays airborne by throwing air downward. Newton's third law
requires an equal and opposite reaction force — upward thrust on the drone.
The efficiency with which a propeller generates thrust depends on how much
air it moves and how fast: it is always more efficient to accelerate a large
mass of air slowly than a small mass quickly. This explains why larger
propellers are more efficient for hover, and directly determines the choice
of prop size for any given mission.

---

## Concept

### Newton's third law as the real explanation of lift

The common answer — "propellers generate lift" — is not wrong but skips
the interesting part. The complete answer starts with Newton's third law:
for every action there is an equal and opposite reaction. A spinning propeller
accelerates a column of air downward. The reaction force — equal in magnitude,
opposite in direction — acts on the propeller and on everything attached to it.
That reaction force is thrust.

This reframe matters immediately. Thrust is not a mysterious aerodynamic
property. It is a direct consequence of throwing mass in one direction and
being pushed in the other. To produce more thrust: move more air, or move
the same air faster.

### Momentum theory and disk loading

The power required to produce a given thrust T from a propeller of disk area A
in air of density ρ is:

    P = T × sqrt(T / (2 × ρ × A))

The key relationship: for the same thrust T, doubling the disk area (which
means approximately 1.41× the propeller diameter) reduces required power by
approximately 30%. A large, slow propeller is always more efficient than a
small, fast one at producing the same thrust — because the large propeller
moves more air per unit time and imparts less kinetic energy to each parcel
of air.

This single equation explains why:
- Helicopters with large rotors are more efficient at hovering than jets
- A 6-inch prop at 28,000 RPM outperforms a 3-inch prop at 60,000 RPM
  for any hover-dominant mission
- Increasing propeller size improves flight time more than increasing
  battery capacity by an equivalent mass

### Drones fall continuously — and continuously correct

A multirotor without motor power is aerodynamically inert. It falls. There
are no wings, no glide path, no natural stability. Every moment of level
flight is the result of active, continuous correction by the flight controller.
What looks like hovering is a computer solving a control problem thousands
of times per second, continuously adjusting motor speed to push the drone
back toward the commanded attitude.

This reframe changes what "flying" means for a multirotor. You are not
harnessing a natural force to maintain equilibrium, as in a glider or a
sailboat. You are running an active correction loop against gravity, inertia,
and wind simultaneously.

---

## Reference

### Induced velocity formula

    v_induced = sqrt(T / (2 × ρ × A))

Where:
- T = total thrust (N)
- ρ = air density (1.225 kg/m³ at sea level, 15°C)
- A = total rotor disk area (m²) = π × (D/2)² × number of rotors

For libdrone at 860 g AUW (8.44 N thrust), 4 × (152 mm / 2)² × π rotor area:
`v_induced ≈ 3.4 m/s` downward — relevant for sensor mast height calculation.
→ See [[induced-velocity]].

### libdrone V2.4.6 thrust figures

| Config | AUW | Peak thrust (4 motors) | Hover throttle | TWR |
|---|---|---|---|---|
| No payload | ~807 g | ~10,000 g | ~28% | ~12.4:1 |
| +80g payload | ~887 g | ~10,000 g | ~30% | ~11.3:1 |

Motor: BrotherHobby Avenger V2 2507 1750KV on 6S, HQ 6×3×3 props.
Peak thrust per motor: 2400–2600 g at 40–55A.

---

## Procedure

<!-- not applicable -->

---

## Rationale

### Why 6-inch props on a 330 mm wheelbase frame

The 6-inch prop diameter (152 mm) at 330 mm wheelbase gives a minimum 15 mm
tip clearance. The momentum theory calculation shows that 6-inch props
require significantly less power for hover than 4-inch or 5-inch props at
the same AUW. The efficiency gain directly translates to longer flight time
per battery charge. For a payload platform where hover-dominant missions are
the norm, this efficiency benefit outweighs the mass and size penalty of the
larger prop.

---

## Connections

requires: []
related:
  - [[six-degrees-of-freedom]]
  - [[induced-velocity]]
  - [[hover-and-forward-flight]]
  - [[thrust-to-weight-ratio]]
  - [[fixed-wing-fundamentals]]
leads_to:
  - [[six-degrees-of-freedom]]
  - [[hover-and-forward-flight]]
  - [[thrust-to-weight-ratio]]
  - [[fixed-wing-fundamentals]]


[induced-velocity]: induced-velocity.md "Induced velocity and sensor placement"
[six-degrees-of-freedom]: six-degrees-of-freedom.md "Six degrees of freedom"
[hover-and-forward-flight]: hover-and-forward-flight.md "Hover and forward flight"
[thrust-to-weight-ratio]: thrust-to-weight-ratio.md "Thrust-to-weight ratio"
[fixed-wing-fundamentals]: fixed-wing-fundamentals.md "Fixed-wing fundamentals"
