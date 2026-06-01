---
id: survey-imaging
title: "Survey and mapping imaging"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - aerial-imaging
personas:
  - 2.operator
  - 3.payload-dev
  - 6.evaluator
platform:
  - pro
  - bandit
lang: en
licence: CC BY-SA 4.0
---

## Summary

Survey and mapping missions require systematic, repeatable flight paths and
GPS-tagged imagery. On libdrone, survey missions are flown in GPS position
hold mode at a planned altitude, with the camera triggered at defined intervals
or by pilot input. The GX12 payload interface provides the GPS position, camera
control GPIO, and data logging infrastructure. Photogrammetric survey (overlapping
images processed into 3D models or orthomosaics) requires 60–80% forward and
lateral overlap between frames. Air quality mapping is a sensor survey variant
where the data stream replaces imagery — but the flight pattern planning principles
are identical.

---

## Concept

### Survey flight patterns

**Lawn-mower pattern**: parallel passes at constant altitude, each offset
laterally by a distance that provides the required overlap with the adjacent
pass. The simplest and most common survey pattern. On libdrone's Bandit
(ArduPilot), this is executed automatically as a waypoint mission. On
Core/Pro (Betaflight), it requires manual flying of the passes.

**Crosshatch pattern**: two sets of parallel passes at 90° to each other.
Provides better photogrammetric reconstruction quality for areas with complex
geometry or when shadow direction makes single-direction passes insufficient.
Doubles flight time.

**Orbit/circle**: the drone orbits a point-of-interest at constant radius
and altitude, with the camera aimed at the centre. Useful for 3D model
construction of structures or for documenting a specific location from all
sides.

### Overlap requirements for photogrammetry

Photogrammetric reconstruction requires finding the same physical point in
multiple overlapping images (feature matching). The overlap must be sufficient
for reliable feature matching:

- **Forward overlap** (between consecutive frames on the same pass): 60–80%
- **Side overlap** (between adjacent passes): 60–70%

Higher overlap: more processing time, more images, but better reconstruction
quality and fewer gaps. Lower overlap: faster data collection, but risk of
reconstruction failures at edges or in low-texture areas.

For a drone flying at 3 m/s at 30 m altitude with a 90° FOV camera:

    Ground footprint ≈ 2 × altitude × tan(FOV/2) ≈ 60 m wide
    Pass spacing for 60% side overlap: 60 × (1 − 0.60) = 24 m between pass centrelines
    Frame interval for 60% forward overlap: 60 × (1 − 0.60) / 3 m/s ≈ 8 s per frame

### Air quality mapping as a survey variant

Air quality mapping using the SEN66 payload is structurally identical to
photogrammetric survey, with sensor readings replacing images. The SEN66
logs data at 1 Hz, GPS-tagged. The "pixel" is the GPS position at each
1-second sample.

Flight parameters for urban air quality mapping:
- Altitude: 15–30 m (above traffic and building-induced turbulence, below
  the mixing layer for reliable street-level measurements)
- Speed: 2–4 m/s (slow enough for representative sampling at each position)
- Pass spacing: 20–50 m depending on the resolution required for the
  pollution map
- Avoid hovering over traffic — vehicle exhaust directly under the drone
  contaminates the local measurement

The SEN66 has a response time of approximately 30 seconds to new particulate
conditions. This means the drone must fly through a zone for at least 30 seconds
before PM2.5 readings represent the ambient conditions at that location. Fast
passes through a zone underestimate PM if there is a source in that zone.

### GPS-triggered imaging with GX12

The GX12 Connector B PIN 6 (AUX GPIO 2) is the camera trigger line. The pilot
activates it via TX16S switch SA (VTX power switch, repurposable for survey).
The payload's ESP32-S3 receives the GPIO signal and triggers the camera shutter.

Automated triggering at defined intervals (time-based or distance-based) requires
ArduPilot (Bandit platform) with a mission defining the trigger interval and
the survey grid. On Betaflight (Pro platform), triggering is manual — the pilot
activates the switch at each trigger point along the pass.

---

## Reference

### Survey mission parameters by application

| Application | Altitude | Speed | Overlap / Spacing | Trigger |
|---|---|---|---|---|
| Photogrammetric 3D model | 30–50 m | 3–5 m/s | 70% forward, 65% side | Every 5–8 s |
| Orthomosaic map | 50–80 m | 5–8 m/s | 70% forward, 70% side | Every 5–8 s |
| Building inspection | 5–20 m | 1–2 m/s | Manual | Manual |
| Air quality grid | 15–30 m | 2–4 m/s | Pass spacing 20–50 m | Continuous (1 Hz sensor) |

### Post-flight data workflow

**Photogrammetric imagery:**
1. Download images from payload SD card via USB or WiFi sync to NAS
2. Import to photogrammetry software (Metashape, OpenDroneMap)
3. Align photos using GPS coordinates + feature matching
4. Build 3D model or orthomosaic
5. Export GeoTIFF or point cloud

**Air quality data:**
1. WiFi sync JSONL log file from payload to local NAS on landing
2. Import GPS-tagged readings to GIS software or custom Python analysis
3. Interpolate between points to produce a continuous concentration map
4. Overlay on street map for contextual display

---

## Procedure

### Manual survey pass on Betaflight platform

1. Plan the survey grid: calculate pass spacing and number of passes for
   required coverage and overlap.
2. Mark start and end waypoints visually (physical markers on the ground).
3. Fly the first pass at constant altitude and speed. Trigger camera at
   consistent intervals using the AUX switch.
4. At the end of the pass, turn and establish the next pass heading.
5. Fly subsequent passes maintaining consistent altitude and spacing.
6. After the last pass, land and review the first few images on the OSD or
   via payload status to confirm trigger timing was correct before deploying
   the full session.

---

## Rationale

### Why automated survey missions are Bandit-only in V2.4.6

ArduPilot's mission planning (via Mission Planner or QGroundControl) supports
fully automated survey grid generation, waypoint missions, and defined trigger
intervals. Betaflight is not designed for autonomous navigation — it provides
excellent manual attitude control but no mission planning. The Bandit platform
(ArduPilot) handles survey automation; Core/Pro (Betaflight) handles manual
and GPS-hold-assisted operations. This is a design choice, not a limitation —
the platforms are matched to their operational modes deliberately.

---

## Connections

requires:
  - [[aerial-imaging-basics]]
  - [[gnss-gps]]
  - [[payload-integration]]
related:
  - [[jello-effect-mitigation]]
  - [[induced-velocity]]
  - [[thermal-imaging-payload]]
  - [[wildlife-survey-operations]]
leads_to:
  - [[piloting-operations]]
  - [[wildlife-survey-operations]]


[aerial-imaging-basics]: aerial-imaging-basics.md "Aerial imaging basics"
[gnss-gps]: gnss-gps.md "GNSS and GPS"
[payload-integration]: payload-integration.md "Payload integration"
[jello-effect-mitigation]: jello-effect-mitigation.md "Jello effect mitigation"
[induced-velocity]: induced-velocity.md "Induced velocity and sensor placement"
[thermal-imaging-payload]: thermal-imaging-payload.md "Thermal imaging payload"
[wildlife-survey-operations]: wildlife-survey-operations.md "Wildlife survey operations"
[piloting-operations]: piloting-operations.md "Piloting and operations"
