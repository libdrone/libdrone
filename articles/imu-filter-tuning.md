---
id: imu-filter-tuning
title: "IMU filter tuning"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - sensors-fc
personas:
  - 1.builder
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

IMU filter tuning configures the software filter chain between the raw gyro
output and the PID calculations. The goal is to remove motor vibration noise
while introducing as little phase lag as possible — every filter adds lag
that makes the control loop slower. With RPM filtering active, the approach
is to set RPM filter harmonics to 3, run the dynamic notch filter, and use
conservative static lowpass filter cutoffs. The result should be a gyro
spectrum with clean fundamental signal below 100 Hz and suppressed motor
peaks above. Betaflight Blackbox and the frequency analysis tool are the
ground truth — filter tuning without Blackbox analysis is guesswork.

---

## Concept

### Phase lag and why it limits filter aggression

Every filter adds phase lag: a delay between when a real motion occurs and
when the filtered signal reflects it. A first-order lowpass (PT1) filter at
cutoff frequency fc introduces approximately:

      phase_lag_degrees ≈ arctan(f / fc)
      At f = 20 Hz (fast roll manoeuvre) with fc = 100 Hz:
      phase_lag ≈ arctan(20/100) ≈ 11°

11° of phase lag means the PID controller is responding to attitude data that
is slightly stale. At 8 kHz loop rate with a high-frequency manoeuvre, this
lag directly limits how high P gain can be set before oscillation.

The RPM filter's narrow notch filters introduce almost no phase lag — they
remove a few Hz of bandwidth at specific frequencies without affecting the
phase response at real signal frequencies. This is why RPM filtering is
superior to broadband lowpass for noise rejection: same noise removal,
far less phase cost.

### Blackbox frequency analysis workflow

1. Fly a 30-second hover with Blackbox enabled. Include some brisk stick inputs
   to excite all frequencies.
2. Open the log in Betaflight Blackbox Explorer. Enable frequency spectrum view.
3. The spectrum shows which frequencies contain the most energy in the gyro signal.
4. A well-filtered build shows: flat or falling energy from 0–100 Hz (real signal),
   a steep drop at 100–200 Hz, and very low energy above that.
5. Remaining peaks above 100 Hz indicate:
   - **Sharp peaks at motor multiples**: RPM filter not tracking — check BiDi DShot
   - **Broad hump 100–300 Hz**: frame resonance — not addressed by RPM filter
   - **Rising floor above 1 kHz**: ESC switching noise or PCB coupling

### Static lowpass filter interaction with RPM filter

With RPM filtering active, the static gyro lowpass cutoff can be raised compared
to a build without RPM filtering. The RPM filter handles motor-frequency noise;
the static lowpass handles the residual broadband floor. Starting values with
RPM filter active:

Gyro lowpass 1:  PT1, 250–300 Hz cutoff
Gyro lowpass 2:  PT1, off (or 500 Hz if needed)
D-term lowpass:  PT1, 100–120 Hz cutoff

Without RPM filter, these would need to be 80–100 Hz to achieve comparable
noise rejection — at 3× the phase cost.

---

## Reference

### Betaflight filter settings for libdrone V2.4.6

| Filter | Type | Cutoff | Notes |
|---|---|---|---|
| RPM filter | Notch (adaptive) | Per motor RPM | 3 harmonics, 4 motors, 3 axes = 36 positions |
| Dynamic notch | Notch (adaptive) | Detected peaks | Min 3 notches per axis |
| Gyro lowpass 1 | PT1 | 250 Hz | Start here; reduce if motor heat persists |
| Gyro lowpass 2 | PT1 | off | Enable at 500 Hz only if gyro LPF1 insufficient |
| D-term lowpass 1 | PT1 | 100 Hz | Most noise-sensitive setting |
| D-term lowpass 2 | PT1 | off | Enable only if severe noise after LPF1 |

### Interpreting the Blackbox spectrum

| Observation | Likely cause | Action |
|---|---|---|
| Sharp spikes at motor RPM multiples | RPM filter not suppressing — BiDi DShot issue | Verify BiDi DShot enabled and ESC firmware supports it |
| Broad peak 100–250 Hz | Frame structural resonance | Lower gyro LPF1; add damping to frame |
| Elevated noise floor everywhere | Prop imbalance or motor bearing damage | Balance props; inspect bearings |
| Clean spectrum but motors still hot | D-term LPF too high | Lower D-term LPF1 by 10–20 Hz |

---

## Procedure

### Filter tuning sequence

1. Ensure RPM filter is active and BiDi DShot is confirmed working (all 4
   motors report eRPM in Betaflight Motors tab).
2. Fly a hover with defaults. Download Blackbox log.
3. Analyse frequency spectrum in Blackbox Explorer. Identify any residual
   peaks above 100 Hz not removed by RPM filter.
4. If frame resonance peak exists (100–300 Hz broad hump): lower gyro LPF1
   by 20–30 Hz increments until the peak is suppressed.
5. After each change: re-fly, re-analyse. Do not change more than one filter
   parameter per flight.
6. Monitor motor temperature after each change. Hotter motors = more noise
   reaching D term via D-term LPF.
7. Final check: gyro spectrum flat below 100 Hz, suppressed above. Motor
   temperature stable at warm (not hot) after 3-minute hover.

---

## Rationale

### Why this article is in sensors-fc and not control-systems

The RPM filter concept and purpose are documented in [[rpm-filter]] (control-systems).
This article covers the hands-on tuning procedure and the interpretation of
Blackbox data — practical builder knowledge that belongs with the sensor
processing chain rather than with the control theory. A student understanding
control theory reads [[rpm-filter]]; a builder configuring a real drone reads this.

---

## Connections

requires:
  - [[imu-gyroscope]]
  - [[rpm-filter]]
related:
  - [[pid-derivative-term]]
  - [[blackbox-analysis]]
leads_to:
  - [[blackbox-analysis]]


[rpm-filter]: rpm-filter.md "RPM filter"
[imu-gyroscope]: imu-gyroscope.md "IMU and gyroscope"
[pid-derivative-term]: pid-derivative-term.md "PID — derivative term"
[blackbox-analysis]: blackbox-analysis.md "Blackbox analysis"
