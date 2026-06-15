#!/usr/bin/env bash
#
# Publish the built example site to a GitHub Pages branch — manually, never in CI.
#
# The build is done by `make publish-example` (hermetic, in the toolkit image);
# THIS script runs on the host so it uses your normal git credentials — they never
# enter the container. It commits the built site to an orphan branch using pure git
# plumbing (a temporary index + a working-tree pointed at the site dir), so your
# working tree and `main` are never touched.
#
# Usage:
#   tools/gh-publish-example.sh [REMOTE] [BRANCH]
#   REMOTE=gh BRANCH=gh-pages tools/gh-publish-example.sh
# Defaults: REMOTE=origin, BRANCH=gh-pages, SITE=example/site
set -euo pipefail

REMOTE="${1:-${REMOTE:-origin}}"
BRANCH="${2:-${BRANCH:-gh-pages}}"
SITE="${SITE:-example/site}"

cd "$(git rev-parse --show-toplevel)"

if [ ! -f "$SITE/index.html" ]; then
  echo "error: no built site at '$SITE'. Run 'make publish-example' (it builds first)." >&2
  exit 1
fi

if ! git remote get-url "$REMOTE" >/dev/null 2>&1; then
  echo "error: git remote '$REMOTE' not found. Add it, or set REMOTE (e.g. REMOTE=gh)." >&2
  echo "       remotes: $(git remote | paste -sd' ' -)" >&2
  exit 1
fi

# GitHub Pages would otherwise run Jekyll and drop files; opt out.
touch "$SITE/.nojekyll"

# Build a tree from the site dir via a throwaway index (force past .gitignore).
TMP_INDEX="$(mktemp)"
trap 'rm -f "$TMP_INDEX"' EXIT
GIT_INDEX_FILE="$TMP_INDEX" git --work-tree="$SITE" add -A -f
TREE="$(GIT_INDEX_FILE="$TMP_INDEX" git --work-tree="$SITE" write-tree)"

MSG="Deploy example docs ($(git rev-parse --short HEAD))"
if PARENT="$(git rev-parse --verify -q "refs/heads/$BRANCH")"; then
  COMMIT="$(git commit-tree "$TREE" -p "$PARENT" -m "$MSG")"
else
  echo "Creating orphan branch '$BRANCH'."
  COMMIT="$(git commit-tree "$TREE" -m "$MSG")"
fi
git update-ref "refs/heads/$BRANCH" "$COMMIT"

echo "Local '$BRANCH' updated -> $COMMIT"
git push "$REMOTE" "$BRANCH"
echo
echo "Pushed to $REMOTE/$BRANCH. If this is the first deploy, enable it once at:"
echo "  GitHub -> Settings -> Pages -> Source: Deploy from a branch -> $BRANCH / (root)"
