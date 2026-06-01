---
id: sk-municipal-emergency-guide
title: "Municipal Emergency Deployment Guide"
version: 1.1.0
date: 2026-06-01
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 6.evaluator
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

After reading this guide, the civil preparedness procurement officer can
specify a libdrone deployment for their municipality, understand the training
and maintenance programme required, and make a budget recommendation. Learning
objective: present a credible libdrone deployment proposal to the municipal
authority, or conclude the platform does not meet their operational requirements.

---

## Concept

### The gap in municipal emergency capability

Municipal emergency management in Central Europe has three well-developed
components: early warning systems, trained response teams, and community
communication protocols. What is almost universally absent: autonomous
aerial awareness for the civil protection officer who is not a professional
pilot and whose municipality cannot afford commercial drone infrastructure.

The cost differential is the key fact: a professional aerial sensing platform
with thermal imaging costs €5,000–50,000. libdrone with thermal payload costs
approximately €1,700 and is repairable with a 3D printer. → [[bom-summary]]
contains the detailed cost breakdown.

This is not a capability difference. → [[platform-overview]] shows the sensor
payloads available. → [[resilience-use-cases]] maps the 15 use cases that are
directly applicable to municipal emergency management: flood route assessment,
chemical plume tracking, structural assessment after events, person search,
night perimeter awareness, small supply delivery.

### The deployment model for municipalities

A municipal deployment is not one drone in a procurement cupboard. It is a
programme with three components:

**Platform and spares**: two Pro units minimum (one operational, one training
and backup), plus a spares kit (→ [[community-deployment]] contains the full
list). The two-drone model ensures the training platform absorbs all the
development crashes while the operational platform accumulates its airworthiness
record cleanly.

**Training**: the workshop programme builds one qualified pilot and one
maintainer per deployment. The pilot must maintain currency — minimum monthly
flight. → [[piloting-progression]] maps the skill development path. A pilot
who is not current is not an asset in an emergency.

**Processes**: pre-flight checklists, post-flight logs, maintenance intervals,
and seasonal calibration of the low-speed profile (→ [[pre-flight-check]],
→ [[scheduled-maintenance]]). The processes transform a capable platform into
a deployable capability. A drone without processes is a hobbyist drone with
municipal branding.

### The legal and regulatory framework

→ [[legal-and-regulatory]] is the single source of truth for operator
obligations and the regulatory route to municipal operations. The key point
for a municipality: a self-built libdrone over 250 g operates in EASA
subcategory A3 in the Open Category (far from people), so the urban and
near-people operations a municipal deployment typically needs run through the
**Specific Category** — an operational authorisation from ÚCL based on a risk
assessment. Read [[legal-and-regulatory]] and form your own view; plan for the
Specific-category route for any urban or near-people deployment.

For operations during declared emergencies: the IZS authority may grant
specific operational authorisation that modifies normal airspace restrictions.
Establish this protocol with your regional HZS before any crisis.

→ [[risk-assessment]] provides the site-specific risk assessment framework
that should be completed before each deployment location is activated.

### The EU dimension

libdrone is CERN OHL-S v2 open hardware, CC BY-SA 4.0 documentation, and
full FOSS firmware stack. → [[foss-stack-libdrone]] maps the complete open
software stack and the EU strategic autonomy argument: EU-origin satellite
navigation (Galileo + EGNOS), auditable firmware, no proprietary supply chain
dependencies. EU procurement frameworks increasingly require this auditability.

→ [[foss-principles]] explains the CERN OHL-S copyleft: any municipality that
modifies the hardware design must publish those modifications under the same
licence. Payload designs the municipality develops are their own IP.

---

## Reference

### Deployment specification for procurement

| Item | Quantity | Cost (CZK) | Notes |
|---|---|---|---|
| libdrone Pro complete build | 2 | ~68,000 | 1 operational + 1 training |
| Air quality payload (SEN66) | 1 | ~2,650 | GPS-tagged PM/CO2/VOC logging |
| Workshop training (5 sessions) | 1 | TBD by provider | 1 pilot + 1 maintainer |
| Spare arm shafts | 20 | ~400 | Print from stock filament |
| Spare motors | 4 | ~2,400 | |
| Spare ELRS receivers | 4 | ~1,600 | |
| Filament stock (PETG + PCCF) | 2 kg each | ~1,200 | 1–2 year supply |

### Regulatory checklist for municipal procurement

- [ ] Review [[legal-and-regulatory]] for current operator obligations
- [ ] Operator registration as applicable
- [ ] Pilot competency for designated pilot(s)
- [ ] Insurance as applicable for UAS operations
- [ ] Specific-category authorisation route confirmed for urban/near-people use
- [ ] Protocol with regional HZS for emergency operational authorisation
- [ ] ID labels on all drone frames

---

## Procedure

### Procurement and commissioning sequence

1. Identify designated pilot and maintainer within the team
2. Place equipment order — allow 14 days for AliExpress delivery
3. Workshop: build both platforms over 5 sessions
4. Acceptance validation: maiden flights, Blackbox review
5. Low-speed mode calibration for operational deployment context
6. Register as an operator as applicable (see [[legal-and-regulatory]])
7. Quarterly: pilot currency flight + maintenance inspection + air quality baseline

---

## Rationale

Municipal procurement decisions require different content than community
preparedness decisions. The evaluator here is a civil protection officer
with budget authority — they need: cost, regulatory compliance, training
programme, maintenance programme, and the institutional deployment model.
This skeleton provides that framing and delegates all technical specifications
to atoms.

---

## Connections

requires: []
related:
  - [[sk-platform-brief]]
  - [[sk-community-resilience-guide]]
leads_to:
  - [[sk-platform-brief]]
  - [[sk-community-resilience-guide]]
