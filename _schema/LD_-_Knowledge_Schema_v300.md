---
doc_id: LD-SYS-010
title: "libdrone — Knowledge Schema Specification"
tier: 0-system
status: released
version: 3.0.0
date: 2026-04-11
author: Jakub Safar
lang: en
licence: CC BY-SA 4.0
publish: [libdrone_eu, github]
tags:
  - libdrone
  - schema
  - knowledge-base
  - documentation
  - atomic-content
---

## About

This document defines the complete schema for the libdrone 3.0.0 knowledge
corpus. Every article in the corpus must conform to this specification.
This document is the single source of truth for article structure, frontmatter
fields, closed tag vocabularies, persona definitions, traversal orders, and
validation rules.

The 2.x documentation stack is frozen at its last released version and remains
available as reference material. The 3.0.0 corpus is built fresh against this
schema. Nothing is migrated wholesale — existing content is rewritten atomically
when an article covering that topic is authored.

**This schema document is itself written in the article format it defines.**

---

## Summary

The libdrone knowledge corpus is a graph of atomic articles. Each article covers
exactly one topic at all relevant depth levels. Articles are connected by explicit
edges. Persona-specific documents are assembled by walking the graph according to
a traversal definition for that persona. No content is duplicated — each fact
exists in exactly one article.

---

## Concept

### Why atomic articles

Traditional documentation organises knowledge into documents — long files that
mix reference, procedure, rationale, and concept for a broad topic area. This
creates duplication when multiple audiences need overlapping knowledge, and creates
drift when the same fact exists in multiple places and is updated inconsistently.

The atomic model separates authorship from delivery. An author writes one article
covering one topic completely. A reader receives a document assembled from the
articles relevant to their persona and task. The same article appears in the
builder manual, the workshop handout, and the student curriculum — authored once,
delivered in context.

### The graph

Articles are nodes. Connections between articles are edges. The corpus is a
directed graph where edges represent conceptual dependencies: understanding
article A is useful or required before article B. The graph is not a tree — an
article can have multiple parents and multiple children.

### Persona traversal

A persona traversal definition is a named walk through the graph: a starting
node, a set of edges to follow, and a sequence weight that determines output
order. The assembler takes a traversal definition and produces a document. Adding
a new article to the corpus immediately makes it available to every traversal
that would reach it — no manual document editing required.

---

## Reference

### Frontmatter specification

Every article begins with a YAML frontmatter block. All fields marked REQUIRED
must be present and non-empty. The validator rejects articles with missing or
invalid required fields.

```yaml
---
id: kebab-case-topic-name          # REQUIRED. Unique across corpus. Kebab-case.
title: "Human readable title"      # REQUIRED. Sentence case. No trailing period.
version: 1.0.0                     # REQUIRED. Semantic versioning. Increment minor
                                   #   for content changes, patch for corrections.
date: YYYY-MM-DD                   # REQUIRED. Date of last revision.
author: initials or name           # REQUIRED.
status: draft                      # REQUIRED. See status vocabulary below.
scope: generic                     # REQUIRED. See scope vocabulary below.
topic:                             # REQUIRED. Exactly one value from topic vocabulary.
  - topic-slug
personas:                          # REQUIRED. One or more from persona vocabulary.
  - 1.builder
platform:                          # REQUIRED. One or more from platform vocabulary.
  - all
lang: en                           # REQUIRED. ISO 639-1.
licence: CC BY-SA 4.0              # REQUIRED. Do not change.
replaced_by:                       # REQUIRED if status=deprecated. ID of replacement.
  - replacement-article-id
---
```

### Section specification

Every article contains exactly these six top-level sections in this order.
Sections with no applicable content for a given topic contain only the comment
`<!-- not applicable -->`. They are never omitted — their presence keeps the
schema consistent and the assembler predictable.

| Section | Purpose | Mandatory content |
|---|---|---|
| `## Summary` | One paragraph. The what and the why. No jargon. Readable by all personas. | Always |
| `## Concept` | The physics, logic, or principle behind the topic. For students and workshop participants. | When topic has underlying theory |
| `## Reference` | Specifications, values, part numbers, settings. For builders and operators. | When topic has quantitative data |
| `## Procedure` | Numbered step-by-step instructions. Imperative mood. For builders and operators. | When topic has a physical or software process |
| `## Rationale` | Why this design decision was made. What was considered and rejected. For contributors and architects. | Always — even if brief |
| `## Connections` | Explicit graph edges. Links to related articles as a YAML list. | Always |

### Connections section format

```markdown
## Connections

\`\`\`yaml
requires:
  - [[article-id]]          # must understand this before the current article
related:
  - [[article-id]]          # relevant but not prerequisite
leads_to:
  - [[article-id]]          # natural next article in the learning path
\`\`\`
```

The validator confirms that every article ID listed in Connections exists in the
corpus. A broken connection reference fails validation.

---

## Procedure

### Creating a new article

1. Copy the article template from `_templates/article.md`
2. Assign an `id` — kebab-case, unique, descriptive of the topic not the persona
3. Fill all required frontmatter fields
4. Write all six sections — use `<!-- not applicable -->` for sections with no content
5. Add Connections — at minimum one `leads_to` or one `related` entry
6. Run the validator: `python3 bin/validate_corpus.py articles/your-article.md`
7. Fix any reported errors before committing

### Updating an existing article

1. Make content changes
2. Increment `version` — minor for content, patch for corrections
3. Update `date`
4. Run validator
5. Commit

### Deprecating an article

1. Change `status` to `deprecated`
2. Add `replaced_by` pointing to the new article ID
3. Do not delete the file — deprecated articles remain in the corpus permanently
4. Run validator

### Article ID conventions

- Kebab-case: `floating-motor-mounts` not `FloatingMotorMounts`
- Topic-first: `pid-tuning` not `tuning-pid`
- Specific: `pid-tuning-rate-profile` not `pid-stuff`
- No version numbers in IDs — versioning is in frontmatter
- No platform prefix in IDs — platform is a frontmatter tag

---

## Rationale

### Why freeze 2.x rather than migrate

Migration of 64 documents into atomic articles before building the first 3.0.0
drone would delay the build indefinitely. The build generates the highest-value
new knowledge — edge cases, failure modes, calibration data — that has never
been documented. Capturing that knowledge correctly from day one in the new
format is more valuable than migrating existing content that is already readable
in its current form.

The 2.x corpus is complete and coherent. It will continue to serve builders who
find it before the 3.0.0 corpus reaches critical mass.

### Why six fixed sections rather than free-form

A fixed section schema makes the assembler deterministic and makes contributor
expectations explicit. Free-form articles produce inconsistent depth coverage —
some topics get extensive rationale, others get none, and the assembler cannot
reliably extract depth-specific content. Fixed sections enforce completeness and
make the corpus navigable by both humans and tools.

### Why Procedure is separate from Reference

Reference is declarative — specifications, values, properties. Procedure is
imperative — actions, sequences, decisions. A builder mid-assembly scanning for
an O-ring specification is in a different cognitive state than a builder following
a torque sequence. Mixing them forces the reader to parse mode constantly. Topics
that have both (PID tuning) benefit most from the separation — the reader can
go directly to the section they need.

### Why deprecated articles are never deleted

The rationale for a rejected design decision is only meaningful if the article
describing that decision still exists. A contributor researching why silicone
isolators were chosen over rubber needs to find the article that explains what
rubber isolators were tried and why they were abandoned. Deletion destroys
institutional memory. Deprecation preserves it.

---

## Connections

```yaml
requires: []
related:
  - knowledge-schema-traversal-definitions
  - knowledge-schema-tag-vocabularies
  - knowledge-schema-validator
leads_to:
  - article-template
  - floating-motor-mounts
```

---

# Appendix A — Closed Tag Vocabularies

These vocabularies are normative. The validator rejects any frontmatter value
not present in the relevant vocabulary. Adding a new value requires a pull
request to this document with justification and a declaration of which existing
articles would be retroactively tagged.

## Persona vocabulary

| ID | Name | Description |
|---|---|---|
| `1.builder` | Builder | Building a libdrone from components |
| `2.operator` | Operator | Flying and maintaining a built drone |
| `3.payload-dev` | Payload developer | Designing hardware that mounts to libdrone |
| `4.workshop` | Workshop participant | Attending a guided Bandit build event |
| `5.student` | Student | Learning drone theory and engineering |
| `6.evaluator` | Evaluator | Assessing libdrone for institutional procurement |
| `7.contributor` | Contributor | Contributing to the libdrone platform |
| `8.architect` | Architect | Maintaining or evolving the platform design |

## Topic vocabulary

| Slug | Domain |
|---|---|
| `physics-flight-mechanics` | Lift, drag, thrust, angular momentum, 6DOF |
| `control-systems` | PID, feed-forward, loop rates, filters |
| `propulsion` | Motors, propellers, ESCs, DShot |
| `power-systems` | LiPo batteries, power rails, sequencing |
| `sensors-fc` | IMU, barometer, magnetometer, GNSS, FC |
| `communication-rf` | RC links, ELRS, MAVLINK, FPV, protocols |
| `frame-structure` | Frame geometry, failure hierarchy, sandwich |
| `materials` | PETG, PCCF, CF rods, material selection |
| `emc-signal-integrity` | Noise, grounding, filtering, antenna placement |
| `payload-architecture` | GX12 ICD, SDK, LCM-1, PSB-1 |
| `piloting-operations` | Flight modes, RTH, compliance/stiffness |
| `software-stack` | Betaflight, ArduPilot, EdgeTX, CLI |
| `manufacturing` | FreeCAD, slicing, print profiles, coupons |
| `safety-regulations` | Pre-flight, LiPo safety, EASA, risk assessment |
| `iff-deconfliction` | ESP32-S3, IFF layers, emissions control |
| `thermal-management` | TRS, cold weather, battery temperature |
| `cad-parametric` | Variable table, parametric model, FreeCAD |
| `open-source-philosophy` | FOSS, CERN OHL-S, community, licensing |
| `aerial-imaging` | Gimbals, exposure, jello effect, composition |
| `resilience-community` | Civilian preparedness, field operations |
| `skeletons` | Skeleton (non-atom) documents |
| `freecad-ui` | Version-specific FreeCAD UI click maps |
| `firmware-autopilot` | Firmware-layer articles (ArduPilot / Betaflight) |

## Platform vocabulary

| Value | Meaning |
|---|---|
| `all` | Applies to all libdrone platforms |
| `bandit` | libdrone Bandit only |
| `core` | libdrone Core only |
| `pro` | libdrone Pro only |
| `ghost` | libdrone Ghost only |
| `wing` | libdrone Wing only |

## Scope vocabulary

| Value | Meaning |
|---|---|
| `generic` | Applies to any multirotor — not libdrone-specific |
| `libdrone` | libdrone-specific implementation or decision |

## Status vocabulary

| Value | Meaning |
|---|---|
| `draft` | Work in progress. Not yet validated or published. |
| `released` | Complete, validated, published. |
| `deprecated` | Superseded. `replaced_by` required. Never deleted. |

---

# Appendix B — Persona Traversal Orders

Traversal orders define the sequence in which a persona walks the graph.
These are starting definitions — they evolve as the corpus grows.

### 1.builder
```
prep-and-parametrics →
procurement →
coupon-validation →
print-production →
airframe-integration →
electronics-installation →
software-commissioning →
acceptance-validation →
maiden-flight
```

### 2.operator
```
pre-flight-check →
post-flight-check →
scheduled-maintenance →
corrective-maintenance →
emergency-procedures
```

### 4.workshop
```
why-build-a-drone →
procurement →
print-production →
airframe-integration →
electronics-installation →
software-commissioning →
first-flight
```

### 5.student
```
physics-flight-mechanics →
control-systems →
propulsion →
power-systems →
sensors-fc →
communication-rf →
frame-structure →
safety-regulations
```

### 7.contributor
```
platform-architecture →
schema-specification →
design-rationale-index →
contributing-guide
```

### 3.payload-dev
```
gx12-icd →
payload-sdk →
lcm1-spec →
psb1-build-guide
```

### 6.evaluator
```
platform-overview →
resilience-use-cases →
bom-summary →
regulatory-overview
```

### 8.architect
No prescribed traversal. Full corpus access.

---

# Appendix C — Folder Structure

```
libdrone-knowledge/
├── _schema/
│   ├── LD_-_Knowledge_Schema_v300.md     ← this document
│   └── tag-vocabularies.yaml             ← machine-readable copy of Appendix A
├── _templates/
│   └── article-template.md                ← blank article template
├── articles/                             ← flat: one .md per atom, no topic subfolders
├── skeletons/                            ← skeleton documents (sk-*.md)
├── hardware/                             ← FreeCAD macros and parametric tooling
└── bin/
    ├── validate_corpus.py
    ├── assemble_persona.py
    └── setup.sh
```

Articles are stored flat in `articles/` — one file per atom, named by `id`,
with no per-topic subfolders. Topic is a frontmatter tag, not a directory.
An atom tagged with multiple topics still lives in a single file; secondary
topics are expressed through `related` connections.

---

# Appendix D — Article Template

```markdown
---
id: 
title: ""
version: 1.0.0
date: YYYY-MM-DD
author: 
status: draft
scope: generic
topic:
  - 
personas:
  - 
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary



## Concept

<!-- not applicable -->

## Reference

<!-- not applicable -->

## Procedure

<!-- not applicable -->

## Rationale



## Connections

\`\`\`yaml
requires: []
related: []
leads_to: []
\`\`\`
```

---

## Revision History

| Version | Date | Author | Description |
|---|---|---|---|
| 3.0.0 | 2026-04-11 | jsa | Initial release. libdrone 3.0.0 knowledge corpus schema. |
| 3.0.0 | 2026-05-30 | jsa | Doc-accuracy corrections: Appendix A reconciled with tag-vocabularies.yaml (skeletons, freecad-ui, firmware-autopilot); Appendix C updated to flat articles/ layout and actual _schema/bin contents; Connections examples switched to unfenced + wikilink. Enforced schema unchanged — corpus remains 3.0.0. |
