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
changes**. The mechanism:

1. Each page records, in its `sources` frontmatter, the `repo` / `branch` / `sha` /
   `committed` it was last verified against (see `CONVENTIONS.md` → Provenance).
2. To find drift, per source: fetch the canonical branch, then diff —
   `git log <sha>..origin/<branch> -- <paths>` when the sha is still reachable, or
   `git log --since=<committed> origin/<branch> -- <paths>` when it was rewritten
   away (squash / rebase / force-push). A non-empty diff means the page is stale.
3. Stale pages become **`DOC-VERIFY`** entries; the drift audit
   (`confidence-and-freshness.md`) works them down, re-verifying and re-stamping
   `sources` + confidence + `last_reviewed`.

This is the concrete form of "keep the docs up to date by feeding changes back in."
Until a change-feed is wired, the time-based drift audit is the fallback — it finds
the same drift, just less precisely.

## What this is not

Not a mandate to mirror product docs or tickets into the site. The goal is a
docs base that is **code-true, why-aware, and self-healing** — secondary sources
serve the first two; the change-feed serves the third.
