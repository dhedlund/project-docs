# Scope & completeness

What "documented enough" means, and why this effort is never truly finished.

## What "covered" means (structural, not a number)

A thing is **covered** when it has a non-stub page that meets the
`audit-checklist.md` bar for its type:

- **Service** — black-box page: responsibilities + explicit non-responsibilities,
  interface (a contract or a `CONTRACT` backlog entry), owned models, one key flow.
- **Model** — the depth-ladder page (business view → storage mapping → schema /
  defaults / constraints / relationships, with enforcement marked).
- **Feature** — journey + a UI → API → data walk-through that links down into the
  services and models it touches.
- **Decision** — an ADR exists for each non-obvious choice encountered.

Confidence is **not** the coverage gate — it's a *quality signal* layered on top. A
covered page can still be confidence 60 (accurate but with unverified corners); the
number says where to spend the next pass, not whether the page "counts." See
`confidence-and-freshness.md`.

## Stubs are a legitimate state

Breadth-first beats depth-first early: every in-scope service/model/feature should
have at least a **stub** (so the cross-link graph is real) before anything is
deepened. A stub is honest progress, not a failure — `status: stub`, low confidence,
and a `DOC-DEEPEN` backlog entry. Stubs aren't "covered" yet, but they make the map
whole.

## "Covered" vs "in scope" vs "out"

- **In scope** — listed in `product.md`. Everything in scope is owed at least a
  stub, then deepening.
- **Out of scope** — named explicitly in `product.md` / `backlog.md` so a cold
  reader sees the decline. Out-of-scope is **permanent and principled**, not "later."
- **Not yet done** — in scope, engineering-bounded, has a backlog entry.

**Anti-pattern:** treating "out of scope" as code for "we'll get to it." If it's
genuinely deferred, it's a backlog entry with a reason, not an OUT entry.

## Never-done, and when to stop

Documentation of a *living* system is perpetual, so a fully-"done" state is an
ideal, not a milestone you reach and hold — every source change re-opens work (see
`enrichment-and-currency.md`). In practice a session **stops** when:

- it has spent the **iteration budget the user set** ("work the next 10 items," "for
  an hour"), or
- if no budget was set, when it **runs out of useful work** — the backlog is empty
  *and* the research threads turn up nothing actionable for a round or two *and* no
  source has changed since the last drift run (see `loop.md`'s stopping rule).

Don't manufacture make-work to avoid stopping, and don't claim a false "done." A
quiet steady state (covered, no open `FINDING`s, threads dry) is a fine place to end
a session; the next source change brings the next session's work.

## Prioritizing maintenance

Once coverage is high the work shifts from authoring to **drift maintenance**.
Prioritize by impact, not just recency: re-verify the pages that readers and other
services depend on most first, and accept some bounded staleness on peripheral pages
(a visible stale badge is fine — better than burning the budget keeping a deprecated
corner perfectly fresh). An optional `tier: core | supporting | peripheral` in
frontmatter makes this explicit once a product is large enough to need it.
