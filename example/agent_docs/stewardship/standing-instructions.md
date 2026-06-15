# Standing instructions (Beacon)

> **Fictional reference** — durable directives the user has given over time. The loop
> reads this at session start, so "keep working the backlog" carries this guidance
> without the user re-stating it. Keep it short, **dated**, and curated — prune what's
> no longer true (same discipline as the plan/backlog).

Cross-cutting directives, preferences, and context that don't belong in `product.md`
(identity/scope), `source-of-truth.md` (access), or `backlog.md` (the work queue).

## Directives & preferences

- **2026-06-10** — Prioritise the **billing** domain; it carries most of the support
  load and churn risk. Deepen it before adding breadth elsewhere.
- **2026-06-10** — Treat **`beacon-web`** as the authority for UI-visible behaviour
  when it disagrees with an older service; record the discrepancy, don't silently pick
  a side.
- **2026-06-12** — The **legacy SMS channel** is being retired — keep it documented
  as `deprecated`, don't invest in deepening it.
- **2026-06-14** — When citing tickets, prefer the **epic** over individual issues
  where one exists; epics are the more stable reference.

## Context worth remembering

- Beacon ships **weekly** (Thursdays); "recent" drift means roughly the last one or
  two releases.
- The read-only clones are refreshed nightly by the maintainer — if drift looks
  impossibly large, the clone may simply be ahead of the last-reviewed sha.
