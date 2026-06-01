---
id: vendor-lock-in
title: "Vendor lock-in"
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

Vendor lock-in occurs when a dependency on a proprietary system gives a
single company unilateral power over your equipment's continued function.
In the FPV community, this happened visibly with FrSky in 2019: a protocol
change broke backwards compatibility across tens of thousands of pilots'
equipment, and because the protocol was proprietary, the community had no
ability to fix it, fork it, or create a compatible alternative. ExpressLRS
was created in direct response. The lesson is not that companies are
untrustworthy — it is that proprietary dependency is a technical vulnerability
that exists regardless of the vendor's current intentions.

---

## Concept

### The FrSky failure — a case study

Between approximately 2012 and 2019, FrSky was the dominant RC radio system
manufacturer for FPV. Their hardware was excellent. Their protocols (D8, D16)
worked reliably. Tens of thousands of pilots built complete RC ecosystems around
FrSky transmitters and receivers.

FrSky's protocols were proprietary. The specification was not published. No one
outside FrSky could write firmware that communicated with FrSky receivers.

In 2019, FrSky released new hardware using a new protocol called ACCESS. New
receivers could not bind to older transmitters without firmware updates. The
updates were slow, incompatible with some configurations, and broke existing
functionality. There was no recourse. The community could not fix it, fork it, or
create an alternative. The only options were waiting for FrSky or replacing
everything.

ExpressLRS was created directly in response. Open protocol specification on GitHub.
Open-source firmware. Hardware reference designs available to any manufacturer.
Within two years, ELRS became the dominant FPV protocol — not because it was
mandated, subsidised, or marketed, but because it was better and immune to the
failure mode that had damaged FrSky's reputation.

### The structural problem

The FrSky case illustrates a pattern that repeats across industries:

1. Company produces good, popular proprietary product
2. Community builds significant investment around it (skill, infrastructure, money)
3. Company's business needs change — new products, new ownership, new strategy
4. Community is stranded because their investment is locked to the proprietary system

This is not malice. FrSky did not set out to harm its community. The structural
problem is that proprietary control gives one entity power over the community's
continued operation, and business decisions that are rational for the company can
be catastrophic for the community.

### The open-source solution

An open-source system's specifications and code are publicly available. The community
can fork the project if the original maintainer changes direction. Any manufacturer
can produce compatible hardware from the published specifications. Any developer can
fix bugs. The community's investment in skills, infrastructure, and training is not
stranded by any single company's decision.

This is why libdrone selects open-source components for every function where the
choice exists: not as an ethical preference, but as a risk management strategy.

### Patterns of lock-in beyond protocols

The FrSky story is the most visible example in the FPV world, but the pattern
appears throughout technology:

- **ESC firmware**: BLHeli_32 went closed-source; the community created AM32
- **Transmitter firmware**: OpenTX development stalled; the community forked EdgeTX
- **CAD software**: vendors abandon file formats or change subscription terms;
  FreeCAD provides an open alternative
- **Cloud services**: a service that stores your data can become inaccessible
  through price changes, business failure, or policy changes; local storage
  and open formats avoid this

In each case, the pattern is identical: proprietary dependency creates a future
risk that open alternatives eliminate.

---

## Reference

### Lock-in risk assessment for drone components

| Component | Proprietary risk | Open alternative | libdrone choice |
|---|---|---|---|
| RC protocol | High (FrSky demonstrated) | ELRS | ELRS ✓ |
| ESC firmware | Medium (BLHeli_32 went closed) | AM32 | AM32 ✓ |
| FC firmware | Low (Betaflight is established FOSS) | Betaflight | Betaflight ✓ |
| Transmitter firmware | Low (EdgeTX is established FOSS) | EdgeTX | EdgeTX ✓ |
| CAD software | High (subscription, format changes) | FreeCAD | FreeCAD ✓ |
| Video system | Medium (HDZero not fully open) | No full open alternative | HDZero (acknowledged exception) |
| Satellite navigation | Medium (GPS = US military) | Galileo (EU) | Galileo + GPS ✓ |

---

## Procedure

<!-- not applicable -->

---

## Rationale

### Why this article matters for evaluators

An institution evaluating libdrone for procurement needs to understand not just
what the platform does today but whether it will continue to function as
expected over the procurement lifetime (typically 5–10 years for equipment).
Proprietary dependencies are the primary risk to long-term function. This article
provides the framework for that evaluation: what is proprietary, what is open,
and what has already happened in the field when proprietary systems changed.

---

## Connections

requires:
  - [[foss-principles]]
related:
  - [[foss-stack-libdrone]]
  - [[elrs-protocol]]
  - [[dji-problem]]
leads_to:
  - [[foss-stack-libdrone]]
