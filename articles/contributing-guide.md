---
id: contributing-guide
title: "Contributing guide"
version: 1.0.1
date: 2026-05-30
author: jsa
status: released
scope: libdrone
topic:
  - open-source-philosophy
personas:
  - 7.contributor
  - 5.student
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

libdrone is maintained on GitHub. Contributions follow
a fork-and-PR workflow. Hardware changes require a coupon validation result
before the PR is accepted. Documentation changes require the validator to pass
with zero errors. Vocabulary changes require ratification by jsa before any
article uses the new tag. The CERN OHL-S v2 licence means hardware design
modifications must be released under the same licence — your payload design
is yours, modifications to the platform are the community's.

---

## Concept

### What can be contributed

Three categories of contribution, each with different review requirements:

**Articles** — new articles or corrections to existing articles in the
3.0.0 corpus. Must pass `bin/validate_corpus.py` with zero errors. Must
respect atom boundaries — an article that expands beyond its topic boundary
will be asked to split. Must not duplicate content owned by an existing article.

**Hardware changes** — modifications to any FreeCAD parametric file, variable,
or printed part geometry. Require a physical coupon validation result attached
to the PR demonstrating that the changed geometry passes the relevant coupon
gates. A PR that only changes CAD files without a coupon result will not be
merged.

**Firmware and software** — Betaflight configuration changes, payload firmware
additions, validator improvements, tooling. These follow standard software
contribution conventions: tested, commented, with a clear description of what
changed and why.

### CERN OHL-S v2 and your IP

The "Strongly Reciprocal" clause means modifications to libdrone's hardware
designs must be released under CERN OHL-S v2. This applies to changes to the
frame geometry, the Platform, the Backplane, or any structural component.

It does not apply to payloads. A payload built to the GX12 interface standard
is a separate design. Your payload firmware, your sensor integration, your
mechanical mast design — these are yours under whatever licence you choose.
Connecting to libdrone via the GX12 interface does not create a licence
obligation on your payload.

---

## Reference

### Repository structure

    libdrone/
      ld300/
        articles/          # corpus articles, flat (no per-domain subfolders)
        _schema/           # LD_-_Knowledge_Schema_v300.md, tag-vocabularies.yaml
        bin/               # validate_corpus.py
        skeletons/         # skeleton documents
      hardware/            # FreeCAD files, DXF exports
      firmware/            # Betaflight diffs, payload firmware
      docs/                # legacy 2.x frozen documents

### Contribution workflow

      # 1. Fork the repository on GitHub
      # 2. Clone your fork
      git clone https://github.com/libdrone/libdrone.git

      # 3. Create a branch
      git checkout -b contrib/article-thermal-soaring

      # 4. Write and validate
      python3 ld300/bin/validate_corpus.py ld300/articles/
      # Must exit 0 before committing

      # 5. Commit with a clear message
      git commit -m "corpus: add thermal-soaring article (physics-flight-mechanics domain)"

      # 6. Push and open a PR on GitHub
      git push origin contrib/article-thermal-soaring

### PR requirements by contribution type

| Type | Required | Reviewer |
|---|---|---|
| New article | Validator passes, atom boundary respected | jsa |
| Article correction | Validator passes, change justified in PR description | jsa |
| New vocabulary tag | Tag ratification from jsa BEFORE the PR | jsa |
| Hardware geometry | Coupon validation result attached, FreeCAD file included | jsa |
| Firmware change | Tested on hardware, configuration diff included | jsa |

### Vocabulary change process

1. Open an issue on GitHub describing: the new tag, which existing articles
   would be retroactively tagged, and why no existing tag covers it
2. Wait for ratification (comment from jsa on the issue)
3. Update `_schema/tag-vocabularies.yaml` with a dated comment
4. Retroactively tag all relevant existing articles
5. Then write the new article using the tag
6. All five steps in one PR

Never use a tag that does not exist in `tag-vocabularies.yaml` — the validator
will reject the article.

---

## Procedure

### Writing a new article from scratch

1. Identify the domain: which topic slug from `tag-vocabularies.yaml`?
2. Check the corpus: does an article already own this topic? If yes,
   is this a correction/extension (edit existing) or a new adjacent topic
   (new article)?
3. Create the file: `ld300/articles/ARTICLE-ID.md`
4. Write all six sections. Never omit a section — use `<!-- not applicable -->`
   if genuinely not applicable.
5. Run the validator: `python3 ld300/bin/validate_corpus.py ld300/articles/ARTICLE-ID.md`
6. Fix any errors. Run again.
7. Run with `--graph`: `python3 ld300/bin/validate_corpus.py ld300/articles/ --graph`
8. Review broken connections: is each referenced ID either already in the
   corpus, or a documented future article? If neither — fix the connection.
9. Open the PR.

### Correcting a factual error

1. Identify the owning article (the article whose topic includes the incorrect fact).
2. Make the correction in that article only — do not correct the same fact in
   multiple articles (that would create duplicate ownership).
3. Bump the article `version` in frontmatter (patch increment: 1.0.0 → 1.0.1).
4. Add a note to the PR description explaining what was wrong and what the
   correct value is, with a reference to the source.

---

## Rationale

### Why hardware PRs require physical coupon results

A FreeCAD file change is not a hardware change until it has been printed and
tested. Parametric geometry can appear correct in CAD and fail in print due
to dimensional accuracy, layer adhesion, or support removal artefacts.
The coupon system exists precisely to catch these failures before they
propagate into production builds. Accepting a hardware PR based only on
CAD review bypasses the entire validation architecture.

### Why vocabulary ratification must precede the article

A tag that appears in one article but not in `tag-vocabularies.yaml` fails
validation — which means the article cannot be committed. The ratification
requirement before writing forces the contributor to think about whether the
new concept actually deserves its own vocabulary entry or whether an existing
tag is sufficient. Most proposed new tags turn out to be covered by existing
ones after five minutes of reflection.

---

## Connections

requires:
  - [[foss-principles]]
  - [[foss-stack-libdrone]]
related:
  - [[vendor-lock-in]]
  - [[coupon-validation]]
leads_to:
  - [[foss-stack-libdrone]]


[foss-principles]: foss-principles.md "Free and open source principles"
[foss-stack-libdrone]: foss-stack-libdrone.md "FOSS stack in libdrone"
[vendor-lock-in]: vendor-lock-in.md "Vendor lock-in"
[coupon-validation]: coupon-validation.md "Coupon validation"
