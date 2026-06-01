---
id: gps-antenna-placement
title: "GPS antenna placement"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - emc-signal-integrity
personas:
  - 5.student
  - 1.builder
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

GPS satellite signals arrive at −130 dBm — ten trillion times weaker than
a WiFi router. The GPS antenna must have an unobstructed sky view with no
electrically conductive material above it, maximum distance from all
high-current wiring, and no conducted noise on its supply line. Carbon fibre
is electrically conductive and blocks GPS signals entirely — an antenna above
a CF plate receives nothing. On libdrone, the M10Q GPS module sits at the top
of the nose bracket above the camera, providing a clear 180° sky view and
maximum separation from the ESC, battery, and motor wires.

---

## Concept

### Signal strength and why placement is non-negotiable

GPS L1 signals arrive from satellites at approximately −130 dBm. To put
this in context:

| Source | Power at receiver |
|---|---|
| WiFi router at 10 m | ~−60 dBm |
| Mobile phone signal | ~−80 dBm |
| GPS satellite signal | ~−130 dBm |

The GPS signal is 10 billion times weaker than a nearby WiFi router.
Any noise or interference that approaches this level can corrupt or prevent
a position fix. The GPS receiver achieves this sensitivity using spread
spectrum correlation — it knows exactly what signal pattern it expects and
can detect it even below the noise floor. But conducted noise on the supply
rail or nearby electromagnetic radiation can raise the effective noise floor
enough to lose the signal entirely.

### Carbon fibre and antenna shielding

Carbon fibre is a conductor. The fibres form a conductive mesh. A GPS patch
antenna placed above a carbon fibre plate cannot receive signals that must
pass through that plate — the plate acts as a Faraday shield, blocking the
electromagnetic wave.

This is why:
- GPS modules must never be mounted under a CF canopy or top plate
- Frames with CF top plates must use an antenna mast or a GPS module on a
  bracket above the plate
- The GPS antenna must face upward with no conductive material in the
  hemisphere above it (not even at an angle — the satellite geometry uses
  the full upper hemisphere)

libdrone's PETG sandwich and Platform are non-conductive — no shielding
issue. The GPS bracket places the M10Q above the camera, with open sky
in all upward directions.

### Separation from motor wires and ESC

A motor wire carrying 20 A at 30 mm from a magnetometer generates a
magnetic field of approximately 130 µT — comparable to Earth's field.
A motor wire at 150 mm (the nose-to-ESC distance on libdrone) generates
~2.6 µT — within calibration compensation range.

The GPS module's integrated QMC5883 magnetometer (compass) is what uses
this distance separation. The GPS receiver chip itself is primarily affected
by conducted noise on its supply and by RF interference near 1.575 GHz.

### Antenna orientation

GPS patch antennas are directional — they receive best from directly above
and reject signals from below. The patch must face upward, parallel to the
ground. Any tilt reduces the effective gain toward overhead satellites while
increasing sensitivity to multipath reflections from the ground. If the bracket
geometry creates any tilt, the Betaflight compass alignment offset must be
set to compensate before the maiden flight.

### The VTX antenna and GPS clearance

The VTX antenna (typically a monopole or cloverleaf mounted at the rear of
the drone) must not obstruct the sky view above the GPS patch antenna. On
libdrone, the VTX antenna mounts at the tail — maximum separation from the
nose-mounted GPS. This positioning is deliberate and must not be changed.

The 5.8 GHz VTX output at 200–800 mW transmit power can also cause
desensitisation of the GPS receiver if the VTX antenna is too close — the
strong 5.8 GHz signal overloads the GPS receiver's front-end amplifier.
At the nose-to-tail separation on libdrone's Platform, this is not an issue.

---

## Reference

### libdrone GPS module placement

| Parameter | Value |
|---|---|
| Module | Matek M10Q-5883 |
| Position | Top of GPS/camera bracket, drone nose |
| Bracket material | PETG (non-conductive) |
| Patch antenna orientation | Facing directly upward, level |
| Distance from ESC | ~150 mm (nose to electronics zone) |
| Distance from VTX antenna | ~250 mm (nose to tail) |
| GLONASS | Disabled (GNSS jamming risk near eastern EU borders) |
| Constellations active | GPS + Galileo + BeiDou |
| Typical satellites visible | 18–26 |
| EGNOS/SBAS | Enabled |
| Update rate | 10 Hz |
| Baud rate | 57,600 (UART2) |

### Compass calibration requirements

After any significant change to the drone's layout — fitting a new payload,
changing the battery position, adding a mast — recalibrate the compass in
Betaflight. Rotate the drone through all orientations (all 6 faces toward
down). Calibrate in an open area away from metal structures and high-voltage
power lines. Recalibrate if the drone consistently fails to hold heading in
GPS-assisted modes.

---

## Procedure

### First-time GPS verification

1. Arm the drone outdoors in open sky with GPS Rescue enabled.
2. Wait for GPS fix: OSD should show "GPS FIX" and a satellite count ≥ 8
   within 90 seconds (cold start). Warm start: within 15 seconds.
3. Walk 10 m from the drone. OSD distance reading should increase to ~10 m.
4. Return to the drone. OSD distance should return to ~0 m.
5. If satellite count does not reach 8 within 3 minutes in open sky:
   check that the M10Q is connected to UART2 at 57,600 baud in Betaflight
   Ports tab; verify the GPS cable is not routed through the power channel.

### Bracket removal and reinstallation

The GPS/camera bracket removes as one unit in under 60 s. After reinstallation:
1. Verify the bracket seats flush against the Platform nose face — no gap.
2. Verify the GPS patch antenna faces directly upward — use a level on the
   drone body and confirm the antenna surface is parallel to the body.
3. If any tilt is visible, set the compass alignment offset in Betaflight
   Configurator → GPS → Compass Alignment before the next flight.

---

## Rationale

### Why GLONASS is disabled

Near the eastern borders of the Czech Republic, GLONASS signal jamming has
been observed. A GNSS receiver that includes GLONASS will attempt to use
GLONASS satellites even at degraded signal levels. At low signal-to-noise
ratio, a GLONASS satellite contribution can corrupt the overall position
solution computed from all constellations — the receiver trusts a bad
measurement more than it should. With GPS + Galileo + BeiDou providing
18–26 satellites, GLONASS adds marginal accuracy benefit while introducing
a jamming vulnerability. The constellation is disabled.

---

## Connections

requires:
  - [[emc-noise-sources]]
  - [[power-signal-separation]]
related:
  - [[gnss-gps]]
  - [[barometer-magnetometer]]
  - [[ferrite-beads]]
leads_to:
  - [[conformal-coating]]
