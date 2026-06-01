---
id: qgroundcontrol
title: "QGroundControl"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: generic
topic:
  - firmware-autopilot
personas:
  - 2.operator
  - 5.student
  - 1.builder
platform:
  - bandit
  - ghost
  - wing
lang: en
licence: CC BY-SA 4.0
---

## Summary

QGroundControl (QGC) is a free and open-source ground control station for
ArduPilot and PX4 aircraft. On libdrone ArduPilot platforms, it serves three
distinct functions: initial vehicle setup and parameter configuration,
pre-flight mission planning and upload, and live telemetry monitoring during
flight. It runs on Linux, macOS, Windows, and Android. QGC connects to the
aircraft via the ELRS MAVLink link (UDP or USB) and receives the continuous
MAVLink telemetry stream from ArduPilot. No cloud account or internet
connection is required for normal operation.

---

## Concept

### Three distinct operational modes

QGC has a modal interface: Fly, Plan, and Analyse views, each serving a
different phase of operation.

**Setup view** (Vehicle Setup in the toolbar) is used during commissioning.
It provides wizards for accelerometer calibration, compass calibration,
RC calibration, and flight mode assignment. Parameters are accessible as a
flat list with search. This is where the ArduPilot parameter groups for ELRS
MAVLink, GPS, and failsafe are entered. See → [[ardupilot-commissioning]].

**Plan view** is the mission planner. The operator draws a survey grid polygon
on an offline map, sets altitude and overlap parameters, and QGC auto-generates
the waypoint mission file. The mission is uploaded to the FC over MAVLink with
a single click. QGC supports survey grid, corridor scan, and structure scan
patterns. For Bandit standard missions: survey grid at 50 m AGL with 80%
front overlap is the starting point.

**Fly view** is the operational HUD during flight. It displays: position on
map, current flight mode, altitude (barometric and relative), groundspeed,
battery voltage and estimated remaining time, RSSI, GPS satellite count and
HDOP, and active mission waypoint. The operator monitors this display
throughout the mission and does not need to touch the transmitter during Auto
mode unless intervention is required.

### Offline maps

QGC can cache map tiles for offline use. For field operations without mobile
internet, cache the survey area at sufficient zoom level before deployment.
A missing map tile does not prevent mission execution — the aircraft follows
the waypoint coordinates regardless — but it removes the operator's visual
reference for the aircraft's ground track.

### Mission confidence before Auto

Do not switch to Auto mode without verifying the uploaded mission in Plan view.
QGC renders the planned flight path with altitude profile. Errors in the plan
— incorrect AGL altitude, waypoints outside the survey area, missing RTL at
mission end — are visible in Plan view and invisible once the aircraft is in
the air.

---

## Reference

| QGC feature | Use in libdrone |
|---|---|
| Vehicle Setup → Parameters | All ArduPilot parameter entry |
| Vehicle Setup → Sensors | Accelerometer and compass calibration |
| Vehicle Setup → Radio | RC channel calibration |
| Vehicle Setup → Flight Modes | Mode switch channel assignment |
| Plan → Survey | Survey grid mission creation |
| Plan → Upload | Mission upload to FC over MAVLink |
| Fly → HUD | Live telemetry monitoring |
| Fly → Instrument Panel | Altitude, speed, battery, GPS |
| Analyse → MAVLink Inspector | Live raw MAVLink message stream |

**Connection:** UDP port 14550 (ELRS Backpack WiFi) or USB-C serial at 460800 baud.

**Download:** docs.qgroundcontrol.com/master/en/qgc-user-guide/getting_started/download_and_install.html

---

## Procedure

### Upload a survey mission to Bandit

1. Connect QGC to aircraft via ELRS MAVLink (WiFi UDP or USB-C).
2. Confirm Fly view shows HEARTBEAT, GPS fix, and correct battery voltage.
3. Switch to Plan view.
4. Select Survey from the pattern menu. Draw the survey area polygon on the
   map by clicking boundary corners.
5. Set parameters: altitude (50 m AGL), overlap (80% front, 70% side for
   mapping; 30% sufficient for wildlife survey).
6. Review the generated flight path — confirm it covers the intended area and
   ends with RTL or Land.
7. Click Upload. QGC shows upload progress; confirm "Mission received" from FC.
8. Switch to Fly view. Arm aircraft in Loiter, confirm GPS lock (HDOP < 2.0).
9. Switch to Auto mode. Aircraft begins executing the uploaded mission.
10. Monitor Fly view HUD throughout. Be ready to switch out of Auto and take
    manual control if the aircraft deviates from the planned path.

---

## Rationale

QGC was selected over Mission Planner as the primary libdrone GCS for two
reasons: native Linux support without Wine, and a cleaner interface for
workshop instruction. Mission Planner has deeper feature coverage but is
Windows-primary and has a steeper learning curve. For the primary use cases
— commissioning, survey mission upload, and flight monitoring — QGC provides
everything needed with less interface overhead. Mission Planner remains
available for advanced parameter work.

---

## Connections

```yaml
requires:
  - [[ardupilot-copter]]
  - [[elrs-mavlink-mode]]
related:
  - [[ardupilot-commissioning]]
  - [[ardupilot-flight-modes]]
  - [[ardupilot-autotune]]
  - [[bandit-variant]]
  - [[wing-variant]]
leads_to:
  - [[ardupilot-autotune]]
  - [[maiden-flight]]
  - [[wildlife-survey-operations]]
```
