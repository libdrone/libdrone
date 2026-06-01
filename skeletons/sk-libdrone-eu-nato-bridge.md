---
id: sk-libdrone-eu-nato-bridge
title: "libdrone documentation as EU/NATO-compatible infrastructure"
version: 1.1.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - skeletons
personas:
  - 6.evaluator
  - 8.architect
  - 7.contributor
platform:
  - all
lang: en
licence: CC BY-SA 4.0
skeleton: true
learning_objective: >
  "After reading this, the reader can propose libdrone as a civilian
  open-infrastructure layer compatible with EU/NATO institutional governance
  requirements — and identify what overlay work would be needed to reach
  a specific compliance posture."
---

## Summary

libdrone's documentation system is non-certified by design. Certification
artefacts — requirements traceability matrices, safety cases, assurance
arguments — are treated as optional overlays that consume the corpus rather
than replace it. This document explains where libdrone's atomic, graph-based
knowledge architecture aligns with modern EU aerospace and defence documentation
principles, where it intentionally diverges, and what a path to NATO-compatible
documentation would look like without structural rewrite. The strategic
positioning: libdrone is the civilian translation layer between fast-moving
open hardware innovation and the institutional governance expectations of EU
and NATO stakeholders.

---

## Concept

### The structural gap European institutions face

European defence, resilience, and civil-protection stakeholders increasingly
face a problem: innovation moves faster than institutional standards. Agile
teams iterate hardware and software in weeks; EU and NATO systems require
traceability, auditability, and long-term accountability measured in years.

Systems fail to transition not because they do not work, but because they
cannot be *explained, audited, and governed* at institutional scale. The
barrier is documentation maturity, not technical capability.

libdrone is designed explicitly to occupy this gap.

### Documentation as infrastructure

Traditional technical documentation treats documents as deliverables — outputs
produced at milestones, filed, and forgotten. Modern aerospace and defence
practice increasingly treats documentation as infrastructure: a living system
that preserves knowledge, rationale, and decision history across years and
organisations.

→ [[platform-architecture]] explains the atomic corpus model. The key properties
that make libdrone documentation infrastructure rather than deliverable: single
source of truth for every fact, explicit graph of dependencies, permanent
preservation of rejected alternatives via deprecated articles, persona-aware
delivery without duplication. These properties are the substrate on which
institutional governance artefacts can be built.

### Why this is not an accident

The libdrone corpus architecture was designed from first principles to match
the *direction* of EU and NATO documentation evolution: modular content,
role-specific delivery, decision traceability, and strong governance of
vocabulary and structure. It exceeds the structural rigour of many legacy
industrial documentation systems — despite remaining fully open and tool-agnostic.

→ [[foss-principles]] explains the CERN OHL-S v2 copyleft and → [[vendor-lock-in]]
explains the deliberate independence from proprietary documentation tooling.
Both are preconditions for institutional trust: an institution cannot audit a
documentation system it cannot inspect.

### The bridge role: from agility to institution

libdrone's strategic value is as a translation layer. It absorbs fast-moving,
high-iteration knowledge from agile builders and expresses it in a form that
institutions can reason about, audit, and sustain over time.

This is analogous to how Red Hat translated Linux into enterprise infrastructure,
or how Raspberry Pi translated open hardware into education and industry. The
underlying technology did not change — the governance layer around it did.
libdrone's documentation system is the governance layer.

To fulfil this role sustainably, libdrone requires sponsorship that values
neutrality and long-term stewardship over short-term commercialisation. A
foundation-style model — like the Apache Software Foundation or the Eclipse
Foundation — enables libdrone to remain open while supporting institutional
integration, certification experiments, and public interest deployments. The
documentation system is the core asset that makes this model viable.

---

## Reference

### Alignment with EU / NATO / miltech documentation dimensions

| Dimension | libdrone approach | Assessment |
|---|---|---|
| Transparency and auditability | CERN OHL-S v2, full git history, CC BY-SA 4.0 docs | Strong — exceeds most industrial systems |
| Provenance and version control | Semantic versioning, date, author on every article | Strong |
| Role separation | 9 defined personas, closed vocabulary | Strong |
| Preservation of rejected alternatives | Deprecated articles never deleted, `replaced_by` required | Strong |
| Resistance to silent drift | Validator enforces schema and graph integrity on every commit | Strong |
| Independence from proprietary tooling | Markdown, Python stdlib, no vendor lock-in | Strong |
| Requirements traceability | Not implemented — optional overlay | Gap (by design) |
| Safety case / assurance argument | Not implemented — optional overlay | Gap (by design) |
| Controlled access / classified handling | Not implemented | Out of scope for civilian platform |

### What a NATO compatibility overlay would require

If libdrone were sponsored for a NATO-adjacent programme, compatibility would
not require replacing the documentation system. The following layers could be
overlaid on the existing corpus:

| Overlay type | Approach | Effort |
|---|---|---|
| Requirements identifiers | Map NATO STANAG or national IDs onto existing atom IDs | Low |
| Safety arguments | Link safety case nodes to atom Rationale sections | Medium |
| Compliance views | Assemble existing graph traversals for specific standards | Low — assembler already supports this |
| Controlled-access mirrors | Fork repo, restrict access, maintain synchronisation | Medium — infrastructure work |
| Certification evidence | Add evidence artefacts as additional atoms or frontmatter fields | Medium |

Critically, these overlays **consume** the libdrone corpus rather than replace it.
The underlying atomic structure is already compatible.

---

## Procedure

### Evaluating libdrone for institutional adoption

For an EU or NATO evaluator assessing whether libdrone documentation meets
governance requirements:

1. Start with → [[schema-specification]] — understand the atomic model and the
   six-section schema. Assess against your institution's documentation structure
   requirements.
2. Review → [[design-rationale-index]] — every major design decision has a
   documented rationale with rejected alternatives. Assess against your
   traceability requirements.
3. Review → [[contributing-guide]] — the vocabulary governance and PR process.
   Assess against your change management requirements.
4. Run `python3 bin/validate_corpus.py articles/ --graph` — zero errors
   demonstrates automated integrity enforcement. Assess against your quality
   gates.
5. Identify the overlay gap: which of your requirements are not met by the
   existing corpus? Map each gap to one of the overlay types in the Reference
   table above.
6. The result is a readiness assessment with a concrete gap/overlay list —
   not a binary pass/fail.

---

## Rationale

### Why non-certification is the correct default

Certification artefacts are outcomes of governance processes, not preconditions
for engineering innovation. Imposing certification overhead on the core libdrone
build workflow would slow the development cycle that produces the high-value
knowledge the corpus captures.

The correct architecture is layers: the corpus provides the technical knowledge
substrate; an institution that requires certification builds that layer above the
corpus without modifying it. This preserves libdrone's agility for civilian
builders while leaving the door open for institutional adoption.

The analogy that holds: Linux was not designed to be certified. Red Hat Enterprise
Linux was. Linux continued to innovate; RHEL provided the certified layer that
institutions needed. Both coexist because they are architecturally separated.

---

## Connections

requires:
  - [[platform-architecture]]
  - [[foss-principles]]
related:
  - [[schema-specification]]
  - [[design-rationale-index]]
  - [[iff-architecture]]
  - [[operational-security]]
  - [[contributing-guide]]
leads_to:
  - [[sk-security-operations-guide]]
  - [[sk-platform-brief]]
