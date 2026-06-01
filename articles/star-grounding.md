---
id: star-grounding
title: "Star grounding"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - emc-signal-integrity
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

Multiple ground connections between components create closed loops. A closed
conductive loop is an antenna: any changing magnetic field passing through
the loop induces a current in the loop, which creates a noise voltage at
every point in the circuit that references that ground. Star grounding
eliminates loops by routing all ground connections to a single point. No
loop can form because there is only one ground node. On libdrone, the ESC
GND pad is the star point: the battery negative, FC ground, and capacitor
negative all connect there directly. No separate ground wires run from
subsystems back to the battery.

---

## Concept

### Why ground loops cause noise

Faraday's law: a changing magnetic flux through a closed loop induces a
voltage proportional to the rate of flux change:

    V_induced = −dΦ/dt

In a drone, changing magnetic fields are everywhere — ESC switching at 48 kHz,
motor commutation at 3,500 Hz, battery lead transients at every throttle change.
Any closed ground loop that encloses some of this flux will have a voltage
induced in it.

The induced voltage appears as a noise voltage across the loop. Every component
connected between two points in that loop experiences the noise as a supply
voltage variation. A gyroscope with ±3.3V supply referenced to a noisy ground
plane may see the supply voltage fluctuate by tens of millivolts — directly
shifting its zero-rate output.

The larger the loop area, the more flux through it, the larger the induced
voltage. A 10 cm × 5 cm ground loop (50 cm²) at 48 kHz with moderate ESC
field strength can induce millivolt-level noise — significant against gyro
signal levels of 0.01°/s.

### Star topology eliminates loops

In a star ground, all components connect their ground to a single point. There
is no path through which current can circulate — no loop. The voltage at every
component's ground reference is the same single-node voltage. Any noise from
the power domain appears equally on all ground references and cancels out in
differential measurements.

The single point must be the highest-current ground node — in a drone, the ESC
GND pad, because all motor current flows through it. Making the ESC GND the star
point ensures that the large motor current transients return directly to the
battery negative without passing through any intermediate node that also
serves as a signal ground.

### What to avoid

The common violation is routing a separate ground wire from a subsystem
(VTX, GPS, camera) back to the battery negative in addition to the ground
connection via the FC. This creates a second ground path from the subsystem
to battery, forming a loop between:
- Subsystem → FC → ESC → battery
- Subsystem → direct wire → battery

Any magnetic field passing through the area enclosed by these two paths will
induce a circulating current. The induced current adds noise to every signal
referenced to either path.

---

## Reference

### libdrone star ground topology

    Battery GND
        │
        ▼
    ESC GND pad ◄── star point (highest current node)
        │
        ├── FC GND (short direct wire to ESC pad)
        │
        ├── 1000µF capacitor GND (directly on ESC pad)
        │
        └── Buck converter GND → VTX GND
            (VTX GND must not return separately to battery)

GPS GND routes via the FC — not via a separate wire to the battery or ESC.
The FC handles GPS, RX, and all logic grounds internally on its own star ground,
then connects that star point to the ESC GND pad via a single wire.

### Violations to avoid

| Practice | Problem |
|---|---|
| Separate GND wire from VTX to battery | Creates a loop with the VTX → FC → ESC → battery path |
| GND wire running parallel to signal wire | Unequal impedance paths create ground potential differences |
| Multiple GND connections from FC to ESC | Creates micro-loops within the stack |
| Camera GND tapped at FC and again at VTX | Loop area equals FC-to-VTX spacing |

---

## Procedure

### Verifying star ground during build

1. Before soldering, draw the ground path on paper: battery (−) → ESC pad →
   FC → each subsystem. Confirm no subsystem has a second path back to battery.
2. After soldering, use a multimeter in continuity mode: probe between any two
   ground points. All should read <0.5 Ω. If any reads open circuit, a ground
   connection is missing.
3. Check for unexpected ground loops: probe between the GND pin of each
   subsystem and the ESC GND pad. Should all read near 0 Ω via the star path.
   If a subsystem reads 0 Ω via two different paths, a loop exists.

---

## Rationale

### Why star grounding is enforced as a layout rule, not a tuning recommendation

Ground loops are not always immediately apparent in flight — they may cause
intermittent noise that appears only at certain throttle levels or motor speeds.
By the time a ground loop is identified as the cause of a problem, the build
is complete and rework is costly. Enforcing star ground topology during the
initial layout prevents the problem entirely. It is a wiring rule, not a
post-build tuning exercise.

---

## Connections

requires:
  - [[emc-noise-sources]]
related:
  - [[twisted-pairs]]
  - [[capacitor-placement-emc]]
  - [[power-signal-separation]]
leads_to:
  - [[capacitor-placement-emc]]


[emc-noise-sources]: emc-noise-sources.md "EMC noise sources in a drone"
[twisted-pairs]: twisted-pairs.md "Twisted pairs"
[capacitor-placement-emc]: capacitor-placement-emc.md "Capacitor placement for EMC"
[power-signal-separation]: power-signal-separation.md "Power and signal separation"
