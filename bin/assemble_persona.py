#!/usr/bin/env python3
"""
libdrone 3.0.0 — Persona Document Assembler

Walks the corpus graph according to a persona traversal definition and
produces a single assembled Markdown document.

Usage:
  python3 bin/assemble_persona.py --persona 1.builder
  python3 bin/assemble_persona.py --persona 6.evaluator --output out.md
  python3 bin/assemble_persona.py --list-personas
  python3 bin/assemble_persona.py --persona 1.builder --skeleton-only
  python3 bin/assemble_persona.py --persona 1.builder --atoms-only

Skeleton articles (skeleton: true in frontmatter) are included as full prose
documents — their narrative connects the atoms. Atom articles are included
with their section content.

The assembler walks the traversal order defined in TRAVERSALS below, then
appends any additionally reachable atoms by following leads_to edges from
the traversal articles (BFS, depth-limited).
"""

import sys
import re
import argparse
from pathlib import Path
from collections import deque

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Path configuration
# ---------------------------------------------------------------------------
REPO_ROOT   = Path(__file__).parent.parent
ARTICLES_DIR = REPO_ROOT / "articles"
SKELETONS_DIR = REPO_ROOT / "skeletons"
SCHEMA_DIR  = REPO_ROOT / "_schema"
VOCAB_FILE  = SCHEMA_DIR / "tag-vocabularies.yaml"

# ---------------------------------------------------------------------------
# Persona traversal definitions
# Mirrors Appendix B of LD_-_Knowledge_Schema_v310.md
# ---------------------------------------------------------------------------
TRAVERSALS = {
    "1.builder": [
        "prep-and-parametrics",
        "procurement",
        "coupon-validation",
        "print-production",
        "airframe-integration",
        "electronics-installation",
        "software-commissioning",
        "acceptance-validation",
        "maiden-flight",
    ],
    "2.operator": [
        "pre-flight-check",
        "post-flight-check",
        "scheduled-maintenance",
        "corrective-maintenance",
        "emergency-procedures",
    ],
    "3.payload-dev": [
        "gx12-icd",
        "payload-sdk",
        "lcm1-spec",
        "psb1-build-guide",
    ],
    "4.workshop": [
        "why-build-a-drone",
        "procurement",
        "print-production",
        "airframe-integration",
        "electronics-installation",
        "software-commissioning",
        "first-flight",
    ],
    "5.student": [
        # Domain-level traversal — served primarily by sk-engineering-101.
        # Article IDs below are domain entry points; the skeleton provides
        # the full arc through each domain.
        "sk-engineering-101",
        "lift-and-thrust",
        "closed-loop-control",
        "brushless-motors",
        "lipo-batteries",
        "imu-gyroscope",
        "sandwich-structure",
        "emc-noise-sources",
    ],
    "6.evaluator": [
        "platform-overview",
        "resilience-use-cases",
        "bom-summary",
        "regulatory-overview",
    ],
    "7.contributor": [
        "platform-architecture",
        "schema-specification",
        "design-rationale-index",
        "contributing-guide",
    ],
    "8.architect": None,  # Full corpus access — no prescribed traversal
    "9.defense": [
        "threat-assessment",
        "iff-architecture",
        "operational-security",
        "platform-selection",
    ],
}

PERSONA_NAMES = {
    "1.builder":    "Builder",
    "2.operator":   "Operator",
    "3.payload-dev": "Payload Developer",
    "4.workshop":   "Workshop Participant",
    "5.student":    "Student",
    "6.evaluator":  "Evaluator",
    "7.contributor": "Contributor",
    "8.architect":  "Architect",
    "9.defense":    "Defense Analyst",
}


# ---------------------------------------------------------------------------
# Article loading
# ---------------------------------------------------------------------------

def find_article(article_id: str) -> Path | None:
    """Find an article file by ID, searching articles/ and skeletons/."""
    for directory in [ARTICLES_DIR, SKELETONS_DIR]:
        if not directory.exists():
            continue
        # Flat search first
        candidate = directory / f"{article_id}.md"
        if candidate.exists():
            return candidate
        # Recursive search (domain subdirectories)
        for path in directory.rglob(f"{article_id}.md"):
            return path
    return None


def parse_article(path: Path) -> tuple[dict, str]:
    """Return (frontmatter_dict, body_text) for an article file."""
    content = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not m:
        return {}, content
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        fm = {}
    body = content[m.end():]
    return fm, body


def is_skeleton(fm: dict) -> bool:
    """Return True if the article is a skeleton document."""
    return bool(fm.get("skeleton"))


def get_connections(body: str) -> dict:
    """Extract the Connections YAML block from article body."""
    connections = {"requires": [], "related": [], "leads_to": []}
    in_connections = False
    in_yaml_block = False
    yaml_lines = []

    for line in body.split("\n"):
        if re.match(r"^## Connections", line):
            in_connections = True
            continue
        if in_connections and re.match(r"^## ", line):
            break
        if in_connections:
            if line.strip() == "```yaml":
                in_yaml_block = True
                continue
            if line.strip() == "```" and in_yaml_block:
                in_yaml_block = False
                try:
                    parsed = yaml.safe_load("\n".join(yaml_lines))
                    if parsed:
                        for k in connections:
                            v = parsed.get(k, [])
                            connections[k] = v if isinstance(v, list) else ([v] if v else [])
                except yaml.YAMLError:
                    pass
                yaml_lines = []
                continue
            if in_yaml_block:
                yaml_lines.append(line)

    return connections


# ---------------------------------------------------------------------------
# Corpus index
# ---------------------------------------------------------------------------

def build_corpus_index() -> dict[str, Path]:
    """Return {article_id: path} for all articles and skeletons."""
    index = {}
    for directory in [ARTICLES_DIR, SKELETONS_DIR]:
        if not directory.exists():
            continue
        for path in directory.rglob("*.md"):
            fm, _ = parse_article(path)
            article_id = fm.get("id")
            if article_id:
                index[article_id] = path
    return index


# ---------------------------------------------------------------------------
# Assembler
# ---------------------------------------------------------------------------

def extract_section(body: str, section_name: str) -> str:
    """Extract the content of a named ## section from body."""
    pattern = rf"## {re.escape(section_name)}\s*\n(.*?)(?=\n## |\Z)"
    m = re.search(pattern, body, re.DOTALL)
    if not m:
        return ""
    return m.group(1).strip()


def render_skeleton(article_id: str, fm: dict, body: str) -> str:
    """Render a skeleton article as a standalone narrative section."""
    title = fm.get("title", article_id)
    lines = [f"# {title}", ""]

    # Include the full body, stripping the Connections section
    # (connections are internal plumbing, not reader content)
    clean_body = re.sub(r"\n## Connections.*", "", body, flags=re.DOTALL)
    lines.append(clean_body.strip())
    lines.append("")
    return "\n".join(lines)


def render_atom(article_id: str, fm: dict, body: str, include_rationale: bool = False) -> str:
    """Render an atom article with its core sections."""
    title = fm.get("title", article_id)
    lines = [f"## {title}", ""]

    summary = extract_section(body, "Summary")
    if summary and summary != "<!-- not applicable -->":
        lines.append(summary)
        lines.append("")

    concept = extract_section(body, "Concept")
    if concept and concept != "<!-- not applicable -->":
        lines.append("### Background")
        lines.append(concept)
        lines.append("")

    reference = extract_section(body, "Reference")
    if reference and reference != "<!-- not applicable -->":
        lines.append("### Reference")
        lines.append(reference)
        lines.append("")

    procedure = extract_section(body, "Procedure")
    if procedure and procedure != "<!-- not applicable -->":
        lines.append("### Procedure")
        lines.append(procedure)
        lines.append("")

    if include_rationale:
        rationale = extract_section(body, "Rationale")
        if rationale and rationale != "<!-- not applicable -->":
            lines.append("### Rationale")
            lines.append(rationale)
            lines.append("")

    return "\n".join(lines)


def assemble(
    persona: str,
    corpus: dict[str, Path],
    include_skeletons: bool = True,
    include_atoms: bool = True,
    include_rationale: bool = False,
    expand_graph: bool = False,
) -> str:
    """
    Assemble a persona document.

    Args:
        persona: Persona ID (e.g. '1.builder')
        corpus: {article_id: path} index
        include_skeletons: Include skeleton articles (full narrative)
        include_atoms: Include atom articles (structured content)
        include_rationale: Include Rationale sections in atoms
        expand_graph: Follow leads_to edges beyond the base traversal (BFS)
    """
    traversal = TRAVERSALS.get(persona)
    persona_name = PERSONA_NAMES.get(persona, persona)

    if traversal is None and persona == "8.architect":
        # Full corpus — all articles sorted by topic
        traversal = sorted(corpus.keys())
    elif traversal is None:
        print(f"ERROR: No traversal defined for persona '{persona}'")
        sys.exit(1)

    # Build ordered list of article IDs to include
    seen = set()
    ordered_ids = []

    queue = deque(traversal)
    while queue:
        article_id = queue.popleft()
        if article_id in seen:
            continue
        seen.add(article_id)
        if article_id in corpus:
            ordered_ids.append(article_id)
            if expand_graph:
                _, body = parse_article(corpus[article_id])
                conns = get_connections(body)
                for next_id in conns.get("leads_to", []):
                    if next_id not in seen:
                        queue.append(next_id)
        else:
            print(f"  WARNING: Article '{article_id}' in traversal not found in corpus",
                  file=sys.stderr)

    # Build output
    from datetime import date
    today = date.today().isoformat()

    lines = [
        f"# libdrone — {persona_name} Guide",
        f"",
        f"*Assembled from the libdrone 3.0.0 knowledge corpus on {today}.*",
        f"*Persona: {persona} — {persona_name}*",
        f"",
        "---",
        "",
    ]

    skeletons_included = 0
    atoms_included = 0

    for article_id in ordered_ids:
        path = corpus[article_id]
        fm, body = parse_article(path)

        if is_skeleton(fm):
            if include_skeletons:
                lines.append(render_skeleton(article_id, fm, body))
                lines.append("---")
                lines.append("")
                skeletons_included += 1
        else:
            if include_atoms:
                lines.append(render_atom(article_id, fm, body,
                                         include_rationale=include_rationale))
                lines.append("---")
                lines.append("")
                atoms_included += 1

    lines.append(f"*End of document. {skeletons_included} skeletons, "
                 f"{atoms_included} atoms included.*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="libdrone persona document assembler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--persona", "-p",
                        help="Persona ID (e.g. 1.builder, 6.evaluator)")
    parser.add_argument("--output", "-o",
                        help="Output file path (default: stdout)")
    parser.add_argument("--list-personas", action="store_true",
                        help="List available personas and exit")
    parser.add_argument("--skeleton-only", action="store_true",
                        help="Include only skeleton documents (omit atoms)")
    parser.add_argument("--atoms-only", action="store_true",
                        help="Include only atom documents (omit skeletons)")
    parser.add_argument("--with-rationale", action="store_true",
                        help="Include Rationale sections in atoms")
    parser.add_argument("--expand", action="store_true",
                        help="Expand graph: follow leads_to edges beyond base traversal")

    args = parser.parse_args()

    if args.list_personas:
        print("Available personas:")
        for pid, name in PERSONA_NAMES.items():
            traversal = TRAVERSALS.get(pid)
            count = len(traversal) if traversal else "full corpus"
            print(f"  {pid:15}  {name:25}  ({count} traversal steps)")
        sys.exit(0)

    if not args.persona:
        parser.print_help()
        sys.exit(1)

    if args.persona not in TRAVERSALS:
        print(f"ERROR: Unknown persona '{args.persona}'")
        print(f"Run with --list-personas to see available options")
        sys.exit(1)

    print(f"Building corpus index...", file=sys.stderr)
    corpus = build_corpus_index()
    print(f"  Found {len(corpus)} articles", file=sys.stderr)

    include_skeletons = not args.atoms_only
    include_atoms = not args.skeleton_only

    print(f"Assembling document for persona: {args.persona}...", file=sys.stderr)
    document = assemble(
        persona=args.persona,
        corpus=corpus,
        include_skeletons=include_skeletons,
        include_atoms=include_atoms,
        include_rationale=args.with_rationale,
        expand_graph=args.expand,
    )

    if args.output:
        Path(args.output).write_text(document, encoding="utf-8")
        print(f"  Written to: {args.output}", file=sys.stderr)
    else:
        print(document)


if __name__ == "__main__":
    main()
