---
id: flight-modes
title: "Flight modes"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - piloting-operations
personas:
  - 2.operator
  - 5.student
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Flight modes are a spectrum of automation, not discrete categories. Rate mode
(manual) corrects rotation rate only — the pilot controls attitude directly.
Angle mode adds accelerometer levelling — the drone returns to level when
sticks are released. GPS position hold adds GNSS — the drone holds its
position against wind. Each mode depends on additional sensors; losing a
sensor drops the drone to the next less-automated mode. A pilot who understands
this dependency chain responds correctly to failures. A pilot who does not
may fight the wrong problem.

---

## Concept

### Rate mode (manual / acro)

The flight controller corrects rotation rate using the gyroscope alone. It
applies corrections to hold the commanded rotation rate — but it does not
level the drone when sticks are centred. If the pilot releases the sticks
at 30° of roll, the drone stays at 30° of roll. The pilot controls attitude
directly and must actively return to level.

Rate mode gives maximum responsiveness and authority — corrections are direct
with no additional processing. It requires the most pilot skill. libdrone is
not optimised for rate-mode flying (the PID baseline is tuned for
GPS-assisted mapping), but rate mode is the fallback when higher-level modes
fail.

### Angle mode (self-levelling)

The flight controller fuses gyroscope and accelerometer data to maintain an
attitude estimate. When sticks are centred, the drone levels itself. Maximum
tilt angle is limited — the pilot cannot roll past a configured maximum (typically
45°). This makes the drone significantly easier to fly than rate mode.

Angle mode requires the accelerometer. If the accelerometer is producing
incorrect data (vibration-contaminated, miscalibrated, temperature-drifted),
angle mode will not hold level correctly. In practice, on a well-built libdrone
with good vibration isolation, angle mode is stable and reliable.

### GPS position hold

The flight controller adds an outer loop using GNSS position. When sticks are
released, the drone holds its current position against wind and drift. The GPS
position loop runs at 10 Hz (one update per 100 ms) — significantly slower
than the inner PID loop (8 kHz). The outer loop feeds position corrections as
attitude setpoints to the inner loops.

GPS position hold requires: accelerometer (for attitude estimate), barometer
(for altitude hold), GPS fix (≥ 8 satellites recommended), and compass (for
heading-lock position hold in wind).

Losing GPS drops the drone to angle mode — it will hold attitude but drift
with wind. The pilot must apply corrections manually. This is not an emergency;
it is the designed fallback.

### The sensor dependency chain

    GPS position hold
      └── requires: GPS fix + compass + barometer + accelerometer + gyroscope

    Angle mode
      └── requires: accelerometer + gyroscope

    Rate mode
      └── requires: gyroscope only

At each level, losing the required sensor drops to the level below. A pilot
who feels the drone suddenly start drifting should immediately consider whether
GPS was lost (switch to angle mode, maintain orientation manually) rather than
fighting the drift with GPS stick corrections that are no longer having effect.

---

## Reference

### Mode comparison

| Mode | Sticks centred | Maximum tilt | Wind resistance | Sensor requirements |
|---|---|---|---|---|
| Rate (manual) | Holds rotation rate — does not level | Unlimited | None — pilot manages | Gyroscope only |
| Angle | Levels automatically | ~45° (configured) | None — drift with wind | Gyro + accelerometer |
| GPS hold | Holds position | ~45° | Full — auto corrects | Gyro + accel + GPS + baro + compass |
| GPS Rescue | Autonomous return | — | Full — auto corrects | Same as GPS hold |

### Mode switching on libdrone TX16S

libdrone does not use a dedicated flight-mode switch for Rate/Angle/GPS.
In Betaflight, the mode stack is:

- Default: **GPS position hold** when GPS fix ≥ 8 sats
- GPS lost: **Angle mode** automatically
- Arm switch off: **Disarmed**

The pilot does not manually select between angle and GPS hold — the firmware
transitions automatically based on GPS fix quality. The Low Speed mode switch
(SD) changes the PID profile (throttle scale), not the flight mode.

---

## Procedure

### Responding to GPS loss in flight

1. OSD will show GPS fix loss (satellite count drops to 0 or flashes).
2. Drone transitions to angle mode — will now drift with wind.
3. Do not release sticks. Apply corrections to maintain position manually.
4. If GPS recovers within 5–10 seconds, position hold will reactivate.
5. If GPS does not recover: fly home in angle mode using VLOS. Keep
   airspeed low to reduce drift.
6. If drone is at risk (obstacles, loss of orientation): activate GPS
   Rescue manual trigger (SE switch) only if GPS fix was present when
   armed — GPS Rescue requires a recorded home point.

---

## Rationale

### Why libdrone does not expose a manual rate-mode switch

Rate mode requires active attitude control at all times. On a payload-carrying
mapping drone flown by operators with varying skill levels, accidental mode
switches into rate mode over an urban area are a safety risk. The firmware
stack is configured to keep the drone in the most automated mode for which
sensor conditions are met. Operators who specifically require rate mode
for freestyle or testing can enable it via a dedicated Betaflight mode switch,
but it is not in the default configuration.

---

## Connections

requires:
  - [[closed-loop-control]]
  - [[gnss-gps]]
  - [[imu-gyroscope]]
related:
  - [[betaflight-gps-rescue]]
  - [[piloting-progression]]
  - [[inertia-and-stopping]]
  - [[ardupilot-flight-modes]]
leads_to:
  - [[piloting-progression]]
  - [[ardupilot-flight-modes]]


[closed-loop-control]: closed-loop-control.md "Closed-loop control"
[gnss-gps]: gnss-gps.md "GNSS and GPS"
[imu-gyroscope]: imu-gyroscope.md "IMU and gyroscope"
[betaflight-gps-rescue]: betaflight-gps-rescue.md "Betaflight GPS Rescue"
[piloting-progression]: piloting-progression.md "Piloting progression"
[inertia-and-stopping]: inertia-and-stopping.md "Inertia and stopping distance"
[ardupilot-flight-modes]: ardupilot-flight-modes.md "ArduPilot flight modes"
