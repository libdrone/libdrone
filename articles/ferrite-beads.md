---
id: ferrite-beads
title: "Ferrite beads"
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

A ferrite bead is a frequency-selective resistor. At DC and low frequencies
it presents near-zero impedance — power passes through normally. At high
frequencies it presents high impedance — noise is attenuated. Unlike a
capacitor, it does not resonate and does not affect DC efficiency. On libdrone,
three to four clip-on ferrite clamps stacked on the VTX power wire at the
XL4015 buck converter output attenuate the 180 kHz switching frequency and its
harmonics before they can propagate along the wire and radiate or couple into
the GPS or receiver.

---

## Concept

### How a ferrite bead works

Ferrite is a magnetic ceramic material — iron oxide combined with other metal
oxides. When a wire passes through a ferrite core, the ferrite increases the
inductance of that wire by a factor determined by the ferrite's permeability.
For DC and low frequencies (where the ferrite's core loss is low), the added
inductance is small and the impedance is minimal — power passes through with
negligible loss.

At high frequencies, the ferrite's core loss increases dramatically. The
bead now acts like a resistor in series with the wire at those frequencies —
it absorbs the high-frequency energy and converts it to heat. The heat is
negligible (milliwatts for typical drone applications). The attenuation is
substantial — a single ferrite bead can provide 20–40 dB of attenuation at
its target frequency.

Unlike an LC filter (inductor + capacitor), the ferrite bead does not
resonate. An LC filter has a resonance peak where it actually amplifies
the signal before cutting off above resonance. A ferrite bead is purely
resistive at high frequencies — no resonance, no amplification, just
monotonically increasing attenuation above its corner frequency.

### Why clip-on and why stack 3–4

Solid ferrite cores (where the wire passes through a pre-formed toroid)
provide the highest impedance per unit length. Clip-on ferrite clamps
(clamshell type) have a small air gap at the clip joint, which slightly
reduces permeability compared to a solid core.

Stacking 3–4 clip-on beads compensates for this reduced permeability: the
total impedance scales approximately linearly with the number of beads.
Three to four clip-on beads achieve impedance comparable to one or two
solid toroids at the target frequency.

Clip-on beads are preferred for drone use because:
- They can be added after wiring is complete — no rethreading required
- They are repositionable if the first placement is not optimal
- They grip the wire by friction — less susceptible to vibration loosening
  than a wire threaded through a toroid and held only by the wire tension

### Application: VTX power wire

The XL4015 buck converter switches at 180 kHz, generating:
- 180 kHz fundamental
- 360 kHz second harmonic
- 540 kHz third harmonic
- ... continuing up into the MHz range

These frequencies propagate along the VTX power wire by conduction, then
radiate from the wire as an antenna. Ferrite beads placed on the wire near
the converter output intercept this conducted noise before it travels further.

The correct placement is at the converter output — as close to the source
as possible. Placing the beads near the VTX end of the wire allows the noise
to propagate and radiate along the unprotected portion of the wire between
converter and beads.

---

## Reference

### Ferrite bead specification

| Parameter | Specification |
|---|---|
| Type | Clip-on split ferrite clamp (clamshell) |
| Size | 3.5 mm bore (fits standard 20–24 AWG wire) |
| Material | Ni-Zn ferrite (effective at 100 kHz–1 MHz range) |
| Quantity | 3–4 stacked on VTX power wire |
| Placement | At XL4015 output, within 30 mm of converter |

Recommended: TDK ZCAT-series or equivalent Ni-Zn clamshell type. Avoid
Mn-Zn ferrite (effective at lower frequencies, < 1 MHz is different material).

### Where ferrite beads are applied on libdrone

| Location | Purpose |
|---|---|
| VTX power wire (at XL4015 output) | Attenuate 180 kHz buck converter switching noise |

Additional applications if noise problems are observed:
- FC 5V supply wire from ESC BEC (attenuates any residual 48 kHz ESC noise)
- GPS supply wire (protects GPS receiver from conducted supply noise)

---

## Procedure

### Installing clip-on ferrite beads

1. Cut the VTX power wire to final length before adding beads — beads are
   added at a fixed point and cannot be slid along a wire once connectors are
   on.
2. Open the clamp. Place the wire in the groove. Snap the clamp shut firmly
   until it clicks. The wire should be centred in the bore.
3. Add the next bead immediately adjacent to the first. Stack 3–4 total.
4. Verify the stack is as close to the XL4015 output as possible — within
   30 mm of the converter output pads.
5. Optionally secure the stack with a cable tie or a small piece of heatshrink
   over the stack to prevent the beads from sliding along the wire in flight.

### Verifying effectiveness

After a maiden flight, review the Blackbox gyroscope spectrum. If the GPS is
reporting correct positions and the receiver link is stable, the ferrite beads
are doing their job. If compass heading drifts or shows noise correlated with
VTX power state (VTX on vs VTX off), add another bead or check placement.

---

## Rationale

### Why ferrite beads rather than an LC filter

An LC low-pass filter (inductor + capacitor) provides steeper roll-off and
lower ripple, but has a resonance frequency where it amplifies rather than
attenuates. If any conducted noise hits near the LC filter's resonance
frequency, the filter makes things worse. For drone EMC where the noise
frequencies are fixed (180 kHz from XL4015) and the filter is placed by a
builder rather than a PCB designer with access to simulation tools, the
ferrite bead's resonance-free behaviour is preferable. The bead always
attenuates at the target frequency — never amplifies.

---

## Connections

requires:
  - [[emc-noise-sources]]
related:
  - [[capacitor-placement-emc]]
  - [[power-signal-separation]]
  - [[voltage-regulation]]
leads_to:
  - [[gps-antenna-placement]]
  - [[conformal-coating]]
