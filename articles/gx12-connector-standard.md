---
id: gx12-connector-standard
title: "GX12 connector standard"
version: 1.1.0
date: 2026-05-24
author: jsa
status: released
scope: libdrone
topic:
  - payload-architecture
personas:
  - 1.builder
  - 3.payload-dev
  - 6.evaluator
  - 7.contributor
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The libdrone payload interface uses two GX12-7 aviation connectors as a
standardised, weatherproof, modular interface between the drone and any
interchangeable payload. Connector A (left, X = −25 mm) carries power and
primary communications. Connector B (right, X = +25 mm) carries data and
auxiliary control. Both are IP65-rated when mated and locked, rated for more
than 500 mating cycles, and use a D-D bore profile in the printed chimney to
prevent rotation under repeated payload swaps. A payload built to this
interface standard works on any compliant libdrone platform regardless of
version or manufacturer.

---

## Concept

### Why a connector standard exists

A drone platform without a defined payload interface requires custom electrical
integration for every new sensor or camera. Each payload is a one-off. When
the platform changes, the payloads must be reworked. This is the primary
reason scientific drone payloads are expensive and slow to develop.

A connector standard inverts this. One airframe, many payloads. Any payload
built to the standard works immediately on any compliant platform. An institution
that invests in developing an air quality payload can also use it on a radiation
survey drone, a mapping drone, or a future platform — without electrical
rework. The standard creates an ecosystem where each new payload adds value
to every existing platform and every existing platform adds value to every
new payload.

The GX12-7 standard was chosen over custom connectors because GX12 aviation
connectors are: globally available from multiple suppliers, rated IP65 when
locked, rated >500 mating cycles, field-serviceable (pins are replaceable),
and mechanically robust enough for outdoor and crash-incident use.

### The D-D bore and anti-rotation

The GX12-7 male body has two parallel flats machined into its cylindrical
body — a "D-D" cross-section. The printed chimney bore must match this profile
exactly. A round bore would allow the connector body to rotate when a payload
is screwed on or off — backing off the retention nut and eventually ejecting
the connector mid-flight.

The D-D bore is not optional. It is the mechanical feature that makes repeated
payload swaps possible. → See [[variable-table-values]] for the exact bore
dimensions (`GX12ChimneyBoreFlatFlat` = 10.80 mm, `GX12ChimneyBoreOD` = 11.87 mm).

**Post-print support removal**: clear the chimney bore with a pick or wire.
Never use a round drill bit — a 12 mm drill cannot enter an 11.87 mm bore
cleanly and will destroy the anti-rotation flats.

### Vibration retention

Drone vibration backs off threaded fasteners in service. A single nut on the
GX12 panel mount is insufficient — it will loosen within tens of flights.
Required retention: double nut (inner against Platform underside, outer
locking against inner) plus Loctite 243 blue on the outer nut thread only.
The D-D bore prevents rotation; the double nut prevents axial loosening.

### Open standard, closed payloads

The CERN OHL-S v2 copyleft applies to modifications of the libdrone platform
hardware. It does not apply to payload designs that implement this connector
interface. A company building a proprietary sensor payload to this standard
retains full ownership of that payload design. The interface is open; the
payloads are yours.

---

## Reference

### Connector positions

All positions from X body centre. Y+ = nose. X+ = right.

| Connector | X | Y | Role |
|---|---|---|---|
| Connector A | −25.0 mm | −66.0 mm | Signal + power (LEFT) |
| Connector B | +25.0 mm | −66.0 mm | Data + aux (RIGHT) |
| Centre-to-centre | 50.0 mm | — | — |

### Connector mechanical specification

| Parameter | Value |
|---|---|
| Type | GX12-7 (7-pin, 12 mm body designation) |
| IP rating | IP65 when mated and locked |
| Retention | Screw-lock ring, finger-tight |
| Mating cycles | >500 rated |
| Drone-side gender | Male panel mount — pins face upward |
| Payload-side gender | Female cable mount |
| Chimney bore | D-D profile, 10.80 mm flat-to-flat, 11.87 mm OD |
| Chimney depth | 25.0 mm below Platform surface |
| Retention | Double nut + Loctite 243 blue |

---

## Procedure

### Verifying D-D bore after printing

1. Print Coupon 10 (GX12 chimney bore test — see [[coupon-validation]]).
2. Insert a GX12-7 male body dry with flats aligned to the bore flats.
   Must seat flush with no binding and no rocking.
3. Panel nut must thread onto the chimney without cross-threading.
4. Body must not rotate when the panel nut is turned — the D-D flats prevent it.
5. If the body is tight: increase `GX12ChimneyBoreFlatFlat` by 0.1 mm and reprint.
6. If the body rotates: the bore is too round — check the FreeCAD sketch trim
   step was applied correctly.

### Installing connectors in the Platform

1. Remove all chimney support material with a pick (not a drill).
2. Insert GX12-7 male connector from above, aligning D-D flats.
3. Thread inner panel nut from below. Tighten until connector is flush with
   Platform surface.
4. Thread outer nut. Tighten against inner nut.
5. Apply a small drop of Loctite 243 to the outer nut thread.
6. Allow 24 hours cure before first payload mating.
7. Fit dust caps on both connectors. Caps are mandatory when no payload fitted.

---

## Rationale

### Why two connectors and not one

The primary reason for the dual-connector architecture is electromagnetic
compatibility, not pin count. The 12 signals in the libdrone payload interface
fall into two categories with incompatible noise characteristics: sensitive
low-voltage signals (I2C at 400 kHz, UART4 at 115,200 baud) and
noise-tolerant or noise-generating signals (GPIO lines driving MOSFETs for
camera control, UART5, GPS tap). Sharing a single cable bundle and connector
body between these two groups allows switching transients from the GPIO lines
to couple capacitively into the I2C and UART4 wires. At 400 kHz Fast Mode
I2C, this coupling is sufficient to corrupt bus transactions.

The solution is physical separation. Connector A carries only the sensitive
signals (I2C SCL/SDA, UART4 TX/RX, 5V regulated, GND). Connector B carries
the auxiliary and noise-tolerant signals (GPIO 1/2, UART5 TX/RX, GPS tap,
GND shield). Each connector's cable runs independently from the payload PCB
to the drone. Two smaller connectors with intentional channel separation
outperform a single larger connector regardless of pin count.

Pin count is a supporting constraint, not the reason. The GX12 body series
has a maximum of 7 pins in the 12 mm diameter. libdrone's 12-signal interface
fits across two GX12-7 connectors with one spare pin each. If a 12-pin body
existed in the GX12 series, the dual-connector split would still be the
correct architecture for the same EMC reasons.

### Why not the Pixhawk Payload Bus standard (DS-014)

The Pixhawk Payload Bus (PPB) defines a 40-pin KEL DY connector carrying raw
battery voltage (12–30V) and high-bandwidth interfaces (100BASE-TX Ethernet,
USB 2.0) for mid-sized payloads such as gimbals and full DSLR cameras on
larger commercial platforms. It requires an automotive-grade PCB-mounted
connector and a rigid payload bay structure — neither of which is compatible
with a 3D-printed small-platform design.

The GX12 dual-connector standard addresses a different tier: small
community-buildable platforms where field replaceability without tools,
crash resilience, and global parts availability are primary requirements.
The two standards are not in conflict. PPB software protocol is MAVLink-based;
libdrone's UART4 channel carries MSP and is MAVLink-capable, so a payload
developer targeting both tiers can share the software layer across physical
interfaces.

---

## Connections

requires:
  - [[variable-table-values]]
related:
  - [[payload-electrical-interface]]
  - [[payload-software-protocol]]
  - [[coupon-validation]]
  - [[power-signal-separation]]
  - [[pro-variant]]
leads_to:
  - [[payload-electrical-interface]]
  - [[payload-software-protocol]]
