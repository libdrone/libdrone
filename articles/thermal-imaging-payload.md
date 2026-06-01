---
id: thermal-imaging-payload
title: "Thermal imaging payload"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: libdrone
topic:
  - payload-architecture
personas:
  - 3.payload-dev
  - 2.operator
  - 8.architect
platform:
  - wing
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

Thermal imaging payloads detect infrared radiation emitted by objects rather
than reflected visible light. Warm objects — animals, people, vehicles, heated
structures — appear bright against a cooler background. For aerial survey at
dawn and dusk, the thermal contrast between warm-blooded animals and the cooling
ground is maximum, enabling reliable detection at altitudes of 40–70 m AGL.
On libdrone Wing, thermal payloads integrate via the standard GX12-7 dual
payload interface, making them compatible with all GX12-equipped family members
without modification.

---

## Concept

### How thermal cameras work

All objects above absolute zero emit infrared radiation proportional to their
temperature. Thermal cameras use microbolometer arrays — grids of temperature-
sensitive resistors — to measure this emission at each pixel. The output is
a temperature map, not a colour image. Warm objects appear bright (high DN
value); cool objects appear dark. False-colour palettes (iron, rainbow, white-
hot) are applied in post-processing or in-camera for visual interpretation.

Unlike visible-light cameras, thermal cameras are not affected by lighting
conditions. They work equally well in full darkness as in daylight. The
constraint is thermal contrast: if the target and background are the same
temperature, they cannot be distinguished regardless of camera sensitivity.

### The dawn/dusk thermal window

Thermal contrast between warm-blooded animals and the ground follows the
environment's thermal cycle. During the day, the ground absorbs solar radiation
and warms to or above animal body temperature — contrast collapses. After
sunset, the ground radiates heat to the sky and cools rapidly. By dawn, ground
temperature is typically 5–15°C below animal body temperature — maximum
contrast. The 30–60 minutes before and after sunrise are the optimal survey
window. This is why Wing's primary operational model specifies dawn and dusk
flights, not midday sorties.

Winter operation (October–February in Central Europe) extends the effective
window because ground temperatures stay low throughout the day. Summer surveys
are less reliable and should not be planned unless thermal contrast conditions
are verified.

### FLIR Lepton vs Boson

Two FLIR module options are specified for Wing:

**FLIR Lepton 3.5** — 160×120 pixels, 57° HFOV, SPI interface, ~7 g. €60–80.
At 50 m AGL, a deer occupies approximately 4–6 pixels. Detection is possible;
precise classification (deer vs wild pig) is not. Appropriate for proof-of-
concept and initial myslivci demonstrations. Does not produce professionally
credible report imagery.

**FLIR Boson 320** — 320×256 pixels, 24° HFOV, USB or MIPI interface, ~18 g.
€400–600. At 50 m AGL, a deer occupies approximately 15–20 pixels with
sufficient detail for species-level classification and GPS-tagged JPEG output
suitable for a professional report. This is the Phase 2 operational standard.

### GX12-7 integration

The thermal payload connects to the Wing belly bay via GX12-7 dual connector:
Connector A (signal): UART telemetry to FC for GPS tagging, trigger input
from RC Channel (AUX1 camera trigger mapped in ArduPilot).
Connector B (power): 5V regulated from BEC.

The same thermal payload module can plug into libdrone Pro's backplane for
ground-based or multirotor thermal work without any modification. See
→ [[gx12-icd]] for the full electrical interface specification.

---

## Reference

| Parameter | FLIR Lepton 3.5 | FLIR Boson 320 |
|---|---|---|
| Resolution | 160×120 px | 320×256 px |
| HFOV | 57° | 24° |
| Interface | SPI | USB / LVDS |
| Mass | ~7 g | ~18 g |
| Cost | €60–80 | €400–600 |
| Pixels per deer at 50 m | ~4–6 | ~15–20 |
| Detection confidence | Low | High |
| Report image quality | POC only | Professional |
| Phase | 1 (POC) | 2 (operational) |

**Survey swath at 50 m AGL:**
- Lepton 3.5 (57° HFOV): ~53 m swath
- Boson 320 (24° HFOV): ~22 m swath

---

## Procedure

### Configure camera trigger in ArduPilot Plane

1. Connect camera trigger signal line to FC AUX1 output.
2. Set CAM_TRIGG_TYPE=1 (servo/relay trigger).
3. Assign AUX1 to camera trigger: SERVO9_FUNCTION=10 (Camera Trigger).
4. In QGroundControl Plan view → Survey → Camera settings: enable
   camera trigger, set distance-based or time-based trigger interval.
5. Verify camera fires on bench: manually trigger from QGC.

### Optimal survey altitude selection

1. Calculate swath width at candidate altitude: swath = 2 × altitude × tan(HFOV/2).
2. Set overlap to 30% for wildlife detection (60–80% for photogrammetry).
3. Calculate transect spacing: transect = swath × (1 − overlap).
4. Import field boundary into QGC Survey; set altitude and transect spacing.

---

## Rationale

The selection of FLIR modules over lower-cost alternatives (InfiRay, Seek
Thermal) is based on SDK availability and community documentation depth.
FLIR's Lepton and Boson have well-documented SPI/USB interfaces, Python
libraries, and extensive aerial survey community usage. For Wing's planned
detection processing script (Python + OpenCV), proven community tooling reduces
development risk. The cost premium over alternatives is justified by reduced
integration uncertainty.

---

## Connections

requires:
  - [[payload-architecture]]
  - [[gx12-icd]]
  - [[gx12-connector-standard]]
related:
  - [[wing-variant]]
  - [[wildlife-survey-operations]]
  - [[payload-sdk]]
  - [[aerial-imaging-basics]]
  - [[survey-imaging]]
leads_to:
  - [[wildlife-survey-operations]]
