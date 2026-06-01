---
id: platform-architecture
title: "Platform architecture"
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

The libdrone 3.0.0 knowledge corpus is a graph of atomic articles assembled
into persona-specific documents at delivery time. It has three layers: atoms
(the indivisible units of knowledge), skeletons (prose that connects atoms
into documents for specific readers), and the graph (the connections between
atoms that reveal dependency and learning paths). The architecture enforces
single-source-of-truth — every fact has exactly one home. A change to an
atom propagates automatically to every skeleton that links to it. No fact
is duplicated. No fact is lost.

---

## Concept

### Atoms, skeletons, graph

**Atoms** are individual Markdown articles, each owning exactly one topic.
They are structured by the six-section schema (Summary, Concept, Reference,
Procedure, Rationale, Connections) and validated by the schema validator.
An atom cannot be deleted — it can only be deprecated with a `replaced_by`
pointer to its successor.

**Skeletons** are free prose documents that link to atoms. A skeleton does
not contain specifications, numbers, or procedures — those live in atoms.
A skeleton carries the narrative: why this sequence matters, how these
concepts connect, what the reader should understand by the end. A skeleton
is rewritten when the reader changes; the atoms beneath it do not change.

**The graph** is the network of `requires`, `related`, and `leads_to`
connections declared in every atom's Connections section. It reveals the
dependency structure of the knowledge base. The validator enforces graph
integrity — a broken connection is an error, not a warning.

### Why atoms and not chapters

Traditional documentation organises knowledge into chapters within documents.
A chapter about floating motor mounts might also contain material about
vibration isolation theory, O-ring selection, and the failure hierarchy —
because all of these are contextually relevant when discussing motor mounts.

This is convenient to write and inconvenient to maintain. When the O-ring
specification changes, the chapter must be updated. When vibration isolation
theory is needed in a different context, it must be duplicated. When the
failure hierarchy is updated, it may be inconsistent with the chapter.

The atom model solves this by giving each topic exactly one home. The O-ring
specification lives in [[floating-motor-mounts]]. The vibration isolation
theory lives in [[vibration-isolation-theory]]. The failure hierarchy lives in
[[failure-hierarchy]]. They link to each other. A change to any one propagates
everywhere it is linked — never duplicated, never inconsistent.

### The persona traversal model

Different readers need different paths through the same knowledge base. A
builder needs the sequence: parametrics → coupons → print → assembly →
electronics → software → maiden. A student needs: physics → control →
propulsion → sensors. An evaluator needs: platform overview → use cases →
BOM → regulation.

These traversals are not different documents — they are different paths
through the same graph. The atoms serve all personas. The skeleton documents
serve specific readers by choosing which atoms to link and in what order.

---

## Reference

### Corpus structure

    ld300/
      articles/           # flat per domain — all articles at this level
        frame-structure/
        materials/
        ...                # 20 domains
      _schema/
        tag-vocabularies.yaml    # closed vocabulary
        article-schema.json      # JSON schema for validation
      bin/
        validate_corpus.py       # schema + graph validator
      skeletons/                 # skeleton documents

### Governance model

| Decision | Authority | Process |
|---|---|---|
| New article | Author | Write, validate, PR |
| New vocabulary tag | jsa ratifies | Issue → ratification → PR with retroactive tagging |
| Domain sign-off | jsa | Review after domain completion |
| Schema change | jsa | Major change — discuss in issue first |
| Skeleton sign-off | jsa | Review at skeleton delivery |

### Article count and status (as of v3.0.0)

| Metric | Value |
|---|---|
| Total articles | 124 |
| Schema errors | 0 |
| Graph broken connections | 0 |
| Domains complete | 20 of 20 |
| Persona traversals fully covered | builder, operator, workshop, evaluator, student, payload-dev, contributor |

---

## Procedure

### Onboarding a new contributor

1. Contributor reads [[platform-architecture]] (this article) — understands the model
2. Contributor reads [[schema-specification]] — understands the article schema
3. Contributor reads [[contributing-guide]] — understands the PR workflow
4. Contributor reads [[floating-motor-mounts]] — the reference example for article depth and tone
5. Contributor identifies a topic gap (missing article or broken connection in `--graph` output)
6. Contributor opens an issue describing the proposed article
7. jsa confirms the topic is not already covered and the scope is appropriate
8. Contributor writes, validates, opens PR

---

## Rationale

### Why the graph validator is the primary quality gate

Manual review of connection integrity across 124+ articles is not feasible.
The validator catches broken connections, invalid vocabulary tags, missing
sections, and malformed frontmatter automatically. Every PR must pass the
validator before review. This means that structural quality is enforced by
tooling, not by the reviewer's memory.

---

## Connections

requires: []
related:
  - [[schema-specification]]
  - [[design-rationale-index]]
  - [[contributing-guide]]
  - [[foss-principles]]
leads_to:
  - [[schema-specification]]
  - [[contributing-guide]]


[floating-motor-mounts]: floating-motor-mounts.md "Floating motor mounts"
[vibration-isolation-theory]: vibration-isolation-theory.md "Vibration isolation theory"
[failure-hierarchy]: failure-hierarchy.md "Failure hierarchy"

[platform-architecture]: platform-architecture.md "Platform architecture"
[schema-specification]: schema-specification.md "Schema specification"
[contributing-guide]: contributing-guide.md "Contributing guide"
[design-rationale-index]: design-rationale-index.md "Design rationale index"
[foss-principles]: foss-principles.md "Free and open source principles"
