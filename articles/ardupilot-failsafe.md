---
id: ardupilot-failsafe
title: "ArduPilot failsafe"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: generic
topic:
  - firmware-autopilot
personas:
  - 1.builder
  - 2.operator
  - 4.workshop
platform:
  - bandit
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

ArduPilot Copter provides three independent failsafe systems: RC link loss
failsafe, battery voltage failsafe, and GCS link loss failsafe. Each triggers
a configurable action — RTL, Land, or Continue — independently of the others.
On Bandit and Ghost, the standard configuration is RC loss → RTL, battery low
→ RTL, battery critical → Land. ArduPilot's failsafe architecture is more
complex than Betaflight's GPS Rescue because the aircraft may be mid-mission
when a link or power event occurs; the configured response must account for
mission state, not just immediate recovery.

---

## Concept

### Three independent trigger paths

**RC link failsafe** activates when ArduPilot stops receiving valid RC input
for longer than FS_THR_ENABLE's timeout (default 1 second). The trigger
condition is set by FS_THR_VALUE — a PWM threshold below which the throttle
channel is treated as lost signal rather than genuine low throttle. On ELRS,
the transmitter sends a failsafe packet with throttle at the preset failsafe
PWM value when signal is lost; ArduPilot detects this and triggers the action
configured in FS_THR_ACTION.

**Battery failsafe** uses two voltage thresholds: BATT_LOW_VOLT triggers a
warning and can initiate RTL; BATT_CRT_VOLT triggers Land regardless of
mission state. These are measured at the FC power input and account for voltage
sag under load. The thresholds must be calibrated against the specific battery
chemistry — a 4S LiPo low threshold (14.8 V) is different from a 4S Li-Ion
pack (14.4 V). See → [[lipo-batteries]] and → [[li-ion-batteries]].

**GCS link failsafe** activates when MAVLink heartbeat from the ground station
is lost for longer than FS_GCS_TIMEOUT seconds. This is distinct from RC link
loss — the GCS link can fail while RC control continues, or vice versa. In
Auto mission mode, the standard behaviour on GCS loss is to continue the
mission, not abort, since the mission was pre-programmed and does not require
live GCS input.

### Difference from Betaflight GPS Rescue

Betaflight GPS Rescue has one trigger (RC link loss) and one response (RTL
and land). ArduPilot's failsafe is a matrix: three triggers, each with
independent configurable responses, which can differ based on current flight
mode. A Bandit in Loiter responding to RC loss behaves differently from a
Bandit in Auto responding to the same event — in Auto, continuing the mission
may be the correct response; in Loiter with no mission context, RTL is safer.
See → [[betaflight-gps-rescue]] for comparison.

---

## Reference

### Standard Bandit / Ghost failsafe parameters

    ; RC link failsafe
    FS_THR_ENABLE,1        ; Enable RC failsafe
    FS_THR_VALUE,975       ; PWM threshold — below this = signal lost
    FS_THR_ACTION,1        ; 1 = RTL

    ; Battery failsafe (4S LiPo — adjust for Li-Ion on Ghost)
    BATT_LOW_VOLT,14.8     ; 3.7V/cell warning; triggers RTL
    BATT_CRT_VOLT,14.4     ; 3.6V/cell critical; triggers Land
    BATT_FS_LOW_ACT,1      ; Low voltage action: RTL
    BATT_FS_CRT_ACT,1      ; Critical voltage action: Land

    ; GCS failsafe
    FS_GCS_ENABLE,1        ; Enable GCS failsafe
    FS_GCS_TIMEOUT,5       ; Seconds before trigger

**Ghost Li-Ion adjustment:** For 4S2P 18650, set BATT_LOW_VOLT=14.4 and
BATT_CRT_VOLT=14.0 (18650 cells have a flatter discharge curve than LiPo).

---

## Procedure

### Verify failsafe before first flight

1. With aircraft armed in AltHold on the bench (props off), switch the
   transmitter off. Confirm QGC shows "RC Failsafe" and FLTMODE changes
   to RTL within 2 seconds.
2. Power on transmitter. Confirm mode returns to pre-failsafe mode.
3. In QGC → Battery screen, confirm voltage readings are live and match
   measured cell voltage.
4. Simulate low battery by temporarily setting BATT_LOW_VOLT above the
   current pack voltage — confirm QGC warning triggers. Restore correct value.

---

## Rationale

The decision to configure RC loss → RTL rather than Land on Bandit is
deliberate: survey missions are typically flown at range where an immediate
Land command would result in the aircraft descending wherever RC signal was
lost — potentially into the survey target, a tree, or a body of water. RTL
returns the aircraft to the known-safe launch point and descends there.
Battery critical → Land overrides this logic because at critical voltage,
the aircraft may not have enough energy to complete RTL. Prioritising safe
immediate landing over precise landing point is correct at critical voltage.

---

## Connections

```yaml
requires:
  - [[ardupilot-copter]]
  - [[ardupilot-flight-modes]]
related:
  - [[betaflight-gps-rescue]]
  - [[lipo-batteries]]
  - [[li-ion-batteries]]
  - [[elrs-mavlink-mode]]
  - [[emergency-procedures]]
leads_to:
  - [[ardupilot-commissioning]]
  - [[maiden-flight]]
```


[lipo-batteries]: lipo-batteries.md "LiPo batteries"
[li-ion-batteries]: li-ion-batteries.md "Li-Ion batteries"
[betaflight-gps-rescue]: betaflight-gps-rescue.md "Betaflight GPS Rescue"
