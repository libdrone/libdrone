---
id: barometer-magnetometer
title: "Barometer and magnetometer"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - sensors-fc
personas:
  - 5.student
  - 2.operator
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The barometer measures atmospheric pressure, which decreases predictably with
altitude, providing a continuous altitude reference for altitude hold and GPS
Rescue. The magnetometer measures the direction of Earth's magnetic field —
telling the FC which direction is north, essential for GPS navigation and
position hold in wind. Both sensors are susceptible to environmental
interference: the barometer to pressure disturbances from propeller wash and
airflow over vents, the magnetometer to magnetic fields from motors, ESC, and
battery current. Placement and calibration are critical for both.

---

## Concept

### Barometer — pressure to altitude

Air pressure decreases with altitude at approximately −12 Pa/m near sea level
(International Standard Atmosphere). The barometer measures this pressure
continuously, and the FC converts pressure to altitude using the barometric
altitude formula. This gives a relative altitude reference — not absolute
above sea level, but altitude change since power-up.

The SPL06-001 barometer on the H7A3-SLIM uses a piezoresistive MEMS element
that changes resistance as pressure flexes a thin silicon diaphragm. It
provides altitude resolution of approximately 10 cm at sea level.

The barometer has two known failure modes in drone applications:

**Propeller wash pressure disturbance:** The airflow induced by the propellers
creates a pressure differential near the body of the drone. The barometer,
if exposed to this flow, measures a combination of static atmospheric pressure
and dynamic pressure from airflow — giving an incorrect altitude reading.
The H7A3-SLIM's barometer is covered by a small foam pad that damps rapid
pressure fluctuations while allowing slow ambient pressure changes to reach
the sensor.

**Altitude hold wind error:** In windy conditions, pressure fluctuations from
gusts can cause the barometer to read brief altitude changes that are not
real. GPS altitude (which does not have this problem) is fused with barometer
altitude in position hold modes to reduce this effect.

### Magnetometer — measuring Earth's field

Earth's magnetic field has both direction (toward magnetic north) and
magnitude (~50 µT). The magnetometer measures all three components (X, Y, Z)
of this field vector. When the drone is level, the horizontal components
give the heading.

The magnetometer is susceptible to two classes of interference:

**Hard-iron interference:** permanent magnets near the sensor (speaker magnets
in buzzers, motor magnets, battery chemistry) create constant magnetic offsets
that deflect the measured field. Calibration compensates for hard-iron by
measuring the field in all orientations and finding the offset.

**Soft-iron interference:** magnetically permeable materials (iron, steel, some
grades of stainless) near the sensor distort the shape of the field, making the
measured field direction incorrect even after hard-iron calibration.

Current in nearby wires also creates magnetic fields. A wire carrying 20A
at 30 mm distance creates ~130 µT — comparable to Earth's field. This is why
the compass must be at the nose of the drone, far from all high-current wiring.
Even 10 mm of additional separation reduces the field by ~50% (field falls
as 1/r² for a straight wire).

---

## Reference

### Barometer specification (SPL06-001, internal to H7A3-SLIM)

| Parameter | Value |
|---|---|
| Pressure range | 300–1100 hPa |
| Pressure resolution | 0.06 Pa (absolute) |
| Altitude resolution | ~10 cm at sea level |
| Interface | I2C / SPI |
| Update rate | Up to 128 Hz |

### Magnetometer (QMC5883, in M10Q-5883)

| Parameter | Value |
|---|---|
| Measurement range | ±2 gauss |
| Resolution | ~2 mG |
| Interface | I2C at 400 kHz |
| Update rate | Up to 200 Hz |
| Placement | Front bracket, nose of drone |

### Effect of payload magnets on compass

Payload modules that include solenoids, high-current traces, or magnetic
sensors should be evaluated for compass interference. Measure compass
heading with and without payload fitted — a deviation > 5° indicates
significant interference that must be compensated by re-running calibration
with the payload fitted.

---

## Procedure

### Barometer verification

1. After arming in Betaflight OSD: altitude should read approximately 0 m
   (or the current altitude above the arm point).
2. Lift the drone by hand to approximately 1 m above the ground. OSD altitude
   should increase by ~1 m within 1–2 seconds.
3. If altitude reads erratically: check that the barometer foam pad is in place
   and uncompressed. Damaged or missing foam allows prop wash to disturb the reading.

### Magnetometer calibration

→ See [[gnss-gps]] §Compass calibration for the procedure. Run calibration
after: initial build, any change to payload or battery that adds magnetic
material near the sensor, and if compass heading diverges from GPS ground
track during level flight.

---

## Rationale

### Why the barometer has a foam pad

The barometer measures static pressure. Propeller airflow has both static and
dynamic components. Without a foam pad, the barometer reads static + dynamic
pressure — incorrectly showing altitude changes during throttle changes.
The foam damps rapid pressure fluctuations (which are from airflow dynamics)
while passing slow atmospheric pressure changes (which are from real altitude
changes). The foam must be foam, not tape — tape blocks the sensor entirely.

---

## Connections

requires:
  - [[flight-controller-hardware]]
related:
  - [[gnss-gps]]
  - [[imu-gyroscope]]
leads_to:
  - [[gnss-gps]]
