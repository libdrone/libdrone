---
id: preflight-checklist
title: "Pre-flight checklist"
version: 2.0.0
date: 2026-05-31
author: jsa
status: released
scope: libdrone
topic:
  - safety-regulations
personas:
  - 2.operator
  - 1.builder
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The printable pre-flight checklist: the step-by-step tick sequence run before
every flight, covering site, structure, electronics, powered verification, and
pilot readiness. For the reasoning behind it and the go/no-go gates, see the
[[pre-flight-check]] process.

---

## Concept

<!-- not applicable — this is a checklist artefact; the reasoning lives in [[pre-flight-check]] -->

---

## Reference

### A. Site assessment
- [ ] Airspace authorisation confirmed (CTR, ATZ, U-space, restricted areas)
- [ ] Maximum altitude for site identified (120 m AGL for Open Category)
- [ ] Obstacles mapped: power lines, trees, buildings, antennas
- [ ] People assessed: bystanders, uninvolved persons, buffer maintained
- [ ] Wind and weather acceptable: wind below operational limit, no rain
- [ ] Emergency landing zones identified (at least two)

### B. Aircraft — structural
- [ ] All 4 propellers inspected: no cracks, chips, nicks, or looseness
- [ ] All 4 arm T-locks verified: tabs fully seated, no rocking
- [ ] Frame sandwich: no visible cracks in PCCF layers or arm roots
- [ ] CF rods: all four present, none protruding past arm shaft outer face
- [ ] Sandwich bolts: all 6 or 8 present, no obvious looseness
- [ ] Motor mount O-rings: not cracked or permanently deformed
- [ ] Bumpers: all 4 present and seated
- [ ] Payload (if fitted): GX12 lock rings finger-tight, mast screws tight

### C. Aircraft — electronics
- [ ] Battery checked: voltage above 24.0 V (fresh pack), no swelling
- [ ] Battery rail secure: no play, strap buckle locked
- [ ] All connectors checked: XT60, MR30 × 4, JST signal connectors
- [ ] Conformal coating intact on FC and ESC
- [ ] VTX antenna secure and unobstructed above GPS antenna

### D. Electronics — powered verification (transmitter on first, then drone)
- [ ] OSD visible in goggles with correct telemetry fields
- [ ] Battery voltage on OSD matches handheld multimeter ±0.2 V
- [ ] GPS fix: ≥ 8 satellites before arming (wait up to 90 s cold start)
- [ ] Payload OSD readings visible (if payload fitted)
- [ ] RSSI / link quality showing good signal from TX16S
- [ ] All 4 motors respond to Motors tab test (props removed, then re-check)
- [ ] Blackbox enabled and device confirmed (onboard flash or SD card)
- [ ] Failsafe configured: GPS Rescue active if ≥ 8 sats

### E. Pilot readiness
- [ ] Not fatigued, impaired, or distracted
- [ ] Site brief complete if flying with observers or participants
- [ ] Weather window confirmed (not just current — for planned flight duration)
- [ ] Operator registration number (e-ID) carried
- [ ] A2 CoC carried (if A2 subcategory operation)

---

## Procedure

<!-- not applicable — execute the ticklist above; the maiden-flight sequence is in [[pre-flight-check]] -->

---

## Rationale

<!-- not applicable — see [[pre-flight-check]] for go/no-go gates and reasoning -->

---

## Connections

requires:
  - [[pre-flight-check]]
related: []
leads_to: []
