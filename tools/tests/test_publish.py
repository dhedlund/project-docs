"""Smoke tests for tools/publish-to-branch.sh.

Runs the script against a throwaway git repo in a temp dir (never the real repo),
so it's safe and self-contained. Skipped if git/bash aren't available.
"""
import os
import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "tools" / "publish-to-branch.sh"

pytestmark = pytest.mark.skipif(
    shutil.which("git") is None or shutil.which("bash") is None,
    reason="git and bash are required",
)


def _git(repo, *args):
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True
    )


def _seed_repo(repo):
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")
    (repo / "README.md").write_text("seed\n")
    _git(repo, "add", "README.md")
    _git(repo, "commit", "-q", "-m", "seed")


def _run(repo, **env):
    return subprocess.run(
        ["bash", str(SCRIPT)],
        cwd=repo,
        env={**os.environ, **env},
        capture_output=True,
        text=True,
    )


def test_commits_site_to_branch(tmp_path):
    repo = tmp_path / "repo"
    _seed_repo(repo)
    site = repo / "site"
    (site / "assets").mkdir(parents=True)
    (site / "index.html").write_text("<h1>hi</h1>\n")
    (site / "assets" / "app.js").write_text("// x\n")

    r = _run(repo, SITE="site", BRANCH="__pubtest__")
    assert r.returncode == 0, r.stderr

    # The branch holds the site at its root, with .nojekyll added.
    files = _git(repo, "ls-tree", "-r", "--name-only", "__pubtest__").stdout.split()
    assert "index.html" in files
    assert ".nojekyll" in files
    assert "assets/app.js" in files

    # Working tree is untouched — still on the original branch.
    head = _git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    assert head in ("main", "master")

    # A second run chains onto the branch (parent = previous commit).
    r2 = _run(repo, SITE="site", BRANCH="__pubtest__")
    assert r2.returncode == 0, r2.stderr
    count = _git(repo, "rev-list", "--count", "__pubtest__").stdout.strip()
    assert count == "2"


def test_errors_without_built_site(tmp_path):
    repo = tmp_path / "repo"
    _seed_repo(repo)
    r = _run(repo, SITE="site", BRANCH="__pubtest__")
    assert r.returncode != 0
    assert "no built site" in (r.stderr + r.stdout).lower()
