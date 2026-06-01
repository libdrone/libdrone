---
id: propellers
title: "Propellers"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - propulsion
personas:
  - 5.student
  - 1.builder
  - 2.operator
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

A propeller converts rotational energy into thrust by accelerating air
downward. Its two primary specifications are diameter (tip-to-tip) and pitch
(theoretical travel per revolution through solid medium). Larger diameter
moves more air per revolution and is more efficient for hover. Higher pitch
moves the drone faster through the air per revolution but draws more current.
Blade count affects the thrust-to-noise trade-off. libdrone uses HQ 6-inch
tri-blade polycarbonate props in two pitch variants: 6×3×3 for standard
conditions and 6×2.5×3 for calm conditions and maximum flight time.

---

## Concept

### Diameter and efficiency

The relationship between diameter and hover efficiency comes directly from
momentum theory. The power required for a given thrust scales inversely with
the square root of disk area:

    P ∝ T / sqrt(A)

Doubling the rotor area (1.41× diameter) reduces power for the same thrust
by approximately 30%. A large, slow propeller is always more efficient for
hover than a small, fast propeller producing the same thrust.

The practical constraint on diameter is tip clearance — adjacent prop tips
must not approach each other. At 330 mm wheelbase, 6-inch (152 mm diameter)
props give a minimum 15 mm tip clearance. 7-inch props would violate this
clearance.

### Pitch

Pitch is the theoretical distance the propeller would advance in one full
rotation through a solid, non-slipping medium. A 6×3 propeller would advance
3 inches per revolution if there were no slip. In real air, slip means the
actual advance per revolution is less than the pitch.

Higher pitch: more air displaced per revolution, more thrust at high RPM,
more current draw, better wind penetration, higher motor temperature. Better
for windy conditions and fast forward flight.

Lower pitch: less air per revolution, less thrust at high RPM, lower current
draw, cooler motors, better efficiency in calm hover. Better for mapping missions
in calm conditions and for maximum flight time.

The pitch-to-diameter ratio beyond approximately 1:2 produces diminishing
returns from aerodynamic losses. Both libdrone prop options (6×3 and 6×2.5)
sit below this limit.

### Blade count

More blades for a given diameter increase thrust at a given RPM but also
increase aerodynamic drag and noise. Two-blade propellers are efficient but
produce more vibration per revolution. Three-blade propellers balance thrust,
noise, and efficiency. Four-blade propellers are used where noise reduction
and compact diameter are important (urban environments).

libdrone uses three-blade props. The tri-blade design provides more thrust
per diameter than two-blade at the same RPM, allowing a lower RPM for the
same thrust — which reduces motor heat and aerodynamic noise.

### Rotation direction and installation

Adjacent props must counter-rotate to cancel net angular momentum. Props are
manufactured for a specific direction and are not interchangeable without
reversing the motor. Standard (CCW) props used on clockwise motors push
the drone into the ground — a common first-build error with an unmistakable
result: the drone pushes down on arm.

Polycarbonate (PC) vs nylon vs carbon fibre:
- **PC (libdrone standard):** durable, consistent weight, balanced from factory.
  Bends under impact rather than shattering. Safe for community builds.
- **Nylon:** cheaper, more flexible, lower performance. Acceptable for training.
- **Carbon fibre:** stiffest, lightest, most efficient. Shatters on impact into
  sharp fragments. Not recommended for community builds or proximity flying.

### Prop balancing

An unbalanced propeller vibrates at exactly its rotation frequency. At
30,000 RPM, an imbalance of 0.1 g at the blade tip generates approximately
75 N of rotating centrifugal force. This force propagates through the motor
into the floating mount (which attenuates but does not eliminate it) and
reaches the gyroscope.

Three minutes on a magnetic balancer per propeller, adding tape to the lighter
blade until the prop rests level in any orientation, measurably reduces the
Blackbox noise floor and extends motor bearing life.

---

## Reference

### libdrone V2.4.6 propeller specification

| Parameter | Set A (HQ 6×3×3) | Set B (HQ 6×2.5×3) |
|---|---|---|
| Diameter | 6 inch (152 mm) | 6 inch (152 mm) |
| Pitch | 3 inch | 2.5 inch |
| Blades | 3 | 3 |
| Material | Polycarbonate | Polycarbonate |
| Mass (each) | 5.4 g | 5.3 g |
| Mass (set of 4) | 21.6 g | 21.2 g |
| Hub diameter | 13.2 mm | — |
| Shaft | 5.0 mm | 5.0 mm |
| Use case | Standard, windy, mapping | Calm, maximum flight time |

Betaflight has two profiles configured, one per prop set. Switch profiles
when changing props — the PID values differ slightly.

### Inspection and replacement criteria

Replace immediately if:
- Any visible crack, chip, or nick in a blade
- Hub shows any cracking or white stress marks around the shaft bore
- Drone has experienced a ground impact at any speed (props absorb significant
  impact energy and may have internal damage invisible externally)
- Vibration level in Blackbox increased compared to previous flights

Polycarbonate props do not have a flight-hour lifespan limit if undamaged.
Replace on damage, not on schedule.

---

## Procedure

### Pre-flight prop check

1. Visually inspect each blade from tip to hub on both faces.
2. Flex each blade gently — cracks produce an audible click.
3. Check hub for looseness on shaft: prop should not rock or wobble.
4. Verify correct rotation direction: top face should face upward on CCW
   motors, downward on CW motors (or check the small "R" or "CW" marking
   on reversed props).

### Prop installation torque

Finger-tight plus 1/8 turn. Over-torquing a polycarbonate prop cracks the
hub. Under-torquing allows the prop to shift position during flight.
M5 prop nut: approximately 0.5–0.8 N·m. Never use standard M5 bolts — always
use the prop nut with the nylon lock built in or a dedicated prop bolt.

---

## Rationale

### Why two prop sets are specified

The 6×3×3 and 6×2.5×3 props have meaningfully different performance profiles
at libdrone's operating conditions. The lower pitch (2.5) draws noticeably less
current at hover — approximately 3–5% less per motor — directly translating to
longer flight time. In calm conditions where wind authority is not needed, this
is a worthwhile gain. In wind, the higher pitch (3.0) provides better authority
and speed. Maintaining both sets and knowing which to use based on conditions
is part of operational competency.

---


### libdrone Pro propeller selection

Two HQProp sets are specified for Pro:

| Set | Spec | Thrust | Current | Use case |
|---|---|---|---|---|
| Set A | HQProp 6×3×3 | Higher | Higher | Standard operations, payloads |
| Set B | HQProp 6×2.5×3 | Lower | Lower | Extended endurance, lower noise |

Set A (higher pitch) produces more thrust at a given RPM and handles heavier
payloads better. Set B (lower pitch) draws less current at the same RPM,
extending flight time by 10–15% at the cost of reduced top-end thrust. For
typical sensor payload missions (860g AUW), Set A is the standard choice.
For long loiter missions with lightweight payloads, Set B extends endurance.


## Connections

requires:
  - [[lift-and-thrust]]
  - [[brushless-motors]]
related:
  - [[electronic-speed-controllers]]
  - [[floating-motor-mounts]]
  - [[vibration-isolation-theory]]
  - [[propeller-balance]]
  - [[acoustic-signature-design]]
leads_to:
  - [[electronic-speed-controllers]]
  - [[propeller-balance]]


[lift-and-thrust]: lift-and-thrust.md "Lift and thrust"
[brushless-motors]: brushless-motors.md "Brushless motors"
[electronic-speed-controllers]: electronic-speed-controllers.md "Electronic speed controllers"
[floating-motor-mounts]: floating-motor-mounts.md "Floating motor mounts"
[vibration-isolation-theory]: vibration-isolation-theory.md "Vibration isolation theory"
[propeller-balance]: propeller-balance.md "Propeller balance"
[acoustic-signature-design]: acoustic-signature-design.md "Acoustic signature design"
