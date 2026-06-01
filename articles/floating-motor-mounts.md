---
id: floating-motor-mounts
title: "Floating motor mounts"
version: 1.0.0
date: 2026-04-11
author: jsa
status: released
scope: libdrone
topic:
  - frame-structure
personas:
  - 1.builder
  - 2.operator
  - 4.workshop
  - 5.student
  - 7.contributor
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Every motor vibrates as it spins. On a rigid frame that vibration travels
directly into the gyroscope, which the flight controller reads as motion and
tries to correct — creating noise, filter latency, and degraded handling.
Floating motor mounts interrupt the vibration path mechanically at its source,
before it reaches the frame. Two silicone O-rings and four silicone sleeves
per motor act as a mechanical low-pass filter. The result is a cleaner gyro
signal, less aggressive software filtering, and lower control loop latency.

---

## Concept

### The vibration problem

A brushless motor spinning at 20,000–40,000 RPM is never perfectly balanced.
Minor imbalances in the rotor, asymmetries in the propeller, and bearing
tolerances all produce periodic forces at the motor's rotational frequency and
its harmonics. On a rigid frame these forces propagate through the arm, through
the body, and into the IMU with minimal attenuation.

The gyroscope samples angular velocity — it cannot distinguish between genuine
aircraft motion and frame vibration. Both appear as signal. The flight controller
attempts to correct for both, generating unnecessary motor commands that
themselves produce further vibration. The system develops oscillation that only
aggressive software filtering can suppress.

### Why mechanical isolation before software filtering

Software filters (RPM filter, dynamic notch) are effective but impose phase
delay. Every filter adds latency between a real motion event and the control
response. Aggressive filtering trades noise rejection for slower loop response —
the drone feels sluggish and is less capable of rejecting external disturbances
such as wind gusts.

Mechanical isolation attenuates vibration before the signal reaches the gyro,
so the software filter can be configured less aggressively. The same signal
quality is achieved at lower latency cost.

The principle generalises: solve the problem as close to its source as possible.
The floating mount addresses vibration at the motor interface. The RPM filter
addresses what remains in software. Both work on the same problem at different
levels of the signal chain.

### How silicone isolators work

The O-rings and sleeves are viscoelastic — they deform under load and dissipate
energy as heat. Their stiffness and damping properties create a mechanical
low-pass filter with a resonance frequency well below the motor's operating RPM
range. Above resonance, attenuation increases at approximately 12–20 dB per
octave. At typical operating RPM (15,000–35,000 RPM / 250–580 Hz) the
attenuation is substantial.

Shore hardness determines the filter characteristics. Softer silicone (30–40A
for sleeves) provides lower resonance frequency and more damping but less
positional stability. Firmer silicone (40–50A for O-rings) provides a stiffer
interface at the bolt axis. The combination is tuned for the mass of the motor
and the stiffness of the PETG arm head.

---

## Reference

### Per-motor bill of materials

| Component | Specification | Qty | Notes |
|---|---|---|---|
| O-ring | Silicone (VMQ), ID 4.0 / OD 7.0 / CS 1.5 mm, 40–50A Shore | 2 | Seats between motor base and arm head top surface |
| Sleeve | Silicone, OD 6.0 / ID 3.5 / L 11.5 mm, 30–40A Shore | 4 | One per bolt hole, prevents metal-to-metal contact at bolt shaft |
| Screw | M3 × 20 mm stainless steel | 4 | Through motor base → sleeve → arm head |
| Nut | M3 nyloc, captured in passive cover | 4 | Pre-captured — do not overtighten |
| Lubricant | Super Lube 52004 (PTFE-based, silicone-compatible) | — | Applied to O-rings and sleeve outer surface at assembly |

### Mass budget (per motor)

| Item | Target mass |
|---|---|
| O-rings × 2 | 0.5 g |
| Sleeves × 4 | 1.0 g |
| Total isolation hardware | 1.5 g |
| Total × 4 motors | 6.0 g |

### Torque specification

`motor_mount_screw_torque = 0.4–0.5 N·m`

Do not exceed 0.5 N·m. Over-torquing compresses the O-rings fully, eliminating
the air gap and creating a rigid metal-to-metal contact path through the bolt
shaft — negating isolation entirely.

### Replacement interval

Replace O-rings and sleeves every 20–30 flight hours, or immediately if:
- Visual inspection shows cracking, tearing, or permanent deformation
- Blackbox shows elevated vibration signature at motor frequencies
- Any motor mount exhibits play beyond normal isolation compliance

### Critical clearance

The passive cover must contact the arm head surface only through the O-ring
bosses. Any direct contact between passive cover and arm head creates a rigid
bypass path that short-circuits the isolation. Verify clearance at assembly.

---

## Procedure

### Initial assembly

1. Apply a thin film of Super Lube 52004 to the outer surface of each sleeve
   and to both O-rings. Do not use petroleum-based lubricants — they degrade
   silicone.
2. Insert one sleeve into each bolt hole in the motor base, lubricated side
   outward. The sleeve should sit flush with the motor base surface.
3. Place one O-ring in each O-ring boss on the arm head top surface.
4. Lower the motor base onto the arm head, aligning bolt holes with O-ring
   bosses. The O-rings should be captured between motor base and arm head.
5. Thread M3 × 20 mm screws through motor base → sleeve → arm head, engaging
   the pre-captured nyloc nut in the passive cover.
6. Tighten to 0.4–0.5 N·m using a torque driver. Tighten in a cross pattern.
7. Verify: passive cover does not contact arm head surface directly anywhere
   except through O-ring bosses. Slide a 0.1 mm feeler gauge around the
   perimeter — it should pass freely everywhere except at the O-ring contact
   zones.

### Routine inspection (every flight or post-crash)

1. Visually inspect all four O-rings for cracking or deformation.
2. Check that each motor mount has no lateral play beyond soft compliance.
3. Check screw torque if any mount feels loose — re-torque to 0.4–0.5 N·m.
4. Check Blackbox motor frequency peaks if any unusual vibration was felt
   during flight.

### O-ring and sleeve replacement

1. Loosen all four screws per motor (do not remove until all are loose).
2. Remove screws, passive cover, and motor base.
3. Remove old O-rings and sleeves. Inspect arm head O-ring bosses for wear.
4. Clean all surfaces with isopropyl alcohol. Allow to dry fully.
5. Install new components following initial assembly procedure above.

---

## Rationale

### Why VMQ (vinyl methyl silicone) specifically

VMQ silicone maintains consistent Shore hardness across the operating
temperature range (−50°C to +200°C). Standard silicone variants exhibit
significant stiffness increase below 0°C, which raises the isolation resonance
frequency and reduces attenuation effectiveness in winter conditions. VMQ is
specified to preserve isolation performance year-round.

Rubber O-rings (NBR, EPDM) were considered and rejected. Rubber provides
comparable stiffness at room temperature but degrades faster under UV and ozone
exposure, and stiffens substantially in cold weather. The mass penalty of VMQ
over rubber is negligible.

### Why 40–50A for O-rings, 30–40A for sleeves

The O-rings carry the compressive load of the motor weight and thrust reaction.
Firmer durometer (40–50A) prevents excessive sag under sustained thrust loads
that would allow motor tilt and change the propeller disc angle.

The sleeves primarily provide radial isolation at the bolt shaft. Softer
durometer (30–40A) at the bolt shaft provides more compliance in the radial
direction — the dominant vibration axis — without affecting vertical stiffness.

### Why Super Lube 52004 and not other lubricants

Petroleum-based lubricants (WD-40, mineral oil, standard greases) swell and
degrade silicone over time, reducing Shore hardness and accelerating cracking.
Super Lube 52004 is PTFE-based with a silicone-compatible carrier — it
lubricates without chemical interaction. No substitution without verification
of silicone compatibility.

### Why nyloc nuts captured in passive cover

Vibration will loosen standard nuts on a drone in service. Nyloc nuts are
specified throughout for vibration resistance. Pre-capturing them in the passive
cover simplifies assembly and prevents loss — a dropped nut inside a built
drone is difficult to recover.

---

## Connections

requires:
  - [[frame-structure-overview]]
  - [[arm-shaft]]
related:
  - [[vibration-isolation-theory]]
  - [[imu-filter-tuning]]
  - [[pid-tuning-rate-profile]]
  - [[winter-protocol]]
  - [[blackbox-analysis]]
  - [[pre-tensioning]]
leads_to:
  - [[electronics-installation]]
  - [[scheduled-maintenance]]
