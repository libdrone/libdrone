---
id: legal-and-regulatory
title: "Legal and regulatory (single source of truth)"
version: 1.0.0
date: 2026-06-01
author: jsa
status: released
scope: libdrone
topic:
  - safety-regulations
personas:
  - 6.evaluator
  - 2.operator
  - 1.builder
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

**Not legal advice.** To the best of our understanding as of June 2026, the
laws, limitations, and practices below constrain how libdrone may be flown. We
are not lawyers; rules change, vary by country, and are interpreted by national
authorities. Verify against your national aviation authority — in the Czech
Republic, ÚCL (caa.cz) and the official DroneMap portal — before flying. You are
responsible for your own compliance. Specific figures marked *(verify)* are from
secondary sources and await confirmation against ÚCL primary sources.

This is the single source of truth for all regulatory, legal, and operational-risk
information in the libdrone corpus. Every other atom that touches legality links
here rather than restating rules. The headline: libdrone is a **privately-built
UAS** under EASA, which is a permanent, named category — not a grey area — but
that status carries real operational limits, and the most important one is that a
self-built Pro flies in subcategory **A3**, not A2.

---

## Concept

### libdrone is a privately-built UAS — what that means

EASA's framework offers three routes into the Open Category: a drone bears a
C0–C4 class mark; or it is **privately built and under 25 kg**; or it is a legacy
drone placed on the market before 31 December 2023. libdrone, assembled by its
builder from open hardware for personal use, takes the **privately-built** route.

This matters because the 2026 class-marking regime (C0–C4 mandatory, only
CE-marked drones may be sold) reshaped the *commercial* market but does **not**
apply to a self-build — nothing is placed on the market, so no class mark is
required or possible. A privately-built UAS is defined by EASA as one assembled
for the builder's own use, explicitly **not** including a drone assembled from a
ready-to-assemble kit sold as a single product. A libdrone built from the open
documentation and separately-sourced parts is privately built; a hypothetical
single boxed libdrone kit sold ready-to-assemble would not be.

### The consequence: self-builds fly by weight, in A1 or A3 only

Because a privately-built drone has no class mark, it cannot access the
class-marked subcategories — and **A2 is a class-marked subcategory (it requires
a C2 mark)**. A self-build therefore flies by weight:

- **Under 250 g → A1.** May operate in populated areas (not over assemblies of
  people).
- **250 g to 25 kg → A3.** Must operate **far from people and built-up areas** —
  *(verify: ~150 m from residential, commercial, industrial, and recreational
  areas in CZ)*. No flight near uninvolved persons.

There is no privately-built route into A2. The A2 "fly 5 m from people in
low-speed mode" provision applies only to C2-class-marked drones, which a
self-build cannot obtain without becoming a manufacturer placing a product on
the market.

### What this means per libdrone variant

- **SCRAP (sub-250 g): A1.** The sub-250 g design target is a genuine regulatory
  advantage — A1 is the least-restricted route. Note: carrying a camera triggers
  operator registration regardless of weight *(verify)*.
- **Core (typically sub-250 g): A1** if the actual built weight is confirmed
  under 250 g; **A3** if any configuration exceeds it.
- **Pro / Ghost / Bandit / Wing (over 250 g, privately built): A3 only** in the
  Open Category — far from people and built-up areas. These cannot legally
  operate near uninvolved persons or in urban settings as Open-category
  self-builds.

### The route to urban, near-people, and municipal operations

libdrone's institutional positioning — municipal emergency response, urban
survey, civil preparedness — describes operations that are **not reachable in the
Open Category** for a self-built Pro. The legal path for those is the **Specific
Category**: an operational authorisation from the national authority (ÚCL in CZ)
based on a risk assessment (SORA), or operation under an EU standard scenario
(STS-01 / STS-02) if the Member State has adopted them *(verify whether CZ has)*.
Any libdrone deployment that is urban, near people, at night, or municipal is a
Specific-category matter — this is the honest answer to "how does libdrone reach
its institutional users legally," and institutional skeletons should frame it
that way rather than implying Open-category access.

---

## Reference

### Operating limits (Czech Republic, Open Category, as of June 2026)

All figures *(verify)* against ÚCL (caa.cz) and DroneMap before relying on them.

| Item | Detail |
|---|---|
| Framework | EASA (EU 2019/947, 2019/945) + CZ Civil Aviation Act 49/1997 Coll. + OOP LKR310–320 *(verify)* |
| Authority | ÚCL — Úřad pro civilní letectví |
| Operator registration | Required if drone > 250 g **or** carries a camera; online, ~200 CZK/year *(verify)*; e-ID number displayed on all drones |
| Pilot competency (A1/A3) | Free online training + 40-question exam, 75% pass, 5-year validity *(verify)* |
| Privately-built subcategories | A1 (< 250 g), A3 (250 g – 25 kg). **No A2 for self-builds.** |
| A3 separation | ~150 m from residential / commercial / industrial / recreational areas *(verify)* |
| Max altitude | 120 m AGL |
| Visual line of sight | Mandatory; FPV goggles require a spotter to count as VLOS |
| Night flight | **Prohibited in Open Category in CZ** — stricter than EASA baseline; requires Specific authorisation *(verify)* |
| National parks | Permit required (Krkonoše, Šumava, Podyjí, České Švýcarsko) *(verify)* |
| Airspace check | DroneMap (official ÚCL portal) before every operation — not manufacturer app maps |
| Insurance | Third-party liability — *(verify CZ threshold and requirement)* |

### Remote ID

EU Remote ID (EASA) requires drones above 250 g to broadcast operator and
position data. For libdrone this is a legal obligation on Pro / Ghost / Bandit
/ Wing, met by a dedicated lightweight broadcast module. Remote ID does **not**
replace operator registration — both are required. *(Verify current CZ
applicability and thresholds.)* Technical implementation lives in
[[remote-id-compliance]]; the legal requirement lives here.

### Data protection (GDPR)

A camera-carrying drone processes personal data and falls under EU GDPR + CZ Act
110/2019 Coll. (supervisor: ÚOOÚ). Filming or photographing identifiable people
in private settings without consent is prohibited. libdrone's local-processing,
no-vendor-cloud architecture is a genuine data-sovereignty advantage here — data
need not leave the operator's control — but it does not remove the operator's
GDPR obligations. *(Verify.)*

---

## Procedure

### Pre-season regulatory check

1. Confirm operator registration is current (renew if due).
2. Confirm A1/A3 pilot certificate is valid.
3. Confirm any required insurance is active.
4. Check caa.cz and easa.europa.eu for changes since last season.
5. Per site: check DroneMap for airspace restrictions and zone permits.
6. For any urban / near-people / night / municipal operation: confirm whether a
   Specific-category authorisation is required and obtain it before flying.

---

## Rationale

### Why a single source of truth

Regulatory awareness belongs everywhere in the corpus — weight targets, throttle
limits, and pre-flight gates all exist partly for legal reasons, and pretending
otherwise would make the engineering incoherent. But a regulatory *claim a reader
might act on* must live in exactly one place, so it can be reviewed once
(ideally by pro-bono legal counsel), corrected once, and dated once. Other atoms
may say "this has regulatory implications — see [[legal-and-regulatory]]"; they
may not state what the law is. This contains the legal risk to one reviewable
document and keeps the technical atoms technically focused.

### Why we corrected the A2 framing

Earlier corpus versions placed libdrone Pro in subcategory A2 and described
low-speed mode as the mechanism that makes urban operation legal. That was
incorrect: A2 requires a C2 class mark, which a privately-built drone cannot
hold. A self-built Pro is A3. The low-speed / throttle-limiting capability
remains valuable — as a beginner-training aid and good airmanship (see
[[throttle-limiting]]) — but it does not unlock A2 separation distances for a
self-build. Where we may have been at fault, we removed the claim. The honest
urban path is the Specific Category.

---

## Connections

requires: []
related:
  - [[throttle-limiting]]
  - [[remote-id-compliance]]
  - [[risk-assessment]]
  - [[dji-problem]]
leads_to: []
