---
id: ardupilot-flight-modes
title: "ArduPilot flight modes"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: generic
topic:
  - firmware-autopilot
personas:
  - 5.student
  - 2.operator
  - 4.workshop
platform:
  - bandit
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

ArduPilot Copter organises its flight modes as a progression of automation
layers, each adding one sensor dependency and one level of autonomous
behaviour. On Bandit, six modes are assigned to a single RC channel in a
deliberate sequence: Stabilize → AltHold → Loiter → Auto → RTL → Land.
This sequence is both a capability ladder and the libdrone training curriculum.
A student who works through the modes in order understands not only what each
mode does but what sensor or system failure strips it away — and what mode the
aircraft falls back to when that happens.

---

## Concept

### Modes as a dependency chain

Each ArduPilot flight mode depends on the modes beneath it:

**Stabilize** requires only the IMU (accelerometer + gyroscope). It corrects
rotation rate to match stick input — no levelling, no position hold. If every
other sensor fails, Stabilize still functions. It is the mode of last resort
and the mode of first learning.

**AltHold** adds barometer. Altitude is locked to the barometric pressure
reading; throttle becomes altitude adjustment rather than raw thrust. The
aircraft returns to the target altitude when throttle is released. GPS is not
required.

**Loiter** adds GPS and compass. Position is locked to the GPS coordinate at
mode entry; the aircraft resists wind drift. Loiter is the first mode that
feels like the aircraft is "flying itself." It is also the first mode that
fails silently if compass interference corrupts the heading estimate —
the aircraft will drift in a compass-correlated direction, not hold position.

**Auto** adds waypoint mission execution. The aircraft follows a pre-uploaded
mission from QGroundControl: survey grid lines, altitude changes, hold times,
trigger events. Pilot input is suppressed — intervention requires switching
out of Auto. This is the mode the awareness curriculum targets as the
threat model: fully autonomous, following a pre-programmed plan, no
continuous pilot required.

**RTL** (Return to Launch) is triggered manually or by failsafe. The aircraft
climbs to RTL altitude, flies to the launch point GPS coordinate, descends,
and lands. It requires GPS and compass. Signal-loss failsafe (ELRS → ArduPilot
FS_THR_ACTION=RTL) uses this mode. See → [[ardupilot-failsafe]].

**Land** commands vertical descent and motor cutoff on touchdown detection. Used
at the end of missions and as the final step of RTL.

### Mode assignment on TX16S (Bandit)

Six modes are mapped to RC Channel 7 using a combination of the TX16S 3-position
switch (SB) and 2-position switch (SC). The specific channel mapping is set in
the ArduPilot parameters as FLTMODE1 through FLTMODE6. The ordering reflects
the training progression: a student in early training should not be able to
accidentally trigger Auto by a casual switch movement.

### Failure modes and fallback behaviour

| Lost sensor | Mode that fails | Fallback |
|---|---|---|
| GPS | Loiter, Auto, RTL | AltHold if pilot switches; Stabilize if baro also fails |
| Compass | Loiter (drifts), Auto (drifts) | Pilot must switch to AltHold or Stabilize |
| Barometer | AltHold, Loiter, Auto | Stabilize |
| RC signal | All | RTL via failsafe (FS_THR_ACTION=RTL) |

---

## Reference

| Mode | ArduPilot name | Sensors required | Training phase |
|---|---|---|---|
| Stabilize | STABILIZE | IMU | Phase 1 |
| Alt Hold | ALT_HOLD | IMU + baro | Phase 2 |
| Loiter | LOITER | IMU + baro + GPS + compass | Phase 3 |
| Auto | AUTO | IMU + baro + GPS + compass + mission | Phase 4 |
| RTL | RTL | IMU + baro + GPS + compass | All phases |
| Land | LAND | IMU + baro | All phases |

**Key ArduPilot parameters:**
    FLTMODE1,0    ; Stabilize
    FLTMODE2,2    ; AltHold
    FLTMODE3,5    ; Loiter
    FLTMODE4,10   ; Auto
    FLTMODE5,11   ; RTL
    FLTMODE6,9    ; Land

---

## Procedure

### Verify mode transitions before first flight

1. Connect QGroundControl. Arm the aircraft on the bench (props off).
2. Cycle through each flight mode using the TX16S switches.
3. Confirm QGC HUD displays the correct mode name for each switch position.
4. Verify Loiter mode shows GPS fix (green GPS icon, HDOP < 2.0) before
   attempting Loiter flight.
5. Verify Auto mode requires a mission to be uploaded — the aircraft should
   refuse to arm in Auto without a valid mission.

---

## Rationale

The six-mode Bandit assignment was chosen to match the progressive exposure
model in the awareness curriculum. Phase 1 (Stabilize) requires the most pilot
skill and builds the most understanding of what the automation is doing in
later modes. A student who starts in Loiter or Auto has no mental model of
what is maintaining position — and therefore no model of what failure looks
like. The progression from manual to autonomous is the curriculum, not just
a feature list.

---

## Connections

```yaml
requires:
  - [[ardupilot-copter]]
  - [[flight-modes]]
  - [[gnss-gps]]
  - [[barometer-magnetometer]]
related:
  - [[ardupilot-failsafe]]
  - [[qgroundcontrol]]
  - [[bandit-variant]]
  - [[imu-gyroscope]]
leads_to:
  - [[ardupilot-commissioning]]
  - [[ardupilot-failsafe]]
  - [[qgroundcontrol]]
```


[ardupilot-failsafe]: ardupilot-failsafe.md "ArduPilot failsafe"
