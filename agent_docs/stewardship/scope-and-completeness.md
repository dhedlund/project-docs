# Scope & completeness

What "documented enough" means, and why this effort is never truly finished. The
loop's anti-coast logic ("done fires only when coverage is at target") depends on
the target being defined — this is that definition.

## The per-layer completeness bar

A thing is "covered" when its page meets the `audit-checklist.md` bar for its type
**and** clears the confidence threshold (see `confidence-and-freshness.md`):

- **Service** — black-box page: responsibilities + explicit non-responsibilities,
  interface (a contract or a `CONTRACT` backlog entry), owned models, one key flow.
- **Model** — the depth-ladder page (business view → storage mapping → schema /
  defaults / constraints / relationships, with enforcement marked).
- **Feature** — journey + a UI → API → data walk-through that links down into the
  services and models it touches.
- **Decision** — an ADR exists for each non-obvious choice encountered while
  documenting.

## Stubs are a legitimate state

Breadth-first beats depth-first early: every in-scope service/model/feature should
have at least a **stub** (so the cross-link graph is real) before anything is
deepened. A stub is honest progress, not a failure — it carries `status: stub`, low
confidence, and a `DOC-DEEPEN` backlog entry.

## "Covered" vs "in scope" vs "out"

- **In scope** — listed in `product.md`. Everything in scope is owed at least a
  stub, then deepening to the confidence threshold.
- **Out of scope** — named explicitly in `product.md` / `backlog.md` so a cold
  reader sees the decline. Out-of-scope is **permanent and principled**, not
  "later."
- **Not yet done** — in scope, engineering-bounded, has a backlog entry.

**Anti-pattern:** treating "out of scope" as code for "we'll get to it." If it's
genuinely deferred, it's a backlog entry with a reason, not an OUT entry.

## Never-done: the maintenance steady state

Documentation of a *living* system is perpetual. "Done" is momentary — it means
coverage is at target, no `FINDING`s are open, and the research threads are
quiescent — and it **re-opens the moment the source changes** (see
`enrichment-and-currency.md` for the change-feed → `DOC-VERIFY` mechanism). Once
coverage is high, the work shifts from authoring to **drift maintenance**; that's
expected, not a sign the project stalled.

## Judging a milestone

A domain (or the whole product) is "documented" when every in-scope
service/model/feature in it is at or above the confidence threshold with no open
`FINDING`s. Use that to decide when to broaden scope vs. keep deepening.
