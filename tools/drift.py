#!/usr/bin/env python3
"""Drift check — which pages are behind their source code.

Usage: docs-drift [DOCS_DIR] [SRC_DIR]   (defaults: docs, /src)

Reads each page's `sources` frontmatter (repo / branch / sha / committed / paths)
and, for each source repo found under SRC_DIR, checks whether the backing code
changed since the page was last verified:

  - sha still reachable -> `git log <sha>..<branch> -- <paths>`
  - sha rewritten away  -> `git log --since=<committed> <branch> -- <paths>`

A non-empty diff means the page is stale -> open a DOC-VERIFY (see
agent_docs/stewardship/enrichment-and-currency.md).

Offline: never fetches; assumes the clones under SRC_DIR are kept current by the
maintainer. Informational — always exits 0. Run via `make drift SRC=/path/to/code`.
"""
import sys
import os
import glob
import subprocess

try:
    import yaml
except ImportError:
    sys.exit("PyYAML not available — run via `make drift` (inside the container).")


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


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)


def main():
    docs = sys.argv[1] if len(sys.argv) > 1 else "docs"
    src = sys.argv[2] if len(sys.argv) > 2 else "/src"
    stale, skipped, checked = [], set(), 0

    for f in sorted(glob.glob(os.path.join(docs, "**", "*.md"), recursive=True)):
        with open(f, encoding="utf-8") as fh:
            sources = parse_frontmatter(fh.read()).get("sources") or []
        if not isinstance(sources, list):
            continue
        rel = os.path.relpath(f, docs)
        for s in sources:
            if not isinstance(s, dict) or not s.get("repo"):
                continue
            repo = s["repo"]
            branch = s.get("branch") or "main"
            sha, committed = s.get("sha"), s.get("committed")
            pathspec = ["--", *map(str, s["paths"])] if s.get("paths") else []
            repo_path = os.path.join(src, repo)
            if not os.path.isdir(os.path.join(repo_path, ".git")):
                skipped.add(repo)
                continue
            checked += 1
            reachable = bool(sha) and git(repo_path, "cat-file", "-e", str(sha)).returncode == 0
            if reachable:
                r = git(repo_path, "log", "--oneline", f"{sha}..{branch}", *pathspec)
                how = "since sha"
            elif committed:
                r = git(repo_path, "log", "--oneline", f"--since={committed}", branch, *pathspec)
                how = f"since {committed} (sha unreachable)"
            else:
                continue
            n = len([ln for ln in r.stdout.splitlines() if ln.strip()])
            if n:
                stale.append((rel, repo, n, how))

    if skipped:
        print(f"NOTE  no clone under {src} for: {', '.join(sorted(skipped))} "
              f"(mount it read-only to check — see source-of-truth.md)")
    for rel, repo, n, how in stale:
        print(f"STALE {rel}  <-  {repo}: {n} commit(s) {how}  -> open DOC-VERIFY")
    print(f"\n{checked} source-link(s) checked · {len(stale)} stale page-source(s)")


if __name__ == "__main__":
    main()
