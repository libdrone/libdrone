---
id: betaflight-gps-rescue
title: "Betaflight GPS Rescue"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - software-stack
personas:
  - 1.builder
  - 2.operator
  - 4.workshop
platform:
  - pro
  - ghost
  - bandit
lang: en
licence: CC BY-SA 4.0
---

## Summary

GPS Rescue is Betaflight's automatic return-to-home failsafe. When the RC
link is lost for longer than the configured timeout, the FC switches to
GPS-guided navigation: it climbs to a safe altitude, heads toward the arm
point, and descends when it arrives. GPS Rescue requires a GPS fix of
at least 8 satellites acquired before arming. The home point is recorded
at arm time — if the pilot moves after arming, GPS Rescue returns the drone
to where the pilot was standing when they armed. All parameters in the base
configuration are conservative defaults; the return altitude must be adjusted
for local terrain and obstacles before each deployment.

---

## Concept

### What GPS Rescue does

When RC link loss is detected for longer than `failsafe_delay` (default 1s),
Betaflight transitions through its failsafe stages:

1. **Stage 1** (link loss detected): holds last known stick positions briefly
2. **Stage 2** (failsafe activated): GPS Rescue takes over
   - Climbs to `gps_rescue_angle` (configured as approach angle, not altitude
     directly — see below) while heading toward home
   - Navigates home using GPS position
   - Descends and lands when over the home point
   - Disarms on landing

If GPS link is lost during Rescue (insufficient satellites), the FC falls
back to angle mode with disarm on impact.

### Home point and why it matters

The home point is recorded at the moment of arming — the GPS position at that
exact instant. This has two important implications:

1. **Walk then arm**: if the pilot arms the drone and then walks away to fly
   it remotely, GPS Rescue will return the drone to the arm location, not to
   the pilot's current position. Arm from the intended landing/recovery area.

2. **Re-arm after moving**: if a flight involves landing at a different location
   and re-arming, the new home point is the new arm location. No manual
   home-point update is needed — it always records automatically.

### Return altitude

`gps_rescue_throttle_hover` and `gps_rescue_angle` together determine the
return flight profile. The return altitude must clear all obstacles between
the drone's position and the home point. There is no obstacle awareness in
GPS Rescue — it flies a straight line at the configured approach.

For each deployment: estimate the maximum obstacle height along the return
path, add at least 10 m clearance, and set the return altitude accordingly.
The default configured in the base diff (return profile conservative for open
terrain) must be reviewed before flying near structures, trees, or antennas.

### Minimum satellite requirement

`gps_rescue_min_sats = 8` means GPS Rescue will not activate unless at least
8 satellites were visible when the drone was armed. If fewer than 8 satellites
are available at arm time, GPS Rescue is silently disabled — link loss will
cause the drone to enter angle-mode failsafe instead of returning home.

The OSD should display satellite count at all times. Do not arm with fewer
than 8 satellites visible if GPS Rescue is operationally required.

---

## Reference

### GPS Rescue configuration parameters (base diff values)

| Parameter | Value | Notes |
|---|---|---|
| `failsafe_procedure` | `GPS-RESCUE` | Activates GPS Rescue on link loss |
| `gps_rescue_min_sats` | 8 | Minimum satellites at arm time |
| `gps_rescue_angle` | 32 | Approach tilt angle (degrees) |
| `gps_rescue_throttle_min` | 1150 | Minimum throttle during rescue |
| `gps_rescue_throttle_max` | 1700 | Maximum throttle during rescue |
| `gps_rescue_throttle_hover` | 1400 | Hover throttle estimate for rescue |
| `gps_rescue_sanity_checks` | `RESCUE_SANITY_ON` | Abort rescue if behaviour is unsafe |

### GPS Rescue pre-flight checklist

- [ ] Satellite count ≥ 8 before arming (check OSD)
- [ ] Arm from intended recovery area
- [ ] Return altitude configured for local terrain and obstacles
- [ ] GPS Rescue manually tested at low altitude on first deployment at new site
- [ ] Battery sufficient for full return distance plus descent

### Testing GPS Rescue

On first deployment at any new location, test GPS Rescue manually:

1. Arm and fly to 15–20 m altitude and 30–50 m from arm point.
2. Activate GPS Rescue via SE switch (manual trigger).
3. Observe: drone should orientate toward home, maintain altitude, and
   approach the arm point.
4. Regain control via SE switch (releasing manual trigger restores RC control).
5. If rescue behaviour is incorrect (wrong direction, wrong altitude): land
   immediately and review GPS Rescue parameters and home point.

---

## Procedure

### Adjusting return altitude for a new site

1. Identify the highest obstacle along the likely return path (trees,
   buildings, powerlines, terrain).
2. Estimate its height above the arm point.
3. Set `gps_rescue_throttle_hover` to a value that produces altitude
   approximately 10–15 m above that obstacle.
4. Calibrate `gps_rescue_throttle_hover` by flying to the target altitude and
   reading the OSD throttle value in hover. Set the parameter to this value.
5. Document the site-specific value. Reset to the conservative default when
   moving to a new site.

---

## Rationale

### Why `RESCUE_SANITY_ON` is mandatory

Sanity checks abort GPS Rescue if the drone is not moving toward home or is
descending outside the home zone. Without sanity checks, a GPS Rescue
activated near the edge of available satellite visibility could cause the
drone to fly in an incorrect direction indefinitely. Sanity checks are a
safety backstop — they cause GPS Rescue to abort and disarm rather than
fly the drone further from home if something is clearly wrong.

---

## Connections

requires:
  - [[betaflight-setup]]
  - [[gnss-gps]]
related:
  - [[betaflight-profiles]]
  - [[closed-loop-control]]
  - [[ardupilot-failsafe]]
leads_to:
  - [[pid-tuning-rate-profile]]
