---
id: risk-assessment
title: "Risk assessment"
version: 1.1.0
date: 2026-06-01
author: jsa
status: released
scope: libdrone
topic:
  - safety-regulations
personas:
  - 2.operator
  - 6.evaluator
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

A risk assessment identifies hazards, estimates the likelihood and severity
of each, and documents the mitigations in place. For libdrone operations it
is both a sound engineering practice and, for some operations, a regulatory
requirement — whether and when it applies is covered in [[legal-and-regulatory]].
As a practical tool, knowing which hazards are highest risk guides where to invest
in mitigation. The primary hazards are rotating propellers, LiPo thermal
runaway, loss of control link, and structural failure. Most are mitigated
to acceptable levels by the design (failure hierarchy, GPS Rescue, conformal
coating) and operational procedures (pre-flight checklist, VLOS, separation
distances).

---

## Concept

### Risk as likelihood × severity

Risk is assessed as the product of two factors: likelihood (how probable is
the hazard occurring?) and severity (what is the impact if it does occur?).
A low-likelihood, high-severity event (e.g. LiPo fire in a crowded area) may
require more mitigation than a high-likelihood, low-severity event (e.g.
arm shaft fracture during a rough landing) because the consequences are
qualitatively different.

The 3×3 matrix (Low/Medium/High for each axis) used in the DSRA provides
a simple but effective framework for categorising and prioritising hazards.

### Design-level vs operational-level mitigations

Some hazards are mitigated at the design level — built into the hardware or
firmware. Others require operational procedures. Understanding which mitigations
are design-level (always active regardless of operator action) versus
operational-level (require the operator to follow a procedure) is essential
for honest risk assessment.

Design-level mitigations: failure hierarchy (arm shaft fuse), GPS Rescue
(autonomous return on link loss), floating motor mounts (vibration isolation),
TVS diode (VBAT spike protection), conformal coating (moisture protection).

Operational-level mitigations: pre-flight checklist, VLOS maintenance,
separation distances, low-speed mode calibration, battery storage discipline,
post-crash inspection.

---

## Reference

### libdrone V2.4.6 hazard register (summary)

| Hazard | Likelihood | Severity | Risk | Primary mitigation |
|---|---|---|---|---|
| Prop strike (person) | Low | High | **High** | VLOS + separation distance + low-speed mode |
| LiPo thermal runaway | Low | High | **High** | Charging procedures, storage, crash inspection |
| Loss of control link | Medium | Medium | **Medium** | GPS Rescue, ELRS 250Hz LBT, VLOS |
| Arm shaft fracture | Medium | Low | **Low** | Failure hierarchy design — shaft is the fuse |
| Motor failure | Low | Medium | **Low** | Pre-flight motor check, GPS Rescue on link loss |
| GPS Rescue failure | Low | Medium | **Low** | Min 8 sats gate, sanity checks enabled |
| Payload separation | Low | Medium | **Low** | Double nut + Loctite, pre-flight connector check |
| Cold weather failure | Medium | Medium | **Medium** | 0°C flight limit, battery warming protocol |
| Compass interference | Medium | Low | **Low** | Nose placement, calibration discipline |
| Video link loss | Medium | Low | **Low** | VLOS maintained independently of FPV |

### High-risk hazard mitigations in detail

**Prop strike (person)**
- Design: prop guards are not standard on libdrone — speed and prop guard
  weight/complexity conflict with the mission profile
- Operational: maintain separation distance per [[legal-and-regulatory]]; never
  fly over uninvolved persons; pre-flight people scan
- Firmware: GPS Rescue prevents uncontrolled flyaway on link loss

**LiPo thermal runaway**
- Design: battery housed in open-sided rail — not enclosed, cannot trap thermal
  energy; conformal coating prevents moisture-induced shorts
- Operational: charging procedures, storage voltage, crash inspection, LiPo
  bag storage, fireproof charging container
- No fully effective design mitigation exists — operational discipline is primary

---

## Procedure

### Site-specific risk assessment

Before each new operational site, complete a site-specific assessment:

1. **Airspace**: any controlled airspace, temporary restrictions, or flight
   information regions within the operating area? If yes: obtain authorisation
   before flying.
2. **People density**: uninvolved persons present? Estimate typical count and
   behaviour. Apply separation distance accordingly.
3. **Obstacles**: identify the highest obstacle in the likely flight area plus
   the return-to-home path. Set GPS Rescue altitude above it.
4. **Emergency landing zones**: identify at least two areas clear of people
   where an emergency landing or crash would have lowest consequence.
5. **Environmental hazards**: RF interference sources (industrial equipment,
   military installations), metal structures near the compass, water features.
6. **Communication**: if flying with observers or bystanders, brief them on
   keep-out zones and the arming/disarming procedure.

Document the assessment briefly before flying. A photo of the site with
annotated zones is adequate for personal operations.

---

## Rationale

### Why the risk assessment is written documentation, not a mental checklist

A mental risk assessment is vulnerable to confirmation bias (assuming the site
is safe because it looks like previous safe sites), time pressure (skipping
hazards when eager to fly), and post-incident dispute (no record of what was
considered). Brief written documentation takes 3–5 minutes, survives the
operator's memory, and provides evidence of due diligence if an incident
occurs. In Specific Category operations, a documented SORA (Specific Operations
Risk Assessment) is required — see [[legal-and-regulatory]]. Practising the
discipline now makes that transition straightforward.

---

## Connections

requires:
  - [[legal-and-regulatory]]
related:
  - [[pre-flight-check]]
  - [[lipo-batteries]]
  - [[betaflight-gps-rescue]]
  - [[failure-hierarchy]]
leads_to:
  - [[piloting-operations]]
