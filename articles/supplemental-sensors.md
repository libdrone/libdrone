---
id: supplemental-sensors
title: "Supplemental sensors"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - sensors-fc
personas:
  - 5.student
  - 3.payload-dev
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Beyond the core IMU, barometer, magnetometer, and GNSS, additional sensors
extend drone capability into environments where the core sensors are inadequate.
Optical flow cameras enable indoor position hold without GPS. Lidars and sonars
provide range measurement for terrain following, precision landing, and collision
avoidance. None of these are fitted on libdrone V2.4.6 in the standard
configuration, but the payload interface and companion computer architecture
support adding them as payload modules.

---

## Concept

### Optical flow

An optical flow camera points downward and captures successive frames of the
terrain below. By comparing the movement of visual features between frames
(the same algorithm used in optical computer mice), it calculates the drone's
lateral velocity relative to the ground. Combined with a height measurement
from a downward-facing sonar or lidar, the velocity measurement can be
integrated to produce a position estimate.

Optical flow enables position hold without GPS — useful indoors, in urban
canyons where GPS multipath is severe, or in any environment where satellite
signals are unavailable. Its limitations: accuracy degrades over uniform or
featureless terrain (water, snow, uniform sand), at high altitude where the
terrain detail falls below the camera's resolution, and at night without a
downward-facing illuminator.

For libdrone, optical flow would be implemented as a payload module on the
GX12 interface, with data routed to the companion Pi Zero 2W running a
MAVLink-compatible position estimation algorithm.

### Lidar (laser range finder)

A lidar emits a laser pulse and measures the time of flight to a reflecting
surface. From this: distance = (time × speed of light) / 2. A single-beam
downward lidar provides precision altitude measurement — far more accurate
than barometric altitude for low-altitude hover and precision landing.

Lidars are used for:
- **Terrain following**: maintaining a fixed height above ground even as
  terrain rises and falls — important for survey missions over uneven ground
- **Precision landing**: landing on a precise spot with centimetre accuracy
- **Collision avoidance**: forward- or side-facing lidars detecting obstacles
  before the drone reaches them

Single-beam lidars suitable for drone altimetry typically have ranges of
0.1–40 m, update at 50–200 Hz, and connect via I2C or UART.

### Sonar (ultrasonic range finder)

A sonar emits an ultrasonic pulse and measures the echo return time.
Distance = (time × speed of sound in air) / 2. Speed of sound in air
(343 m/s at 20°C) is much slower than light, so the measurement is
inherently slower than lidar. Effective range is typically 0.2–4 m —
adequate for precision landing and low-altitude hover but not for
terrain following at height.

Sonars are cheaper, lighter, and more robust to dust and water than lidars.
They are sensitive to temperature (speed of sound changes with temperature,
introducing range error if not compensated) and to very soft or angled
surfaces that absorb or reflect the pulse at angles that miss the receiver.

### Compatibility with libdrone payload architecture

Supplemental sensors can be added as payload modules via the GX12-7 interface:

- **I2C sensors** (many lidars, sonars): directly available on GX12 Connector A
  PIN 5 (SCL) and PIN 6 (SDA), 400 kHz Fast Mode.
- **UART sensors**: GX12 Connector B PIN 3/4 (UART5 TX/RX) or Connector A
  PIN 3/4 (UART4 TX/RX) for sensors with serial output.
- **Processing-intensive sensors** (optical flow): require the companion
  Pi Zero 2W running the position estimation algorithm and forwarding position
  corrections to the FC via MAVLink over UART6.

---

## Reference

### Sensor comparison

| Sensor type | Range | Update rate | Interface | Limitations |
|---|---|---|---|---|
| Optical flow | N/A (velocity) | 50–200 Hz | SPI/UART | Fails over featureless terrain, needs height reference |
| Lidar (single beam) | 0.1–40 m | 50–200 Hz | I2C/UART | Cost, fragile optics |
| Sonar (ultrasonic) | 0.2–4 m | 10–50 Hz | I2C/UART/analog | Temperature-sensitive, limited range |
| RTK GNSS | Global | 10–20 Hz | UART | Requires base station, outdoor only |

### libdrone standard sensor complement

libdrone V2.4.6 ships with: IMU (ICM-42688-P), barometer (integrated on FC),
magnetometer (QMC5883 on M10Q module), GNSS (u-blox M10 on M10Q module).

No optical flow, lidar, or sonar in standard configuration. These are
available as payload module additions.

---

## Procedure

<!-- not applicable — sensor installation is payload-architecture domain -->

---

## Rationale

### Why supplemental sensors are not in the standard build

Each additional sensor adds mass, wiring complexity, and firmware configuration
surface area. The standard libdrone build is optimised for outdoor payload
missions where GPS and barometric altitude are adequate. Adding optical flow
for indoor use, or a lidar for precision landing, is a workflow-specific choice
that should be made deliberately when the mission requires it, not included
by default where it adds complexity without benefit.

---

## Connections

requires:
  - [[flight-controller-hardware]]
related:
  - [[gnss-gps]]
  - [[barometer-magnetometer]]
  - [[imu-gyroscope]]
  - [[sen66-sensor]]
leads_to:
  - [[payload-architecture]]
  - [[sen66-sensor]]
