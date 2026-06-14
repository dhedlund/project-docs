"""Tests for docs-check (tools/check.py). Run via `make test`."""
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]


def run_check(docs):
    return subprocess.run(
        [sys.executable, str(TOOLS / "check.py"), str(docs)],
        capture_output=True, text=True,
    )


def write(docs, name, body):
    p = docs / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body)


def test_valid_model_passes(tmp_path):
    docs = tmp_path / "docs"
    write(docs, "models/m.md",
          "---\ntitle: M\ntype: model\nstatus: active\nreviewed_confidence: 80\n"
          "sources:\n  - repo: r\n    branch: main\n---\n# M\n")
    r = run_check(docs)
    assert r.returncode == 0, r.stdout  # orphan model warns, but no errors


def test_missing_title_errors(tmp_path):
    docs = tmp_path / "docs"
    write(docs, "x.md",
          "---\ntype: glossary\nstatus: active\n---\n# X\n")
    r = run_check(docs)
    assert r.returncode == 1 and "missing required frontmatter 'title'" in r.stdout


def test_code_derived_requires_sources(tmp_path):
    docs = tmp_path / "docs"
    write(docs, "s.md", "---\ntitle: S\ntype: service\nstatus: active\n---\n# S\n")
    r = run_check(docs)
    assert r.returncode == 1 and "missing `sources`" in r.stdout


def test_stub_exempt_from_sources(tmp_path):
    docs = tmp_path / "docs"
    write(docs, "s.md", "---\ntitle: S\ntype: service\nstatus: stub\n---\n# S\n")
    r = run_check(docs)
    assert r.returncode == 0, r.stdout


def test_bool_confidence_errors(tmp_path):
    docs = tmp_path / "docs"
    write(docs, "g.md",
          "---\ntitle: G\ntype: glossary\nstatus: active\nreviewed_confidence: true\n---\n# G\n")
    r = run_check(docs)
    assert r.returncode == 1 and "reviewed_confidence" in r.stdout


def test_duplicate_stem_warns(tmp_path):
    docs = tmp_path / "docs"
    write(docs, "a/x.md", "---\ntitle: X1\ntype: glossary\nstatus: active\n---\n# X\n")
    write(docs, "b/x.md", "---\ntitle: X2\ntype: glossary\nstatus: active\n---\n# X\n")
    r = run_check(docs)
    assert "duplicate page stem 'x'" in r.stdout


def test_refs_must_be_list(tmp_path):
    docs = tmp_path / "docs"
    write(docs, "g.md",
          "---\ntitle: G\ntype: glossary\nstatus: active\nrefs: JIRA-1\n---\n# G\n")
    r = run_check(docs)
    assert "refs should be a list" in r.stdout
