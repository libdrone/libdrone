#!/usr/bin/env python3
"""
libdrone 3.0.0 — Knowledge Corpus Validator
Usage:
  python3 validate_corpus.py articles/topic/article.md   # validate one article
  python3 validate_corpus.py articles/                   # validate all articles
  python3 validate_corpus.py --graph articles/           # validate + check connections
"""

import sys
import os
import re
import argparse
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)

SCHEMA_DIR = Path(__file__).parent.parent / "_schema"
VOCAB_FILE = SCHEMA_DIR / "tag-vocabularies.yaml"
ARTICLES_DIR = Path(__file__).parent.parent / "articles"

REQUIRED_FIELDS = ["id", "title", "version", "date", "author", "status",
                   "scope", "topic", "personas", "platform", "lang", "licence"]

REQUIRED_SECTIONS = ["Summary", "Concept", "Reference", "Procedure", "Rationale", "Connections"]

NOT_APPLICABLE = "<!-- not applicable -->"


def load_vocabularies():
    if not VOCAB_FILE.exists():
        print(f"WARNING: Vocabulary file not found at {VOCAB_FILE}. Skipping vocabulary checks.")
        return {}
    with open(VOCAB_FILE) as f:
        return yaml.safe_load(f)


def parse_frontmatter(content):
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return None, content
    try:
        fm = yaml.safe_load(match.group(1))
        body = content[match.end():]
        return fm, body
    except yaml.YAMLError as e:
        return {"_parse_error": str(e)}, ""


def get_sections(body):
    found = []
    for line in body.split("\n"):
        m = re.match(r"^## (.+)$", line)
        if m:
            found.append(m.group(1).strip())
    return found


def get_connections(body):
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
            # Handle fenced ```yaml block (legacy format)
            if line.strip() == "```yaml":
                in_yaml_block = True
                continue
            if line.strip() == "```" and in_yaml_block:
                in_yaml_block = False
                try:
                    parsed = yaml.safe_load("\n".join(yaml_lines))
                    if parsed:
                        connections.update({k: v or [] for k, v in parsed.items()})
                except yaml.YAMLError:
                    pass
                yaml_lines = []
                continue
            if in_yaml_block:
                yaml_lines.append(line)
                continue
            # Handle unfenced YAML (new format) — collect non-blank lines
            if line.strip() and not line.strip().startswith("#"):
                yaml_lines.append(line)

    # Parse any unfenced yaml_lines collected after the loop
    if yaml_lines and not in_yaml_block:
        try:
            parsed = yaml.safe_load("\n".join(yaml_lines))
            if parsed:
                connections.update({k: v or [] for k, v in parsed.items()})
        except yaml.YAMLError:
            pass

    return connections


def collect_all_ids(articles_dir):
    ids = set()
    for md_file in Path(articles_dir).rglob("*.md"):
        with open(md_file) as f:
            content = f.read()
        fm, _ = parse_frontmatter(content)
        if fm and "id" in fm:
            ids.add(fm["id"])
    return ids


def validate_article(filepath, vocab, known_ids=None):
    errors = []
    warnings = []
    filepath = Path(filepath)

    if not filepath.exists():
        return [f"File not found: {filepath}"], []

    with open(filepath) as f:
        content = f.read()

    fm, body = parse_frontmatter(content)

    if fm is None:
        return ["No frontmatter block found — article must begin with ---"], []

    if "_parse_error" in fm:
        return [f"Frontmatter YAML parse error: {fm['_parse_error']}"], []

    # Required fields
    for field in REQUIRED_FIELDS:
        if field not in fm or fm[field] is None or fm[field] == "":
            errors.append(f"Missing required field: {field}")

    # Vocabulary checks
    if vocab:
        if "status" in fm and fm["status"] not in vocab.get("statuses", []):
            errors.append(f"Invalid status '{fm['status']}' — not in vocabulary")

        if "scope" in fm and fm["scope"] not in vocab.get("scopes", []):
            errors.append(f"Invalid scope '{fm['scope']}' — not in vocabulary")

        if "topic" in fm:
            for t in (fm["topic"] if isinstance(fm["topic"], list) else [fm["topic"]]):
                if t not in vocab.get("topics", []):
                    errors.append(f"Invalid topic '{t}' — not in vocabulary")

        if "personas" in fm:
            for p in (fm["personas"] if isinstance(fm["personas"], list) else [fm["personas"]]):
                if p not in vocab.get("personas", []):
                    errors.append(f"Invalid persona '{p}' — not in vocabulary")

        if "platform" in fm:
            for pl in (fm["platform"] if isinstance(fm["platform"], list) else [fm["platform"]]):
                if pl not in vocab.get("platforms", []):
                    errors.append(f"Invalid platform '{pl}' — not in vocabulary")

    # Deprecated articles must have replaced_by
    if fm.get("status") == "deprecated":
        if not fm.get("replaced_by"):
            errors.append("Deprecated article must have 'replaced_by' field pointing to replacement")

    # Section checks
    sections_found = get_sections(body)
    for section in REQUIRED_SECTIONS:
        if section not in sections_found:
            errors.append(f"Missing required section: ## {section}")

    # Check sections have content (not just heading with nothing)
    for section in REQUIRED_SECTIONS:
        pattern = rf"## {section}\s*\n(\s*\n)*(?=## |\Z)"
        if re.search(pattern, body):
            errors.append(f"Section '## {section}' is empty — use '{NOT_APPLICABLE}' if not applicable")

    # Connection graph integrity
    if known_ids is not None:
        connections = get_connections(body)
        for conn_type, ids in connections.items():
            for ref_id in ids:
                if not isinstance(ref_id, str):
                    continue
                ref_id = ref_id.strip()
                # Strip wikilink brackets if present: [[id]] → id
                ref_id = re.sub(r'^\[\[(.+)\]\]$', r'\1', ref_id)
                if ref_id not in known_ids:
                    errors.append(f"Broken connection in '{conn_type}': article '{ref_id}' not found in corpus")

    # Version format
    if "version" in fm:
        if not re.match(r"^\d+\.\d+\.\d+$", str(fm["version"])):
            warnings.append(f"Version '{fm['version']}' should follow semantic versioning (e.g. 1.0.0)")

    # ID format
    if "id" in fm:
        if not re.match(r"^[a-z0-9-]+$", str(fm["id"])):
            errors.append(f"ID '{fm['id']}' must be kebab-case (lowercase letters, numbers, hyphens only)")

    return errors, warnings


def validate_path(target, check_graph=False):
    vocab = load_vocabularies()
    target = Path(target)
    files = []

    if target.is_file():
        files = [target]
    elif target.is_dir():
        # Section landing pages (e.g. articles/index.md) are not atoms — skip them.
        files = [f for f in target.rglob("*.md") if f.name != "index.md"]
    else:
        print(f"ERROR: {target} is not a file or directory")
        sys.exit(1)

    known_ids = None
    if check_graph:
        known_ids = collect_all_ids(ARTICLES_DIR if ARTICLES_DIR.exists() else target)

    total = 0
    failed = 0

    for filepath in sorted(files):
        errors, warnings = validate_article(filepath, vocab, known_ids)
        total += 1
        rel = filepath.relative_to(Path.cwd()) if filepath.is_absolute() else filepath

        if errors or warnings:
            if errors:
                failed += 1
                print(f"\n✗ {rel}")
                for e in errors:
                    print(f"  ERROR   {e}")
                for w in warnings:
                    print(f"  WARNING {w}")
            else:
                print(f"\n~ {rel}")
                for w in warnings:
                    print(f"  WARNING {w}")
        else:
            print(f"  ✓ {rel}")

    print(f"\n{'─'*60}")
    print(f"Validated {total} article(s). {failed} failed.")
    return failed == 0


def main():
    parser = argparse.ArgumentParser(description="libdrone corpus validator")
    parser.add_argument("target", help="Article file or articles directory")
    parser.add_argument("--graph", action="store_true",
                        help="Also validate connection graph integrity")
    args = parser.parse_args()

    success = validate_path(args.target, check_graph=args.graph)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
