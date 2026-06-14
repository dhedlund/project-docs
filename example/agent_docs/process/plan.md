# Beacon plan

> **Fictional reference** — a plan mid-flight, after bootstrap and a few passes.

The rolling plan: *Now* plus the immediately-next item. The durable queue lives in
`backlog.md`. Target ≤ ~200 lines. See `../../../agent_docs/process/loop.md` for how
to update this.

## Where Beacon is

Deepened so far: `billing-service`, `messaging-service`, the `Subscription`,
`Delivery event`, and `Organization` models, the `Plan upgrade` and `Suspend an
organization` features, and ADRs 0001 (superseded) + 0002. `accounts-service` and
`Plan` exist as **stubs**. `Delivery event` is now flagged `[stale]` (last reviewed
2026-03-10) by `make report`.

## Now

**Deepen `accounts-service` from stub to a full black-box page (+ its contract), and
add the `User` model it owns.** Definition of done: service page meets the
`audit-checklist.md` service checklist (responsibilities, a contract or a `CONTRACT`
backlog entry, owned models, one flow diagram); `User` model meets the model
checklist with provenance; both link bidirectionally with `Organization`. Source:
`beacon-accounts`.

## Up next

- Deepen the `Plan` stub, then author the `Invoice` model (referenced by
  `Subscription`).

## Last completed

Added the `Suspend an organization` feature and ADR 0002 (delivery-event schema
validator), superseding ADR 0001. Git log is the canonical history.

## Recent discoveries

(Empty per the loop — discoveries are distilled into the backlog / page callouts.)

## Open questions

- Document `beacon-web` UI components now, or after backend coverage is complete?
  (Leaning: after, so features link down into settled service/model pages.)
