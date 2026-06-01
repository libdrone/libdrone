---
id: crsf-protocol
title: "CRSF protocol"
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

CRSF (Crossfire Serial Format) is the serial protocol that carries RC channels,
link statistics, and bidirectional MSP commands between the ELRS receiver and
the flight controller over a single UART wire pair. It operates at 420,000 baud
and delivers 16 channels at 11-bit resolution (2048 discrete values per channel)
plus RSSI, SNR, and link quality in every packet. CRSF replaced the legacy
1000–2000 µs PWM pulse protocol with a digital, noise-immune, bidirectional
link that updates at the full 250 Hz ELRS packet rate.

---

## Concept

### Why CRSF replaced PWM for RC signal

The original RC protocol — the pulse-width modulation scheme inherited from
servo control in the 1970s — encoded each channel as a pulse width between
1000 and 2000 microseconds. Problems for a modern flight controller:

- **Noise susceptibility**: electrical noise could shift pulse width,
  producing spurious stick inputs
- **Resolution**: ~1000 discrete values per channel
- **One wire per channel**: 8 channels required 8 wires to the FC
- **No feedback**: the receiver could not communicate link statistics back
  to the FC or transmitter

SBUS (from Futaba, 2008) improved this by multiplexing up to 16 channels on
one wire at 100,000 baud, but remained one-way and used an inverted signal
that required hardware inversion on some FCs.

CRSF solves all of these: digital framing with CRC, one wire pair for all
channels bidirectionally, full link statistics in every packet, and
implementation at 420,000 baud matches the 250 Hz ELRS update rate.

### CRSF frame structure

The RC channels frame (type 0x16) is 26 bytes. 64 bytes is the CRSF protocol's
maximum frame size, not the size of every frame:

    Byte 0:     Device address (0xC8 = FC)
    Byte 1:     Frame length
    Byte 2:     Frame type (0x16 = RC channels)
    Bytes 3–24: 11-bit packed channel values (16 channels × 11 bits = 176 bits = 22 bytes)
    Byte 25:    CRC-8

The 11-bit channel values map to RC range: 172 = minimum, 992 = centre, 1811 = maximum.
Betaflight maps these internally to its own range. The CRC protects against
single-bit errors — a corrupted frame is discarded rather than applied.

### Bidirectional telemetry

CRSF is bidirectional on the same wire. The FC can send MSP frames back to the
receiver, which relays them to the transmitter. This enables:

- **Link statistics in the OSD**: RSSI, SNR, and LQ (link quality percentage)
  from the receiver appear in the Betaflight OSD without any additional wiring
- **Sensor telemetry at the transmitter**: battery voltage, GPS position,
  altitude, and flight mode are visible on the TX16S screen during flight
- **Parameter configuration**: some advanced ELRS configurations can be adjusted
  via the transmitter's telemetry link without USB access to the receiver

---

## Reference

### CRSF configuration in Betaflight

In Betaflight Configurator → Ports tab:
- UART3: Serial RX enabled (leave baud on Auto — CRSF auto-negotiates)

In Configuration tab:
- Receiver: Serial (via UART)
- Serial Receiver Provider: CRSF

### Channel mapping verification

In Receiver tab with transmitter connected:
- All sticks centred: CH1–CH4 should read approximately 1500
- Roll right: CH1 increases
- Pitch forward: CH2 decreases (in Betaflight's convention)
- Throttle up: CH3 increases
- Yaw right: CH4 increases
- ARM switch (SF down): CH5 changes from ~1000 to ~2000

If any channel is reversed, reverse it in EdgeTX model mixing (not in Betaflight
— always fix at the transmitter side).

### CRSF vs legacy protocols comparison

| Protocol | Channels | Resolution | Baud | Bidirectional | Noise immunity |
|---|---|---|---|---|---|
| PWM (1 wire) | 1 per wire | ~1000 values | 50 Hz | No | Low |
| SBUS | 16 | 2048 | 100,000 | No | Medium |
| CRSF | 16 | 2048 | 420,000 | Yes | High (CRC) |

---

## Procedure

### Diagnosing CRSF issues

1. **No channels in Betaflight Receiver tab**: UART3 not set to Serial RX,
   or baud rate set to a fixed value (should be Auto).
2. **Channels present but wrong direction**: reverse affected channels in
   EdgeTX, not in Betaflight.
3. **Link statistics not showing in OSD**: telemetry not enabled in ELRS
   module settings on TX16S. Enable "Telemetry" in ELRS menu.
4. **Intermittent channel spikes**: electrical noise on UART3 wire. Check
   the wire is routed in the signal channel (not alongside power wires),
   and that the signal ground is connected.

---

## Rationale

### Why CRSF at 420,000 baud rather than a lower baud rate

At 250 Hz ELRS packet rate, one new RC frame arrives every 4 ms. The RC
channels frame is 26 bytes. At 420,000 baud (approximately 42,000 bytes/second
with 8N1 framing), a 26-byte frame transmits in ~0.6 ms — well within the 4 ms
window. Even a maximum-size 64-byte CRSF frame takes only ~1.4 ms, so the link
has ample margin. At lower baud rates, serial transmission would approach or
exceed the packet interval, causing frame queuing and added latency. The
420,000 baud rate is chosen to clear the packet rate with comfortable margin.

---

## Connections

requires:
  - [[elrs-protocol]]
related:
  - [[flight-controller-hardware]]
  - [[edgetx-model]]
leads_to:
  - [[sk-radio-controller-guide]]
  - [[digital-fpv]]


[elrs-protocol]: elrs-protocol.md "ExpressLRS protocol"
[flight-controller-hardware]: flight-controller-hardware.md "Flight controller hardware"
[edgetx-model]: edgetx-model.md "EdgeTX model configuration"
[sk-radio-controller-guide]: ../skeletons/sk-radio-controller-guide.md "Radio Controller Guide"
[digital-fpv]: digital-fpv.md "Digital FPV"
