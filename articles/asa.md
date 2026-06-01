---
id: asa
title: "ASA filament"
version: 1.0.0
date: 2026-05-30
author: jsa
status: draft
scope: generic
topic:
  - materials
personas:
  - 1.builder
  - 5.student
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

ASA (Acrylonitrile Styrene Acrylate) is a UV- and weather-resistant
thermoplastic with mechanical properties close to ABS but markedly better
outdoor durability. In the libdrone context it is a candidate material for
printed parts exposed to prolonged sunlight, where PETG and PETG-CF can soften
or degrade over time. It prints harder than PETG — it warps, needs an enclosure,
and releases styrene fumes that require ventilation — so it is chosen only where
outdoor longevity justifies the added process difficulty.

---

## Concept

ASA is a styrenic terpolymer: the acrylate rubber phase that replaces ABS's
butadiene is what gives it its defining property — resistance to UV degradation
and yellowing. Where ABS chalks and embrittles after months of sun exposure,
and where PETG slowly loses dimensional stability under combined UV and heat,
ASA holds its colour, surface, and mechanical properties outdoors for years.

Mechanically it is comparable to ABS: a glass transition around 100 °C, good
impact strength and stiffness, and ductile rather than brittle failure. The
trade-offs are all in processing. ASA has a high coefficient of thermal
expansion, so it warps and can delaminate without a heated, draught-free
enclosure. It emits styrene during printing and must be run with ventilation
or filtration. It is more hygroscopic than PLA and benefits from dry storage.

Against the other libdrone materials: PETG-CF is the structural default —
stiff, abrasion-resistant, easy to print, but not selected for long-term UV
service. PCCF (polycarbonate-carbon fibre) is for high-temperature, high-load
structural parts. ASA occupies a narrow niche between them: parts that are not
primarily structural but must survive sustained outdoor exposure.

---

## Reference

The values below are generic starting points drawn from common ASA filament
datasheets, not libdrone-validated print settings. Treat them as a baseline to
dial in against your own printer, enclosure, and the specific part.

| Parameter | Generic starting range |
|---|---|
| Nozzle temperature | 240–260 °C |
| Bed temperature | 90–110 °C |
| Enclosure | Required (passive enclosure minimum) |
| Chamber draughts | Eliminate — warping and layer splitting otherwise |
| Ventilation | Required — styrene emission during printing |
| Bed adhesion | Glue stick or ABS/ASA slurry; brim on tall parts |
| Cooling fan | Low or off — aggressive cooling causes delamination |
| Storage | Dry; mildly hygroscopic |
| Nozzle | Standard 0.4 mm brass acceptable (non-abrasive) |

<!-- libdrone part-specific profiles to be added after build validation -->

---

## Procedure

<!-- not applicable -->

---

## Rationale

ASA earns a place in the corpus for one reason: outdoor UV survivability. Any
libdrone part that sits in direct sun for extended periods — and that is not
carrying primary structural load — is a candidate to move from PETG-CF to ASA,
because PETG's long-term behaviour under combined UV and thermal load is the
weak point ASA is specifically formulated to address.

Which libdrone parts, if any, should actually be printed in ASA is a decision
that is deliberately left open here. The corpus principle is that material
choices are validated by real build and field experience, not asserted from
datasheets. ASA's added process difficulty — enclosure, ventilation, warping —
is a real cost, and committing a part to ASA should follow a printed-and-tested
coupon, not a specification written in advance. This atom is therefore marked
`draft`: it captures why ASA exists in the material set and how to print it
generically, and defers the libdrone-specific part assignments and validated
profiles to build experience.

---

## Connections

requires:
  - [[material-selection-philosophy]]
related:
  - [[petg]]
  - [[pccf]]
  - [[print-profiles]]
leads_to:
  - [[print-profiles]]
