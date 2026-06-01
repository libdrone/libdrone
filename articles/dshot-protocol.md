---
id: dshot-protocol
title: "DShot protocol"
version: 1.0.1
date: 2026-05-30
author: jsa
status: released
scope: generic
topic:
  - propulsion
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

DShot is the digital protocol that carries throttle commands from the flight
controller to the ESC. It replaced analog PWM by encoding the throttle value
as a digital packet with a CRC checksum — corrupted packets are discarded
rather than executed, eliminating the motor spikes that electrical noise caused
in analog systems. Bidirectional DShot (BiDi) extends the protocol: the ESC
uses the same wire to return the motor's eRPM every PID cycle. This eRPM
feedback is what makes the RPM filter possible. libdrone uses DShot600
(600 kbit/s) with bidirectional DShot enabled on all four ESC outputs.

---

## Concept

### Why analog PWM was insufficient

The original ESC protocol — inherited from RC servo control — was a 50 Hz
analog pulse: a pulse between 1000 and 2000 µs wide, repeated 50 times per
second. Width encoded the throttle command.

The problems with this for a fast PID loop:
1. **Noise susceptibility**: a voltage spike on the signal wire could be
   read as a different pulse width, causing a sudden unintended motor command.
2. **Resolution**: ~1000 discrete levels across the throttle range.
3. **Update rate**: 50 Hz meant 20 ms between commands — 160× slower than
   an 8 kHz PID loop. Each new throttle command was delayed by up to 20 ms.

Later protocols (Oneshot, Multishot) raised the update rate but kept the
analog format and its noise susceptibility. DShot solved both problems by
making the protocol fully digital.

### DShot packet structure

Each DShot packet is 16 bits:

    [11 bits throttle] [1 bit telemetry request] [4 bits CRC]

- **11-bit throttle**: 2048 discrete levels (0 = disarmed, 48–2047 = throttle
  range). More than double the resolution of analog PWM.
- **Telemetry request bit**: when set, requests extended telemetry from the
  ESC on the next packet (temperature, voltage, current).
- **4-bit CRC**: computed from the preceding 12 bits. If the receiver computes
  a different CRC, the packet is discarded. Noise-corrupted packets are never
  executed.

At DShot600 (600 kbit/s), transmitting 16 bits takes ~26.7 µs — comfortably
within the 125 µs window at 8 kHz loop rate.

### Bidirectional DShot

BiDi DShot adds an eRPM response to every packet exchange on the same wire.
After the FC finishes transmitting, it switches its UART to receive mode.
The ESC responds with a 21-bit eRPM packet in the gap before the next
command. The entire exchange fits within one PID loop cycle.

    FC transmits:  [DShot600 packet — 26.7 µs]
    Gap:           [signal line quiet — ~5 µs]
    ESC responds:  [eRPM packet — ~21 µs]
    Remaining:     [~72 µs idle — other tasks run here]

The eRPM value is what Betaflight's RPM filter uses to track motor vibration
frequencies in real time. Without BiDi DShot, the RPM filter cannot function.

    Mechanical RPM = eRPM ÷ pole_pairs

    For BrotherHobby 2507 (7 pole pairs):
    Mechanical RPM = eRPM ÷ 7

### DShot variant comparison

| Protocol | Speed | Type | CRC | BiDi |
|---|---|---|---|---|
| PWM | 50–490 Hz | Analog | No | No |
| Oneshot125 | 1× loop rate | Analog | No | No |
| DShot150 | 150 kbit/s | Digital | Yes | No |
| DShot300 | 300 kbit/s | Digital | Yes | Optional |
| DShot600 | 600 kbit/s | Digital | Yes | Yes (libdrone) |

DShot600 is the recommended choice for H7-class flight controllers. On
noisier electrical environments or longer wire runs, DShot300 provides more
margin against signal corruption.

---

## Reference

### libdrone DShot configuration

| Parameter | Value |
|---|---|
| Protocol | DShot600 |
| Bidirectional DShot | Enabled |
| Motor pole count | 14 (7 pole pairs) — set in Betaflight for RPM filter |
| ESC firmware | AM32 with BiDi support |
| FC | Matek H7A3-SLIM (H7 class — required for 8 kHz + RPM filter) |

### Verifying BiDi DShot is working

In Betaflight Motors tab, with props removed:
1. Advance master throttle slider to ~20%.
2. All four motors should display non-zero eRPM values.
3. eRPM values should increase proportionally as slider advances.
4. If any motor shows 0 eRPM: check AM32 Configurator that BiDi DShot
   is enabled on that motor output; check DShot signal wire continuity.

### DShot commands (special functions)

Beyond throttle, DShot encodes special commands in the 0–47 throttle range:

| Command value | Function |
|---|---|
| 0 | Disarmed / motor off |
| 1–5 | Beeper (tone selection) |
| 7 / 8 | Set spin direction (1 / 2) |
| 9 / 10 | 3D mode off / on |
| 12 | Save settings |
| 20 / 21 | Spin direction normal / reversed |

These are sent by the FC during ESC configuration, not during normal flight.
They require the motor to be at idle (throttle = 0) and the FC to send the
command multiple times for confirmation.

---

## Procedure

### Enabling DShot600 and BiDi DShot in Betaflight

1. In Betaflight Configurator → Configuration tab:
   - Motor Protocol: **DShot600**
   - Enable Bidirectional DSHOT: **checked**
2. In ESC Configurator (AM32 Configurator or BLHeli Suite):
   - For each motor output: enable **Bidirectional DSHOT**
3. Save and reboot both FC and ESC (power cycle).
4. Verify: in Betaflight Motors tab, all four motors report eRPM when spun up.
5. In Betaflight Filtering tab: confirm RPM filter shows as active.

---

## Rationale

### Why BiDi DShot is specified rather than optional

BiDi DShot is the prerequisite for the RPM filter, which is the prerequisite
for effective PID tuning. Without BiDi DShot, the RPM filter falls back to
static notch filters which do not track motor frequency with throttle.
The result: significantly more gyro noise reaching the D term, requiring
lower D gain, resulting in more prop wash and poorer disturbance rejection.
BiDi DShot is not a nice-to-have on libdrone — it is a hard dependency of
the tuning baseline.

---

## Connections

requires:
  - [[electronic-speed-controllers]]
related:
  - [[brushless-motors]]
  - [[rpm-filter]]
  - [[sk-complete-build-guide]]
leads_to:
  - [[rpm-filter]]


[electronic-speed-controllers]: electronic-speed-controllers.md "Electronic speed controllers"
[brushless-motors]: brushless-motors.md "Brushless motors"
[rpm-filter]: rpm-filter.md "RPM filter"
[sk-complete-build-guide]: ../skeletons/sk-complete-build-guide.md "Complete Build Guide"
