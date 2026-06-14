"""Tests for the mkdocs build hook helpers (tools/mkdocs_hook.py)."""
import importlib.util
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("mkdocs_hook", TOOLS / "mkdocs_hook.py")
hook = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hook)


def test_first_h1_skips_fenced_code():
    # a `# ...` inside a code fence must not be mistaken for the page H1
    lines = ["```bash", "# not a heading", "```", "# Real Heading", "body"]
    assert hook._first_h1_outside_fence(lines) == 3


def test_first_h1_plain():
    assert hook._first_h1_outside_fence(["# Title", "x"]) == 0


def test_first_h1_none():
    assert hook._first_h1_outside_fence(["no heading", "here"]) is None


def test_provenance_formats_repo_sha_date():
    s = [{"repo": "r", "sha": "abc123", "committed": "2026-05-30"}]
    assert hook._provenance(s) == "r@abc123 (2026-05-30)"


def test_provenance_multiple_repos():
    s = [{"repo": "a", "sha": "1"}, {"repo": "b"}]
    assert hook._provenance(s) == "a@1, b"


def test_provenance_non_list_is_empty():
    assert hook._provenance("nope") == ""
    assert hook._provenance(None) == ""
