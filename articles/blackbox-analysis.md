---
id: blackbox-analysis
title: "Blackbox analysis"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - piloting-operations
personas:
  - 2.operator
  - 1.builder
  - 8.architect
platform:
  - core
  - pro
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

Betaflight's blackbox logs gyroscope data, motor outputs, PID terms, and RC
inputs at the full loop rate during every flight. After a flight, this data
is downloaded and analysed in Betaflight Blackbox Explorer or PIDtoolbox to
verify PID tuning, diagnose vibration issues, and identify structural or
electrical problems. The maiden flight blackbox trace is the ground truth for
whether the build is correctly tuned and mechanically sound. Analysing
blackbox data is a skill, not a black art — a few specific patterns in the
gyro spectrum and motor output traces answer most diagnostic questions.

---

## Concept

### What blackbox records

At 8 kHz loop rate with `blackbox_rate_denom = 2`, blackbox logs at 4 kHz —
one record every 250 µs. Each record contains:

- Raw and filtered gyro (roll, pitch, yaw) in degrees/second
- Motor outputs (0–2047 for DShot)
- PID P, I, D terms for each axis
- RC stick inputs
- Battery voltage and current (from ADC)
- Motor eRPM (if BiDi DShot is active)

This is the full picture of what the flight controller saw and did during
the flight. No other diagnostic tool provides this level of detail.

### Reading the gyro spectrum

In Blackbox Explorer, the spectral analyser view shows the frequency content
of the gyro signal. A clean build shows:

- Flat noise floor below approximately −40 dB in the 0–200 Hz range
- No narrow peaks at motor RPM harmonics (these should be removed by the RPM filter)
- Possible broad elevation in the 100–300 Hz range (frame resonance — acceptable
  if below −30 dB)
- Sharp roll-off above 400–600 Hz

A problematic build shows:
- Narrow spikes at motor RPM harmonics → RPM filter not active or BiDi DShot not working
- Broad elevated noise floor → vibration reaching gyroscope, check motor mounts
- Peaks at fixed frequencies regardless of throttle → frame resonance, not motor-related

### Reading the gyro time trace

The time-domain gyro trace shows how the drone responded to stick inputs and
disturbances. Key patterns:

- **P too high**: sustained rapid oscillation on the relevant axis after any input
- **D too low**: ringing for 3+ cycles after a sharp input, visible as decaying oscillation
- **D too high**: gyro trace has elevated high-frequency content visible at rest; motor
  traces show rapid oscillation; motors are warm after hover
- **I too low**: baseline gyro offset drifts slowly over 10–30 second segments
- **Prop wash**: oscillation on roll/pitch axes during descents or speed changes;
  short-duration burst, not sustained

### Reading motor output traces

Motor output traces reveal mixing and saturation events. Clean traces show:
- Smooth variation correlated with stick inputs
- No sustained high-frequency buzzing at idle (would indicate D too high)
- All four motors responding proportionally (one motor significantly different
  from others may indicate a loose motor mount or ESC issue)

---

## Reference

### Diagnostic guide

| Symptom | Blackbox pattern | Diagnosis | Action |
|---|---|---|---|
| High gyro noise floor | Elevated spectrum 50–500 Hz | Motor vibration reaching gyro | Check motor mount O-rings, balance props |
| Spikes at motor RPM harmonics | Narrow peaks tracking RPM | RPM filter not active | Enable BiDi DShot, check motor_poles setting |
| Post-input ringing | 3+ oscillation cycles in time trace | P too high or D too low | Reduce P 10% or raise D 5% |
| Motor buzz at idle | High-freq oscillation in motor traces | D too high | Reduce D 5% |
| Slow gyro drift | Baseline offset drifts 10–30 s scale | I too low | Raise I 10% |
| Prop wash oscillation | Burst oscillation during descent | D insufficient for prop wash | Raise D 5% if not already at max |
| One motor runs hotter | Single motor output elevated | Mechanical or electrical imbalance | Check motor mount, MR30 connection |

### Betaflight Blackbox Explorer quick reference

1. Download flash: Configurator → Blackbox tab → Download Flash
2. Open in Blackbox Explorer (web or desktop)
3. For spectral analysis: Analyser tab → select gyro filtered → set FFT window
4. For time trace: adjust Zoom and scroll to a representative segment
5. For motor traces: enable motor output channels in the trace selector
6. For PID terms: enable P/I/D trace per axis

---

## Procedure

### Post-maiden blackbox analysis sequence

1. Download blackbox immediately after maiden flight.
2. Open Analyser view. Check gyro spectrum:
   - Are motor harmonics visible? (Should not be if RPM filter is working)
   - What is the noise floor level between 0–200 Hz?
3. Open time trace. Find a segment with 2–3 sharp stick inputs on each axis.
   Count oscillation cycles after each input. Target: 1–2 cycles to settle.
4. Check motor output traces during the same inputs. Should be smooth, no
   high-frequency buzzing.
5. Note any anomalies. Cross-reference with the diagnostic table above.
6. Adjust one PID parameter at a time, refly, and compare the new trace
   to the baseline. Never change more than one parameter between analysis flights.

---

## Rationale

### Why blackbox analysis is mandatory, not optional

Subjective feel during flight is a poor diagnostic tool. A pilot cannot detect
oscillation below approximately 20% of the visible threshold. A build with
elevated motor noise in the gyro signal can feel smooth to fly while running
motors significantly hotter than necessary and showing degraded prop wash
handling that only appears under pressure. Blackbox analysis takes 15 minutes
after a maiden flight and answers these questions objectively. It is the
difference between a tuned build and a build that happened to fly without
immediately crashing.

---

## Connections

requires:
  - [[betaflight-setup]]
  - [[pid-tuning-rate-profile]]
  - [[rpm-filter]]
related:
  - [[pid-derivative-term]]
  - [[floating-motor-mounts]]
  - [[vibration-isolation-theory]]
leads_to:
  - [[scheduled-maintenance]]
