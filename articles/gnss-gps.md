---
id: gnss-gps
title: "GNSS and GPS"
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
  - 1.builder
platform:
  - bandit
  - core
  - pro
lang: en
licence: CC BY-SA 4.0
---

## Summary

A GNSS receiver calculates geographic position from the measured travel time
of signals from multiple satellites. Four satellites are the minimum to solve
for three position coordinates plus receiver clock error simultaneously. libdrone
uses the Matek M10Q-5883, configured for GPS + Galileo + BeiDou with GLONASS
disabled. EGNOS SBAS augmentation reduces position error from 2–5 m to
0.5–1.5 m CEP over Europe. GPS Rescue requires a valid home point (recorded at
arm time) and a minimum of 8 satellites — fly only after GPS fix is confirmed.

---

## Concept

### How GNSS positioning works

Each satellite continuously broadcasts a precisely timestamped signal. The
receiver measures the difference between the time the signal was sent (encoded
in the signal) and the time it arrived. Travel time × speed of light = distance
from that satellite.

With known distances from three satellites, the receiver's position lies at
the intersection of three spheres — which gives two candidate points (one
on Earth's surface, one in space). Four satellites eliminate the clock error
ambiguity: the receiver's clock is imprecise, adding an unknown timing offset.
Four range equations with four unknowns (latitude, longitude, altitude, clock
error) yield a unique solution. More satellites improve accuracy by
over-constraining the solution.

### Constellations and why multiple constellations matter

GPS (US, 31 satellites), Galileo (EU, 28 satellites), BeiDou (China, 35+
satellites), and GLONASS (Russia, 24 satellites) all broadcast at overlapping
frequencies. A dual- or triple-constellation receiver sees more satellites from
any location, giving better geometry (lower PDOP), faster fix acquisition, and
redundancy if one constellation is unavailable.

libdrone configuration: **GPS + Galileo + BeiDou enabled. GLONASS disabled.**

GLONASS is disabled because near the eastern borders of the Czech Republic,
GLONASS jamming has been observed. A GLONASS satellite at degraded signal level
can corrupt the combined position solution even without providing a valid fix.
Disabling the constellation removes the attack vector. With GPS + Galileo +
BeiDou and clear sky, 18–26 satellites are typically visible — more than
sufficient for an accurate, fast fix.

### EGNOS augmentation

EGNOS (European Geostationary Navigation Overlay Service) is the European
Satellite-Based Augmentation System. A network of precisely surveyed ground
stations across Europe continuously measure their own GPS-derived positions,
compare them to their known exact positions, and broadcast the difference as
correction data via geostationary satellites at 1575.42 MHz (same frequency
as GPS L1).

Receivers that use EGNOS apply these corrections, reducing position error from
the typical raw 2–5 m CEP to approximately 0.5–1.5 m CEP. For air quality
mapping where sensor readings are correlated with GPS coordinates, this matters
directly: a 1 m position accuracy means the pollution map correctly locates
readings to specific streets and buildings.

EGNOS is enabled by default in the M10Q-5883 configuration for libdrone. SBAS
signals are available across most of continental Europe. Over UK, Iceland, or
areas at the edge of EGNOS coverage, performance may be reduced.

### Compass and GPS interaction

The M10Q-5883 integrates both the GNSS receiver (M10 chip) and a magnetometer
(QMC5883). The compass provides heading for GPS navigation — GPS alone cannot
determine which direction the drone is pointing (only where it is). GPS Rescue
uses the compass to point the drone toward home. Position hold uses it to
maintain heading in wind.

The compass is mounted at the front of the drone on the GPS/camera bracket —
maximum physical separation from the ESC, battery leads, and motor wires.
A single motor wire carrying 20A at 30 mm distance creates a magnetic field
of approximately 130 µT at the compass — comparable to Earth's field (~50 µT).
Placement at the nose is mandatory. After any significant electronics layout
change (adding a payload, different battery), re-run compass calibration.

---

## Reference

### Matek M10Q-5883 specification

| Parameter | Value |
|---|---|
| GNSS chip | u-blox M10 |
| Constellations | GPS + Galileo + BeiDou (GLONASS disabled on libdrone) |
| SBAS | EGNOS enabled |
| Update rate | 10 Hz |
| Protocol | UBX (binary) |
| UART baud | 57,600 |
| Cold start TTFF | 30–90 s |
| Warm start TTFF | 5–15 s |
| Position accuracy (EGNOS) | 0.5–1.5 m CEP |
| Magnetometer | QMC5883 |
| Connector | JST-GH 6-pin |
| Mass | 15 g (including cable) |
| Mounting | Front bracket, above camera |

### GPS Rescue configuration

| Parameter | Betaflight setting |
|---|---|
| Minimum satellites to arm | 8 |
| Return altitude | 30 m (adjust for local terrain and obstacles) |
| GPS Rescue mode | Enabled |
| Home point | Recorded at arm time |

Home point is set when the drone arms, not when GPS fix is acquired. If the
pilot moves after arming (while walking to take-off position), the home point
reflects where the drone was standing, not where the pilot is standing. This
is important for return-to-home accuracy in the field.

---

## Procedure

### GPS module configuration (initial setup)

1. In Betaflight Configurator → Configuration: enable GPS, set protocol to UBX.
2. In Ports tab: set UART2 to GPS, baud 57,600.
3. Power cycle. In GPS tab: verify satellites are detected and increasing.
4. Configure constellations via UBX config or BetaflightGPS passthrough:
   enable GPS, Galileo, BeiDou; disable GLONASS.
5. Enable SBAS/EGNOS.
6. Verify in GPS tab: fix acquired, satellite count ≥ 8 in open sky.

### Compass calibration

1. In Betaflight Configurator → Calibration tab: initiate compass calibration.
2. Rotate the drone slowly through all orientations: nose up/down/left/right,
   all roll angles. Aim for smooth, continuous rotation covering the full sphere.
3. Keep all electronic components in their normal flight positions — payload,
   battery, everything. Calibrate with the full payload fitted if the payload
   contains any magnets or high-current wiring.
4. Save calibration. Verify in attitude display that heading rotates correctly
   as the drone is turned.

---

## Rationale

### Why GPS fix is required before arming (not just recommended)

→ See [[power-sequencing]] for the full rationale. In summary: without a GPS
fix at arm time, GPS Rescue has no home point and cannot function. In any
environment with obstacles — trees, buildings, pylons — a drone without GPS
Rescue is a single-point-of-failure system. The 30–90 second wait is not
optional for safe field operations.

---

## Connections

requires:
  - [[flight-controller-hardware]]
related:
  - [[barometer-magnetometer]]
  - [[power-sequencing]]
leads_to:
  - [[piloting-operations]]
