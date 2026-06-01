---
id: piloting-operations
title: "Piloting and operations"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - piloting-operations
personas:
  - 2.operator
  - 4.workshop
  - 5.student
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The piloting-operations domain covers everything that happens between battery
connection and battery removal: flight modes and their sensor dependencies,
piloting skill progression, scheduled maintenance intervals, post-flight
blackbox analysis, and winter operating procedures. These articles address the
operator persona — the person flying and maintaining a built drone — and are
distinct from the builder domain that covers construction and configuration.

---

## Concept

<!-- not applicable — this is a domain index article -->

---

## Reference

### Articles in this domain

| Article | Content |
|---|---|
| [[flight-modes]] | Rate / angle / GPS modes, sensor dependencies, failure transitions |
| [[piloting-progression]] | Learning phases from hover to FPV orientation to emergencies |
| [[scheduled-maintenance]] | Maintenance intervals by component, post-crash inspection |
| [[blackbox-analysis]] | Gyro spectrum, time trace, motor output, PID diagnostic guide |

---

## Procedure

<!-- not applicable -->

---

## Rationale

### Why piloting and operations share a domain

Pilot skill and platform maintenance are inseparable in practice. A pilot
who does not understand the maintenance requirements of their platform will
fly degraded hardware. A maintenance-focused operator who does not understand
flight modes cannot respond correctly to in-flight failures. The domain
captures both and treats the operator as a single persona responsible for both.

---

## Connections

requires: []
related:
  - [[pre-flight-check]]
  - [[flight-modes]]
  - [[scheduled-maintenance]]
  - [[blackbox-analysis]]
leads_to:
  - [[flight-modes]]
