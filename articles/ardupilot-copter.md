---
id: ardupilot-copter
title: "ArduPilot Copter"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: generic
topic:
  - firmware-autopilot
personas:
  - 5.student
  - 1.builder
  - 2.operator
  - 8.architect
platform:
  - bandit
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

ArduPilot Copter is an open-source autopilot firmware for multirotor aircraft.
Where Betaflight is designed for fast manual FPV flight, ArduPilot Copter is
designed for autonomous mission execution — GPS-guided waypoint flights, sensor
integration, and ground control station communication via MAVLink. On libdrone,
ArduPilot Copter runs on the Matek H7A3-SLIM (target: MatekH7A3) on Bandit
and Ghost, replacing Betaflight entirely. The firmware change is not an
incremental modification — it changes the operational model of the platform
from pilot-controlled to mission-controlled.

---

## Concept

### The fundamental difference from Betaflight

Betaflight's job is to execute the pilot's stick inputs as accurately and
quickly as possible. Its loop runs at 8 kHz; its state model is attitude and
rate. It does not know where the drone is, where it is going, or what the
mission is. GPS Rescue is the only autonomous behaviour, and it is a failsafe,
not a mission feature.

ArduPilot Copter's job is to execute a mission. Its core abstractions are
position, waypoints, and flight modes on a spectrum from fully manual
(Stabilize) to fully autonomous (Auto). It carries an Extended Kalman Filter
that fuses IMU, barometer, GPS, and compass into a continuous position estimate.
It streams telemetry to a ground control station. It can accept parameter
changes, new missions, and mode commands from the GCS in flight.

This difference is architectural, not parametric. You cannot configure
Betaflight to execute a survey grid. You cannot configure ArduPilot to behave
like a freestyle FPV firmware. They are different tools for different jobs.

### The EKF and sensor fusion

ArduPilot's Extended Kalman Filter is the component that makes autonomous
flight possible. The EKF maintains a probabilistic estimate of the aircraft's
position, velocity, and attitude by continuously fusing:
- IMU accelerometer and gyroscope (high rate, drifts over time)
- Barometer (altitude reference, affected by pressure changes)
- GPS (absolute position, 5–10 Hz update rate)
- Compass (heading reference, affected by magnetic interference)

When any sensor degrades — GPS constellation thinning, compass interference
from motors — the EKF detects the inconsistency and falls back to the remaining
sensors. This graceful degradation is what allows ArduPilot to continue a
mission through a temporary GPS gap that would cause Betaflight to trigger
GPS Rescue immediately.

### MAVLink telemetry

ArduPilot streams MAVLink messages continuously: HEARTBEAT, GLOBAL_POSITION_INT,
ATTITUDE, BATTERY_STATUS, VFR_HUD, and others. Any device connected to the FC's
telemetry UART — a ground control station, an ESP32-S3 companion board, a
Mission Planner laptop — receives the full picture of the aircraft's state.
This is the data stream that enables ATAK integration, Remote ID broadcast,
and autonomous mission monitoring from QGroundControl. See → [[serial-protocols]]
and → [[elrs-mavlink-mode]].

---

## Reference

| Parameter | Value |
|---|---|
| Firmware project | ArduPilot (ardupilot.org) |
| Relevant firmware | ArduCopter (multirotor) |
| libdrone target | `MatekH7A3` |
| Minimum version | ArduCopter 4.5.x |
| Flash tool | STM32CubeProgrammer (recommended) |
| Firmware URL | firmware.ardupilot.org/Copter/stable/MatekH7A3/ |
| GCS | QGroundControl or Mission Planner |
| Telemetry protocol | MAVLink 2 |
| Licence | GPL v3 |

**Flash warning:** Do not use Betaflight Configurator to flash ArduPilot on
H7-series boards. Use STM32CubeProgrammer. The BF flash process is known to
freeze at 50% if full chip erase is selected on H7-series hardware.

---

## Procedure

### Flash ArduPilot Copter on H7A3-SLIM

1. Download the correct binary: `MatekH7A3` from firmware.ardupilot.org →
   Copter → stable.
2. Connect H7A3-SLIM via USB-C in DFU mode (hold boot button, apply USB,
   release boot).
3. Open STM32CubeProgrammer → select USB DFU device.
4. Load the `.hex` file → click Download.
5. Disconnect and reconnect USB-C. ArduPilot will boot; the board will show
   three fast flashes on the status LED.
6. Connect QGroundControl → proceed to mandatory calibration:
   accelerometer, compass, RC, ESC. See → [[ardupilot-commissioning]].

---

## Rationale

The selection of ArduPilot over other autopilot stacks (PX4, iNAV) for Bandit
and Ghost was driven by three factors. First, ArduPilot has the largest
community-validated parameter set for the MatekH7A3 target — reducing setup
risk on first build. Second, ArduPilot's MAVLink implementation is the most
widely supported in the ATAK ecosystem, making IFF integration via CoT bridge
straightforward. Third, ArduPilot's training curriculum model (progressive
flight modes) is the deepest educational fit for Bandit's awareness programme
purpose.

---

## Connections

```yaml
requires:
  - [[flight-controller-hardware]]
  - [[gnss-gps]]
  - [[imu-gyroscope]]
related:
  - [[betaflight-setup]]
  - [[flight-modes]]
  - [[ardupilot-flight-modes]]
  - [[elrs-mavlink-mode]]
  - [[serial-protocols]]
  - [[bandit-variant]]
  - [[ghost-variant]]
leads_to:
  - [[ardupilot-commissioning]]
  - [[ardupilot-flight-modes]]
  - [[qgroundcontrol]]
```
