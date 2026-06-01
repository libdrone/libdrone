---
id: betaflight-setup
title: "Betaflight setup"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - software-stack
personas:
  - 1.builder
  - 4.workshop
  - 8.architect
platform:
  - core
  - pro
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

Betaflight is the open-source flight controller firmware running on libdrone's
Matek H7A3-SLIM. Initial setup requires flashing the correct firmware target,
applying the base configuration diff via CLI, setting board orientation,
calibrating battery voltage and current sensing, configuring UART port
assignments, and verifying motor direction. The base configuration diff
(`LD_V245_Betaflight_base`) covers all mandatory settings in a single paste
operation. No default Betaflight profile produces a flyable libdrone — the
diff must be applied before the maiden flight.

---

## Concept

### Firmware target and versions

Betaflight firmware is compiled per flight controller hardware. The correct
target for the H7A3-SLIM is `MATEKH743`. Flashing any other target will
produce a non-functional build. Betaflight 4.5 is the tested version for
libdrone V2.4.5/V2.4.6. Do not use 4.4 (missing filter improvements) or
pre-release builds.

### Configuration diff vs full dump

Betaflight stores configuration as key-value pairs. A "diff" is the minimal
set of settings that differ from Betaflight defaults — it can be applied
cleanly on top of a fresh flash without carrying over stale settings from
a previous build. A "dump" is the complete configuration including defaults —
it can produce unexpected results when applied to a different firmware version.

Always start from a fresh flash, then apply the libdrone diff. Never apply
a dump from a different firmware version.

### UART assignment must match physical wiring

The diff configures specific UARTs for specific functions. The physical wiring
on the H7A3-SLIM must match the UART assignments in the configuration.
If a device is soldered to UART2 but the diff configures UART2 as VTX and
UART1 as GPS, nothing will work correctly. Verify physical connections before
applying the diff, or apply the diff first and then wire to match.

---

## Reference

### Betaflight base configuration diff (LD-FW-001)

Apply in Betaflight Configurator → CLI tab. Paste the entire block and press
Enter after `save`.

    # MIXER / MOTORS
    mixer QUADX
    set motor_poles = 14
    set motor_pwm_protocol = DSHOT600
    set dshot_bidir = ON
    set motor_direction_inversion = ON

    # RECEIVER
    set receiver_type = SERIAL
    set serialrx_provider = CRSF

    # FEATURES
    feature GPS
    feature TELEMETRY
    feature OSD
    feature AIRMODE
    feature BLACKBOX

    # FAILSAFE / GPS RESCUE
    set failsafe_procedure = GPS-RESCUE
    set gps_rescue_angle = 32
    set gps_rescue_min_sats = 8
    set gps_rescue_throttle_min = 1150
    set gps_rescue_throttle_max = 1700
    set gps_rescue_throttle_hover = 1400
    set gps_rescue_sanity_checks = RESCUE_SANITY_ON

    # BATTERY (SUMMER DEFAULT)
    set vbat_min_cell_voltage = 35
    set vbat_warning_cell_voltage = 36
    set vbat_max_cell_voltage = 43
    set current_meter = ESC
    set battery_capacity = 1800

    # PIDs — V2.4.5 starting values (Profile 1)
    profile 1
    set p_roll  = 47
    set i_roll  = 85
    set d_roll  = 32
    set f_roll  = 105
    set p_pitch = 50
    set i_pitch = 85
    set d_pitch = 36
    set f_pitch = 105
    set p_yaw   = 42
    set i_yaw   = 85
    set d_yaw   = 0
    set f_yaw   = 100
    set iterm_relax_cutoff = 15
    set iterm_relax = RPY
    set iterm_rotation = ON
    set anti_gravity_gain = 5

    # FILTERS
    set gyro_lowpass_hz = 200
    set gyro_lowpass2_hz = 0
    set dterm_lowpass_hz = 100
    set dterm_lowpass2_hz = 0
    set dyn_notch_count = 3
    set dyn_notch_min_hz = 100
    set dyn_notch_max_hz = 600
    set dyn_notch_q = 250

    # BLACKBOX
    set blackbox_device = ONBOARD_FLASH
    set blackbox_rate_num = 1
    set blackbox_rate_denom = 2
    set blackbox_record_acc = ON

    save

### UART port assignments

Configure in Betaflight Configurator → Ports tab:

| UART | Configuration | Baud |
|---|---|---|
| UART1 | VTX (MSP DisplayPort) | 115200 |
| UART2 | GPS | 57600 |
| UART3 | Serial RX (CRSF) | — (auto) |
| UART4 | MSP (payload Connector A) | 115200 |
| UART5 | Serial passthrough (payload Connector B) | configurable |
| UART6 | Spare / companion | 921600 |

### Board orientation

If the FC is mounted with the arrow pointing forward: no adjustment needed.
If mounted rotated (common to avoid connector conflicts), set in
Configuration tab → Board and Sensor Alignment → Yaw Degrees = actual rotation.

---

## Procedure

### Initial setup sequence

1. Flash `MATEKH743` target with Betaflight 4.5 via Configurator.
2. Connect to Configurator. Go to CLI tab.
3. Type `defaults nosave` to reset to factory defaults without rebooting.
4. Paste the entire diff block above. Press Enter. Wait for `save` to complete.
5. Reboot (Configurator will reconnect automatically).
6. Go to Ports tab. Set UART assignments per the table above.
7. Go to Configuration tab → Battery Voltage → calibrate scale factor to match
   handheld multimeter reading within 0.2V.
8. Go to Motors tab → verify all four motors report eRPM when spun up
   (props removed, battery connected).
9. Verify motor directions in Motors tab — all must match expected rotation.
10. Go to Setup tab → rotate drone on all axes → verify 3D model responds correctly.

---

## Rationale

### Why the diff starts with `profile 1`

Betaflight supports multiple PID profiles. The diff explicitly sets Profile 1
as the base (chase) configuration. Profile 2 is left for the low-speed
compliance overlay. Applying the diff without specifying `profile 1` first
would write the PID values to whichever profile was last active — a
non-deterministic and error-prone outcome.

---

## Connections

requires:
  - [[flight-controller-hardware]]
  - [[dshot-protocol]]
  - [[rpm-filter]]
related:
  - [[betaflight-profiles]]
  - [[betaflight-gps-rescue]]
  - [[pid-derivative-term]]
  - [[pro-variant]]
leads_to:
  - [[betaflight-profiles]]
  - [[betaflight-gps-rescue]]


[flight-controller-hardware]: flight-controller-hardware.md "Flight controller hardware"
[dshot-protocol]: dshot-protocol.md "DShot protocol"
[rpm-filter]: rpm-filter.md "RPM filter"
[betaflight-profiles]: betaflight-profiles.md "Betaflight profiles and modes"
[betaflight-gps-rescue]: betaflight-gps-rescue.md "Betaflight GPS Rescue"
[pid-derivative-term]: pid-derivative-term.md "PID — derivative term"
[pro-variant]: pro-variant.md "Pro variant"
