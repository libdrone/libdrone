---
id: induced-velocity
title: "Induced velocity and sensor placement"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - physics-flight-mechanics
personas:
  - 5.student
  - 3.payload-dev
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

When a propeller pushes air downward, it creates a recirculation zone around
the drone — a toroidal vortex of disturbed, turbulent air that extends roughly
one to 1.5 rotor radii above the propeller plane. Air inside this zone has
already passed through the propellers. A sensor placed inside this zone does
not measure the ambient environment — it measures air the drone itself disturbed.
The sensor mast on libdrone is exactly as tall as it needs to be to position
the sensor above this zone, and no taller.

---

## Concept

### The propeller's effect on surrounding air

A spinning propeller does not push a discrete parcel of air downward and leave
everything else undisturbed. It induces a velocity field: air below the prop
accelerates downward, air around the edges fans outward, and above the drone
a pressure differential draws air inward and downward through the prop disk.
The result is a continuous recirculation: air enters from above and the sides,
passes through the prop disk, exits downward and outward below, then
recirculates back up around the perimeter.

The recirculation region above the prop plane — where air is being drawn in
toward the rotor — is turbulent and not representative of the ambient atmosphere.
This is where instrument placement matters.

### The toroidal vortex

The recirculation forms a toroid — a donut-shaped region centred on the drone,
extending upward approximately one to 1.5 rotor radii (76–114 mm for a 6-inch
prop) above the propeller plane. Inside this zone:
- Air has already passed through the propellers
- Air is turbulent and has elevated temperature from motor and ESC heat
- Particulate matter, CO₂, and VOCs emitted by the motors are present
- Humidity measured is influenced by prop wash, not ambient air

For a gas sensor, temperature sensor, or particulate matter sensor, measurement
inside this zone produces data that is partly the ambient environment and partly
an artefact of the drone itself. The fraction of drone artefact varies with
throttle, wind speed, and flight manoeuvre.

### Calculating sensor mast height

The minimum mast height to clear the recirculation zone is:

    h_mast > 1.5 × R_rotor

Where `R_rotor` = rotor radius = prop diameter / 2.

For libdrone's 6-inch (152 mm diameter) props:

    R_rotor = 76 mm
    h_mast > 1.5 × 76 = 114 mm


The libdrone medium mast is 80 mm, the tall mast is 120 mm. For the SEN66
air quality payload, the tall mast (120 mm) clears the theoretical minimum.
In practice, in hover conditions with the sensor above the prop arc, the
Sensirion SEN66 on a 120 mm mast consistently produces readings consistent
with ground-level reference measurements during field validation.

### The induced velocity magnitude

The average induced velocity through the prop disk in hover:

    v_induced = sqrt(T / (2 × ρ × A))

For libdrone at ~860 g AUW (8.44 N), 4 × 152mm props:

    A = 4 × π × (0.076)² ≈ 0.0727 m²
    v_induced = sqrt(8.44 / (2 × 1.225 × 0.0727)) ≈ 3.4 m/s downward

3.4 m/s downward flow through the prop disk. This flow is what recirculates
upward around the perimeter. The recirculation velocity above the prop plane
is lower than this — roughly 0.5–1.5 m/s — but sufficient to draw contaminated
air into any sensor positioned below the toroidal vortex boundary.

### Tradeoff: mast height vs CG and handling

A taller mast raises the payload mass higher, increasing the drone's CG.
→ See [[pendulum-stability]] for the quantitative effect.

At 40 g sensor payload on a 120 mm mast, the CG shift is approximately 5 mm
upward. This shortens the effective pendulum arm, raises the natural oscillation
frequency slightly, and requires marginal D-term reduction. For the SEN66
payload weight (approximately 20 g for the mast assembly), the effect is within
noise. For heavier future payloads, the calculation should be repeated.

---

## Reference

### Mast heights and clearance

| Mast height | Clearance above 1.5 × R for 6-inch prop | Recommendation |
|---|---|---|
| 40 mm (short) | Not cleared — 74 mm below threshold | Avoid for gas/particulate sensors |
| 80 mm (medium) | Not cleared — 34 mm below threshold | Use only for sensors with field validation |
| 120 mm (tall) | Cleared — 6 mm above threshold | Recommended for all air quality sensors |

Note: the 1.5 × R threshold is theoretical. Real recirculation geometry
depends on throttle level, wind, and flight manoeuvre. Field validation with
a reference sensor at ground level is always the authoritative test for a
new payload design.

### Effect of forward flight

In forward flight, the drone moves through undisturbed air. The recirculation
zone is swept behind the drone and the sensor is continuously encountering
fresh ambient air. Sensor readings in forward flight are more representative
of the ambient environment than in hover. For mapping missions, this means
data quality improves when the drone maintains forward speed rather than
hovering to take measurements.

---

## Procedure

<!-- not applicable — for mast design see payload-architecture domain -->

---

## Rationale

### Why the mast height is the minimum necessary and no more

Every additional millimetre of mast height: increases CG height (reduces
pendulum stability), increases frontal area (increases drag), increases
structural leverage on the GX12 connectors in a crash, and adds mass.
The mast is sized to clear the recirculation zone — not to provide comfortable
margin. If field validation shows the 120 mm mast still shows recirculation
contamination at specific flight conditions, the next mast increment should
be calibrated from measurement, not from an arbitrary safety factor.

---

## Connections

requires:
  - [[lift-and-thrust]]
related:
  - [[hover-and-forward-flight]]
  - [[vortex-ring-state]]
  - [[pendulum-stability]]
leads_to:
  - [[vortex-ring-state]]


[pendulum-stability]: pendulum-stability.md "Pendulum stability"
[lift-and-thrust]: lift-and-thrust.md "Lift and thrust"
[hover-and-forward-flight]: hover-and-forward-flight.md "Hover and forward flight"
[vortex-ring-state]: vortex-ring-state.md "Vortex ring state"
