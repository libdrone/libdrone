---
id: sk-scrap-build-guide
title: "SCRAP Build Guide"
version: 1.1.0
date: 2026-05-10
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
  - manufacturing
  - power-systems
  - frame-structure
  - software-stack
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

After following this guide, the builder has a flyable, Betaflight-configured
SCRAP quad with correct wiring, tested motor directions, and at least one
successful hover. Total active build time is approximately 4–6 hours. Total
elapsed time from ordering to first flight is approximately 3 weeks — primarily
waiting for AliExpress delivery, not active work. The 6sfull.cz components
arrive in 2–3 days and can be inspected immediately. The frame can be printed
the same evening the decision is made.

---

## Concept

### Read before you solder

The single most dangerous step in this build is connecting the HDZero ECO VTX
to the wrong power pad. The ECO VTX is rated 1S–3S (maximum ~12.6 V). A 4S
battery fully charged reads 16.8 V. Connecting VBAT directly to the VTX
destroys it instantly and permanently. It is not a recoverable mistake. The
VTX must be powered from the SpeedyBee's 5V BEC output — minimum 5V @ 2A,
which the SpeedyBee F405 Mini provides at 5V @ 3A. This note appears three
times in this guide. That is intentional.

### The five build phases

SCRAP breaks down into five phases: print, assemble, wire, configure, maiden.
Each phase has a hard gate — do not move to the next phase until the gate is
passed. Phase 3 (wiring) is where most first builds go wrong. Read
→ [[wire-gauge-selection]] before picking up a soldering iron.

---

## Phase 1 — Print the frame

Download the Whifflepick 3" V1 from Printables (model 1207344). Print in
PETG-CF on a 0.4 mm hardened steel nozzle. Use the 0.20 QUALITY or 0.20
BALANCED profile — 0.10 FAST DETAIL adds print time without structural benefit.

**Slicer settings — non-negotiable:**
- Perimeters: 3
- Top/bottom layers: 3
- Infill: 0%
- Supports: none
- Material: PETG-CF (0.4 mm hardened nozzle mandatory — PETG-CF is abrasive)

See → [[print-profiles]] for the full PETG-CF profile rationale. PETG without
CF reinforcement is not recommended — it is too soft under 4S motor loads.
PLA will delaminate on the first hard crash. PETG-CF is the minimum.

Print time at 0.20 is approximately 90–120 minutes. Store the filament in a
drybox during printing — PETG-CF absorbs moisture and prints poorly when damp.

**Gate:** Frame printed and post-inspected. Check motor mount holes for clean
geometry. The 20×20 stack mount area must be flat. Verify M3 hole diameters
accept bolts without force. If geometry is off, re-print — do not file.

---

## Phase 2 — Assemble the airframe

**You will need:** M3 standoffs (4×), M2 screws for motor mounts, M3 nylon
nuts or lock nuts for stack, threadlocker (medium, not high-strength).

### Motor installation

The EX1404 motors use a standard 9N12P 14×4 mm stator with 1.5 mm shaft.
Mount pattern fits the Whifflepick motor mount directly. Torque the M2 motor
screws to finger-tight plus a quarter turn — no more. The frame material at
motor mounts is the thinnest point; over-torquing cracks the mount. Use
medium threadlocker on all motor screws. Do not use high-strength threadlocker
— you will need to remove these motors after crashes.

**Motor direction for SCRAP (standard Betaflight quad layout):**
- Front-left: CCW (counter-clockwise)
- Front-right: CW (clockwise)
- Rear-left: CW
- Rear-right: CCW

Do not install props during assembly. Props go on last, after motor direction
is confirmed in Betaflight. See → [[motor-mixing]] for the physics behind
the layout.

### Stack installation

Install the SpeedyBee F405 Mini FC + ESC stack using M3 nylon standoffs.
Anti-vibration grommets are preferred if supplied — they reduce IMU noise.
Do not overtighten. The stack must be able to flex slightly on the standoffs.
The USB-C port must face a direction accessible from outside the frame with
props removed. Check access before bolting down.

---

## Phase 3 — Wiring

This is the critical phase. Read → [[wire-gauge-selection]] before starting.
Read the HDZero ECO VTX power warning above again.

### Wire selection

| Connection | AWG | Reason |
|---|---|---|
| Battery lead (XT30 to ESC) | 20 AWG | 35A ESC max, short run, XT30 rated 30A continuous |
| Motor phase wires | Pre-soldered (EX1404) | Match existing gauge on motor |
| VTX power (5V BEC to VTX) | 24 AWG | <0.5A current, short run |
| RX power and UART | 24–26 AWG | Signal line, <0.1A |
| Camera signal | Use supplied cable | ECO Bundle cable is pre-terminated |

See → [[wire-gauge-selection]] for the full current/gauge calculation methodology.
At SCRAP power levels (35A ESC maximum, 4S) the motor phase wires are the highest
current path. The EX1404 ships with phase wires pre-soldered at the correct gauge
— do not replace them with thinner wire.

### Soldering sequence

Solder in this order. Do not skip ahead.

**Step 1 — Motor phase wires to ESC**
Solder all four motors to the ESC pads. Polarity does not matter for brushless
motors — motor direction is changed in Betaflight (or by swapping any two phase
wires). Keep wire runs short — no more than 30 mm of exposed wire between motor
and ESC pad. See → [[brushless-motors]] for why motor direction polarity is
arbitrary on three-phase brushless.

**Step 2 — Battery lead**
Solder a short 20 AWG pigtail to the ESC battery pads with XT30 female connector.
Wire length from ESC pad to connector body: 40–60 mm. No longer. Every additional
centimetre of battery lead increases the parasitic inductance that causes voltage
spikes on hard throttle chops. See → [[capacitor-placement-emc]] for why this
matters. The ESC stack ships with a capacitor — verify it is soldered to the ESC
power pads, not on a wire pigtail. A capacitor on a pigtail is partially ineffective.

**Step 3 — VTX power (CRITICAL)**
Identify the 5V BEC output pad on the SpeedyBee F405 Mini FC. It is labelled 5V.
Do NOT use the pad labelled VBAT or VTX_PWR unless the SpeedyBee documentation
explicitly confirms that pad is voltage-regulated to 5V.

Solder 24 AWG red wire from FC 5V pad to HDZero ECO VTX power input.
Solder 24 AWG black wire from FC GND pad to HDZero ECO VTX GND.

**The ECO VTX is rated 1S–3S (maximum ~12.6 V). 4S fully charged = 16.8 V.
VBAT on 4S destroys the ECO VTX immediately. Power it from 5V BEC only.**

**Step 4 — VTX data**
The HDZero ECO uses a composite video signal — no MIPI cable. Connect the
video data wire from the ECO camera to the ECO VTX per the bundle's wiring
diagram. The elimination of the MIPI cable is the primary reason the ECO Bundle
was selected for SCRAP: the MIPI cable is fragile and difficult to resolder
after a crash. The composite signal interface survives crashes.

**Step 5 — ELRS receiver**
The EP1 Dual connects to the FC via UART. Solder to an available UART TX/RX
pad pair on the FC, plus 5V and GND. Note which UART number — you will need
it in Betaflight. The EP1 Dual includes two antennas; mount them at 90°
to each other for diversity. Route antenna leads away from motor phase wires.

See → [[elrs-protocol]] for UART vs SPI receiver distinction and why UART
is the correct choice for a repairable build. SPI receivers are not field-
updatable and are deprecated in Happymodel's own current product line.

### Post-solder inspection

Before any power-on: visually inspect every solder joint. Look for:
- Bridges between adjacent pads
- Cold joints (dull, granular surface)
- Wire insulation melted against the PCB
- Motor phase wires not fully tinned at the ESC pad

Do not power on until all joints pass visual inspection. See → [[electronics-installation]]
for the full pre-power inspection checklist used on Pro builds — the same criteria apply.

---

## Phase 4 — Betaflight configuration

Connect the SpeedyBee to Betaflight Configurator via USB-C. Do not connect
the battery until motor direction is confirmed in Betaflight with props off.

See → [[betaflight-setup]] for the full Betaflight configuration sequence. The
SCRAP-specific settings that differ from Pro:

**Ports tab:**
- Enable Serial RX on the UART where the EP1 is wired
- Enable HDZero on the UART wired to the ECO VTX (or use the dedicated VTX pad
  if the SpeedyBee provides one — check the FC pinout diagram)

**Configuration tab:**
- Receiver: Serial (CRSF/ELRS)
- Enable: Airmode, Anti-gravity
- Accelerometer: enable for self-levelling practice modes

**ESC/Motor tab:**
- Protocol: DSHOT300 (not PWM, not Oneshot)
- Enable DSHOT Bidirectional for RPM filter
- Motor spin direction: verify each motor individually using the Betaflight
  motor test (props off, motors spun one at a time, 3–5% throttle maximum)

**Motor direction verification:**
Spin each motor individually. Confirm rotation matches the standard layout
(CCW front-left and rear-right, CW front-right and rear-left). If a motor
spins the wrong way, use the motor tab direction toggle — do not swap phase
wires at this stage. See → [[motor-mixing]] for the layout rationale.

**Failsafe:**
Set to **Drop** (not Angle, not GPS Rescue). SCRAP has no GPS. Drop mode
disarms the motors immediately on signal loss. For practice flying near water
or obstacles, a drone that falls from 5 m height is recoverable. A drone that
continues flying without a pilot is not. See → [[emergency-procedures]] for
the broader failsafe design philosophy across the libdrone stack.

**Rates:**
Start with conservative rates. Betaflight defaults are appropriate. Do not
copy Pro rates to SCRAP — the Pro rates are tuned for a 330 mm 6S airframe.
On a 130 mm 4S quad, Pro rates will make SCRAP uncontrollable for a beginner.
After 5–10 hours of SCRAP flight time, adjust rates based on feel.
See → [[pid-tuning-rate-profile]] for the rate tuning methodology.

---

## Phase 5 — Props and maiden flight

### Simulator prerequisite

Do not skip this gate. A minimum of 10 hours in an FPV simulator (Velocidrone
or Liftoff) using the actual transmitter and goggles is the recommended threshold
before maiden flight. The simulator costs ~€15 and saves at least one crashed
drone. The TX16S connects via USB and works out of the box. HDZero Goggles 2
can be used in the simulator via HDMI input for full immersion. A pilot who
cannot fly a consistent circuit in the simulator will crash SCRAP on the first
battery. A pilot who can fly circuits in the simulator will crash SCRAP on
the third battery — which is a much better outcome. See → [[piloting-progression]]
for the full skill development arc.

**Gate:** 10+ simulator hours logged. Consistent circuits without binning every
30 seconds. Move to prop installation only after this gate is passed.

### Prop installation

**Install props last.** Verify motor direction in Betaflight before props are on.

HQProp T3X3X3 are polycarbonate 3-inch 3-blade props. The T prefix indicates
triblades. Shaft bore is 1.5 mm — matches the EX1404 1.5 mm shaft exactly.

Props must be installed in the correct rotation direction. Each prop is marked
CW or CCW. A CW prop on a CCW motor will generate lift in reverse and destabilise
the quad on arming. Match prop rotation to motor rotation confirmed in Betaflight.

Tighten to firm finger-tight plus one quarter turn. Self-locking prop nuts are
preferred. Do not use standard nuts without threadlocker — props must not loosen
in flight. A departing prop at 4S is a hazard.

### Pre-flight check

Before arming for the first time:
- Props installed, correct direction, no play on shaft
- Battery connector mated but not yet connected to board
- Check all motor screws are tight
- Check no loose wires that could enter a prop arc
- Visual check that VTX power is on 5V wire, not VBAT (one last time)
- Connect battery. Verify HDZero Goggles receive video from ECO VTX.
- Arm only after confirmed video link.

See → [[pre-flight-check]] for the full pre-flight procedure used on Pro builds.
The SCRAP version is shorter but the principle — gate on video, gate on signal,
never arm without confirmed telemetry — is identical.

### Maiden flight

Phase 1: hover at 0.5 m altitude in the practice space. No obstacles.
30 seconds. Land. Inspect all motor mounts for movement. Inspect all ESC
pads for heat. Feel each motor — warm is acceptable, hot is not. A hot motor
on a hover indicates wrong prop direction or mechanical binding. Identify and
resolve before proceeding.

Phase 2: slow circuits at low altitude. One obstacle at a time. No aggressive
manoeuvres until 5+ flights are completed. SCRAP is 4S — it has significantly
more authority than a 1S or 2S tinywhoop. The throttle response will be faster
than any simulator at default rates. Respect the gap between simulator muscle
memory and real-hardware behaviour.

See → [[maiden-flight]] for the measurement-first approach to maiden flights.
The principles apply to SCRAP even though the stakes are lower than Pro.
See → [[piloting-progression]] for the skill development arc from hover to
obstacle work.

---

## Failure modes and prevention

### ESC burnout
Cause: motor stall (crash with motor still powered), or motor bearing seizure.
Prevention: enable crash detection in Betaflight — it cuts motor output
immediately on impact detection. Also enable DSHOT Bidirectional — stalled
motor back-EMF is detectable. The SpeedyBee BLS 35A has no separate ESC board
that can be replaced; the FC/ESC stack is one unit. A burned ESC means
replacing the whole stack (~CZK 1,640). See → [[electronic-speed-controllers]].

### VTX failure
Cause: overvoltage from incorrect VBAT connection (see Phase 3 warning),
or impact damage. The ECO Bundle composite signal interface is significantly
more crash-resistant than MIPI-based systems. Impact damage is usually to
the camera mount, not the VTX board. A spare ECO Bundle costs CZK 1,769 from
6sfull.cz and ships in 2–3 days.

### Motor failure
Cause: bearing wear, ingested debris, hard crash. EX1404 motors have 1.5 mm
shafts — thinner than motors on larger builds and more susceptible to bending
on direct impacts. Two spare bundles of four were ordered with the build. A
motor replacement requires unsoldering three phase wires and resoldering. 15
minutes with a clean iron.

### Frame failure
Cause: hard crash, rock or hard surface impact on an arm. PETG-CF arms survive
grass and soil impacts well. Rock impacts at speed will crack the arm. Reprint
time: under two hours. Frame material cost: negligible. Keep the slicer profile
saved and the filament in the drybox.

### Loss of video
Cause: VTX or camera connector, or ECO VTX overheating. The ECO VTX has a
25 mW and 200 mW output mode. Use 25 mW for the practice space — it is
sufficient at the distances involved and generates less heat. If video cuts
out mid-flight, land immediately using line-of-sight. Do not attempt to fly
blind to recover video.

---

## Connections

requires:
  - [[scrap-variant]]
  - [[print-profiles]]
  - [[wire-gauge-selection]]
  - [[betaflight-setup]]
  - [[lipo-batteries]]
related:
  - [[electronic-speed-controllers]]
  - [[brushless-motors]]
  - [[motor-mixing]]
  - [[elrs-protocol]]
  - [[digital-fpv]]
  - [[electronics-installation]]
  - [[pre-flight-check]]
  - [[maiden-flight]]
  - [[piloting-progression]]
  - [[capacitor-placement-emc]]
  - [[pid-tuning-rate-profile]]
  - [[emergency-procedures]]
  - [[pccf]]
  - [[petg]]
leads_to:
  - [[betaflight-setup]]
  - [[maiden-flight]]
  - [[piloting-progression]]
  - [[core-variant]]
