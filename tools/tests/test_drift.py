"""Tests for docs-drift (tools/drift.py) against a real throwaway git repo."""
import os
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
}


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True,
                   capture_output=True, env=GIT_ENV)


def head_sha(repo):
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
                          capture_output=True, text=True).stdout.strip()


def run_drift(docs, src):
    return subprocess.run(
        [sys.executable, str(TOOLS / "drift.py"), str(docs), str(src)],
        capture_output=True, text=True,
    )


def page(docs, fm):
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "p.md").write_text(f"---\ntitle: T\ntype: model\nstatus: active\n{fm}---\n# T\n")


def make_repo(srcroot, name="myrepo"):
    repo = srcroot / name
    repo.mkdir(parents=True)
    git(repo, "init", "-b", "main")
    (repo / "a.txt").write_text("v1")
    git(repo, "add", "."); git(repo, "commit", "-m", "first")
    return repo


def test_clean_then_stale(tmp_path):
    src = tmp_path / "src"
    repo = make_repo(src)
    sha = head_sha(repo)
    docs = tmp_path / "docs"
    page(docs, f"sources:\n  - repo: myrepo\n    branch: main\n    sha: {sha}\n    committed: 2026-01-01\n")
    r = run_drift(docs, src)
    assert "0 stale" in r.stdout, r.stdout
    # a new commit makes the page stale
    (repo / "a.txt").write_text("v2")
    git(repo, "add", "."); git(repo, "commit", "-m", "second")
    r = run_drift(docs, src)
    assert "STALE" in r.stdout and "1 stale" in r.stdout, r.stdout


def test_missing_branch_is_problem(tmp_path):
    src = tmp_path / "src"
    make_repo(src)
    docs = tmp_path / "docs"
    page(docs, "sources:\n  - repo: myrepo\n    branch: nope\n    sha: deadbeef\n    committed: 2026-01-01\n")
    r = run_drift(docs, src)
    assert "PROBLEM" in r.stdout, r.stdout


def test_no_clone_skips(tmp_path):
    docs = tmp_path / "docs"
    page(docs, "sources:\n  - repo: ghost\n    branch: main\n    sha: x\n    committed: 2026-01-01\n")
    r = run_drift(docs, tmp_path / "empty")
    assert "no clone" in r.stdout and "0 stale" in r.stdout, r.stdout


def test_string_paths_does_not_crash(tmp_path):
    src = tmp_path / "src"
    repo = make_repo(src)
    sha = head_sha(repo)
    docs = tmp_path / "docs"
    # paths given as a scalar string (not a list) must be tolerated
    page(docs, f"sources:\n  - repo: myrepo\n    branch: main\n    sha: {sha}\n"
               f"    committed: 2026-01-01\n    paths: a.txt\n")
    r = run_drift(docs, src)
    assert r.returncode == 0 and "0 stale" in r.stdout, r.stdout
