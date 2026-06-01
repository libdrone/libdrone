---
id: emergency-procedures
title: "Emergency procedures"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - piloting-operations
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

Emergency procedures are practiced responses to the three most likely in-flight
failures: RC link loss, video loss, and low battery. Each has a defined
response sequence. The critical insight is that emergency procedures only work
if they are practiced before an emergency — a pilot encountering GPS Rescue for
the first time in an uncontrolled situation will not respond correctly. Every
emergency procedure in this article should be practiced deliberately during
normal flying before it is ever needed under pressure.

---

## Concept

### The hierarchy of emergencies

Not all emergencies require the same response. Priority sequence:

1. **Safety first**: people and the drone are separated. If the drone is
   approaching people and is not under control — disarm. The drone is
   replaceable. People are not.
2. **Control before correction**: regain control before diagnosing. A pilot
   who is diagnosing a problem while the drone is drifting into an obstacle
   is making the situation worse.
3. **Know when to let GPS Rescue run**: a pilot who fights GPS Rescue —
   applying opposing stick inputs — will override the rescue and cause a
   crash. If GPS Rescue activates and the drone is returning correctly,
   let it run.

### Practice over procedure

Emergency procedures read as simple. Executing them correctly under stress is
different. The corrective reflex — "the drone is moving right, so I push left"
— does not degrade under stress because it is automatic. The analytical
reflex — "GPS lock has dropped, I should switch to angle mode and orient
manually" — requires conscious processing that stress degrades.

Practices recommended before relying on these procedures in the field:
- Fly a complete GPS Rescue cycle deliberately at low altitude over a known
  clear area
- Practice identifying drone orientation at 30m distance in different lighting
- Practice a forced landing on a specific target from 20m altitude

---

## Reference

### RC link loss

**What happens:** the ELRS link drops for longer than the failsafe delay (1s
default). Betaflight activates GPS Rescue automatically.

**GPS Rescue is running correctly:**
1. Do not apply opposing stick inputs — this overrides GPS Rescue and
   disables it
2. Watch the drone return. It should climb to rescue altitude, orient toward
   home, fly home, and descend
3. When the drone is within 5m of the home point, be ready to regain control
   as link recovers
4. If you regain link before the drone lands: flip SE switch to deactivate
   GPS Rescue manually if needed

**GPS Rescue is not behaving correctly (flying wrong direction, descending
in wrong location):**
1. Regain RC link if possible (move toward the drone, eliminate obstacles)
2. If link is regained: take manual control immediately
3. If link cannot be regained: GPS Rescue sanity checks will abort the rescue
   if it detects clearly wrong behaviour — the drone will disarm on impact
4. The outcome of a failed rescue is a crash. A crash is survivable for the
   drone. Stay calm.

**GPS was not acquired at arm time (< 8 sats):**
GPS Rescue is silently disabled. On link loss, the drone enters angle mode
and drifts with wind. If you observe this: regain link and fly home manually.
This is why the pre-flight satellite count gate is mandatory.

### Video loss

**What happens:** the HDZero link drops. Goggles show a frozen frame or black.

**Immediate response:**
1. Do not panic. Remove goggles immediately.
2. Locate the drone visually using eyes — VLOS is a regulatory requirement and
   a safety backstop for exactly this situation.
3. Fly back toward you using visual orientation only.
4. Land at the nearest clear area.

**If you cannot locate the drone visually:**
1. Listen for motor sound to locate approximate direction.
2. Reduce throttle slightly — the motor pitch will change, confirming audio
   is the drone.
3. Carefully fly toward the sound while scanning visually.
4. If still cannot locate: activate GPS Rescue manually (SE switch) to return
   to home.

**Prevention:** never fly FPV without confirming you can visually locate the
drone from your position first. Extend range only to the point where VLOS is
maintained.

### Low battery

**OSD shows battery warning (first warning voltage — 22.2V / 3.7V per cell):**
1. Begin returning to landing area immediately.
2. Do not extend the flight to "finish the pass."
3. Land within 2–3 minutes.

**OSD shows battery critical (minimum cell voltage — 21.6V / 3.6V per cell):**
1. Land immediately. Nearest clear area.
2. Do not prioritise reaching the designated landing spot — land now.
3. A LiPo discharged below 3.0V/cell is damaged. If the critical warning
   appears, you are already close to that threshold under load.

**In cold conditions (< 5°C):** the winter voltage thresholds are higher
(3.7V warning, 3.6V minimum). Cold cells sag faster and deeper under load.
Land earlier than the OSD warning if flying in cold — do not wait for the
first warning before beginning return.

### Fly-away (GPS malfunction or compass error)

**Signs:** drone flying in unexpected direction despite stick inputs, not
responding correctly to GPS Rescue.

**Response:**
1. Switch to angle mode (if not already) — removes GPS from the loop.
2. Use manual stick inputs to slow the drift and orient the drone toward you.
3. If fly-away continues and drone is approaching obstacles or people:
   disarm. Controlled crash is preferable to collision with a person.

---

## Procedure

### Emergency procedures practice session

Before relying on these procedures under pressure, schedule a practice
session in a large open area with no obstacles and no people other than
a safety observer:

1. GPS Rescue test: fly 50m out at 20m altitude, activate SE switch. Watch
   full return and observe behaviour. Regain control via SE switch release.
2. Video off test: cover goggles with hand while flying at 10m altitude 15m
   out. Locate drone visually, fly back by sight only. Land.
3. Low battery simulation: fly until first OSD warning appears. Practice
   calm return and landing without rushing.
4. Disarm drill: hover at 2m, disarm deliberately. The drone drops — this
   is expected. Practice the correct mental association: disarm = controlled
   crash = acceptable outcome.

---

## Rationale

### Why disarming is listed as an emergency option

Disarming in flight causes an immediate power-off crash. This is correct when
the alternative is an uncontrolled collision with a person. A drone crashing
from 10m altitude is dangerous but survivable for anyone below. A drone
colliding with a person at speed is more dangerous. When the only way to
protect a person is to disarm, disarm.

This is not a recommendation to disarm casually — it is the last resort when
all other options have failed or are unavailable.

---

## Connections

requires:
  - [[flight-modes]]
  - [[betaflight-gps-rescue]]
related:
  - [[pre-flight-check]]
  - [[piloting-progression]]
  - [[winter-protocol]]
leads_to:
  - [[piloting-progression]]
