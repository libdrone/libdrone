---
id: pid-loop-rate
title: "PID loop rate"
version: 1.0.0
date: 2026-04-15
author: jsa
status: released
scope: generic
topic:
  - software-stack
personas:
  - 5.student
  - 8.architect
  - 1.builder
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The PID loop rate is how many times per second the flight controller reads
the gyroscope, runs the PID calculation, and sends new motor commands. Betaflight
on the H7A3-SLIM runs at 8 000 Hz — 40× faster than the Nyquist minimum for
the highest useful manoeuvre frequency. This is not excess: each step in the
gyro-to-motor chain introduces delay, and lower delay per cycle allows higher
PID gains with the same stability margin. Higher P gain means better disturbance
rejection. Better disturbance rejection means the drone holds attitude more
precisely in wind. The H7's hardware FPU makes this possible without compromising
processor headroom for the RPM filter, GPS parsing, and blackbox logging running
simultaneously.

---

## Concept

### Why faster than Nyquist

The Nyquist-Shannon theorem states that to faithfully capture a signal
of frequency F, you must sample at ≥ 2F. The highest meaningful control
frequency for drone attitude manoeuvres is approximately 100 Hz — so a 200 Hz
loop rate would satisfy Nyquist. Betaflight runs at 8 000 Hz — 40× this minimum.
Why?

In a control system, delay is the enemy of stability. Every processing step
between gyro measurement and motor command takes time, and that accumulated
delay reduces the phase margin of the PID controller. Lower phase margin means
the PID gain must be set lower to avoid oscillation. Lower P gain means slower
disturbance rejection and less precise attitude hold.

At 1 000 Hz, each loop cycle takes 1 ms. At 8 000 Hz, each cycle takes
125 µs. The PID gain that is stable at 8 000 Hz would cause oscillation at
1 000 Hz because the 8× longer cycle latency reduces the phase margin below
the stability threshold. Higher loop rate does not change the control physics
— it changes the achievable gain, and higher gain means better performance.

### The full processing chain

At each 125 µs loop cycle, the H7A3-SLIM executes this sequence:

**Gyro read via DMA** (~13 µs): The DMA controller transfers 16 bytes from
the ICM-42688-P over SPI at 10 MHz without CPU involvement. The CPU set up
the transfer and receives an interrupt when data arrives.

**RPM filter** (~20 µs): eRPM telemetry from the four ESCs is used to
calculate current motor frequencies and harmonics. Thirty-six notch filter
coefficients are updated and the raw gyro data is filtered.

**Dynamic notch filter** (~10 µs): A sliding spectrum estimate identifies
high-amplitude noise peaks not corresponding to motor frequencies and places
additional notch filters at them.

**PID calculation** (~15 µs): Three independent loops (roll, pitch, yaw)
each compute P, I, and D terms. The hardware FPU executes floating-point
multiply-accumulate in a single clock cycle — PID arithmetic is effectively
free.

**Motor mixing** (~5 µs): Three PID outputs are combined with base throttle
through the mixer matrix to produce four motor commands.

**DShot600 transmission** (~26 µs): Four 16-bit DShot packets are transmitted
simultaneously via hardware timer peripherals.

Total: ~90 µs. This leaves 35 µs of slack in the 125 µs window for lower-
priority tasks: GPS parsing, OSD frame generation, UART communication, and
blackbox logging.

### Why the H7A3 is necessary

The F4 processor could run the PID loop at 8 000 Hz but not the RPM filter
simultaneously — it lacked the CPU headroom. The H7A3 runs both with
processor headroom to spare. This is not marketing — it is the specific
reason why the RPM filter is available without trade-offs on the H7A3 and
required dropping loop rate to 4 000 Hz on F4. See → [[rpm-filter]].

---

## Reference

| Loop rate | Cycle time | End-to-end latency | Typical gain ceiling |
|---|---|---|---|
| 1 000 Hz | 1 000 µs | ~5–10 ms | Low |
| 4 000 Hz | 250 µs | ~1–2 ms | Medium |
| 8 000 Hz | 125 µs | ~500 µs | High |

**H7A3-SLIM processing headroom at 8 kHz:**
- PID + RPM filter + dynamic notch: ~84 µs per cycle
- Remaining headroom: ~41 µs (33% of loop window)
- Used for: GPS, OSD, UART, blackbox

**DShot600 bit rate**: 600 kbit/s — transmits one 16-bit packet in ~26 µs.
All four motor packets transmitted simultaneously via independent hardware
timer channels.

---

## Procedure

### Verify loop rate in Betaflight

In Betaflight Configurator → Configuration tab → PID Loop:
- Gyro update frequency: 8 kHz
- PID loop frequency: 8 kHz

If the H7A3-SLIM shows less than 8 kHz, check that RPM filter (bidirectional
DShot) is enabled — the filter requires F7/H7 class processor. Disable RPM
filter temporarily to confirm 8 kHz is achievable, then re-enable.

---

## Rationale

Understanding loop rate as a consequence of control system latency requirements
— rather than as a marketing specification — changes how builders interpret
build anomalies. If a build oscillates at a gain setting that should be stable
on H7A3, the first diagnostic question is whether the loop rate is actually
achieving 8 kHz or has been throttled by a conflicting process. If props-in
arming fails on a new build, checking DShot and loop rate is the correct
starting point. Loop rate is not set-and-forget — it is the timing substrate
that every other flight controller behaviour depends on.

---

## Connections

requires:
  - [[flight-controller-hardware]]
  - [[closed-loop-control]]
  - [[rpm-filter]]
related:
  - [[imu-gyroscope]]
  - [[imu-filter-tuning]]
  - [[dshot-protocol]]
  - [[pid-derivative-term]]
  - [[resonance-filtering]]
leads_to:
  - [[rpm-filter]]
  - [[pid-tuning-rate-profile]]
  - [[blackbox-analysis]]
