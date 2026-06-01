---
id: foss-principles
title: "Free and open source principles"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
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

Free and Open Source Software (FOSS) grants four freedoms: to run the software
for any purpose, to study and modify it, to redistribute copies, and to
distribute modified versions. The word "free" means freedom, not price. For
engineering contexts, the more important argument is not philosophical but
practical: a proprietary system is a technical vulnerability. When the vendor
changes direction, the users have no recourse. Open source eliminates this
vulnerability — the community can fix it, fork it, or replace it regardless
of what any single company does. libdrone uses FOSS components not because of
ideology but because they are better, more auditable, and not subject to
unilateral external decisions.

---

## Concept

### The four freedoms

In 1985, Richard Stallman published the GNU Manifesto, articulating what he
called "free software." The four freedoms:

1. Freedom to run the program for any purpose
2. Freedom to study how the program works and modify it
3. Freedom to redistribute copies
4. Freedom to distribute modified versions

"Free" here is libre (without restriction), not gratis (without cost). A
program can cost money and still be free software. A program can be provided
at no cost and still not be free software. The distinction matters because
freedom — not price — is what prevents vendor lock-in.

### The engineering argument

The philosophical argument for FOSS (users deserve control) and the
engineering argument (public code is auditable and not subject to vendor lock-in)
are both correct and reinforcing. For a student choosing what to learn, the
engineering argument is more directly relevant.

A proprietary system is a technical dependency with an unknown risk profile.
The vendor can: change the protocol, discontinue the hardware, go bankrupt,
be acquired, or simply stop supporting the version you depend on. You have
no recourse. Your investment in learning the system, building infrastructure
around it, or deploying it in a product may be stranded.

An open-source system's code and specifications are publicly available. If the
original maintainer abandons it, the community can fork it. If a company stops
making compatible hardware, any other company can use the published specifications
to make a compatible alternative. If there is a bug, anyone can fix it.

This is a risk assessment, not an ethical stance. Proprietary dependency is
a technical liability. Open source mitigates it.

### Open source in hardware: CERN OHL-S

Software licensing frameworks (GPL, MIT, Apache) cover code. Hardware requires
different licences because physical objects are manufactured, not copied.

CERN OHL-S v2 (CERN Open Hardware Licence Strongly Reciprocal) is the licence
used for libdrone's hardware designs. Its key provisions:

- Anyone may produce, study, and modify the covered designs
- Any modified version must be released under the same licence
- The licence covers design files, not manufactured objects — a product built
  from CERN OHL-S designs may be sold commercially
- Payload designs that use the libdrone GX12 interface do not inherit the
  CERN OHL-S requirement — the payload's design is independent

The "Strongly Reciprocal" clause means that improvements to the libdrone
platform design must flow back to the community. This is the same logic as
GPL for software: the commons that benefits you must be strengthened by
your contribution.

---

## Reference

### FOSS licences used in libdrone

| Component | Licence | Key provision |
|---|---|---|
| Hardware designs | CERN OHL-S v2 | Modifications must be released under same licence |
| Documentation | CC BY-SA 4.0 | Modifications must be released under same licence |
| Betaflight firmware | GPL v3 | Modifications must be open-sourced |
| ExpressLRS firmware | GPL v3 | Same |
| AM32 ESC firmware | MIT | Permissive — no copyleft requirement |
| EdgeTX transmitter firmware | GPL v2 | Same |
| FreeCAD | LGPL v2 | Library use permitted without GPL obligations |
| ESP32-S3 / MicroPython | MIT | Permissive |

### Exceptions acknowledged

No real-world system is fully open. libdrone's known proprietary dependencies:

- HDZero VTX encoding firmware — not open source
- Synology NAS DSM — partially proprietary
- RadioMaster TX16S PCB schematics — not published

Being honest about these exceptions is more useful than pretending the
ecosystem is perfectly pure. The goal is to minimise proprietary dependencies,
be aware of them, and not depend on them for critical functionality.

---

## Procedure

<!-- not applicable -->

---

## Rationale

### Why FOSS selection is an engineering decision, not a political one

Some teams treat open-source selection as an ethical or political commitment
that must be balanced against practical concerns. This framing is wrong.
The practical benefits of open source — auditability, vendor independence,
community maintainability, no licence fees — are engineering properties that
compound over time. A system built on open foundations is less fragile, less
expensive, and more maintainable than an equivalent proprietary system. The
philosophical agreement with FOSS principles is a pleasant side effect of
making the better engineering decision.

---

## Connections

requires: []
related:
  - [[vendor-lock-in]]
  - [[foss-stack-libdrone]]
leads_to:
  - [[vendor-lock-in]]
  - [[foss-stack-libdrone]]
