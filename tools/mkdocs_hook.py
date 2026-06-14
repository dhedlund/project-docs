"""mkdocs build hook — surfaces page metadata automatically.

Two jobs, both derived from frontmatter so authors never hand-maintain them:

1. A **status badge** (confidence / last-reviewed / status) at the top of each
   content page.
2. A **"Used by"** backlinks section at the bottom — the reverse of every
   `related_*` / `uses_*` / `owned_*` / `depends_on` reference, so links are
   maintained in one direction only.

Baked into the toolkit image; referenced from mkdocs.yml as:
    hooks:
      - /usr/local/lib/docs/hook.py
"""
import os
import glob

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

CONTENT_TYPES = {"model", "service", "feature", "glossary", "decision"}
REL_FIELDS = [
    "related_models", "related_features", "related_services",
    "uses_services", "uses_models", "owned_models", "owned_by", "depends_on",
]

_index = {}  # docs_dir -> {"refs": {name: [(src_uri, title)]}}


def _parse_frontmatter(text):
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(text[3:end]) or {}
    except yaml.YAMLError:
        return {}


def _build_index(docs_dir):
    refs = {}
    for f in glob.glob(os.path.join(docs_dir, "**", "*.md"), recursive=True):
        src = os.path.relpath(f, docs_dir)
        with open(f, encoding="utf-8") as fh:
            meta = _parse_frontmatter(fh.read())
        title = meta.get("title") or os.path.splitext(os.path.basename(f))[0]
        for field in REL_FIELDS:
            vals = meta.get(field) or []
            if isinstance(vals, str):
                vals = [vals]
            for v in vals:
                name = str(v).strip()
                if name:
                    refs.setdefault(name, []).append((src, title))
    return {"refs": refs}


def on_page_markdown(markdown, page, config, files):
    if yaml is None:
        return markdown
    docs_dir = config["docs_dir"]
    idx = _index.get(docs_dir) or _index.setdefault(docs_dir, _build_index(docs_dir))
    meta = page.meta or {}
    out = markdown

    # 1. Status badge (content pages only), inserted just after the H1.
    if meta.get("type") in CONTENT_TYPES:
        bits = []
        conf = meta.get("reviewed_confidence")
        if isinstance(conf, int):
            bits.append(f"**Confidence:** {conf}/100")
        if meta.get("last_reviewed"):
            bits.append(f"**Last reviewed:** {meta['last_reviewed']}")
        if meta.get("status"):
            bits.append(f"**Status:** {meta['status']}")
        if bits:
            badge = '!!! info ""\n    ' + " · ".join(bits)
            lines = out.split("\n")
            at = next((i + 1 for i, ln in enumerate(lines) if ln.startswith("# ")), 0)
            lines.insert(at, "\n" + badge + "\n")
            out = "\n".join(lines)

    # 2. "Used by" backlinks (reverse of the relationship fields).
    cur = page.file.src_uri
    stem = os.path.splitext(os.path.basename(cur))[0]
    seen, uniq = set(), []
    for src, title in idx["refs"].get(stem, []):
        if src != cur and src not in seen:
            seen.add(src)
            uniq.append((src, title))
    if uniq:
        links = [
            f"- [{title}]({os.path.relpath(src, os.path.dirname(cur))})"
            for src, title in sorted(uniq, key=lambda x: x[1].lower())
        ]
        out += "\n\n## Used by\n\n" + "\n".join(links) + "\n"

    return out
