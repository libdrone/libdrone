---
id: scrap-variant
title: "SCRAP variant"
version: 1.1.2
date: 2026-06-01
author: jsa
status: released
scope: libdrone
topic:
  - frame-structure
  - manufacturing
  - piloting-operations
personas:
  - 1.builder
  - 5.student
  - 4.workshop
platform:
  - core
lang: en
licence: CC BY-SA 4.0
---

## Summary

SCRAP — Simple Configurable Repeatable Aerial Platform — is the entry-level
printable 3-inch 4S FPV build in the libdrone family. It is not an official
platform variant with a payload interface or a mission role. It is the build
that teaches you to build. SCRAP uses a freely downloadable printable frame,
a standard 20×20 FC/ESC stack, and the same ELRS and HDZero ecosystem as Core
and Pro. A pilot who builds and tunes SCRAP has directly transferable skills
when stepping up to Core. A builder who crashes and reprints SCRAP has learned
what breaks and why — which is the Core design input it was designed to provide.

---

## Concept

### What SCRAP is not

SCRAP is not a libdrone platform variant in the mission sense. It has no GX12-7
payload interface. It has no defined sensor suite. Its sub-250 g design target
has regulatory implications for where it may be flown — see
[[legal-and-regulatory]] and decide for yourself. It will crash. It will crash
again. That is its purpose.

### What SCRAP is

SCRAP is the learning environment that precedes Core. It answers the question
every builder asks before committing to a full Core or Pro build: can I actually
do this? The answer is yes — and SCRAP is the proof. The frame prints in an
evening on a Prusa CoreOne+ in PETG-CF. The electronics cost roughly CZK 9,500
total. The build takes one afternoon. The first flight can happen within 30 days
of the decision to build.

### The printable frame

The Whifflepick 3" toothpick frame (Printables model 1207344) is the reference
SCRAP frame. 3 perimeter walls, 3 top/bottom layers, 0% infill, no supports.
PETG-CF is the correct material — carbon-fibre-reinforced PETG is abrasion-
resistant, available on a standard 0.4 mm hardened nozzle, and stiff enough
for 4S loads on 3-inch props. The arms are integral to the frame. When an arm
breaks — and it will — the print time for a replacement is under two hours.

The 20×20 mm FC stack mounting pattern is the only dimensional constraint
that matters. It is universal across every micro FC stack sold.

### Ecosystem alignment

SCRAP uses the same radio ecosystem as Core and Pro:
- **Radio:** ExpressLRS 2.4 GHz UART (EP1 Dual or EP2) — same as Core and Pro
- **FC firmware:** Betaflight — same as Core
- **Video:** HDZero ECO Bundle — same ecosystem as Pro, lower weight than full HDZero stack
- **Transmitter:** EdgeTX on TX16S — same as Core and Pro

Every hour of SCRAP flight time is directly applicable to Core and Pro operation.
Betaflight rate profiles learned on SCRAP transfer directly. ELRS binding procedures
are identical. The only difference is the absence of a payload interface and the
smaller prop disc.

### Core design input

SCRAP is a Core prototype with a lower budget and a printable frame. Every crash
produces information: what breaks first, what survives, what is fiddly to reassemble
under field conditions. This information feeds directly into Core frame design
decisions. The educational intent of Core — building and repairing a drone as a
workshop curriculum — requires a builder who has built and repaired a drone.
SCRAP is how that builder is made.

---

## Reference

| Parameter | Value |
|---|---|
| Frame | Whifflepick 3" (Printables model 1207344) |
| Wheelbase | ~130 mm (3-inch class) |
| Frame material | PETG-CF |
| FC | SpeedyBee F405 Mini |
| ESC | SpeedyBee BLS 35A Mini V2 (integrated stack) |
| Stack mount | 20×20 mm, M3 |
| Motors | Happymodel EX1404 3500KV |
| Motor shaft | 1.5 mm |
| Props | HQProp T3X3X3 3-blade polycarbonate |
| Battery | Tattu 450 mAh 4S 75C XT30 |
| Battery connector | XT30 |
| Video TX | HDZero ECO VTX (~4.5 g) |
| Camera | HDZero ECO Camera (~1.6 g) |
| Video power | 5V BEC — NOT VBAT |
| Receiver | Happymodel EP1 Dual ELRS 2.4 GHz TCXO |
| Charging | XT30/XT60 parallel charging board |
| LiPo storage | Fireproof LiPo safe bag (mandatory) |
| Firmware | Betaflight |
| Weight target | sub-250 g (regulatory implications — see [[legal-and-regulatory]]) |
| BOM cost | ~CZK 9,500 |

---

## Procedure

<!-- not applicable -->

---

## Rationale

The decision to build SCRAP rather than buy a BNF tinywhoop (e.g. Happymodel
M8 HDZero) was reached by analysing the actual use case: outdoor pilot practice
in a 2,700 m² space with obstacle poles in variable wind conditions. A tinywhoop
at 80 mm wheelbase and 33 g is dominated by wind above 15 km/h and provides no
crash resistance in grass. SCRAP at 130 mm wheelbase with 3-inch props and 4S
power handles outdoor conditions while remaining buildable, repairable, and cheap
enough to crash without concern.

The choice of HDZero ECO over analog video was made on ecosystem coherence:
the operator already owns HDZero Goggles 2. Buying an analog VTX plus an analog
receiver module for the goggles would have cost approximately the same as the
ECO Bundle while creating a separate ecosystem with no skill transfer value.
HDZero ECO keeps the video pipeline identical to Pro.

The Whifflepick 3" was chosen over the PecaJosef 3" because it is actively
maintained (updated April 2025), requires no supports (fast reprints), and
uses PETG-CF natively. The PecaJosef has more community build reports but
is a heavier design and the Whifflepick community has confirmed 4S flight.

---

## Connections

requires:
  - [[platform-overview]]
  - [[print-profiles]]
  - [[betaflight-setup]]
  - [[lipo-batteries]]
related:
  - [[core-variant]]
  - [[digital-fpv]]
  - [[elrs-protocol]]
  - [[wire-gauge-selection]]
  - [[electronic-speed-controllers]]
  - [[brushless-motors]]
  - [[petg]]
  - [[pccf]]
leads_to:
  - [[sk-scrap-build-guide]]
  - [[core-variant]]
  - [[betaflight-setup]]
