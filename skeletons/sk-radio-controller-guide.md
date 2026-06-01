---
id: sk-radio-controller-guide
title: "Radio Controller Guide"
version: 1.2.0
date: 2026-05-31
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 1.builder
  - 4.workshop
  - 5.student
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

After reading this guide, the builder understands the complete radio control
chain from transmitter stick movement to motor response, can configure the
TX16S for libdrone, understands ELRS link mechanics and why it outperforms
legacy RC protocols, and has established pre-flight radio habits that prevent
the most common pilot-induced failures. This is the 3.0.0 replacement for
the V2.4.6 Radio Controller document.

---

## Concept

### The control chain: hands to motors

Understanding the entire chain prevents a class of debugging failures where
the problem is at one layer but the symptom appears at another.

1. **Physical input**: TX16S stick or switch moves → hardware potentiometer
   changes voltage → ADC converts to digital value
2. **EdgeTX processing**: digital value mapped to channel output (CH1–CH16)
   per the model's mixer definition
3. **ELRS transmission**: 16 channels packed into a Chirp Spread
   Spectrum packet, transmitted at 250 Hz on 2.4 GHz
4. **ELRS receiver**: RP2 demodulates, reconstructs the 16 channels
5. **CRSF serial**: RP2 forwards channels to FC via CRSF protocol at
   420,000 baud on UART3
6. **Betaflight**: maps CRSF channels to AETR + AUX switches, applies to
   PID loop and flight mode logic
7. **DShot**: PID output → motor mixer → DShot600 command to ESC → motor RPM

A stick input that doesn't reach the motors always has its root in one
specific layer. → [[crsf-protocol]] and → [[elrs-protocol]] cover layers 3–5.
→ [[betaflight-setup]] covers layers 6–7.

### The TX16S and EdgeTX

The RadioMaster TX16S MKII MAX AG01 ELRS is the specified transmitter.
→ [[edgetx-model]] covers the complete model configuration for libdrone:
channel order (AETR), the arm/mode/rate/rescue switch map, ELRS settings
(250 Hz LBT), and the ELRS Backpack configuration for goggle video link.

EdgeTX is the open-source firmware running on the TX16S. Unlike its
predecessors (OpenTX, frSky TX firmware), EdgeTX has no manufacturer
lock-in — it runs on any compatible transmitter hardware, and your models
are yours unconditionally. → [[foss-stack-libdrone]] covers the EdgeTX
licensing context.

Key EdgeTX concepts for new builders:
- **Model**: a named configuration for one aircraft. The TX16S stores many models.
  Switching between them physically changes all switch assignments, rates, and mixes.
- **Mixer**: defines what each stick/switch contributes to each channel output.
  The libdrone model uses a standard 4-channel mixer (AETR) with additional
  AUX channels mapped to switches.
- **Logical switches**: EdgeTX allows conditional logic — for example, an alarm
  that triggers if battery voltage drops below a threshold.

### ELRS — why it matters

→ [[elrs-protocol]] covers the technical depth. The key points for operators:

**Chirp Spread Spectrum (CSS)**: ELRS doesn't transmit on a single frequency —
it sweeps across the 2.4 GHz band in a defined pattern. This provides two
advantages: resistance to narrowband interference (a jammer on one frequency
doesn't block the whole link), and processing gain that allows reception
even when the signal is below the ambient noise floor. This is why ELRS
provides reliable range in urban RF environments where legacy protocols degrade.

**250 Hz at LBT**: the libdrone configuration uses 250 Hz packet rate in
Listen-Before-Talk mode. LBT is the EU regulatory compliance mode — the
transmitter checks the channel is clear before transmitting. At 250 Hz, a
new control packet arrives every 4ms — fast enough for both racing and
precision mapping work.

**Dynamic power**: ELRS adjusts transmitter power based on link quality.
At close range it runs at 10 mW; as distance increases it steps up to
100 mW or beyond. This conserves TX battery and reduces RF signature at
close range — relevant to the OPSEC considerations in → [[operational-security]].

### Betaflight channel mapping

→ [[betaflight-setup]] contains the full channel assignment table. The mapping
that causes the most first-time confusion:

- CH1 = Roll (right stick left/right on Mode 2)
- CH2 = Pitch (right stick up/down)
- CH3 = Throttle (left stick up/down)
- CH4 = Yaw (left stick left/right)

**Critically**: "AETR" in EdgeTX means Aileron/Elevator/Throttle/Rudder on
CH1/2/3/4 respectively. Betaflight by default expects AETR. If channels are
mapped differently (TAER is common), the drone will attempt to yaw when you
push throttle. Verify the Receiver tab in Betaflight before arming: move each
stick and confirm only the expected channel moves.

### Switch assignments and their operational logic

→ [[edgetx-model]] has the full switch map and the safety reasoning behind it.
The map is organised so that dangerous functions are isolated and need a
deliberate reach, while recoverable functions get convenient placement. The
same map serves Pro and SCRAP — SCRAP simply leaves the GPS-dependent switch
unused.

**SA (2-position) — ARM.** Down = armed, up = disarmed. A firm left-shoulder
toggle that is hard to brush by accident, and arming is gated on throttle being
low, so the aircraft cannot arm in flight even if SA is moved. Disarm is never
gated — it is the emergency stop and must always be available.

**SD (2-position) — FLIGHT MODE.** Up = Angle (self-levelling, the beginner
mode), down = Acro. Only two states, both flyable, so a mis-touch is
recoverable. There is deliberately no GPS Rescue position here.

**SE (2-position) — GPS RESCUE (Pro only).** Isolated on its own switch so
triggering it is always deliberate, never a side-effect of changing mode or
rate. On SCRAP there is no GPS, so this switch is inactive.

**SB (3-position) — RATE / SPEED.** Position 1 = training/low-speed (throttle
capped + soft rates), 2 = normal, 3 = sport. On SCRAP position 1 is the beginner
training mode; on Pro it is also the EASA A2 low-speed compliance mode. See
→ [[betaflight-profiles]].

**SH (momentary) — BUZZER.** Press to activate the lost-model buzzer. Spring-
return, so it cannot latch into a bad state.

### Pre-flight radio habits

The habits that prevent the most common pilot-induced accidents:

1. **Transmitter on before battery.** Always. The receiver must acquire
   the RC link before arming is possible — if battery connects first, the
   drone may briefly respond to noise. → [[power-sequencing]] explains the
   electrical reason.

2. **Verify ARM switch before throttle.** Before any throttle input, confirm
   the SA switch is in the disarmed (up) position. A drone that arms with
   throttle already applied will launch immediately.

3. **Stick check in Receiver tab before outdoor arming.** Confirm channels
   respond correctly and in the right direction. Takes 20 seconds; prevents
   an inverted-pitch incident.

4. **Check GPS satellite count before arming.** GPS Rescue is silently
   disabled if satellite count is below the threshold at arm time. If GPS
   Rescue is not available and you lose RC link, there is no autonomous
   return. → [[betaflight-gps-rescue]] covers the satellite count gate.

### Simulator practice

Every new pilot should practice in a simulator before first flight. The
muscle memory for stabilisation — the reflexive correction for unexpected
drift — develops in the simulator at zero cost. Two crashes in simulation
are worth more than one in reality.

Recommended: Velocidrone or Liftoff using the TX16S over USB. The TX16S
appears as a generic USB joystick — configure the simulator to match the
libdrone channel mapping (AETR, Mode 2).

---

## Reference

### Quick reference: TX16S → Betaflight channel map

| Channel | TX16S input | Betaflight function |
|---|---|---|
| CH1 | Right stick L/R | Roll |
| CH2 | Right stick U/D | Pitch |
| CH3 | Left stick U/D | Throttle |
| CH4 | Left stick L/R | Yaw |
| CH5 | SA (2-pos) | Arm (throttle-low gated) |
| CH6 | SD (2-pos) | Flight mode (Angle / Acro) |
| CH7 | SE (2-pos) | GPS Rescue (Pro only) |
| CH8 | SB (3-pos) | Rate / speed profile |
| CH9 | SH (momentary) | Buzzer |

---

## Procedure

### Binding a new RP2 receiver

1. Put RP2 into bind mode: hold bind button on boot (or via Betaflight CLI)
2. On TX16S, open the ELRS Lua script → enter bind mode
3. Confirm: RP2 LED turns solid green (linked)
4. Set bind phrase in ELRS Lua to match your TX16S bind phrase
5. Verify link in Betaflight Receiver tab: move sticks, confirm channels respond

---

## Rationale

The V2.4.6 Radio Controller document (743 lines) covered TX16S hardware,
ELRS theory, channel mapping, and pre-flight habits in depth appropriate for
a student building their first drone. This skeleton retains that narrative
depth while delegating specifications to atoms (→ [[elrs-protocol]],
→ [[crsf-protocol]], → [[edgetx-model]]) so version-specific configuration
details have a single maintainable home.

---

## Connections

requires: []
related:
  - [[sk-complete-build-guide]]
  - [[sk-electronics-deep-dive]]
leads_to:
  - [[sk-complete-build-guide]]
