---
id: feed-forward-control
title: "Feed-forward control"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - control-systems
personas:
  - 5.student
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Feed-forward (FF) responds to the pilot's stick input rate directly, before
the drone has moved — it is anticipatory rather than reactive. When the pilot
pushes the roll stick, FF immediately generates a proportional motor correction
in anticipation of the commanded roll. This dramatically improves stick
responsiveness without increasing P gain. For libdrone's mapping role, FF
is set conservatively: the drone operates mostly in GPS-assisted modes with
slow, waypoint-driven commands rather than rapid manual inputs, so FF's
benefits are marginal and its sensitivity to stick noise is not desirable.

---

## Concept

### Reactive vs anticipatory control

PID control is inherently reactive: error must exist before any correction
is applied. This creates an irreducible delay:

1. Pilot commands a roll
2. Drone begins to deviate from commanded rate
3. Error builds up
4. P term detects error and begins correction
5. D term detects error rate and damps the correction

The delay between step 1 and step 5 is the latency of the reactive system.
On a well-tuned drone with a fast loop rate, this delay is small (a few
milliseconds) but perceptible as a slight softness in the stick response.

Feed-forward removes this delay for commanded inputs. It acts on the stick
input signal directly:

    FF_output = K_FF × d(setpoint)/dt

When the stick moves, FF generates a correction immediately — before the
gyro has registered any change. The drone begins correcting in the same
instant the pilot moves the stick.

### Why FF does not replace PID

FF only helps with commanded changes (stick movement). It does nothing for
external disturbances (wind gusts) because wind is not reflected in stick
input. PID continues to handle disturbances. FF and PID are complementary:
FF provides immediate response to intentional inputs, PID provides rejection
of unintentional disturbances.

FF also cannot correct itself if it overshoots — it applies a fixed correction
proportional to stick rate, regardless of whether the drone has actually moved.
If the correction is slightly wrong (due to aerodynamic conditions, different
battery voltage, different altitude), PID error correction compensates.

### FF and stick noise

FF amplifies the rate of change of stick position. If the transmitter signal
is noisy — rapid small fluctuations in the commanded rate — FF amplifies
these fluctuations into motor commands. On a high-quality transmitter like
the TX16S with ELRS at 250 Hz, stick signal is very clean and FF noise is
negligible. On a noisy or low-quality radio link, FF can introduce motor
buzz.

For libdrone, the dominant operational mode is GPS-commanded waypoint flight.
In this mode, stick position is usually fixed and FF sees near-zero stick rate.
FF only becomes significant during manual transitions between waypoints or
during manual positioning. Setting FF conservatively avoids any risk of
amplifying GPS-mode stick noise.

---

## Reference

### FF vs PID response comparison

| Input type | PID response | FF response |
|---|---|---|
| Wind gust (disturbance) | Detects error → corrects | No response (no stick movement) |
| Stick roll command | Detects rate error → corrects | Immediately generates correction |
| Slow stick movement | Normal PID correction | Small FF boost |
| Fast stick movement | May lag behind | Large FF correction, drone responds instantly |

### Betaflight FF settings for libdrone

| Mode | Recommended FF | Reason |
|---|---|---|
| GPS mapping mission | Low (30–50% of aggressive freestyle value) | Slow waypoint commands, no rapid manual inputs |
| Manual positioning | Moderate (50–70%) | Some manual inputs during setup and positioning |
| Manual rate mode | Not tested / not recommended | libdrone is not tuned for aggressive manual flight |

---

## Procedure

<!-- not applicable — detailed Betaflight FF configuration in software-stack domain -->

---

## Rationale

### Why FF is documented as a control-systems concept here and not just in software

FF is a general control system concept applicable to any closed-loop controller —
it is not specific to Betaflight or any firmware. Understanding what FF does at
the conceptual level (anticipatory vs reactive, stick input rate vs error) is
necessary before the Betaflight-specific implementation is meaningful. The
concept belongs here; the Betaflight sliders and recommended values belong
in the software-stack domain.

### Why libdrone does not maximise FF

A mapping drone optimised for stable, precise hovering at fixed positions gains
almost nothing from high FF. The primary performance demand is disturbance
rejection (wind rejection in position hold), which is PID's domain, not FF's.
High FF would improve the feel of manual stick inputs at the cost of potential
motor noise in GPS mode. The trade is not worth making for this mission profile.

---

## Connections

requires:
  - [[closed-loop-control]]
  - [[pid-proportional-term]]
related:
  - [[pid-derivative-term]]
  - [[pid-integral-term]]
leads_to:
  - [[rpm-filter]]


[closed-loop-control]: closed-loop-control.md "Closed-loop control"
[pid-proportional-term]: pid-proportional-term.md "PID — proportional term"
[pid-derivative-term]: pid-derivative-term.md "PID — derivative term"
[pid-integral-term]: pid-integral-term.md "PID — integral term"
[rpm-filter]: rpm-filter.md "RPM filter"
