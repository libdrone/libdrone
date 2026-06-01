---
id: sen66-sensor
title: "SEN66 environmental sensor"
version: 1.0.0
date: 2026-04-15
author: jsa
status: released
scope: libdrone
topic:
  - sensors-fc
personas:
  - 5.student
  - 3.payload-dev
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The Sensirion SEN66 is a multi-parameter environmental sensor measuring
particulate matter (PM₁, PM₂.₅, PM₄, PM₁₀), CO₂, VOC index, NOx index,
temperature, and humidity in a single I2C module. On libdrone, it mounts
on the sensor mast above the propeller plane, where it samples uncontaminated
ambient air rather than the drone's own downwash. Each measurement principle
is physically distinct: Mie scattering for particles, NDIR absorption for
CO₂, metal-oxide resistance shift for VOC/NOx. Understanding these principles
tells the operator what the sensor can and cannot detect, and what environmental
conditions limit its accuracy.

---

## Concept

### Particulate matter — Mie scattering

The SEN66 measures aerosol particle concentration by passing a laser beam
through a sample chamber and measuring the light scattered by particles
crossing the beam. This is Mie scattering — light scattering by particles
whose diameter is comparable to the light's wavelength. The scattered light
intensity and its angular distribution encode both particle size and
concentration.

The sensor counts particles in four size bins: PM₁ (< 1 µm diameter), PM₂.₅
(< 2.5 µm), PM₄ (< 4 µm), and PM₁₀ (< 10 µm). Fine particles (PM₁, PM₂.₅)
are the public health concern — they penetrate deep into the lungs. Coarse
particles (PM₄, PM₁₀) are road dust, pollen, sea salt. The ratio between
size fractions carries information about the particle source.

Limitation: the Mie scattering signal requires clean optics. Dust or condensate
on the laser or detector window degrades readings. The SEN66 has an automatic
cleaning cycle (heats the measurement chamber to evaporate condensate) that
activates after each power cycle.

### CO₂ — NDIR absorption

The SEN66 measures CO₂ concentration using Non-Dispersive Infrared (NDIR)
absorption. CO₂ molecules absorb infrared light at a specific wavelength
band centred on 4.26 µm — a consequence of the molecule's vibrational modes.
The sensor shines an IR source through a sealed measurement cell; a detector
on the other side measures how much light was absorbed. More CO₂ in the cell
→ more absorption → lower detector signal → higher reported concentration.

NDIR is the gold standard for CO₂ measurement: it is direct, stable over
time, and not confused by other gases (each gas absorbs at different
wavelengths). The SEN66's range is 400–30,000 ppm. Ambient outdoor CO₂ is
approximately 420 ppm; a sealed room with people can reach 2,000+ ppm;
combustion nearby can produce short spikes to thousands of ppm.

Cross-sensitivity: water vapour absorbs in nearby wavelength bands and
can elevate CO₂ readings in high-humidity conditions. The SEN66 corrects
for this using its onboard temperature and humidity sensor.

### VOC and NOx — metal-oxide resistance

Volatile Organic Compounds (VOCs) and nitrogen oxides (NOx) are measured
by a metal-oxide (MOx) semiconductor sensor. The MOx sensor consists of
a heated metal-oxide crystal whose electrical resistance changes in the
presence of reducing gases (VOC) or oxidising gases (NOx). Higher temperature
(~350°C, maintained by a microscopic heating element) accelerates the
surface reactions, increasing sensitivity.

The SEN66 outputs VOC Index and NOx Index (both 1–500 scale) rather than
raw concentration values. The index is relative to a rolling baseline: index
100 is the recent background; values above 100 indicate elevated VOC or NOx;
values below 100 indicate unusually clean air. This design makes the sensor
practical in varying environments — the baseline adapts over hours rather
than requiring factory calibration against a reference gas.

Limitation: MOx sensors are broad-spectrum — they cannot distinguish which
specific VOC or NOx compound is present. They detect "something is elevated"
but not "specifically benzene" or "specifically NO₂."

### Why the mast height matters

The propellers create a toroidal recirculation zone: a doughnut-shaped ring
of disturbed air approximately one rotor radius above the propeller plane,
extending 80–120mm above the rotor disk at libdrone's typical hover thrust.
Air inside this zone has passed through the propellers — it is turbulent,
heated, and contaminated with whatever the motors and ESC are outgassing.

Mounting the SEN66 inside this zone measures the drone's own emissions, not
the ambient atmosphere. The sensor mast height (85mm above the prop plane
on the V2.4.6 reference design) places the sensor above the recirculation
zone boundary with margin. See → [[induced-velocity]] for the fluid dynamics
derivation. Every millimetre of mast above the minimum height increases the
pendulum arm and slightly affects PID tuning; the mast height is set to the
minimum that clears the recirculation zone.

---

## Reference

| Parameter | SEN66 specification |
|---|---|
| Particulate matter | PM₁, PM₂.₅, PM₄, PM₁₀ (µg/m³) |
| CO₂ range | 400–30,000 ppm, ±40 ppm + 5% of reading |
| VOC index | 1–500 (relative, baseline-corrected) |
| NOx index | 1–500 (relative, baseline-corrected) |
| Temperature range | −10 to 60°C, ±1°C |
| Humidity range | 0–95% RH, ±4.5% RH |
| Interface | I2C, address 0x6B (fixed), 400 kHz fast mode |
| Power supply | 3.3V or 5V (on-module regulator) |
| Warm-up time | 30 s (stable particulate readings) |
| Auto-cleaning cycle | 168 h (1 week) default; triggered on power cycle |
| Mass | ~10 g including housing |

**I2C connection on H7A3-SLIM:**
I2C1 (SDA1/SCL1 pads, or via GX12 Connector A pin 5/6). Address 0x6B.
No address configuration required — SEN66 has a fixed address.

**Betaflight / ArduPilot note:** The SEN66 is not natively supported by
Betaflight or ArduPilot. It is read by the LCM-1 (Pi Zero 2W) companion
computer or ESP32-S3 payload module via I2C, which handles the Sensirion
I2C protocol and logs data to SD card or forwards via WiFi.

---

## Procedure

### Verify SEN66 on bench before first flight

1. Connect SEN66 to I2C1 on H7A3-SLIM or to the LCM-1 I2C bus.
2. Power on. Wait 30 seconds for warm-up.
3. Issue a `0x36 0x03` (measure start) command at address 0x6B and read
   back the 48-byte measurement frame.
4. Confirm CO₂ reading is in the range 400–600 ppm (normal room air).
5. Breathe near the sensor inlet — CO₂ should rise to 1000+ ppm within
   5 seconds, then return to ambient within 30 seconds.
6. If CO₂ reads 0 or > 10,000 ppm at rest, check I2C connection and
   confirm 3.3V supply.

---

## Rationale

The SEN66 was selected over single-purpose sensors (CO₂-only, PM-only)
because the combination of four physical measurement principles in one
module reduces the payload mass and GX12 wiring complexity. A separate
CO₂ sensor, PM sensor, VOC sensor, and temperature/humidity sensor would
require a custom circuit board; the SEN66 provides all eight outputs on a
single I2C address. The trade-off is reduced specificity on VOC/NOx — if
the application required identifying specific compounds rather than detecting
elevated levels, a more specialised sensor would be needed.

---

## Connections

requires:
  - [[payload-architecture]]
  - [[gx12-connector-standard]]
  - [[induced-velocity]]
related:
  - [[supplemental-sensors]]
  - [[payload-sdk]]
  - [[payload-electrical-interface]]
  - [[gps-antenna-placement]]
leads_to:
  - [[payload-sdk]]
  - [[payload-integration]]
