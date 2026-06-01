---
id: power-sequencing
title: "Power sequencing"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - power-systems
personas:
  - 1.builder
  - 2.operator
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Connecting the battery on libdrone initiates a fixed power-up sequence. The
ESC main bus charges immediately; the flight controller starts ~100 ms later;
Betaflight initialises and runs gyro calibration for 3 seconds (the drone
must not move during this window); the ELRS receiver connects; and GPS
acquires a fix over 30–90 seconds. Only after GPS fix should the pilot arm.
The sequence is not configurable — it is determined by the hardware and
firmware startup behaviours. Understanding it prevents the most common
first-flight errors.

---

## Concept

### The 3-second gyro calibration window

The gyroscope calibration at startup measures the sensor's zero-rate offset —
the output the gyro produces when the drone is perfectly stationary. This
offset is subtracted from all subsequent readings so that a stationary drone
shows zero rotation rate.

If the drone moves during calibration, the calibration captures motion as
zero — offset. Every subsequent gyro reading is wrong by that amount. The
drone will drift continuously in the calibrated-wrong direction, requiring
constant stick input to stay level. Worse, the PID loop sees a persistent
non-zero rate and fights it, increasing motor temperature and reducing battery
life.

The calibration window is 3 seconds from the moment Betaflight initialises
(approximately 100–200 ms after battery connection). During this window, the
drone must sit completely still on a flat surface.

### GPS fix before arming

GPS position is recorded as the home point at the moment of arming. This home
point is used for:
- GPS position hold (holds the arming position)
- GPS Rescue / Return to Home (navigates back to the home point if RC link is lost)

If the pilot arms before GPS fix, the home point is not set. GPS Rescue is
unavailable. If the RC link fails, Betaflight falls back to attitude hold —
the drone maintains its current attitude but does not navigate home. In open
terrain this is manageable; near obstacles it is dangerous.

GPS cold start (no recent position data) takes 30–90 seconds for the M10Q-5883
to acquire a fix with 8+ satellites. Warm start (recent position data saved)
takes 5–15 seconds. Galileo + GPS dual-constellation improves fix time by
providing more visible satellites, particularly at high latitudes.

Betaflight shows GPS fix status in the OSD — the satellite count icon. Do not
arm until the OSD shows the configured minimum satellite count (default: 8).

### Full power-up sequence

    t = 0 ms     Battery connects
    t = 0 ms     ESC main bus charges (XT60 → capacitor → ESC)
    t = 100 ms   FC BEC powers on (internal LDO startup time)
    t = 100 ms   H7A3-SLIM begins Betaflight initialisation
    t = 200 ms   ELRS receiver powers on via BEC
    t = 200 ms   GPS module powers on via BEC
    t = 300 ms   Betaflight begins 3-second gyro calibration
                → DO NOT MOVE during t=300ms to t=3300ms
    t = 700 ms   ELRS receiver acquires transmitter link
    t = 3300 ms  Gyro calibration complete. FC shows "ready to arm" in OSD
    t = 30–90 s  GPS acquires fix (cold start)
    t = 30–90 s  Arm (after GPS fix confirmed)

### Power-off sequence

There is no controlled power-off sequence. Removing the battery simultaneously
cuts all power domains. Best practice: disarm first, wait 2 seconds (allows
Betaflight to flush Blackbox buffer to flash memory), then remove battery.
Removing battery while armed is not dangerous but may lose the last few seconds
of Blackbox data.

---

## Reference

### Startup indicators (Betaflight OSD)

| Indicator | Meaning |
|---|---|
| "CALIB" or gyro icon | Gyro calibration in progress — do not move |
| "DISARMED" | Calibration complete, ready to arm |
| Satellite count < 8 | GPS still acquiring — do not arm yet |
| Satellite count ≥ 8 | GPS fix confirmed, safe to arm |
| Battery voltage in OSD | Power domain active and monitored |

### ELRS binding and first connection

On first use, the ELRS receiver requires binding to the transmitter. Binding
is a one-time procedure that stores the transmitter's UID in the receiver.
After binding, the receiver connects automatically within 500 ms of power-up
whenever the transmitter is on and in range.

If the receiver does not connect (OSD shows no RSSI), check: transmitter is
powered and in correct RF mode (2.4 GHz ELRS); receiver and transmitter are
on the same ELRS version; receiver LED is blinking (searching), not off (no power).

---

## Procedure

### Standard pre-flight power-up

1. Place drone on flat, stable surface.
2. Ensure transmitter is powered and RC link is active.
3. Connect battery.
4. **Do not touch drone for 5 seconds** (3 s calibration + 2 s margin).
5. Verify OSD shows: battery voltage, "DISARMED", receiver RSSI, gyro
   calibration complete.
6. Wait for satellite count ≥ 8 in OSD.
7. Arm.

### If gyro calibration is suspected to be wrong

Symptoms: drone drifts consistently in one direction in stabilised mode;
requires persistent stick input to hover level; PID loop sounds laboured.

1. Disarm. Land.
2. Remove battery, wait 5 seconds.
3. Place drone on flat, stable surface.
4. Reconnect battery. **Do not touch for 5 full seconds.**
5. Re-arm and test hover.

If drift persists after confirmed clean calibration: check for mechanical
asymmetry (bent arm, different prop sets), then check Betaflight accelerometer
calibration.

---

## Rationale

### Why the gyro calibration cannot be extended

3 seconds is the window Betaflight allocates to average out sensor noise and
measure the zero-rate offset. Longer calibration would improve precision
marginally but would add to pre-flight time with diminishing returns —
3 seconds is sufficient for the sensor's noise floor to average to a stable
value. The operator's cost of keeping the drone still for 3 seconds is zero
if the pre-flight procedure is followed correctly.

### Why GPS fix is a hard gate before arming

An armed drone without GPS Rescue enabled will fly normally until RC link
is lost, then switch to attitude hold and drift with the wind until battery
is exhausted or it hits something. GPS Rescue requires a valid home point.
A valid home point requires GPS fix at arming time. The 30–90 second wait
for GPS fix is the single biggest time cost in the pre-flight sequence —
but it is not optional for safe operation in any area with obstacles.

---

## Connections

requires:
  - [[lipo-batteries]]
  - [[power-rail-architecture]]
related:
  - [[closed-loop-control]]
leads_to:
  - [[piloting-operations]]


[lipo-batteries]: lipo-batteries.md "LiPo batteries"
[power-rail-architecture]: power-rail-architecture.md "Power rail architecture"
[closed-loop-control]: closed-loop-control.md "Closed-loop control"
[piloting-operations]: piloting-operations.md "Piloting and operations"
