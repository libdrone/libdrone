---
id: kebab-case-topic-name            # REQUIRED. Unique across corpus.
title: "Human readable title"        # REQUIRED. Sentence case. No trailing period.
version: 1.0.0                      # REQUIRED. Semantic versioning.
date: YYYY-MM-DD                    # REQUIRED. Last revision date.
author: initials-or-name             # REQUIRED.
status: draft                       # REQUIRED. draft | released | deprecated
scope: generic                      # REQUIRED. generic | libdrone
topic:                              # REQUIRED. Exactly one topic.
  - topic-slug
personas:                           # REQUIRED. One or more.
  - 1.builder
platform:                           # REQUIRED. One or more.
  - all
lang: en                            # REQUIRED. ISO 639-1.
licence: CC BY-SA 4.0               # REQUIRED. Do not change.
# learning_objective:               # OPTIONAL but STRONGLY encouraged.
#   "After reading this article, the reader can [perform a real-world action]."
# replaced_by:                      # REQUIRED only if status: deprecated.
#   - replacement-article-id
---

## Summary

One paragraph answering:
- What this is
- Why it matters (consequence of getting it wrong)
- Where it fits in the system
- What a correct outcome looks like

No jargon. Readable by all personas.

## Concept

Explain the underlying principle, physics, or logic.
Assume a competent but uninitiated reader.

If no theory is required for this topic, use:
<!-- not applicable -->

## Reference

Authoritative facts only:
- specifications
- dimensions
- values
- part numbers
- limits
- settings

No procedure. No narrative.

If the topic has no quantitative data, use:
<!-- not applicable -->

## Procedure

Numbered steps in imperative mood.
One physical or software action per step.
End with an observable verification outcome.

If the topic has no process, use:
<!-- not applicable -->

## Rationale

Explain *why* this design or decision exists.
State alternatives that were considered and rejected.
Preserve institutional memory.

Never empty — even one sentence is sufficient.

## Connections

requires:
  - [[prerequisite-article-id]]
related:
  - [[related-article-id]]
leads_to:
  - [[next-logical-article-id]]