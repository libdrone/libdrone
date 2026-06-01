---
id: pid-tuning-rate-profile
title: "PID tuning and rate profile"
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
  - 8.architect
platform:
  - core
  - pro
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

PID tuning on libdrone starts from documented baseline values, is adjusted
using Blackbox evidence, and follows a fixed sequence: P first, then D, then
I, then feed-forward. The V2.4.6 geometry change (lower CG) requires D-term
reduction of 10–15% from the V2.14 baseline at maiden. Rate profiles set
stick sensitivity independently of PID gains — one profile per prop set.
Tuning should happen in calm conditions on a fully charged battery with the
intended payload fitted. A blackbox trace from the maiden flight is the
ground truth — do not tune by feel alone.

---

## Concept

### Why the baseline values are a starting point, not a final answer

The documented PID values are derived from a reference build using the
specified components in average conditions. Real builds vary: motor-to-motor
variation, prop balance quality, arm tab engagement depth, bearing condition,
and even filament batch affect the frame's dynamic behaviour. The baseline
gets the drone in the air safely; Blackbox analysis gets it tuned correctly.

Tuning by feel without Blackbox evidence is unreliable. The human perception
threshold for oscillation is ~20% above where Blackbox can detect it. A drone
that feels smooth may have significant noise in the gyro signal that will cause
motor heating and prop wash on aggressive inputs.

### V2.4.6 CG effect on D-term

The V2.4.6 platform moved the battery from an elevated tray to a flat
side-slide rail, lowering the CG by 8–12 mm. This shortens the pendulum arm,
raises the natural oscillation frequency, and makes the D-term more sensitive
to any given gain value. The practical consequence:

- Start D-term at 10–15% below the V2.14 or published baseline
- If Blackbox shows prop wash handling is poor, raise D in 5% steps
- If motor temperature is elevated after hover, lower D in 5% steps

The P and I baselines are not significantly affected by the CG change.

### Rate profile and prop set

The two prop sets (HQ 6×3×3 and HQ 6×2.5×3) have different pitch
characteristics. Higher pitch translates faster, responds differently to
roll/pitch inputs. Rate Profile 1 is tuned for the 6×3×3; Rate Profile 2
for the 6×2.5×3. Always switch rate profiles when switching prop sets.
Running the wrong rate profile makes the drone feel either sluggish or
twitchy relative to its actual potential.

---

## Reference

### Maiden flight PID sequence

| Step | Action | Evidence to look for |
|---|---|---|
| 1 | Set D to baseline − 15% | No motor buzz, motors not hot |
| 2 | Maiden flight — hover and gentle inputs | Blackbox: clean settle, no sustained oscillation |
| 3 | Review Blackbox P behaviour | Gyro trace: snappy correction, 1–2 cycles to settle |
| 4 | Review Blackbox D behaviour | Gyro trace: no ringing after stick inputs |
| 5 | Adjust P ±10% if needed | Repeat until clean |
| 6 | Adjust D ±5% if needed | Repeat until clean |
| 7 | Tune I last | Hover 30s — drift indicates low I |
| 8 | Set FF conservatively (libdrone mapping default) | Smooth GPS-mode response |

### Blackbox indicators and adjustments

| Observation | Diagnosis | Action |
|---|---|---|
| Slow oscillation in gyro trace | P too high | Reduce P 10% |
| Drone drifts in hover | I too low | Increase I 10% |
| Ringing after stick inputs | D too low | Increase D 5% |
| Motor buzz / motor heat | D too high | Reduce D 5% |
| Noise peaks at motor RPM harmonics | RPM filter not active | Check BiDi DShot |
| Broad noise floor elevated | Vibration reaching gyro | Check motor mounts |

### V2.4.6 PID starting values (from base diff)

    Profile 1 (standard):
    P_roll=47  I_roll=85  D_roll=32  F_roll=105
    P_pitch=50 I_pitch=85 D_pitch=36 F_pitch=105
    P_yaw=42   I_yaw=85   D_yaw=0    F_yaw=100

For V2.4.6 maiden: start with D_roll=28, D_pitch=31 (15% below baseline).

### Winter voltage adjustment

When flying below 5°C, apply the winter voltage diff to prevent premature
low-battery warnings caused by cold-induced voltage sag:

    set vbat_min_cell_voltage = 36
    set vbat_warning_cell_voltage = 37

This raises the warning threshold — the pack is considered lower than it
appears on the OSD due to cold-induced internal resistance increase.

---

## Procedure

### Post-maiden Blackbox review

1. After maiden flight, download Blackbox from the FC onboard flash
   via Betaflight Configurator → Blackbox tab.
2. Open in Betaflight Blackbox Explorer.
3. View the gyro (filtered) spectrum: motor harmonics should be largely absent
   (RPM filter working). Residual peaks > −50 dB indicate filter gaps.
4. View the gyro trace during a sharp stick input: count oscillation cycles
   before the signal settles. 1–2 cycles = correctly tuned P. 3+ cycles = P
   too high or D too low.
5. View motor output traces during the same inputs: if any motor trace shows
   large rapid fluctuations not corresponding to stick inputs, vibration is
   reaching the D-term — check motor mount condition.

---

## Rationale

### Why F (feed-forward) is set conservatively

libdrone's primary mission is GPS-assisted mapping where stick inputs are slow
or absent. Feed-forward benefits rapid manual stick inputs — exactly what
mapping missions do not produce. Conservative FF avoids amplifying any noise
on the RC signal during long GPS-hold segments where sticks are stationary.
Raise FF only if the operational profile shifts toward active manual flying.

---

## Connections

requires:
  - [[betaflight-setup]]
  - [[pid-derivative-term]]
  - [[rpm-filter]]
related:
  - [[betaflight-profiles]]
  - [[blackbox-analysis]]
  - [[pendulum-stability]]
  - [[lipo-batteries]]
leads_to:
  - [[blackbox-analysis]]


[betaflight-setup]: betaflight-setup.md "Betaflight setup"
[pid-derivative-term]: pid-derivative-term.md "PID — derivative term"
[rpm-filter]: rpm-filter.md "RPM filter"
[betaflight-profiles]: betaflight-profiles.md "Betaflight profiles and modes"
[blackbox-analysis]: blackbox-analysis.md "Blackbox analysis"
[pendulum-stability]: pendulum-stability.md "Pendulum stability"
[lipo-batteries]: lipo-batteries.md "LiPo batteries"
