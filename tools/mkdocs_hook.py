"""mkdocs build hook — surfaces page metadata automatically.

Two jobs, both derived from frontmatter so authors never hand-maintain them:

1. A **status badge** (confidence / last-reviewed / status / provenance) near the
   top of each content page.
2. A **"Related pages"** block at the bottom, grouped by relationship type — the
   reverse of every `related_*` / `uses_*` / `owned_*` / `depends_on` reference, so
   links are maintained in one direction only.

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

CONTENT_TYPES = {
    "model", "service", "feature", "glossary", "decision", "datastore",
    "domain", "capability", "options", "flow", "roles",
    "api", "webhook", "sdk", "integration", "surface", "auth",
}

# Each relationship field, and the label its *reverse* gets on the target page.
FIELD_LABELS = {
    "uses_services": "Used by",
    "uses_models": "Used by",
    "owned_models": "Owned by",
    "owned_by": "Owns",
    "depends_on": "Depended on by",
    "domain": "In this domain",
    "surfaces": "Surfaced here",
    "related_models": "Related",
    "related_features": "Related",
    "related_services": "Related",
}
# Order in which grouped sections are emitted.
LABEL_ORDER = ["Used by", "Owned by", "Depended on by", "In this domain",
               "Surfaced here", "Owns", "Related"]

_index = {}  # docs_dir -> {"refs": {name: [(src_uri, title, label)]}}


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
        for field, label in FIELD_LABELS.items():
            vals = meta.get(field) or []
            if isinstance(vals, str):
                vals = [vals]
            for v in vals:
                name = str(v).strip()
                if name:
                    refs.setdefault(name, []).append((src, title, label))
    return {"refs": refs}


def _first_h1_outside_fence(lines):
    """Index of the first `# ` heading that is not inside a fenced code block."""
    in_fence = False
    for i, ln in enumerate(lines):
        stripped = ln.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if not in_fence and ln.startswith("# "):
            return i
    return None


def _provenance(sources):
    if not isinstance(sources, list):
        return ""
    parts = []
    for s in sources:
        if isinstance(s, dict) and s.get("repo"):
            tag = s["repo"]
            if s.get("sha"):
                tag += f"@{s['sha']}"
            if s.get("committed"):
                tag += f" ({s['committed']})"
            parts.append(tag)
    return ", ".join(parts)


def on_page_markdown(markdown, page, config, files):
    if yaml is None:
        return markdown
    docs_dir = config["docs_dir"]
    idx = _index.get(docs_dir) or _index.setdefault(docs_dir, _build_index(docs_dir))
    meta = page.meta or {}
    out = markdown

    # 1. Status badge (content pages only), inserted after the first real H1.
    if meta.get("type") in CONTENT_TYPES:
        paras = []
        bits = []
        conf = meta.get("reviewed_confidence")
        if isinstance(conf, int) and not isinstance(conf, bool):
            bits.append(f"**Confidence:** {conf}/100")
        if meta.get("last_reviewed"):
            bits.append(f"**Last reviewed:** {meta['last_reviewed']}")
        if meta.get("status"):
            bits.append(f"**Status:** {meta['status']}")
        if bits:
            paras.append(" · ".join(bits))
        prov = _provenance(meta.get("sources"))
        if prov:
            paras.append(f"**Verified against:** {prov}")
        if paras:
            badge_lines = ['!!! info ""']
            for i, p in enumerate(paras):
                if i > 0:
                    badge_lines.append("")
                badge_lines.append("    " + p)
            badge = "\n".join(badge_lines)
            lines = out.split("\n")
            h1 = _first_h1_outside_fence(lines)
            at = (h1 + 1) if h1 is not None else 0
            lines.insert(at, "\n" + badge + "\n")
            out = "\n".join(lines)

    # 2. "Related pages" — reverse links, grouped by relationship type.
    cur = page.file.src_uri
    stem = os.path.splitext(os.path.basename(cur))[0]
    groups = {}
    seen = set()
    for src, title, label in idx["refs"].get(stem, []):
        if src == cur or (label, src) in seen:
            continue
        seen.add((label, src))
        groups.setdefault(label, []).append((src, title))
    if groups:
        section = ["\n\n## Related pages\n"]
        for label in LABEL_ORDER:
            items = groups.get(label)
            if not items:
                continue
            links = ", ".join(
                f"[{t}]({os.path.relpath(s, os.path.dirname(cur))})"
                for s, t in sorted(items, key=lambda x: x[1].lower())
            )
            section.append(f"**{label}:** {links}\n")
        out += "\n".join(section) + "\n"

    return out
