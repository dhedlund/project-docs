# Stewardship

The authority on **what this documentation effort covers, how it decides, and
where its ground truth comes from**. Where the process docs say *how* to work, the
stewardship docs say *what's in scope* and *what counts as true*. They outlive any
single page or pass.

These are **product-specific** and are written/filled during the
[new-project bootstrap](../process/new-project-bootstrap.md).

## Layout

**Generic** (ship with the scaffold; apply to every product):

- **`scope-and-completeness.md`** — the per-layer "documented enough" bar and the
  never-done maintenance posture.
- **`confidence-and-freshness.md`** — the `reviewed_confidence` scale, staleness,
  and audit cadence.
- **`enrichment-and-currency.md`** — how product docs / tickets / git history fold
  in (link, don't merge) and how source changes re-enter the loop.

**Product-specific** (written during the bootstrap):

- **`product.md`** — what this product is, its domains, the repositories that make
  it up, and the documentation scope and explicit non-goals.
- **`source-of-truth.md`** — the load-bearing axis. How agents reach the source
  code (the code-access model), the provenance/ref convention, and the rule that
  **code-derived facts outrank product docs and tickets**.

Add further axis docs only when an axis is genuinely in play.

## How to use these

When a piece of proposed work shows up — document area X, fold in product doc Y,
reconcile a contradiction — the question is "does this map to what this effort has
committed to or declined."

- Aligned with the stated scope → just do it.
- Lands on a stated non-goal → decline; name the reason so the next agent sees it.
- Touches what counts as true → `source-of-truth.md` is the bar: code is ground
  truth; lower-confidence sources are linked, not merged over.
- Maps to nothing here → either routine work (do it) or a scope question the docs
  haven't taken a position on (settle it here, before the work).

## What this is not

Not marketing, not the rendered product docs themselves. Audience is the
maintainer and the agents. If a doc grows past a screen, split it.
