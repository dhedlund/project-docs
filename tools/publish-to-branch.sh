#!/usr/bin/env bash
#
# Commit a built docs site to a local branch (default gh-pages) — locally only.
# Pushing is a SEPARATE step you run yourself: `git push <remote> <branch>`.
#
# This runs on the host so it uses your normal git setup; nothing here touches your
# working tree or current branch. It uses pure git plumbing (a temporary index +
# commit-tree), creating the branch as an orphan the first time.
#
# Usage:
#   tools/publish-to-branch.sh [BRANCH]
#   BRANCH=docs-site SITE=site tools/publish-to-branch.sh
# Defaults: BRANCH=gh-pages, SITE=site  (the Makefiles build first and pass SITE).
set -euo pipefail

BRANCH="${1:-${BRANCH:-gh-pages}}"
SITE="${SITE:-site}"

cd "$(git rev-parse --show-toplevel)"

if [ ! -f "$SITE/index.html" ]; then
  echo "error: no built site at '$SITE'. Build the docs first (e.g. 'make build')." >&2
  exit 1
fi

# GitHub Pages would otherwise run Jekyll and drop files; opt out.
touch "$SITE/.nojekyll"

# Build a tree from the site dir via a throwaway index (force past .gitignore).
# Use a fresh path, not mktemp's empty file — git rejects an empty index.
TMP_INDEX="$(mktemp -u)"
trap 'rm -f "$TMP_INDEX"' EXIT
GIT_INDEX_FILE="$TMP_INDEX" git --work-tree="$SITE" add -A -f
TREE="$(GIT_INDEX_FILE="$TMP_INDEX" git --work-tree="$SITE" write-tree)"

MSG="Publish docs ($(git rev-parse --short HEAD))"
if PARENT="$(git rev-parse --verify -q "refs/heads/$BRANCH")"; then
  COMMIT="$(git commit-tree "$TREE" -p "$PARENT" -m "$MSG")"
else
  echo "Creating orphan branch '$BRANCH'."
  COMMIT="$(git commit-tree "$TREE" -m "$MSG")"
fi
git update-ref "refs/heads/$BRANCH" "$COMMIT"

echo "Committed the site to local branch '$BRANCH' ($COMMIT)."
echo
echo "Next steps (done separately, with your own remote):"
echo "  git push <remote> $BRANCH"
echo "  then once: GitHub -> Settings -> Pages -> Deploy from a branch -> $BRANCH / (root)"
