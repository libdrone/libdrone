---
id: sk-wing-survey-guide
title: "Wing Survey Guide"
version: 1.1.0
date: 2026-06-01
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 2.operator
  - 6.evaluator
platform:
  - wing
lang: en
licence: CC BY-SA 4.0
---

## Summary

After reading this guide, an operator or service evaluator can plan and
execute a thermal wildlife survey mission with libdrone Wing from weather
check through report delivery. The guide covers the operational workflow
that distinguishes Wing from the multirotor family: fixed-wing efficiency,
thermal imaging constraints, dawn/dusk timing, and the detection processing
pipeline. Learning objective: the operator can deliver a GPS-referenced
wildlife detection report from a single Wing sortie.

---

## Concept

### The service, not the hardware

Wing's value is not in the hardware — it is in the report on the customer's
desk. A GPS map showing 23 deer at specific coordinates, confirmed at dawn
on a specific date, is something the customer can submit to a ministry
meeting. The drone is how you get that data. The processing pipeline is how
you turn that data into the deliverable.

This reframe has operational consequences. A technically successful flight
that produces no usable thermal data — because it was flown at the wrong
time of day or the wrong altitude — has zero commercial value. Pre-flight
planning is the primary quality gate, not the aircraft's performance.

→ [[wing-variant]] for the platform concept and airframe options.

### Why fixed-wing for this mission

A multirotor covering a 20-hectare field requires 8–10 battery cycles.
Wing covers it in one 45-minute sortie. The efficiency difference is not
incremental — it is categorical for area coverage.

Fixed-wing does not hover. Launch requires a hand throw or bungee; recovery
requires a clear landing zone or belly landing. These are operational
constraints, not deficiencies — if the mission requires hover, Wing is wrong;
if the mission requires area coverage, Wing is the correct tool.

→ [[fixed-wing-fundamentals]] explains why fixed-wing is categorically more
efficient for coverage missions.

### The thermal window

Thermal contrast between warm-blooded animals and ground peaks at dawn and
dusk in autumn and winter. Daytime surveys in warm weather produce no usable
data regardless of camera quality. The survey window is the operational
constraint that everything else is planned around.

→ [[thermal-imaging-payload]] covers the physics and camera selection.
→ [[wildlife-survey-operations]] has the window timing by season.

---

## Reference

### ArduPilot Plane vs Copter

Wing runs ArduPilot Plane (MatekH7A3-WING target), not ArduPilot Copter
(MatekH7A3 target). The firmware is different; the QGroundControl interface
is the same. Key Plane-specific concepts:

**TECS** (Total Energy Control System) manages throttle and pitch together
to maintain airspeed and altitude simultaneously. The operator specifies
target airspeed (12 m/s cruise) and altitude; TECS handles the rest.

**Elevon mixing** for flying wing: right stick right tilts right; both
sticks forward = pitch down. ArduPilot handles the elevon mixing internally
when FRAME_CLASS=2.

**Auto-takeoff**: arm with throttle at idle, hand-launch, switch to TAKEOFF
mode immediately. ArduPilot climbs at configured pitch angle to TKOFF_ALT
then transitions to AUTO.

→ [[ardupilot-plane]] for the full configuration reference.

### Survey coverage per battery

| Camera | Altitude | Swath | Overlap | Area per battery |
|---|---|---|---|---|
| FLIR Lepton 3.5 | 50m | ~53m | 30% | ~35 ha |
| FLIR Boson 320 | 50m | ~22m | 30% | ~18 ha |
| FLIR Boson 320 | 60m | ~26m | 30% | ~22 ha |

Values assume 3 m/s cruise speed, 45 min endurance, 30% side overlap.

---

## Procedure

### Pre-mission planning (evening before)

1. **Confirm thermal window**: check sunrise/sunset time. Plan to be airborne
   30 min before sunrise for dawn surveys.
2. **Check weather**: wind < 6 m/s sustained, no precipitation, temperature
   < 10°C for maximum contrast. Check forecast for the full survey window,
   not just launch time.
3. **Plan survey grid in QGroundControl** (offline, at home):
   - Draw field boundary polygon on cached map
   - Set altitude (50–60m AGL), camera trigger distance
   - Confirm flight path covers full area, ends with RTL
   - Estimate total flight time — ensure it fits within battery endurance
4. **Prepare equipment**: charge batteries, format SD card in ESP32-S3
   payload, cache QGC map tiles for the survey area.

### Launch day — T−45 min to T=0

**T−45 min**: Arrive at survey site. Set up GCS laptop. Power on Wing and
payload. Wait for GPS lock (HDOP < 1.5, ≥ 8 satellites).

**T−30 min**: Upload survey grid mission. Verify in Plan view — flight path
correct, RTL at end. Confirm payload camera trigger is active (test fire on
bench, confirm SD write LED).

**T−15 min**: Full pre-flight check: → [[pre-flight-check]] as baseline,
plus Wing-specific: control surface deflection correct (elevons), battery
secured in belly bay, no loose payload connectors.

**T=0 (thermal window opens)**: Hand-launch. Switch to TAKEOFF mode
immediately after release. Monitor climb in QGC. Confirm aircraft reaches
survey altitude before switching to AUTO.

### During survey

Monitor QGC Fly view: altitude (should hold within ±5m of plan), airspeed
(should hold at cruise ±2 m/s), battery, GPS quality. Be ready to override
AUTO if aircraft deviates from planned track — cross-track error > 10m
warrants investigation.

The aircraft is flying itself. The operator's job is situational awareness,
not stick inputs.

### Recovery and data retrieval

Wing executes RTL on mission completion or command. Monitor approach. For
belly landing: designate a flat 5m × 5m area at least 50m from the launch
point. For hand-catch: position the catcher downwind, motor should cut at
flare.

Immediately after landing: retrieve SD card from payload bay. Battery
voltage check — note remaining capacity for cycle log.

### Detection processing (field laptop)

1. Copy SD card images and GPS log to laptop
2. Run detection script: Python + OpenCV, identifies thermal blobs above
   confidence threshold, extracts GPS coordinates from image EXIF/log
3. Review detections manually — filter false positives (rocks, fence posts,
   water) by thermal signature shape and temperature offset
4. Generate KML for GIS overlay (QGIS)
5. Generate PDF report: date, area, detection count per species, GPS
   positions, representative thermal frames

→ [[wildlife-survey-operations]] has the full workflow with timing.

---

## Rationale

Wing is the only fixed-wing platform in the libdrone family and its
operational workflow differs fundamentally from all multirotor variants.
Hand-launch, TECS, auto-land, thermal window constraints, and the detection
processing pipeline are Wing-specific. A dedicated skeleton prevents Wing
operators from having to navigate a multirotor-centric operations manual
to find what applies to them.

---

## Connections

requires:
  - [[wing-variant]]
  - [[fixed-wing-fundamentals]]
  - [[ardupilot-plane]]
  - [[thermal-imaging-payload]]
  - [[wildlife-survey-operations]]
  - [[qgroundcontrol]]
related:
  - [[sk-ardupilot-operator-guide]]
  - [[legal-and-regulatory]]
  - [[esp32-s3-companion]]
  - [[gnss-gps]]
  - [[pre-flight-check]]
  - [[post-flight-check]]
leads_to:
  - [[wildlife-survey-operations]]
  - [[thermal-imaging-payload]]
  - [[legal-and-regulatory]]
