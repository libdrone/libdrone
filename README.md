# libdrone

**Open-source aerial payload platform. EU-origin, CERN OHL-S v2 licensed, zero cloud dependency.**

→ Documentation and build guides: **[libdrone.eu](https://libdrone.eu)**

---

## What this is

libdrone is a modular, repairable aerial payload platform designed for
civilian resilience, research, and community deployment. It is not a
consumer drone. It is a platform — a documented physical standard that
any sensor, camera, or instrument can attach to without modifying the
airframe or negotiating a developer programme.

The frame costs €16 in filament. A complete build with goggles and sensor
payload costs approximately €1,400. Every component has a documented
alternative. No cloud subscription. No proprietary firmware in the
critical path.

Designed in the Czech Republic. Legal entity in the Czech Republic.

---

## Why it exists

Institutional drone users in the EU increasingly cannot accept DJI: closed
software, cloud-dependent data pipelines, Chinese supply chain. Academic
open platforms start at €10,000–50,000. Racing FPV drones have no payload
concept. No credible open, documented, EU-origin payload platform existed.

libdrone fills that gap at community cost with institutional-grade documentation.

→ [The DJI problem](articles/dji-problem.md) explains the gap in full.

---

## Platform variants

| Variant | Flight system | Primary use |
|---------|--------------|-------------|
| **Pro** | Betaflight, 6S | Research, mapping, payload operations |
| **Bandit** | ArduPilot, 4S | Autonomous missions, ATAK integration |
| **Core** | Betaflight, 4S | Training, education, under 250 g |
| **Ghost** | Betaflight, 4S | Long endurance, reduced emissions |
| **Wing** | ArduPilot | Fixed-wing, forestry, long-range survey |
| **SCRAP** | Betaflight, 4S | Entry-level build, pilot practice |

All variants except SCRAP carry the GX12-7 dual payload interface standard.

---

## Repository contents

```
articles/          Atomic reference articles (~170 topics)
skeletons/         Long-form guides assembling articles into reading paths
hardware/          FreeCAD parametric variable macro
bin/               Corpus validation tooling
_schema/           Schema specification and tag vocabularies
_templates/        Article and skeleton templates
```

The `articles/` and `skeletons/` directories are the primary content.
Each article covers exactly one topic at full depth. Skeletons are
narrative guides that link articles into coherent reading paths for a
specific audience (builder, operator, evaluator, researcher).

---

## The payload interface

Every libdrone platform (except SCRAP) has two GX12-7 aviation connectors
on its sealed top surface. They provide:

- Regulated 5 V / 2 A power
- GPS coordinates at 10 Hz (57,600 baud NMEA)
- Bidirectional communications (UART + I2C)
- Radio-controlled GPIO switching
- OSD overlay in the pilot's goggles

Any payload built to this interface works on any compliant platform.
**Your payload IP is yours** — the CERN OHL-S v2 copyleft applies to
modifications of the platform, not to payloads that connect via the
GX12 interface.

→ [GX12 connector standard](articles/gx12-connector-standard.md)
→ [Payload electrical interface](articles/payload-electrical-interface.md)
→ [Payload SDK](articles/payload-sdk.md)

---

## FreeCAD macro

`hardware/LD_V300_Variables.FCMacro` creates the complete parametric
variable spreadsheet in FreeCAD. Run it once on a new document to
populate all 15 sections (~170 variables) with correct aliases.

**Install:**
1. Copy the macro to your FreeCAD Macro folder:
   - macOS: `~/Library/Preferences/FreeCAD/Macro/`
   - Linux Flatpak: confirm via Tools → Macros
   - Linux native: `~/.FreeCAD/Macro/`
   - Windows: `%APPDATA%\FreeCAD\Macro\`
2. Tools → Macros → select `LD_V300_Variables` → Execute.

FreeCAD 1.1 stable required. Download: https://www.freecad.org/downloads.php

The `.FCStd` model files are not yet in this repository — hardware validation
is ongoing. The macro and the variable reference articles
([variable-table-structure.md](articles/variable-table-structure.md),
[variable-table-values.md](articles/variable-table-values.md)) provide
everything needed to begin modelling or to contribute CAD work.

---

## Contributing

See [contributing-guide.md](articles/contributing-guide.md) for the full
workflow. Short version:

1. Fork this repository on GitHub
2. Articles and skeletons must pass `python3 bin/validate_corpus.py` with zero errors
3. Hardware geometry changes require a physical coupon validation result
4. Vocabulary changes require ratification before the article is written
5. Open a PR — all reviews go through the maintainer (jsa)

If you have FreeCAD experience and want to contribute to the parametric model,
open an issue describing your background and proposed scope before starting.
The variable table and reference articles are the starting point.

---

## Licence

- Hardware design: **CERN OHL-S v2** (Strongly Reciprocal)
- Documentation: **CC BY-SA 4.0**

CERN OHL-S v2 means modifications to the platform hardware must be published
under the same licence. It does not apply to payloads built to the GX12
interface standard — those are yours.

---

## Links

| | |
|---|---|
| Documentation | https://libdrone.eu |
| GitHub | https://github.com/libdrone/libdrone |
| Licence (hardware) | https://ohwr.org/cern_ohl_s_v2.txt |
| Licence (docs) | https://creativecommons.org/licenses/by-sa/4.0/ |
