---
id: piloting-progression
title: "Piloting progression"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - piloting-operations
personas:
  - 2.operator
  - 4.workshop
  - 5.student
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Drone piloting follows a repeatable progression from hover stability through
basic manoeuvres, orientation reversal, precision, and emergency scenarios.
Each phase builds on the previous — attempting precision flying before
orientation is mastered produces bad habits that are harder to unlearn than
to avoid. The most common beginner mistake is not hovering too long, but
progressing too quickly. For libdrone specifically, a second important
milestone is understanding FPV orientation — flying from first-person view
in a drone rather than line-of-sight is a separate skill requiring its own
deliberate practice.

---

## Concept

### Why progression matters

Flying skill is built from reflex-level responses that only become reliable
through repetition at each stage. Attempting complex manoeuvres before the
underlying skills are reflexive produces a pilot who can execute the manoeuvre
in good conditions but fails when conditions degrade. Each phase of the
progression trains a specific sensorimotor pattern to automatic level before
the next phase is introduced.

### Phase 1 — Hover stability

Learn to hold a stable hover at 1.5–2 m altitude in calm conditions. Focus
on one axis at a time: altitude first, then yaw, then lateral. Understand
drone inertia — a moving drone does not stop instantly; it must be actively
decelerated. The most common Phase 1 error is over-correction: the pilot
applies a correction, the drone moves, the pilot overcorrects in the other
direction. The cure is small inputs and patience, not larger corrections.

### Phase 2 — Basic manoeuvres

Controlled ascent and descent (always at an angle, never straight down in
calm air — VRS avoidance habit). Slow forward, backward, and lateral
translation. Turning while maintaining altitude. Goal: the pilot can move
the drone to a specific point and stop it there without significant overshoot.

### Phase 3 — Orientation reversal

When the drone is nose-toward-the-pilot, all horizontal controls are reversed:
pushing the roll stick right moves the drone to the pilot's left (the drone's
right). This is the most common cause of crashes for intermediate pilots flying
beyond a comfortable distance.

The milestone: the pilot can fly a figure-eight circuit at a comfortable
altitude without pausing to mentally translate controls. This should become
reflexive before any mission flying begins.

### Phase 4 — FPV orientation

Flying from first-person view via the HDZero goggles is a separate orientation
challenge. In FPV, the pilot's frame of reference is always the drone's nose-
forward perspective. There is no visual cue from the drone's physical position
relative to the pilot. Loss of video (link dropout, obstruction) is an
emergency — the pilot must immediately look up from the goggles and locate
the drone visually (VLOS requirement).

Practice: begin FPV flying in large open areas at comfortable altitude and
distance. Establish the habit of always knowing where the drone is in real
space, not only in the video feed. The HDZero Goggle 2 DVR (digital video
recording) can be used to review FPV footage and identify disorientation
patterns.

### Phase 5 — Emergency scenarios

Practice the following responses until they are reflexive:
- **Link loss**: how does the drone behave? (GPS Rescue activates) Where is
  the home point? Is the return altitude appropriate?
- **Low battery**: what does the OSD show? What is the landing priority?
- **GPS loss**: the drone transitions to angle mode. What corrective inputs
  are needed?
- **Video loss**: look up immediately. Find the drone visually. Land.

---

## Reference

### Progression milestones

| Phase | Milestone | Test |
|---|---|---|
| 1 | Stable hover | Hold position ±0.5 m for 30 s without correction after initial placement |
| 2 | Basic manoeuvres | Fly to a target 5 m away and land within 0.5 m |
| 3 | Orientation | Complete a figure-eight without pausing to translate controls |
| 4 | FPV orientation | Complete a circuit at 30+ m distance without VLOS support needed |
| 5 | Emergencies | Simulate link loss: GPS Rescue activates and returns to home correctly |

### Time to proficiency (estimated)

| Phase | Typical sessions (30 min each) |
|---|---|
| 1 — Hover | 2–3 sessions |
| 2 — Basic manoeuvres | 3–5 sessions |
| 3 — Orientation reversal | 5–10 sessions |
| 4 — FPV orientation | 5–10 sessions |
| 5 — Emergency scenarios | 2–3 sessions |

These are estimates for a motivated adult with no prior RC experience. Flight
simulation software (e.g. Liftoff, Velocidrone) accelerates Phase 1–3 significantly.

---

## Procedure

### First FPV session

1. Fly without goggles first. Establish VLOS position awareness.
2. Put goggles on. Keep flights short (< 30 s) and close (< 20 m).
3. After each short FPV segment: remove goggles, verify drone location visually.
4. Gradually extend duration and distance as confidence builds.
5. Always have a spotter available during Phase 4 training — VLOS
   is a regulatory requirement and a safety net.

---

## Rationale

### Why FPV orientation is a separate phase

Many pilots believe that flying FPV is simply "flying with a better view."
It is actually a different sensorimotor skill. The visual frame of reference
changes. Spatial awareness of the drone's position in the physical world must
be maintained in parallel with the FPV view. Video latency (even 4–8 ms for
HDZero) affects timing. Video blackout is a new failure mode that does not
exist in VLOS flying. Treating FPV orientation as a separate phase with
deliberate practice prevents the development of VLOS-only pilots who are
unsafe in FPV but proceed anyway because they can fly the easy phases.

---

## Connections

requires:
  - [[flight-modes]]
  - [[inertia-and-stopping]]
  - [[vortex-ring-state]]
related:
  - [[betaflight-gps-rescue]]
  - [[pre-flight-check]]
leads_to:
  - [[piloting-operations]]
  - [[scheduled-maintenance]]
