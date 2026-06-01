---
id: electronic-speed-controllers
title: "Electronic speed controllers"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - propulsion
personas:
  - 5.student
  - 1.builder
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

An electronic speed controller (ESC) converts digital throttle commands from
the flight controller into three-phase AC power for a brushless motor. Inside,
six N-channel MOSFETs form a three-phase bridge — at any instant two MOSFETs
are active, directing current through two of the three motor windings and
creating a magnetic field the rotor chases. The ESC switches this pattern
thousands of times per second, keeping the rotor in continuous pursuit.
libdrone uses the Pilotix 75A AM32 4-in-1 6S ESC: four independent motor
controllers in one unit, running AM32 open-source firmware with bidirectional
DShot support.

---

## Concept

### The three-phase bridge

Inside the ESC, six N-channel MOSFETs are arranged in three half-bridge pairs,
one per motor phase:

    Battery+ ── HI_A ──┬── LO_A ── Battery−   (Phase A)
    Battery+ ── HI_B ──┬── LO_B ── Battery−   (Phase B)
    Battery+ ── HI_C ──┬── LO_C ── Battery−   (Phase C)

At any moment, exactly one high-side and one low-side MOSFET are active. This
connects two phases through the motor windings, creating a magnetic field. The
third phase floats — its back-EMF is monitored to detect the rotor position
without sensors. As the rotor approaches the active field position, the ESC
advances to the next commutation step, moving the field forward. The rotor
chases continuously.

MOSFET selection is critical. N-channel MOSFETs have low on-resistance (Rds_on)
— typically 2–5 mΩ for modern FET ESC designs. A MOSFET with 2 mΩ Rds_on
carrying 30 A dissipates only 1.8 W as heat. The same current through an older
bipolar transistor would dissipate several times more. Low Rds_on = high efficiency
= cooler ESC.

### Sensorless commutation and back-EMF

The ESC does not use sensors to detect rotor position. It infers position from
the back-EMF — the voltage the spinning rotor induces in the floating (inactive)
phase. When the back-EMF on the floating phase crosses through the midpoint
between supply rails (the zero-crossing), the rotor is at a known position
relative to the active field. The ESC uses this zero-crossing to time the
next commutation step.

At very low RPM (startup), back-EMF is too small to detect reliably. The ESC
uses a startup sequence — briefly running in open-loop, forcing commutation at
a fixed rate to accelerate the motor until back-EMF becomes detectable. This
is why motors take ~0.5 s to reach minimum stable RPM after an arm command.

### AM32 firmware

AM32 is open-source 32-bit ESC firmware running on an STM32F051 microcontroller
inside the ESC. It handles commutation timing, DShot protocol decoding,
bidirectional DShot eRPM reporting, and current limiting. It runs at 48 kHz
switching frequency — each MOSFET switches on and off 48,000 times per second.

48 kHz provides approximately 14 switching cycles per commutation step at
30,000 RPM (3,500 Hz electrical frequency). This gives smooth current waveforms
with low ripple, which means cooler motor windings and less electromagnetic noise
compared to lower switching frequencies.

AM32 is the open alternative to proprietary BLHeli_32. Its source code is
publicly available; the community adds features and fixes bugs. → See
[[open-source-philosophy]].

### Current rating and safety margin

The ESC must handle the peak current any single motor-propeller combination
draws at full throttle. The BrotherHobby 2507 draws 40–55 A per motor at peak.
The Pilotix 75A ESC provides a 35–85% safety margin over the measured peak.

A safety margin is necessary because: motor current increases as battery
voltage drops during a flight (lower back-EMF headroom means more current for
the same mechanical output); simultaneous full-throttle events on all four motors
can create brief current spikes above the steady-state maximum; and ESC
temperature derating reduces the continuous rating by 10–20% when warm.

### Capacitor placement

The 1000 µF low-ESR electrolytic capacitor soldered directly to the ESC power
pads is not there for energy storage — it stores only ~0.24 J (trivial). Its
function is suppressing back-EMF voltage spikes when motors rapidly decelerate.
A decelerating motor briefly acts as a generator, pushing voltage back into
the power bus. At 6S, unclamped spikes can exceed the MOSFET drain-source
breakdown voltage and destroy the ESC.

**Critical:** every millimetre of wire or trace between the capacitor and the
ESC pads adds approximately 1 nH of inductance. At a 50 A/µs transient, each
1 nH adds 50 mV to the unclamped spike. The capacitor must be soldered directly
onto the ESC power pads — no pigtail wire. The TVS diode (SMBJ28A, integrated
in the Pilotix ESC) provides additional clamping at nanosecond timescales.

---

## Reference

### Pilotix 75A AM32 4-in-1 6S — libdrone specification

| Parameter | Value |
|---|---|
| Current rating | 75 A continuous per motor |
| Voltage rating | 6S (up to 25.2V) |
| Firmware | AM32 (open-source) |
| Protocol | DShot600, bidirectional DShot |
| Switching frequency | 48 kHz |
| Internal processor | STM32F051 |
| TVS protection | SMBJ28A (integrated) |
| Battery connector | XT60H-M (ships installed) |
| Mass | 19 g |
| Mounting | 30.5 mm stack pattern |

### Thermal management

The ESC sits at the centre of the Platform middle layer. The always-on
Gdstime 3010 fan at the Platform rear draws air front-to-rear across the
ESC/FC stack. This active cooling keeps ESC junction temperatures within
operating range during sustained full-throttle climbing and aggressive
manoeuvres. Without the fan, sustained high-throttle flight at ambient
temperatures above 25°C may trigger the ESC's thermal current-limiting,
which reduces thrust asymmetrically and degrades flight performance.

---

## Procedure

### ESC startup verification

1. Connect battery. Do not arm for 5 seconds — wait for gyro calibration.
2. Arm. All four motors should initialise simultaneously (brief beep sequence).
3. In Betaflight Motors tab (props removed): advance master slider to 10%.
   All four motors should spin up simultaneously. If any motor lags by more
   than ~1 second, BiDi DShot may not be fully synchronised — rebind or
   check DShot configuration.
4. Verify eRPM reporting: at ~20% throttle, all four motors should report
   non-zero eRPM values proportional to commanded speed.

### Post-crash ESC inspection

1. Visually inspect the ESC PCB for burnt components, lifted pads, or
   discolouration from heat.
2. Check motor solder joints — crash forces can crack solder joints on
   motor phase wires.
3. After any hard crash, run the motor verification above before the
   next flight — a damaged ESC MOSFET may still function at low throttle
   but fail at high current.

---

## Rationale

### Why a 4-in-1 ESC rather than four individual ESCs

A 4-in-1 ESC consolidates four controllers onto one PCB, sharing the power
input and ground connections. This reduces connector count, wiring length, and
total mass compared to four separate ESCs. The single shared power pad accepts
one set of battery lead connections and one capacitor location. With four
separate ESCs, each needs its own power tap, capacitor, and mounting — adding
~15–20 g of wiring and connectors and introducing multiple additional failure
points. The 4-in-1 design also uses the stack mounting pattern directly,
eliminating the need for ESC mounting plates.

---

## Connections

requires:
  - [[brushless-motors]]
related:
  - [[propellers]]
  - [[dshot-protocol]]
  - [[rpm-filter]]
leads_to:
  - [[dshot-protocol]]


[open-source-philosophy]: open-source-philosophy.md "Open source philosophy"
[brushless-motors]: brushless-motors.md "Brushless motors"
[propellers]: propellers.md "Propellers"
[dshot-protocol]: dshot-protocol.md "DShot protocol"
[rpm-filter]: rpm-filter.md "RPM filter"
