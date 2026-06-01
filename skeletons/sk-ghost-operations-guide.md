---
id: sk-ghost-operations-guide
title: "Ghost Operations Guide"
version: 1.0.0
date: 2026-04-15
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 2.operator
  - 9.defense
  - 6.evaluator
platform:
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

After reading this guide, an operator can build, commission, and deploy
libdrone Ghost for long-endurance survey and security-sensitive operations.
The guide covers Ghost-specific hardware decisions — Li-Ion battery pack,
CF plate arms, mandatory ESP32-S3 — and the operational considerations
that follow from Ghost's acoustic profile and IFF architecture. For the
ArduPilot commissioning that Ghost shares with Bandit, read
→ [[sk-ardupilot-operator-guide]] first.

---

## Concept

### What makes Ghost different in the field

Ghost shares its electronics stack with Bandit — same FC, same ESC, same
ELRS link, same ArduPilot parameters. What the operator experiences
differently:

**Endurance**: 30–45 minutes versus Bandit's 12 minutes. Mission planning
changes. Batteries require longer charging cycles. Post-flight battery
temperature management is different for Li-Ion chemistry.

**Acoustic profile**: Ghost at 50m AGL produces approximately 50–55 dB(A)
versus Bandit's 60–65 dB(A). The detection range reduction is real and
operationally meaningful for security-sensitive missions — but it is not
invisibility. → [[acoustic-signature-design]] quantifies it.

**Arm repair**: Ghost arms are laser-cut 2mm CF plate, not 3D-printed. Field
repair requires pre-cut spare plates and an M3 hex driver — no print time,
but no improvisation either. Carry spares. → [[cf-plate-arms]] has the
repair procedure.

**IFF mandatory**: Ghost always flies with ESP32-S3 active. The EMCON kill
switch is a deliberate RF control tool, not an emergency measure.
→ [[esp32-s3-companion]] and → [[iff-architecture]].

---

## Reference

### Ghost-specific parameter changes from Bandit baseline

    ; Battery failsafe — Li-Ion thresholds (NOT LiPo defaults)
    BATT_LOW_VOLT,14.4     ; 3.6V/cell — Li-Ion flatter discharge
    BATT_CRT_VOLT,14.0     ; 3.5V/cell — minimum safe discharge

    ; Flight performance — larger props, lower authority
    ANGLE_MAX,2500         ; 25° max lean (vs 35° for Bandit)
    PILOT_SPEED_UP,100     ; Conservative climb rate (cm/s)

    ; Motor — low-KV 12-inch
    MOT_THST_HOVER,0.35    ; Starting estimate; auto-learns after hover

### Li-Ion battery handling

→ [[li-ion-batteries]] for the full chemistry, construction, and charging
reference. Key operational differences from LiPo:

- Charge at 0.5–1C (3–6A for the 6000mAh pack) — slower than LiPo
- Nominal voltage per cell is 3.6V, not 3.7V — BATT_LOW_VOLT must be
  recalibrated below the LiPo default
- No puffing failure mode — Li-Ion cells fail by capacity fade over hundreds
  of cycles, not by physical swelling
- Store at 3.6V/cell (50% charge), not the 3.8V/cell LiPo storage voltage

### CF plate arm field kit

Carry per-deployment: 2 spare arm plate pairs (4 plates), M3 hex driver,
4× M3×10mm bolts with Loctite 243 dots pre-applied. Arm replacement:
15 minutes maximum.

---

## Procedure

### Pre-deployment EMCON check

Ghost operates in three EMCON levels defined in → [[operational-security]]:

**EMCON standard** (civilian survey): All emissions active. ESP32-S3 running
CoT bridge, Remote ID, and detection logging. ELRS at 100mW. VTX at full
power.

**EMCON reduced** (security-sensitive, non-contested): VTX at 25mW. ELRS
at 25mW. ESP32-S3 CoT bridge and Remote ID active. Flip EMCON switch to
reduced power mode before launch.

**EMCON minimum** (contested environment): Toggle the EMCON kill switch on
the Ghost body. All ESP32-S3 RF (WiFi, BLE, Remote ID) cuts immediately.
Detection logging to MicroSD continues. IR strobe continues — strobe is
independent of the kill switch. VTX disabled via ArduPilot relay.

Verify EMCON kill switch function before every deployment in security-sensitive
context: activate switch, confirm ATAK CoT icon freezes within 5 seconds,
confirm BLE packets cease on a phone scanner.

### Acoustic profile measurement (Bandit B2.1 method)

Before first operational deployment, measure Ghost's actual detection range:

1. Ghost in Loiter at 50m AGL, operator at launch point with QGC
2. Second operator walks downwind on flat terrain until aircraft is
   inaudible — marks distance
3. Walks back until reliably audible again — marks distance
4. Repeat upwind and crosswind
5. Average of three directions is the acoustic detection range in these
   specific conditions

Record conditions (wind speed, temperature, terrain) with the result.
Detection range is weather-dependent — warm calm evenings produce longer
ranges than cold windy ones.

### Post-flight Li-Ion handling

Unlike LiPo, Li-Ion packs do not require immediate cooling or storage voltage
management after flight. Standard procedure:

1. Allow pack to cool to ambient temperature before charging (15 min minimum)
2. Check cell balance on charger — all four series groups should be within
   50mV of each other
3. If balance deviation > 100mV, do a balance-only charge before next
   flight
4. Log charge cycle count — replace pack after 300 full cycles or when
   capacity falls below 80% of nominal

---

## Rationale

Ghost operations differ enough from standard Bandit operations to warrant
a dedicated guide. The Li-Ion chemistry, CF arm repair workflow, EMCON
procedure, and acoustic measurement methodology are all Ghost-specific.
Incorporating them into a general ArduPilot guide would either require
extensive platform conditionals or bury Ghost-specific content behind
shared content that Ghost operators do not need to re-read.

---

## Connections

requires:
  - [[ghost-variant]]
  - [[ardupilot-copter]]
  - [[li-ion-batteries]]
  - [[cf-plate-arms]]
  - [[esp32-s3-companion]]
  - [[acoustic-signature-design]]
  - [[iff-architecture]]
  - [[operational-security]]
related:
  - [[sk-ardupilot-operator-guide]]
  - [[sk-security-operations-guide]]
  - [[bandit-variant]]
  - [[ardupilot-failsafe]]
  - [[iff-layers]]
leads_to:
  - [[sk-ardupilot-operator-guide]]
  - [[operational-security]]
  - [[iff-architecture]]


[sk-ardupilot-operator-guide]: sk-ardupilot-operator-guide.md "ArduPilot Operator Guide"
[acoustic-signature-design]: ../articles/acoustic-signature-design.md "Acoustic signature design"
[cf-plate-arms]: ../articles/cf-plate-arms.md "CF plate arms"
[esp32-s3-companion]: ../articles/esp32-s3-companion.md "ESP32-S3 companion board"
[iff-architecture]: ../articles/iff-architecture.md "IFF architecture"

[li-ion-batteries]: ../articles/li-ion-batteries.md "Li-Ion batteries"
[operational-security]: ../articles/operational-security.md "Operational security"
[ghost-variant]: ../articles/ghost-variant.md "Ghost variant"
[ardupilot-copter]: ../articles/ardupilot-copter.md "ArduPilot Copter"
[sk-security-operations-guide]: sk-security-operations-guide.md "Security Operations Guide"
[bandit-variant]: ../articles/bandit-variant.md "Bandit variant"
[ardupilot-failsafe]: ../articles/ardupilot-failsafe.md "ArduPilot failsafe"
[iff-layers]: ../articles/iff-layers.md "IFF layers"
