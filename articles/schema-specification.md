---
id: schema-specification
title: "Schema specification"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - open-source-philosophy
personas:
  - 7.contributor
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

Every article in the libdrone corpus follows a fixed schema: YAML frontmatter
with twelve required fields, followed by six fixed sections in a fixed order.
The schema is enforced by `bin/validate_corpus.py` — a non-compliant article
fails validation and cannot be merged. The six sections are Summary, Concept,
Reference, Procedure, Rationale, and Connections. Sections that do not apply
to a given article use the placeholder `<!-- not applicable -->`, not omission.
The Connections section is never empty — every article declares at least one
graph edge.

---

## Concept

### Why a fixed schema

A corpus with variable structure is a corpus that requires the reader to
learn each article's individual organisation before finding the information
they need. A corpus with fixed structure allows the reader to build one
mental model and apply it everywhere: Summary is always at the top, Procedure
is always the numbered steps, Rationale is always the design decision context.

The fixed schema also makes the validator possible. A validator that must
infer structure from content cannot reliably catch missing sections. A
validator that knows exactly what structure to expect can catch every deviation.

### Section purposes

**Summary** — one paragraph, no jargon, every persona can read it. Answers:
what is this, why does it matter, what are the limits, what does success look
like. Never empty.

**Concept** — physics, logic, underlying principle. The *why* behind the
procedure. Supports students and workshop participants. Not applicable for
pure-lookup reference articles.

**Reference** — specifications, values, part numbers, settings tables. The
*what* that procedures act on. Not applicable for pure-concept articles.

**Procedure** — numbered steps in imperative mood. Real tasks, not product
functions. One action per step. States starting state. Ends with verification.
Not applicable for overview and index articles.

**Rationale** — why this design decision was made, what alternatives were
rejected, and why. Supports contributors and architects. Never empty — even
one sentence stating the reason for the primary design choice.

**Connections** — graph edges as a fenced YAML block. Three edge types:
`requires` (must understand before this article makes sense), `related`
(relevant but not prerequisite), `leads_to` (natural next step). Never empty.

---

## Reference

### Frontmatter fields

    ---
    id: kebab-case-topic-name           # unique, no version numbers
    title: "Human readable title"       # sentence case, no trailing period
    version: 1.0.0                      # semver — bump on substantive change
    date: YYYY-MM-DD                    # last significant revision date
    author: jsa                         # originating author
    status: draft | released | deprecated
    scope: generic | libdrone           # generic = any multirotor
    topic:                              # one or more from closed vocabulary
      - topic-slug
    personas:                           # one or more from closed vocabulary
      - 1.builder
    platform:                           # one or more: all, bandit, core, pro, ghost, wing
      - all
    lang: en                            # ISO 639-1
    licence: CC BY-SA 4.0
    replaced_by:                        # only when status: deprecated
      - replacement-id
    ---

All twelve fields are required. The validator rejects articles with missing
or unrecognised field values.

### ID conventions

- Kebab-case: [[floating-motor-mounts]] not `FloatingMotorMounts`
- Topic-first: `pid-tuning` not `tuning-pid`
- Specific: [[pid-tuning-rate-profile]] not `pid-stuff`
- No version numbers in IDs
- No platform prefix — platform is a frontmatter tag

### Connections format

## Connections

    [fenced yaml block]
    requires:
      - prerequisite-article-id
    related:
      - related-article-id
    leads_to:
      - next-article-id
    [end fenced yaml block]

The connections block must be a fenced YAML block (triple backtick yaml).
The validator parses this block to build the graph. An unfenced connections
section is not parsed and produces a broken graph.

### When each section is legitimately `<!-- not applicable -->`

| Section | Legitimately not applicable when |
|---|---|
| Concept | Pure lookup reference (e.g. variable table), pure procedure (e.g. CLI command sequence) |
| Reference | Pure concept article (e.g. an analogy or historical context) |
| Procedure | Overview, index, concept-only article |
| Rationale | Never — even one sentence is required |
| Connections | Never — every article connects to at least one other |

If you find yourself writing `<!-- not applicable -->` in Rationale or
Connections — stop. Either the article scope is wrong (too narrow to have
rationale) or the connections are not thought through.

---

## Procedure

### Validating a new article

# Single article
    python3 bin/validate_corpus.py articles/domain/article.md

# Full corpus with graph check
    python3 bin/validate_corpus.py articles/ --graph

The validator exits 0 on success, 1 on any error. Run before every commit.
A PR that fails validation is not reviewed until it passes.

### Common validation errors and fixes

| Error | Cause | Fix |
|---|---|---|
| `Invalid persona 'X'` | Typo or unlisted persona | Check `tag-vocabularies.yaml` for exact spelling |
| `Missing required field 'X'` | Frontmatter field omitted | Add the field |
| `Broken connection: article 'X' not found` | Links to non-existent article | Fix the ID or remove the link |
| `Section '## Rationale' missing` | Section omitted | Add the section with at least one sentence |
| `Connections block not parseable` | Not a fenced YAML block | Wrap in triple backtick yaml |

---

## Rationale

### Why all six sections are present even when some are not applicable

A schema that conditionally omits sections is harder to validate and harder
to read. A reader who knows the schema always expects six sections — if
Procedure is absent, they do not know whether it was omitted legitimately
or simply forgotten. The placeholder `<!-- not applicable -->` makes the
omission explicit and intentional, not ambiguous. The validator confirms
the placeholder is present and the section is not merely missing.

---

## Connections

requires:
  - [[platform-architecture]]
related:
  - [[contributing-guide]]
  - [[design-rationale-index]]
leads_to:
  - [[contributing-guide]]


[floating-motor-mounts]: floating-motor-mounts.md "Floating motor mounts"
[pid-tuning-rate-profile]: pid-tuning-rate-profile.md "PID tuning and rate profile"
[platform-architecture]: platform-architecture.md "Platform architecture"
[contributing-guide]: contributing-guide.md "Contributing guide"
[design-rationale-index]: design-rationale-index.md "Design rationale index"


[floating-motor-mounts]: floating-motor-mounts.md "Floating motor mounts"
[pid-tuning-rate-profile]: pid-tuning-rate-profile.md "PID tuning and rate profile"


[floating-motor-mounts]: floating-motor-mounts.md "Floating motor mounts"
[pid-tuning-rate-profile]: pid-tuning-rate-profile.md "PID tuning and rate profile"
