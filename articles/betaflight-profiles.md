---
id: betaflight-profiles
title: "Betaflight profiles and modes"
version: 2.1.0
date: 2026-06-01
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
  - core
  - pro
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

libdrone uses Betaflight PID profiles and rate profiles selected together by
the SB rate switch, giving three flight states: training/low-speed, normal, and
sport. Position 1 links a throttle-capped PID profile with soft rates — a gentle,
forgiving mode for learning to fly and for any operation where a lower top speed
is wanted. Because the throttle cap and the soft rates switch together, "position
1" means slow-and-calm on every aircraft. Switching is instant in flight with no
reboot. A low top speed can also matter for regulatory reasons depending on how
and where you fly — whether it does is a question for [[legal-and-regulatory]];
this atom covers only the mechanism.

---

## Concept

### PID profiles vs rate profiles, and why they are linked

Betaflight separates two independently switchable configuration sets:

**PID profiles** (up to 3) store PID gains, filter settings, and throttle
limiting. The throttle limit is what caps maximum speed — a rate profile cannot
do this.

**Rate profiles** (up to 3) store stick sensitivity (rates, expo, RC
smoothing). They change how twitchy or gentle the sticks feel, but they do
**not** cap speed.

A beginner "calm" mode needs *both* at once: a throttle cap so full stick does
not rocket the aircraft away, and soft rates so stick inputs are forgiving.
libdrone therefore **links** the two: selecting the
rate-switch position also selects the matching PID profile, so one switch
movement changes both together. This is configured in Betaflight so that rate
profile and PID profile track each other.

> Important: the throttle cap (speed limit) lives in the PID profile, not the
> rate profile. If the profile link is misconfigured, the rates will soften but
> the speed will NOT be capped. The worst case is "training mode is faster than
> expected" — verify the link on the bench (see Procedure). If you are relying on
> a speed ceiling for a regulatory reason, the requirement and whether it applies
> is a matter for [[legal-and-regulatory]]; do not assume this mechanism makes any
> operation legal.

### The three SB positions

| SB position | SCRAP (learning) | Pro |
|---|---|---|
| 1 | **Training** — throttle cap ~55–60 % + soft rates | **Low-speed** — throttle cap (calibrate to a target if one is needed) + soft rates |
| 2 | **Normal** — full throttle, standard rates | **Normal** — full throttle, standard rates |
| 3 | Spare (copy of 2 for now; "sport" later) | Sport — full throttle, higher rates |

As a first-time pilot you should spend your entire early sessions in **position
1**, in **Angle mode** (SD up). Move to position 2 only once hovering and basic
manoeuvres are comfortable. Position 3 is for much later.

### Low-speed / training mechanism (PID Profile 2)

The cap is `THROTTLE_LIMIT_TYPE SCALE` with `THROTTLE_LIMIT_PERCENT`. The sticks
still reach 100 % of their range, but actual motor output is scaled down. This
is a simple, zero-latency mechanical cap that holds regardless of GPS or FC
state — if GPS is lost, the cap remains.

**For SCRAP (training):** start at `throttle_limit_percent = 55`. There is no
target speed to calibrate to — pick a value that feels controllable and lower it
if the aircraft still gets away from you. This is about learning, not a number.

**For Pro (calibrated speed ceiling):** if an operation requires a specific
maximum ground speed, calibrate the cap so peak GPS speed stays a clear margin
below that target. Fly a straight pass at full throttle in calm conditions, read
peak GPS speed, and adjust. The calibrated value varies with battery charge,
payload weight, and conditions — calibrate on the day and document the value with
the payload weight used. Whether such a speed limit is required for your
operation is a question for [[legal-and-regulatory]], not an assumption to make
here. See [[throttle-limiting]] for the full mechanism.

### Angle mode for beginners (SD)

The SD switch selects flight mode: **Angle (up)** self-levels — release the
sticks and the aircraft returns to level. **Acro (down)** does not self-level
and holds whatever attitude you set. A first-time pilot should learn in Angle:
it is far more forgiving and lets you focus on position and altitude before
adding attitude control. Angle mode requires the accelerometer enabled in
Betaflight (it is on by default). Move to Acro only deliberately, much later in
the [[piloting-progression]].

---

## Reference

### PID Profile 2 — throttle cap overlay

Apply on top of the base configuration. Paste in CLI:

    profile 2
    set throttle_limit_type = SCALE
    set throttle_limit_percent = 55
    save

SCRAP: 55 % is a sensible training start; lower if needed.
Pro: calibrate to GPS speed ≤ 4.8 m/s (see Procedure), then save the value.

### Linking the PID profile to the rate switch

Configure Betaflight so rate-profile selection also selects the matching PID
profile, so the SB switch moves both together. Verify the link on the bench
before flying — the cap must follow the switch, not just the rates.

### Rate profile starting values

    # Rate profile 1 — training / low-speed (soft, forgiving)
    rateprofile 1
    set roll_rc_rate = 70
    set pitch_rc_rate = 70
    set yaw_rc_rate = 70
    set roll_expo = 25
    set pitch_expo = 25
    set yaw_expo = 20

    # Rate profile 2 — normal
    rateprofile 2
    set roll_rc_rate = 90
    set pitch_rc_rate = 90
    set yaw_rc_rate = 80
    set roll_expo = 15
    set pitch_expo = 15
    set yaw_expo = 10

Rate profile 1 uses lower rc_rate and higher expo than profile 2 — both make
stick response gentler around centre, which is what a learning pilot wants.

---

## Procedure

### Verifying the profile link on the bench (props off)

1. Connect to Betaflight Configurator, battery connected, **props removed**.
2. Set SB to position 1. Confirm the active PID profile is 2 and the active
   rate profile is 1 (shown in Configurator).
3. Set SB to position 2. Confirm PID profile and rate profile both change to
   the normal pair. If only the rates change and the PID profile does not, the
   link is not configured — fix before flying.
4. In position 1, briefly run the motors up (still props off) and confirm in
   the Motors tab that output is capped below the position-2 maximum.

### Calibrating the cap for the day (Pro, if a speed target applies)

1. Select SB position 1 (low-speed).
2. Fly outdoors in calm conditions. Make a straight horizontal pass at full
   throttle away from the pilot.
3. Note peak GPS speed from OSD or post-flight Blackbox.
4. If peak speed > your target: reduce `throttle_limit_percent` by 5.
5. If peak speed is well under target: increase by 5.
6. Repeat until peak speed sits a clear margin below the target. Save in Profile 2
   and document the value with the payload weight used.

### Switching in flight

The SB position can be changed at any time; the new profile pair takes effect
immediately with no glitch or reboot. Verify the active position before arming —
configure the profile number as an OSD element so it is visible in the goggles.

---

## Rationale

### Why training and speed-ceiling are the same switch position

A beginner needs a slow, forgiving mode to learn in. Some operations need a
speed-capped mode for operational or regulatory reasons. Both are the same
mechanism — a throttle cap plus soft rates — so libdrone makes them the same
switch position rather than two separate controls. The pilot learns "position 1
= slow and calm" on SCRAP as a first-time flyer, and that exact habit carries
straight to Pro. One muscle memory serves both the learning curve and any
later speed-limited operation. Whether a given operation requires a speed limit
is a regulatory question — see [[legal-and-regulatory]].

### Why throttle scale rather than GPS-based speed limiting

Betaflight does not implement GPS-based speed limiting in standard operation —
GPS speed feedback would need an outer loop at the GPS update rate (10 Hz),
incompatible with tight PID timing. Throttle scale is a simple, reliable,
zero-latency cap that guarantees motor output cannot exceed the set level
regardless of GPS or FC state. It is fail-safe: if GPS is lost, the cap remains
active.

---

## Connections

requires:
  - [[betaflight-setup]]
related:
  - [[edgetx-model]]
  - [[betaflight-gps-rescue]]
  - [[lipo-batteries]]
  - [[pid-proportional-term]]
  - [[throttle-limiting]]
  - [[legal-and-regulatory]]
  - [[piloting-progression]]
leads_to:
  - [[betaflight-gps-rescue]]
  - [[throttle-limiting]]


[legal-and-regulatory]: legal-and-regulatory.md "Legal and regulatory (single source of truth)"
[throttle-limiting]: throttle-limiting.md "Throttle limiting"
[piloting-progression]: piloting-progression.md "Piloting progression"


[legal-and-regulatory]: legal-and-regulatory.md "Legal and regulatory (single source of truth)"
[throttle-limiting]: throttle-limiting.md "Throttle limiting"
[piloting-progression]: piloting-progression.md "Piloting progression"

[betaflight-setup]: betaflight-setup.md "Betaflight setup"
[edgetx-model]: edgetx-model.md "EdgeTX model configuration"
[betaflight-gps-rescue]: betaflight-gps-rescue.md "Betaflight GPS Rescue"
[lipo-batteries]: lipo-batteries.md "LiPo batteries"
[pid-proportional-term]: pid-proportional-term.md "PID — proportional term"


[legal-and-regulatory]: legal-and-regulatory.md "Legal and regulatory (single source of truth)"
[throttle-limiting]: throttle-limiting.md "Throttle limiting"
[piloting-progression]: piloting-progression.md "Piloting progression"
