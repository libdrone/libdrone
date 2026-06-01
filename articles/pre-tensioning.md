---
id: pre-tensioning
title: "Pre-tensioning"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: generic
topic:
  - manufacturing
personas:
  - 5.student
  - 1.builder
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Pre-tensioning is the deliberate introduction of compressive or tensile stress
into a joint before any operational load is applied. In libdrone's CF rod
and arm architecture, pre-tension is created by interference fit: the arm's
rod channel is designed slightly smaller than the rod diameter, so inserting
the rod deforms the channel slightly and loads the joint with clamping force
that exists before any propeller thrust or crash load arrives. This passive
pre-load increases joint stiffness, reduces micro-movement at the interface
under vibration, and extends fatigue life without adding mass.

---

## Concept

### Why joints are the problem

A structure fails where stress concentrates. In a drone frame, stress
concentrates at joints — the transitions between dissimilar materials, at
fasteners, and at the rod-arm interface. A joint under cyclic vibration
with no pre-load will develop micro-slip: the surfaces move fractionally
against each other under each vibration cycle. Micro-slip generates fretting
wear, transfers vibration through the structure rather than damping it,
and eventually loosens fasteners or cracks the printed material around the
bore.

Pre-tension eliminates micro-slip by ensuring the joint surfaces remain in
contact and under compressive load even when the vibration load would
otherwise separate them. The pre-load must exceed the maximum separation
force from operational loads for this to work.

### Interference fit in the CF rod channel

The arm rod channel in libdrone is designed with a bore diameter 0.1–0.15 mm
smaller than the CF rod nominal diameter. When the rod is pressed into the
channel, the printed material deforms elastically — PETG at its yield
boundary — generating a clamping force distributed around the rod
circumference. This force is the pre-tension.

The magnitude of pre-tension is controlled by the interference amount and the
Young's modulus of the printed material. PETG has a Young's modulus of
approximately 2 GPa — stiff enough to maintain meaningful clamping force,
compliant enough to be pressed in without cracking. PC-CF (used on Pro arms)
has a higher modulus and requires tighter interference tolerances to avoid
cracking during assembly.

### Pre-tension and vibration isolation

The floating motor mount on libdrone arms uses an O-ring that applies a
separate pre-tension to the motor interface. The O-ring's elastomeric pre-load
decouples the motor's vibration from the arm at frequencies above the O-ring's
natural frequency. This is a different mechanism from the rod channel
interference — the O-ring provides both pre-tension and vibration isolation,
where the rod channel interference provides pre-tension and stiffness only.
See → [[floating-motor-mounts]] and → [[vibration-isolation-theory]].

---

## Reference

| Interface | Pre-tension mechanism | Material |
|---|---|---|
| CF rod in arm channel | Interference fit (0.1–0.15 mm) | PETG or PC-CF arm |
| Motor in mount | O-ring radial pre-load | TPU O-ring |
| Sandwich bolt | Fastener torque pre-load | M3 steel bolt |
| Rod end in bumper | Interference fit | ASA bumper |

**Interference fit tolerances (libdrone V2.4.x):**
- Rod nominal diameter: 3.00 mm
- Arm channel bore: 2.85–2.90 mm
- Interference: 0.10–0.15 mm

---

## Procedure

### Verify pre-tension on rod insertion

1. Dry-fit the rod into the arm channel without adhesive. The rod should
   require finger pressure to insert but not require a mallet — if a mallet
   is needed, the interference is too tight; if the rod slides freely, it is
   too loose.
2. The rod should not rotate in the channel when the arm is held and
   a 0.5 N·m torque is applied to the rod. If it rotates, reprint with
   tighter bore tolerance.
3. After full assembly, verify no rod movement is visible when the frame
   is flexed gently by hand.

### Acoustic ping verification

The acoustic ping is the field test for rod pre-tension. It requires no tools.

1. Power off the drone. Hold the frame at the body — not the arm.
2. Tap the CF rod near the arm tip lightly with a non-metallic tool
   (a pen cap or fingernail works).
3. Listen for the resulting tone. A correctly pre-tensioned rod produces
   a clear, high-pitched ring in the 2.2–2.6 kHz range — audible as a
   musical "ping" that sustains for 0.5–1 second.
4. A dull thud or very brief low tone indicates the rod has lost
   pre-tension — it is no longer gripped tightly in the channel. This
   happens after crashes that deform the channel slightly, or as PETG
   creep reduces clamping force over many flight hours.
5. If the tone is dull: tighten the pinch slit bolt gradually (¼ turn at
   a time) until the ring tone returns. Do not exceed the point where the
   tone goes very high — this indicates over-stress risk.
6. A smartphone spectrum analyser app (e.g. Spectroid) can confirm the
   exact frequency if the tone is ambiguous to the ear.

Perform the acoustic ping check at the maintenance intervals in
→ [[scheduled-maintenance]] and after every hard landing or crash.

---

## Rationale

Pre-tensioning via interference fit was selected over a separate fastener
(set screw or clamp bolt) at the rod-arm interface because it adds zero mass
and zero parts count. A set screw adds a stress concentration point at the
rod surface; a clamp bolt adds a fastener that can loosen under vibration.
The interference fit is passive — it cannot loosen, does not require
maintenance, and is established correctly or incorrectly at print time.
The print tolerance is the quality gate.

---

## Connections

requires:
  - [[frame-structure-overview]]
  - [[cf-rod-architecture]]
related:
  - [[floating-motor-mounts]]
  - [[vibration-isolation-theory]]
  - [[exact-constraint-design]]
  - [[sandwich-structure]]
  - [[petg]]
  - [[bolt-torque-reference]]
leads_to:
  - [[floating-motor-mounts]]
  - [[exact-constraint-design]]
  - [[bolt-torque-reference]]
