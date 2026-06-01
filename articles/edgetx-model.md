---
id: edgetx-model
title: "EdgeTX model configuration"
version: 2.0.0
date: 2026-05-31
author: jsa
status: released
scope: libdrone
topic:
  - software-stack
personas:
  - 1.builder
  - 2.operator
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

EdgeTX is the open-source firmware running on the RadioMaster TX16S MKII
transmitter. The libdrone model configuration sets channel order (AETR), maps
the flight-critical switches, configures ELRS at 250 Hz LBT for EU regulatory
compliance, and enables telemetry for in-transmitter battery and RSSI
monitoring. The switch map is designed around one principle: dangerous
functions (arm, GPS Rescue) are isolated and require a deliberate reach, while
recoverable functions (rate, VTX) get convenient placement. The same map serves
both Pro and SCRAP — SCRAP simply leaves the GPS-dependent switches unused. The
model must be created manually in EdgeTX; there is no importable binary model
file.

---

## Concept

### AETR channel order

libdrone uses AETR channel assignment: Aileron on CH1, Elevator on CH2,
Throttle on CH3, Rudder on CH4. This matches Betaflight's default CRSF channel
expectations and avoids the need for channel remapping in Betaflight. The
alternative (TAER, common in DJI workflows) would require reconfiguring the
CRSF channel assignments on the FC.

### ELRS 250 Hz LBT

ExpressLRS in the EU must operate in LBT (Listen Before Talk) mode: the
transmitter checks channel occupancy before each transmission. This is a
regulatory requirement in several EU countries for the 2.4 GHz band. At 250 Hz,
one packet is sent every 4 ms. Total stick-to-FC latency is approximately
6–8 ms — well within the threshold for responsive control.

LBT adds a small variable latency per packet (the listen step before talk) but
in practice this is imperceptible, and the link statistics show no significant
packet-loss increase versus non-LBT mode in typical EU operating environments.

### Dynamic power

ELRS dynamic power adjusts transmit power automatically based on link quality.
At close range (strong signal) it runs at minimum power (10 mW). As range
increases or obstacles intervene, it increases to the configured maximum
(100 mW for the LBT/EU regulatory limit). This reduces RF noise in the 2.4 GHz
band during proximity operations without requiring manual power adjustment.

### Switch safety: isolate the dangerous, place the recoverable

The switch map is organised by what happens if a switch is actuated
accidentally while the pilot's full attention is on flying. Two actuations are
genuinely dangerous:

- **Disarm in flight** — instant power-off; the aircraft drops.
- **Unwanted mode change** — dropping from Angle into Acro mid-hover, or
  triggering GPS Rescue and then having to fight an autonomous return.

Everything else (wrong rate profile, VTX power, buzzer) is recoverable or
harmless if knocked. The map therefore follows three rules:

1. **Dangerous functions are isolated** — GPS Rescue sits alone on its own
   switch, so reaching it is always a deliberate act and never a side-effect
   of changing something else.
2. **Nothing dangerous shares a switch with a routinely-changed function** —
   the flight-mode switch is reduced to two safe, flyable states (Angle/Acro)
   with no Rescue detent in the ladder.
3. **Arm is protected twice** — by switch feel (a firm shoulder detent that is
   hard to brush) and by a throttle-low arming gate, so arming is impossible
   in flight even if the switch is moved (disarm always remains available — it
   is the emergency stop and is deliberately never gated).

---

## Reference

### TX16S switch assignments

The TX16S MKII has two-position and three-position toggles on the shoulders
(SA/SD/SG left, SB/SE/SH right) and on the front faces (SC front-left, SF
front-right). SH is the only spring-return (momentary) switch.

| Switch | Type | Label | Function | Positions |
|---|---|---|---|---|
| SA | 2-pos (L shoulder) | ARM | Arm / disarm (throttle-low gated) | Up = disarmed, Down = armed |
| SD | 2-pos (L shoulder) | MODE | Flight mode | Up = Angle, Down = Acro |
| SE | 2-pos (R shoulder) | RESC | GPS Rescue (isolated, Pro only) | Up = off, Down = Rescue |
| SB | 3-pos (R shoulder) | RATE | Rate profile select | Rate 1 / Rate 2 / Rate 3 |
| SH | momentary (R shoulder) | BUZZ | Lost-model buzzer | Press = beep |
| SC | 3-pos (front-left) | VTX | VTX power (optional; see note) | 25 / 200 / 800 mW |
| SF, SG | — | — | Spare | — |

**Rate profile and A2 low-speed mode:** on Pro, Rate 1 is the calibrated EASA
A2 low-speed profile (≤ 4.8 m/s) — selecting Rate 1 puts the aircraft in
regulatory low-speed mode. Rate 2 is standard, Rate 3 is sport. On SCRAP
(A1 sub-250 g, no A2 obligation), Rate 1/2/3 are plain rate profiles with no
regulatory role. See [[betaflight-profiles]].

**VTX power:** on both Pro and SCRAP, VTX power is normally set once per session
and rarely changed in flight. It can be left in the HDZero OSD menu and SC kept
spare, or mapped to SC if in-flight switching is wanted. The default is OSD-set,
switch spare — fewer live controls means fewer things to hit by accident.

### Pro vs SCRAP — same map, fewer active switches on SCRAP

| Switch | Pro | SCRAP |
|---|---|---|
| SA — ARM | ✓ | ✓ |
| SD — MODE (Angle/Acro) | ✓ | ✓ |
| SE — GPS Rescue | ✓ | unused (no GPS) |
| SB — RATE | ✓ | ✓ |
| SH — BUZZ | ✓ | ✓ |

SCRAP has no GPS, so SE is simply inactive — a new pilot on the trainer
literally cannot trigger the dangerous autonomous-return mode, because the
hardware for it is not present. Same physical map, fewer live controls on the
learning platform.

### ELRS module settings

| Parameter | Value |
|---|---|
| Frequency | 2.4 GHz |
| Regulatory domain | LBT (EU) |
| Packet rate | 250 Hz |
| Telemetry ratio | 1:16 |
| Switch mode | Wide |
| Model Match | OFF |
| Dynamic Power | ON |
| Min Power | 10 mW |
| Max Power | 100 mW (LBT limit) |

### EdgeTX model setup sequence

1. Create new model: Model Setup → Name: `libdrone`
2. Internal RF: ELRS, 250 Hz, LBT regulatory domain
3. Channel order: AETR
4. Mixes: standard AETR on CH1–CH4 (no mixing required)
5. CH5–CH9: assign switches per the table above
   - CH5 (ARM): SA 2-position
   - CH6 (MODE): SD 2-position
   - CH7 (RESC): SE 2-position (Pro only; leave assigned but inactive on SCRAP)
   - CH8 (RATE): SB 3-position
   - CH9 (BUZZ): SH momentary
   - CH10 (VTX): SC 3-position — optional; omit if VTX power is OSD-set
6. Telemetry: enable RSSI and Bat sensor display on the main screen
7. Bind receiver: hold the bind button on the receiver while powering on →
   TX16S → ELRS menu → Bind

### Arm switch safety

The ARM switch (SA) must be configured so the aircraft cannot arm accidentally.
In EdgeTX, set SA as a logical switch combined with a throttle-low condition:
the aircraft only arms when SA is down AND throttle is below 5%. This prevents
arming mid-air if SA is moved unintentionally. Disarm is never gated — it must
always be available as the emergency stop.

In Betaflight Configurator → Modes tab: set ARM mode to the SA channel with the
appropriate range.

### GPS Rescue switch margin (Pro)

To widen the accidental-actuation margin on the isolated Rescue switch, set the
SE range in Betaflight narrow and on the position furthest from rest, so partial
or glancing movement does not cross the activation threshold. Rescue should
require a full, deliberate flip.

---

## Procedure

### Verifying the model after setup

1. Connect the TX16S to EdgeTX Companion (optional, for backup).
2. Power on the TX16S with the aircraft connected to Betaflight Configurator.
3. Go to the Receiver tab in Betaflight. Move each stick and verify the correct
   channel responds in the correct direction.
4. Flip each switch and verify the correct channel changes in the Betaflight
   Receiver tab.
5. Arm the aircraft (throttle low, SA down) and verify the ARM indicator
   appears in the Betaflight status bar. Confirm that raising throttle first
   then moving SA does NOT arm.
6. Verify GPS Rescue trigger (Pro): flip SE → Betaflight should log a mode
   change to GPS Rescue in the status bar. Confirm SD (mode) has no Rescue
   position.

---

## Rationale

### Why arm is on SA, not a front switch

Arm belongs on a two-position shoulder switch with a firm detent, not a
three-position or front-face switch. Shoulder toggles have unambiguous up/down
feel and sit where the left thumb naturally rests, so the pilot can confirm arm
state without looking — and, critically, they are hard to brush accidentally
while reaching for a stick. Front switches (SC, SF) are far easier to catch with
a moving finger, which is exactly why no flight-critical function is placed
there. SA arm is also the near-universal Betaflight convention, so the map
matches muscle memory built on any other Betaflight aircraft.

### Why GPS Rescue is isolated, not in the mode ladder

The intuitive design puts Angle / Acro / GPS-Rescue as three detents on one
flight-mode switch. That design is rejected because it places a dangerous
function one accidental nudge away during a focused flight: a single mis-touch
could drop the aircraft into Acro when the pilot is not ready, or trigger an
autonomous return the pilot must then fight. Isolating Rescue on its own
switch (SE) means actuating it is always deliberate and never a side-effect of
changing mode or rate. The flight-mode switch (SD) is reduced to two states,
both of which are flyable, so a mis-touch there is recoverable rather than
dangerous.

### Why Wide switch mode and not Hybrid

ELRS Wide switch mode allocates 12 bits to a subset of switches per packet,
cycling through all switches over multiple packets. Hybrid mode allocates all
switch bits per packet but at reduced per-switch resolution. For libdrone, Wide
mode is preferred because the ARM switch gets full 2-position resolution on
every packet — the arm state is never delayed by the cycling schedule. Switch
latency is imperceptible for any non-safety-critical switch; the arm switch is
the one where latency matters most, and Wide mode prioritises it.

---

## Connections

requires: []
related:
  - [[betaflight-setup]]
  - [[betaflight-profiles]]
  - [[betaflight-gps-rescue]]
leads_to:
  - [[betaflight-setup]]
