---
id: capacitor-placement-emc
title: "Capacitor placement for EMC"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - emc-signal-integrity
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

A decoupling capacitor absorbs voltage spikes before they propagate as noise.
Its effectiveness is determined by how fast it can respond to a spike — which
is limited by the inductance of every millimetre of wire between the capacitor
and the noise source. Every millimetre of wire or trace adds approximately 1 nH
of inductance. At a 50 A/µs current transient, each 1 nH adds 50 mV to the
unclamped spike. Capacitors must be soldered directly to the noise source pads
with no pigtail wire. A capacitor at the end of a 100 mm lead is nearly useless
for fast transients. Two complementary capacitor stages at different positions
address different frequency ranges: the 1000 µF electrolytic on the ESC pads
for slow large spikes, and 100 µF MLCC ceramics on the FC logic supply for
fast small spikes.

---

## Concept

### Why placement dominates performance

A capacitor is a charge reservoir. When a voltage spike occurs on the power bus,
the capacitor should supply or absorb charge to hold the voltage steady. But
before the capacitor can respond, the spike must travel from the noise source
to the capacitor along the connecting wire. That wire is an inductor — it resists
changes in current. The inductance of the wire limits how fast the capacitor can
respond.

The voltage spike that appears at the unprotected node before the capacitor can
respond:

    V_spike = L × dI/dt

For a 50 A/µs motor deceleration transient through 1 nH of inductance:

    V = 1×10⁻⁹ × 50×10⁶ = 50 mV per nH per A/µs

A 100 mm pigtail wire to the capacitor has approximately 100 nH of inductance.
The unclamped spike has ~5 V of unclamped energy before the capacitor responds.
This spike propagates into the ESC MOSFET drain-source junction. On 6S (25.2V
full charge), this spike can bring the MOSFET's Vds close to or beyond the
breakdown voltage, causing failure.

Solder the capacitor directly onto the ESC pads with lead lengths under 5 mm:
100 nH → under 5 nH. V_spike reduced by 20×.

### Low-ESR requirement

Equivalent Series Resistance (ESR) is the parasitic resistance of the capacitor.
A capacitor with high ESR has a voltage drop across it proportional to the current
flowing through it — for a fast, high-current transient, a high-ESR capacitor
has a proportionally high drop, reducing its effective clamping. At 100 kHz,
a generic electrolytic capacitor may have ESR of 1–5 Ω. A low-ESR type
(Panasonic FM or low-Z series) has ESR <0.1 Ω at 100 kHz — 10–50× better
for fast transients.

For the 1000 µF electrolytic on the ESC pads, low-ESR is mandatory, not
recommended. A generic capacitor will appear to work but will fail to clamp
fast spikes that a low-ESR type would suppress.

### Two-stage filtering

A single capacitor cannot cover the full frequency range of noise:
- **1000 µF electrolytic (low-ESR)** on ESC pads: handles large, moderate-speed
  spikes from motor deceleration (µs timescales). Its ESL (equivalent series
  inductance, typically 5–20 nH for a leaded electrolytic) limits effectiveness
  at very high frequencies.
- **100 µF MLCC ceramic** on FC 5V supply pads: handles fast, small spikes that
  propagate onto the logic supply (ns timescales). MLCC ceramics have very low
  ESL (<1 nH) and respond faster than any leaded component.

The two stages address different frequency bands and complement each other. The
electrolytic does not make the ceramic redundant (too slow for ns-scale spikes);
the ceramic does not make the electrolytic redundant (too small for µs-scale
large current transients).

---

## Reference

### Capacitor specification

| Capacitor | Location | Value | Type | ESR requirement |
|---|---|---|---|---|
| ESC bulk decoupling | ESC VBAT/GND pads | 1000 µF 35V | Low-ESR electrolytic | <0.1 Ω at 100 kHz |
| Logic supply decoupling | FC 5V pads | 100 µF | MLCC ceramic | Inherently low |

Recommended: Panasonic FM series (1000 µF 35V, 8×11.5 mm), or equivalent
low-Z type. Part number: EEU-FM1V102.

### Wire inductance reference

| Wire/lead length | Inductance (approx) | V_spike at 50 A/µs |
|---|---|---|
| 0 mm (direct on pad) | ~1–2 nH | 50–100 mV |
| 10 mm | ~10 nH | 500 mV |
| 50 mm | ~50 nH | 2.5 V |
| 100 mm (typical pigtail) | ~100 nH | 5 V |

On 6S with 25.2V full charge and MOSFETs rated to 30V Vds, a 5V unclamped
spike leaves only 0V margin — the MOSFET is at its limit.

---

## Procedure

### Installing the 1000 µF capacitor

1. Verify the capacitor polarity (positive lead = longer lead on electrolytic).
2. Trim leads to ~5 mm — the minimum needed to reach the ESC VBAT and GND pads.
3. Position the capacitor so its body lies flat across the ESC PCB.
4. Solder directly to the VBAT and GND pads. The joint between lead and pad
   should have no visible gap — the capacitor must be mechanically seated on
   the pad.
5. Verify: no lead length between capacitor body and pad exceeds 5 mm from
   the solder joint.
6. Secure the capacitor body with a drop of hot glue or a cable tie to prevent
   vibration fatigue on the solder joints over hundreds of flight hours.

---

## Rationale

### Why "no pigtail" is a hard rule

A pigtail — even a short 20 mm wire — adds enough inductance to allow a
significant portion of the motor deceleration spike to appear on the MOSFET
drain before the capacitor can respond. ESCs fail silently at first (reduced
maximum safe current) and then catastrophically (MOSFET avalanche). The cost
of an ESC failure is €30–50 and days of repair time. The cost of soldering
the capacitor correctly the first time is zero.

---

## Connections

requires:
  - [[emc-noise-sources]]
  - [[star-grounding]]
related:
  - [[electronic-speed-controllers]]
  - [[power-rail-architecture]]
leads_to:
  - [[power-signal-separation]]
  - [[ferrite-beads]]


[emc-noise-sources]: emc-noise-sources.md "EMC noise sources in a drone"
[star-grounding]: star-grounding.md "Star grounding"
[electronic-speed-controllers]: electronic-speed-controllers.md "Electronic speed controllers"
[power-rail-architecture]: power-rail-architecture.md "Power rail architecture"
[power-signal-separation]: power-signal-separation.md "Power and signal separation"
[ferrite-beads]: ferrite-beads.md "Ferrite beads"
