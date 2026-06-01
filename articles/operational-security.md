---
id: operational-security
title: "Operational security"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - iff-deconfliction
personas:
  - 9.defense
  - 2.operator
  - 8.architect
platform:
  - pro
  - bandit
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

Operational security (OPSEC) for drone operations in security-sensitive
environments requires managing what the drone broadcasts, who can receive it,
and when broadcasting is a liability rather than an asset. Every RF emission
from a drone — ELRS control link, HDZero video, Remote ID, ESP32-S3 WiFi —
is a detectable signal that reveals operator position, drone position, and
operational intent to any sufficiently capable observer. OPSEC is not achieved
by turning everything off; it is achieved by understanding which emissions
are required, which are optional, and what each reveals to different observer
categories. The IR strobe remains the only IFF layer with no electronic
emissions.

---

## Concept

### The emissions inventory

Every libdrone platform generates these RF emissions during operation:

| Emission | Frequency | Power | Detectable at |
|---|---|---|---|
| ELRS control link | 2.4 GHz | 10–100 mW (dynamic) | 100m–2km (spectrum monitor) |
| HDZero FPV video | 5.8 GHz | 25–800 mW | 50m–500m (spectrum monitor) |
| Remote ID (WiFi NAN) | 2.4 GHz | < 10 mW | ~300m (any smartphone, Remote ID app) |
| Remote ID (BLE) | 2.4 GHz | < 10 mW | ~100m (any Bluetooth scanner) |
| ESP32-S3 WiFi (CoT, NAS sync) | 2.4 GHz | < 20 mW | ~100–200m |
| HDZero OSD uplink (MSP) | Through video link | — | Same as video |

The ELRS control link is the largest and most persistent emission. Even with
dynamic power at minimum (10 mW), it is detectable by a sensitive 2.4 GHz
spectrum monitor at several hundred metres. This is not a solvable problem
for radio-controlled operations — the control link must exist. OPSEC focuses
on the controllable emissions.

### Controllable vs uncontrollable emissions

**Uncontrollable** (drone cannot fly without them):
- ELRS control link
- ELRS telemetry (1:16 ratio, low power)

**Controllable** (can be selectively disabled):
- HDZero FPV video — disable VTX or reduce to 25 mW
- Remote ID — legally required in EU civilian airspace; may be suspended
  under specific operational authority. Do not assume this is switchable
  without explicit authority.
- ESP32-S3 WiFi hotspot — disable in firmware config before flight
- CoT output — disable in ESP32 firmware config when not on an authorised network

**Reduced but not eliminated**:
- ELRS dynamic power minimum (10 mW) — reduce to minimum, accept reduced range

### EMCON levels

**EMCON standard** (normal civilian operations): all emissions active, full
capability. Remote ID broadcasting. CoT active if on a trusted TAK network.
HDZero at operational power.

**EMCON reduced** (security-sensitive, non-contested): VTX at 25 mW. ELRS
at minimum dynamic power. ESP32-S3 WiFi hotspot disabled during flight.
CoT output to authenticated TAK server only (not multicast). Remote ID active
(regulatory compliance maintained).

**EMCON minimum** (contested or high-risk environment): VTX disabled (relay
mode only, or accept no video). ELRS at minimum power, accept reduced range
and plan accordingly. ESP32-S3 WiFi off during flight. Remote ID: consult
operational authority. IR strobe provides the only IFF capability at this level.

### Operator position disclosure

Remote ID broadcasts the operator's GPS position. In an environment where
the operator's position should not be disclosed, Remote ID is a liability
as well as a regulatory requirement. There is no technical solution to this
tension within the EU regulatory framework — the regulation does not provide
an operator-initiated broadcast suspension mechanism for civilian operators.

For operations where this matters: consult the relevant authority before
deploying. Understand what you are broadcasting and to whom.

### Network security for CoT

UDP multicast CoT (239.2.3.1:6969) is unencrypted and unauthenicated. Any
device on the same network can read the CoT feed. For operational use:
- Use an authenticated TAK server (TAK Server Enterprise or FreeTAKServer)
  rather than UDP multicast
- Authenticate with X.509 certificates
- Restrict TAK server access to known participants
- Understand that the WiFi network itself may be observable

---

## Reference

### EMCON configuration checklist

| Setting | Standard | Reduced | Minimum |
|---|---|---|---|
| VTX power | 200 mW | 25 mW | Off |
| ELRS dynamic power | 10–100 mW | 10 mW fixed | 10 mW fixed |
| ESP32 WiFi hotspot | On (post-flight sync) | Off during flight | Off |
| Remote ID | On | On | Consult authority |
| CoT output | Multicast or TAK server | Authenticated TAK only | Off |
| IR strobe | On (if NVG environment) | On | On — only IFF layer |

### To disable ESP32-S3 WiFi hotspot

In `/boot/lcm1_config.json` on the ESP32-S3's SD card:

    {
      "wifi_hotspot_on_boot": false,
      "cot_output": false,
      "nas_sync_on_landing": false
    }

Applies on next power cycle. SD logging and OSD continue to function —
only the WiFi-dependent functions are suspended.

---

## Procedure

### Pre-deployment EMCON decision

1. Assess the operational environment: civilian airspace, security-sensitive
   civilian, or conflict-adjacent.
2. Determine applicable EMCON level from the table above.
3. Configure ESP32-S3 firmware and TAK settings to match EMCON level before
   departure — not in the field.
4. Brief all team members on which emissions are active and what they reveal.
5. If Remote ID is active: assume operator position is observable by any
   smartphone in range. Plan operator positioning accordingly.
6. Document the EMCON configuration in the flight log before each operation.

---

## Rationale

### Why EMCON discipline is an operator skill, not a firmware feature

A firmware feature that automatically adjusts emissions based on operational
context would require the firmware to understand that context — a level of
situational awareness that is not appropriate to embed in the platform
firmware. EMCON decisions require human judgment: what are the threat actors
capable of detecting, what are the regulatory constraints, what capability
am I willing to trade for reduced signature. These are operator decisions.
The firmware provides the controls. The operator exercises them.

---

## Connections

requires:
  - [[threat-assessment]]
  - [[iff-architecture]]
  - [[emissions-control]]
related:
  - [[remote-id-compliance]]
  - [[digital-fpv]]
  - [[elrs-protocol]]
  - [[lcm1-spec]]
  - [[acoustic-signature-design]]
  - [[esp32-s3-companion]]
leads_to:
  - [[platform-selection]]


[threat-assessment]: threat-assessment.md "Threat assessment"
[iff-architecture]: iff-architecture.md "IFF architecture"
[emissions-control]: emissions-control.md "Emissions control"
[remote-id-compliance]: remote-id-compliance.md "Remote ID compliance"
[digital-fpv]: digital-fpv.md "Digital FPV"
[elrs-protocol]: elrs-protocol.md "ExpressLRS protocol"
[lcm1-spec]: lcm1-spec.md "LCM-1 compute module"
[acoustic-signature-design]: acoustic-signature-design.md "Acoustic signature design"
[esp32-s3-companion]: esp32-s3-companion.md "ESP32-S3 companion board"
[platform-selection]: platform-selection.md "Platform selection"
