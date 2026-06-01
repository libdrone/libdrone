---
id: voltage-regulation
title: "Voltage regulation"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - power-systems
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

A 6S LiPo varies from 25.2V (full) to 21.0V (minimum), and voltage fluctuates
by 3–5V during aggressive flight as motor currents change. Every sensitive
electronic component needs stable, clean voltage to function correctly. Two
regulation approaches are used on libdrone: the BEC (Battery Eliminator
Circuit) inside the flight controller provides regulated 5V for logic
electronics using a linear topology; the XL4015 switching buck converter
provides 9–12V for the video transmitter at much higher efficiency. Each
has specific noise characteristics that must be managed.

---

## Concept

### Linear regulation (BEC/LDO)

A linear regulator passes current through a series transistor that drops the
excess voltage as heat. Input 22V, output 5V: the transistor drops 17V.
At 0.5A load, the heat dissipated is 17V × 0.5A = 8.5W — substantial.

The internal BEC in the H7A3-SLIM uses a linear architecture. Linear regulators
have one major advantage: their output is inherently quiet. There is no switching,
no oscillation, no harmonics. The output noise is low and broadband — easily
filtered by small capacitors at the point of use. For sensitive digital logic
(gyroscope, receiver, GPS) this clean supply is essential.

The H7A3-SLIM BEC is rated 5V / 1A continuous, 2A peak. The total load
budget:

    FC logic:        ~200 mA
    ELRS receiver:   ~150 mA
    GPS module:      ~100 mA
    Buzzer:          ~30 mA (intermittent)
    Fan:             ~70 mA (always-on)
    GX12 payload:    ~200 mA (typical SEN66 mast)
    ─────────────────────────────
    Total typical:   ~750 mA (within 1A continuous rating)
    Peak:            ~900 mA (within 2A peak rating)

### Switching regulation (buck converter)

A buck converter (step-down switching regulator) rapidly switches a MOSFET
on and off, storing energy in an inductor during the on phase and releasing
it during the off phase. The output capacitor smooths the result. Output
voltage is controlled by the duty cycle.

The XL4015 switching at 180 kHz achieves ~90% efficiency from 22V to 12V
at 400 mA — dissipating ~0.5W versus ~4W for an equivalent LDO. This
makes the switcher practical for the VTX supply where an LDO would need
a heatsink and reduce system endurance.

The switching creates electromagnetic interference at 180 kHz and its
harmonics. These harmonics propagate along the output wire and radiate
from it as an antenna. Three to four clip-on ferrite beads (mix 31 or
mix 43 material) on the output wire immediately at the converter output
add approximately 250–500 Ω of impedance at 180 kHz, reducing harmonic
propagation by 20–30 dB. Without ferrites, the 180 kHz switching noise
can couple onto the GPS antenna feed line and degrade satellite reception.

### Decoupling capacitors

Every integrated circuit has a power supply rejection ratio (PSRR) — the
ability to reject noise on its supply voltage. For digital ICs, PSRR falls
rapidly with frequency: good at DC, poor at MHz. A 100 nF ceramic capacitor
directly on the IC's supply pin provides a local energy reservoir that supplies
transient current demand locally (preventing voltage droops that propagate back
to the supply) and bypasses high-frequency noise to ground before it enters
the IC.

The placement rule is absolute: the bypass capacitor must be on the same PCB
as the IC, as close to the supply pin as possible. A capacitor 10 mm away on
a different board, connected by a wire, provides almost no high-frequency
bypassing — the wire inductance dominates above a few MHz.

This is why the ESC's 1000 µF capacitor must be soldered directly to the ESC
power pads. → See [[electronic-speed-controllers]].

---

## Reference

### Regulation comparison

| Method | Topology | Efficiency | Output noise | Use on libdrone |
|---|---|---|---|---|
| BEC (internal) | Linear | Low (~23% at 22V→5V, 0.5A) | Very low | FC, receiver, GPS, fan |
| XL4015 | Switching (buck) | High (~90%) | 180 kHz harmonics | VTX only |
| Direct battery | None | 100% | Motor switching noise | ESC/motors only |

### XL4015 operating parameters

| Parameter | Value |
|---|---|
| Input voltage range | 8–36V |
| Output voltage | 9–12V (adjustable, set to 12V on libdrone) |
| Maximum output current | 5A |
| Switching frequency | ~180 kHz |
| Efficiency at 22V→12V, 0.4A | ~90% |
| Heat dissipated at this point | ~0.5W |
| EMC mitigation | 3–4 ferrite beads on output wire |

### BEC load limits and consequences of overload

If the total BEC load exceeds 1A continuous (or 2A peak), the H7A3-SLIM's
internal BEC thermal protection activates — the 5V rail folds back to protect
the IC. The immediate effect: the ELRS receiver drops connection (RC link
lost), GPS stops, FC may reset. This is effectively a failsafe trigger.
Heavy payloads requiring more than 200 mA from the GX12 5V rail should use
a dedicated payload power converter from battery voltage rather than loading
the BEC.

---

## Procedure

### Verifying power rail voltages

1. Before first flight: connect battery, allow full power-up sequence.
2. In Betaflight: verify battery voltage shown in OSD matches physical
   cell meter reading (within 0.1V).
3. Check 5V BEC: Betaflight Configurator → Power tab shows BEC output
   voltage if the FC has a 5V ADC channel. Alternatively, measure with
   multimeter at a known 5V pad (receiver power, GPS power).
4. Check VTX supply: VTX menu typically shows input voltage. Should read
   9–12V stable during flight. If VTX shows lower voltage during full
   throttle, check XL4015 output capacitors.

---

## Rationale

### Why the VTX has its own converter rather than sharing the BEC

The HDZero Freestyle V2 VTX draws up to 600 mA at 800 mW output power.
Adding 600 mA to the BEC load would bring total BEC consumption close to
the 1A continuous limit. This leaves no margin for payload sensors, BEC
thermal derating on hot days, or transient demand spikes. Isolating the VTX
on its own dedicated converter also prevents VTX RF switching noise from
coupling into the BEC output and reaching the receiver or GPS.

### Why the VTX supply is set to 12V and not 9V

The HDZero VTX accepts 7–25V. At lower supply voltage, the VTX's internal
power amplifier runs at lower efficiency for the same RF output power —
dissipating more heat. At 12V, the internal amplifier operates in its optimal
efficiency region for the 200–800 mW range used in typical field deployment.
The efficiency difference is small (~5%) but relevant for thermal management
during extended mapping missions.

---

## Connections

requires:
  - [[lipo-batteries]]
  - [[power-rail-architecture]]
related:
  - [[electronic-speed-controllers]]
  - [[emc-signal-integrity]]
leads_to:
  - [[power-sequencing]]


[electronic-speed-controllers]: electronic-speed-controllers.md "Electronic speed controllers"
[lipo-batteries]: lipo-batteries.md "LiPo batteries"
[power-rail-architecture]: power-rail-architecture.md "Power rail architecture"
[emc-signal-integrity]: emc-signal-integrity.md "EMC and signal integrity"
[power-sequencing]: power-sequencing.md "Power sequencing"
