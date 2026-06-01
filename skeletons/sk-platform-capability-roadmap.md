---
id: sk-platform-capability-roadmap
title: "Platform Capability Roadmap"
version: 1.1.0
date: 2026-06-01
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 8.architect
  - 7.contributor
  - 6.evaluator
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

This document maps the honest gap between libdrone's current capability and
enterprise-grade drone platforms. It exists for one reason: to make the
contribution path obvious to whoever picks it up. No promises are made about
timelines or delivery. Some gaps are closeable by a single skilled contributor
in weeks. Others require sustained platform investment. All of them are
documented here with enough technical specificity to start work tomorrow.
The frame: if libdrone is to become infrastructure that serious operators —
including those in demining, civil defence, and contested-environment survey
— can stake real operations on, these are the capabilities that close the
distance.

---

## Concept

### Why this document exists

Enterprise drone platforms — DJI Matrice, Autel EVO Max, Skydio X10 — are
technically impressive. They are also closed, cloud-dependent, foreign-made,
and opaque. For the growing number of institutional operators who cannot
accept those conditions, no credible open alternative exists at the sub-€2,000
price point. libdrone is the nearest candidate. The gap between "nearest
candidate" and "viable alternative" is specific and mappable. This document
maps it.

The secondary audience is the unknown contributor. Somewhere there is a
systems engineer who spent three years on RTK modules for a mining company and
now has six months of free time. There is a robotics PhD student whose
demining NGO contact just asked whether an open platform could do systematic
area coverage. There is a FOSS developer who built a gimbal controller for a
previous project and never found the right platform to contribute it to. This
document tells them exactly where the door is.

### What counts as a gap

A gap is a capability that enterprise platforms deliver as standard and
libdrone either does not deliver at all, delivers only partially, or delivers
only on one platform variant. The assessment is honest: where libdrone is
already competitive, that is stated. Where the gap is fundamental and
requires months of work, that is stated. Where a single contributor with the
right background could close a gap in weeks, that is stated.

### The Ukraine/demining context

This framing is not rhetorical. Ukraine has approximately 174,000 km² of land
contaminated with mines and unexploded ordnance — roughly one-third of the
country's territory. Systematic survey of that area requires aerial platforms
that can: execute precise waypoint coverage, georeference every data point
reliably, operate without cloud dependency, be repaired in the field by a
technician with a 3D printer and basic electronics skills, and be audited by
any operator without vendor access. No commercial platform satisfies all five
conditions. libdrone satisfies four of them today. The fifth — precise
georeferencing — is the RTK gap described below.

The demining use case also reshapes the priority order. Gimbal stabilisation
and AI inference are secondary to: RTK accuracy, reliable BVLOS range,
systematic area coverage, and GPS jamming resistance. The gap table below
reflects this ordering.

---

## Reference

### Capability gap table

| Capability | libdrone today | Enterprise standard | Gap | Contributor effort |
|---|---|---|---|---|
| Positioning accuracy | EGNOS, 0.5–1.5 m CEP | RTK, 1–2 cm CEP | 100× | Medium — F9P module |
| Autonomous waypoint nav | ArduPilot on Bandit | Universal | Solved on Bandit | None |
| MAVLink / QGroundControl | Bandit only | Universal | Medium on Pro | LCM-1 bridge |
| Gimbal stabilisation | None | 2–3 axis brushless | Complete gap | Medium — BaseCam FOSS |
| Thermal imaging | Lepton 3.5 (designed) | FLIR Vue Pro | Small | Nearly closed |
| Optical survey mapping | GPIO trigger only | Integrated camera | Large | Camera mount needed |
| BVLOS link range | ELRS 2.4GHz, ~5 km | Cellular fallback | Medium | 900 MHz ELRS module |
| Swarm / multi-agent | None | Proprietary | Complete gap | Hard |
| Edge AI inference | Pi Zero 2W (limited) | Jetson / NPU class | Large | Coral TPU fits bay |
| GPS jamming resistance | None | Partial | Significant | Hard |
| Data encryption at rest | None | Partial | Medium | Software only |
| Systematic area survey | ArduPilot AUTO mode | Integrated | Solved on Bandit | None |
| Remote ID compliance | Module required | Integrated | Small | Module already exists |
| Precision landing | None | Optical / lidar | Medium | Lidar payload module |

### Gap 1 — RTK positioning

**Current state:** libdrone uses the Matek M10Q-5883 (u-blox M10 chip) with
EGNOS SBAS augmentation. Position accuracy: 0.5–1.5 m CEP under good sky.
→ [[gnss-gps]]

**Enterprise standard:** RTK (Real-Time Kinematic) achieves 1–2 cm horizontal
accuracy by computing carrier-phase corrections between the airborne receiver
and a fixed base station or NTRIP correction network. For mine survey,
construction mapping, or precision agriculture, this is the minimum viable
accuracy.

**The gap in practice:** A 1 m position error means a grid survey pass
covering 20 m track spacing will have ±1 m uncertainty on every data point.
For air quality mapping at neighbourhood scale, this is acceptable. For mine
clearance survey where a false negative at 1 m offset may mean an undetected
device, it is not.

**What closing it requires:**
- An RTK-capable GNSS receiver payload module. The u-blox F9P (SparkFun
  GPS-RTK2, ~€80) outputs centimetre-accurate position via UART at 10 Hz.
  It connects to Connector B PIN 3/4 (UART5) on the GX12 interface.
- Either a local base station (second F9P with antenna, ~€150) or an NTRIP
  subscription (commercial correction network, ~€20–50/month).
- Firmware on the payload MCU to forward RTK-corrected NMEA to the SD card
  and override the standard GPS tap position with corrected coordinates.
- No changes to the drone airframe, FC firmware, or payload interface.

**Contributor profile:** someone with u-blox F9P experience. The hardware
integration is mechanical and electrical, not exotic. The firmware is UART
parsing and NMEA forwarding. Estimated effort: 3–6 weeks for a contributor
familiar with the platform.

### Gap 2 — MAVLink on Pro

**Current state:** The Bandit platform runs ArduPilot with full MAVLink
telemetry via ELRS MAVLink mode. → [[elrs-mavlink-mode]], [[ardupilot-copter]]
The Pro platform runs Betaflight, which does not natively speak MAVLink.

**Enterprise standard:** MAVLink is the universal drone protocol. QGroundControl,
Mission Planner, and ATAK all speak MAVLink. An operator who cannot connect
their drone to QGC cannot plan systematic area missions, cannot view a moving
map, and cannot integrate with command-and-control infrastructure.

**What closing it requires:**
The Pi Zero 2W in the Pi bay (→ [[lcm1-spec]]) has a permanent UART6
connection to the FC at 921,600 baud. The companion computer can run a
MAVLink-to-MSP bridge (MAVLink router + MSP bridge firmware). This gives Pro
platform operators a QGC connection without reflashing the flight controller.
The tradeoff: latency is higher than native ArduPilot MAVLink. For mission
planning and telemetry it is irrelevant. For control authority it is not the
right path — use Bandit for autonomous missions.

**Contributor profile:** someone comfortable with MAVLink routing and
MicroROS/MAVLink2 on embedded Linux. The companion UART is already wired.

### Gap 3 — Gimbal stabilisation

**Current state:** No gimbal. Cameras and sensors mount on fixed masts.
At wind speeds above ~3 m/s, a fixed camera produces jello-corrupted imagery
unsuitable for photogrammetric reconstruction.

**Enterprise standard:** 2–3 axis brushless gimbal controllers are universal
on professional mapping platforms. The market standard open-source controller
is SimpleBGC (BaseCam Electronics). Fully open API, documented serial protocol,
actively maintained.

**What closing it requires:**
- A gimbal mechanical design for the payload bay — a 2-axis brushless gimbal
  that mounts to the existing M3 boss pads at 20 mm spacing. Mass budget: the
  gimbal mechanism must stay under ~60 g to leave budget for camera.
- A BaseCam SimpleBGC Mini controller (~€60) connected to Connector B PIN 3/4
  (UART5) for FC-commanded axis control.
- GX12 power tap: the gimbal motors draw 0.5–1.5 A peak — within the 2 A
  limit on Connector A PIN 1.
- No changes to the drone airframe required. The boss pad footprint is the
  mechanical interface.

**Contributor profile:** someone with brushless gimbal design and tuning
experience. The electrical integration is straightforward. The mechanical
design requires FreeCAD proficiency. → [[freecad-parametric-scaling]]

### Gap 4 — BVLOS link range

**Current state:** ELRS 2.4 GHz at 250 Hz LBT with 100 mW achieves practical
range of 3–5 km in open terrain. For urban survey in a RF-congested
environment, this decreases significantly. → [[elrs-protocol]]

**Enterprise standard:** Commercial BVLOS platforms use cellular (4G/5G LTE)
as a primary or fallback link, extending range to tens of kilometres with
reliable telemetry.

**What closing it requires at FOSS:**
ELRS supports 900 MHz operation (SX1276 chip, Radiomaster Ranger module).
At 900 MHz with equivalent power, range extends to 15–30 km in flat terrain.
The TX16S ELRS bay accepts a Ranger module as a direct swap. On the drone
side, the RP2 2.4 GHz receiver is replaced with a 900 MHz receiver.
Regulatory note: 900 MHz ELRS output power in the EU is limited to 25 mW
ERP in the 868 MHz ISM band — less than the 2.4 GHz capability, but the
propagation advantage at 900 MHz more than compensates at range.

Cellular via the Pi Zero 2W companion is the longer-range path: a 4G USB
dongle + WireGuard tunnel provides MAVLink telemetry over cellular with
no range limit. RC authority over cellular is not safe practice — this is
telemetry and monitoring only.

### Gap 5 — Edge AI inference

**Current state:** The Pi Zero 2W (→ [[lcm1-spec]]) provides Linux-class
compute in the Pi bay. It runs threshold logic and event filtering adequately.
It does not run real-time neural network inference at useful frame rates.

**Enterprise standard:** DJI Dock 2 onboard processing, Skydio's onboard
obstacle avoidance, and demining-specific AI (mine signature detection in
multispectral or ground-penetrating radar data) all require inference at
5–30 fps with sub-second latency.

**What closing it requires:**
The Pi bay internal dimensions (72 × 38 × 6 mm) do not physically
accommodate a Raspberry Pi 4 or Jetson Nano. However, the Google Coral USB
Accelerator (30 × 65 × 8 mm, ~30 g) connects to the Pi Zero 2W USB port and
runs TensorFlow Lite models at 4 TOPS. Object detection at 10–30 fps is
feasible on a Coral + Pi Zero 2W combination within the existing bay geometry.

For heavier inference workloads, the next step is a Pi bay redesign to
accommodate a CM4 (Compute Module 4, 55 × 40 × 4.7 mm, 16 TOPS with
appropriate carrier board). This requires FreeCAD changes to the platform
geometry — non-trivial but a single well-defined design task.

**Contributor profile:** ML engineer with embedded Linux experience.
Hardware path is clear. Model selection depends on the target application
(mine detection vs. structural survey vs. person detection).

### Gap 6 — GPS jamming resistance

**Current state:** No jamming detection or mitigation. A hostile jammer at
~1 W within 5 km can deny GPS to the platform. The drone falls back to
barometric altitude hold and loses position awareness. → [[gnss-gps]]

**Enterprise standard:** Commercial platforms have limited mitigation:
multi-constellation receivers reduce susceptibility, some use inertial
dead-reckoning during outage. Military-grade anti-jam is not applicable here.

**What closing it requires:**
- Optical flow as a GPS-denied position hold fallback. → [[supplemental-sensors]]
  The Pi Zero 2W runs optical flow algorithms (px4flow protocol or OpenCV-based)
  and forwards position corrections to the FC via MAVLink over UART6.
- Anomaly detection: monitor GPS accuracy metrics (HDOP, satellite count,
  carrier-to-noise ratio). If metrics degrade abruptly, alert operator and
  switch to optical flow hold.
- This is a software and payload problem, not an airframe problem.

**Contributor profile:** computer vision engineer with MAVLink/ArduPilot
experience. Significant but well-defined work.

### What is already solved

These gaps are closed or not relevant to libdrone's primary use cases:

**Systematic area survey:** ArduPilot AUTO mode with survey grid missions
in QGroundControl is the enterprise standard. Bandit implements this
completely. → [[ardupilot-copter]], [[qgroundcontrol]]

**MAVLink / QGroundControl on Bandit:** Already solved. ELRS MAVLink mode
provides bidirectional telemetry. → [[elrs-mavlink-mode]]

**Data sovereignty:** By design. No cloud dependency, no vendor data
access, no subscription requirement. All data on SD card and local NAS.
→ [[foss-stack-libdrone]]

**Field repairability:** By design. Arm shafts are sacrificial and
print in 45 minutes. The entire airframe reprints in under 12 hours.
No proprietary spare parts. → [[failure-hierarchy]]

**EU regulatory compliance:** privately-built UAS under EASA; see
→ [[legal-and-regulatory]].

**FOSS stack end-to-end:** Every component from transmitter firmware
to FC to ESC to CAD tool is open source. Auditable by any operator.
→ [[foss-stack-libdrone]]

---

## Procedure

### If you want to contribute

1. Read the relevant atoms for your gap (linked above in each gap section)
2. Read → [[contributing-guide]] for corpus and hardware contribution process
3. The PSB-1 (→ [[psb1-build-guide]]) is the bench starting point for
   any payload-level contribution — it gives you the full electrical interface
   without a flying drone
4. Open an issue on the libdrone Gitea repo with your proposed approach
   before spending significant time — architecture decisions affect other
   contributors

### If you are evaluating libdrone for a specific mission

The gap table above maps to use cases directly:

| Use case | Critical gaps | Already solved |
|---|---|---|
| Mine/UXO area survey | RTK (Gap 1), BVLOS (Gap 4) | Waypoint nav, QGC, data sovereignty |
| Urban air quality mapping | None critical | EGNOS adequate at neighbourhood scale |
| Structural inspection | Gimbal (Gap 3) | Manual piloting, thermal payload |
| Civil preparedness monitoring | None critical | Thermal, FPV, ArduPilot AUTO |
| Research payload deployment | RTK if precision needed | Full payload SDK, open interface |

---

## Rationale

### Why honesty about gaps is an asset, not a liability

A platform that overstates its capability will fail in the field at exactly
the wrong moment. An operator who deploys libdrone for mine survey on the
strength of "sub-metre EGNOS accuracy" and discovers this means 1.5 m
error in dense forest cover has learned an expensive lesson. The gap table
above is written for the operator who needs to make a real decision about a
real mission. If the current capability is insufficient for that mission,
they should know before deployment, not after.

For contributors, honesty is also functional: a precise description of a
gap is a contribution specification. "RTK accuracy" is a marketing category.
"F9P UART5 connection to Connector B PIN 3/4 with NMEA forwarding to SD"
is a task.

### Why the demining frame is not rhetorical

The technical requirements for mine survey — RTK accuracy, systematic area
coverage, no cloud dependency, field repairability, open audit — overlap
almost exactly with the technical requirements for civilian resilience
deployment and research-grade environmental monitoring. A platform that
closes the demining gaps is simultaneously a competitive platform for
academic survey, municipal emergency response, and any institutional
context where data sovereignty is a procurement requirement.

The demining application concentrates the requirements into a single
high-stakes context that makes the gap priorities obvious. That clarity
is useful regardless of whether the contributor's actual target application
is Ukraine or a Czech municipality.

---

## Connections

requires:
  - [[platform-overview]]
  - [[payload-architecture]]
  - [[bandit-variant]]
leads_to:
  - [[contributing-guide]]
  - [[sk-payload-developer-guide]]
  - [[sk-libdrone-eu-nato-bridge]]
related:
  - [[gnss-gps]]
  - [[elrs-mavlink-mode]]
  - [[lcm1-spec]]
  - [[supplemental-sensors]]
  - [[foss-stack-libdrone]]
  - [[failure-hierarchy]]
  - [[civilian-preparedness]]
