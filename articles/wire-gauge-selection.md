---
id: wire-gauge-selection
title: "Wire gauge selection"
version: 1.0.0
date: 2026-04-15
author: jsa
status: released
scope: libdrone
topic:
  - power-systems
personas:
  - 1.builder
  - 5.student
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Wire gauge determines how much current a wire can carry safely and how much
voltage it drops doing so. Every wire in a drone build is a trade between
mass and resistance: thicker wire carries more current with less heat and
less voltage drop, but adds weight. Under-gauged wire overheats and drops
voltage to sensors and motors; over-gauged wire wastes mass. The AWG standard
numbers counterintuitively — lower number means thicker wire. The libdrone
wiring specification defines six gauges covering every connection from the
battery backbone to the payload signal lines.

---

## Concept

### The physics: resistance, heat, and voltage drop

Every wire has resistance proportional to its length and inversely proportional
to its cross-sectional area. When current flows through this resistance, two
things happen simultaneously:

**Heat** is generated at rate P = I² × R. A wire carrying 30 A through
8.3 mΩ/m of resistance generates 30² × 0.0083 = 7.5 W/m of heat. A 30 cm
battery lead produces 2.25 W of heat — enough to melt insulation if the wire
is undersized.

**Voltage drops** across the wire at V = I × R. The same 30 A through 8.3 mΩ/m
over 0.3 m drops 30 × 0.0025 = 0.075 V. On a 6S (25.2 V) battery, that is
a 0.3% drop — acceptable. But on a 5V BEC rail feeding the flight controller,
a 0.15 V drop from undersized wire brings 5V down to 4.85 V — enough to cause
FC resets at high current draw.

The ESC power feed and the signal feed must be treated separately. The
main battery lead carries tens of amps and can tolerate small fractional
voltage drops. The BEC-fed signal rail carries milliamps but operates at 5V
where fractions of a volt matter for logic stability.

### AWG numbering convention

AWG (American Wire Gauge) is the universal drone wiring standard. The
numbering is counterintuitive: each step up in AWG number reduces the
wire diameter by approximately 10.9%, and the cross-sectional area by
approximately 20.7%. A 12 AWG wire has roughly four times the cross-section
of a 20 AWG wire.

Higher gauge numbers are thinner, higher resistance, lower current capacity.
Lower gauge numbers are thicker, lower resistance, higher current capacity.

---

## Reference

### libdrone wire gauge table

| AWG | Diameter (mm) | Resistance (mΩ/m) | Continuous current | Colour | libdrone use case |
|---|---|---|---|---|---|
| 12 | 2.05 | 5.2 | 40 A | Red / Black | Battery leads to ESC pads (XT60) |
| 14 | 1.63 | 8.3 | 30 A | Red / Black | ESC–PDB links, XT60 pigtails |
| 20 | 0.81 | 33 | 10 A | Red / Black | VTX power from buck converter; fan |
| 22 | 0.64 | 53 | 5 A | Red / Black | 5V BEC rails, sense wires |
| 24 | 0.51 | 84 | 2.5 A | Blue / Green | DShot signal wires, short UART runs |
| 28 | 0.32 | 213 | 0.8 A | Blue / Green | All signal wires: GPS, I2C, GX12 payload |

### Colour code discipline

Consistent colour coding prevents miswiring during maintenance:
- **Red**: all positive power lines (any voltage)
- **Black**: all negative / ground lines (any voltage)
- **Blue / Green**: signal and data lines

Do not use red or black for signal wires. Do not use blue or green for
power wires. The colour code must survive removing and reinstalling wires
under field conditions without requiring a wiring diagram.

### Worked example — battery lead voltage drop

Battery: 6S 25.2V fully charged. ESC draw at full throttle: 60 A.
Battery lead: 12 AWG, 150 mm each side = 300 mm total.
Resistance: 0.30 m × 5.2 mΩ/m = 1.56 mΩ
Voltage drop: 60 A × 0.00156 Ω = 0.094 V (0.37% of 25.2 V) — acceptable.

Same calculation with 20 AWG (wrong choice):
Resistance: 0.30 m × 33 mΩ/m = 9.9 mΩ
Voltage drop: 60 A × 0.0099 Ω = 0.594 V — and the wire would overheat
catastrophically (60² × 0.0099 = 35.6 W/m).

---

## Procedure

### Select the correct gauge for any connection

1. Identify the maximum continuous current for the connection.
2. Find the first gauge in the table whose continuous current rating exceeds
   the required current by ≥ 20% margin (for thermal headroom).
3. Calculate the voltage drop over the actual wire run length:
   V_drop = I × (resistance_per_metre × length_metres).
4. Confirm the voltage drop is acceptable for the circuit:
   - Power circuits (motor, ESC): < 1% of supply voltage
   - BEC rail (5V FC/sensor supply): < 50 mV
   - Signal lines (UART, I2C, DShot): < 0.1 V
5. If voltage drop is too high, step down one AWG number (thicker wire).

### Wiring audit before first flight

Walk all wires and confirm:
- Battery leads: 12 AWG, no joins, correct colour
- Motor phase wires: same gauge as ESC (typically 16–18 AWG on 6S systems)
- BEC 5V rail: 22 AWG maximum run length 200 mm
- All signal wires: 24–28 AWG, separated ≥ 20 mm from motor phase wires
- No wire crosses an arm without strain relief at the channel exit

See → [[power-signal-separation]] for the three-zone routing discipline
that determines where each gauge runs.

---

## Rationale

Wire gauge selection was not atomised in the 2.x documentation stack, leaving
it as implicit knowledge in the DMOM and Wiring document. The `sk-wiring-reference`
skeleton explicitly flagged this as a future atom. The consequence of the gap was
that builders either copied the gauge decisions without understanding them, or made
incorrect gauge substitutions when specified parts were unavailable. The worked
example for voltage drop is specifically designed to make the failure mode of
under-gauged wire visible before the build rather than after the first full
throttle run.

---

## Connections

requires:
  - [[power-rail-architecture]]
  - [[electronics-installation]]
related:
  - [[power-signal-separation]]
  - [[star-grounding]]
  - [[twisted-pairs]]
  - [[capacitor-placement-emc]]
  - [[emc-noise-sources]]
  - [[voltage-regulation]]
leads_to:
  - [[power-signal-separation]]
  - [[electronics-installation]]
