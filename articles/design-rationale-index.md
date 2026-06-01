---
id: design-rationale-index
title: "Design rationale index"
version: 2.0.0
date: 2026-04-15
author: jsa
status: released
scope: libdrone
topic:
  - open-source-philosophy
personas:
  - 7.contributor
  - 8.architect
  - 5.student
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Every significant design decision in libdrone has a documented rationale —
not just what was decided, but why, and what alternatives were rejected.
This index maps the major decisions to the atoms that contain their rationale.
It serves contributors who want to understand the reasoning before proposing
changes, architects who need to understand load-bearing constraints before
forking, and students who want to see engineering thinking applied to a real
system they can hold. The rationale for each decision lives in the owning
atom's Rationale section — this article is the map.

---

## Concept

### Why design rationale matters more than design decisions

A design decision without documented rationale looks arbitrary to the next
person who encounters it. They will either follow it blindly — possibly in
a context where the original reasoning no longer applies — or override it
without understanding what they are losing. Documented rationale transforms
a constraint into a principle: "we chose X because Y, given constraints A
and B." When Y changes or A and B no longer hold, the decision can be
revisited intelligently rather than by accident.

For an open-source platform, documented rationale is also the institutional
memory. The original designer cannot be in every future discussion. The
index is.

### The three categories of decision

**Structural decisions** are the hardest to reverse — changing the arm
attachment, the connector standard, or the battery chemistry requires
physical redesign. Their rationale must be explicit because the cost of
changing one's mind is high.

**Configuration decisions** are reversible but interdependent — changing
the ESC firmware, the loop rate, or the GPS constellation requires
recalibration or retuning. Their rationale explains which changes are
safe to make independently and which require cascading updates.

**Decisions reversed** are the most valuable entries in this index.
When a decision was made, reconsidered, and changed — dual GX12 replacing
single, battery spoiler removed, Core gaining the full payload interface —
the reversal reveals what the original decision was protecting against and
what evidence changed the calculus. These entries contain more engineering
thinking per word than any others.

---

## Reference

### Structural and mechanical decisions

| Decision | Atom | Why — and why not the alternative |
|---|---|---|
| Five-layer PETG-PCCF-PCCF-PCCF-PETG sandwich | [[sandwich-structure]] | Each material zone plays a distinct structural role; PETG faces absorb impact, PCCF core carries load. Single-material construction cannot optimise both simultaneously. |
| Arms as crash-sacrificial fuses | [[failure-hierarchy]] | The arm costs cents; the FC costs €55. Designing the arm to fail first and predictably means crashes are a 5-minute field repair, not an electronics replacement. |
| Floating motor mounts — silicone O-rings | [[floating-motor-mounts]] | Isolates vibration at source before it reaches the IMU. Shore 40–50A silicone: stiff enough to resist motor torque, compliant enough to isolate 500Hz+ frequencies. TPU was considered but fails below −10°C. |
| 2.0mm CF rods through all five sandwich layers | [[cf-rod-architecture]] | Rods pre-tension the assembly and serve as the assembly alignment tool simultaneously. Four rods at offset heights form a closed box section — torsional stiffness orders of magnitude above an open profile. |
| Pre-tensioning via interference fit (not set screw) | [[pre-tensioning]] | Zero mass, zero maintenance, cannot loosen. A set screw adds a stress concentration point and requires Loctite. Interference fit is established correctly or incorrectly at print time — the print is the quality gate. |
| Exact constraint in T-slot tab system | [[exact-constraint-design]] | Tab constrained in two lateral DOFs by slot, rod provides axial. Deliberate floating in assembly direction accommodates ±0.3mm print tolerance without internal stress. Over-constraint cracks PCCF. |
| Zonal stiffness: stiff body, compliant arms | [[zonal-stiffness]] | Routes crash energy to the sacrificial zone. A frame with uniform stiffness fails unpredictably. A frame with a designed stiffness gradient fails at the arm base, every time. |
| Arm tabs as separate parts from the shaft | [[arm-shaft]] | Tabs remain in the sandwich when the shaft fractures. Shaft replacement requires no sandwich disassembly — 4 M2 screws, under 5 minutes. Integral arm-and-tab designs require full disassembly after every crash. |
| PETG for arm shafts (not PC-CF, not ASA) | [[petg]] | Controlled ductile fracture. PETG bends and cracks predictably in the designed direction. PC-CF shatters unpredictably, potentially into the propellers. ASA is stiffer than PETG at equivalent geometry — less energy absorption. |
| PC-CF for sandwich structural layers | [[pccf]] | High modulus (8–12 GPa) needed for T-slot dimensional precision. PETG's lower modulus (1.5–2 GPa) would deform under rod pre-tension, losing the stack geometry. |
| TPU 95A for Bandit arm shafts | [[bandit-variant]] | Bandit is a training platform — crash frequency is higher than Pro. TPU absorbs crash energy and recovers shape rather than fracturing, enabling shorter inter-crash repair cycles. PETG fracture is correct for Pro; TPU deformation is correct for Bandit. |
| CF plate arms on Ghost (not printed) | [[cf-plate-arms]] | 12-inch arms require bending stiffness that printed polymer cannot provide at 210mm span. 2mm CF plate is 15× stiffer than equivalent PETG cross-section. The non-printable trade-off is accepted because Ghost is a specialist platform, not a community build. |
| 6-bolt sandwich pattern (not 4-bolt) | [[sandwich-structure]] | Nose and tail perimeter bolts added at V2.4.5 to address bowing in the fore/aft body under battery weight. 4-bolt corner-only pattern allowed the long axis to flex under load. 6-bolt eliminates measurable deflection. |
| True-X geometry | [[frame-structure-overview]] | Equal moment arms to all four motors gives symmetric PID response and equal prop clearance. H-frame reduces yaw authority and complicates motor mixing without benefit for this mission profile. |
| ASA for bumpers only | [[asa]] | UV stability required for field-exposed surfaces accumulating hundreds of flight hours. PETG yellows and weakens under prolonged UV. ASA is not used structurally because it is less predictable as a crash element than PETG. |

### Electronics and EMC decisions

| Decision | Atom | Why — and why not the alternative |
|---|---|---|
| Star grounding at ESC pad | [[star-grounding]] | All high-current return paths terminate at the battery negative pad on the ESC. Ground loops between distributed return paths are the primary EMC noise source — star topology eliminates them structurally. |
| 1000µF capacitor directly on ESC pads | [[capacitor-placement-emc]] | Wire inductance of even 50mm of lead wire defeats the capacitor's function during motor back-EMF spikes. Distance is performance — the capacitor must be on the pads, not on a pigtail. |
| Three-zone power/signal routing | [[power-signal-separation]] | Physical separation of high-current, low-current, and signal zones into the Platform geometry. Software filtering addresses the symptoms of poor routing; physical separation addresses the cause. |
| GPS mast height derived from recirculation zone | [[induced-velocity]] | The toroidal recirculation zone extends 80–120mm above the rotor disk. Mast height is set to the minimum that clears this zone — not shorter (contaminates sensor data), not longer (increases pendulum arm and changes PID tuning). |
| External compass only — FC internal disabled | [[barometer-magnetometer]] | Motor current creates magnetic fields that corrupt the onboard compass at the distances typical in a 330mm frame. External compass on mast at 40mm above prop plane: sufficient separation for clean heading data. COMPASS_USE2=0 is not optional. |
| Matek H7A3-SLIM FC | [[flight-controller-hardware]] | H7 class required for 8kHz loop rate plus RPM filter simultaneously. IMU moat provides a second isolation stage. F4 can run 8kHz but not RPM filter without dropping to 4kHz. The H7A3 runs both with 33% processor headroom remaining. |
| Pilotix AM32 ESC | [[electronic-speed-controllers]] | Open firmware. Bidirectional DShot telemetry. EU-accessible supply chain. BLHeli_32 went closed in 2022 — vendor lock-in risk in a platform explicitly designed to avoid it. |
| Ferrite bead on VTX power | [[ferrite-beads]] | XL4015 buck converter switches at 180kHz, injecting noise onto the 9V VTX rail. Ferrite bead provides frequency-selective attenuation without the resonance risk of an LC filter. |
| GLONASS disabled | [[gps-antenna-placement]] | Russian military jamming of GLONASS is documented at EU borders and in active conflict zones. Disabling GLONASS removes a known-jammable constellation without reducing position accuracy — GPS + Galileo + BeiDou is sufficient. |
| Conformal coating before first flight | [[conformal-coating]] | Moisture-induced shorts are the leading cause of electronics failure in field deployments. Coating is applied once and lasts the lifetime of the board — the cost is 20 minutes, the benefit is permanent. |

### Wire and power decisions

| Decision | Atom | Why — and why not the alternative |
|---|---|---|
| 12 AWG for battery-to-ESC backbone | [[wire-gauge-selection]] | 40A continuous rating provides margin above 6S peak draw. Undersized wire generates heat and voltage sag that appear as reduced motor performance before the wire fails visibly. |
| Colour discipline: red/black power, blue/green signal | [[wire-gauge-selection]] | Field rewiring in poor light by a fatigued operator. Colour code must survive the worst maintenance context without a wiring diagram. |
| Twisted pairs on motor phase wires | [[twisted-pairs]] | Motor phase wires carry fast-switching high current — strong RF emitters. Twisting cancels the magnetic field and eliminates the wire-as-antenna problem. |

### Software, firmware and protocol decisions

| Decision | Atom | Why — and why not the alternative |
|---|---|---|
| Betaflight for Pro/Core (not ArduPilot) | [[betaflight-setup]] | 8kHz PID loop, RPM filter, aggressive tuning for manual payload flight. ArduPilot's conservative PID loop is optimised for autonomous stability, not dynamic payload repositioning. |
| ArduPilot for Bandit/Ghost/Wing (not Betaflight) | [[ardupilot-copter]] | Autonomous mission execution, EKF sensor fusion, MAVLink telemetry, and QGroundControl integration require ArduPilot. Betaflight GPS Rescue is a failsafe, not a mission executor. |
| ArduPilot over PX4 for autonomous variants | [[ardupilot-copter]] | Largest community-validated parameter set for MatekH7A3 target. Deepest QGroundControl and ATAK integration. PX4 is equally capable but MatekH7A3 community documentation is sparse. |
| ELRS MAVLink mode (not separate SiK radio) | [[elrs-mavlink-mode]] | The RC link already exists. ELRS ≥3.5 carries RC and MAVLink telemetry on one UART simultaneously. SiK adds 15–30g, a second UART, and a second antenna. The discovery that the existing link was sufficient eliminated the SiK from the BOM. |
| ELRS at 250Hz LBT (not 500Hz, not 50Hz) | [[elrs-protocol]] | EU LBT regulatory compliance requires Listen Before Talk. 250Hz balances latency (sufficient for survey missions) against range (better than 500Hz). 50Hz would be acceptable for mapping but creates sluggish manual response during training phases. |
| AM32 over BLHeli_32 | [[foss-stack-libdrone]] | BLHeli_32 went closed source in 2022. AM32 is MIT-licensed, actively maintained, supports BiDi DShot. Any firmware that can go closed can go abandoned — AM32's openness is a reliability argument, not just a philosophy argument. |
| MSP DisplayPort for OSD | [[digital-fpv]] | FC generates all OSD data via MSP; HDZero VTX renders it. No custom OSD hardware. Any FC that supports MSP DisplayPort works without modification. |
| 8kHz PID loop (not 4kHz or 1kHz) | [[pid-loop-rate]] | Lower loop latency allows higher PID gains at the same stability margin. Higher P gain means better disturbance rejection in wind. The H7A3's hardware FPU makes 8kHz plus RPM filter possible simultaneously — on F4 it required choosing one or the other. |
| RPM filter over static notch filter | [[rpm-filter]] | Motor frequencies move with throttle. A static notch placed at a fixed frequency misses the noise except at one throttle point. RPM filter tracks the noise wherever it goes using BiDi DShot eRPM telemetry — the notch always sits exactly on the motor harmonic. |

### Payload interface decisions

| Decision | Atom | Why — and why not the alternative |
|---|---|---|
| GX12-7 as the payload connector standard | [[gx12-connector-standard]] | IP65 weather sealing. D-D anti-rotation (payload cannot be inserted incorrectly). 500+ cycle rating. No single-vendor dependency — aviation-grade connectors from multiple sources. Custom PCB edge connectors were considered and rejected: no IP rating, no mechanical keying, fragile in field conditions. |
| Dual connectors A and B (not single) | [[gx12-icd]] | Separating power and signal between two connectors eliminates power line noise coupling onto signal lines. A single connector carrying both is an EMC problem by design. The separation also allows payload power to be switched independently of signal. |
| Dual GX12-7 mandatory on ALL variants (including Core) | [[core-variant]] | A payload built on Core must fly on Pro without modification. If Core had a simplified connector, every payload developer would need to build and test on two interface versions. Standardising the interface across all capable variants collapses this to one. Students learn the real interface from day one — not a substitute. |
| GX12-7 replaced GX12-12 at V2.4.6 | [[gx12-connector-standard]] | GX12-12 (12-pin) was over-specified for the actual signal count required. Larger connector, more pins to solder, higher failure probability. 7-pin carries all required signals with two reserved for future use. Smaller connector fits the chimney geometry with better structural margin. |
| Payload master enable logic (physical + radio AUX in OR) | [[payload-integration]] | Either source enables the payload independently. Physical switch allows bench testing and pre-flight logging before drone power is connected. Radio AUX allows in-flight payload control. Neither alone is sufficient for both use cases. |

### Platform family decisions

| Decision | Atom | Why — and why not the alternative |
|---|---|---|
| Five variants (not one configurable platform) | [[platform-selection]] | Different missions require different physics: a 12-inch low-RPM platform cannot be made from a 6-inch high-RPM platform by configuration change. The motor, battery chemistry, and arm architecture differ fundamentally. Configuration flags on a single design would produce compromise in every direction. |
| Bandit on Core scale (220mm), not Pro scale (330mm) | [[bandit-variant]] | Bandit's primary missions (awareness curriculum, survey training, ATAK integration drills) do not require Pro's payload capacity. Smaller scale reduces BOM cost, keeps AUW below 500g, and makes the platform more forgiving during Phase 1 training when crashes are frequent. |
| Ghost uses Li-Ion (not LiPo) | [[li-ion-batteries]] | Ghost's operating profile — large props at low RPM, low average current draw, long hover endurance — is exactly where Li-Ion's energy density advantage materialises without the discharge rate becoming a constraint. LiPo would provide similar capacity at 25–30% higher weight. |
| Ghost arms not 3D-printable | [[cf-plate-arms]] | The stiffness requirement at 540mm wheelbase cannot be met by printed polymer without exceeding the weight budget. The trade-off was accepted explicitly: Ghost is a specialist platform, not a community build, and the DXF-to-laser-cut workflow is accessible to a narrower audience by design. |
| Core retains sub-250g target | [[core-variant]] | EASA Open A1 removes operator licence and airspace notification requirements in most scenarios. For educational deployments in school yards and events, this regulatory access is operationally decisive. 250g is not an accident — it is a calculated constraint on every other Core design decision. |
| Wing fixed-wing (not extended endurance multirotor) | [[fixed-wing-fundamentals]] | Area coverage efficiency is categorically different between fixed-wing and multirotor — 3–5× more area per watt at survey speeds. Extended endurance multirotors (like Ghost) close the gap somewhat but cannot reach the area coverage rate of a fixed-wing at the same battery weight. |

### Operational and IFF decisions

| Decision | Atom | Why — and why not the alternative |
|---|---|---|
| Five-layer IFF architecture (L1 IR strobe through L6 reserved) | [[iff-architecture]] | Each layer adds coverage where layers above it fail. IR strobe works without any electronics. Remote ID works without network. ATAK works without internet. Each successive layer requires more infrastructure and is available in fewer contexts. |
| ESP32-S3 mandatory on Ghost and Wing | [[esp32-s3-companion]] | Ghost operates in security-sensitive contexts where ATAK presence and Remote ID are not optional. Making the ESP32-S3 mandatory rather than optional eliminates the "I forgot to fit it" failure mode on a platform where IFF matters most. |
| EMCON kill switch cuts all RF simultaneously | [[operational-security]] | A kill switch that requires individual disabling of VTX, BLE, WiFi, and Remote ID is a switch the operator will misconfigure under stress. A single latching toggle that cuts all ESP32-S3 RF in one action is the only design that works in time-critical operational contexts. |
| Non-weaponisation declaration as a licence condition | [[foss-principles]] | CERN OHL-S v2 permits all uses. The non-weaponisation declaration adds an explicit use restriction beyond what the licence requires. It is not legally watertight in all jurisdictions but it communicates the platform's intent unambiguously and must be retained in all forks. |
| Zero cloud dependency as a design constraint | [[civilian-preparedness]] | The most critical deployments — emergency response, infrastructure assessment after disruption — occur when networks fail. Any feature that requires internet connectivity fails at exactly the moment it is most needed. Cloud dependency is architectural debt that compounds in crisis conditions. |

### Decisions revisited and reversed

These entries are particularly valuable: they reveal what the original
decision was protecting against, and what evidence changed the calculus.

| Original decision | Reversed to | Atom | What changed |
|---|---|---|---|
| Battery spoiler as a structural extension | Removed entirely in V2.4.6 | [[variable-table-values]] | Spoiler added mass and manufacturing complexity without measurable structural benefit. Battery side-slide rails provided equivalent battery retention with lower parts count. |
| GX12-12 (12-pin connector) | GX12-7 (7-pin) | [[gx12-connector-standard]] | Actual signal count was 5 used + 2 reserved. 12-pin oversized the chimney, added mass, increased solder joint count. Smaller connector with reserved pins for growth is the correct standard. |
| Core: no payload interface | Core: dual GX12-7 mandatory | [[core-variant]] | Original rationale was cost and complexity reduction. Reversed when the implication became clear: any payload developer targeting Core would need a second connector variant. Platform standard coherence outweighs the cost saving. |
| Single GX12-7 per platform | Dual GX12-7 A/B | [[gx12-icd]] | EMC analysis showed power-signal coupling on a single connector was unacceptable for sensor payloads measuring sub-millivolt signals. Two connectors with physical separation between power and signal domains is not optional for clean sensor data. |
| 4-bolt sandwich pattern | 6-bolt pattern (V2.4.5) | [[sandwich-structure]] | Fore/aft body bowing under battery weight was measured on assembled frames. Corner-only bolt pattern left the long axis unsupported. Nose and tail perimeter bolts at (0, +22mm) and (0, −22mm) eliminated the deflection. |
| Betaflight GPS Rescue as autonomous capability | ArduPilot Copter on Bandit | [[ardupilot-copter]] | GPS Rescue is a failsafe — it returns the aircraft to home and lands. It cannot execute a waypoint survey, maintain a mission on GCS link loss, or integrate with QGroundControl. The use case required a real autopilot, not a glorified failsafe. |

---

## Procedure

<!-- not applicable -->

---

## Rationale

This index exists as a dedicated article rather than a section inside
`platform-architecture` because the decision record is a living document.
New articles add entries, decisions get revisited, alternatives previously
rejected may become viable as technology changes. A dedicated article allows
the index to be updated without touching the architecture overview. It also
gives contributors a single search target: the answer to "why does libdrone
do X this way?" always starts here.

Version 2.0.0 adds three improvements over v1.0.0: expanded coverage of
decisions made during the 3.0.0 documentation pass, a new section for
platform family decisions that explains why five variants exist rather than
one, and a dedicated "decisions reversed" section — the most informative
entries in any design record, because reversals reveal what the original
decision was actually protecting.

---

## Connections

requires:
  - [[platform-architecture]]
related:
  - [[schema-specification]]
  - [[contributing-guide]]
  - [[failure-hierarchy]]
  - [[sandwich-structure]]
  - [[foss-principles]]
  - [[platform-selection]]
  - [[gx12-connector-standard]]
  - [[ardupilot-copter]]
  - [[iff-architecture]]
leads_to:
  - [[contributing-guide]]
  - [[platform-selection]]
