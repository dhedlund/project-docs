#!/usr/bin/env python3
"""Coverage & staleness report for the docs.

Usage: docs-report [DOCS_DIR]   (default: docs)

Surfaces what the confidence/freshness frontmatter is *for*: which content pages
are low-confidence or stale, so an audit pass knows where to look first. Sorted
lowest-confidence (then stalest) first. Informational — always exits 0.
Run via `make report`.
"""
import sys
import os
import glob
import datetime

try:
    import yaml
except ImportError:
    sys.exit("PyYAML not available — run via `make report` (inside the container).")

CONTENT_TYPES = {"model", "service", "feature"}
LOW_CONF = 50
STALE_DAYS = 90


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(text[3:end]) or {}
    except yaml.YAMLError:
        return {}


def main():
    docs = sys.argv[1] if len(sys.argv) > 1 else "docs"
    today = datetime.date.today()
    rows = []
    for f in sorted(glob.glob(os.path.join(docs, "**", "*.md"), recursive=True)):
        with open(f, encoding="utf-8") as fh:
            meta = parse_frontmatter(fh.read())
        if meta.get("type") not in CONTENT_TYPES:
            continue
        rel = os.path.relpath(f, docs)
        conf = meta.get("reviewed_confidence")
        conf = conf if isinstance(conf, int) and not isinstance(conf, bool) else None
        lr = meta.get("last_reviewed")
        age = None
        if lr:
            try:
                age = (today - datetime.date.fromisoformat(str(lr))).days
            except ValueError:
                pass
        rows.append((rel, meta.get("status", "?"), conf, lr, age))

    # Unscored first (most urgent), then lowest confidence, then stalest.
    rows.sort(key=lambda r: (r[2] if r[2] is not None else -1, -(r[4] or 0)))

    print(f"{'conf':>4}  {'reviewed':<12} {'age':>5}  {'status':<10} page")
    print("-" * 66)
    low = stale = 0
    for rel, status, conf, lr, age in rows:
        c = str(conf) if conf is not None else "—"
        a = f"{age}d" if age is not None else "—"
        flag = ""
        if conf is None:
            low += 1
            flag += " [unscored]"
        elif conf < LOW_CONF:
            low += 1
            flag += " [low]"
        if age is not None and age > STALE_DAYS:
            stale += 1
            flag += " [stale]"
        print(f"{c:>4}  {str(lr or '—'):<12} {a:>5}  {status:<10} {rel}{flag}")
    print("-" * 66)
    print(f"{len(rows)} content pages · {low} below conf {LOW_CONF} · {stale} older than {STALE_DAYS}d")


if __name__ == "__main__":
    main()
