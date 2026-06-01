---
id: sk-operations-manual
title: "Operations and Maintenance Manual"
version: 1.1.0
date: 2026-06-01
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 2.operator
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

After reading this manual, the operator can fly libdrone safely, respond
correctly to in-flight failures, maintain the platform to its design
specification, and document operations in a way that supports continued
airworthiness. Flying libdrone has regulatory obligations — see
[[legal-and-regulatory]] for what applies to your operation. This is the 3.0.0
replacement for the V2.4.6 Maintenance and Operations Manual (DMOM).

---

## Concept

### The operator's contract with the platform

A built drone is not a finished product. It is a machine under continuous
maintenance. The arm shafts are designed to fracture in crashes — they need
to be inspected after every rough landing and replaced when they do fracture.
The O-rings degrade with heat cycles and UV exposure. The LiPo cells age with
every charge/discharge cycle. A drone that was airworthy at 10 flight hours
may not be airworthy at 50 flight hours if maintenance was skipped.

The operator's contract is simple: inspect before every flight, maintain on
interval, repair after every damage event, and document everything. The
platform holds its end of the contract by being field-repairable in under
10 minutes for the most common failure modes.

### Before every flight

→ [[pre-flight-check]] is non-negotiable. It covers four areas: site
assessment (airspace, obstacles, weather, people), aircraft structure (props,
arms, T-locks, sandwich bolts, payload connectors), electronics verification
(GPS fix, battery voltage, Blackbox enabled), and pilot readiness.

The regulatory requirements that precede any operation — registration, pilot
competency, insurance, and the airspace check that must happen before arriving
at the site — are consolidated in → [[legal-and-regulatory]]; read it and decide
what applies to your operation.
→ [[risk-assessment]] provides the site-specific assessment framework.

Low-speed mode should be calibrated before deployment with a new payload
weight if you are relying on a speed ceiling — → [[betaflight-profiles]] and
→ [[throttle-limiting]] explain why and how.

### After every flight

→ [[post-flight-check]] runs immediately after landing, before battery removal.
It catches damage while the flight context is fresh and ensures the battery
is handled correctly before it is warm. The 15-minute window between landing
and safe battery handling is the inspection window — use it.

Log every flight in the maintenance logbook: date, site, flight count,
battery cycles used, duration, anomalies. Without this log, maintenance
intervals become guesses.

### Scheduled maintenance

→ [[scheduled-maintenance]] defines what must be done and when. The critical
intervals:
- **Every flight**: prop inspection, T-lock check
- **Every 10 flights**: motor mount O-ring visual, motor mount screw re-torque
- **Every 20–30 flight hours**: motor mount O-ring set replacement
- **After every crash**: full post-crash inspection sequence

The O-ring replacement is the most important interval. Degraded O-rings
transmit vibration to the gyroscope — the first symptom is elevated noise
in the Blackbox spectrum, not visible mechanical failure. By the time the
O-rings are visibly cracked, they have already been failing functionally.

### Corrective maintenance

→ [[corrective-maintenance]] is triggered by a finding — not a schedule. The
post-crash triage sequence runs in order from most to least likely damaged:
props, arm shafts, motor mount O-rings, CF rods (acoustic ping), T-slot
walls, electronics.

Arm shaft replacement is the most common corrective task: → [[arm-shaft]]
contains the geometry; [[corrective-maintenance]] contains the procedure.
Field replacement kit: two spare arm shafts, an M2 hex key, four spare
props, four M5 prop nuts. Under 10 minutes.

### Emergency procedures

→ [[emergency-procedures]] covers the three most likely in-flight failures
and the correct responses. The critical insight: GPS Rescue is a known and
trusted behaviour only if it has been deliberately triggered in controlled
conditions before the first uncontrolled activation. Practice GPS Rescue
at low altitude over a clear area on every new deployment.

Winter operations require the winter protocol — → [[winter-protocol]] covers
the LiPo behaviour changes below 5°C, the elevated voltage thresholds, and
the reduced flight time planning.

### Flight modes and when they apply

Understanding what the flight controller does in each mode is not optional
for safe operation. → [[flight-modes]] explains the sensor dependency chain:
GPS position hold requires GPS + compass + barometer + accelerometer + gyro.
Losing GPS drops to angle mode — the correct response is manual correction,
not confusion. Losing video is handled the same way as losing GPS: remove
the goggles, locate the drone visually, fly home manually.

### ArduPilot platform operations (Bandit, Ghost, Wing)

The operations above apply to Pro and Core (Betaflight). Bandit, Ghost, and
Wing run ArduPilot — a different operational model. The full ArduPilot
workflow is in → [[sk-ardupilot-operator-guide]]. Key differences the
operator must be aware of:

**Commissioning**: ArduPilot requires a strict sequential setup — ELRS
MAVLink mode first, then GPS/compass, then sensor calibration, then failsafe.
→ [[ardupilot-commissioning]] has the exact parameter values and sequence.

**Failsafe**: ArduPilot failsafe has three independent triggers (RC loss,
battery, GCS link), each with configurable responses. → [[ardupilot-failsafe]]
contrasts this with Betaflight GPS Rescue and provides the standard Bandit/Ghost
parameter set.

**Speed limiting**: The Betaflight throttle-limiting described in
→ [[betaflight-profiles]] and → [[throttle-limiting]] applies to Pro and Core.
ArduPilot platforms enforce speed limits differently — set via PILOT_SPEED_MAX
and WP_SPEED parameters. Whether a speed limit is required for your operation is
a regulatory question — see [[legal-and-regulatory]].


---

## Reference

### Operator quick reference

| Situation | Article |
|---|---|
| Before every flight | [[pre-flight-check]] |
| After every flight | [[post-flight-check]] |
| Flight mode sensor dependencies | [[flight-modes]] |
| RC link loss / GPS Rescue | [[betaflight-gps-rescue]], [[emergency-procedures]] |
| Video loss | [[emergency-procedures]] |
| Low battery | [[emergency-procedures]] |
| Scheduled maintenance intervals | [[scheduled-maintenance]] |
| Post-crash inspection | [[corrective-maintenance]] |
| Arm shaft replacement | [[corrective-maintenance]], [[arm-shaft]] |
| O-ring replacement | [[scheduled-maintenance]] |
| Winter operations | [[winter-protocol]] |
| ArduPilot operations | [[sk-ardupilot-operator-guide]] |
| ArduPilot failsafe | [[ardupilot-failsafe]] |
| Speed limiting | [[throttle-limiting]] |

| Regulatory requirements | [[legal-and-regulatory]], [[risk-assessment]] |
| Low-speed mode calibration | [[betaflight-profiles]] |

---

## Procedure

### First deployment at a new site

1. Run site risk assessment → [[risk-assessment]]
2. Check airspace and regulatory obligations → [[legal-and-regulatory]]
3. Set GPS Rescue return altitude for local terrain → [[betaflight-gps-rescue]]
4. Calibrate low-speed profile for payload weight → [[betaflight-profiles]]
5. Complete pre-flight checklist → [[pre-flight-check]]
6. Test GPS Rescue manually at low altitude before operational use

---

## Rationale

The DMOM (V2.4.6) combined maintenance planning, maintenance procedures, and
technical log guidance in a single document. This skeleton separates the
procedures (in atoms) from the navigation (here). An operator who needs the
O-ring replacement procedure finds it in [[scheduled-maintenance]]. An operator
who needs to understand when to do it finds that context in this skeleton.
Neither document carries the other's content.

---

## Connections

requires: []
related:
  - [[sk-complete-build-guide]]
  - [[sk-platform-brief]]
  - [[sk-ardupilot-operator-guide]]
  - [[ardupilot-commissioning]]
  - [[ardupilot-failsafe]]
  - [[throttle-limiting]]
leads_to:
  - [[sk-platform-brief]]
