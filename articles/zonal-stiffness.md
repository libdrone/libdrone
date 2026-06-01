---
id: zonal-stiffness
title: "Zonal stiffness"
version: 1.0.0
date: 2026-04-14
author: jsa
status: released
scope: generic
topic:
  - manufacturing
personas:
  - 5.student
  - 8.architect
  - 1.builder
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Zonal stiffness is a structural design strategy that deliberately assigns
different stiffness values to different regions of a structure, routing crash
energy to a controlled sacrificial zone rather than distributing it uniformly.
In libdrone, the centre body is stiff (PCCF sandwich, high infill) and the
arms are compliant (PETG or TPU, lower infill, slimmer cross-section). A crash
load enters at the motor, travels up the arm, and ideally breaks the arm at
the arm-body interface before the energy reaches the electronics stack.
Zonal stiffness is the engineering basis of the failure hierarchy.

---

## Concept

### Stiffness gradient as energy routing

When a structure is loaded to failure, it fails at the point where stress
exceeds the local material strength. If every region has the same strength,
failure location is unpredictable — it may be a prop, an arm, the body, or
the flight controller mount. If the structure is designed so one zone
(the arm) is the weakest link by a controlled margin, failure always occurs
there. The electronics survive; only the arm needs replacing.

The stiffness gradient works as follows. A stiff core resists deformation and
redistributes the crash impulse across the joint area rather than concentrating
it at one point. The compliant arm absorbs and dissipates the remaining energy
by deforming plastically before the core reaches its yield point. The
transition between the two zones — the arm-body joint — is designed as a
stress concentrator: the arm cross-section reduces at the joint, ensuring that
if the arm is going to fracture, it fractures at the joint base and separates
cleanly rather than mid-arm with a jagged break.

### The three zones

**Zone 1 — Motors and propellers:** Designed to survive all normal loads but
release under crash loads. Propellers shatter; motor mounts flex. Energy
absorption is primarily plastic deformation of propellers and the TPU bumper
sleeve on CF rod ends.

**Zone 2 — Arms:** The primary sacrificial zone. PETG arms on Core and Bandit
are designed to fracture at the arm base under crash loads exceeding a defined
threshold. Replacement is the intended repair action, not prevention of failure.
TPU arms on Bandit deform without fracture — they absorb crash energy and
recover shape. Ghost's CF plate arms are stiffer and rely more on the
motor-end deformation.

**Zone 3 — Body sandwich:** The protected zone. PC-CF or PETG sandwich with
high infill and 6-bolt clamping pattern. Should survive all crashes that Zone 2
handles correctly. Electronics, FC, and ESC live here.

### Consequence of violating the gradient

Over-stiffening the arms (printing PC-CF arms with 80% infill) transfers crash
energy directly to the body. The arm does not yield; the body does. FC mounting
holes crack; the electronics stack loosens. This is not a catastrophic crash
failure — it is a subtle structural degradation that produces intermittent
electrical contacts and unexplained flight instability.

Under-stiffening the body (printing the sandwich at 10% infill to save weight)
allows the body to deform under normal flight vibration, not just crashes.
The battery mount loosens; the GX12 connector alignment shifts.

---

## Reference

| Zone | Component | Material | Infill | Role |
|---|---|---|---|---|
| 1 | Props, motor mount | ABS/nylon props; TPU bumper | — | First absorber |
| 2 | Arms | PETG (Core/Pro), TPU 95A (Bandit) | 25–40% | Sacrificial zone |
| 2 | Arms | PC-CF (Pro option) | 40% | Semi-sacrificial |
| 3 | Body sandwich | PCCF layers | 40% | Protected zone |
| 3 | Body sandwich | PETG top/bottom | 25% | Protected zone |

---

## Procedure

### Verify zone stiffness at print time

1. Print a coupon section of each arm and body material at the specified infill.
   See → [[coupon-validation]] for the coupon workflow.
2. Bend the arm coupon by hand at the arm-body joint geometry. It should
   deflect noticeably before any body coupon deflects — the arm must be
   measurably more compliant.
3. Drop test: drop the assembled frame (without electronics) from 1 m onto
   a hard surface. The arm should fail before the body shows any damage.
   If the body cracks first, reduce arm infill or increase body infill.

---

## Rationale

The zonal stiffness approach was adopted because it converts an unpredictable
event (crash) into a predictable outcome (arm breaks, body survives, replace
arm and fly again). The alternative — maximising overall stiffness — produces
a frame that either survives the crash entirely (if under-loaded) or fails
catastrophically (if over-loaded), with no controlled intermediate. For a
platform used in workshop teaching contexts where crashes are expected, a
predictable, cheap repair path is more valuable than maximum crash resistance.
Arms cost €0.50 to print. Flight controllers cost €55. Protecting the FC
at the cost of the arm is the correct trade.

---

## Connections

requires:
  - [[frame-structure-overview]]
  - [[failure-hierarchy]]
related:
  - [[sandwich-structure]]
  - [[pre-tensioning]]
  - [[exact-constraint-design]]
  - [[monocoque-structure]]
  - [[petg]]
  - [[pccf]]
leads_to:
  - [[failure-hierarchy]]
  - [[coupon-validation]]
