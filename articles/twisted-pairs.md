---
id: twisted-pairs
title: "Twisted pairs"
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
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Twisting two wires that carry equal and opposite currents together causes their
magnetic fields to cancel at any external point. Each half-twist reverses which
wire is on top, alternating the direction of the net field — the fields from
adjacent half-twists cancel each other. The result is near-zero external
magnetic radiation from the pair. This is the lowest-cost EMC mitigation
available — it requires no additional components, adds negligible mass, and
is applied during wiring. On libdrone it is applied to motor phase wires,
battery leads, and I2C signal pairs.

---

## Concept

### Why equal and opposite currents cancel

Two wires carrying equal and opposite currents produce magnetic fields that
point in opposite directions at any external point. If the wires are side by
side in a straight run, the fields partially cancel but not completely — the
net field falls off as the inverse square of distance from the pair, not the
slower inverse relationship of a single wire. Twisting adds the crucial
spatial alternation: the wire that is "on top" (closer to the victim) alternates
every half-twist. The fields from adjacent half-twists have opposite net
directions and cancel each other. The net external field approaches zero.

This is why professional telecommunications cables (CAT5/6 Ethernet) use
twisted pairs throughout: each pair carries a differential signal (equal and
opposite currents), and the twisting eliminates both the radiation from the pair
and its susceptibility to externally induced common-mode noise.

### Application to drone wiring

**Motor phase wires**: Three wires per motor (phases A, B, C) carry equal
and opposite currents summing to zero at any instant (in balanced three-phase
operation). All three should be twisted together before entering the arm cable
groove — approximately 1 twist per 15 mm. The twisting cancels the magnetic
field from the commutation current, directly reducing the contamination of the
gyroscope and compass.

**Battery leads**: The positive and negative battery leads carry equal and
opposite DC and AC currents (AC from throttle changes). Twisting them from
the XT60 connector to the ESC power pads reduces the radiated field from motor
current transients. In practice, the short run from XT60 to ESC pad (typically
50–80 mm) limits the available benefit, but any twisting helps.

**I2C signal wires (SDA + SCL)**: I2C is a two-wire bus where both wires carry
related signals at 400 kHz. Twisting SDA and SCL together reduces their
susceptibility to externally induced common-mode noise, which is the dominant
failure mode for I2C at higher frequencies and longer wire runs. On libdrone
the I2C run from FC to GX12 Connector A is short (~80 mm) but the payload cable
can be longer — all I2C wire runs in payload cables should be twisted.

**UART4 TX/RX and UART5 TX/RX pairs**: Twisted together in their respective
GX12 chimney cable bundles. These are differential in nature (TX/RX of one
channel are related) and benefit from twisting against adjacent wires.

### What twisting does not fix

Twisting reduces the field radiated by a wire pair carrying balanced currents.
It does not help when:
- Only one wire of a pair is twisted (the other is a ground plane trace, for example)
- Currents are not balanced (common-mode noise on both wires simultaneously)
- The wires are routing near each other but not twisted (still couples)

For unbalanced signals (single-ended UART, GPS), twisting the signal wire
with a dedicated return wire (rather than relying on a shared ground) provides
additional benefit. In practice this is rarely done on drones due to connector
constraints, but it is the correct approach for longer signal runs.

---

## Reference

### Twisting specification for libdrone wiring

| Wire run | Specification | Why |
|---|---|---|
| Motor phase wires (3×) | ~1 twist / 15 mm | Cancels 3-phase commutation field, reduces gyro noise |
| Battery leads (+/−) | Twist from XT60 to ESC pad | Reduces motor transient radiation |
| I2C SDA + SCL (GX12 A) | Twist together throughout run | Reduces susceptibility to conducted noise on 400 kHz bus |
| UART4 TX/RX | Twist together | Reduces cross-coupling with adjacent wires |
| UART5 TX/RX | Twist together | Reduces cross-coupling with adjacent wires |
| 5V power + GND (GX12 A) | No twisting — run separately | Not differential; twisting does not help |

---

## Procedure

### Twisting motor phase wires during arm wiring

1. Cut motor phase wires to length before twisting — twisted wires are ~5–10%
   shorter than straight wires for the same point-to-point distance.
2. Hold all three wires together at one end and tape the bundle to the work surface.
3. Grip the free ends and rotate the bundle clockwise while advancing along the
   length — 1 twist approximately every 15 mm.
4. The twist should be consistent along the entire run. Irregular twisting
   provides inconsistent cancellation.
5. Route the twisted bundle through the arm cable groove before connecting to
   the ESC. Do not untwist the bundle at the groove entry — pass through twisted.

---

## Rationale

### Why 1 twist per 15 mm and not tighter

Tighter twists (more twists per cm) provide marginally better field cancellation
but increase the physical length needed for the same wire run, add rigidity that
makes routing harder, and at some point the mechanical stress on the wire
insulation becomes a factor. 1 twist per 15 mm is an established practice in
FPV drone building that provides substantial cancellation at no practical cost.
Tighter is not meaningfully better for the wire lengths involved in a 330 mm
frame.

---

## Connections

requires:
  - [[emc-noise-sources]]
related:
  - [[star-grounding]]
  - [[power-signal-separation]]
leads_to:
  - [[star-grounding]]
