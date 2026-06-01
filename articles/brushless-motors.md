---
id: brushless-motors
title: "Brushless motors"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: generic
topic:
  - propulsion
personas:
  - 5.student
  - 1.builder
  - 4.workshop
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

A brushless motor produces rotation by generating a rotating magnetic field
in fixed stator coils that permanent rotor magnets chase. Unlike brushed
motors, commutation is handled electronically by the ESC rather than
mechanically by carbon brushes — this eliminates brush wear, enables very
high RPM, and allows precise digital speed control. The motor's stator
designation (e.g. "2507"), kV rating, and pole count together define its
operating characteristics. For libdrone, the BrotherHobby Avenger V2 2507
1750kV is specified: a wide, short stator optimised for torque on 6-inch
propellers at 6S voltage.

---

## Concept

### How a brushless motor works

The stator — the stationary part — consists of copper coils wound around iron
teeth arranged in a ring. The rotor — the spinning bell — carries permanent
magnets around its inner circumference. The ESC energises two stator coils at
a time, creating a combined magnetic field pointing in a specific direction.
The rotor's permanent magnets are attracted to this field and rotate to align
with it. Before they reach alignment, the ESC advances to the next commutation
step — energising different coils and moving the stator field forward. The
rotor chases the advancing field continuously. This chase is rotation.

The motor has no mechanical contact between the rotating and stationary
parts other than the bearings. No brushes wear. No sparks. Maximum RPM is
limited by bearing quality and aerodynamic drag, not by mechanical friction.
This is why brushless motors last thousands of hours versus hundreds for
brushed motors.

### Stator designation

A motor designated "2507" has a 25 mm stator diameter and 7 mm stator height.

- **Larger diameter**: longer moment arm for the magnetic force → more torque
  per amp of current. Wide stators suit large propellers.
- **Taller height**: more copper in the winding → higher current capacity →
  more power. Tall stators suit high-RPM small-propeller applications.

The 2507 is wide and short — optimised for torque. A 2306 (23 × 6 mm) is
narrower and taller — optimised for RPM. 6-inch propellers need torque;
5-inch props need RPM. The stator geometry follows the application.

### kV rating

kV specifies RPM per volt applied, at no load. It is determined entirely
by the winding: fewer turns of wire per stator tooth → higher kV (faster,
less torque per amp); more turns → lower kV (slower, more torque per amp).
The "V" is volts, not kilovolts.

    No-load RPM = kV × supply voltage
    BrotherHobby 2507 1750kV on 6S nominal (22.2V):
    No-load RPM = 1750 × 22.2 = 38,850 RPM
    Under propeller load at hover:
    Actual RPM ≈ 28,000–32,000 RPM

The under-load RPM is lower because back-EMF limits it. As the motor spins,
it generates a counter-voltage proportional to RPM. Effective driving voltage
= supply voltage − back-EMF − resistive drop. Equilibrium RPM is where these
balance.

Motor selection: target operating RPM for the chosen prop → kV = target RPM ÷
supply voltage. Then verify the motor can handle the current at that operating
point.

### Pole count and commutation frequency

The 2507 has 14 permanent magnets (7 pole pairs) and 12 stator teeth — a
14N12P configuration. The 14-pole/12-tooth relationship minimises cogging
torque (the tendency to snap to discrete positions) while keeping electrical
frequency in a manageable range.

    Electrical frequency = mechanical RPM × pole pairs ÷ 60
    At 30,000 RPM: 30,000 × 7 ÷ 60 = 3,500 Hz

The ESC must commutate 3,500 times per second at this speed. At AM32's 48 kHz
switching frequency, there are ~14 switching cycles per commutation step —
sufficient for smooth phase transitions and low motor current ripple.

The pole count is also what converts the ESC's eRPM telemetry to mechanical RPM:
`mechanical RPM = eRPM ÷ pole_pairs`. This must be configured correctly in
Betaflight for the RPM filter to track motor frequencies accurately.
→ See [[rpm-filter]].

### Thrust curve non-linearity

The relationship between throttle and thrust is not linear:

| Throttle | Thrust (approx) | Current (approx) |
|---|---|---|
| 50% | 900–1000 g | 15–18 A |
| 75% | 1800–2000 g | 28–32 A |
| 100% | 2400–2600 g | 40–55 A |

The last 20% of throttle delivers proportionally less thrust per amp. For
libdrone hovering at 28–35% throttle, the operating point is well into the
efficient region of the thrust curve.

---

## Reference

### BrotherHobby Avenger V2 2507 1750kV — libdrone specification

| Parameter | Value |
|---|---|
| Stator diameter | 25 mm |
| Stator height | 7 mm |
| kV rating | 1750 kV |
| Pole count | 14 (7 pole pairs) |
| Stator tooth count | 12 (14N12P) |
| Recommended prop | HQ 6×3×3 or HQ 6×2.5×3 on 6S |
| Peak thrust (HQ 6×3×3, 6S) | 2400–2600 g at 40–55 A |
| Hover thrust per motor | ~220–240 g at ~4–5 A |
| Motor mass | 40 g including 20 cm cables |
| Total 4× mass | 160 g |
| Mount pattern | M3 × 9 mm (4 bolts) |
| Shaft diameter | 5 mm |

### Replacing a motor

Inspect bearings after any hard crash landing on the motor head. A motor
with damaged bearings produces a grinding sound and elevated vibration at
low RPM. A motor with bent shaft produces vibration at all RPM levels.
Both require immediate replacement — damaged bearings propagate vibration
directly to the floating mount and degrade gyro signal quality.

---

## Procedure

### Verifying motor health before flight

1. With props removed, arm and spin all four motors to 20% throttle.
2. Listen for grinding, irregular sound, or vibration inconsistent across motors.
3. In Betaflight Motors tab: verify all four motors respond to throttle commands
   and report eRPM proportional to commanded speed.
4. Feel each motor housing (carefully) — all should reach similar temperature
   within 30 seconds. A noticeably cooler motor may indicate a poor connection;
   a noticeably hotter motor may indicate a winding fault.

### Post-crash motor inspection

1. Spin each motor by hand with no power. It should rotate smoothly and silently
   with minimal resistance. Any roughness indicates bearing damage.
2. Check the shaft for straightness: spin slowly and observe the prop collet
   for wobble. Any wobble >0.5 mm indicates a bent shaft.
3. Inspect the bell for contact marks or dents from ground contact.

---

## Rationale

### Why 1750kV and not higher kV on 6S

Higher kV on the same voltage means higher RPM. The BrotherHobby 2507 at
2200kV would reach approximately 48,800 RPM on 6S unloaded — too fast for
efficient 6-inch propeller operation. At those RPMs, the 6-inch prop is
operating outside its efficient pitch speed range and current draw increases
sharply without proportional thrust gain. 1750kV was selected to place the
operating RPM (28,000–34,000 under load) in the optimal range for 6-inch
polycarbonate props on 6S.

---

## Connections

requires:
  - [[lift-and-thrust]]
related:
  - [[propellers]]
  - [[electronic-speed-controllers]]
  - [[dshot-protocol]]
  - [[floating-motor-mounts]]
  - [[rpm-filter]]
  - [[acoustic-signature-design]]
leads_to:
  - [[propellers]]
  - [[electronic-speed-controllers]]
  - [[acoustic-signature-design]]


[rpm-filter]: rpm-filter.md "RPM filter"
[lift-and-thrust]: lift-and-thrust.md "Lift and thrust"
[propellers]: propellers.md "Propellers"
[electronic-speed-controllers]: electronic-speed-controllers.md "Electronic speed controllers"
[dshot-protocol]: dshot-protocol.md "DShot protocol"
[floating-motor-mounts]: floating-motor-mounts.md "Floating motor mounts"
[acoustic-signature-design]: acoustic-signature-design.md "Acoustic signature design"
