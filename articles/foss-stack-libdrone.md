---
id: foss-stack-libdrone
title: "FOSS stack in libdrone"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - open-source-philosophy
personas:
  - 5.student
  - 6.evaluator
  - 7.contributor
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Every software and firmware component in libdrone was selected on FOSS criteria
first: auditability, vendor independence, and community maintainability. The
complete stack from transmitter firmware through flight controller, ESC, GPS
infrastructure, CAD tools, and payload firmware is open source or open standard.
Two known exceptions (HDZero VTX encoding firmware, Synology NAS DSM) are
acknowledged and are not in the critical path. The EU strategic autonomy
argument — using EU-origin infrastructure where it exists — adds Galileo and
EGNOS as deliberate choices over GPS-only. Contributing back to the FOSS
ecosystem is the expected behaviour of anyone who benefits from it.

---

## Concept

### Why the entire stack matters

A chain is only as open as its weakest proprietary link. A build that uses
open-source firmware on the FC but proprietary RC protocol on the radio link
has a single proprietary dependency that can strand the entire investment.
Selecting FOSS throughout the stack ensures that no single vendor decision
can disable the platform's core function.

### The EU strategic autonomy dimension

The European Union's strategic autonomy policy — articulated in the European
Chips Act, Cyber Resilience Act, and research funding frameworks — explicitly
addresses dependency on non-EU technology for critical infrastructure.

For institutions in the EU:
- Using EU-origin satellite navigation (Galileo + EGNOS) instead of GPS-only
  removes dependency on US military policy decisions (GPS Selective Availability
  demonstrated this risk is real)
- Using auditable open-source firmware addresses the EU Cyber Resilience Act's
  increasing requirements for software transparency
- Using CERN OHL-S licensed hardware satisfies open science requirements in
  EU research funding frameworks

These are not abstract policy considerations — they are increasingly concrete
procurement requirements that a FOSS-throughout platform satisfies by design.

---

## Reference

### Complete FOSS stack map

| Layer | Component | Licence | Open? | Notes |
|---|---|---|---|---|
| Transmitter firmware | EdgeTX on TX16S | GPL v2 | ✓ Full | PCB schematics not published |
| RC protocol | ExpressLRS (ELRS) | GPL v3 | ✓ Full | Protocol spec + firmware + hardware reference |
| Flight controller firmware | Betaflight | GPL v3 | ✓ Full | 17-year FOSS ancestry |
| FC hardware | Matek H7A3-SLIM | Schematic published | ✓ Partial | Schematics public, layout not |
| ESC firmware | AM32 | MIT | ✓ Full | Community-created after BLHeli_32 went closed |
| GPS infrastructure | Galileo + EGNOS | EU public infrastructure | ✓ Full | No subscription, no single-vendor dependency |
| CAD tools | FreeCAD | LGPL v2 | ✓ Full | All frame design files reproducible |
| Hardware licence | CERN OHL-S v2 | CERN OHL-S v2 | ✓ Full | Strongly reciprocal copyleft |
| Documentation | CC BY-SA 4.0 | CC BY-SA 4.0 | ✓ Full | Modifications must remain open |
| Payload MCU firmware | MicroPython on ESP32-S3 | MIT | ✓ Full | Full ESP32-S3 chip documentation |

**Known exceptions:**
- HDZero VTX encoding firmware: not open source. Not in critical control path.
- Synology NAS DSM: partially proprietary. Not a flight-critical component.
- RadioMaster TX16S PCB layout: not published (firmware is open).

### Contributing to the FOSS stack

libdrone's community benefits from contributions at every level:

- **Bug reports** with reproducible steps: more valuable than they appear —
  they save developer hours and benefit every user
- **Documentation**: perpetually underserved in all FOSS projects; clear
  explanation of how something works is as valuable as implementing it
- **Testing new firmware**: catching problems before they reach thousands of users
  is critical community infrastructure
- **Publishing build modifications**: every improvement to the frame, every new
  payload design, every calibration procedure published publicly adds to the
  commons that benefits everyone
- **Code contributions**: fixing bugs, adding features, reviewing pull requests

The career argument is direct: a student with commits in Betaflight, in the ELRS
repository, or in the libdrone hardware repository has a public portfolio of real
engineering work visible to any future employer. Work done on proprietary tools
is invisible and inaccessible.

---

## Procedure

### Evaluating a new component against FOSS criteria

Before adding any new component to libdrone (new sensor, new FC, new protocol),
evaluate:

1. Is the firmware/protocol specification publicly available?
2. Can the community fix bugs or add features without vendor permission?
3. If the manufacturer discontinues the component, is the design reproducible
   from publicly available information?
4. If proprietary: is the dependency on a critical path? Is there a viable
   open alternative? What is the exit path?

Document the evaluation. Record any proprietary dependencies explicitly.
The goal is informed decision-making, not purity for its own sake.

---

## Rationale

### Why FOSS selection compounds in value over time

A single open-source component selection is a marginal improvement. A complete
FOSS stack is compounding advantage. Each open component reduces the risk from
every other component — the community that maintains one component's firmware is
likely to maintain the others. The documentation culture that produces clear
Betaflight docs is likely to produce clear ELRS docs. The contributor network
that caught a bug in AM32 will catch bugs in the payload firmware.

Open-source ecosystems have network effects just like proprietary platforms — but
the network effects accrue to the community rather than to a single vendor.
libdrone participates in and contributes to a FOSS ecosystem that will outlast
any individual component manufacturer's business lifetime.

---

## Connections

requires:
  - [[foss-principles]]
  - [[vendor-lock-in]]
related:
  - [[elrs-protocol]]
  - [[betaflight-setup]]
  - [[open-source-philosophy]]
leads_to:
  - [[contributing-guide]]
