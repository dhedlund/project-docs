# Enrichment & currency

How non-code sources fold in over time, and how the docs stay current as the system
changes. `source-of-truth.md` establishes *what counts as true* (code); this doc is
about everything that orbits it — the "why," and the feedback loop that fights rot.

## Enrichment: secondary sources (the "why")

Product docs, ticket histories (JIRA), and git history are **lower-confidence
context**, valuable for *why* the system is the way it is — domain reasoning,
history, intent — not for *what* it does.

**Rule: link, don't merge.** Secondary sources are linked and cited, never written
over a code-derived fact. Concretely:

- A product doc or ticket explains intent → cite it from the relevant page /ADR; it
  raises understanding, not the page's authority over facts.
- A secondary source **contradicts the code** → a `Discrepancy` callout on the page
  plus a `FINDING` backlog entry. The code-derived fact stands; the conflict is
  surfaced, not silently resolved.
- The "why" layer: link tickets/commits to the entities and ADRs they explain, so
  the rationale is reachable from the thing it explains.

**Sequencing.** Build from code first (high confidence), enrich later. Never block
a code-derived page on missing product docs or tickets — enrichment is additive.

**Don't bulk-ingest.** Secondary docs are provenance-tagged annotations, not content
to import wholesale (they drift worse than code and carry no enforcement).

## Currency: the feedback loop that fights rot

The docs track a living system, so the loop must **re-open when the source
changes**. The mechanism, made concrete:

1. Each page records, in its `sources` frontmatter, the `repo` / `branch` / `sha` /
   `committed` (+ optional `paths`) it was last verified against (see
   `CONVENTIONS.md` → Provenance). `make check` *requires* this on code-derived
   pages, so provenance coverage isn't optional.
2. **`make drift SRC=<code>`** (the `docs-drift` tool) diffs each page's `sources`
   against the clones: `git log <sha>..<branch> -- <paths>` when the sha is
   reachable, else `git log --since=<committed> <branch> -- <paths>` when it was
   rewritten away. Git/branch/sha errors are reported, never silently swallowed.
3. **It runs automatically, not on a whim.** The loop runs `make drift` + `make
   report` at **session start** (`loop.md` step 1), and a scheduled CI job can run
   it without an agent (`.github/workflows/docs-ci.yml.example`). The output is filed
   as `DOC-VERIFY` before the session proceeds — that's the re-entry path.
4. The drift audit (`confidence-and-freshness.md`) then works those entries down,
   re-verifying against current source and re-stamping `sources` + confidence +
   `last_reviewed`.

**The `--since` fallback is approximate.** After a rebase/squash, commit dates
shift, so it can over-report — `docs-drift` marks those `APPROX`. Treat an APPROX
hit as "re-anchor the `sha` (re-verify only if the content actually changed),"
not a full re-read. A precise commit/ticket **change-feed** is optional automation
on top; until it's wired, session-start `make drift` is the dependable path.

## What this is not

Not a mandate to mirror product docs or tickets into the site. The goal is a
docs base that is **code-true, why-aware, and self-healing** — secondary sources
serve the first two; the change-feed serves the third.
