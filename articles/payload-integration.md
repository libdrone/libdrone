---
id: payload-integration
title: "Payload integration"
version: 1.1.0
date: 2026-06-01
author: jsa
status: released
scope: libdrone
topic:
  - payload-architecture
personas:
  - 3.payload-dev
  - 1.builder
  - 2.operator
  - 6.evaluator
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

A compliant payload consists of a mechanical mast, the PSB-1 shield board,
a sensor or actuator, and a companion MCU (ESP32-S3) running payload firmware.
It connects to the drone via two GX12-7 female connectors and mounts to the
boss pads on the Backplane. The payload is electrically enabled by the pilot
via radio switch, sends live readings to the OSD, logs GPS-tagged data to SD
card, and is commanded by the FC. Field swap from one payload to another takes
under 2 minutes and requires no tools beyond a small hex key for the mast
screws.

---

## Concept

### The modular payload concept

libdrone's value proposition is: one airframe, multiple instruments. The
mast-based payload architecture achieves this by separating the flying
platform from the sensing payload completely. All electrical connections are
at the GX12 interface. All mechanical connections are at the M3 boss pads
(20 mm spacing) on the Backplane. The Pi bay adds 6 mm of height above the
Backplane surface — all mast heights account for this.

Swapping payloads in the field:
1. Remove battery (mandatory — never swap payload live)
2. Unscrew two M3 screws at mast base (~15 s)
3. Unplug both GX12 connectors (~10 s)
4. Plug in new payload GX12 connectors (~10 s)
5. Screw in new mast (~15 s)
6. Fit dust caps on now-empty drone connectors if no second payload ready
7. Reconnect battery and verify OSD shows new payload readings before arming

Total: under 2 minutes. No tools beyond a 2.5 mm hex key.

### Mast height selection

Three mast heights are available: 40 mm (short), 80 mm (medium), 120 mm (tall).

The minimum height to clear the propeller downwash recirculation zone for
air quality sensing is 120 mm. → See [[induced-velocity]] for the calculation.

Short and medium masts are appropriate for: non-atmospheric sensors (cameras,
radiation detectors shielded from aerodynamic effects), sensors where absolute
position rather than atmospheric sampling is the goal, or payloads where mass
must be minimised.

Mast height directly affects CG. The CG shift for a 40 g payload on a 120 mm
mast is approximately 5–6 mm upward. For payloads above 60 g on tall masts,
recalculate CG and consider D-term adjustment. → See [[pendulum-stability]].

### Payload mass budget

Keeping total payload mass low matters both for flight performance and for the
drone's all-up weight, which has regulatory implications — see
[[legal-and-regulatory]]. The air quality mast (SEN66 + ESP32-S3 + PSB-1 + mast
body) weighs approximately 55–65 g.

Heavier payloads push the all-up weight up, with regulatory consequences that
depend on how and where you fly. → See [[legal-and-regulatory]].

---

## Reference

### Payload mast specifications

| Mast | Height | Target mass | Typical use |
|---|---|---|---|
| Short | 40 mm | 15 g | Cameras, compact sensors, tests |
| Medium | 80 mm | 18 g | Near-surface atmospheric sampling with validation |
| Tall | 120 mm | 22 g | Air quality, gas sensors — required height for clean air |

All mast heights use identical base footprint: 2× M3 × 8 mm screws into
boss pads at 20 mm spacing on the Backplane surface.

### Reference payload: SEN66 air quality mast (medium/tall)

| Component | Mass |
|---|---|
| Mast body (PETG, 80 mm) | 18 g |
| PSB-1 shield board (perfboard) | 8 g |
| ESP32-S3 mini dev board | 5 g |
| Sensirion SEN66 module | 6 g |
| GX12-7 female cable connectors (×2) | 8 g |
| Cabling and hardware | 5 g |
| **Total** | **~50 g** |

### Pre-flight payload checklist

- [ ] OSD shows payload readings within 10 s of power-on
- [ ] GPS position visible in payload serial log (open site required)
- [ ] SD card inserted and logging confirmed (LED indicator on PSB-1)
- [ ] GX12 lock rings finger-tight on both connectors
- [ ] Payload master switch ON (physical switch, not only radio)
- [ ] Mast screws torqued (finger-tight + 1/4 turn, not overtightened)
- [ ] Payload mass confirmed within EASA budget

---

## Procedure

### Mating sequence (payload installation)

1. Battery removed from drone.
2. Remove dust caps from both drone-side GX12 connectors. Store in field bag.
3. Align Connector A (LEFT, payload) with Connector A (LEFT, drone).
   Match D-D anti-rotation flats. Seat until fully engaged.
4. Screw lock ring clockwise, finger-tight.
5. Repeat for Connector B (RIGHT).
6. Align mast base with boss pads. Insert 2× M3 × 8 mm screws.
7. Tighten screws — finger-tight plus 1/4 turn. Do not crush PETG.
8. Connect battery. Verify OSD shows payload readings before arming.

### Demating sequence (payload removal)

1. Disarm. Remove battery.
2. Remove 2× mast screws.
3. Unscrew Connector B lock ring. Pull straight out.
4. Unscrew Connector A lock ring. Pull straight out.
5. Fit dust caps on both drone-side connectors immediately.
6. Inspect all pins before storage.

---

## Rationale

### Why battery removal is mandatory before payload swap

The GX12 connectors are not hot-swap rated. Connecting or disconnecting under
live power can cause brief short circuits between adjacent pins during
connector engagement/disengagement. On a 5V rail this is generally harmless,
but the payload's ESP32-S3 MCU may experience a brownout or latch-up during
the transition. Removing the battery takes 5 seconds and eliminates the risk
entirely.

### Why M3 screws and not a quick-release

Quick-release mechanisms add complexity, wear over many cycles, and can fail
in ways that a simple screw fastener cannot. An M3 screw into a PETG boss
pad provides positive, inspectable, known-torque retention. Two screws prevent
any rotation of the mast on the boss pads. The 15-second per-mast swap time
is acceptable for a professional operational context.

---

## Connections

requires:
  - [[gx12-connector-standard]]
  - [[psb1-shield-board]]
related:
  - [[induced-velocity]]
  - [[pendulum-stability]]
  - [[lipo-batteries]]
  - [[legal-and-regulatory]]
leads_to:
  - [[airframe-integration]]
