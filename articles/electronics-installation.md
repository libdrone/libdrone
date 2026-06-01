---
id: electronics-installation
title: "Electronics installation"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - manufacturing
personas:
  - 1.builder
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Electronics installation populates the completed airframe with the FC/ESC
stack, power components, sensors, video system, and payload connectors.
The sequence is fixed: capacitors first (before any other soldering), then
the power domain, then motors, then signal chain. Every wire is routed
before the stack is bolted down. EMC rules govern every routing decision:
star ground, twisted pairs on all high-current wires, power wires right
channel, signal wires left channel. Conformal coating is mandatory before
first power-on. Total duration: approximately 8–10 hours including cure time.

---

## Concept

### Why capacitors install first

The 1000 µF bulk capacitor must be soldered directly to the ESC VBAT/GND
pads before any motor or power wiring is connected. The first time full
battery voltage is applied through any path, inrush current will spike.
The capacitor needs to be in place to absorb that spike before it reaches
the MOSFETs. Installing the capacitor last means the first power test is
the first unprotected high-current event.

The 100 µF MLCC ceramic capacitor on the FC 5V pads handles the faster
high-frequency spikes the electrolytic cannot respond to quickly enough.
Both are mandatory. → See [[capacitor-placement-emc]] for the physics.

### Route before you bolt

Every cable must be routed to its final position before the FC/ESC stack
is bolted down. Attempting to route cables with the stack in place means
working around standoffs and connectors in a tight space — the probability
of disturbing a previously soldered joint or routing a wire into the wrong
channel increases significantly. Route, verify, then bolt.

---

## Reference

### Installation sequence

| Step | Action | Gate check |
|---|---|---|
| 5.1 | Solder 1000 µF Panasonic low-ESR cap directly to ESC VBAT+/GND pads. Leads ≤ 5 mm. Solder 100 µF MLCC to FC 5V pads. | Cap body flat on ESC surface. No pigtail wire. |
| 5.2 | Route ALL cables. Do not bolt stack down yet. | All cables reach destinations without tension |
| 5.3 | Solder MR30 pigtails to ESC motor outputs. Label M1–M4 with heatshrink colour. Twist 3 phase wires per motor immediately. | Labels correct per motor layout diagram |
| 5.4 | Install buck converter XL4015 output → VTX power. Clip 3–4 TDK ferrite beads onto VTX power wire at converter output. Install TVS diode SMBJ28A on ESC VBAT/GND pads alongside primary cap. | Ferrites within 30 mm of converter output |
| 5.5 | Battery leads: twist + and − from XT60 to ESC pads. Target 40–50 mm length. Route rearward, drop through battery lead relief notch. | No sharp bends. Loop area minimal. |
| 5.6 | Bind RP2 receiver to TX16S before installing. Route receiver signal wire along LEFT channel. | Link established in Betaflight Receiver tab |
| 5.7 | GPS M10Q: route cable LEFT channel only. GPS GND via FC — not a separate wire to ESC. | Never adjacent to phase wires |
| 5.8 | HDZero VTX: mount at Platform −104 to −133 mm. Camera on GPS/camera bracket. Route MIPI cable (225 mm) through Platform centreline channel. VTX power from buck converter via ferrites. | MIPI minimum bend radius 30 mm respected |
| 5.9 | Bolt down FC/ESC stack. Solder joint inspection under magnification. | All joints shiny, concave fillet. No matte or balled joints. |
| 5.10 | Conformal coating: mask all connectors, USB, MIPI ZIF, ESC motor pads, cap pads. Two thin coats. 24 h cure. UV inspect. | UV lamp: all exposed copper fluoresces |
| 5.11 | Wire management: zip-ties at 30 mm intervals. 5 mm minimum separation antenna to power wires. | No wire contacts rotating parts |
| 5.12 | GX12 payload connectors: solder all 12 wires to FC before placing Platform top layer. Thread bundle through chimney during top layer placement. Insert connector, tighten panel nut, fit dust caps. | Continuity test all 12 pins. No shorts between adjacent pins. |

### Star ground topology (mandatory)

    ESC GND pad ← master ground point
      ├── Battery GND lead (direct)
      ├── FC GND (short direct wire)
      ├── 1000 µF cap GND (on pad)
      ├── TVS diode GND (on pad)
      └── Buck converter GND → VTX GND

    GPS GND → via FC → NOT a separate wire to ESC
    RP2 receiver GND → via FC signal GND

Never create a second GND path from any subsystem back to the battery.
→ See [[star-grounding]].

### Wire channel assignment

| Wire type | Channel | Side |
|---|---|---|
| Motor phase wires | Arm shaft dovetail groove | Bottom face of arm |
| Battery leads | Platform battery lead relief notch | Centreline rear |
| ESC power, buck converter | Power channel | RIGHT (X = +20 mm) |
| MIPI cable | Platform centreline channel | Enclosed, centre |
| GPS, UART, I2C, receiver | Signal channel | LEFT (X = −20 mm) |
| GX12 wires (Connector A) | Signal channel | LEFT |
| GX12 wires (Connector B) | Power channel | RIGHT |

---

## Procedure

### Solder joint inspection criteria (step 5.9)

Inspect every joint under a 5× loupe or USB microscope:

- **Accept**: shiny surface, concave fillet flowing onto wire and pad, wire
  fully tinned, no cracks
- **Reject and resolder**: matte or grainy surface (cold joint), balled solder
  not wetting the pad, visible crack at wire-to-solder interface, solder
  bridges between adjacent pads

High-current joints (XT60 lugs, ESC VBAT pads, motor MR30s): after visual
pass, do a voltage-drop check. Apply 1A from bench PSU. Measure across each
joint. Above 5 mV at 1A indicates a high-resistance joint — resolder.

### First power-on sequence

Do not apply battery power until conformal coating is fully cured (24 h).

1. Transmitter on first.
2. Connect bench PSU set to 5V current-limited to 500 mA to the FC 5V pad
   via a current-limited cable (bypasses ESC). Verify FC boots, Betaflight
   connects via USB.
3. Disconnect bench PSU. Connect battery via ShortSaver V2 (or equivalent
   current-limited power path). Verify ESC arms in Betaflight Motors tab.
4. Spin each motor in Motors tab (props off). Verify all four respond.
5. Verify battery voltage on OSD matches handheld multimeter ±0.2V.

---

## Rationale

### Why conformal coating precedes first power-on

Solder flux residue left on PCB surfaces is mildly conductive and hygroscopic.
In humid conditions, flux residue can create resistive leakage paths between
adjacent pads. Applying power to an uncoated board in a humid environment
risks creating salt bridges. Conformal coating applied over clean flux residue
seals it permanently. Coating applied after the first power cycle may seal
in moisture already absorbed. The correct order is: clean solder joints,
inspect, coat, cure, then power on.

---

## Connections

requires:
  - [[airframe-integration]]
  - [[star-grounding]]
  - [[twisted-pairs]]
  - [[capacitor-placement-emc]]
  - [[power-signal-separation]]
  - [[conformal-coating]]
  - [[gx12-connector-standard]]
related:
  - [[ferrite-beads]]
  - [[voltage-regulation]]
  - [[flight-controller-hardware]]
leads_to:
  - [[betaflight-setup]]


[capacitor-placement-emc]: capacitor-placement-emc.md "Capacitor placement for EMC"
[star-grounding]: star-grounding.md "Star grounding"
[airframe-integration]: airframe-integration.md "Airframe integration"
[twisted-pairs]: twisted-pairs.md "Twisted pairs"
[power-signal-separation]: power-signal-separation.md "Power and signal separation"
[conformal-coating]: conformal-coating.md "Conformal coating"
[gx12-connector-standard]: gx12-connector-standard.md "GX12 connector standard"
[ferrite-beads]: ferrite-beads.md "Ferrite beads"
[voltage-regulation]: voltage-regulation.md "Voltage regulation"
[flight-controller-hardware]: flight-controller-hardware.md "Flight controller hardware"
[betaflight-setup]: betaflight-setup.md "Betaflight setup"
