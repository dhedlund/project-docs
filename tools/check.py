#!/usr/bin/env python3
"""Frontmatter + cross-link checks for the docs.

Usage: docs-check [DOCS_DIR]        (default: docs)

Complements `mkdocs build --strict` (which catches broken internal links and bad
nav). This catches what mkdocs won't: invalid/missing frontmatter, malformed
`sources` provenance, dangling relationship references, and orphan pages.

- ERRORS  (exit 1): things that should block — missing required frontmatter,
  out-of-range confidence, bad dates.
- WARNINGS (exit 0): things to surface but not block — dangling references
  (likely need a stub + backlog entry), orphans, soft `sources` issues.

Run via `make check` so it executes inside the toolkit container.
"""
import sys
import os
import glob
import datetime

try:
    import yaml
except ImportError:
    sys.exit("PyYAML not available — run via `make check` (inside the container).")

PAGE_TYPES = {
    "model", "service", "feature", "decision",
    "index", "overview", "domain", "datastore", "glossary",
}
STATUSES = {
    "active", "deprecated", "partial", "unknown", "stub",
    "proposed", "accepted", "superseded",
}
REL_FIELDS = [
    "related_models", "related_features", "related_services",
    "uses_services", "uses_models", "owned_models", "owned_by", "depends_on",
]


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, "no frontmatter block"
    end = text.find("\n---", 3)
    if end == -1:
        return None, "unterminated frontmatter block"
    try:
        return (yaml.safe_load(text[3:end]) or {}), None
    except yaml.YAMLError as e:
        return None, f"invalid YAML frontmatter: {e}"


def main():
    docs = sys.argv[1] if len(sys.argv) > 1 else "docs"
    files = sorted(glob.glob(os.path.join(docs, "**", "*.md"), recursive=True))
    errors, warnings = [], []
    pages = {}          # stem -> relpath
    meta_by_path = {}   # relpath -> meta

    for f in files:
        rel = os.path.relpath(f, docs)
        with open(f, encoding="utf-8") as fh:
            meta, err = parse_frontmatter(fh.read())
        if meta is None:
            warnings.append(f"{rel}: {err}")
            continue
        meta_by_path[rel] = meta
        pages.setdefault(os.path.splitext(os.path.basename(f))[0], rel)

        for k in ("title", "type", "status"):
            if not meta.get(k):
                errors.append(f"{rel}: missing required frontmatter '{k}'")
        if (t := meta.get("type")) and t not in PAGE_TYPES:
            warnings.append(f"{rel}: unknown type '{t}'")
        if (s := meta.get("status")) and s not in STATUSES:
            warnings.append(f"{rel}: unknown status '{s}'")

        rc = meta.get("reviewed_confidence")
        if rc not in (None, ""):
            if not (isinstance(rc, int) and 1 <= rc <= 100):
                errors.append(f"{rel}: reviewed_confidence must be an int 1-100, got {rc!r}")
        if lr := meta.get("last_reviewed"):
            try:
                datetime.date.fromisoformat(str(lr))
            except ValueError:
                errors.append(f"{rel}: last_reviewed not YYYY-MM-DD: {lr!r}")

        src = meta.get("sources")
        if src:
            if not isinstance(src, list):
                warnings.append(f"{rel}: sources should be a list")
            else:
                for i, e in enumerate(src):
                    if not isinstance(e, dict) or not e.get("repo"):
                        warnings.append(f"{rel}: sources[{i}] needs at least 'repo'")
                    elif not e.get("branch"):
                        warnings.append(f"{rel}: sources[{i}] missing 'branch' (record the canonical branch)")

    # Relationship graph: dangling references + orphans.
    referenced = set()
    for rel, meta in meta_by_path.items():
        for field in REL_FIELDS:
            vals = meta.get(field) or []
            if isinstance(vals, str):
                vals = [vals]
            for v in vals:
                name = str(v).strip()
                if not name:
                    continue
                referenced.add(name)
                if name not in pages:
                    warnings.append(f"{rel}: {field} -> '{name}' has no page (stub it or backlog a DOC-NEW)")

    for stem, rel in pages.items():
        meta = meta_by_path.get(rel, {})
        if meta.get("type") == "model" and stem not in referenced:
            warnings.append(f"{rel}: orphan (model referenced by no other page)")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{len(files)} pages · {len(errors)} error(s) · {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
