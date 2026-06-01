---
id: iff-layers
title: "IFF layers"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - iff-deconfliction
personas:
  - 6.evaluator
  - 8.architect
  - 2.operator
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Identification Friend or Foe (IFF) for civilian drones is a layered problem
with no single complete solution. Classical military IFF (NATO Mode 4/5) is
classified, encrypted, and inaccessible to civilian operators. libdrone's
response is a layered civilian IFF architecture that applies the maximum
available identification capability at each accessible layer: infrared
strobe (passive, NVG-visible, jamming-immune), EU Remote ID (broadcast,
regulatory compliance), ATAK/Cursor-on-Target (tactical network integration
via ArduPilot on Bandit), and ESP32-S3 CoT gateway (software extension on
Betaflight platforms). Each layer has different cost, capability, and
resilience characteristics. The simplest layer — IR strobe — is also the
most resilient in denied environments.

---

## Concept

### The identification gap

Traditional military IFF was designed for manned aircraft: classified
cryptographic challenge-response, hardware costing thousands of euros,
incompatible with COTS flight controllers, unavailable to civilian operators.
The rapid adoption of small drones by criminal and state-affiliated hybrid
warfare actors created a dangerous ambiguity: when a drone appears overhead,
the observer cannot reliably determine whether it belongs to a friendly actor,
a hostile actor, or an unaware civilian. Fratricide and asset loss follow.

libdrone's response is not to replicate classified systems but to maximise
useful identification at each accessible layer, treating the layers as
complementary rather than alternatives.

### Layer overview

| Layer | Technology | Cost | Dependency | Resilience in denied env. |
|---|---|---|---|---|
| L1 | IR strobe | €8–15 | None | Maximum — no electronics |
| L2 | EU Remote ID | €80–120 | GPS + FC UART | High — local broadcast |
| L3 | ATAK / CoT | SW only | WiFi/LTE + GPS | Medium — network dependent |
| L4 | ESP32-S3 CoT gateway | €10 HW | WiFi/LTE + FC MAVLink | Medium — network dependent |
| L5 | Classified mil IFF (Mode 4/5) | N/A | N/A | N/A — not accessible |

### L1 — Infrared strobe

An 850/940 nm IR LED strobe is invisible to the unaided eye and to standard
colour cameras, but clearly visible to any night-vision device or thermal
sensor. Deployed widely by Ukrainian forces from 2022 as a standard
fratricide-prevention measure.

**Key properties**: lowest cost in the IFF stack; requires no integration with
any drone system; not jammable; functions when radio networks are jammed, GPS
is denied, and the internet is down. This is exactly the scenario libdrone's
resilience mission must plan for.

**Proposed implementation**: a standard mounting point on every platform for
an 850 nm cycling strobe. Powered by its own internal USB-rechargeable battery —
independent of drone power. Drone power failure does not extinguish the strobe.

### L2 — EU Remote ID

EU Implementing Regulation 2019/947 requires all drones above 250 g to
continuously broadcast identity, GPS position, altitude, and operator location
via WiFi Neighbor Awareness Networking (NAN) and/or Bluetooth 5.0 Long Range.

Remote ID is regulatory compliance, not tactical IFF. It differentiates
registered civilian operators from unregistered hostile actors in civilian
airspace management systems. It does not convey friend/foe tactical status
to military forces. Range is limited (~300 m WiFi NAN).

**Important operational consideration**: broadcasting GPS position is a
liability in actively contested environments. Remote ID should be evaluated
per-deployment — there are scenarios where compliance-driven broadcasting
is tactically inadvisable.

### L3/L4 — ATAK / Cursor on Target

ATAK (Android Team Awareness Kit) is the tactical situational awareness
platform deployed by US, NATO, and partner forces including Ukrainian units.
A drone feeding its position into ATAK appears as a Blue Force icon on every
allied operator's screen simultaneously.

**ArduPilot path (Bandit)**: ArduPilot natively bridges GPS position to CoT
format via MAVLink. The Bandit platform has this capability without additional
software.

**Betaflight path (Core/Pro)**: Betaflight does not support CoT natively.
The ESP32-S3 companion board running an MAVLink bridge firmware receives GPS
and attitude data from the FC and converts it to CoT XML for ATAK.

---

## Reference

### Layer deployment matrix

| Platform | L1 IR strobe | L2 Remote ID | L3/L4 ATAK |
|---|---|---|---|
| Core | Optional | Not required (<250g typical) | L4 via ESP32-S3 |
| Pro | Recommended | Required | L4 via ESP32-S3 |
| Ghost | Recommended | Required | L4 via ESP32-S3 |
| Bandit | Required | Required | L3 native (ArduPilot) |

---

## Procedure

<!-- not applicable — implementation is in ir-strobe-implementation and remote-id-setup -->

---

## Rationale

### Why the IR strobe is the most resilient layer

Electronic systems fail under jamming, GPS denial, and network disruption —
exactly the conditions under which IFF matters most. An IR strobe has no
electronics that can be jammed, no network to lose, and no GPS to deny. It
functions in the complete absence of electronic infrastructure. The lesson
from Ukraine 2022–2025 is that the simplest physical layer provided the most
reliable fratricide prevention precisely because of its lack of dependencies.
Building libdrone deployments around the assumption that electronic layers
will work is a false baseline in contested environments.

---

## Connections

requires: []
related:
  - [[remote-id-compliance]]
  - [[emissions-control]]
  - [[esp32-s3-companion]]
leads_to:
  - [[remote-id-compliance]]
  - [[emissions-control]]
  - [[esp32-s3-companion]]
