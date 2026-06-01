---
id: ardupilot-commissioning
title: "ArduPilot commissioning"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: libdrone
topic:
  - firmware-autopilot
personas:
  - 1.builder
  - 4.workshop
platform:
  - bandit
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

ArduPilot commissioning on the Matek H7A3-SLIM covers four parameter groups
that must be configured correctly before first flight: frame and motor setup,
ELRS MAVLink mode on UART2, GPS and compass on UART3, and VTX power control
via the switchable 9V BEC. Mandatory calibration (accelerometer, compass, RC,
ESC) follows. The entire sequence is completed in QGroundControl; no
command-line access is required. A commissioning error in any of the four
parameter groups will prevent safe autonomous flight — working through them
in order and verifying each before proceeding is the correct workflow.

---

## Concept

### Parameter groups and their dependencies

ArduPilot commissioning is ordered by dependency. Frame type must be set
before motor test (DSHOT requires correct frame geometry for correct motor
direction). ELRS MAVLink must be configured before RC calibration (the RC
channel mapping is carried inside the MAVLink stream, not on a separate SBUS
wire). GPS must be configured before compass calibration (the external compass
on the M8Q-5883 is the only compass used; the FC internal compass must be
disabled to prevent interference from motor noise).

### The ELRS MAVLink UART assignment

The H7A3-SLIM has RC input pre-configured on USART2 (SERIAL2) with
SERIAL2_PROTOCOL=23 (RCIN) by default. For ELRS MAVLink mode, this must be
changed to SERIAL2_PROTOCOL=2 (MAVLink2). In ELRS MAVLink mode, the RC channel
data is embedded inside the MAVLink stream — setting the protocol to RCIN will
prevent telemetry from working while setting it to MAVLink2 handles both RC
and telemetry on the same UART. This is the most common commissioning error
on first Bandit builds. See → [[elrs-mavlink-mode]] for the full mode explanation.

### Compass isolation

The H7A3-SLIM carries an internal compass. Motor current produces magnetic
fields that corrupt compass readings during flight, particularly at the
distances between the FC and the motors on a 220 mm frame. The external
QMC5883L compass on the Matek M8Q-5883 mast is mounted 40 mm above the prop
plane — sufficient distance for clean readings. Setting COMPASS_USE2=0
disables the internal compass entirely. Never run Bandit or Ghost with the
internal compass enabled.

---

## Reference

### Parameter group 1 — Frame and motor

    FRAME_CLASS,1          ; Quad
    FRAME_TYPE,1           ; X
    MOT_PWM_TYPE,6         ; DSHOT300
    MOT_SPIN_ARM,0.1       ; Spin on arm for motor check
    MOT_THST_HOVER,0.35    ; Starting estimate; auto-learned after hover

### Parameter group 2 — ELRS MAVLink (UART2)

    SERIAL2_PROTOCOL,2     ; MAVLink2 — RC carried inside MAVLink stream
    SERIAL2_BAUD,460       ; 460800 baud
    RSSI_TYPE,5            ; Telemetry radio (ELRS MAVLink mode)
    RC_PROTOCOLS,512       ; CRSF enabled
    RC_OPTIONS,8448        ; Bit 9 + Bit 13 (ELRS-specific)

### Parameter group 3 — GPS and compass (UART3)

    SERIAL3_PROTOCOL,5     ; GPS
    SERIAL3_BAUD,38        ; 38400 for M8Q
    GPS_TYPE,1             ; uBlox
    COMPASS_USE,1          ; External compass (M8Q)
    COMPASS_USE2,0         ; Disable FC internal compass
    COMPASS_ORIENT,0       ; Arrow forward on GPS mast

### Parameter group 4 — VTX power (9V switchable BEC)

    RELAY1_PIN,81          ; GPIO81 = PC13 = 9V BEC on H7A3-SLIM
    RCx_OPTION,28          ; Assign to TX switch for VTX on/off

---

## Procedure

### Full commissioning sequence

1. Flash ArduPilot (see → [[ardupilot-copter]] for flash procedure).
2. Connect QGroundControl. Navigate to Vehicle Setup → Parameters.
3. Enter parameter groups 1–4 in order. Write each group before proceeding.
4. **Mandatory calibration sequence:**
   a. Accelerometer calibration (6-position, follow QGC prompts).
   b. Compass calibration (rotate aircraft on all axes until QGC confirms).
   c. RC calibration (verify all channels, confirm mode switches map correctly
      — see → [[ardupilot-flight-modes]]).
   d. ESC calibration if using non-DSHOT ESCs (Bandit/Ghost use DSHOT300;
      ESC calibration is not required).
5. Motor test (QGC → Motors tab): confirm correct spin direction for X frame,
   props off.
6. First hover test in AltHold, props on, open area: confirm altitude hold,
   confirm RTL on RC signal loss.
7. Run Autotune in AltHold before first Auto mission.
   See → [[ardupilot-autotune]].

---

## Rationale

Splitting commissioning into four named parameter groups rather than a flat
parameter list reduces the error surface for workshop builds. Each group has
a single failure mode: if ELRS MAVLink is broken, RC calibration fails
obviously. If GPS is wrong, Loiter refuses to engage. If the compass is not
isolated, Loiter drifts on a predictable bearing. Named groups make the
diagnosis path shorter when something does not work.

---

## Connections

```yaml
requires:
  - [[ardupilot-copter]]
  - [[elrs-mavlink-mode]]
  - [[gnss-gps]]
  - [[barometer-magnetometer]]
related:
  - [[ardupilot-flight-modes]]
  - [[ardupilot-autotune]]
  - [[ardupilot-failsafe]]
  - [[software-commissioning]]
leads_to:
  - [[ardupilot-flight-modes]]
  - [[ardupilot-autotune]]
  - [[maiden-flight]]
```


[elrs-mavlink-mode]: elrs-mavlink-mode.md "ELRS MAVLink mode"
[ardupilot-copter]: ardupilot-copter.md "ArduPilot Copter"
[ardupilot-flight-modes]: ardupilot-flight-modes.md "ArduPilot flight modes"
[ardupilot-autotune]: ardupilot-autotune.md "ArduPilot Autotune"
