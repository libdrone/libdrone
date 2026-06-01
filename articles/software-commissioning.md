---
id: software-commissioning
title: "Software commissioning"
version: 1.1.0
date: 2026-05-31
author: jsa
status: released
scope: libdrone
topic:
  - software-stack
personas:
  - 1.builder
  - 4.workshop
platform:
  - pro
  - core
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

Software commissioning configures all firmware layers in sequence: EdgeTX
transmitter model, Betaflight flight controller, AM32 ESC, HDZero VTX and
goggles. Each layer must be complete and verified before the next begins —
a mis-configured UART in Betaflight will cause the GPS to show zero satellites
regardless of how well the GPS hardware is installed. The commissioning
sequence ends with Blackbox enabled, low-speed profile calibrated, and a
complete configuration backup committed to the repository. Estimated duration:
6 hours including sensor logger setup.

---

## Concept

### Why commissioning is a separate phase from hardware installation

Hardware integration (Phase 5) places and solders components. Software
commissioning (Phase 6) configures them to work together as a system.
A correctly soldered drone with misconfigured firmware is not flyable.
The two phases are separated because they require different tools, different
attention, and different verification methods — soldering requires physical
inspection, commissioning requires Betaflight Configurator and a working
RC link.

### Commissioning sequence dependency

The commissioning steps have hard dependencies:

1. EdgeTX must be configured before ELRS binding can be tested
2. ELRS must be bound before Betaflight Receiver tab can be verified
3. Betaflight UARTs must be assigned before GPS, VTX, and payload can
   communicate with the FC
4. Betaflight must be configured before ESC motor directions can be verified
   (requires arming logic)
5. Everything above must complete before low-speed mode can be calibrated
   (requires outdoor GPS fix)

Skipping steps or reversing order does not save time — it creates debugging
work when a downstream step fails for an upstream reason.

---

## Reference

### Commissioning checklist

**6.1 EdgeTX setup**
- TX16S model created: ELRS 250Hz LBT, channel order AETR
- Switch assignments per [[edgetx-model]] reference (SA arm, SD mode, SE rescue,
  SB rate/speed, SH buzzer)
- ELRS Backpack configured (goggle video link)
- Arm (SA) configured with throttle-low logical gate

**6.2–6.3 Betaflight firmware and ports**
- Flash Betaflight 4.5 `MATEKH743` target
- UART assignments per [[betaflight-setup]] reference table
- GPS on UART2 57,600 baud; CRSF on UART3 auto; VTX on UART1 115,200

**6.4–6.8 Betaflight configuration**
- DSHOT600, BiDShot ON, 14 poles, Props In, GPS feature enabled
- Voltage scale calibrated to ±0.2V of multimeter
- PID starting values entered exactly per base diff
- RPM filter ON — verify BiDShot RPM readout in Motors tab
- Three rate profiles entered; SB rate/speed switch confirmed
- PID Profile 2 linked to SB position 1 (throttle cap follows the switch) —
  verify on bench per [[betaflight-profiles]]

**6.9 GPS Rescue**
- Minimum 8 satellites gate
- Return altitude set for local terrain
- Failsafe → GPS Rescue confirmed

**6.10 AM32 ESC**
- 48kHz PWM, Props In, BiDShot ON, extended telemetry
- Motor directions verified in Betaflight Motors tab (all correct for True-X)

**6.11–6.13 HDZero VTX and goggles**
- MSP DisplayPort on UART1 confirmed
- 1080p60 selected
- OSD layout: GPS speed, ESC temp, home arrow, battery voltage visible
- Goggles firmware current; DVR capacity checked

**6.14 Low-speed profile calibration**
- SB position 1 active (training/low-speed)
- Fly straight at full throttle, read GPS speed in OSD
- Adjust `throttle_limit_percent` until GPS speed ≤ 4.8 m/s
- Document calibrated value in build log

**6.15 Blackbox**
- Device: onboard flash
- Rate: 1/2 (500Hz)
- GYRO_SCALED debug mode
- Confirm ≥50% flash space available

**6.16 Compass calibration**
- Outdoors, away from metal structures and power lines
- Rotate through all 6 axes in Betaflight Calibration wizard
- Confirm compass heading agrees with known direction (±10°)

**6.17–6.18 Post-commissioning checks**
- Re-verify motor mount torque after all power cycles
- Full configuration backup: Betaflight diff, AM32 settings, HDZero config,
  EdgeTX model — all saved to repository

**6.19 Sensor logger (if payload fitted)**
- Flash ESP32-S3 with MicroPython
- Install SEN66 library and logger script
- Verify I2C connection to SEN66
- Verify SD card write
- Bench test: 30-minute log run, check timestamps and data quality

---

## Procedure

### Low-speed calibration procedure

1. Outdoors in calm conditions, GPS fix ≥ 8 satellites.
2. Arm. Select SB position 1 (low-speed).
3. Fly a straight horizontal pass at full stick throttle away from the pilot.
4. Note peak GPS speed from OSD (or post-flight from Blackbox).
5. If peak > 4.8 m/s: reduce `throttle_limit_percent` by 5 in CLI.
6. If peak < 3.5 m/s: increase `throttle_limit_percent` by 5.
7. Repeat until peak is consistently 3.8–4.5 m/s.
8. `save` in CLI. Document value in build log with payload weight used.

### Configuration backup

# Betaflight diff — connect FC via USB, open CLI
    diff all
# Copy output to: firmware/betaflight_diff_V246_YYYYMMDD.txt

# AM32 — export settings via ESC Configurator
# HDZero — export from VTX web interface
# EdgeTX — backup via EdgeTX Companion

Commit all backup files to the repository before the maiden flight. If a
firmware update corrupts a configuration, the last-known-good state must be
recoverable from version control.

---

## Rationale

### Why EdgeTX before Betaflight

EdgeTX channel assignments determine which Betaflight AUX channels map to which
radio switches. Configuring Betaflight Modes before confirming EdgeTX channel
output will produce either correct results by coincidence or wrong results that
require rework. The correct sequence is: transmitter (what channels does the
radio send?) → flight controller (what do those channels mean?).

---

## Connections

requires:
  - [[electronics-installation]]
  - [[betaflight-setup]]
  - [[edgetx-model]]
related:
  - [[betaflight-profiles]]
  - [[betaflight-gps-rescue]]
  - [[pid-tuning-rate-profile]]
leads_to:
  - [[acceptance-validation]]


[edgetx-model]: edgetx-model.md "EdgeTX model configuration"
[betaflight-setup]: betaflight-setup.md "Betaflight setup"
[betaflight-profiles]: betaflight-profiles.md "Betaflight profiles and modes"


[edgetx-model]: edgetx-model.md "EdgeTX model configuration"
[betaflight-setup]: betaflight-setup.md "Betaflight setup"
[betaflight-profiles]: betaflight-profiles.md "Betaflight profiles and modes"

[electronics-installation]: electronics-installation.md "Electronics installation"
[betaflight-gps-rescue]: betaflight-gps-rescue.md "Betaflight GPS Rescue"
[pid-tuning-rate-profile]: pid-tuning-rate-profile.md "PID tuning and rate profile"
[acceptance-validation]: acceptance-validation.md "Acceptance validation"
