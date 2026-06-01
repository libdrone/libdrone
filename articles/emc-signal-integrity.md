---
id: emc-signal-integrity
title: "EMC and signal integrity"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - emc-signal-integrity
personas:
  - 1.builder
  - 5.student
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The emc-signal-integrity domain covers how electromagnetic noise is generated,
how it couples into sensitive sensors, and how it is mitigated. On a drone,
the noise sources (ESC switching, motor transients, buck converter) and the
victims (gyroscope, GPS, receiver) are centimetres apart. Mitigation requires
a layered approach: physical separation of power and signal wiring, twisted
pairs on high-current runs, star grounding to eliminate loops, decoupling
capacitors placed directly on noise sources, ferrite beads on conducted noise
paths, and conformal coating for environmental protection.

---

## Concept

<!-- not applicable — this is a domain index article -->

---

## Reference

### Articles in this domain

| Article | Content |
|---|---|
| [[emc-noise-sources]] | ESC switching, motor transients, battery leads, buck converter |
| [[twisted-pairs]] | Field cancellation physics, application to motor and signal wires |
| [[star-grounding]] | Ground loop mechanism, single-point topology |
| [[capacitor-placement-emc]] | Wire inductance vs clamping, low-ESR requirement |
| [[power-signal-separation]] | Three-zone routing, MIPI channel, EMC geometry gates |
| [[ferrite-beads]] | Frequency-selective attenuation, VTX power wire application |
| [[gps-antenna-placement]] | GPS signal levels, CF shielding, compass distance |
| [[conformal-coating]] | Moisture protection, application sequence, inspection |

---

## Procedure

<!-- not applicable -->

---

## Rationale

### Why EMC is a dedicated domain

EMC issues are invisible until they cause problems. A builder who does not
understand EMC will produce a build that works in benign conditions and fails
intermittently in the field — and will have no framework to diagnose why.
Treating EMC as a domain with dedicated articles, rather than scattered notes
in the build guide, ensures that every builder encounters the core concepts
before wiring the first motor phase wire.

---

## Connections

requires: []
related:
  - [[emc-noise-sources]]
  - [[power-signal-separation]]
  - [[twisted-pairs]]
leads_to:
  - [[emc-noise-sources]]
