---
id: emissions-control
title: "Emissions control"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - iff-deconfliction
personas:
  - 2.operator
  - 6.evaluator
  - 8.architect
platform:
  - ghost
  - bandit
lang: en
licence: CC BY-SA 4.0
---

## Summary

Emissions control (EMCON) is the deliberate management of a platform's
electromagnetic and optical signature to reduce its detectability by
hostile sensors. For civilian drone platforms operating in security-sensitive
environments, EMCON means: minimising radio frequency emissions (reducing FPV
VTX power or switching to relay-based operation, disabling non-essential
broadcast), minimising optical signature (avoiding highly reflective surfaces
in the visual spectrum, considering IR-dark configurations), and understanding
what sensors can and cannot detect at what distances. The Ghost platform
variant specifically addresses reduced-emissions operation. Full EMCON is
operationally demanding — it trades capability for reduced detectability.

---

## Concept

### What can detect a small drone

| Detection method | Range (typical) | Detects what | EMCON countermeasure |
|---|---|---|---|
| Visual (eye) | <200 m in open, much less in clutter | Physical drone | Dark colour, small size |
| Acoustic | 50–300 m depending on noise floor | Motor noise | Lower RPM, electric motors already quiet |
| RF passive (spectrum monitor) | 100s of m to km | Active radio transmissions | Reduce/eliminate RF emissions |
| Radar | Depends on system — typically >1 km for dedicated C-UAS | Physical size + motion | Low radar cross-section, terrain masking |
| Infrared | 100s of m for thermal systems | Heat signature | Manage waste heat, avoid hot surfaces |
| Remote ID receiver | ~300 m | Broadcast position | Remote ID cannot be disabled for legal compliance |

For civilian platforms, the most controllable signature is radio frequency.
The FPV VTX is the largest deliberate RF emitter on the drone (25–800 mW
at 5.8 GHz). The ELRS RC link is much lower power (10–100 mW at 2.4 GHz)
but is still detectable by a sensitive spectrum monitor.

### RF emission sources on libdrone

| Source | Frequency | Power | Controllable? |
|---|---|---|---|
| FPV VTX (HDZero) | 5.8 GHz | 25–800 mW | Yes — switch SA on TX16S |
| ELRS RC link | 2.4 GHz | 10–100 mW (dynamic) | Partially — dynamic power |
| Remote ID | 2.4 GHz (WiFi NAN + BLE) | <10 mW | No — legally mandatory |
| ESP32-S3 payload WiFi | 2.4 GHz | <20 mW | Yes — disable hotspot mode |
| ESC switching noise | 48 kHz (radiated) | Low | Partially — twisted pairs help |

### Ghost platform reduced-emissions configuration

The Ghost variant is configured for minimum RF emission in security-sensitive
deployments:
- FPV VTX at 25 mW minimum power or disabled (relay-based operation)
- ELRS dynamic power minimum set to 10 mW
- Payload WiFi hotspot disabled during flight
- Remote ID compliant (legally unavoidable)
- Dark matte PETG finish reduces optical reflectivity

For fully relay-based operation (pilot not co-located with drone): the FPV
feed is relayed via a separate encrypted link rather than direct 5.8 GHz
transmission from the drone. This is a mission planning configuration, not
a hardware change.

### What EMCON does not hide

Motor noise is inherent to multirotor operation and cannot be eliminated without
changing the fundamental propulsion system. A small drone at 50 m altitude
is audible in a quiet environment. Electric motors are significantly quieter
than combustion engines, but "electric = silent" is incorrect. At 20 m
altitude, a 330 mm libdrone is clearly audible.

Radar detection depends on radar cross-section and system sensitivity. Small
drones at low altitude in cluttered environments (tree lines, buildings) are
difficult for non-dedicated radar systems. Dedicated C-UAS radars can detect
small drones at ranges of hundreds of metres to several kilometres.

---

## Reference

### Emissions control operating modes

| Mode | VTX power | ELRS power | Payload WiFi | When to use |
|---|---|---|---|---|
| Standard | 200 mW | Dynamic 10–100 mW | On | Normal operations |
| Low emission | 25 mW | 10 mW fixed | Off | Security-sensitive environments |
| RF-dark | Off (relay only) | 10 mW fixed | Off | Highest-risk deployments |

### Selecting the appropriate mode

Emissions control is a mission planning decision, not a default setting.
For standard air quality mapping and civilian operations: Standard mode.
For operations in proximity to sensitive sites, at night, or in
security-relevant contexts: Low emission or RF-dark as appropriate.

---

## Procedure

### Switching to low-emission mode

1. On TX16S, set VTX power switch (SA) to minimum (25 mW) position.
2. In ELRS settings: set minimum power to 10 mW (already default).
3. Disable ESP32-S3 WiFi hotspot mode in payload firmware before flight
   (set `WIFI_HOTSPOT_ON_BOOT = False` in config).
4. Remote ID remains active — legally required.
5. Brief the operation: low-emission mode reduces FPV link margin. Maintain
   closer range or accept shorter maximum range.

---

## Rationale

### Why emissions control is a Ghost/Bandit topic and not all-platform

Core and Pro are designed for civilian operations where RF emission is not
a concern — in fact, maximum FPV video quality and link reliability are
desirable. Emissions control is an operational mode for platforms deployed in
security-sensitive contexts, which maps to Ghost (reduced-emission variant)
and Bandit (autonomous resilience operations). Including emissions control
considerations in the Core/Pro operational guidance would add complexity
without operational relevance for those platforms' primary use cases.

---

## Connections

requires:
  - [[iff-layers]]
related:
  - [[remote-id-compliance]]
  - [[digital-fpv]]
  - [[elrs-protocol]]
leads_to:
  - [[resilience-community]]
