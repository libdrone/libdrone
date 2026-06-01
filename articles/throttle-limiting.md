---
id: throttle-limiting
title: "Throttle limiting"
version: 2.0.0
date: 2026-06-01
author: jsa
status: released
scope: libdrone
topic:
  - software-stack
personas:
  - 2.operator
  - 1.builder
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Throttle limiting caps a drone's maximum speed by scaling the throttle range,
in Betaflight via `throttle_limit_type = SCALE` on a switchable rate profile.
On libdrone it serves two purposes: a gentle, forgiving mode for a first-time
pilot learning to fly, and a calibrated speed ceiling for any operation where a
maximum ground speed must be held. The cap is per-profile and transmitter-
switchable, so full-speed capability is preserved on another profile. This is
the first of a planned set of approachability and safety features that bring a
beginner-friendly flight envelope to an open platform; where a speed ceiling is
held for a regulatory reason, the regulatory question itself lives in
[[legal-and-regulatory]].

---

## Concept

### What throttle limiting does

Betaflight's `throttle_limit_type = SCALE` reduces the effective throttle range
from 0–100% to 0–N%, where N is the configured limit percentage. At full stick,
the motors receive only N% of their maximum PWM signal. `throttle_limit_percent`
sets N. The result is a lower top speed with the full stick range still usable —
the pilot uses the whole throttle travel, but the ceiling is lower, which makes
control finer and overshoot smaller.

The limit is profile-specific and switchable from the transmitter, so a single
aircraft carries both a capped mode and a full-speed mode and the pilot chooses
between them in flight. On libdrone this maps to the SB rate/speed switch (see
[[betaflight-profiles]]): position 1 = capped, higher positions = progressively
faster.

### Why it matters for a beginner

A capped top speed is the single most useful aid for a first-time pilot. It does
not change *how* the sticks respond, only how far the aircraft can get away
before the pilot reacts — which is exactly the margin a learner needs. Combined
with soft rates and self-levelling Angle mode, throttle limiting turns an
otherwise twitchy quad into something a novice can keep over a field. It is the
libdrone equivalent of the "beginner mode" on a commercial drone, achieved with
a single open Betaflight parameter rather than locked vendor firmware — and it is
the first entry in a planned set of approachability features in that spirit.

### What it does not guarantee

Throttle limiting is an operational tool, not a hard ceiling. Wind assistance,
dive angles, and motor differences can push actual ground speed above the
nominal cap. It reduces speed; it does not enforce an absolute limit, and it is
not a safety certification of any kind. Where a specific maximum speed must be
held for a regulatory reason, that requirement and whether it applies to your
operation is a matter for [[legal-and-regulatory]] — decide for yourself from the
single source of truth there; this atom only describes the mechanism.

---

## Reference

### Betaflight CLI (per profile)

    profile 2

    # Enable throttle scaling
    set throttle_limit_type = SCALE
    set throttle_limit_percent = 55   # starting point; tune to taste or target
    save

- Beginner / training start: ~55%, lower if the aircraft still gets away.
- For a measured speed target: calibrate against GPS ground speed (below).

### OSD

Enable the `gps_speed` OSD element to read real-time ground speed, and the
profile-name or number element to confirm which profile is active before flying.

### Transmitter mapping

Throttle limiting follows the rate/speed profile on the SB switch per
[[edgetx-model]] and [[betaflight-profiles]]: position 1 is the capped profile,
higher positions are uncapped or faster.

---

## Procedure

### Calibrating to a measured speed target

When a specific maximum ground speed must be held (confirm whether and why such a
requirement applies to your operation in [[legal-and-regulatory]]):

1. Enable GPS and the OSD ground-speed element.
2. In the capped profile, set `throttle_limit_percent` to a conservative start.
3. Fly a straight pass at full throttle in calm conditions (< 2 m/s wind);
   read peak GPS ground speed.
4. Adjust `throttle_limit_percent` by ±5 points and repeat until peak speed sits
   a clear margin below the target.
5. Confirm on three separate passes.
6. Record the value with battery cell count and prop size in the build log;
   recalibrate if either changes, or if payload weight changes.

---

## Rationale

A switchable rate-profile parameter was chosen over a dedicated flight mode or a
firmware modification because it needs no flight-controller code change — it is a
pure Betaflight parameter compatible with any Betaflight version, reversible from
the transmitter, and immediately visible to the pilot. GPS-based speed limiting
in firmware was rejected: it depends on features not present in standard
Betaflight releases and an outer GPS-rate loop incompatible with tight PID
timing, adding complexity without improving the operational result. Keeping the
mechanism this simple is also what lets it double as a beginner aid — there is
nothing to misconfigure beyond one percentage.

---

## Connections

requires:
  - [[betaflight-profiles]]
  - [[betaflight-setup]]
related:
  - [[edgetx-model]]
  - [[gnss-gps]]
  - [[legal-and-regulatory]]
leads_to:
  - [[betaflight-profiles]]
  - [[first-flight]]


[legal-and-regulatory]: legal-and-regulatory.md "Legal and regulatory (single source of truth)"
[betaflight-profiles]: betaflight-profiles.md "Betaflight profiles and modes"


[legal-and-regulatory]: legal-and-regulatory.md "Legal and regulatory (single source of truth)"
[betaflight-profiles]: betaflight-profiles.md "Betaflight profiles and modes"


[legal-and-regulatory]: legal-and-regulatory.md "Legal and regulatory (single source of truth)"
[betaflight-profiles]: betaflight-profiles.md "Betaflight profiles and modes"

[edgetx-model]: edgetx-model.md "EdgeTX model configuration"
[betaflight-setup]: betaflight-setup.md "Betaflight setup"
[gnss-gps]: gnss-gps.md "GNSS and GPS"
[first-flight]: first-flight.md "First flight"
