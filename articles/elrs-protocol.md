---
id: elrs-protocol
title: "ExpressLRS protocol"
version: 1.0.1
date: 2026-05-30
author: jsa
status: released
scope: generic
topic:
  - communication-rf
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

ExpressLRS (ELRS) is an open-source long-range RC link protocol using chirp
spread spectrum (CSS) modulation on the SX1280 2.4 GHz transceiver. The
carrier frequency sweeps linearly across a bandwidth on every packet — the
receiver correlates the received signal against the expected chirp, achieving
processing gain that allows decoding at signal levels below the noise floor.
This gives ELRS exceptional range and interference rejection compared to
traditional frequency-hopping systems. libdrone uses ELRS at 250 Hz with LBT
(Listen Before Talk) regulatory mode for EU compliance. Total stick-to-FC
latency is approximately 6–8 ms.

---

## Concept

### Chirp spread spectrum

A conventional radio transmitter emits at a fixed frequency. A receiver tuned
to that frequency receives the signal; any interference at that frequency
degrades it. Frequency-hopping spread spectrum (FHSS — used by earlier RC
systems like FrSky) hops between frequencies on each packet, making it harder
to jam but still susceptible when channels overlap with other users.

Chirp spread spectrum (CSS) works differently. On each packet, the carrier
frequency sweeps continuously and linearly from a low frequency to a high
frequency (or vice versa) across a defined bandwidth — this sweep is the
"chirp." The receiver knows exactly what sweep rate and bandwidth to expect.
It correlates the received signal against a copy of the expected chirp. Even
if the received signal is weaker than the ambient noise floor, the correlation
process extracts it — the processing gain from the correlation is proportional
to the bandwidth-time product of the chirp.

The result: ELRS can decode signals that are literally quieter than the ambient
noise level. In an urban 2.4 GHz environment saturated with WiFi routers, the
ELRS link remains functional where a conventional narrow-band RC link would
have already failed.

### ELRS packet structure and update rate

libdrone uses 250 Hz packet rate: one RC packet every 4 ms. Each packet carries
up to 12 channels at 10-bit resolution (or 4 channels at full 12-bit resolution
in full-resolution mode). The total stick-to-FC latency chain:

    TX16S stick movement
      → EdgeTX samples gimbal (~1 ms)
      → ELRS module encodes and transmits (~1 ms)
      → SX1280 radio propagation (negligible at flying distances)
      → RP2 receiver decodes (~1 ms)
      → CRSF serial to FC (~1.5 ms)
      → FC reads CRSF and applies to PID setpoint (~0.125 ms)
    Total: ~6–8 ms

### LBT mode

Listen Before Talk (LBT) is a regulatory requirement in the EU for certain
frequency bands. Before each transmission, the ELRS module checks whether the
channel is occupied by another transmitter. If occupied, it waits and checks
again. This adds a small variable latency per packet (typically 0–1 ms) but
ensures compliance with EU regulatory requirements.

At 250 Hz with LBT, the practical link behaviour is indistinguishable from
non-LBT at all but the most congested RF environments. Packet loss rate in
typical EU outdoor environments is well below 1%.

### Open source and ecosystem

ELRS is licensed under GPL. The protocol specification is published. Any
manufacturer can produce ELRS-compatible hardware. The community maintains
the firmware and adds features through pull requests. This is the direct
lesson from the FrSky proprietary protocol failure: a protocol that no single
company controls cannot be abandoned by that company. → See
[[open-source-philosophy]].

---

## Reference

### ELRS configuration for libdrone

| Parameter | Value |
|---|---|
| Frequency band | 2.4 GHz |
| Modulation | LoRa CSS (SX1280) |
| Packet rate | 250 Hz |
| Regulatory mode | LBT (EU) |
| Telemetry ratio | 1:16 (one telemetry packet per 16 RC packets) |
| Switch mode | Wide |
| Dynamic power | ON (10–100 mW, LBT limit) |
| Binding | Standard (TX16S ELRS menu → Bind) |

### Link quality indicators (OSD)

| Indicator | Healthy | Warning | Critical |
|---|---|---|---|
| RSSI (dBm) | > −80 | −80 to −100 | < −100 |
| LQ (%) | > 90% | 70–90% | < 70% |
| SNR (dB) | > 0 | −5 to 0 | < −5 |

Low LQ at close range often indicates local 2.4 GHz congestion rather than
insufficient transmit power. Dynamic power will increase output, but if LQ
remains low despite maximum power, consider antenna orientation.

---

## Procedure

### Binding RP2 receiver to TX16S

1. Remove props from drone.
2. Power on TX16S. Navigate to ELRS module settings.
3. Press and hold bind button on RP2 receiver while connecting battery to drone.
4. RP2 LED flashes rapidly — binding mode active.
5. On TX16S ELRS screen: tap Bind.
6. RP2 LED changes to solid — bound.
7. Power cycle drone. Link should be established within 1 second.
8. Verify in Betaflight Receiver tab: all channels respond to stick movement.

---

## Rationale

### Why 250 Hz and not 500 Hz

ELRS supports packet rates from 50 Hz to 500 Hz. Higher rates give lower
latency but less range (shorter dwell time per packet = less processing gain).
At 500 Hz, the useful range in LBT mode drops noticeably compared to 250 Hz.
For libdrone's mapping and payload missions — where 6 ms vs 3 ms latency is
imperceptible but maximum reliable range matters — 250 Hz is the correct
trade-off. Racing builds optimise for minimum latency at short range; libdrone
optimises for reliable link at operational range.

---

## Connections

requires: []
related:
  - [[crsf-protocol]]
  - [[edgetx-model]]
  - [[elrs-mavlink-mode]]
leads_to:
  - [[crsf-protocol]]
  - [[elrs-mavlink-mode]]
  - [[sk-radio-controller-guide]]


[open-source-philosophy]: open-source-philosophy.md "Open source philosophy"
[crsf-protocol]: crsf-protocol.md "CRSF protocol"
[edgetx-model]: edgetx-model.md "EdgeTX model configuration"
[elrs-mavlink-mode]: elrs-mavlink-mode.md "ELRS MAVLink mode"
[sk-radio-controller-guide]: ../skeletons/sk-radio-controller-guide.md "Radio Controller Guide"
