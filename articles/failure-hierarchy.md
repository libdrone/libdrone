---
id: failure-hierarchy
title: "Failure hierarchy"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - frame-structure
personas:
  - 1.builder
  - 2.operator
  - 5.student
  - 7.contributor
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

A drone frame that fails unpredictably in a crash is more dangerous and more
expensive than one that fails predictably. libdrone implements a deliberate
failure hierarchy: in any crash, energy is absorbed in a fixed sequence that
protects the most expensive and least replaceable components. The arm shaft
fractures first, the tabs yield second, the T-slots fail third, the X body
core fails last. Electronics survive all but the most destructive crashes
because they are the final element in the sequence, protected by everything
in front of them.

---

## Concept

### The failure sequence

    arm shaft fractures
      → tabs stay intact
        → T-slots stay intact
          → X body core stays intact
            → electronics survive

Each element in the sequence must be weaker than the element behind it —
not by accident, but because the designer chose materials, cross-sections,
and geometries to enforce the order. If any element fails out of sequence,
the hierarchy collapses and crash energy finds its own path, usually through
the electronics.

### Analogies from other engineering domains

This pattern appears wherever engineers manage failure in critical systems:

- **Automotive crumple zones:** the bonnet and front rails deform progressively
  to absorb impact energy, protecting the cabin. The cabin is stiff; the
  crumple zones are compliant. The order is designed, not accidental.
- **Aircraft engine fuse pins:** a pin designed to shear under overload allows
  the engine to separate from the wing rather than tearing the wing spar.
  The pin is the designed weak link that saves the wing.
- **Electrical fuses:** the fuse wire is the deliberate weak link in the circuit,
  protecting the wiring and devices downstream.

In all cases the key insight is the same: a controlled failure at a known
location is far cheaper than an uncontrolled failure at an unknown one.

### Zonal stiffness

The failure hierarchy is the crash expression of a broader design principle:
zonal stiffness layering. The frame is not uniformly stiff or uniformly
compliant — it is stiff where precision matters (gyro mount, motor axis, core),
compliant where damping is needed (motor-to-frame interface), and deliberately
weak where crash energy must be managed (arm shaft).

A uniformly stiff frame (solid CF plate) distributes crash energy across all
zones simultaneously — the electronics receive the same impulse as the arm tip.
A uniformly compliant frame cannot hold geometry under motor thrust and
vibration. Zonal layering achieves both goals without contradiction.

---

## Reference

### Element properties by zone

| Zone | Material | Failure mode | Replacement cost | Replacement time |
|---|---|---|---|---|
| Bumper | ASA | Crush / split | < €0.50 | 30 s |
| Arm shaft | PETG | Bending fracture | < €1.00 (filament) | < 5 min |
| Arm tab | PETG | Shear at T-lock root | < €0.20 (filament) | 20 min (sandwich partial disassembly) |
| T-slot (PCCF layer) | PCCF | Crack at slot transition | ~€3–5 (filament) | 60 min (full disassembly) |
| X body core | PCCF (3 layers) | Catastrophic crack | ~€10–15 (filament) | Full rebuild |
| Electronics | Mixed | Impact damage | €100–300 | Full rebuild |

### Calibration check: shaft vs tab strength

The arm shaft must fail before the tab. This is ensured by geometry:

- The shaft is loaded in **bending** over an unsupported length of ~100 mm.
  Bending moment = force × length. Long lever arm → high moment → early failure.
- The tab is loaded in **shear** over 20 mm of engagement depth in the T-slot.
  Shear area = tab width × engagement depth. Short, wide section → high shear
  resistance → later failure.

If a build produces tabs that fracture before shafts in crash testing, the
tab is too thin or the engagement depth is too shallow. Increase engagement
depth (variable `#TabLength`) before increasing shaft cross-section.

### Post-crash diagnostic protocol

| Observation | Diagnosis | Action |
|---|---|---|
| Shaft broken, tabs intact, body intact | Hierarchy worked correctly | Replace shaft only |
| Shaft broken, tab cracked at T-lock root | Partial hierarchy failure | Replace shaft + tab + inspect T-slot |
| T-slot cracked, PCCF layer damaged | Hierarchy failure — tab was too strong | Replace PCCF layer, review tab geometry |
| Core damaged, electronics affected | Full hierarchy failure | Full rebuild, root cause analysis |
| No visible damage, drone flies erratically | Check rod seating and bolt torque | Re-torque, check rod channels |

---

## Procedure

### Post-crash inspection sequence

Inspect in hierarchy order — stop when no damage is found.

1. **Bumpers:** visible crack, split, or missing. Replace immediately if damaged.
2. **Arm shafts:** flex each shaft by hand. A cracked shaft has play at the
   break. Visually inspect at motor head root and mid-shaft. Replace if cracked.
3. **Arm tabs:** remove shaft (4 × M2 screws). Inspect tab at T-lock root
   — narrow section immediately inside the PCCF layer face. Any cracking means
   tab replacement.
4. **T-slots (PCCF layers):** with tabs removed, visually inspect the T-slot
   interior through the open arm extension gap. Cracking at the slot edges or
   at the core transition means the PCCF layer must be replaced.
5. **X body core:** if the T-slot inspection above passes, core damage is
   unlikely. Inspect rod channels for visible gap or looseness. Re-press if needed.
6. **Electronics:** if any structural element above the tab level showed damage,
   inspect the electronics for vibration damage and connector security. Verify
   Blackbox on next flight if any doubt.

---

## Rationale

### Why the arm shaft is deliberately the weakest structural element

The arm shaft is the cheapest part in the failure sequence. Filament cost for
one shaft is under €1. It is printable from any machine with a 220 × 220 mm
bed and no special materials. It installs in 5 minutes without tools beyond
a hex key. Designing it as the weak link means the majority of crashes cost
under €1 and 5 minutes. Any alternative design that makes a more expensive
element fail first multiplies crash cost without reducing the physical energy
involved.

### Why the bumper is outside the hierarchy

Bumpers absorb very small crash energies — tip scrapes, hard landings, grass
contact. They are consumables that protect the arm shaft tip, not elements in
the primary crash energy path. A bumper that is too strong would transfer ground
contact loads directly into the shaft tip, initiating shaft bending from the
end rather than at the root. Bumpers are intentionally hollow and sacrificial.

### Why no adhesive between layers

Adhesive bonding the sandwich layers would redistribute crash energy across
the bonded interface rather than concentrating it at the designed failure point.
A crash that should fracture one shaft might instead peel a bonded interface in
an unpredictable location. Keeping the sandwich mechanically joined (rods + bolts)
preserves the zonal failure behaviour.

### Calibration for a new geometry

If the frame geometry is changed (different wheelbase, different arm cross-section
via the variable table), the failure hierarchy must be re-verified. The key test
is a drop test from 1.5 m onto a hard surface: the shaft should crack, the tab
should be undamaged. If the tab cracks first, increase `#TabLength` (deeper
T-slot engagement). Print a coupon and test before committing to a full build.
→ See [[coupon-validation]].

---

## Connections

requires:
  - [[frame-structure-overview]]
related:
  - [[sandwich-structure]]
  - [[arm-shaft]]
  - [[coupon-validation]]
  - [[petg]]
  - [[pccf]]
leads_to:
  - [[scheduled-maintenance]]


[coupon-validation]: coupon-validation.md "Coupon validation"
[frame-structure-overview]: frame-structure-overview.md "Frame structure overview"
[sandwich-structure]: sandwich-structure.md "Sandwich structure"
[arm-shaft]: arm-shaft.md "Arm shaft"
[petg]: petg.md "PETG — properties and libdrone use"
[pccf]: pccf.md "PCCF — properties and libdrone use"
[scheduled-maintenance]: scheduled-maintenance.md "Scheduled maintenance"
